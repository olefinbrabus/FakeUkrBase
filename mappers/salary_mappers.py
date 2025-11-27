import pandas as pd

from core.models import SalaryPayment, AbstractEmployee


# def salaries_to_dataframe(all_persons_salaries_list: list[list[SalaryPayment]]) -> pd.DataFrame:
#     # return pd.DataFrame({f"{i}":salary_list for i, v in enumerate(salary_list)})
#     rows: list[dict] = []
#
#
#     for employee_id, payments in enumerate(all_persons_salaries_list):
#         for p in payments:
#             rows.append({
#                 "employee_id": employee_id,
#
#                 "month": pd.to_datetime(p.month),
#                 "gross_amount": float(p.gross_amount),
#                 # "net_amount": float(p.net_amount or -1.0),
#                 "bonus_amount": float(p.bonus_amount),
#                 "penalty_amount": float(p.penalty_amount),
#                 "is_delayed": bool(p.is_delayed),
#                 "delay_days": int(p.delay_days),
#                 "pay_date": pd.to_datetime(p.pay_date) if p.pay_date else None,
#
#             })
#
#     return pd.DataFrame(rows)


def salaries_to_dataframe(
    employees: list[AbstractEmployee],
    all_persons_salaries_list: list[list[SalaryPayment]],
) -> pd.DataFrame:
    rows = []

    for emp, payments in zip(employees, all_persons_salaries_list):
        person_id = emp.id

        job_name = emp.job.name
        job_qualification = str(emp.job.qualification)
        job_address = emp.job.address

        for p in payments:
            rows.append(
                {
                    "person_id": person_id,
                    "job_name": job_name,
                    "job_qualification": job_qualification,
                    "job_address": job_address,
                    "month": pd.to_datetime(p.month),
                    "gross_amount": float(p.gross_amount),
                    "bonus_amount": float(p.bonus_amount),
                    "penalty_amount": float(p.penalty_amount),
                    "is_delayed": bool(p.is_delayed),
                    "delay_days": int(p.delay_days),
                    "pay_date": pd.to_datetime(p.pay_date),
                }
            )

    df = pd.DataFrame(rows)
    return df
