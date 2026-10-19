import { useState, useEffect, useCallback } from 'react';
import {
  connectWallet,
  connectWalletByType,
  disconnectWallet,
  getConnectedAddress,
  getWalletBalance,
  detectWallets,
} from '../services/wallet';
import type { WalletType } from '../services/wallet';
import { useAppStore } from '../store';

export interface UseWalletResult {
  address: string | null;
  balance: number | null;
  isConnected: boolean;
  isConnecting: boolean;
  error: string | null;
  connect: () => Promise<void>;
  /** Connect to a specific wallet by type (used by the wallet selection modal) */
  connectByType: (type: WalletType) => Promise<void>;
  disconnect: () => void;
  /** Which wallet extensions are available in the current browser */
  availableWallets: { freighter: boolean; albedo: boolean };
}

const STORAGE_KEY = 'bankerchanger_wallet_address';

export function useWallet(): UseWalletResult {
  const { walletAddress, walletBalance, isConnecting, setWallet, clearWallet } = useAppStore();
  const [error, setError] = useState<string | null>(null);
  const [availableWallets, setAvailableWallets] = useState<{ freighter: boolean; albedo: boolean }>({
    freighter: false,
    albedo: false,
  });

  useEffect(() => {
    const stored = getConnectedAddress();
    if (stored) {
      getWalletBalance().then((bal) => setWallet(stored, bal)).catch(() => {});
    }
    setAvailableWallets(detectWallets());
  }, []);

  const connect = useCallback(async () => {
    setError(null);
    useAppStore.setState({ isConnecting: true });
    try {
      const address = await connectWallet();
      const balance = await getWalletBalance();
      sessionStorage.setItem(STORAGE_KEY, address);
      setWallet(address, balance);
    } catch (e: any) {
      setError(e?.message ?? 'Failed to connect wallet');
    } finally {
      useAppStore.setState({ isConnecting: false });
    }
  }, [setWallet]);

  const connectByType = useCallback(async (type: WalletType) => {
    setError(null);
    useAppStore.setState({ isConnecting: true });
    try {
      const address = await connectWalletByType(type);
      const balance = await getWalletBalance();
      sessionStorage.setItem(STORAGE_KEY, address);
      setWallet(address, balance);
    } catch (e: any) {
      setError(e?.message ?? 'Failed to connect wallet');
    } finally {
      useAppStore.setState({ isConnecting: false });
    }
  }, [setWallet]);

  const disconnect = useCallback(() => {
    disconnectWallet();
    sessionStorage.removeItem(STORAGE_KEY);
    clearWallet();
  }, [clearWallet]);

  return {
    address: walletAddress,
    balance: walletBalance,
    isConnected: !!walletAddress,
    isConnecting,
    error,
    connect,
    connectByType,
    disconnect,
    availableWallets,
  };
}
