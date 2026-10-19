import { Pool } from 'pg';

const DATABASE_URL = process.env.DATABASE_URL ?? 'postgresql://bankerchanger:bankerchanger@localhost:5432/bankerchanger';

export const pool = new Pool({ connectionString: DATABASE_URL });
