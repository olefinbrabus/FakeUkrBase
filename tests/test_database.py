from services.db.models import EmployeeDB, JobDB, SalaryDB
from services.db.save import save_frames_to_db


def test_save_frames_inserts_all(session_factory, valid_employee_frame, valid_salary_frame):
    save_frames_to_db(
        valid_employee_frame,
        valid_salary_frame,
        session_factory=session_factory,
    )

    s = session_factory()
    try:
        assert s.query(EmployeeDB).count() == 1
        assert s.query(JobDB).count() == 1
        assert s.query(SalaryDB).count() == 12
    finally:
        s.close()


def test_jobs_are_reused(session_factory, valid_employee_frame, valid_salary_frame):
    salary_df = valid_salary_frame.copy(deep=True)
    for i, (idx, _) in enumerate(salary_df.iterrows(), start=1):
        salary_df.loc[idx, "month"] = f"2025-{i:02d}-01"
    save_frames_to_db(valid_employee_frame, salary_df, session_factory=session_factory)

    s = session_factory()
    try:
        assert s.query(JobDB).count() == 1
        assert s.query(SalaryDB).count() == 12
    finally:
        s.close()