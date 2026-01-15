import statistics
from collections import Counter

def calculate_stats(berries_names, growth_times):
    """
    Calculate min, max, mean, median, variance an frequency
    """
    if not growth_times:
        raise ValueError("There are no growth times.")

    freq = dict(Counter(growth_times))

    stats = {
        "berries_names": berries_names,
        "min_growth_time": min(growth_times),
        "max_growth_time": max(growth_times),
        "mean_growth_time": round(statistics.mean(growth_times), 2),
        "median_growth_time": round(statistics.median(growth_times), 2),
        "variance_growth_time": round(statistics.variance(growth_times), 2) if len(growth_times) > 1 else 0,
        "frequency_growth_time": freq
    }
    return stats
