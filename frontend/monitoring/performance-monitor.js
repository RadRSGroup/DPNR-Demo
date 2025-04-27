// Simple performance monitoring utility

const metrics = {};

export function recordMetric(name, value) {
  metrics[name] = value;
}

export function incrementMetric(name, inc = 1) {
  metrics[name] = (metrics[name] || 0) + inc;
}

export function getMetrics() {
  return { ...metrics };
}

export function logMetrics() {
  // Output metrics in a readable table format
  // eslint-disable-next-line no-console
  console.table(metrics);
} 