import json
import csv
from pathlib import Path


class Reporter:

    def __init__(self):

        self.output_dir = Path("evaluation/results")
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_metrics(self, metrics):

        output_file = self.output_dir / "metrics.json"

        with open(output_file, "w") as f:
            json.dump(
                metrics,
                f,
                indent=4
            )

        print(f"Saved metrics to {output_file}")

    def save_results_csv(self, results):

        output_file = self.output_dir / "retrieval_results.csv"

        with open(output_file, "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([
                "Query ID",
                "Query",
                "Retrieved Grants",
                "Expected Grants",
                "Hit Rate",
                "Precision@5",
                "Recall@5",
                "MRR",
                "Latency (s)"
            ])

            writer.writerows(results)

        print(f"Saved retrieval results to {output_file}")

    def save_markdown_report(self, metrics):

        output_file = self.output_dir / "evaluation_report.md"

        report = f"""# Grant Match AI Evaluation Report

## Retrieval Metrics

| Metric | Value |
|--------|-------|
| Hit Rate | {metrics["hit_rate"]:.2f} |
| Precision@5 | {metrics["precision_at_5"]:.2f} |
| Recall@5 | {metrics["recall_at_5"]:.2f} |
| MRR | {metrics["mrr"]:.2f} |
| Average Latency (s) | {metrics["average_latency"]:.4f} |

## Evaluation Summary

- Total Benchmark Queries: {metrics["total_queries"]}
- Retrieval Model: SentenceTransformer (all-MiniLM-L6-v2)
- Vector Similarity: Cosine Similarity
- Database: SQLite
- Evaluation Dataset: Human-validated benchmark queries
"""

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"Saved report to {output_file}")