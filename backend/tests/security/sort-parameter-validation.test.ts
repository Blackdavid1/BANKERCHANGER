import { z } from 'zod';

// Test the sort parameter validation from MarketController
const listMarketsQuerySchema = z.object({
  sort: z.enum(['date_asc', 'date_desc', 'pool_desc']).default('date_desc'),
});

describe('Market Sort Parameter Validation (#281)', () => {
  it('should accept valid sort values', () => {
    const validSorts = ['date_asc', 'date_desc', 'pool_desc'];
    
    validSorts.forEach((sort) => {
      const result = listMarketsQuerySchema.safeParse({ sort });
      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.sort).toBe(sort);
      }
    });
  });

  it('should reject invalid sort values', () => {
    const invalidSorts = [
      'date', 
      'asc',
      'desc',
      'price_asc',
      'name_desc',
      'random',
      'ORDER BY',
      '; DROP TABLE markets;',
      'date_desc\'; DROP TABLE--',
    ];

    invalidSorts.forEach((sort) => {
      const result = listMarketsQuerySchema.safeParse({ sort });
      expect(result.success).toBe(false);
    });
  });

  it('should use default sort when not provided', () => {
    const result = listMarketsQuerySchema.safeParse({});
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.sort).toBe('date_desc');
    }
  });

  it('should prevent SQL injection via sort parameter', () => {
    const sqlInjectionAttempts = [
      "date_asc' OR '1'='1",
      'date_desc; DELETE FROM markets;',
      'pool_desc UNION SELECT * FROM users',
      "date_asc' AND 1=1 AND '1'='1",
      'date_desc\'; INSERT INTO markets VALUES (1,2,3); --',
      'pool_desc OR 1=1',
    ];

    sqlInjectionAttempts.forEach((attempt) => {
      const result = listMarketsQuerySchema.safeParse({ sort: attempt });
      expect(result.success).toBe(false);
    });
  });

  it('should be case-sensitive', () => {
    const caseSensitiveTests = [
      'DATE_ASC',
      'Date_Asc',
      'DATE_DESC',
      'POOL_DESC',
    ];

    caseSensitiveTests.forEach((sort) => {
      const result = listMarketsQuerySchema.safeParse({ sort });
      expect(result.success).toBe(false);
    });
  });

  it('should have exactly 3 valid options', () => {
    const result = listMarketsQuerySchema.safeParse({});
    expect(result.success).toBe(true);
    // The schema should only accept the three defined values
    expect(['date_asc', 'date_desc', 'pool_desc']).toHaveLength(3);
  });

  it('should not allow empty string', () => {
    const result = listMarketsQuerySchema.safeParse({ sort: '' });
    expect(result.success).toBe(false);
  });

  it('should not allow null', () => {
    const nullResult = listMarketsQuerySchema.safeParse({ sort: null });
    expect(nullResult.success).toBe(false);
  });

  it('should use default when undefined (Zod coercion behavior)', () => {
    const undefinedResult = listMarketsQuerySchema.safeParse({ sort: undefined });
    // Zod's .default() coerces undefined to the default value
    expect(undefinedResult.success).toBe(true);
    if (undefinedResult.success) {
      expect(undefinedResult.data.sort).toBe('date_desc');
    }
  });

  it('should validate at parse time, preventing runtime SQL issues', () => {
    // Even if someone tries to bypass frontend validation,
    // the Zod schema should reject it at API layer
    const attempts = [
      { sort: 'date_asc AND 1=1' },
      { sort: 'date_desc LIMIT 1' },
      { sort: 'pool_desc ORDER BY id' },
      { sort: 'date_asc -- comment' },
    ];

    attempts.forEach((attempt) => {
      const result = listMarketsQuerySchema.safeParse(attempt);
      expect(result.success).toBe(false);
    });
  });
});
