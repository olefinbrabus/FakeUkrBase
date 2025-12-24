from core.countries_data.ukraine.job_dict import JOB_FACTORS
from core.models import Job
import logging

logger = logging.getLogger(__name__)


def validate_job(job: Job):
    if job.name not in JOB_FACTORS.keys():
        logger.log(logging.ERROR, f"Job {job.name} not found")
        return False
    return True


def validate_jobs(jobs: list[Job]):
    return all(validate_job(job) for job in jobs)
