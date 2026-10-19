import { Pool } from 'pg';

const DATABASE_URL = process.env.DATABASE_URL ?? 'postgresql://bankerchanger:bankerchanger@localhost:5432/bankerchanger';

const parseNumber = (value: string | undefined, defaultValue: number): number => {
  if (value) {
    const num = Number(value);
    if (!isNaN(num) && num > 0) {
      return num;
    }
  }
  return defaultValue;
};

export const pool = new Pool({
  connectionString: DATABASE_URL,
  max: parseNumber(process.env.DB_POOL_MAX, 10),
  idleTimeoutMillis: parseNumber(process.env.DB_POOL_IDLE_TIMEOUT_MS, 30000),
  connectionTimeoutMillis: parseNumber(process.env.DB_POOL_CONNECTION_TIMEOUT_MS, 5000),
});
