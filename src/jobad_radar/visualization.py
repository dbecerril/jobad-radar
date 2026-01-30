from typing import Dict
import matplotlib.pyplot as plt


def plot_top_frequencies(
    freqs: Dict[str, int],
    *,
    title: str,
    top_n: int = 10,
):
    """
    Simple bar chart for top-N frequency items.
    """

    if not freqs:
        print("No data to plot.")
        return

    items = sorted(freqs.items(), key=lambda x: x[1], reverse=True)[:top_n]
    labels, values = zip(*items)

    plt.figure(figsize=(8, 4))
    plt.bar(labels, values)
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
