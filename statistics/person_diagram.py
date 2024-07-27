import matplotlib.pyplot as plt
import numpy as np

from dataframes.dataframe_person import PersonDataFrame


def phone_diagram(person_df: PersonDataFrame):
    plt.style.use("fast")
    persons_operators_counts = person_df.get_phone_operators_count()
    counts = list(persons_operators_counts.values())
    operators = [f"{key} {value}" for key, value in persons_operators_counts.items()]
    colors = ["blue", "yellow", "red"]

    # plot
    fig, ax = plt.subplots(dpi=300)
    fig.suptitle(
        f"Діаграма операторів телефонів зі\n{len(person_df)} користувачів",
        fontsize=12,
        fontweight="bold",
    )

    ax.pie(
        counts,
        labels=operators,
        colors=colors,
        labeldistance=0.6,
        radius=1.2,
        textprops=dict(fontsize=12, fontweight="bold"),
        explode=(tuple([0.01 for _ in counts])),
        wedgeprops={"linewidth": 1, "edgecolor": "black"},
    )
    plt.show()


def first_name_diagram(person_df: PersonDataFrame):
    plt.style.use("classic")
    plt.title("Статистика імен")
    first_names = [
        str(first_name).split(" ")[0] for first_name in person_df.dataframe["full name"]
    ]
