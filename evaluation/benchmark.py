import json


def load_benchmarks():

    with open("evaluation/benchmark_queries.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_ground_truth():

    with open("evaluation/ground_truth.json", "r", encoding="utf-8") as f:
        ground_truth = json.load(f)

    return {
        int(query_id): set(expected_grants)
        for query_id, expected_grants in ground_truth.items()
    }