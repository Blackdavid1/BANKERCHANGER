# Contributing to BANKERCHANGER

Thank you for contributing! Please read these guidelines before opening a PR.

## Branch Protection Rules for `main`

Direct pushes to `main` are blocked. All changes must go through a pull request.

### Required Status Checks

The following CI jobs **must pass** before a PR can be merged:

| Check | Workflow |
|-------|----------|
| `Backend` | `.github/workflows/backend-ci.yml` |
| `Frontend / TypeScript Build + Tests` | `.github/workflows/frontend-ci.yml` |
| `Frontend / E2E Tests` | `.github/workflows/frontend-ci.yml` |
| `Contracts` | `.github/workflows/contracts-ci.yml` |

### Configuring Branch Protection via GitHub UI

1. Navigate to **Settings → Branches → Branch protection rules** and click **Add rule**.
2. Set **Branch name pattern** to `main`.
3. Enable **Require a pull request before merging**.
   - Set **Required approvals** to `1`.
   - Enable **Dismiss stale pull request approvals when new commits are pushed**.
4. Enable **Require status checks to pass before merging**.
   - Enable **Require branches to be up to date before merging**.
   - Search for and add each check listed in the table above.
5. Enable **Do not allow bypassing the above settings** so admins are also subject to them.
6. Click **Save changes**.

### Configuring Branch Protection via `gh` CLI

```bash
gh api repos/doradenise-jpg/BANKERCHANGER/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["Backend","Frontend / TypeScript Build + Tests","Frontend / E2E Tests","Contracts"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
  --field restrictions=null
```

## Naming Conventions

This project was originally prototyped under the name **boxmeout**. The canonical name is now **BANKERCHANGER**. Use the table below whenever adding new code, comments, configuration, or documentation.

| Context | Accepted name | Never use |
|---------|--------------|-----------|
| Repository name, PR titles, docs headings | `BANKERCHANGER` | `BoxMeOut`, `boxmeout`, `BOXMEOUT` |
| App name in UI / metadata | `BANKERCHANGER` | `BoxMeOut` |
| npm package names | `bankerchanger-backend`, `bankerchanger-frontend` | `boxmeout-backend`, `boxmeout-frontend` |
| Database name / user / password (local dev) | `bankerchanger` | `boxmeout` |
| `DATABASE_URL` default | `postgresql://bankerchanger:bankerchanger@localhost:5432/bankerchanger` | any `boxmeout` URL |
| Email sender address | `no-reply@bankerchanger.app` | `no-reply@boxmeout.app` |
| `APP_NAME` env var | `BANKERCHANGER` | `BoxMeOut` |
| localStorage / sessionStorage keys | `bankerchanger_*` | `boxmeout_*` |
| Custom DOM events | `bankerchanger:*` | `boxmeout:*` |
| Prometheus job label | `bankerchanger` | `boxmeout` |
| Source-file comment headers | `// BANKERCHANGER — …` | `// BOXMEOUT — …` |
| Soroban contract package names in `Cargo.toml` | **unchanged** — `boxmeout-market`, `boxmeout-market-factory`, `boxmeout-treasury`, `boxmeout-shared` | do **not** rename these |
| Rust `use` / function-call paths in contracts | **unchanged** — `boxmeout_shared::…` | do **not** rename these |
| Compiled WASM filenames | **unchanged** — `boxmeout_treasury.wasm`, `boxmeout_market_factory.wasm`, `boxmeout_market.wasm` | do **not** rename these |

> **Why keep the contract names?** The Soroban smart contracts are deployed on-chain under those identifiers. Renaming the Rust crate names would require redeploying all contracts and migrating all existing on-chain state — a breaking change outside the scope of this rebranding.

## Development Workflow

1. Fork the repository and create a feature branch from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. Make your changes and commit following [Conventional Commits](https://www.conventionalcommits.org/).
3. Run the full check suite locally before pushing:
   ```bash
   npm run lint && npm test && npm run build
   ```
4. Open a pull request against `main`. The PR description must reference the issue it addresses (`Closes #N`).
5. A changelog entry is required for any PR that ships a user-visible change. Add it to `CHANGELOG.md` under `[Unreleased]`.

## Commit Message Format

```
<type>(<scope>): <short summary>

[optional body]

[optional footer: Closes #N]
```

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`.

## Reporting Bugs

Open a GitHub Issue using the bug report template. Include reproduction steps, expected vs actual behaviour, and environment details.
