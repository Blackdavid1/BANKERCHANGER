import express, { Request, Response } from 'express';
import cors from 'cors';
import { getPollerHealth } from './poller';

const app = express();

app.use(cors());
app.use(express.json());

app.get('/health', (req: Request, res: Response) => {
  try {
    const health = getPollerHealth();
    
    // Return 200 if poller is running, 503 if not
    const statusCode = health.isRunning ? 200 : 503;
    
    res.status(statusCode).json({
      success: statusCode === 200,
      status: health.isRunning ? 'healthy' : 'unhealthy',
      poller: {
        isRunning: health.isRunning,
        consecutiveFailures: health.consecutiveFailures,
        lastError: health.lastError,
        lastErrorAt: health.lastErrorAt,
        lastSuccessfulPollAt: health.lastSuccessfulPollAt,
        eventsProcessed: health.eventsProcessed,
      },
    });
  } catch (err: any) {
    res.status(500).json({ 
      success: false, 
      status: 'error',
      error: err.message 
    });
  }
});

export default app;
