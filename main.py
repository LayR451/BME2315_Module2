# This doc contains: code to state class, interpolate the data, create graphs for the fat fraction and DUX4 expression 
# Comparing if metrics like clinical severity score are equal or better to fat fraction. 
# Two questions: does clincal severity score reflect what is happening in the muscles, or does it simply report perceieved functionality? 
# And, does fat fraction provide a more objective measure of muscle health compared to clinical severity score, and therefore more useful for clinical trial?


import numpy as np
import pandas as pd
import csv
from patientclass import Patient   
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

df = pd.read_csv("Module2_FSHD_Dataset.csv")
print(df.shape)
df.head()

# Check for missing visits -- not every subject has a Year 1 and/or Year 2 visit
print("Subjects:", len(df))
print("Have a Year 1 visit:", df['lag_months_y1'].notna().sum())
print("Have a Year 2 visit:", df['lag_months_y2'].notna().sum())

T1 = df['lag_months_y1'].min()   # earliest Year-1 visit across all subjects
T2 = df['lag_months_y2'].min()   # earliest Year-2 visit across all subjects
print(f"T1 = {T1:.2f} months")
print(f"T2 = {T2:.2f} months")




results = []

for idx, row in df.iterrows():
    subject_id = row['subject_id']

    # TODO: pull this subject's lag_months and ff_R values into arrays,
    #       the same way we did for Subject 13-0004 above.
    row = df.loc[df['subject_id'] == subject_id].iloc[0]

    lag_months = np.array([row['lag_months_baseline'], row['lag_months_y1'], row['lag_months_y2']])
    ff_values = np.array([row['ff_baseline_R'], row['ff_y1_R'], row['ff_y2_R']])

    print("lag_months:", lag_months)
    print("ff_values: ", ff_values)


    # TODO: if this subject has at least baseline + Year 1 (no NaNs), compute
    #       their linear estimate at T1 (hint: interp1d with kind='linear').
    #       If they don't have enough data, use NaN instead.

    if not np.isnan(lag_months[:2]).any() and not np.isnan(ff_values[:2]).any():
        estimate_T1_linear = float(interp1d(lag_months[:2], ff_values[:2], kind='linear')(T1))
    else:
        estimate_T1_linear = np.nan

    # TODO: if this subject has all three visits (no NaNs), compute their
    #       quadratic estimate at T2 (hint: interp1d with kind='quadratic').
    #       If they don't, use NaN instead.

    if not np.isnan(lag_months).any() and not np.isnan(ff_values).any():
        estimate_T2_quadratic = float(interp1d(lag_months, ff_values, kind='quadratic')(T2))
    else:
        estimate_T2_quadratic = np.nan
    
    results.append({'subject_id': subject_id, 'estimate_T1_linear': estimate_T1_linear, 'estimate_T2_quadratic': estimate_T2_quadratic})

    pass

# TODO: turn `results` into a DataFrame and inspect it
results_df = pd.DataFrame(results)
results_df.head()

plt.plot(
    results_df['estimate_T1_linear'],
    results_df['estimate_T2_quadratic'],
    'o'
)
plt.title("Fat Fraction at T1 vs T2")
plt.xlabel("Estimated fat fraction at T1 (%)")
plt.ylabel("Estimated fat fraction at T2 (%)")
plt.grid(True, alpha=0.3)
plt.show()



# Do i want this?????



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Common comparison times, already calculated in your earlier code
T1 = df['lag_months_y1'].min()
T2 = df['lag_months_y2'].min()

# Store interpolated fat fractions for each patient
estimates = []

for _, row in df.iterrows():
    times = np.array([
        row['lag_months_baseline'],
        row['lag_months_y1'],
        row['lag_months_y2']
    ], dtype=float)

    ff = np.array([
        row['ff_baseline_R'],
        row['ff_y1_R'],
        row['ff_y2_R']
    ], dtype=float)

    # Keep only visits with both a time and a fat fraction measurement
    valid = np.isfinite(times) & np.isfinite(ff)
    times = times[valid]
    ff = ff[valid]

    # Sort visits by time
    order = np.argsort(times)
    times = times[order]
    ff = ff[order]

    # Average estimates at baseline, T1, and T2
    estimate_baseline = (
        ff[0] if len(times) > 0 and times[0] == 0 else np.nan
    )

    estimate_T1 = np.nan
    estimate_T2 = np.nan

    # Interpolate only when the target falls within observed times
    if len(times) >= 2 and times[0] <= T1 <= times[-1]:
        estimate_T1 = float(
            interp1d(times, ff, kind='linear')(T1)
        )

    if len(times) >= 2 and times[0] <= T2 <= times[-1]:
        estimate_T2 = float(
            interp1d(times, ff, kind='linear')(T2)
        )

    estimates.append({
        'subject_id': row['subject_id'],
        'baseline': estimate_baseline,
        'T1': estimate_T1,
        'T2': estimate_T2
    })

# Turn estimates into a DataFrame
estimates_df = pd.DataFrame(estimates)

# Calculate the average across patients at each time point
mean_ff = estimates_df[['baseline', 'T1', 'T2']].mean()
counts = estimates_df[['baseline', 'T1', 'T2']].count()

# Plot average interpolated fat fraction
labels = [
    'Baseline (0 months)',
    f'T1 ({T1:.1f} months)',
    f'T2 ({T2:.1f} months)'
]

plt.figure(figsize=(8, 5))
plt.plot(labels, mean_ff.values, marker='o', linewidth=2)

for i, (mean, n) in enumerate(zip(mean_ff.values, counts.values)):
    plt.annotate(
        f'{mean:.2f}% (n={n})',
        (i, mean),
        xytext=(0, 10),
        textcoords='offset points',
        ha='center'
    )

plt.title('Average Interpolated Right-Side Fat Fraction')
plt.xlabel('Time Point')
plt.ylabel('Mean Fat Fraction (%)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
