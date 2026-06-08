import requests
import time
import random
import uuid

HUB_URL = "http://localhost:8081"
USERS = ["god", "demo", "man44", "friend"]
JOB_TYPES = ["ml", "gaming", "compute"]

def submit_random_job():
    user = random.choice(USERS)
    job_type = random.choice(JOB_TYPES)
    slices = random.randint(1, 10)
    
    scripts = {
        "ml": "import time\nprint('Training neural network...')\ntime.sleep(5)\nprint('Accuracy: 0.98')",
        "compute": "print(f'Hash: {uuid.uuid4()}')",
        "gaming": "print('Streaming frame 1024x768...')"
    }
    
    data = {
        "type": job_type,
        "submitter_id": user,
        "script": scripts.get(job_type, "print('hello')"),
        "slices": slices,
        "priority": random.randint(0, 5)
    }
    
    try:
        resp = requests.post(f"{HUB_URL}/jobs/submit", json=data)
        if resp.status_code == 200:
            print(f"[Traffic] Submitted {job_type} job for {user} ({slices} slices)")
        else:
            print(f"[Traffic] Failed to submit: {resp.text}")
    except Exception as e:
        print(f"[Traffic] Error: {e}")

if __name__ == "__main__":
    print("Starting Traffic Simulator...")
    while True:
        submit_random_job()
        time.sleep(random.randint(5, 20))
