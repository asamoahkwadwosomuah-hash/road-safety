"""
02_build_dashboard.py
------------------------
Builds a 4-panel dashboard. The design intent is that panels 1-3 look
solid and complete (measured data) while panel 4 deliberately looks
incomplete - because the cause data IS incomplete, and a chart that
tidied it up would misrepresent it.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import Patch

nat = pd.read_csv("../data/national_annual.csv")
reg = pd.read_csv("../data/regional_rate.csv")
dem = pd.read_csv("../data/casualty_demographics_2025.csv")
cau = pd.read_csv("../data/stated_causes.csv")
cond = pd.read_csv("../data/road_condition_by_region.csv")

ASPHALT = "#2E3138"
AMBER   = "#E8A33D"
RUST    = "#B5482F"
STONE   = "#9AA0A8"
CREAM   = "#F1EDE6"

fig, axes = plt.subplots(3, 2, figsize=(15, 17))
fig.suptitle("Ghana Road Safety — Outcomes Are Measured Well, Inputs Are Not",
             fontsize=16, fontweight="bold", y=0.995)
fig.text(0.5, 0.973,
         "Sources: National Road Safety Authority (2024–2025 releases) and Ghana Highway Authority (2023 Road Condition Survey) — see README for caveats",
         ha="center", fontsize=9, style="italic", color="gray")

# ---- Panel 1: deaths outpacing crashes -------------------------------
ax = axes[0, 0]
x = [0, 1]
w = 0.35
crash_idx = (nat.crashes / nat.crashes.iloc[0] * 100).tolist()
death_idx = (nat.deaths / nat.deaths.iloc[0] * 100).tolist()
ax.bar([i - w/2 for i in x], crash_idx, w, label="Crashes", color=STONE)
ax.bar([i + w/2 for i in x], death_idx, w, label="Deaths", color=RUST)
ax.set_xticks(x); ax.set_xticklabels(["2024", "2025"])
ax.set_ylabel("Indexed to 2024 = 100")
ax.set_title("Deaths Rose Twice as Fast as Crashes\nFatality rate: 18.5 → 20.0 deaths per 100 crashes", fontsize=11)
ax.axhline(100, color=ASPHALT, lw=0.8, ls="--")
ax.legend(fontsize=9, loc="upper left")
for xi, (c, d) in enumerate(zip(crash_idx, death_idx)):
    ax.text(xi - w/2, c + 1, f"{c:.0f}", ha="center", fontsize=9)
    ax.text(xi + w/2, d + 1, f"{d:.0f}", ha="center", fontsize=9, fontweight="bold")
ax.set_ylim(0, 132)

# ---- Panel 2: rate vs count ------------------------------------------
ax = axes[0, 1]
r = reg.sort_values("crashes", ascending=True)
y = range(len(r))
ax.barh([i - 0.2 for i in y], r.crashes, height=0.4, color=STONE, label="Crashes")
ax.barh([i + 0.2 for i in y], r.deaths, height=0.4, color=RUST, label="Deaths")
ax.set_yticks(list(y)); ax.set_yticklabels(r.region)
ax.set_title("Crash Volume Hides Where People Die\n(Jan–May 2025)", fontsize=11)
ax.set_xlabel("Count")
ax.legend(fontsize=9, loc="lower right")
for i, (_, row) in enumerate(r.iterrows()):
    ax.text(row.crashes + 40, i - 0.2, f"{row.crashes:,}", va="center", fontsize=8.5)
    ax.text(row.deaths + 40, i + 0.2,
            f"{row.deaths}  ({row.deaths_per_100_crashes}/100)",
            va="center", fontsize=8.5, fontweight="bold", color=RUST)

# ---- Panel 3: who dies (complete partition) --------------------------
ax = axes[1, 0]
sex = dem[dem.dimension == "Sex"]
age = dem[dem.dimension == "Age"]
bars = [
    ("Male", sex[sex.category == "Male"].deaths.iat[0], ASPHALT),
    ("Female", sex[sex.category == "Female"].deaths.iat[0], AMBER),
    ("Under 18", age[age.category == "Under 18"].deaths.iat[0], AMBER),
    ("18 and over", age[age.category == "18 and over"].deaths.iat[0], ASPHALT),
]
labels = [b[0] for b in bars]
vals = [b[1] for b in bars]
cols = [b[2] for b in bars]
ax.bar(labels, vals, color=cols)
ax.set_title("Who Dies — Measured, and Sums to 100%\nSex and age each total 2,949 — complete records", fontsize=11)
ax.set_ylabel("Deaths (2025)")
ax.tick_params(axis="x", rotation=12)
total = 2949
for i, v in enumerate(vals):
    ax.text(i, v + 40, f"{v:,}\n({v/total*100:.1f}%)", ha="center", fontsize=9)
ax.set_ylim(0, 3150)

# ---- Panel 4: why they die (deliberately incomplete) -----------------
ax = axes[1, 1]
c = cau.copy()
c["plot_val"] = c.share_pct.fillna(0)
c = c.sort_values("plot_val", ascending=True)
ypos = range(len(c))
for i, (_, row) in enumerate(c.iterrows()):
    if row.quantified:
        ax.barh(i, row.share_pct, color=RUST, height=0.6)
        ax.text(row.share_pct + 1.5, i, f"{row.share_pct:.0f}%",
                va="center", fontsize=9, fontweight="bold", color=RUST)
    else:
        # hatched placeholder bar = named as a cause, never given a number
        ax.barh(i, 60, color="none", edgecolor=STONE, height=0.6,
                hatch="///", linewidth=1.0, alpha=0.85)
        ax.text(2, i, "named, never quantified", va="center",
                fontsize=8.5, style="italic", color=ASPHALT)
ax.set_yticks(list(ypos))
ax.set_yticklabels([t if len(t) < 40 else t[:37] + "…" for t in c.stated_cause], fontsize=8.5)
ax.set_xlim(0, 72)
ax.set_xlabel("Share of crashes attributed (%)")
ax.set_title("Why They Die — Attributed, and Does NOT Sum to 100%\nThe two published figures overlap: a speeding drunk driver counts in both", fontsize=11)
ax.legend(handles=[
    Patch(facecolor=RUST, label="Quantified by NRSA"),
    Patch(facecolor="none", edgecolor=STONE, hatch="///", label="Named only — no figure published"),
], fontsize=8, loc="lower right")


# ---- Panel 5: road condition by region, crash-data regions highlighted ----
ax = axes[2, 0]
c = cond.sort_values("pct_poor", ascending=True)
have = set(reg.region)
colors5 = [RUST if r in have else STONE for r in c.region]
ax.barh(c.region, c.pct_poor, color=colors5)
ax.set_title("Road Condition vs. Crash-Data Coverage\nRed = has published crash+death data; grey = none", fontsize=11)
ax.set_xlabel("% of trunk road length in POOR condition (GHA 2023)")
ax.tick_params(axis="y", labelsize=8.5)
for i, (_, row) in enumerate(c.iterrows()):
    ax.text(row.pct_poor + 0.8, i, f"{row.pct_poor}%", va="center", fontsize=8)

# ---- Panel 6: the paired natural experiment ----
ax = axes[2, 1]
m = reg.merge(cond, on="region")
m = m.sort_values("deaths_per_100_crashes")
x = range(len(m))
w = 0.38
ax.bar([i - w/2 for i in x], m.pct_poor, w, label="% roads POOR", color=STONE)
ax.bar([i + w/2 for i in x], m.deaths_per_100_crashes, w,
       label="Deaths per 100 crashes", color=RUST)
ax.set_xticks(list(x)); ax.set_xticklabels(m.region, fontsize=9)
ax.set_title("Identical Road Quality, 3.8x Different Lethality\nRoad condition cannot explain the fatality gap", fontsize=11)
ax.legend(fontsize=9)
ax.set_ylim(0, 40)
for i, (_, row) in enumerate(m.iterrows()):
    ax.text(i - w/2, row.pct_poor + 0.8, f"{row.pct_poor}%", ha="center", fontsize=9)
    ax.text(i + w/2, row.deaths_per_100_crashes + 0.8,
            f"{row.deaths_per_100_crashes}", ha="center", fontsize=9, fontweight="bold", color=RUST)
ax.text(0.5, 0.80, "all three: 10% poor roads", transform=ax.transAxes,
        ha="center", fontsize=9.5, style="italic", color=ASPHALT)

plt.tight_layout(rect=[0, 0, 1, 0.955])
plt.savefig("../outputs/dashboard.png", dpi=150, bbox_inches="tight")
print("Saved ../outputs/dashboard.png")
