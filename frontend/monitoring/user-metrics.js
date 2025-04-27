// User metrics collection utility

const metrics = {};

export function incrementUserMetric(name, inc = 1) {
  metrics[name] = (metrics[name] || 0) + inc;
}

export function recordUserMetric(name, value) {
  metrics[name] = value;
}

export function getUserMetrics() {
  return { ...metrics };
}

export function logUserMetrics() {
  // eslint-disable-next-line no-console
  console.table(metrics);
} 