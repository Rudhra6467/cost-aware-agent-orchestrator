# M1 Verification Gate

## Purpose

This document records the final gate before CAOS moves from foundation work into the end-user planning experience.

## Current HEAD

The branch contains the M1 build, routing, handoff, continuation, repair, verification, telemetry, and planning components, plus regression contracts added during integration cleanup.

## CI requirement

A GitHub Actions run must execute against the current HEAD and finish with `pytest -q` returning zero failures. Historical workflow results do not qualify because they ran against earlier commits.

## No speculative changes

Until a current-HEAD test result is available, production architecture should not be expanded merely to obtain another CI trigger. Any new failure should be fixed from its actual traceback.

## M2 entry criterion

Once the gate is green, begin the first end-user slice:

`idea -> understanding -> blueprint -> resource discovery -> cost/quality/time comparison -> recommendation -> BUILD/DIY`

M2 should reuse the existing domain pipeline rather than creating a parallel planning architecture.
