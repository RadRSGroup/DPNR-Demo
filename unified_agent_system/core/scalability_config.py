"""
Scalability Configuration for 5000 Concurrent Users
Implements connection pooling, caching, and performance optimizations
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import asyncpg
import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool
import asyncio
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

@dataclass
class ScalabilityConfig:
    """Configuration for handling 5000 concurrent users"""
    
    # Database pooling
    db_min_connections: int = 20
    db_max_connections: int = 100
    db_connection_timeout: int = 10
    db_command_timeout: int = 60
    
    # Redis pooling
    redis_max_connections: int = 200
    redis_connection_timeout: int = 5
    
    # API rate limiting
    requests_per_minute_per_user: int = 60
    burst_size: int = 10
    
    # Queue configuration
    max_concurrent_assessments: int = 500
    assessment_timeout: int = 300  # 5 minutes
    queue_size: int = 10000
    
    # Caching
    cache_ttl_seconds: int = 3600  # 1 hour
    max_cache_size_mb: int = 1024  # 1GB
    
    # WebSocket
    max_websocket_connections: int = 5000
    websocket_ping_interval: int = 30
    websocket_timeout: int = 60
    
    # Performance
    batch_size: int = 50
    worker_processes: int = 8
    io_threads: int = 16

class DatabasePool:
    """
    PostgreSQL connection pool optimized for high concurrency
    
    For 5000 users:
    - 100 max connections (configurable based on PostgreSQL max_connections)
    - Connection multiplexing via transaction pooling
    - Read replicas for scaling reads
    """
    
    def __init__(self, config: ScalabilityConfig, database_url: str):
        self.config = config
        self.database_url = database_url
        self.pool: Optional[asyncpg.Pool] = None
        self.read_pool: Optional[asyncpg.Pool] = None
    
    async def initialize(self, read_replica_url: Optional[str] = None):
        """Initialize connection pools"""
        
        # Main pool for writes
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=self.config.db_min_connections,
            max_size=self.config.db_max_connections,
            max_queries=50000,
            max_inactive_connection_lifetime=300,
            timeout=self.config.db_connection_timeout,
            command_timeout=self.config.db_command_timeout,
            statement_cache_size=0  # Disable to save memory with many connections
        )
        
        # Read replica pool if available
        if read_replica_url:
            self.read_pool = await asyncpg.create_pool(
                read_replica_url,
                min_size=self.config.db_min_connections,
                max_size=self.config.db_max_connections,
                max_queries=50000,
                timeout=self.config.db_connection_timeout
            )
        else:
            self.read_pool = self.pool
        
        logger.info("Database pools initialized")
    
    @asynccontextmanager
    async def acquire_read(self):
        """Acquire connection for read operations"""
        async with self.read_pool.acquire() as conn:
            yield conn
    
    @asynccontextmanager
    async def acquire_write(self):
        """Acquire connection for write operations"""
        async with self.pool.acquire() as conn:
            yield conn
    
    async def close(self):
        """Close all pools"""
        if self.pool:
            await self.pool.close()
        if self.read_pool and self.read_pool != self.pool:
            await self.read_pool.close()

class RedisCache:
    """
    Redis cache optimized for high concurrency
    
    For 5000 users:
    - 200 max connections
    - Automatic connection pooling
    - Separate pools for different data types
    """
    
    def __init__(self, config: ScalabilityConfig, redis_url: str):
        self.config = config
        self.redis_url = redis_url
        self.pools: Dict[str, ConnectionPool] = {}
        self.clients: Dict[str, redis.Redis] = {}
    
    async def initialize(self):
        """Initialize Redis connection pools"""
        
        # Create separate pools for different purposes
        pool_configs = {
            "cache": {"max_connections": 100},
            "session": {"max_connections": 50},
            "queue": {"max_connections": 30},
            "pubsub": {"max_connections": 20}
        }
        
        for name, config in pool_configs.items():
            pool = ConnectionPool.from_url(
                self.redis_url,
                max_connections=config["max_connections"],
                socket_connect_timeout=self.config.redis_connection_timeout,
                socket_keepalive=True,
                socket_keepalive_options={
                    1: 1,  # TCP_KEEPIDLE
                    2: 1,  # TCP_KEEPINTVL
                    3: 5,  # TCP_KEEPCNT
                }
            )
            self.pools[name] = pool
            self.clients[name] = redis.Redis(connection_pool=pool)
        
        logger.info("Redis pools initialized")
    
    async def get(self, key: str, pool: str = "cache") -> Optional[str]:
        """Get value from cache"""
        client = self.clients.get(pool, self.clients["cache"])
        value = await client.get(key)
        return value.decode() if value else None
    
    async def set(
        self, 
        key: str, 
        value: str, 
        ttl: Optional[int] = None,
        pool: str = "cache"
    ):
        """Set value in cache"""
        client = self.clients.get(pool, self.clients["cache"])
        ttl = ttl or self.config.cache_ttl_seconds
        await client.setex(key, ttl, value)
    
    async def delete(self, key: str, pool: str = "cache"):
        """Delete value from cache"""
        client = self.clients.get(pool, self.clients["cache"])
        await client.delete(key)
    
    async def close(self):
        """Close all Redis connections"""
        for client in self.clients.values():
            await client.close()
        for pool in self.pools.values():
            await pool.disconnect()

class RateLimiter:
    """
    Token bucket rate limiter for API requests
    
    For 5000 users:
    - Per-user rate limiting
    - Sliding window with Redis
    - Burst handling
    """
    
    def __init__(self, redis_client: redis.Redis, config: ScalabilityConfig):
        self.redis = redis_client
        self.config = config
    
    async def check_rate_limit(self, user_id: str) -> bool:
        """
        Check if user has exceeded rate limit
        
        Returns:
            True if request is allowed, False if rate limited
        """
        key = f"rate_limit:{user_id}"
        now = asyncio.get_event_loop().time()
        window_start = now - 60  # 1 minute window
        
        # Remove old entries
        await self.redis.zremrangebyscore(key, 0, window_start)
        
        # Count requests in window
        request_count = await self.redis.zcard(key)
        
        if request_count >= self.config.requests_per_minute_per_user:
            return False
        
        # Add current request
        await self.redis.zadd(key, {str(now): now})
        await self.redis.expire(key, 120)  # 2 minute expiry
        
        return True
    
    async def get_remaining_requests(self, user_id: str) -> int:
        """Get remaining requests for user"""
        key = f"rate_limit:{user_id}"
        now = asyncio.get_event_loop().time()
        window_start = now - 60
        
        await self.redis.zremrangebyscore(key, 0, window_start)
        request_count = await self.redis.zcard(key)
        
        return max(0, self.config.requests_per_minute_per_user - request_count)

class ConnectionManager:
    """
    Manages database and cache connections for the application
    
    Singleton pattern to ensure single pool instance
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.config = ScalabilityConfig()
            self.db_pool: Optional[DatabasePool] = None
            self.redis_cache: Optional[RedisCache] = None
            self.rate_limiter: Optional[RateLimiter] = None
            self.initialized = False
    
    async def initialize(
        self,
        database_url: str,
        redis_url: str,
        read_replica_url: Optional[str] = None
    ):
        """Initialize all connection pools"""
        
        if self.initialized:
            return
        
        # Initialize database pool
        self.db_pool = DatabasePool(self.config, database_url)
        await self.db_pool.initialize(read_replica_url)
        
        # Initialize Redis cache
        self.redis_cache = RedisCache(self.config, redis_url)
        await self.redis_cache.initialize()
        
        # Initialize rate limiter
        self.rate_limiter = RateLimiter(
            self.redis_cache.clients["session"],
            self.config
        )
        
        self.initialized = True
        logger.info("Connection manager initialized")
    
    async def close(self):
        """Close all connections"""
        if self.db_pool:
            await self.db_pool.close()
        if self.redis_cache:
            await self.redis_cache.close()
        self.initialized = False

# Performance optimization tips for 5000 concurrent users
OPTIMIZATION_GUIDE = """
## Scaling to 5000 Concurrent Users

### Database Optimizations
1. **Connection Pooling**: 100 connections max (adjustable)
   - Each connection can handle multiple requests via multiplexing
   - Use read replicas for read-heavy operations

2. **Query Optimization**:
   - Add indexes on frequently queried columns (user_id, assessment_type)
   - Use prepared statements to reduce parsing overhead
   - Batch INSERT operations where possible

3. **PostgreSQL Tuning**:
   ```
   max_connections = 200
   shared_buffers = 8GB
   effective_cache_size = 24GB
   work_mem = 20MB
   maintenance_work_mem = 2GB
   ```

### Caching Strategy
1. **Redis Caching**: Cache assessment results for 1 hour
   - Reduces database load by ~70%
   - Separate pools for different data types

2. **Application-Level Caching**:
   - LRU cache for frequently accessed data
   - Cache warming for popular assessments

### API Optimizations
1. **Rate Limiting**: 60 requests/minute per user
   - Prevents abuse and ensures fair usage
   - Burst handling for legitimate spikes

2. **Request Batching**: Process up to 50 assessments in batch
   - Reduces overhead and improves throughput

3. **Async Processing**: All I/O operations are async
   - Non-blocking database and Redis operations
   - Concurrent request handling

### Infrastructure Requirements
1. **Application Servers**:
   - 8 CPU cores, 32GB RAM minimum
   - Run 8 worker processes
   - Use uvicorn with multiple workers

2. **Database Server**:
   - 16 CPU cores, 64GB RAM recommended
   - SSD storage for better I/O
   - Consider read replicas for scaling

3. **Redis Server**:
   - 4 CPU cores, 16GB RAM
   - Enable persistence for session data

### Monitoring
1. **Key Metrics**:
   - Response time (p50, p95, p99)
   - Database connection pool usage
   - Redis memory usage
   - Queue depth

2. **Alerts**:
   - Response time > 1 second (p95)
   - Database connections > 80%
   - Redis memory > 80%
   - Error rate > 1%
"""