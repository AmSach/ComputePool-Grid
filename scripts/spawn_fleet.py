import subprocess
import time
import os

HUB_URL = "http://127.0.0.1:8081"
nodes = [
    {"name": "swarm-node-alpha", "gpu": "rtx-4090", "region": "us"},
    {"name": "swarm-node-beta", "gpu": "rtx-3090", "region": "eu"},
    {"name": "swarm-node-gamma", "gpu": "rtx-4070", "region": "in"},
    {"name": "swarm-node-delta", "gpu": "cpu", "region": "uk"},
    {"name": "swarm-node-epsilon", "gpu": "rtx-3060", "region": "us"},
]

processes = []

os.makedirs("/home/workspace/compute-pool/logs", exist_ok=True)

for node in nodes:
    env = os.environ.copy()
    env["HUB_URL"] = HUB_URL
    env["NODE_NAME"] = node["name"]
    env["GPU_TIER"] = node["gpu"]
    env["REGION"] = node["region"]
    
    log_file = open(f"/home/workspace/compute-pool/logs/{node['name']}.log", "w")
    
    p = subprocess.Popen(
        ["python3.12", "/home/workspace/compute-pool/backend/agent.py"],
        env=env,
        stdout=log_file,
        stderr=log_file
    )
    processes.append((p, log_file))
    print(f"Started node {node['name']}")
    time.sleep(1)

print(f"Spawned {len(processes)} nodes. Keeping script alive...")

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    for p, f in processes:
        p.terminate()
        f.close()
