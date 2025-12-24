from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Boolean,
    Date,
    Numeric,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .session import Base

PK_INT = BigInteger().with_variant(Integer, "sqlite")

class EmployeeDB(Base):
    __tablename__ = "employees"

    id = Column(PK_INT, primary_key=True, autoincrement=True)
    # external_id = Column(BigInteger, nullable=False, index=True)

    sex = Column(String, nullable=False)

    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    second_name = Column(String, nullable=False)

    first_name_en = Column(String)
    middle_name_en = Column(String)
    second_name_en = Column(String)

    email = Column(String, nullable=False)
    address_uk = Column(String)
    address_en = Column(String)
    populated_type = Column(String)

    birthdate = Column(Date, nullable=False)
    phone_number = Column(String)

    working_email = Column(String, nullable=True)
    working_phone = Column(String, nullable=True)

    contract_payment = Column(Numeric, nullable=False)

    salaries = relationship(
        "SalaryDB", back_populates="employee", cascade="all, delete-orphan"
    )


class JobDB(Base):
    __tablename__ = "jobs"

    id = Column(PK_INT, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    qualification = Column(String, nullable=False)
    address = Column(String)

    __table_args__ = (
        UniqueConstraint("name", "qualification", "address", name="uq_job"),
    )

    salaries = relationship("SalaryDB", back_populates="job")


class SalaryDB(Base):
    __tablename__ = "salaries"

    id = Column(PK_INT, primary_key=True, autoincrement=True)

    employee_id = Column(
        BigInteger, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False
    )
    job_id = Column(
        BigInteger, ForeignKey("jobs.id", ondelete="RESTRICT"), nullable=False
    )

    month = Column(Date, nullable=False)
    gross_amount = Column(Numeric(14, 2), nullable=False)
    # base_amount = Column(Numeric(14, 2), nullable=False)
    bonus_amount = Column(Numeric(14, 2), nullable=False)
    penalty_amount = Column(Numeric(14, 2), nullable=False)

    is_delayed = Column(Boolean, nullable=False)
    delay_days = Column(Integer, nullable=False)
    pay_date = Column(Date, nullable=False)

    employee = relationship("EmployeeDB", back_populates="salaries")
    job = relationship("JobDB", back_populates="salaries")

    __table_args__ = (
        UniqueConstraint("employee_id", "month", name="uq_salary_employee_month"),
    )
