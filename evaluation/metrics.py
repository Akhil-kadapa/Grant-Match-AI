def hit_rate(retrieved, expected):
    """
    Returns 1 if at least one retrieved grant
    appears in the expected set.
    """

    retrieved = set(retrieved)
    expected = set(expected)

    return int(len(retrieved & expected) > 0)


def precision_at_k(retrieved, expected):

    retrieved = set(retrieved)
    expected = set(expected)

    return len(retrieved & expected) / len(retrieved)

def recall_at_k(retrieved, expected):

    retrieved = set(retrieved)
    expected = set(expected)

    return len(retrieved & expected) / len(expected)

def mean_reciprocal_rank(retrieved, expected):
    """
    Returns the reciprocal rank of the first relevant result.
    """

    expected = set(expected)

    for rank, grant in enumerate(retrieved, start=1):
        if grant in expected:
            return 1 / rank

    return 0