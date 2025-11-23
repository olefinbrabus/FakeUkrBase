import calendar
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

from config import base_random
from core.countries_data.ukraine.job_dict import JOB_FACTORS
from core.countries_data.ukraine.salary_cluster_dict import CLUSTER_CONFIG
from core.models import AbstractEmployee, SalaryPayment


def _clamp(x: float, min_v: float, max_v: float) -> float:
    return max(min_v, min(max_v, x))


def _sample_share(mean: float, std: float) -> float:
    val = base_random.normalvariate(mean, std)
    return _clamp(val, 0.0, mean * 3)


def generate_salary_payments_for_year(
    employee: AbstractEmployee,
    year: int,
) -> list[SalaryPayment]:
    job_name = employee.job.name
    job_data = JOB_FACTORS.get(job_name)

    if not job_data:
        cluster = "other"
    else:
        cluster = job_data["cluster"]

    cfg = CLUSTER_CONFIG.get(cluster, CLUSTER_CONFIG["other"])

    base_monthly: Decimal = employee.contract_payment

    payments: list[SalaryPayment] = []

    for month in range(1, 13):
        month_date = date(year, month, 1)
        base_amount = base_monthly


        bonus_amount = Decimal("0.00")
        if base_random.random() < cfg.bonus_prob:
            share = _sample_share(cfg.bonus_share_mean, cfg.bonus_share_std)
            bonus_amount = (base_amount * Decimal(str(share))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


        penalty_amount = Decimal("0.00")
        if base_random.random() < cfg.penalty_prob:
            share = _sample_share(cfg.penalty_share_mean, cfg.penalty_share_std)
            penalty_amount = (base_amount * Decimal(str(share))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


        is_delayed = base_random.random() < cfg.delay_prob
        delay_days = 0
        if is_delayed:
            delay_days = base_random.randint(cfg.delay_days_min, cfg.delay_days_max)

        last_day = calendar.monthrange(year, month)[1]
        scheduled_pay_date = date(year, month, last_day)
        pay_date = scheduled_pay_date + timedelta(days=delay_days)

        gross = base_amount + bonus_amount - penalty_amount
        gross = gross.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        payment = SalaryPayment(
            month=month_date,
            gross_amount=gross,
            bonus_amount=bonus_amount,
            penalty_amount=penalty_amount,
            is_delayed=is_delayed,
            delay_days=delay_days,
            pay_date=pay_date,
        )
        payments.append(payment)

    return payments