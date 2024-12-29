from itertools import groupby

from IPython.core.display import Markdown
from IPython.core.display_functions import display
from matplotlib import pyplot as plt

from test_suite.helper import bits_to_bytes
from test_suite.test_runner import TestResult, TestCaseResult


def visualize_test_result(test_result: TestResult):
    display(Markdown(f"# {test_result.test_name}"))

    grouped_by_channel = {
        key: list(group) for key, group in groupby(test_result.case_results, lambda x: x.channel_name)
    }

    for channel_key in grouped_by_channel:
        channel_results: list[TestCaseResult] = grouped_by_channel[channel_key]
        display(Markdown(f"## {channel_key}"))
        visualize_channel_test_case_results(channel_results)


def visualize_channel_test_case_results(case_results: list[TestCaseResult]):
    visualize_decoded_values(case_results)
    visualize_bits_per_second(case_results)
    visualize_bit_error_rate(case_results)
    visualize_avg_error_length(case_results)
    visualize_error_count(case_results)
    visualize_error_distribution_random(case_results)
    visualize_error_mask(case_results)


def visualize_decoded_values(case_results: list[TestCaseResult]):
    display(Markdown("## Decoded Values"))

    for result in case_results:
        print(f"{result.coder_name}: {', '.join([str(bits_to_bytes(rep.received_bits)) for rep in result.repetitions])}")


def visualize_bits_per_second(case_results: list[TestCaseResult]):
    display(Markdown("## Bits per Second"))
    coder_names = [result.coder_name for result in case_results]
    bits_per_second = [result.bits_per_second for result in case_results]

    # Create bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(coder_names, bits_per_second, color='skyblue')

    # Add labels and title
    plt.xlabel("Coder Name")
    plt.ylabel("Bits per Second")
    plt.title("Bits per Second per Coder")
    plt.ylim(0, max(bits_per_second) * 1.2)  # Add some space above the tallest bar

    # Display values above bars
    for i, bits in enumerate(bits_per_second):
        plt.text(i, bits + 0.1, f"{bits:.2f}", ha='center', va='bottom')

    # Show the plot
    plt.tight_layout()
    plt.show()


def visualize_bit_error_rate(case_results: list[TestCaseResult]):
    display(Markdown("## Bit Error Rate"))
    coder_names = [result.coder_name for result in case_results]
    bit_error_rates = [result.bit_error_rate for result in case_results]

    # Create bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(coder_names, bit_error_rates, color='skyblue')

    # Add labels and title
    plt.xlabel("Coder Name")
    plt.ylabel("Bit Error Rate")
    plt.title("Bit Error Rate per Coder")
    plt.ylim(0, max(max(bit_error_rates) * 1.2, 0.1))  # Add some space above the tallest bar

    # Display values above bars
    for i, rate in enumerate(bit_error_rates):
        plt.text(i, rate + 0.001, f"{rate:.2%}", ha='center', va='bottom')

    # Show the plot
    plt.tight_layout()
    plt.show()


def visualize_avg_error_length(case_results: list[TestCaseResult]):
    display(Markdown("## Average Error Length"))
    coder_names = [result.coder_name for result in case_results]
    avg_error_lengths = [result.avg_error_length for result in case_results]

    # Create bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(coder_names, avg_error_lengths, color='skyblue')

    # Add labels and title
    plt.xlabel("Coder Name")
    plt.ylabel("Average Error Length")
    plt.title("Average Error Length per Coder")
    plt.ylim(0, max(max(avg_error_lengths) * 1.2, 0.1))  # Add some space above the tallest bar

    # Display values above bars
    for i, length in enumerate(avg_error_lengths):
        plt.text(i, length + 0.1, f"{length:.2f}", ha='center', va='bottom')

    # Show the plot
    plt.tight_layout()
    plt.show()


def visualize_error_count(case_results: list[TestCaseResult]):
    display(Markdown("## Error Count"))
    coder_names = [result.coder_name for result in case_results]
    error_counts = [result.error_count for result in case_results]

    # Create bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(coder_names, error_counts, color='skyblue')

    # Add labels and title
    plt.xlabel("Coder Name")
    plt.ylabel("Error Count")
    plt.title("Error Count per Coder")
    plt.ylim(0, max(max(error_counts) * 1.2, 0.1))  # Add some space above the tallest bar

    # Display values above bars
    for i, count in enumerate(error_counts):
        plt.text(i, count + 0.1, f"{count}", ha='center', va='bottom')

    # Show the plot
    plt.tight_layout()
    plt.show()


def visualize_error_distribution_random(case_results: list[TestCaseResult]):
    display(Markdown("## Is Error Distribution random"))
    for result in case_results:
        print(f"{result.coder_name}: {result.error_distribution_random}")
        
def visualize_error_mask(case_results: list[TestCaseResult]):
    display(Markdown("## Errors over time"))
    plt.figure(figsize=(10, 6))

    for result in case_results:
        # Generate time axis based on bits_per_second
        time = [i / result.bits_per_second for i in range(len(result.repetitions[0].error_mask))]
        
        # Plot the error mask
        plt.plot(time, result.error_mask(), label=f"{result.channel_name} ({result.coder_name})")

    # Add labels and legend
    plt.xlabel("Time (s)")
    plt.ylabel("Error Mask")
    plt.title("Error Masks Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()