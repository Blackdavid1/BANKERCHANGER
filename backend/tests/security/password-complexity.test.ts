import { passwordSchema } from '../../src/schemas/validation.schemas';

describe('Password Complexity Requirements (#284)', () => {
  it('should accept a password meeting all requirements', () => {
    const validPassword = 'SecurePass123!';
    const result = passwordSchema.safeParse(validPassword);
    expect(result.success).toBe(true);
  });

  it('should require at least 12 characters', () => {
    // 11 characters - should fail
    const shortPassword = 'Secure12!aB';
    const result = passwordSchema.safeParse(shortPassword);
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toContain('12 characters');
    }
  });

  it('should accept exactly 12 characters if other requirements are met', () => {
    const twelveCharPassword = 'SecurePass1!';
    const result = passwordSchema.safeParse(twelveCharPassword);
    expect(result.success).toBe(true);
  });

  it('should require at least one uppercase letter', () => {
    const noUppercase = 'securepass123!';
    const result = passwordSchema.safeParse(noUppercase);
    expect(result.success).toBe(false);
  });

  it('should require at least one lowercase letter', () => {
    const noLowercase = 'SECUREPASS123!';
    const result = passwordSchema.safeParse(noLowercase);
    expect(result.success).toBe(false);
  });

  it('should require at least one digit', () => {
    const noDigit = 'SecurePassWord!';
    const result = passwordSchema.safeParse(noDigit);
    expect(result.success).toBe(false);
  });

  it('should require at least one special character', () => {
    const noSpecial = 'SecurePass1234';
    const result = passwordSchema.safeParse(noSpecial);
    expect(result.success).toBe(false);
  });

  it('should accept special characters like @#$%^&*', () => {
    const passwords = [
      'SecurePass123@',
      'SecurePass123#',
      'SecurePass123$',
      'SecurePass123%',
      'SecurePass123^',
      'SecurePass123&',
      'SecurePass123*',
    ];
    passwords.forEach((pwd) => {
      const result = passwordSchema.safeParse(pwd);
      expect(result.success).toBe(true);
    });
  });

  it('should reject password longer than 128 characters', () => {
    const longPassword = 'SecurePass123!' + 'a'.repeat(115); // 129 total
    const result = passwordSchema.safeParse(longPassword);
    expect(result.success).toBe(false);
  });

  it('should accept password of exactly 128 characters if requirements are met', () => {
    const maxPassword = 'SecurePass123!' + 'a'.repeat(114); // 128 total
    const result = passwordSchema.safeParse(maxPassword);
    expect(result.success).toBe(true);
  });

  it('should reject passwords shorter than 12 characters', () => {
    const testCases = [
      'Secure12!',     // 9 chars
      'Secure123!a',   // 11 chars
      'Pass1!Aa',      // 8 chars
    ];

    testCases.forEach((pwd) => {
      const result = passwordSchema.safeParse(pwd);
      expect(result.success).toBe(false);
    });
  });
});
