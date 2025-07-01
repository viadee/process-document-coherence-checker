def compare_results_with_config(config, result):
    """Compare the result from GPT with the expected changes from the config file."""
    if config is None:
        print("Config is None, proceeding with empty changes.")
        temp_relevant_changes = []
        temp_unrelated_changes = []
        temp_negligible_changes = []
    else:
        temp_relevant_changes = config.get("relevant changes", [])
        temp_unrelated_changes = config.get("unrelated changes", [])
        temp_negligible_changes = config.get("negligible changes", [])
    
    if result is None:
        temp_identified_changes = []
    else:
        temp_identified_changes = [
            change for change in result.get("classification", [])
            if change.get("Change Category") == "Relevant"
        ]

    # Combine unrelated and negligible changes into a single list
    remaining_irrelevant_changes = temp_unrelated_changes + temp_negligible_changes

    correct_changes = 0
    temp_extra_changes_correct_dimension = 0

    # Create lists to track remaining changes
    remaining_relevant_changes = temp_relevant_changes[:]
    remaining_identified_changes = []

    # Primary matching: Identified changes with relevant changes by dimension
    for identified_change in temp_identified_changes:
        match_found = False
        for relevant_change in remaining_relevant_changes:
            if identified_change["dimension"] == relevant_change["dimension"]:
                correct_changes += 1
                remaining_relevant_changes.remove(relevant_change)
                match_found = True
                break
                
        if not match_found:
            remaining_identified_changes.append(identified_change)

    temp_identified_changes = remaining_identified_changes
    remaining_identified_changes = []

    # Secondary matching: Remaining identified changes with irrelevant changes by dimension
    for identified_change in temp_identified_changes:
        match_found = False
        for irrelevant_change in remaining_irrelevant_changes:
            if identified_change["dimension"] == irrelevant_change["dimension"]:
                temp_extra_changes_correct_dimension += 1
                remaining_irrelevant_changes.remove(irrelevant_change)
                match_found = True
                break

        if not match_found:
            remaining_identified_changes.append(identified_change)

    temp_identified_changes = remaining_identified_changes

    # Calculate final counts
    length_temp_relevant_changes = len(remaining_relevant_changes)
    length_temp_irrelevant_changes = len(remaining_irrelevant_changes)
    length_temp_identified_changes = len(temp_identified_changes)

    identified_but_wrong_dimension = min(length_temp_relevant_changes, temp_extra_changes_correct_dimension)
    length_temp_relevant_changes -= identified_but_wrong_dimension
    extra_changes_correct_dimension = temp_extra_changes_correct_dimension - identified_but_wrong_dimension
    extra_changes_wrong_dimension = min(length_temp_identified_changes, length_temp_irrelevant_changes)
    extra_changes_out_of_config = length_temp_identified_changes - extra_changes_wrong_dimension

    #temp_unmatched_relevant_changes = max((length_temp_relevant_changes - (correct_changes + identified_but_wrong_dimension)),0)
    print(f"temp_unmatched_relevant_changes: {length_temp_relevant_changes}")

    for i in range(length_temp_relevant_changes):
        print(f"length_temp_relevant_changes: {length_temp_relevant_changes - i}")
        if (extra_changes_out_of_config > 0):
            identified_but_wrong_dimension += 1
            extra_changes_out_of_config -= 1
        elif (extra_changes_wrong_dimension > 0):
            identified_but_wrong_dimension += 1
            extra_changes_wrong_dimension -= 1
        elif (extra_changes_correct_dimension > 0):
            identified_but_wrong_dimension += 1
            extra_changes_correct_dimension -= 1
        

    # Debugging information
    relevant_counts = {}
    for change in config.get("relevant changes", []):
        dim = change["dimension"]
        relevant_counts[dim] = relevant_counts.get(dim, 0) + 1

    unrelated_negligible_counts = {}
    for change in config.get("unrelated changes", []) + config.get("negligible changes", []):
        dim = change["dimension"]
        unrelated_negligible_counts[dim] = unrelated_negligible_counts.get(dim, 0) + 1
    
    identified_counts = {}
    if result is not None:
        for change in result.get("classification", []):
            if change.get("Change Category") == "Relevant":
                dim = change["dimension"]
                identified_counts[dim] = identified_counts.get(dim, 0) + 1
    
    # Calculate achievable points
    total_relevant_changes = len(config.get("relevant changes", []))
    total_unrelated_and_negligible_changes = len(config.get("unrelated changes", [])) + len(config.get("negligible changes", []))
    achievable_points = total_relevant_changes + (total_unrelated_and_negligible_changes * 0.5)

    # Calculate final accuracy points
    accuracy_points = (correct_changes 
                       +(identified_but_wrong_dimension * 0.5) 
                       -(extra_changes_correct_dimension * 0.25) 
                       -(extra_changes_wrong_dimension * 0.5) 
                       -(extra_changes_out_of_config * 1) 
                       +(total_unrelated_and_negligible_changes * 0.5))
    
    if achievable_points == 0:
        print("Achievable points are zero, indicating no changes were expected or relevant data is missing from the config.")
        if accuracy_points == 0:
            accuracy_percentage = 1
        else:
            accuracy_percentage = 0
    else:
        accuracy_percentage = max(accuracy_points / achievable_points, 0)  # Avoid division by zero

    # Set overall_incoherence_correctness_indicator
    has_original_relevant_changes = len(config.get("relevant changes", [])) > 0
    if result is not None:
        has_identified_relevant_changes = len([change for change in result.get("classification", []) if change.get("Change Category") == "Relevant"]) > 0
    else:
        has_identified_relevant_changes = False

    if has_original_relevant_changes == has_identified_relevant_changes:
        overall_incoherence_correctness_indicator = 0
    elif has_identified_relevant_changes and not has_original_relevant_changes:
        overall_incoherence_correctness_indicator = 1
    elif has_original_relevant_changes and not has_identified_relevant_changes:
        overall_incoherence_correctness_indicator = -1

    # Print detailed accuracy calculation for debugging
    print(f"Relevant counts: {relevant_counts}")
    print(f"Unrelated and negligible counts: {unrelated_negligible_counts}")
    print(f"Identified counts: {identified_counts}")
    print(f"Correct changes: {correct_changes}")
    print(f"Identified but wrong dimension: {identified_but_wrong_dimension}")
    print(f"Extra changes in correct dimension: {extra_changes_correct_dimension}")
    print(f"Extra changes in wrong dimension: {extra_changes_wrong_dimension}")
    print(f"Extra changes out of config: {extra_changes_out_of_config}")
    print(f"Total unrelated and negligible changes: {total_unrelated_and_negligible_changes}")
    print(f"Accuracy points: {accuracy_points}")
    print(f"Achievable points: {achievable_points}")
    print(f"Accuracy percentage: {accuracy_percentage * 100:.2f}%")
    print(f"Overall Incoherence Correctness Indicator: {overall_incoherence_correctness_indicator}")


    return accuracy_percentage, overall_incoherence_correctness_indicator