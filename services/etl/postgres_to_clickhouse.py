from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Iterable, Sequence, Callable, Any, List

import psycopg2
from clickhouse_driver import Client

logger = logging.getLogger("etl_pg_to_ch")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


@dataclass(frozen=True)
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
    return psycopg2.connect(
        host=cfg.pg_host,
        port=cfg.pg_port,
        dbname=cfg.pg_db,
        user=cfg.pg_user,
        password=cfg.pg_password,
    )


def get_ch(cfg: DBConfig) -> Client:
    return Client(
        host=cfg.ch_host,
        port=cfg.ch_port,
        database=cfg.ch_db,
        user=cfg.ch_user,
        password=cfg.ch_password,
        settings={
            "use_numpy": False,
            "max_insert_block_size": cfg.batch_size,
            "max_block_size": cfg.batch_size,
        },
    )


def truncate(ch: Client) -> None:
    ch.execute("TRUNCATE TABLE dim_employee")
    ch.execute("TRUNCATE TABLE dim_job")
    ch.execute("TRUNCATE TABLE salary_fact")
    logger.info("ClickHouse tables truncated.")


def extract_tuples(pg_conn, query: str, batch_size: int) -> Iterable[List[tuple]]:
    cur_name = "etl_cursor"
    with pg_conn.cursor(name=cur_name) as cur:
        cur.itersize = batch_size
        cur.execute(query)
        while True:
            rows = cur.fetchmany(batch_size)
            if not rows:
                break
            yield rows


def load_table(
    *,
    pg_conn,
    ch: Client,
    pg_query: str,
    ch_insert_sql: str,
    transform: Callable[[Sequence[tuple]], List[list]],
    batch_size: int,
    label: str,
) -> int:
    total = 0
    for rows in extract_tuples(pg_conn, pg_query, batch_size):
        payload = transform(rows)
        if payload:
            ch.execute(ch_insert_sql, payload, types_check=False)
            total += len(payload)
    logger.info("%s → %d rows loaded.", label, total)
    return total


def run_etl(full_reload: bool = False) -> None:
    cfg = load_config()
    pg = get_pg_conn(cfg)
    ch = get_ch(cfg)

    try:
        if full_reload:
            truncate(ch)
        else:
            logger.warning("full_reload=False: repeated runs will append duplicates to ClickHouse tables.")

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

        emp_insert = """
            INSERT INTO dim_employee
            (employee_id, sex, full_name, email, address_uk, populated_type, birthdate)
            VALUES
        """

        def tr_emp(rows: Sequence[tuple]) -> List[list]:
            out: List[list] = []
            for (
                employee_id,
                sex,
                first_name,
                middle_name,
                second_name,
                email,
                address_uk,
                populated_type,
                birthdate,
            ) in rows:
                second = (second_name or "").strip()
                first = (first_name or "").strip()
                middle = (middle_name or "").strip()
                full_name = " ".join(p for p in (second, first, middle) if p)

                out.append(
                    [
                        int(employee_id),
                        str(sex or ""),
                        full_name,
                        str(email or ""),
                        str(address_uk or ""),
                        str(populated_type or ""),
                        birthdate,
                    ]
                )
            return out

        load_table(
            pg_conn=pg,
            ch=ch,
            pg_query=emp_q,
            ch_insert_sql=emp_insert,
            transform=tr_emp,
            batch_size=cfg.batch_size,
            label="dim_employee",
        )

        job_q = """
            SELECT id AS job_id, name, qualification, address
            FROM jobs
            ORDER BY id
        """

        job_insert = """
            INSERT INTO dim_job (job_id, name, qualification, address)
            VALUES
        """

        def tr_job(rows: Sequence[tuple]) -> List[list]:
            out: List[list] = []
            for job_id, name, qualification, address in rows:
                out.append(
                    [
                        int(job_id),
                        str(name or ""),
                        str(qualification or ""),
                        str(address or ""),
                    ]
                )
            return out

        load_table(
            pg_conn=pg,
            ch=ch,
            pg_query=job_q,
            ch_insert_sql=job_insert,
            transform=tr_job,
            batch_size=cfg.batch_size,
            label="dim_job",
        )

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

        sal_insert = """
            INSERT INTO salary_fact
            (employee_id, job_id, month, gross, bonus, penalty, is_delayed, delay_days, pay_date)
            VALUES
        """

        def tr_sal(rows: Sequence[tuple]) -> List[list]:
            out: List[list] = []
            for (
                employee_id,
                job_id,
                month,
                gross_amount,
                bonus_amount,
                penalty_amount,
                is_delayed,
                delay_days,
                pay_date,
            ) in rows:
                out.append(
                    [
                        int(employee_id),
                        int(job_id),
                        month,
                        float(gross_amount or 0.0),
                        float(bonus_amount or 0.0),
                        float(penalty_amount or 0.0),
                        1 if is_delayed else 0,
                        int(delay_days or 0),
                        pay_date,
                    ]
                )
            return out

        load_table(
            pg_conn=pg,
            ch=ch,
            pg_query=sal_q,
            ch_insert_sql=sal_insert,
            transform=tr_sal,
            batch_size=cfg.batch_size,
            label="salary_fact",
        )

        logger.info("ETL FINISHED")

    finally:
        pg.close()