import statistics
from collections import Counter
import matplotlib.pyplot as plt
import io
import base64


def calculate_stats(berries_names, growth_times, freq=None):
    if not growth_times:
        raise ValueError("No growth_time data available.")
    if freq is None:
        freq = dict(Counter(growth_times))

    return {
        "berries_names": berries_names,
        "min_growth_time": min(growth_times),
        "max_growth_time": max(growth_times),
        "mean_growth_time": round(statistics.mean(growth_times), 2),
        "median_growth_time": round(statistics.median(growth_times), 2),
        "variance_growth_time": round(statistics.variance(growth_times), 2) if len(growth_times) > 1 else 0,
        "frequency_growth_time": freq
    }


def generate_histogram(growth_times):
    plt.figure(figsize=(8, 4))
    plt.hist(growth_times, bins=range(min(growth_times), max(growth_times) + 2), color='#A6CE39', edgecolor='black')
    plt.title("Histogram of Berry Growth Times")
    plt.xlabel("Growth Time")
    plt.ylabel("Frequency")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    html = f'<img src="data:image/png;base64,{img_base64}"/>'
    return html
