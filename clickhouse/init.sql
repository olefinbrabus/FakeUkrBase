CREATE DATABASE IF NOT EXISTS fakeukrbase;

CREATE TABLE IF NOT EXISTS fakeukrbase.dim_employee
(
  employee_id   UInt64,
  sex           String,
  full_name     String,
  email         String,
  address_uk    String,
  populated_type String,
  birthdate     Date,
  ingested_at   DateTime DEFAULT now()
)
ENGINE = ReplacingMergeTree(ingested_at)
ORDER BY employee_id;

CREATE TABLE IF NOT EXISTS fakeukrbase.dim_job
(
  job_id        UInt64,
  name          String,
  qualification String,
  address       String,
  ingested_at   DateTime DEFAULT now()
)
ENGINE = ReplacingMergeTree(ingested_at)
ORDER BY job_id;

CREATE TABLE IF NOT EXISTS fakeukrbase.salary_fact
(
  employee_id UInt64,
  job_id      UInt64,
  month       Date,
  gross       Float64,
  bonus       Float64,
  penalty     Float64,
  is_delayed  UInt8,
  delay_days  UInt16,
  pay_date    Date,
  ingested_at DateTime DEFAULT now()
)
ENGINE = ReplacingMergeTree(ingested_at)
ORDER BY (employee_id, job_id, month);