import pandas as pd

from core.models import SalaryPayment


def salary_to_dataframe(all_persons_salaries_list: list[list[SalaryPayment]]) -> pd.DataFrame:
    # return pd.DataFrame({f"{i}":salary_list for i, v in enumerate(salary_list)})
    rows: list[dict] = []

    for employee_idx, payments in enumerate(all_persons_salaries_list):
        for p in payments:
            rows.append({
                "employee_idx": employee_idx,

                "month": pd.to_datetime(p.month),
                "gross_amount": float(p.gross_amount),
                # "net_amount": float(p.net_amount or -1.0),
                "bonus_amount": float(p.bonus_amount),
                "penalty_amount": float(p.penalty_amount),
                "is_delayed": bool(p.is_delayed),
                "delay_days": int(p.delay_days),
                "pay_date": pd.to_datetime(p.pay_date) if p.pay_date else None,

            })

    return pd.DataFrame(rows)