import pandas as pd
import seaborn as sns

from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from config import SESSION_PERSON_FILE_DIR, SESSION_SALARY_FILE_DIR


def load():
    persons = pd.read_parquet(SESSION_PERSON_FILE_DIR)
    salary = pd.read_parquet(SESSION_SALARY_FILE_DIR)
    df = salary.merge(persons, left_on="person_id", right_on="id", how="left")
    return df


def run_descriptive(df: pd.DataFrame):
    stats = df[["gross_amount", "bonus_amount", "penalty_amount"]].describe()
    delays = df["is_delayed"].value_counts(normalize=True) * 100

    return {"summary": stats, "delay_distribution": delays}


def run_correlations(df: pd.DataFrame):
    numeric = df.select_dtypes(include="number")
    corr_matrix = numeric.corr(method="spearman")
    return corr_matrix


def run_regression(df: pd.DataFrame):
    data = df.dropna(subset=["length_of_work", "gross_amount"])
    X = data[["length_of_work"]]
    y = data["gross_amount"]

    model = LinearRegression()
    model.fit(X, y)

    return {
        "coef": model.coef_[0],
        "intercept": model.intercept_,
        "r2_score": model.score(X, y),
    }


def run_timeseries(df):
    ts = df.groupby("month")["gross_amount"].mean().sort_index()
    model = ExponentialSmoothing(ts).fit()
    forecast = model.forecast(6)

    return {"trend": ts, "forecast": forecast}


def run_clustering(df):
    subset = df[["gross_amount", "length_of_work"]].dropna()
    model = KMeans(n_clusters=3, random_state=42)
    subset["cluster"] = model.fit_predict(subset)

    return subset, model.cluster_centers_


def run_anomaly(df):
    model = IsolationForest(random_state=42)
    df["anomaly"] = model.fit_predict(df[["gross_amount"]])
    return df[df["anomaly"] == -1]


def run_statistics(method="all", *, show_plots_flag: bool = True):
    df = load()

    results = {}

    if method in ("descriptive", "all"):
        results["descriptive"] = run_descriptive(df)

    if method in ("correlation", "all"):
        results["correlation"] = run_correlations(df)

    if method in ("regression", "all"):
        results["regression"] = run_regression(df)

    if method in ("timeseries", "all"):
        results["timeseries"] = run_timeseries(df)

    if method in ("clustering", "all"):
        results["clustering"] = run_clustering(df)

    if method in ("anomaly", "all"):
        results["anomaly"] = run_anomaly(df)

    if show_plots_flag:
        show_plots(df)

    show_plots(df)
    report_text = interpret(results)

    return results, report_text


def show_plots(df: pd.DataFrame):

    plt.figure(figsize=(10, 4))
    sns.boxplot(x=df["gross_amount"])
    plt.title("Розподіл заробітних плат (Боксплот)")
    plt.xlabel("Заробітна плата (UAH)")
    plt.show()
    plt.close()

    plt.figure(figsize=(10, 4))
    sns.histplot(df["bonus_amount"], kde=True, bins=20)
    plt.title("Гістограма премій")
    plt.xlabel("Премія (UAH)")
    plt.ylabel("Кількість")
    plt.show()
    plt.close()

    df_sorted = df.sort_values("month")
    plt.figure(figsize=(10, 4))
    sns.lineplot(x="month", y="gross_amount", data=df_sorted)
    plt.title("Тренд середньої зарплати по місяцях")
    plt.xticks(rotation=45)
    plt.ylabel("Середня зарплата (UAH)")
    plt.show()
    plt.close()


def interpret(results: dict) -> str:
    lines: list[str] = []

    reg = results.get("regression")
    if reg is not None:
        r2 = reg.get("r2_score")
        coef = reg.get("coef")
        if r2 is not None:
            if r2 > 0.6:
                lines.append(
                    f"1) Регресійний аналіз\n"
                    f"Модель демонструє сильну залежність рівня заробітної плати від стажу роботи.\n"
                    f"Коефіцієнт детермінації R² = {r2:.3f}, "
                    f"коефіцієнт при стажі = {coef:.2f} (грн за одиницю стажу)."
                )
            else:
                lines.append(
                    f"1) Регресійний аналіз\n"
                    f"Залежність заробітної плати від стажу роботи є відносно слабкою.\n"
                    f"Коефіцієнт детермінації R² = {r2:.3f}, "
                    f"коефіцієнт при стажі = {coef:.2f}."
                )

    corr = results.get("correlation")
    if corr is not None and "gross_amount" in corr.index:

        def safe_corr(col: str):
            try:
                return float(corr.loc["gross_amount", col])
            except Exception:
                return None

        c_bonus = safe_corr("bonus_amount")
        c_penalty = safe_corr("penalty_amount")

        parts = []
        if c_bonus is not None:
            parts.append(f"кореляція із преміями = {c_bonus:.2f}")
        if c_penalty is not None:
            parts.append(f"кореляція із штрафами = {c_penalty:.2f}")

        if parts:
            lines.append(
                "2) Кореляційний аналіз\n"
                "Спостерігається наступна кореляція заробітної плати з іншими показниками: "
                + "; ".join(parts)
                + "."
            )

    desc = results.get("descriptive")
    if desc is not None:
        summary = desc.get("summary")
        delays = desc.get("delay_distribution")
        if summary is not None:
            mean_salary = summary.loc["mean", "gross_amount"]
            median_salary = summary.loc["50%", "gross_amount"]
            lines.append(
                "3) Описова статистика\n"
                f"Середня заробітна плата = {mean_salary:.2f} грн, "
                f"медіана = {median_salary:.2f} грн."
            )
        if delays is not None:
            delayed_pct = float(delays.get(1, 0.0))
            lines.append(
                f"Частка виплат із затримкою становить приблизно {delayed_pct:.1f} % від усіх виплат."
            )

    cl = results.get("clustering")
    if cl is not None:
        _, centers = cl
        lines.append(
            "4) Кластеризація працівників\n"
            "Було виділено кілька кластерів працівників за стажем та рівнем оплати праці.\n"
            f"Координати центрів кластерів (стаж, зарплата): {centers}."
        )

    an = results.get("anomaly")
    if an is not None:
        n_anom = len(an)
        lines.append(
            "5) Виявлення аномалій\n"
            f"Виявлено {n_anom} записів із нетиповими значеннями заробітної плати "
            "або пов'язаними показниками. Їх доцільно перевірити окремо."
        )

    if not lines:
        return (
            "Аналітичний звіт поки що порожній — не вдалося інтерпретувати результати."
        )

    return "\n\n".join(lines)