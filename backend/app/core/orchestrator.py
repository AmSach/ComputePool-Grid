import asyncio
import logging
from typing import List, Dict, Any
from app.db.session import SessionLocal
from app.api.v1.endpoints.market import ComputeMarket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComputeOrchestrator:
    """
    Advanced Orchestrator for distributed compute task allocation.
    Handles node discovery, job prioritization, and failure recovery.
    """
    def __init__(self):
        self.nodes = {}
        self.active_jobs = {}
        self.market = ComputeMarket()

    async def register_node(self, node_id: str, capacity: Dict[str, Any]):
        """Registers a new compute node with its hardware capabilities."""
        self.nodes[node_id] = {
            "capacity": capacity,
            "status": "idle",
            "last_heartbeat": asyncio.get_event_loop().time()
        }
        logger.info(f"Node {node_id} registered with capacity: {capacity}")

    async def allocate_task(self, task_id: str, requirements: Dict[str, Any]):
        """Allocates a task to the most suitable idle node using a weighted scoring algorithm."""
        best_node = None
        best_score = -1

        for node_id, data in self.nodes.items():
            if data["status"] == "idle":
                score = self._calculate_score(data["capacity"], requirements)
                if score > best_score:
                    best_score = score
                    best_node = node_id

        if best_node:
            self.nodes[best_node]["status"] = "busy"
            self.active_jobs[task_id] = best_node
            logger.info(f"Task {task_id} allocated to Node {best_node} (Score: {best_score})")
            return best_node
        
        logger.warning(f"No available nodes for task {task_id}")
        return None

    def _calculate_score(self, capacity: Dict[str, Any], requirements: Dict[str, Any]) -> float:
        """Heuristic for node-task matching."""
        score = 0.0
        if capacity.get("gpu_vram", 0) >= requirements.get("min_vram", 0):
            score += 10.0
        if capacity.get("cpu_cores", 0) >= requirements.get("min_cores", 0):
            score += 5.0
        return score

    async def monitor_fleet(self):
        """Background loop to monitor node health and reclaim timed-out nodes."""
        while True:
            current_time = asyncio.get_event_loop().time()
            for node_id, data in list(self.nodes.items()):
                if current_time - data["last_heartbeat"] > 60:
                    logger.warning(f"Node {node_id} timed out. Reclaiming...")
                    data["status"] = "offline"
            await asyncio.sleep(10)

# Global orchestrator instance
orchestrator = ComputeOrchestrator()
