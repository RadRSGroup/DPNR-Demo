"""
GDPR-Compliant Authentication and Data Protection System
Implements JWT auth with encryption, audit logging, and right to erasure
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
import secrets
import jwt
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json
import asyncio
import asyncpg
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

logger = logging.getLogger(__name__)

@dataclass
class UserConsent:
    """GDPR consent tracking"""
    data_processing: bool
    marketing_emails: bool
    analytics_tracking: bool
    consent_timestamp: datetime
    ip_address: str
    consent_version: str = "1.0"

@dataclass
class AuthToken:
    """JWT token with GDPR metadata"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    consent_status: Dict[str, bool] = None

class GDPRCompliantAuth:
    """
    GDPR-compliant authentication system with:
    - JWT tokens with short expiry
    - Data encryption at rest
    - Audit logging
    - Right to erasure
    - Consent management
    """
    
    def __init__(
        self,
        secret_key: str,
        database_url: str,
        token_expiry_minutes: int = 60,
        refresh_token_expiry_days: int = 30
    ):
        self.secret_key = secret_key
        self.database_url = database_url
        self.token_expiry = timedelta(minutes=token_expiry_minutes)
        self.refresh_expiry = timedelta(days=refresh_token_expiry_days)
        self.security = HTTPBearer()
        
        # Generate encryption key from secret
        self._init_encryption()
        
    def _init_encryption(self):
        """Initialize Fernet encryption for sensitive data"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'stable_salt',  # In production, use random salt stored securely
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.secret_key.encode()))
        self.cipher = Fernet(key)
    
    def _encrypt_pii(self, data: str) -> str:
        """Encrypt personally identifiable information"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def _decrypt_pii(self, encrypted_data: str) -> str:
        """Decrypt personally identifiable information"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
    
    async def create_user(
        self,
        email: str,
        password: str,
        consent: UserConsent,
        db_pool: asyncpg.Pool
    ) -> Dict[str, Any]:
        """
        Create user with GDPR compliance:
        - Encrypted PII storage
        - Consent tracking
        - Audit logging
        """
        
        # Validate consent
        if not consent.data_processing:
            raise HTTPException(
                status_code=400,
                detail="Data processing consent is required"
            )
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        # Encrypt email (PII)
        encrypted_email = self._encrypt_pii(email)
        
        # Generate user ID
        user_id = secrets.token_urlsafe(16)
        
        async with db_pool.acquire() as conn:
            try:
                # Create user record
                await conn.execute("""
                    INSERT INTO users (
                        user_id, encrypted_email, email_hash, password_hash,
                        created_at, last_login, is_active
                    ) VALUES ($1, $2, $3, $4, $5, NULL, true)
                """, 
                    user_id,
                    encrypted_email,
                    self._hash_email(email),  # For lookups without decryption
                    password_hash,
                    datetime.utcnow()
                )
                
                # Store consent record
                await conn.execute("""
                    INSERT INTO user_consent (
                        user_id, data_processing, marketing_emails,
                        analytics_tracking, consent_timestamp, ip_address,
                        consent_version
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                """,
                    user_id,
                    consent.data_processing,
                    consent.marketing_emails,
                    consent.analytics_tracking,
                    consent.consent_timestamp,
                    self._encrypt_pii(consent.ip_address),
                    consent.consent_version
                )
                
                # Audit log
                await self._audit_log(
                    conn, user_id, "user_created", 
                    {"consent_given": True, "consent_version": consent.consent_version}
                )
                
                return {
                    "user_id": user_id,
                    "message": "User created successfully",
                    "consent_recorded": True
                }
                
            except asyncpg.UniqueViolationError:
                raise HTTPException(status_code=409, detail="User already exists")
    
    def _hash_email(self, email: str) -> str:
        """Create searchable hash of email"""
        return bcrypt.hashpw(email.lower().encode(), bcrypt.gensalt()).decode()
    
    async def authenticate(
        self,
        email: str,
        password: str,
        db_pool: asyncpg.Pool
    ) -> AuthToken:
        """Authenticate user and generate JWT tokens"""
        
        email_hash = self._hash_email(email)
        
        async with db_pool.acquire() as conn:
            # Find user by email hash
            user = await conn.fetchrow("""
                SELECT user_id, password_hash, is_active, encrypted_email
                FROM users
                WHERE email_hash = $1
            """, email_hash)
            
            if not user or not user['is_active']:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
            # Verify password
            if not bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
                await self._audit_log(
                    conn, user['user_id'], "failed_login",
                    {"reason": "invalid_password"}
                )
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
            # Get consent status
            consent = await conn.fetchrow("""
                SELECT data_processing, marketing_emails, analytics_tracking
                FROM user_consent
                WHERE user_id = $1
                ORDER BY consent_timestamp DESC
                LIMIT 1
            """, user['user_id'])
            
            # Generate tokens
            access_token = self._generate_token(
                user['user_id'],
                token_type="access",
                expiry=self.token_expiry
            )
            
            refresh_token = self._generate_token(
                user['user_id'],
                token_type="refresh",
                expiry=self.refresh_expiry
            )
            
            # Update last login
            await conn.execute("""
                UPDATE users SET last_login = $1 WHERE user_id = $2
            """, datetime.utcnow(), user['user_id'])
            
            # Audit log
            await self._audit_log(
                conn, user['user_id'], "successful_login",
                {"ip_address": "masked_for_privacy"}
            )
            
            return AuthToken(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=int(self.token_expiry.total_seconds()),
                consent_status={
                    "data_processing": consent['data_processing'],
                    "marketing_emails": consent['marketing_emails'],
                    "analytics_tracking": consent['analytics_tracking']
                } if consent else None
            )
    
    def _generate_token(self, user_id: str, token_type: str, expiry: timedelta) -> str:
        """Generate JWT token"""
        payload = {
            "user_id": user_id,
            "type": token_type,
            "exp": datetime.utcnow() + expiry,
            "iat": datetime.utcnow(),
            "jti": secrets.token_urlsafe(16)  # Unique token ID for revocation
        }
        
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
    
    async def verify_token(
        self,
        credentials: HTTPAuthorizationCredentials,
        db_pool: asyncpg.Pool
    ) -> Dict[str, Any]:
        """Verify JWT token and return user info"""
        
        token = credentials.credentials
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            
            # Check if token is revoked
            async with db_pool.acquire() as conn:
                revoked = await conn.fetchval("""
                    SELECT EXISTS(
                        SELECT 1 FROM revoked_tokens 
                        WHERE token_jti = $1
                    )
                """, payload['jti'])
                
                if revoked:
                    raise HTTPException(status_code=401, detail="Token has been revoked")
                
                # Check if user is still active
                is_active = await conn.fetchval("""
                    SELECT is_active FROM users WHERE user_id = $1
                """, payload['user_id'])
                
                if not is_active:
                    raise HTTPException(status_code=401, detail="User account is inactive")
            
            return {
                "user_id": payload['user_id'],
                "token_type": payload['type'],
                "jti": payload['jti']
            }
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    async def refresh_access_token(
        self,
        refresh_token: str,
        db_pool: asyncpg.Pool
    ) -> AuthToken:
        """Generate new access token from refresh token"""
        
        try:
            payload = jwt.decode(refresh_token, self.secret_key, algorithms=["HS256"])
            
            if payload['type'] != 'refresh':
                raise HTTPException(status_code=401, detail="Invalid token type")
            
            # Generate new access token
            access_token = self._generate_token(
                payload['user_id'],
                token_type="access",
                expiry=self.token_expiry
            )
            
            return AuthToken(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=int(self.token_expiry.total_seconds())
            )
            
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    async def revoke_token(self, token_jti: str, db_pool: asyncpg.Pool):
        """Revoke a token by adding to revocation list"""
        async with db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO revoked_tokens (token_jti, revoked_at)
                VALUES ($1, $2)
            """, token_jti, datetime.utcnow())
    
    async def delete_user_data(self, user_id: str, db_pool: asyncpg.Pool) -> Dict[str, Any]:
        """
        GDPR Right to Erasure implementation
        Anonymizes user data while maintaining referential integrity
        """
        
        async with db_pool.acquire() as conn:
            async with conn.transaction():
                # Anonymize user record
                anonymous_id = f"deleted_user_{secrets.token_urlsafe(8)}"
                
                await conn.execute("""
                    UPDATE users 
                    SET encrypted_email = $1,
                        email_hash = $2,
                        password_hash = $3,
                        is_active = false,
                        deleted_at = $4
                    WHERE user_id = $5
                """,
                    self._encrypt_pii(anonymous_id),
                    "DELETED",
                    "DELETED",
                    datetime.utcnow(),
                    user_id
                )
                
                # Remove consent records
                await conn.execute("""
                    DELETE FROM user_consent WHERE user_id = $1
                """, user_id)
                
                # Anonymize assessment data
                await conn.execute("""
                    UPDATE assessments
                    SET user_metadata = '{"anonymized": true}'::jsonb
                    WHERE user_id = $1
                """, user_id)
                
                # Audit log
                await self._audit_log(
                    conn, user_id, "data_deletion_requested",
                    {"anonymized": True, "timestamp": datetime.utcnow().isoformat()}
                )
                
                return {
                    "status": "success",
                    "message": "User data has been anonymized",
                    "deletion_timestamp": datetime.utcnow().isoformat()
                }
    
    async def export_user_data(self, user_id: str, db_pool: asyncpg.Pool) -> Dict[str, Any]:
        """
        GDPR Right to Data Portability
        Export all user data in machine-readable format
        """
        
        async with db_pool.acquire() as conn:
            # Fetch user data
            user_data = await conn.fetchrow("""
                SELECT encrypted_email, created_at, last_login
                FROM users WHERE user_id = $1
            """, user_id)
            
            # Fetch assessments
            assessments = await conn.fetch("""
                SELECT assessment_type, created_at, results
                FROM assessments 
                WHERE user_id = $1
                ORDER BY created_at DESC
            """, user_id)
            
            # Fetch consent history
            consent_history = await conn.fetch("""
                SELECT * FROM user_consent
                WHERE user_id = $1
                ORDER BY consent_timestamp DESC
            """, user_id)
            
            # Decrypt PII for export
            decrypted_email = self._decrypt_pii(user_data['encrypted_email'])
            
            return {
                "user_profile": {
                    "email": decrypted_email,
                    "created_at": user_data['created_at'].isoformat(),
                    "last_login": user_data['last_login'].isoformat() if user_data['last_login'] else None
                },
                "assessments": [
                    {
                        "type": a['assessment_type'],
                        "date": a['created_at'].isoformat(),
                        "results": a['results']
                    }
                    for a in assessments
                ],
                "consent_history": [
                    {
                        "data_processing": c['data_processing'],
                        "marketing_emails": c['marketing_emails'],
                        "analytics_tracking": c['analytics_tracking'],
                        "timestamp": c['consent_timestamp'].isoformat()
                    }
                    for c in consent_history
                ],
                "export_timestamp": datetime.utcnow().isoformat()
            }
    
    async def _audit_log(
        self,
        conn: asyncpg.Connection,
        user_id: str,
        action: str,
        metadata: Dict[str, Any]
    ):
        """Create audit log entry for GDPR compliance"""
        await conn.execute("""
            INSERT INTO audit_logs (user_id, action, metadata, timestamp)
            VALUES ($1, $2, $3, $4)
        """, user_id, action, json.dumps(metadata), datetime.utcnow())

# Database schema for GDPR compliance
GDPR_SCHEMA = """
-- Users table with encrypted PII
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(32) PRIMARY KEY,
    encrypted_email TEXT NOT NULL,
    email_hash VARCHAR(128) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    deleted_at TIMESTAMP,
    UNIQUE(email_hash)
);

-- Consent tracking
CREATE TABLE IF NOT EXISTS user_consent (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(32) REFERENCES users(user_id),
    data_processing BOOLEAN NOT NULL,
    marketing_emails BOOLEAN NOT NULL,
    analytics_tracking BOOLEAN NOT NULL,
    consent_timestamp TIMESTAMP NOT NULL,
    ip_address TEXT NOT NULL,
    consent_version VARCHAR(10) NOT NULL,
    INDEX idx_user_consent (user_id, consent_timestamp DESC)
);

-- Token revocation
CREATE TABLE IF NOT EXISTS revoked_tokens (
    token_jti VARCHAR(32) PRIMARY KEY,
    revoked_at TIMESTAMP NOT NULL,
    INDEX idx_revoked_at (revoked_at)
);

-- Audit logs for compliance
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(32),
    action VARCHAR(50) NOT NULL,
    metadata JSONB,
    timestamp TIMESTAMP NOT NULL,
    INDEX idx_audit_user (user_id, timestamp DESC),
    INDEX idx_audit_action (action, timestamp DESC)
);

-- Data retention policy (auto-delete old audit logs)
CREATE OR REPLACE FUNCTION delete_old_audit_logs() RETURNS void AS $$
BEGIN
    DELETE FROM audit_logs WHERE timestamp < NOW() - INTERVAL '2 years';
    DELETE FROM revoked_tokens WHERE revoked_at < NOW() - INTERVAL '90 days';
END;
$$ LANGUAGE plpgsql;
"""