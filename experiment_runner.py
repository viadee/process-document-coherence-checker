import os
import json
import time
import csv
import statistics
from result_comparison import compare_results_with_config
from coherence_checker import run_coherence_check

def load_config(file_path):
    """Load JSON config file from a given path."""
    with open(file_path, 'r') as file:
        return json.load(file)

def run_experiment_for_directory(directory, num_runs):
    """Run the coherence checking experiment for the given directory."""
    config_path = os.path.join(directory, 'solution_config.json')

    if not os.path.exists(config_path):
        print(f"No config file found in {directory}")
        return

    config = load_config(config_path)
    experiment_results = []

    for i in range(num_runs):
        print(f"\nExperiment #{i+1} started")
        
        start_time = time.time()
        result = run_coherence_check(directory)
        end_time = time.time()
        
        duration = end_time - start_time

        if result['txt_coherence_result']:
            try:
                result_json = json.loads(result['txt_coherence_result'])
                accuracy, overall_incoherence_indicator = compare_results_with_config(config, result_json)
            except json.JSONDecodeError:
                accuracy, overall_incoherence_indicator = compare_results_with_config(config, None)
        else:
            accuracy, overall_incoherence_indicator = compare_results_with_config(config, None)
            result['txt_coherence_result'] = ""
        
        if not result['bpmn_comparison_result_json']:
            result['bpmn_comparison_result_json'] = ""

        experiment_results.append({
            'iteration': i + 1,
            'duration': round(duration, 2),
            'accuracy': round(accuracy, 2),
            'overall_incoherence_indicator': overall_incoherence_indicator,
            'tokens_used': result['total_tokens'],
            'total_api_cost': float(result['total_api_cost']),
            'json_result': (result['bpmn_comparison_result_json'] + "\n\n" + result['txt_coherence_result']),
        })

    log_results(directory, experiment_results)

def log_results(directory, results):
    """Log the results of the experiments."""
    log_dir = os.path.join(directory, 'ExperimentLog')
    os.makedirs(log_dir, exist_ok=True)
    llm_output_dir = os.path.join(log_dir, 'LLM Output')
    os.makedirs(llm_output_dir, exist_ok=True)
    csv_file = os.path.join(log_dir, 'experiment_log.csv')

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Iteration', 'Duration', 'Accuracy', 'Overall Incoherence Indicator', 'Tokens Used', 'Total API Costs (€)'])

        for result in results:
            writer.writerow([result['iteration'], result['duration'], result['accuracy'], result['overall_incoherence_indicator'], result['tokens_used'], f"{result['total_api_cost']:.6f}"])

    # Now save each JSON result associated with the experiment iteration:
    for result in results:
        iteration = result['iteration']
        json_output_path = os.path.join(llm_output_dir, f'llm_output_iteration_{iteration}.json')
        if 'json_result' in result and result['json_result']:
            with open(json_output_path, 'w') as outFile:
                outFile.write(result['json_result'])

    # Calculate consistency (spread of accuracy)
    accuracies = [result['accuracy'] for result in results]
    incoherence_indicators = [result['overall_incoherence_indicator'] for result in results]

    # Calculate the percentage of overall_incoherence_correctness_indicator being zero
    overall_incoherence_correct_indicator_zeros = incoherence_indicators.count(0)
    overall_incoherence_correctness_percentage = (overall_incoherence_correct_indicator_zeros / len(incoherence_indicators)) * 100 if incoherence_indicators else 0

    summary_file = os.path.join(log_dir, 'experiment_summary.txt')
    with open(summary_file, 'w') as file:
        file.write(f'Average Accuracy: {statistics.mean(accuracies)}\n')
        file.write(f'Overall Incoherence Correctness Percentage: {overall_incoherence_correctness_percentage:.2f}%\n')
        file.write(f'Standard Deviation of Accuracy: {statistics.stdev(accuracies) if len(accuracies) > 1 else 1}\n')
        file.write(f'Total Tokens Used (avg per run): {statistics.mean([result["tokens_used"] for result in results])}\n')
        file.write(f'Total API Costs ($) (avg per run): {statistics.mean([result["total_api_cost"] for result in results])}\n')
