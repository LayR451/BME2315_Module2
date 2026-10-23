import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

# df = pd.read_csv("Module2_FSHD_Dataset.csv")
# T1 = df["lag_months_y1"].min()
# T2 = df["lag_months_y2"].min()
# t_cols = ["lag_months_baseline", "lag_months_y1", "lag_months_y2"]

# def interp_at(df, y_cols, T, kind="linear"):
#     def one(row):
#         t = row[t_cols].to_numpy(dtype=float)
#         y = row[y_cols].to_numpy(dtype=float)
#         ok = ~np.isnan(t) & ~np.isnan(y)
#         t, y = t[ok], y[ok]
#         if len(t) < (3 if kind == "quadratic" else 2):
#             return np.nan
#         return float(interp1d(t, y, kind=kind, bounds_error=False)(T))
#     return df.apply(one, axis=1)

# ff_cols    = ["ff_baseline_R", "ff_y1_R", "ff_y2_R"]
# score_cols = ["clinical_severity_score_baseline", "clinical_severity_score_y1", "clinical_severity_score_y2"]   # <-- your real clinical column names

# res = pd.DataFrame({"subject_id": df["subject_id"]})
# res["ff_T2"]      = interp_at(df, ff_cols, T2)
# res["score_T2"]   = interp_at(df, score_cols, T2)
# res["ff_change"]    = res["ff_T2"] - df["ff_baseline_R"]        # change over T2 months
# res["score_change"] = res["score_T2"] - df["clinical_severity_score_baseline"]


# def compare(x, y, xlabel, ylabel):
#     d = pd.concat([x, y], axis=1).dropna()
#     rho, p = spearmanr(d.iloc[:, 0], d.iloc[:, 1])
#     plt.scatter(d.iloc[:, 0], d.iloc[:, 1])
#     plt.xlabel(xlabel); plt.ylabel(ylabel)
#     plt.title(f"Spearman rho = {rho:.2f}, p = {p:.3f}, n = {len(d)}")
#     plt.show()

# compare(res["ff_T2"], res["score_T2"], "Fat fraction at T2 (%)", "Clinical score at T2")
# compare(res["ff_change"], res["score_change"], "Δ fat fraction", "Δ clinical score")



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

df = pd.read_csv("Module2_FSHD_Dataset.csv")
print(df.shape)

# Check for missing visits -- not every subject has a Year 1 and/or Year 2 visit
print("Subjects:", len(df))
print("Have a Year 1 visit:", df['lag_months_y1'].notna().sum())
print("Have a Year 2 visit:", df['lag_months_y2'].notna().sum())

T1 = df['lag_months_y1'].min()   # earliest Year-1 visit across all subjects
T2 = df['lag_months_y2'].min()   # earliest Year-2 visit across all subjects
print(f"T1 = {T1:.2f} months")
print(f"T2 = {T2:.2f} months")

# ---------- Example subject 13-0004 ----------
row = df.loc[df['subject_id'] == '13-0004'].iloc[0]

lag_months = np.array([row['lag_months_baseline'], row['lag_months_y1'], row['lag_months_y2']], dtype=float)
ff_values  = np.array([row['ff_baseline_R'], row['ff_y1_R'], row['ff_y2_R']], dtype=float)

print("lag_months:", lag_months)
print("ff_values: ", ff_values)

f_linear = interp1d(lag_months, ff_values, kind='linear')
f_quadratic = interp1d(lag_months, ff_values, kind='quadratic')

estimate_T1 = float(f_linear(T1))        # needed by the plot
estimate_T2 = float(f_quadratic(T2))     # needed by the plot
print("f_linear(T1)    =", estimate_T1)
print("f_quadratic(T2) =", estimate_T2)

# ---------- Plot ----------
TEAL = "#1f7a8c"
PINK = "#e0569b"
ORANGE = "#e8821e"

x_curve = np.linspace(lag_months[0], lag_months[-1], 200)
quad_curve = f_quadratic(x_curve)

plt.figure(figsize=(7.5, 5))
plt.plot(x_curve, quad_curve, color=ORANGE, lw=2.5, linestyle="--", label="Quadratic (all 3 points)")
plt.plot(lag_months[:2], ff_values[:2], color=PINK, lw=2.5, linestyle="--", label="Linear (baseline -> Year 1)")
plt.scatter(lag_months, ff_values, color=TEAL, s=90, zorder=4, label="Measured visits (known)")
plt.scatter([T1], [estimate_T1], color=PINK, marker="D", s=120, zorder=5, label=f"Linear estimate @ T1={T1:.1f}")
plt.scatter([T2], [estimate_T2], color=ORANGE, marker="D", s=120, zorder=5, label=f"Quadratic estimate @ T2={T2:.1f}")
plt.title("Subject 13-0004 — right tibialis anterior fat fraction")
plt.xlabel("Months since baseline (lag_months)")
plt.ylabel("Fat fraction (%)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()

# ---------- All subjects ----------
results = []

for idx, row in df.iterrows():
    lag = np.array([row['lag_months_baseline'], row['lag_months_y1'], row['lag_months_y2']], dtype=float)
    ff  = np.array([row['ff_baseline_R'], row['ff_y1_R'], row['ff_y2_R']], dtype=float)

    est_T1_linear = np.nan
    if not np.isnan(lag[:2]).any() and not np.isnan(ff[:2]).any():
        est_T1_linear = float(interp1d(lag[:2], ff[:2], kind='linear')(T1))

    est_T2_quadratic = np.nan
    if not np.isnan(lag).any() and not np.isnan(ff).any():
        est_T2_quadratic = float(interp1d(lag, ff, kind='quadratic')(T2))

    results.append({
        'subject_id': row['subject_id'],
        'lag_y1_real': lag[1],
        'lag_y2_real': lag[2],
        'ff_baseline': ff[0],
        'ff_y1_real': ff[1],
        'ff_y2_real': ff[2],
        'estimate_T1_linear': est_T1_linear,
        'estimate_T2_quadratic': est_T2_quadratic,
    })

results_df = pd.DataFrame(results)

print(results_df.to_string())          # all 34 rows, not just 5
print("\nRows:", len(results_df))
print(results_df[['estimate_T1_linear', 'estimate_T2_quadratic']].notna().sum())

results_df.to_csv('interpolated_estimates.csv', index=False)

import matplotlib.pyplot as plt
from scipy.stats import wilcoxon

cols = ['ff_baseline', 'estimate_T1_linear', 'estimate_T2_quadratic']
d = results_df.dropna(subset=cols)          # subjects with all three values
x = [0, T1, T2]

plt.figure(figsize=(7, 5))
plt.plot(x, d[cols].to_numpy().T, color="gray", alpha=0.4, marker="o", ms=3)   # one line per subject
plt.plot(x, d[cols].mean(), color="#e8821e", lw=3.5, marker="s", ms=9, label=f"Mean (n={len(d)})")
plt.xticks(x, ["Baseline", f"T1 ({T1:.1f} mo)", f"T2 ({T2:.1f} mo)"])
plt.ylabel("Right tibialis anterior fat fraction (%)")
plt.title("Fat fraction over the interpolated time frame")
plt.grid(alpha=0.3)
plt.legend()
plt.show()

# Did it change? Paired test of each time point against baseline
for name, col in [("T1", 'estimate_T1_linear'), ("T2", 'estimate_T2_quadratic')]:
    pair = results_df.dropna(subset=['ff_baseline', col])
    change = pair[col] - pair['ff_baseline']
    stat, p = wilcoxon(change)
    print(f"Baseline -> {name}: median change = {change.median():+.2f} points, "
          f"n = {len(pair)}, Wilcoxon p = {p:.4f}")