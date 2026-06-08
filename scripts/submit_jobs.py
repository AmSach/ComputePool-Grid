import requests
import random
import time

API_URL = "http://127.0.0.1:8081"
job_types = ["ml", "gaming", "compute"]
users = ["man44", "default"]

for i in range(10):
    job_type = random.choice(job_types)
    user_id = random.choice(users)
    payload = {
        "type": job_type,
        "submitter_id": user_id,
        "script": "import time; print('Working...'); time.sleep(5); print('Done.')",
        "slices": random.randint(1, 5),
        "priority": random.randint(0, 10)
    }
    resp = requests.post(f"{API_URL}/jobs/submit", json=payload)
    if resp.status_code == 200:
        print(f"Submitted {job_type} job from {user_id}")
    else:
        print(f"Failed to submit: {resp.text}")
    time.sleep(1)
