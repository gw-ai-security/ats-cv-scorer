from .ats_scoring_dataset import parse as ats_scoring_dataset
from .resume_job_matching import parse as resume_job_matching
from .resume_data_ranking import parse as resume_data_ranking
from .job_descriptions_2025 import parse as job_descriptions_2025
from .job_skill_set import parse as job_skill_set


ADAPTERS = {
    "ats_scoring_dataset": ats_scoring_dataset,
    "resume_job_matching": resume_job_matching,
    "resume_data_ranking": resume_data_ranking,
    "job_descriptions_2025": job_descriptions_2025,
    "job_skill_set": job_skill_set,
}

__all__ = ["ADAPTERS"]
