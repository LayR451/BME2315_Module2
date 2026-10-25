
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

    if not np.isnan(lag_months[:2]).any() and not np.isnan(ff_values[:2]).any() and lag_months[0] != lag_months[1]:
        estimate_T1_linear = float(interp1d(lag_months[:2], ff_values[:2], kind='linear')(T1))
    else:
        estimate_T1_linear = np.nan

    # TODO: if this subject has all three visits (no NaNs), compute their
    #       quadratic estimate at T2 (hint: interp1d with kind='quadratic').
    #       If they don't, use NaN instead.

    if not np.isnan(lag_months).any() and not np.isnan(ff_values).any() and len(set(lag_months)) == 3:
        estimate_T2_quadratic = float(interp1d(lag_months, ff_values, kind='quadratic')(T2))
    else:
        estimate_T2_quadratic = np.nan
    
    results.append({'subject_id': subject_id, 'estimate_T1_linear': estimate_T1_linear, 'estimate_T2_quadratic': estimate_T2_quadratic})

    pass

results_df = pd.DataFrame(results)
results_df.head()


# A KINDA USELESS GRAPH!?
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
#####



# Store interpolated clinical severity scores for each patient
estimates = []

# now the loop for the clinical score! 
for idx, row in df.iterrows():
    subject_id = row['subject_id']

    # TODO: pull this subject's lag_months and clinical severity score values into arrays,
    #       the same way we did for Subject 13-0004 above.
    row = df.loc[df['subject_id'] == subject_id].iloc[0]

    lag_months = np.array([row['lag_months_baseline'], row['lag_months_y1'], row['lag_months_y2']])
    clinical_severity_score_values = np.array([row['clinical_severity_score_baseline'], row['clinical_severity_score_y1'], row['clinical_severity_score_y2']])

    print("lag_months:", lag_months)
    print("clinical_severity_score_values: ", clinical_severity_score_values)


    # TODO: if this subject has at least baseline + Year 1 (no NaNs), compute
    #       their linear estimate at T1 (hint: interp1d with kind='linear').
    #       If they don't have enough data, use NaN instead.

    if not np.isnan(lag_months[:2]).any() and not np.isnan(clinical_severity_score_values[:2]).any() and lag_months[0] != lag_months[1]:
        estimate_T1_linear = float(interp1d(lag_months[:2], clinical_severity_score_values[:2], kind='linear')(T1))
    else:
        estimate_T1_linear = np.nan

    # TODO: if this subject has all three visits (no NaNs), compute their
    #       quadratic estimate at T2 (hint: interp1d with kind='quadratic').
    #       If they don't, use NaN instead.

    if not np.isnan(lag_months).any() and not np.isnan(clinical_severity_score_values).any() and len(set(lag_months)) == 3:
        estimate_T2_quadratic = float(interp1d(lag_months, clinical_severity_score_values, kind='quadratic')(T2))
    else:
        estimate_T2_quadratic = np.nan
    
    estimates.append({'subject_id': subject_id, 'estimate_T1_linear': estimate_T1_linear, 'estimate_T2_quadratic': estimate_T2_quadratic})

    pass
    
    estimates.append({
        'subject_id': row['subject_id'],
        'baseline': clinical_severity_score_values[0],
        'T1': estimate_T1_linear,
        'T2': estimate_T2_quadratic
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

plt.title('Average Interpolated Clinical Severity Score')
plt.xlabel('Time Point')
plt.ylabel('Mean Clinical Severity Score')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


# MORE GRAPHHHHHHSSSSSSSSSS

# ================= EXTRA GRAPHS =================

# --- combine fat fraction + clinical severity into one table (matched on subject_id) ---
ff = pd.DataFrame({
    'subject_id': results_df['subject_id'],
    'ff0': df['ff_baseline_R'].values,
    'ff1': results_df['estimate_T1_linear'],
    'ff2': results_df['estimate_T2_quadratic'],
})
css = (estimates_df[['subject_id', 'baseline', 'T1', 'T2']]
       .dropna(subset=['baseline'])          # keeps only the rows from your 2nd append
       .drop_duplicates('subject_id')
       .rename(columns={'baseline': 'css0', 'T1': 'css1', 'T2': 'css2'}))
comb = ff.merge(css, on='subject_id')
comb['ff_change'] = comb['ff2'] - comb['ff0']       # baseline -> T2
comb['css_change'] = comb['css2'] - comb['css0']

x_months = [0, T1, T2]
tlabels = ['Baseline', f'T1\n({T1:.1f} mo)', f'T2\n({T2:.1f} mo)']

# --- GRAPH A: fat fraction change vs clinical severity change ---
d = comb.dropna(subset=['ff_change', 'css_change'])
rho, p = spearmanr(d['ff_change'], d['css_change'])
plt.figure(figsize=(6.5, 5))
plt.scatter(d['ff_change'], d['css_change'], color="#1f7a8c", s=60)
if len(d) > 2:
    m, b = np.polyfit(d['ff_change'], d['css_change'], 1)
    xs = np.linspace(d['ff_change'].min(), d['ff_change'].max(), 50)
    plt.plot(xs, m * xs + b, color="#e8821e", lw=2, ls="--")
plt.axhline(0, color="gray", lw=0.8)
plt.axvline(0, color="gray", lw=0.8)
plt.xlabel("Change in fat fraction, baseline to T2 (points)")
plt.ylabel("Change in clinical severity score, baseline to T2")
plt.title(f"Fat fraction change vs severity change\nSpearman rho = {rho:.2f}, p = {p:.3f}, n = {len(d)}")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# --- GRAPH B: both measures together against the interpolated times (two y-axes) ---
d = comb.dropna(subset=['ff0', 'ff1', 'ff2', 'css0', 'css1', 'css2'])
n = len(d)
ff_mean = d[['ff0', 'ff1', 'ff2']].mean().values
ff_sem = d[['ff0', 'ff1', 'ff2']].sem().values
css_mean = d[['css0', 'css1', 'css2']].mean().values
css_sem = d[['css0', 'css1', 'css2']].sem().values

fig, ax1 = plt.subplots(figsize=(7.5, 5))
ax1.errorbar(x_months, ff_mean, yerr=ff_sem, color="#e8821e", marker='o', lw=2.5, capsize=4)
ax1.set_ylabel("Mean fat fraction (%)", color="#e8821e")
ax2 = ax1.twinx()
ax2.errorbar(x_months, css_mean, yerr=css_sem, color="#1f7a8c", marker='s', lw=2.5, capsize=4)
ax2.set_ylabel("Mean clinical severity score", color="#1f7a8c")
ax1.set_xticks(x_months)
ax1.set_xticklabels(tlabels)
ax1.set_xlabel("Interpolated time point")
ax1.set_title(f"Fat fraction and clinical severity over time (mean ± SEM, n = {n})")
ax1.grid(alpha=0.3)
fig.tight_layout()
plt.show()

# --- GRAPH C: every patient's trajectory (lines) + bars for the average ---
def patient_lines_and_bars(ax, data, cols, title, ylabel, bar_color):
    dd = data.dropna(subset=cols)
    vals = dd[cols].to_numpy()
    pos = [0, 1, 2]
    means = vals.mean(axis=0)
    sems = dd[cols].sem().values
    ax.bar(pos, means, yerr=sems, color=bar_color, alpha=0.35, capsize=5, width=0.6, label="Average ± SEM")
    ax.plot(pos, vals.T, color="gray", alpha=0.5, marker='o', ms=3, lw=1)
    ax.set_xticks(pos)
    ax.set_xticklabels(tlabels)
    ax.set_title(f"{title} (n = {len(dd)})")
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3, axis='y')
    ax.legend()

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12, 5))
patient_lines_and_bars(axL, comb, ['ff0', 'ff1', 'ff2'], "Fat fraction per patient", "Fat fraction (%)", "#e8821e")
patient_lines_and_bars(axR, comb, ['css0', 'css1', 'css2'], "Clinical severity per patient", "Clinical severity score", "#1f7a8c")
fig.tight_layout()
plt.show()