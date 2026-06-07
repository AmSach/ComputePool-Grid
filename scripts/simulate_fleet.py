import requests
import time
import random
import uuid
import threading

HUB_URL = "http://127.0.0.1:8081"
NUM_NODES = 10
PROJECT_IDS = ["Omega-System", "AgadaHealth", "GhostPilot", "VoxelNav", "LiveTranslate"]

GPU_TIERS = ["rtx-4090", "rtx-3090", "rtx-3060", "cpu"]
REGIONS = ["in", "us", "uk", "eu"]

class VirtualNode:
    def __init__(self, name, gpu_tier, region):
        self.name = name
        self.gpu_tier = gpu_tier
        self.region = region
        self.node_id = None
        self.owner_id = "man44"

    def register(self):
        try:
            resp = requests.post(f"{HUB_URL}/nodes/register", params={
                "node_name": self.name,
                "gpu_tier": self.gpu_tier,
                "owner_id": self.owner_id,
                "region": self.region
            })
            self.node_id = resp.json()["node_id"]
            print(f"Registered {self.name} as {self.node_id}")
        except Exception as e:
            print(f"Failed to register {self.name}: {e}")

    def heartbeat(self):
        if not self.node_id: return
        try:
            requests.post(f"{HUB_URL}/nodes/heartbeat", params={"node_id": self.node_id})
        except Exception as e:
            print(f"Heartbeat failed for {self.node_id}: {e}")

    def run(self):
        self.register()
        while True:
            self.heartbeat()
            # Try to get a job
            try:
                resp = requests.get(f"{HUB_URL}/jobs/next", params={"node_id": self.node_id})
                job = resp.json().get("job")
                if job:
                    print(f"Node {self.name} executing job {job['id']}")
                    time.sleep(random.randint(5, 15))
                    requests.post(f"{HUB_URL}/jobs/complete", params={
                        "job_id": job['id'],
                        "result_cid": f"ipfs://{uuid.uuid4().hex}"
                    })
            except Exception as e:
                pass
            time.sleep(random.randint(10, 30))

def submitter_loop():
    # Register user first
    try:
        requests.post(f"{HUB_URL}/auth/register", params={"user_id": "man44", "name": "Aman Sachan"})
        requests.post(f"{HUB_URL}/credits/topup", params={"user_id": "man44", "amount": 10000})
    except: pass

    while True:
        try:
            job_type = random.choice(["ml", "gaming", "compute"])
            requests.post(f"{HUB_URL}/jobs/submit", params={
                "type": job_type,
                "submitter_id": "man44",
                "slices": random.randint(1, 4)
            })
            print(f"Submitted new {job_type} job")
        except Exception as e:
            print(f"Submission failed: {e}")
        time.sleep(random.randint(20, 60))

if __name__ == "__main__":
    nodes = []
    for i in range(NUM_NODES):
        n = VirtualNode(f"swarm-node-{i}", random.choice(GPU_TIERS), random.choice(REGIONS))
        t = threading.Thread(target=n.run, daemon=True)
        t.start()
        nodes.append(n)

    submitter_loop()
