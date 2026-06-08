# 💎 ComputePool: The Decentralized GPU/CPU Grid

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Stack: Next.js + FastAPI + PostgreSQL](https://img.shields.io/badge/Stack-Full--Stack-green)](https://github.com/AmSach/ComputePool-Grid)
[![Network Status](https://img.shields.io/badge/Nodes-Online-brightgreen)](https://man44.zo.space/compute-pool)

**ComputePool is a high-performance orchestration layer for the decentralized compute marketplace.**

It allows individuals to lease their spare GPU and CPU capacity to a global pool, providing developers with affordable, high-performance compute on-demand. Unlike centralized clouds, ComputePool is resilient, trustless, and dynamically priced.

## 🚀 Key Features

### ⚖️ Weighted Orchestration
The heart of ComputePool is its **Weighted Scoring Algorithm** (`backend/app/core/orchestrator.py`). It intelligently matches compute tasks with nodes based on VRAM capacity, CPU core count, and historical reliability scores.

### 💰 Spot Pricing Marketplace
Our dynamic marketplace allows node providers to list their compute with real-time bidding. Users can deploy jobs to the "best-priced" node that meets their hardware affinity requirements.

### 📊 Live Mesh Visualization
The [Interactive Dashboard](https://man44.zo.space/compute-pool) provides a real-time view of the network topology, showing active nodes, job throughput, and resource utilization across the global mesh.

## 🏗 Full-Stack Architecture

- **Frontend**: Next.js (TypeScript) + Tailwind CSS + Lucide Icons.
- **Backend**: FastAPI (Python) + SQLAlchemy + PostgreSQL (Neon).
- **Orchestration**: Custom asynchronous scheduler for job-to-node mapping.
- **Node Agent**: Lightweight Python daemon for resource reporting and job execution.

## 🛠 Developer Quickstart

```bash
# Clone the marketplace
git clone https://github.com/AmSach/ComputePool-Grid.git
cd ComputePool-Grid

# Setup backend
cd backend
pip install -r requirements.txt
python3 -m app.main

# Setup frontend
cd ../frontend
npm install
npm run dev
```

## 🎥 Demo Video
Check out the live recording of the ComputePool Command Center in action:
`file 'stardance_assets/computepool_demo_v2.webm'`

---
*Built for the Stardance Challenge. Decentralizing the future of compute.*
