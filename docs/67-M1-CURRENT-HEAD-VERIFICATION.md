# M1 — Current HEAD Verification

This pass establishes explicit regression contracts for the three areas exposed by the historical CI failure: build/handoff/routing.

## Required invariants

1. A build artifact must become a workspace file before verification.
2. Handoff state must preserve the changed-file set and accept the historical `changed_files` alias.
3. Free-first routing must remain an explicit product policy when a free resource satisfies the required capability.

## Verification status

The regression contracts are now committed on `feat/m1-real-build-pipeline`.

A fresh GitHub Actions execution on the current HEAD is still required before M1 is declared green.

## After green

Move immediately to the first real end-user planning slice: raw idea → blueprint → cost/practicality comparison → recommendation → BUILD/DIY.
