import { Router } from 'express';
import {
  listProposals,
  listProposalsValidation,
  getProposal,
} from '../api/controllers/GovernanceController';

const router = Router();

/**
 * @swagger
 * tags:
 *   name: Governance
 *   description: Governance proposal endpoints
 */

/**
 * @swagger
 * /governance/proposals:
 *   get:
 *     summary: List all governance proposals (paginated)
 *     tags: [Governance]
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *           default: 1
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *           default: 20
 *           maximum: 100
 *       - in: query
 *         name: status
 *         schema:
 *           type: string
 *           enum: [active, passed, failed, executed]
 *     responses:
 *       200:
 *         description: Paginated list of proposals
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   type: array
 *                   items:
 *                     type: object
 *                     properties:
 *                       id:
 *                         type: string
 *                       type:
 *                         type: string
 *                       value:
 *                         type: string
 *                       description:
 *                         type: string
 *                       status:
 *                         type: string
 *                       proposer:
 *                         type: string
 *                       votesFor:
 *                         type: number
 *                       votesAgainst:
 *                         type: number
 *                       votesAbstain:
 *                         type: number
 *                       createdAt:
 *                         type: string
 *                         format: date-time
 *                       expiresAt:
 *                         type: string
 *                         format: date-time
 *                 pagination:
 *                   type: object
 *                   properties:
 *                     page:
 *                       type: integer
 *                     limit:
 *                       type: integer
 *                     total:
 *                       type: integer
 *                     totalPages:
 *                       type: integer
 *                     hasNextPage:
 *                       type: boolean
 *                     hasPrevPage:
 *                       type: boolean
 *       400:
 *         description: Invalid parameters
 */
router.get('/proposals', listProposalsValidation, listProposals);

/**
 * @swagger
 * /governance/proposals/{proposal_id}:
 *   get:
 *     summary: Get a single proposal by ID
 *     tags: [Governance]
 *     parameters:
 *       - in: path
 *         name: proposal_id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Proposal details
 *       404:
 *         description: Proposal not found
 */
router.get('/proposals/:proposal_id', getProposal);

export default router;
