import * as OTPAuth from 'otpauth';
import { generateSecret, generateQRCode, verifyToken } from '../../src/services/totp.service';

describe('totp.service', () => {
  let secret: string;
  let otpauthUrl: string;

  beforeEach(() => {
    ({ secret, otpauthUrl } = generateSecret('test@example.com'));
  });

  describe('generateSecret', () => {
    it('returns a base32 secret and otpauth URL', () => {
      expect(secret).toMatch(/^[A-Z2-7]+=*$/);
      expect(otpauthUrl).toMatch(/^otpauth:\/\/totp\//);
      expect(otpauthUrl).toContain('BANKERCHANGER');
    });
  });

  describe('generateQRCode', () => {
    it('returns a data URL', async () => {
      const qr = await generateQRCode(otpauthUrl);
      expect(qr).toMatch(/^data:image\/png;base64,/);
    });
  });

  describe('verifyToken', () => {
    let totp: OTPAuth.TOTP;
    let validOtp: string;

    beforeEach(() => {
      totp = new OTPAuth.TOTP({
        algorithm: 'SHA1',
        digits: 6,
        period: 30,
        secret: OTPAuth.Secret.fromBase32(secret),
      });
      validOtp = totp.generate();
    });

    it('accepts a valid current OTP', () => {
      expect(verifyToken(secret, validOtp)).toBe(true);
    });

    it('rejects an OTP from an adjacent window when window=0', () => {
      const adj = totp.generate({
        timestamp: Date.now() - 60_000, // 2 steps ago
      });
      expect(verifyToken(secret, adj)).toBe(false);
    });

    it('accepts an OTP from an adjacent window when a wider window is passed', () => {
      const adj = totp.generate({
        timestamp: Date.now() - 60_000, // 2 steps ago
      });
      expect(verifyToken(secret, adj, 2)).toBe(true);
    });

    it('rejects a wrong OTP', () => {
      expect(verifyToken(secret, '000000')).toBe(false);
    });

    it('rejects an OTP with wrong length', () => {
      expect(verifyToken(secret, '12345')).toBe(false);
    });

    it('rejects an empty string', () => {
      expect(verifyToken(secret, '')).toBe(false);
    });

    it('respects the TOTP_WINDOW environment variable', () => {
      process.env.TOTP_WINDOW = '2';
      const adj = totp.generate({
        timestamp: Date.now() - 60_000,
      });
      // When window=2, a token 2 steps ago is within the accepted range
      expect(verifyToken(secret, adj)).toBe(true);
      delete process.env.TOTP_WINDOW;
    });
  });
});
