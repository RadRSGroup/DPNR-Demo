export function logError(message, error) {
  // Basic error logger. Extend to send to backend monitoring if needed.
  console.error(`[ERROR] ${message}:`, error);
} 