import logging
from decimal import Decimal
from collections.abc import Callable
from progress.bar import ShadyBar

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import EmployeeDB, JobDB, SalaryDB
from .session import SessionLocal

logger = logging.getLogger(__name__)


def save_frames_to_db(
    persons_df: pd.DataFrame,
    salary_df: pd.DataFrame,
    *,
    session_factory: Callable[[], Session] = SessionLocal,
) -> None:
    session = session_factory()
    try:
        job_cache: dict[tuple[str, str, str | None], JobDB] = {}
        gen_id_to_db_id: dict[int, int] = {}

        persons_total = len(persons_df.index)
        salaries_total = len(salary_df.index)

        persons_bar = ShadyBar(
            message="Saving employees in Postgres",
            max=persons_total,
            suffix="%(percent)d%% | %(index)d/%(max)d | elapsed: %(elapsed_td)s | eta: %(eta_td)s",
        )
        try:
            for _, row in persons_df.iterrows():
                generated_id = int(row["id"])

                db_emp = EmployeeDB(
                    sex=row.get("sex"),
                    first_name=row.get("first_name"),
                    middle_name=row.get("middle_name"),
                    second_name=row.get("second_name"),
                    first_name_en=row.get("first_name_eng_lang"),
                    middle_name_en=row.get("middle_name_eng_lang"),
                    second_name_en=row.get("second_name_eng_lang"),
                    email=row.get("email_address"),
                    address_uk=row.get("address"),
                    address_en=row.get("address_eng_lang"),
                    populated_type=row.get("type_populated_area"),
                    contract_payment=row.get("contract_payment"),
                    birthdate=(
                        pd.to_datetime(row["birthdate"]).date()
                        if pd.notna(row.get("birthdate"))
                        else None
                    ),
                    phone_number=(
                        str(row.get("phone_number"))
                        if row.get("phone_number") is not None
                        else None
                    ),
                    working_email=row.get("working_email_address"),
                    working_phone=(
                        str(row.get("working_phone_number"))
                        if row.get("working_phone_number") is not None
                        else None
                    ),
                )
                session.add(db_emp)
                session.flush()
                gen_id_to_db_id[generated_id] = db_emp.id
                persons_bar.next()
        finally:
            persons_bar.finish()

        session.commit()

        def get_or_create_job(
            name: str, qualification: str, address: str | None
        ) -> JobDB:
            key = (name, qualification, address)
            if key in job_cache:
                return job_cache[key]

            job = (
                session.query(JobDB)
                .filter(
                    JobDB.name == name,
                    JobDB.qualification == qualification,
                    JobDB.address == address,
                )
                .one_or_none()
            )
            if job is None:
                job = JobDB(name=name, qualification=qualification, address=address)
                session.add(job)
                session.flush()

            job_cache[key] = job
            return job

        salary_df = salary_df.copy()
        salary_df["month"] = pd.to_datetime(salary_df["month"]).dt.date
        salary_df = salary_df.drop_duplicates(
            subset=["person_id", "month"], keep="last"
        )

        existing: set[tuple[int, object]] = set(
            session.execute(select(SalaryDB.employee_id, SalaryDB.month)).all()
        )

        salary_bar = ShadyBar(
            message="Saving salaries",
            max=salaries_total,
            suffix="%(percent)d%% | %(index)d/%(max)d | elapsed: %(elapsed_td)s | eta: %(eta_td)s",
        )
        try:
            for _, row in salary_df.iterrows():
                generated_id = int(row["person_id"])
                employee_id = gen_id_to_db_id[generated_id]

                month = row["month"]
                key = (int(employee_id), month)

                if key in existing:
                    salary_bar.next()
                    continue

                job = get_or_create_job(
                    row.get("job_name"),
                    row.get("job_qualification"),
                    row.get("job_address"),
                )

                salary = SalaryDB(
                    employee_id=employee_id,
                    job_id=job.id,
                    month=month,
                    gross_amount=Decimal(str(row["gross_amount"])),
                    bonus_amount=Decimal(str(row["bonus_amount"])),
                    penalty_amount=Decimal(str(row["penalty_amount"])),
                    is_delayed=bool(row["is_delayed"]),
                    delay_days=int(row["delay_days"]),
                    pay_date=pd.to_datetime(row["pay_date"]).date(),
                )
                session.add(salary)

                existing.add(key)
                salary_bar.next()
        finally:
            salary_bar.finish()

        session.commit()

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
