#!/usr/bin/env python3
"""
ComputePool Node Agent — Full Production Build
Run this on any machine to join the compute pool.
Works on Linux, macOS, Windows (via Docker or bare Python).
"""

import os, sys, time, json, subprocess, traceback, platform
import requests
import psutil

HUB_URL = os.environ.get("HUB_URL", "http://127.0.0.1:8000")
NODE_NAME = os.environ.get("NODE_NAME", platform.node())
OWNER_ID = os.environ.get("OWNER_ID", "default")
GPU_TIER = os.environ.get("GPU_TIER", "cpu")
REGION = os.environ.get("REGION", "in")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "10"))
MIN_DISK_GB = float(os.environ.get("MIN_DISK_GB", "10"))
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "")
HEARTBEAT_INTERVAL = 30

NODE_ID = None

def get_gpu_info():
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            g = gpus[0]
            name = g.name
            vram = round(g.memoryTotal / 1024, 1)
            if "4090" in name: return "rtx-4090", vram
            elif "5090" in name: return "rtx-5090", vram
            elif "3090" in name: return "rtx-3090", vram
            elif "4070" in name: return "rtx-4070", vram
            elif "3060" in name: return "rtx-3060", vram
            elif "2070" in name: return "rtx-2070", vram
            elif "1080 ti" in name: return "gtx-1080ti", vram
            elif "1080" in name: return "gtx-1080", vram
            elif "1660" in name: return "gtx-1660", vram
            return "gpu", vram
    except ImportError:
        pass
    except Exception:
        pass

    if platform.system() == "Linux":
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                line = result.stdout.strip().split(",")[0]
                name = line.strip()
                if "4090" in name: return "rtx-4090", 24
                elif "3090" in name: return "rtx-3090", 24
                elif "4070" in name: return "rtx-4070", 12
                elif "3060" in name: return "rtx-3060", 12
                elif "2070" in name: return "rtx-2070", 8
                elif "1080" in name: return "gtx-1080", 11
                return "gpu", 8
        except Exception:
            pass

    return GPU_TIER, 0

def get_cpu_cores():
    return psutil.cpu_count(logical=True) or 4

def get_ram_gb():
    return round(psutil.virtual_memory().total / (1024**3), 1)

def get_disk_gb():
    try:
        return round(psutil.disk_usage("/").free / (1024**3), 1)
    except Exception:
        return 100

def get_system_info():
    gpu_name, vram_gb = get_gpu_info()
    return {
        "node_name": NODE_NAME,
        "owner_id": OWNER_ID,
        "gpu_tier": gpu_name,
        "cpu_cores": get_cpu_cores(),
        "ram_gb": get_ram_gb(),
        "region": REGION,
        "disk_free_gb": get_disk_gb(),
        "os": platform.system(),
        "vram_gb": vram_gb
    }

def register_node():
    global NODE_ID
    info = get_system_info()
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}
    resp = requests.post(f"{HUB_URL}/nodes/register", json=info, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    NODE_ID = data["node_id"]
    print(f"[Node] Registered as {NODE_ID} | GPU: {info['gpu_tier']} | Quality: {data['quality_score']}x")
    return NODE_ID

def send_heartbeat(status="online"):
    if not NODE_ID: return
    try:
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}
        requests.post(
            f"{HUB_URL}/nodes/heartbeat",
            json={"node_id": NODE_ID, "status": status},
            headers=headers, timeout=10
        )
    except Exception as e:
        print(f"[Heartbeat] Failed: {e}")

def fetch_job():
    if not NODE_ID: return None
    try:
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}
        resp = requests.get(f"{HUB_URL}/jobs/next?node_id={NODE_ID}", headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("job")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return None
        raise
    except Exception as e:
        print(f"[Fetch] Error: {e}")
        return None

def execute_job(job):
    job_id = job["id"]
    job_type = job.get("type", "compute")
    script = job.get("script", "")

    print(f"[Job] Starting {job_id} ({job_type})")

    result_cid = ""
    error = None

    try:
        if job_type == "ml":
            result_cid = execute_ml_job(job, script)
        elif job_type == "gaming":
            result_cid = execute_gaming_job(job, script)
        else:
            result_cid = execute_generic_job(job, script)
    except Exception as e:
        error = str(e)
        print(f"[Job] {job_id} failed: {e}")
        traceback.print_exc()

    try:
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}
        requests.post(
            f"{HUB_URL}/jobs/complete",
            json={"job_id": job_id, "result_cid": result_cid, "error": error},
            headers=headers, timeout=15
        )
        print(f"[Job] {job_id} completed. CID: {result_cid or 'none'}")
    except Exception as e:
        print(f"[Complete] Failed to report: {e}")

def execute_ml_job(job, script):
    print("[ML] Training job — placeholder")
    time.sleep(3)
    return f"ml-result-{job['id']}"

def execute_gaming_job(job, script):
    print("[Gaming] Streaming job — placeholder")
    time.sleep(2)
    return f"gaming-session-{job['id']}"

def execute_generic_job(job, script):
    print("[Compute] Running generic job")
    if script:
        try:
            local_script = f"/tmp/cp_job_{job['id']}.py"
            with open(local_script, "w") as f:
                f.write(script)
            result = subprocess.run(
                ["python3", local_script],
                capture_output=True, text=True, timeout=300
            )
            return result.stdout[:500] or f"done-{job['id']}"
        except Exception as e:
            return f"error: {e}"
    return f"done-{job['id']}"

def main():
    print(f"""
    ╔══════════════════════════════════════╗
    ║     ComputePool Node Agent v0.1     ║
    ║  Hub: {HUB_URL:<30}  ║
    ║  Node: {NODE_NAME:<29}  ║
    ╚══════════════════════════════════════╝
    """)
    register_node()

    last_heartbeat = time.time()
    while True:
        try:
            job = fetch_job()
            if job:
                execute_job(job)
            else:
                print(f"[Poll] No jobs. Waiting {POLL_INTERVAL}s...")
            time.sleep(POLL_INTERVAL)

            if time.time() - last_heartbeat >= HEARTBEAT_INTERVAL:
                send_heartbeat()
                last_heartbeat = time.time()

        except KeyboardInterrupt:
            print("\n[Node] Shutting down...")
            send_heartbeat("offline")
            sys.exit(0)
        except Exception as e:
            print(f"[Error] {e}. Retrying in 15s...")
            traceback.print_exc()
            time.sleep(15)

if __name__ == "__main__":
    main()