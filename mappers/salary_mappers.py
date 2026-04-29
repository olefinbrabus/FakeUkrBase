import pandas as pd

from core.models import SalaryPayment, AbstractEmployee


def salaries_to_dataframe(
    employees: list[AbstractEmployee],
    all_persons_salaries_list: list[list[SalaryPayment]],
) -> pd.DataFrame:
    rows = []

    for emp, year_salaries in zip(employees, all_persons_salaries_list):
        job_name = emp.job.name
        job_qualification = str(emp.job.qualification)
        job_address = emp.job.address

        for salary in year_salaries:
            rows.append(
                {
                    "person_id": salary.person_id,
                    "job_name": job_name,
                    "job_qualification": job_qualification,
                    "job_address": job_address,
                    "month": pd.to_datetime(salary.month),
                    "gross_amount": float(salary.gross_amount),
                    "bonus_amount": float(salary.bonus_amount),
                    "penalty_amount": float(salary.penalty_amount),
                    "is_delayed": bool(salary.is_delayed),
                    "delay_days": int(salary.delay_days),
                    "pay_date": pd.to_datetime(salary.pay_date),
                }
            )

    df = pd.DataFrame(rows)
    return df
