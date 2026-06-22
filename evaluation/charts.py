from pathlib import Path
import matplotlib.pyplot as plt


class ChartGenerator:

    def __init__(self):

        self.output_dir = Path("evaluation/results/charts")
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_bar_chart(
        self,
        title,
        value,
        max_value,
        filename
    ):

        plt.figure(figsize=(5, 4))

        plt.bar(
            [title],
            [value]
        )

        plt.ylim(0, max_value)

        plt.title(title)

        plt.ylabel("Score")

        plt.tight_layout()

        plt.savefig(
            self.output_dir / filename
        )

        plt.close()

    def generate_all(self, metrics):

        self.save_bar_chart(
            "Hit Rate",
            metrics["hit_rate"],
            1.0,
            "hit_rate.png"
        )

        self.save_bar_chart(
            "Precision@5",
            metrics["precision_at_5"],
            1.0,
            "precision_at_5.png"
        )

        self.save_bar_chart(
            "Recall@5",
            metrics["recall_at_5"],
            1.0,
            "recall_at_5.png"
        )

        self.save_bar_chart(
            "MRR",
            metrics["mrr"],
            1.0,
            "mrr.png"
        )

        self.save_bar_chart(
            "Average Latency",
            metrics["average_latency"],
            max(metrics["average_latency"] * 1.2, 0.1),
            "latency.png"
        )

        print("Saved evaluation charts to", self.output_dir)