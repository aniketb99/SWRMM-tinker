import pandas as pd 
import os
import subprocess


def modify_input_file(template_file, output_file, params, subcatchment_count=8):
    # Read the template file
    with open(template_file, 'r') as file:
        data = file.readlines()

    # Flags to identify which section we are in
    in_subcatchments = False
    in_infiltration = False
    in_subareas = False
    in_timeseries = False

    # Modify the parameters in the input file
    for i in range(subcatchment_count):
        subcatchment_name = f"{i+1}"
        area = params['Area (acres)'][i]
        imperv = params['% Impervious'][i]
        slope = params['Slope (%)'][i]
        max_infil = params['Max Infiltration Rate (in/hr)'][i]
        min_infil = params['Min Infiltration Rate (in/hr)'][i]
        n_imperv = params['Manning\'s n (Impervious)'][i]
        n_perv = params['Manning\'s n (Pervious)'][i]
        s_imperv = params['Depressional Storage (Impervious, in)'][i]
        s_perv = params['Depressional Storage (Pervious, in)'][i]

        for idx, line in enumerate(data):
            # Check if we are in the [SUBCATCHMENTS] section
            if line.startswith("[SUBCATCHMENTS]"):
                in_subcatchments = True
                in_infiltration = in_subareas = in_timeseries = False

            # Check if we are in the [INFILTRATION] section
            elif line.startswith("[INFILTRATION]"):
                in_infiltration = True
                in_subcatchments = in_subareas = in_timeseries = False

            # Check if we are in the [SUBAREAS] section
            elif line.startswith("[SUBAREAS]"):
                in_subareas = True
                in_subcatchments = in_infiltration = in_timeseries = False

            # Check if we are in the [TIMESERIES] section
            elif line.startswith("[TIMESERIES]"):
                in_timeseries = True
                in_subcatchments = in_infiltration = in_subareas = False

            # Modify the [SUBCATCHMENTS] section
            if in_subcatchments and line.startswith(subcatchment_name):
                parts = line.split()
                parts[3] = f"{area}"
                parts[4] = f"{imperv}"
                parts[6] = f"{slope}"
                data[idx] = ' '.join(parts) + "\n"

            # Modify the [INFILTRATION] section
            if in_infiltration and line.startswith(subcatchment_name):
                parts = line.split()
                parts[1] = f"{max_infil}"
                parts[2] = f"{min_infil}"
                data[idx] = ' '.join(parts) + "\n"

            # Modify the [SUBAREAS] section
            if in_subareas and line.startswith(subcatchment_name):
                parts = line.split()
                parts[1] = f"{n_imperv}"
                parts[2] = f"{n_perv}"
                parts[3] = f"{s_imperv}"
                parts[4] = f"{s_perv}"
                data[idx] = ' '.join(parts) + "\n"

        # Modify the [TIMESERIES] section for rainfall
        if in_timeseries:
            for idx, line in enumerate(data):
                if line.startswith('TS1'):
                    for time_idx, value in enumerate(params['Rainfall Time Series']):
                        data[idx + time_idx + 1] = f"TS1   {time_idx}:00   {value}\n"
                    break
    
    # Write the modified input file
    with open(output_file, 'w') as file:
        file.writelines(data)


if __name__ == "__main__":

    input_file = "test.inp"
    modified_input_file = "modified_test.inp"
    modify_input_file(input_file,modified_input_file,)