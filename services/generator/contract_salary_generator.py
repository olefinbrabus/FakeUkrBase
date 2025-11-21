from decimal import Decimal, ROUND_HALF_UP

from config import base_random
from core.countries_data.ukraine.job_dict import JOB_FACTORS, QUAL_LEVELS, SECTOR_BASE
from core.enums import QualificationType

POPULATE_AREA_COEF = {
    "village": 0.6,
    "urban_settlement": 0.8,
    "city": 1.0,
    "capital": 1.1,
    "remote": 1.1,
}


def experience_coef(years: int) -> float:
    years = max(0, min(years, 40))
    first = min(years, 10)
    rest = max(0, years - 10)
    return 1.0 + 0.03 * first + 0.015 * rest


def variation() -> float:
    x = base_random.normalvariate(1.0, 0.15)
    return max(0.7, min(1.4, x))


def calculate_average_payment(
    job_name: str,
    qualification: QualificationType,
    populate_area_type: str,
    employee_stage: int,
) -> Decimal:
    job_data = JOB_FACTORS[job_name]
    sector = job_data["cluster"]

    base = SECTOR_BASE[sector]

    raw = (
        base
        * job_data["salary_coef"]
        * QUAL_LEVELS[qualification]
        * experience_coef(employee_stage)
        * POPULATE_AREA_COEF[populate_area_type]
        * variation()
    )

    return Decimal(str(raw)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


if __name__ == "__main__":
    [
        print(
            calculate_average_payment(
                populate_area_type="village",
                qualification=QualificationType.junior,
                job_name="Програміст",
                employee_stage=4,
            )
        )
        for _ in range(100)
    ]
