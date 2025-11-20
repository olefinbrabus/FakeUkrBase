from config import base_random
from core.countries_data.ukraine.job_dict import JOB_FACTORS

def create_job(populate_area_type):
    is_remote_work = base_random.choices([True, False],weights=[0.1, 0.8], k=1)[0]

    job_by_location: list[str] = get_jobs_for_location(
        "remote" if is_remote_work else populate_area_type)

    return choose_job_by_popularity(job_by_location)



def get_jobs_for_location(location: str, *, only_strict: bool = False) -> list[str]:
    result = []
    for job_name, data in JOB_FACTORS.items():
        allowed = data["allowed_locations"]
        if only_strict:
            if allowed == {location}:
                result.append(job_name)
        else:
            if location in allowed:
                result.append(job_name)
    return result

def choose_job_by_popularity(jobs: list[str]) -> str:
    if not jobs:
        raise ValueError("list of jobs is empty")

    weights = [JOB_FACTORS[j]["popularity_coef"] for j in jobs]
    return  base_random.choices(jobs, weights=weights, k=1)[0]

if __name__ == "__main__":
    [print(create_job(populate_area_type="city")) for _ in range(100)]

