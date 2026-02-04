JOBS = {}

def update_job(job_id: str, status: str, message: str = None, result: bytes = None, error: str = None):
    if job_id not in JOBS:
        JOBS[job_id] = {}
    
    updates = {"status": status}
    if message: updates["message"] = message
    if result: updates["result"] = result
    if error: updates["error"] = error
    
    JOBS[job_id].update(updates)

def get_job(job_id: str):
    return JOBS.get(job_id)