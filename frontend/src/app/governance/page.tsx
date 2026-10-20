'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Proposal, ProposalStatus } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';
const PROPOSALS_PER_PAGE = 20;

export default function GovernanceList() {
  const [proposals, setProposals] = useState<Proposal[]>([]);
  const [statusFilter, setStatusFilter] = useState<ProposalStatus | 'All'>('All');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchProposals();
  }, [currentPage, statusFilter]);

  const fetchProposals = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const statusParam = statusFilter === 'All' ? '' : `&status=${statusFilter.toLowerCase()}`;
      const url = `${API_BASE_URL}/api/governance/proposals?page=${currentPage}&limit=${PROPOSALS_PER_PAGE}${statusParam}`;
      
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      const json = await response.json();
      if (!json.success) {
        throw new Error(json.error || 'Failed to fetch proposals');
      }

      setProposals(json.data || []);
      setTotalPages(json.pagination?.totalPages || 1);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load proposals');
      setProposals([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStatusChange = (newStatus: ProposalStatus | 'All') => {
    setStatusFilter(newStatus);
    setCurrentPage(1); // Reset to first page when filter changes
  };

  const handlePreviousPage = () => {
    setCurrentPage(p => Math.max(1, p - 1));
  };

  const handleNextPage = () => {
    setCurrentPage(p => Math.min(totalPages, p + 1));
  };

  return (
    <div className="max-w-4xl mx-auto p-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold">Governance</h1>
          <p className="text-gray-400 mt-2">Discover and vote on network proposals</p>
        </div>
        <div className="flex gap-4">
          <select
            value={statusFilter}
            onChange={(e) => handleStatusChange(e.target.value as any)}
            className="px-4 py-2 bg-gray-800 border border-gray-700 rounded text-sm font-medium"
            disabled={isLoading}
          >
            <option value="All">All Proposals</option>
            <option value="Active">Active</option>
            <option value="Passed">Passed</option>
            <option value="Failed">Failed</option>
            <option value="Executed">Executed</option>
          </select>
          <Link 
            href="/governance/new" 
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium transition-colors disabled:opacity-50"
          >
            New Proposal
          </Link>
        </div>
      </div>

      {error && (
        <div className="p-4 mb-4 bg-red-500/10 border border-red-500/20 rounded text-red-400">
          {error}
        </div>
      )}

      {isLoading ? (
        <div className="text-center p-8 text-gray-400">Loading proposals...</div>
      ) : (
        <>
          <div className="space-y-4">
            {proposals.length === 0 ? (
              <div className="text-center p-8 bg-gray-800/50 rounded-xl border border-gray-700">
                <p className="text-gray-400">No proposals found matching this filter.</p>
              </div>
            ) : (
              proposals.map((proposal) => (
                <ProposalCard key={proposal.id} proposal={proposal} />
              ))
            )}
          </div>

          {/* Pagination controls */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between mt-8 pt-8 border-t border-gray-700">
              <div className="text-sm text-gray-400">
                Page {currentPage} of {totalPages}
              </div>
              <div className="flex gap-2">
                <button
                  onClick={handlePreviousPage}
                  disabled={currentPage === 1 || isLoading}
                  className="px-4 py-2 bg-gray-800 border border-gray-700 rounded text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-700"
                >
                  Previous
                </button>
                <button
                  onClick={handleNextPage}
                  disabled={currentPage === totalPages || isLoading}
                  className="px-4 py-2 bg-gray-800 border border-gray-700 rounded text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-700"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

function ProposalCard({ proposal }: { proposal: Proposal }) {
  const totalVotes = proposal.votesFor + proposal.votesAgainst + proposal.votesAbstain;
  
  const getStatusColor = (status: ProposalStatus) => {
    switch (status) {
      case 'Active': return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
      case 'Passed': return 'bg-green-500/10 text-green-400 border-green-500/20';
      case 'Failed': return 'bg-red-500/10 text-red-400 border-red-500/20';
      case 'Executed': return 'bg-purple-500/10 text-purple-400 border-purple-500/20';
      default: return 'bg-gray-500/10 text-gray-400 border-gray-500/20';
    }
  };

  const getTimeRemaining = () => {
    if (proposal.status !== 'Active') return 'Ended';
    const ms = new Date(proposal.expiresAt).getTime() - Date.now();
    if (ms <= 0) return 'Ended';
    const days = Math.floor(ms / (1000 * 60 * 60 * 24));
    return `${days} day${days !== 1 ? 's' : ''} left`;
  };

  const formatType = (type: string) => {
    return type.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  };

  return (
    <Link href={`/governance/${proposal.id}`} className="block">
      <div className="p-5 bg-gray-900 border border-gray-800 rounded-xl hover:border-gray-600 transition-colors">
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${getStatusColor(proposal.status)}`}>
                {proposal.status}
              </span>
              <span className="text-sm font-mono text-gray-400">
                {formatType(proposal.type)}
              </span>
            </div>
            <p className="text-gray-200 font-medium mb-3">{proposal.description}</p>
            <div className="flex items-center gap-4 text-sm text-gray-500">
              <span>Proposer: <span className="font-mono">{proposal.proposer}</span></span>
              <span>•</span>
              <span>{totalVotes.toLocaleString()} votes cast</span>
            </div>
          </div>
          
          <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center">
            <div className="text-sm font-medium text-gray-400 mb-1">
              {getTimeRemaining()}
            </div>
            <div className="flex items-center gap-1.5 mt-2">
              <div className="w-2 h-2 rounded-full bg-green-500" title="For" />
              <div className="w-2 h-2 rounded-full bg-red-500" title="Against" />
              <div className="w-2 h-2 rounded-full bg-gray-500" title="Abstain" />
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
}
