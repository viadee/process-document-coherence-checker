import os
from experiment_runner import run_experiment_for_directory
from single_process_checker import run_single_process_check


if __name__ == "__main__":
    num_runs = 5  # Hardcoded number of runs

    root_directory = r'C:\Users\B229\OneDrive - viadee Unternehmensberatung AG\Masterarbeit\Code\Data'

    subfolders_exist = any(
        os.path.isdir(os.path.join(root_directory, name)) and name != "modified"
        for name in os.listdir(root_directory)
    )
    
    if subfolders_exist:
            for folder in os.listdir(root_directory):
                folder_path = os.path.join(root_directory, folder)
                if os.path.isdir(folder_path):
                    print(f"Running experiments for folder: {folder_path}")
                    run_experiment_for_directory(folder_path, num_runs)
                    print("""\n--------------------------------------------------------------------------------------------------------------------------------\n""")
            print(f"\nAll experiments have been finished successfully!")
    else:
        print(f"Running single process check for directory: {root_directory}")
        run_single_process_check(root_directory)
        print("""\n--------------------------------------------------------------------------------------------------------------------------------\n""")
        print(f"\nThe Process Coherence Check has been finished successfully!")