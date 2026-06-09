# Shared infrastructure

This tree holds the infrastructure every lab reuses so that no lab requires paid API calls to
learn.

- `harness/`: the runner that drives a lab in dry-run or live mode.
- `mock_services/`: stand-in implementations of the external tools and services the labs call.
- `fixtures/`: recorded request and response fixtures used to replay realistic behavior offline.
- `evals/`: the evaluation definitions used to score a lab's solution against its failure modes.

The contract for every lab: a dry-run path uses the mocks and fixtures and costs nothing. Live runs
against real models and services are optional and clearly marked. See `../WHAT_NOT_TO_DO.md` ("do
not require paid API calls to learn"). These directories are seeded for v0.1 and filled as each lab
is built out.
