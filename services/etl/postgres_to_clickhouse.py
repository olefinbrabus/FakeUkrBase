from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Iterable, List, Dict, Any

import psycopg2
import psycopg2.extras
from clickhouse_driver import Client

logger = logging.getLogger("etl_pg_to_ch")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


@dataclass
class DBConfig:
    # Postgres
    pg_host: str
    pg_port: int
    pg_db: str
    pg_user: str
    pg_password: str

    # ClickHouse
    ch_host: str
    ch_port: int
    ch_db: str
    ch_user: str
    ch_password: str

    batch_size: int = 10_000


def load_config() -> DBConfig:
    return DBConfig(
        pg_host=os.getenv("POSTGRES_HOST", "localhost"),
        pg_port=int(os.getenv("POSTGRES_PORT", "5432")),
        pg_db=os.getenv("POSTGRES_DB", "fakeukrbase"),
        pg_user=os.getenv("POSTGRES_USER", "fakeukrbase"),
        pg_password=os.getenv("POSTGRES_PASSWORD", "fakeukrbase"),
        ch_host=os.getenv("CLICKHOUSE_HOST", "localhost"),
        ch_port=int(os.getenv("CLICKHOUSE_PORT", "9000")),
        ch_db=os.getenv("CLICKHOUSE_DB", "fakeukrbase"),
        ch_user=os.getenv("CLICKHOUSE_USER", "fakeukrbase_ch"),
        ch_password=os.getenv("CLICKHOUSE_PASSWORD", "fakeukrbase_ch"),
    )


def get_pg_conn(cfg: DBConfig):
    conn = psycopg2.connect(
        host=cfg.pg_host,
        port=cfg.pg_port,
        dbname=cfg.pg_db,
        user=cfg.pg_user,
        password=cfg.pg_password,
    )
    return conn


def get_ch(cfg: DBConfig) -> Client:
    return Client(
        host=cfg.ch_host,
        port=cfg.ch_port,
        database=cfg.ch_db,
        user=cfg.ch_user,
        password=cfg.ch_password,
        settings={"use_numpy": False},
    )


def truncate(ch: Client) -> None:
    ch.execute("TRUNCATE TABLE IF EXISTS dim_employee")
    ch.execute("TRUNCATE TABLE IF EXISTS dim_job")
    ch.execute("TRUNCATE TABLE IF EXISTS salary_fact")
    logger.info("ClickHouse tables truncated.")


def extract(pg_conn, query: str, batch_size: int) -> Iterable[List[Dict[str, Any]]]:
    with pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(query)
        while True:
            chunk = cur.fetchmany(batch_size)
            if not chunk:
                break
            yield [dict(row) for row in chunk]


def run_etl(full_reload: bool = False) -> None:
    cfg = load_config()
    pg = get_pg_conn(cfg)
    ch = get_ch(cfg)

    try:
        if full_reload:
            truncate(ch)

        # dim_employee
        emp_q = """
            SELECT 
                id AS employee_id,
                sex,
                first_name,
                middle_name,
                second_name,
                email,
                address_uk,
                populated_type,
                birthdate
            FROM employees
            ORDER BY id
        """

        total_emps = 0
        for batch in extract(pg, emp_q, cfg.batch_size):
            data = []
            for r in batch:
                second = str(r.get("second_name") or "").strip()
                first = str(r.get("first_name") or "").strip()
                middle = str(r.get("middle_name") or "").strip()

                full_name_parts = [second, first, middle]
                full_name = " ".join(p for p in full_name_parts if p)

                data.append(
                    [
                        int(r["employee_id"]),
                        str(r.get("sex") or ""),
                        full_name,
                        str(r.get("email") or ""),
                        str(r.get("address_uk") or ""),
                        str(r.get("populated_type") or ""),
                        r.get("birthdate"),  # psycopg2 date -> ClickHouse Date
                    ]
                )

            if data:
                ch.execute(
                    """
                    INSERT INTO dim_employee
                    (employee_id, sex, full_name, email, address_uk, populated_type, birthdate)
                    VALUES
                    """,
                    data,
                )
                total_emps += len(data)

        logger.info("dim_employee → %d rows loaded.", total_emps)

        # dim_job
        job_q = """
            SELECT 
                id AS job_id,
                name,
                qualification,
                address
            FROM jobs
            ORDER BY id
        """

        total_jobs = 0
        for batch in extract(pg, job_q, cfg.batch_size):
            data = [
                [
                    int(r["job_id"]),
                    str(r.get("name") or ""),
                    str(r.get("qualification") or ""),
                    str(r.get("address") or ""),  # нормализация None -> ""
                ]
                for r in batch
            ]

            if data:
                ch.execute(
                    """
                    INSERT INTO dim_job(job_id, name, qualification, address)
                    VALUES
                    """,
                    data,
                )
                total_jobs += len(data)

        logger.info("dim_job → %d rows loaded.", total_jobs)

        # salary_fact
        sal_q = """
            SELECT 
                employee_id,
                job_id,
                month,
                gross_amount,
                bonus_amount,
                penalty_amount,
                is_delayed,
                delay_days,
                pay_date
            FROM salaries
            ORDER BY employee_id, month
        """

        total_sal = 0
        for batch in extract(pg, sal_q, cfg.batch_size):
            data = [
                [
                    int(r["employee_id"]),
                    int(r["job_id"]),
                    r.get("month"),
                    float(r.get("gross_amount") or 0.0),
                    float(r.get("bonus_amount") or 0.0),
                    float(r.get("penalty_amount") or 0.0),
                    1 if r.get("is_delayed") else 0,
                    int(r.get("delay_days") or 0),
                    r.get("pay_date"),
                ]
                for r in batch
            ]

            if data:
                ch.execute(
                    """
                    INSERT INTO salary_fact
                    (employee_id, job_id, month, gross, bonus, penalty, is_delayed, delay_days, pay_date)
                    VALUES
                    """,
                    data,
                )
                total_sal += len(data)

        logger.info("salary_fact → %d rows loaded.", total_sal)
        logger.info("ETL FINISHED")

    finally:
        pg.close()
