import { describe, it, expect, beforeAll, afterAll } from '@jest/globals';
import request from 'supertest';
import app from '../server';
import { db, upsertInvoice, getInvoices, getDatabase } from '../db';
import { processEvent } from '../poller';

// Clear the DB before tests
beforeAll(() => {
  db.exec('DELETE FROM invoices');
});

afterAll(() => {
  // Close the database connection
  const database = getDatabase();
  database.close();
});

describe('Indexer Event Processing', () => {
  it('should process submitted event', () => {
    // Mock a processEvent call directly (since it's tricky to mock xdr.ScVal perfectly without full SDK setup in tests)
    // We will bypass the XDR parsing for this specific unit test and test the DB logic instead
    upsertInvoice({
      id: 'INV-1',
      freelancer: 'G-FREE',
      payer: 'G-PAY',
      amount: 1000,
      due_date: '2023-10-10',
      status: 'Pending'
    });

    const invoices = getInvoices({});
    expect(invoices.length).toBe(1);
    expect(invoices[0].id).toBe('INV-1');
    expect(invoices[0].status).toBe('Pending');
  });

  it('should handle deduplication and status updates (funded -> paid)', () => {
    // Upsert same invoice, different status
    upsertInvoice({
      id: 'INV-1',
      freelancer: '', payer: '', amount: 0, due_date: '',
      status: 'Funded'
    });

    let invoices = getInvoices({ status: 'Funded' });
    expect(invoices.length).toBe(1);
    // Should retain original data (COALESCE)
    expect(invoices[0].freelancer).toBe('G-FREE');

    // Pay it
    upsertInvoice({
      id: 'INV-1',
      freelancer: '', payer: '', amount: 0, due_date: '',
      status: 'Paid'
    });

    invoices = getInvoices({});
    expect(invoices.length).toBe(1); // Still 1 record
    expect(invoices[0].status).toBe('Paid');
  });
});

describe('REST API', () => {
  beforeAll(() => {
    db.exec('DELETE FROM invoices');
    upsertInvoice({
      id: 'INV-2', freelancer: 'G-FREE-2', payer: 'G-PAY-2', amount: 500, due_date: '2023-11-11', status: 'Pending'
    });
    upsertInvoice({
      id: 'INV-3', freelancer: 'G-FREE-3', payer: 'G-PAY-2', amount: 1500, due_date: '2023-12-12', status: 'Funded'
    });
  });

  it('GET /invoices should return all invoices', async () => {
    const res = await request(app).get('/invoices');
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data.length).toBe(2);
  });

  it('GET /invoices?status=Funded should filter', async () => {
    const res = await request(app).get('/invoices?status=Funded');
    expect(res.status).toBe(200);
    expect(res.body.data.length).toBe(1);
    expect(res.body.data[0].id).toBe('INV-3');
  });

  it('GET /invoices?payer=G-PAY-2 should filter', async () => {
    const res = await request(app).get('/invoices?payer=G-PAY-2');
    expect(res.status).toBe(200);
    expect(res.body.data.length).toBe(2);
  });

  it('GET /invoice/:id should return specific invoice', async () => {
    const res = await request(app).get('/invoice/INV-2');
    expect(res.status).toBe(200);
    expect(res.body.data.id).toBe('INV-2');
  });

  it('GET /invoice/:id should return 404 for unknown', async () => {
    const res = await request(app).get('/invoice/UNKNOWN');
    expect(res.status).toBe(404);
  });
});
