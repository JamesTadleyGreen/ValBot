from typing import Tuple
import matplotlib.pyplot as plt


def create_graph(title, data: dict[str, Tuple[list[int], list[int]]]) -> None:
    # Data looks like {'Chicken': ([1,2,3], [10,3,2])}
    plt.title(f"A comparison of {title}")
    for player in data:
        xs, ys = data[player]
        plt.plot(xs, ys, label=player)
    plt.legend()
    plt.savefig("graph.png")
    plt.close()
