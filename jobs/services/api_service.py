import requests

API_URL = "https://remoteok.com/api"


def search_jobs(keyword=None):
    try:
        response = requests.get(
            API_URL,
            headers={
                "User-Agent": "Mozilla/5.0",
            },
            timeout=10,
        )

        response.raise_for_status()
    except Exception as e:
        return []
    data = response.json()

    jobs = data[1:]

    if keyword:
        keyword = keyword.lower()

        jobs = [
            job
            for job in jobs
            if keyword in job.get("position", "").lower()
            or keyword in job.get("company", "").lower()
            or keyword in " ".join(job.get("tags", [])).lower()
        ]

    normalized_jobs = []

    for job in jobs:
        normalized_jobs.append({
            "title": job.get("position"),
            "company": job.get("company"),
            "location": job.get("location"),
            "url": job.get("url"),
            "description": job.get("description"),
            "tags": job.get("tags", []),
        })

    return normalized_jobs