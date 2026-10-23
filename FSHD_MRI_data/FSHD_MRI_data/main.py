# This doc contains: code to state class, interpolate the data, create graphs for the fat fraction and DUX4 expression 
# Comparing if metrics like clinical severity score are equal or better to fat fraction. 
# Two questions: does clincal severity score reflect what is happening in the muscles, or does it simply report perceieved functionality? 
# And, does fat fraction provide a more objective measure of muscle health compared to clinical severity score, and therefore more useful for clinical trial?


import numpy as np
import pandas as pd
import csv
from patientclass import Patient   

# summon patients from the CSV file 
patients = []
patients = Patient.instantiate_from_csv("Module2_FSHD_Dataset.csv")

print(patients[0].year1_visit())

# Find out the max and min values of the set to use for interpolation 
year1_values = [patient.year1_visit()["lag_months"] for patient in patients]
year2_values = [patient.year2_visit()["lag_months"] for patient in patients]

print("max_year1 =", max(year1_values))
print("max_year2 =", max(year2_values))


