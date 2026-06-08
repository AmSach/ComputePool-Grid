# Devlog: Session 01 - The Hub and The Agent
**Date:** 2026-06-05 22:00
**Duration:** 6 hours

The vision for ComputePool is simple: make compute as liquid as cash. I spent the first session building the FastAPI Hub and the Python Node Agent.

**Key Accomplishments:**
- Implemented the registration handshake where the agent probes the local hardware (CPU, RAM, GPU) and reports it to the Hub.
- Built the "Quality Score" algorithm. An RTX 4090 shouldn't be paid the same as a 10-year-old laptop. The Hub now weighs rewards based on hardware tiers.
- Set up the Neon PostgreSQL schema to handle concurrent node heartbeats.

**Struggles:**
- Handling `nvidia-smi` parsing on machines without drivers installed. Had to build a multi-layered fallback system using `GPUtil` and `psutil`.
