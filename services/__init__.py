from .db.save import save_frames_to_db
from .etl.postgres_to_clickhouse import run_etl
from .generator import generate_persons, generate_year_salaries_per_each_employee
from .statistics.analytics_methods import run_statistics

__all__ = (save_frames_to_db, run_etl, generate_persons, run_statistics, generate_year_salaries_per_each_employee)