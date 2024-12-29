import math


class FrequencyBucket:
    freq_range: range
    amplitudes: list[float]

    def __init__(self, freq_range: range):
        self.freq_range = freq_range
        self.amplitudes = []

    def add_amplitude(self, amplitude: float):
        self.amplitudes.append(amplitude)

    def average(self) -> float:
        return sum(self.amplitudes) / len(self.amplitudes)

    def standard_deviation(self) -> float:
        avg = self.average()
        return math.sqrt(sum((x - avg) ** 2 for x in self.amplitudes) / len(self.amplitudes))
    
    def loud_counts(self, threshold: float) -> int:
        return len([x for x in self.amplitudes if x > threshold])


def create_freq_buckets(lower_freq: int, upper_freq: int, count: int) -> list[FrequencyBucket]:
    a = math.log(lower_freq / upper_freq) / count

    buckets: list[FrequencyBucket] = []
    prev_upper_val = upper_freq
    for i in range(1, count + 1):
        freq_val = upper_freq * math.exp(a * i)
        freq_val = round(freq_val)
        freq_range = range(freq_val, prev_upper_val)
        buckets.append(FrequencyBucket(freq_range))
        prev_upper_val = freq_val

    return list(reversed(buckets))

def plot_averages(freq_buckets: list[FrequencyBucket]):
    import matplotlib.pyplot as plt

    labels = [f"{bucket.freq_range.start}-{bucket.freq_range.stop} Hz" for bucket in freq_buckets]
    averages = [bucket.average() for bucket in freq_buckets]
    
    print(averages)
    
    # Plotting
    plt.figure(figsize=(12, 6))
    plt.bar(labels, averages, color='skyblue', edgecolor='black')
    
    # Adding labels and title
    plt.title('Average Amplitudes Across Frequency Buckets', fontsize=14)
    plt.xlabel('Frequency Range (Hz)', fontsize=12)
    plt.ylabel('Average Amplitude', fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Display the plot
    plt.tight_layout()
    plt.show()
    
def plot_standard_deviations(freq_buckets: list[FrequencyBucket]):
    import matplotlib.pyplot as plt

    labels = [f"{bucket.freq_range.start}-{bucket.freq_range.stop} Hz" for bucket in freq_buckets]
    standard_deviations = [bucket.standard_deviation() for bucket in freq_buckets]
    
    # Plotting
    plt.figure(figsize=(12, 6))
    plt.bar(labels, standard_deviations, color='skyblue', edgecolor='black')
    
    # Adding labels and title
    plt.title('Standard deviation Across Frequency Buckets', fontsize=14)
    plt.xlabel('Frequency Range (Hz)', fontsize=12)
    plt.ylabel('Standard deviation', fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Display the plot
    plt.tight_layout()
    plt.show()

def plot_loud_counts(freq_buckets: list[FrequencyBucket], loud_threshold: int):
    import matplotlib.pyplot as plt

    labels = [f"{bucket.freq_range.start}-{bucket.freq_range.stop} Hz" for bucket in freq_buckets]
    loud_counts = [bucket.loud_counts(loud_threshold) for bucket in freq_buckets]
    
    # Plotting
    plt.figure(figsize=(12, 6))
    plt.bar(labels, loud_counts, color='skyblue', edgecolor='black')
    
    # Adding labels and title
    plt.title('Count of loud segments', fontsize=14)
    plt.xlabel('Frequency Range (Hz)', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Display the plot
    plt.tight_layout()
    plt.show()
    
def plot_bucket(bucket: FrequencyBucket, sample_rate: int, segment_length_sec: int):
    import matplotlib.pyplot as plt
    import numpy as np

    w = np.linspace(0, len(bucket.amplitudes) / sample_rate, len(bucket.amplitudes))
    
    plt.figure(1)
    
    plt.plot(w, bucket.amplitudes)
    plt.xlabel('time')
    plt.ylabel('amplitude')
    plt.show()