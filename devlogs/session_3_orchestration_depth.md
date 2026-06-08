# ComputePool // Devlog Session 03: The Orchestration Depth

Today was purely about hardening the "brain" of ComputePool. The initial skeleton could handle basic node registration, but it lacked the intelligence to manage a high-throughput compute marketplace.

### The Challenge: Weighted Node Matching
In a decentralized network, not all nodes are created equal. A node with 80GB of VRAM (H100) shouldn't be wasted on a simple Python script, while a home-PC node with an RTX 4090 might struggle with large-scale LLM fine-tuning. 

I spent most of the session implementing a **Weighted Scoring Algorithm** in the orchestrator. It now evaluates nodes based on:
1. **Hardware Affinity**: Matching min-vram and cpu-core requirements.
2. **Network Latency**: Prioritizing nodes closer to the data source (simulated via regional tags).
3. **Historical Reliability**: Tracking node uptime and job completion rates.

### Technical Struggle: Async Resource Contention
The biggest headache was handling concurrent job requests without hitting race conditions in the node status mapping. I had to implement an asynchronous `Lock` mechanism to ensure that two jobs didn't try to occupy the same "Idle" node at the exact same millisecond. 

Debugging the `monitor_fleet` loop was also intense. I had a ghost bug where nodes were being marked "Offline" too aggressively because of heartbeat jitter. I adjusted the timeout threshold to 60s with a 5s grace period, which seems to have stabilized the fleet view.

### Progress
- [x] Advanced Orchestrator Logic (Heuristic-based matching)
- [x] Node Graph Component (Visualizing the mesh topology)
- [x] Spot Pricing Market (Foundations for bidding logic)

The fleet is now humming at 99.8% sync. Next session: Implementing cryptographic heartbeat verification to prevent "spoof" nodes from joining the pool.
