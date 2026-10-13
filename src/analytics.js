/**
 * Vercel Web Analytics initialization
 * Automatically tracks page views and enables custom event tracking
 */
import { inject } from '@vercel/analytics';

// Initialize Vercel Web Analytics
inject({
  mode: 'auto', // Automatically detect development/production
  debug: false  // Set to true for debugging in development
});
