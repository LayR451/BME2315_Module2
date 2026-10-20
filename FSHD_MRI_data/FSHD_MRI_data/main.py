# This doc contains: code to state class, interpolate the data, create graphs for the fat fraction and DUX4 expression 
# Use dorsiflexion_qmt_R_baseline,dorsiflexion_qmt_R_y1,dorsiflexion_qmt_R_y2,dorsiflexion_qmt_L_baseline,dorsiflexion_qmt_L_y1,dorsiflexion_qmt_L_y2

# Compare a clincal marker like dorsiflexion_qmt_R_baseline against fat fraction  
import numpy as np
import pandas as pd
import csv
from patientclass import Patient   


patients = []

with open('Module2_FSHD_Dataset.csv', 'r', newline='') as file:
    reader = csv.reader(file)

    for row in reader:
        patient = Patient(*row)
        patients.append(patient)

print(patients)



# T1 = ['lag_months_y1'].min() 
# T2 = ['lag_months_y2'].min() 

x1, x2 = 1, 3
y1, y2 = 1, 3
Z = np.array([[1, x1], [1, x2]])
Y = np.array([y1, y2])
A = np.linalg.solve(Z, Y)
print(A)

