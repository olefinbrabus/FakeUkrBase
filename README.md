# FakeUkrBase

Synthetic Ukrainian employee dataset generator with database storage, OLAP pipeline, and BI analytics support.

---

## Features

- Generate realistic synthetic Ukrainian personal & employment data  
- Salary simulation (delays, bonuses, penalties included)  
- Export to **Parquet / CSV / XLSX**
- PostgreSQL relational storage with **Alembic migrations**
- ETL → ClickHouse for OLAP analytics  
- BI dashboards via Metabase  

---

## Installation

```bash
git clone https://github.com/olefinbrabus/FakeUkrBase
cd FakeUkrBase
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Copy environment config:
```bash
cp .env.example .env

```
Edit .env to match your local setup.

---

## Run Infrastructure

Requires Docker.
```bash
docker compose up -d
```

Apply DB migrations:

```bash
alembic upgrade head
```

## Usage Examples

Generate employees
```bash```
```bash```
```bash
python main.py generate --count 100 -p abstractemployee --seed 42
```

Save generated data into PostgreSQL

```bash
python main.py save
```

Build OLAP layer in ClickHouse

```bash
python main.py olap --full
```

## Data Model

| Layer       | 	Storage	    | Tables                             |
|-------------|--------------|------------------------------------| 
| Source data | 	PostgreSQL	 | employees, jobs, salaries          |
| Analytics   | ClickHouse   | dim_employee, dim_job, salary_fact |


---

## BI Dashboard Ideas

Some insights possible after ETL:
- Salary distribution by qualification level
- Payroll anomalies (late payments, penalty patterns)
- Compensation comparison across settlements
- Yearly payroll change tracking
- Employee churn vs salary dynamics (future roadmap)

