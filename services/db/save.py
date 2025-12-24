import logging
from decimal import Decimal
from typing import Callable

import pandas as pd
from sqlalchemy.orm import Session

from .models import EmployeeDB, JobDB, SalaryDB
from .session import SessionLocal

logger = logging.getLogger(__name__)


def save_frames_to_db(
    persons_df: pd.DataFrame,
    salary_df: pd.DataFrame,
    session: Callable[[], Session] = SessionLocal,
) -> None:
    try:
        job_cache: dict[tuple[str, str, str | None], JobDB] = {}

        gen_id_to_db_id: dict[int, int] = {}

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
                    if "birthdate" in row and pd.notna(row["birthdate"])
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

        for _, row in salary_df.iterrows():
            generated_id = int(row["person_id"])
            employee_id = gen_id_to_db_id[generated_id]

            job_name = row.get("job_name")
            job_qual = row.get("job_qualification")
            job_addr = row.get("job_address")
            job = get_or_create_job(job_name, job_qual, job_addr)

            month = pd.to_datetime(row["month"]).date()
            pay_date = pd.to_datetime(row["pay_date"]).date()

            salary = SalaryDB(
                employee_id=employee_id,
                job_id=job.id,
                month=month,
                gross_amount=Decimal(str(row["gross_amount"])),
                bonus_amount=Decimal(str(row["bonus_amount"])),
                penalty_amount=Decimal(str(row["penalty_amount"])),
                is_delayed=bool(row["is_delayed"]),
                delay_days=int(row["delay_days"]),
                pay_date=pay_date,
            )
            session.add(salary)

        session.commit()

    except Exception as e:
        logger.log(logging.ERROR, e)
        session.rollback()
        raise
    finally:
        session.close()
