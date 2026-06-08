# Devlog: Session 02 - Job Scheduling and Payouts
**Date:** 2026-06-06 23:30
**Duration:** 8 hours

Today was all about the "Job Lifecycle". A marketplace is useless if jobs don't move.

**Updates:**
- Implemented the `JobStatus` state machine: PENDING → ASSIGNED → RUNNING → COMPLETED/FAILED.
- Built the "Stardust" credit system. Users top up, submit jobs, and nodes earn based on the work done.
- Added a platform fee (20%) to sustain the hub infrastructure.

**Hurdles:**
- Race conditions during job assignment. Two nodes would try to grab the same job at the exact same millisecond. Solved it using a row-level lock in the DB (`SELECT FOR UPDATE`).
