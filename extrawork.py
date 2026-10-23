import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.stats import wilcoxon

df = pd.read_csv("Module2_FSHD_Dataset.csv")
print(df.shape)

def analyze(base_col, y1_col, y2_col, label):
    rows = []
    for _, row in df.iterrows():
        lag = np.array([row['lag_months_baseline'], row['lag_months_y1'], row['lag_months_y2']], dtype=float)
        y = np.array([row[base_col], row[y1_col], row[y2_col]], dtype=float)

        est_T1 = np.nan
        if not np.isnan(lag[:2]).any() and not np.isnan(y[:2]).any():
            est_T1 = float(interp1d(lag[:2], y[:2], kind='linear')(T1))

        est_T2 = np.nan
        if not np.isnan(lag).any() and not np.isnan(y).any():
            est_T2 = float(interp1d(lag, y, kind='quadratic')(T2))

        rows.append({'subject_id': row['subject_id'], 'baseline': y[0],
                     'T1_linear': est_T1, 'T2_quadratic': est_T2})

    res = pd.DataFrame(rows)

    # plot: one line per subject plus the mean
    cols = ['baseline', 'T1_linear', 'T2_quadratic']
    d = res.dropna(subset=cols)
    x = [0, T1, T2]
    plt.figure(figsize=(7, 5))
    plt.plot(x, d[cols].to_numpy().T, color="gray", alpha=0.4, marker="o", ms=3)
    plt.plot(x, d[cols].mean(), color="#e8821e", lw=3.5, marker="s", ms=9, label=f"Mean (n={len(d)})")
    plt.xticks(x, ["Baseline", f"T1 ({T1:.1f} mo)", f"T2 ({T2:.1f} mo)"])
    plt.ylabel(label)
    plt.title(f"{label} over the interpolated time frame")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show()

    # paired test of each time point against baseline
    for name, col in [("T1", "T1_linear"), ("T2", "T2_quadratic")]:
        pair = res.dropna(subset=['baseline', col])
        change = pair[col] - pair['baseline']
        try:
            p = wilcoxon(change).pvalue
        except ValueError:          # happens if every change is exactly 0
            p = np.nan
        print(f"{label}, baseline -> {name}: median change = {change.median():+.2f}, "
              f"n = {len(pair)}, Wilcoxon p = {p:.4f}")
    return res

ff_res  = analyze('ff_baseline_R', 'ff_y1_R', 'ff_y2_R', 'Right TA fat fraction (%)')
css_res = analyze('clinical_severity_score_baseline', 'clinical_severity_score_y1',
                  'clinical_severity_score_y2', 'Clinical severity score')