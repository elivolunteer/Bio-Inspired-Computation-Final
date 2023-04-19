import pandas as pd
import subprocess

varrying_map = {
    'num_particles': [x for x in range(10, 100, 10)],
    'inertia': [x/10 for x in range(1, 11)],
    'cognition': [x/10 for x in range(1, 41)],
    'social': [x/10 for x in range(1, 41)],
    'tau': [x for x in range(1, 11, 1)],
}


# Define dataframe columns
columns = ['i','num_particles', 'inertia', 'cognition', 'social', 'tau', 'epoch_stop', 'solution_found', 'fitness', 'found']

# loop over the map 
df_list = []
for tau_value in varrying_map['tau']:
    print("Running for", tau_value)
    for i in range(50):
        output = subprocess.check_output(['python', 'dpso.py', '--tau', str(tau_value)])
        output = output.decode('utf-8').splitlines()

        # Create a dictionary to store the output
        row = {}
        row['i'] = i
        for line in output:
            key, value = line.split(':')
            row[key] = value.strip()
        
        # If the fitness is not 0, then the solution was not found. 
        if float(row['fitness']) > 1e-10:
            row['found'] = False
        else:
            row['found'] = True

        df_list.append(row)
        print(row)

df = pd.DataFrame(df_list, columns=columns)
df.to_csv(f'200/R_tau_lower_phi_1.csv', index=False)