from evaluation.reporter import Reporter
from evaluation.charts import ChartGenerator
import time

from retrieval import (
    search_grants,
    calculate_matches
)

from evaluation.benchmark import (
    load_benchmarks,
    load_ground_truth
)

from evaluation.metrics import (
    hit_rate,
    precision_at_k,
    recall_at_k,
    mean_reciprocal_rank
)


class Evaluator:

    def __init__(self):

        self.benchmarks = load_benchmarks()
        self.ground_truth = load_ground_truth()

        self.hit_rates = []
        self.precisions = []
        self.recalls = []
        self.mrr_scores = []
        self.latencies = []

        self.results = []

        self.reporter = Reporter()
        self.chart_generator = ChartGenerator()

    def print_query_results(
        self,
        benchmark,
        top5,
        expected,
        hit,
        precision,
        recall,
        mrr,
        latency
    ):

        print(f"\nQuery {benchmark['id']}")

        print("\nRetrieved:")

        for rank, result in enumerate(top5, start=1):
            print(f"{rank}. {result[0]} ({result[1]:.4f})")

        print("\nExpected:")

        for grant in expected:
            print("-", grant)

        print(f"\nHit Rate: {hit}")
        print(f"Precision@5: {precision:.2f}")
        print(f"Recall@5: {recall:.2f}")
        print(f"MRR: {mrr:.2f}")
        print(f"Latency: {latency:.4f} seconds")

    def save_reports(self):

        metrics = {
            "hit_rate": sum(self.hit_rates) / len(self.hit_rates),
            "precision_at_5": sum(self.precisions) / len(self.precisions),
            "recall_at_5": sum(self.recalls) / len(self.recalls),
            "mrr": sum(self.mrr_scores) / len(self.mrr_scores),
            "average_latency": sum(self.latencies) / len(self.latencies),
            "total_queries": len(self.benchmarks)
        }

        self.reporter.save_metrics(metrics)
        self.reporter.save_markdown_report(metrics)
        self.reporter.save_results_csv(self.results)

        self.chart_generator.generate_all(metrics)

    def run(self):

        print("=" * 60)
        print("Running Retrieval Evaluation")
        print("=" * 60)

        for benchmark in self.benchmarks:

            start = time.perf_counter()

            df = search_grants(
                min_funding=0,
                category="All",
                organization="All",
                eligibility="All"
            )

            results = calculate_matches(
                benchmark["query"],
                df
            )

            end = time.perf_counter()

            latency = end - start
            self.latencies.append(latency)

            results.sort(
                key=lambda x: x[1],
                reverse=True
            )

            top5 = results[:5]

            retrieved = [result[0] for result in top5]
            expected = list(self.ground_truth[benchmark["id"]])

            hit = hit_rate(retrieved, expected)
            precision = precision_at_k(retrieved, expected)
            recall = recall_at_k(retrieved, expected)
            mrr = mean_reciprocal_rank(retrieved, expected)

            self.hit_rates.append(hit)
            self.precisions.append(precision)
            self.recalls.append(recall)
            self.mrr_scores.append(mrr)

            self.print_query_results(
                benchmark,
                top5,
                expected,
                hit,
                precision,
                recall,
                mrr,
                latency
            )

            self.results.append([
                benchmark["id"],
                benchmark["query"],
                ", ".join(retrieved),
                ", ".join(expected),
                hit,
                round(precision, 2),
                round(recall, 2),
                round(mrr, 2),
                round(latency, 4)
            ])

        self.save_reports()