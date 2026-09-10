"""
01_analysis.py
----------------
Analyses Ghana's road crash data along three axes:
  (a) what the well-measured casualty data shows        (outcomes)
  (b) what the cause-attribution data cannot show       (attribution)
  (c) whether the physical inputs to a crash - road condition and
      vehicle age - can be tested against outcomes at all   (inputs)

Also documents an unresolved inconsistency between two official NRSA
sources on Ashanti regional deaths.
"""

import pandas as pd

nat = pd.read_csv("../data/national_annual.csv")
reg = pd.read_csv("../data/regional_rate.csv")
dem = pd.read_csv("../data/casualty_demographics_2025.csv")
cau = pd.read_csv("../data/stated_causes.csv")
cond = pd.read_csv("../data/road_condition_by_region.csv")
veh = pd.read_csv("../data/vehicle_age_availability.csv")

BAR = "=" * 66

print(BAR)
print("Q1. Did deaths rise faster than crashes in 2025?")
print(BAR)
c24, c25 = nat.loc[nat.year == 2024], nat.loc[nat.year == 2025]
crash_chg = (c25.crashes.iat[0] / c24.crashes.iat[0] - 1) * 100
death_chg = (c25.deaths.iat[0] / c24.deaths.iat[0] - 1) * 100
print(f"  crashes  {c24.crashes.iat[0]:,} -> {c25.crashes.iat[0]:,}  ({crash_chg:+.1f}%)")
print(f"  deaths   {c24.deaths.iat[0]:,} -> {c25.deaths.iat[0]:,}  ({death_chg:+.1f}%)")
print(f"  fatality rate {c24.deaths_per_100_crashes.iat[0]} -> "
      f"{c25.deaths_per_100_crashes.iat[0]} deaths per 100 crashes")
print("\n  Deaths rose roughly twice as fast as crashes. Ghana's roads did not")
print("  just get busier with collisions - the collisions got deadlier.")

print("\n" + BAR)
print("Q2. Does crash volume tell you where people die? (rate vs count)")
print(BAR)
print(reg.sort_values("deaths_per_100_crashes").to_string(index=False))
hi = reg.loc[reg.deaths_per_100_crashes.idxmax()]
lo = reg.loc[reg.deaths_per_100_crashes.idxmin()]
print(f"\n  {hi.region} has {lo.crashes/hi.crashes:.1f}x FEWER crashes than {lo.region},")
print(f"  but {hi.deaths/lo.deaths:.1f}x MORE deaths.")
print(f"  Per 100 crashes: {hi.region} {hi.deaths_per_100_crashes} vs "
      f"{lo.region} {lo.deaths_per_100_crashes} "
      f"({hi.deaths_per_100_crashes/lo.deaths_per_100_crashes:.1f}x deadlier).")
print("\n  Ranking regions by crash count would put Greater Accra first and")
print("  hide that Eastern is by far the most lethal place to crash.")

print("\n" + BAR)
print("Q3. OUTCOMES - who dies? (measured, forms a proper partition)")
print(BAR)
for dim in dem.dimension.unique():
    sub = dem[dem.dimension == dim].copy()
    sub["share_pct"] = (sub.deaths / sub.deaths.sum() * 100).round(1)
    print(f"  {dim}:")
    for _, r in sub.iterrows():
        print(f"    {r.category:<14} {r.deaths:>6,}  ({r.share_pct:>5.1f}%)")
    print(f"    {'TOTAL':<14} {sub.deaths.sum():>6,}  (100.0%)  <- sums correctly")

print("\n" + BAR)
print("Q4. ATTRIBUTION - why do they die? (does NOT form a partition)")
print(BAR)
q = cau[cau.quantified]
u = cau[~cau.quantified]
print(f"  causes named by officials: {len(cau)}")
print(f"  causes given any number:   {len(q)}  ({len(q)/len(cau)*100:.0f}%)")
print(f"  causes never quantified:   {len(u)}  ({len(u)/len(cau)*100:.0f}%)")
print(f"\n  The two quantified shares sum to {q.share_pct.sum():.0f}% - and they OVERLAP")
print("  (a drunk driver who is speeding falls in both). So they cannot be")
print("  charted as slices of a whole. Never quantified at all:")
for _, r in u.iterrows():
    print(f"    - {r.stated_cause}")

print("\n" + BAR)
print("Q5. INPUTS (i) - does road condition explain where crashes are deadliest?")
print(BAR)
m = reg.merge(cond, on="region")
print(m[["region", "pct_good", "pct_fair", "pct_poor", "deaths_per_100_crashes"]].to_string(index=False))
print(f"\n  All three regions share an IDENTICAL poor-road share: {sorted(m.pct_poor.unique())}%")
ga = m[m.region == "Greater Accra"].iloc[0]
ea = m[m.region == "Eastern"].iloc[0]
print(f"  Greater Accra and Eastern have IDENTICAL condition mixes "
      f"({ga.pct_good}/{ga.pct_fair}/{ga.pct_poor} good/fair/poor),")
print(f"  yet Eastern is {ea.deaths_per_100_crashes/ga.deaths_per_100_crashes:.1f}x deadlier per crash "
      f"({ea.deaths_per_100_crashes} vs {ga.deaths_per_100_crashes}).")
print("\n  Holding road quality constant does not close the fatality gap, so road")
print("  surface condition cannot be what separates these two regions.")
print("\n  BUT this is not a real test, for three reasons:")
print("    1. n = 3 regions. No correlation coefficient would be meaningful.")
print("    2. The data is missing exactly where it would matter - the worst-road")
print("       regions have NO published crash/death breakdown:")
for _, r in cond.nlargest(4, "pct_poor").iterrows():
    print(f"         {r.region:<16} {r.pct_poor}% poor roads   - no crash data published")
print("    3. GHA surveys TRUNK roads only (~16% of the national network).")
print("       Greater Accra's crashes are overwhelmingly on urban roads that")
print("       this survey does not cover.")

print("\n" + BAR)
print("Q6. INPUTS (ii) - does vehicle age explain crash outcomes?")
print(BAR)
print(f"  vehicle-age metrics published:      {len(veh)}")
print(f"  of those linked to crash outcomes:  {int(veh.crash_linked.sum())}")
print("\n  Fleet context IS published:")
for _, r in veh[veh.value != "NOT PUBLISHED"].iterrows():
    print(f"    {r.metric:<45} {r.value}")
print("\n  Crash-linked age data is NOT:")
for _, r in veh[veh.value == "NOT PUBLISHED"].iterrows():
    print(f"    {r.metric:<45} {r.value}")
print("\n  NRSA records vehicles involved by CATEGORY (private / commercial /")
print("  motorcycle), never by AGE, so the question cannot be answered with")
print("  Ghanaian data. International evidence suggests the effect is large:")
print("  NHTSA finds drivers of 18+ year old vehicles 71% more likely to be")
print("  fatally injured than drivers of vehicles 3 years old or newer.")

print("\n" + BAR)
print("Q7. Data-integrity check: Ashanti 2025 deaths")
print(BAR)
print("  Two official NRSA sources give different figures for the same region")
print("  and year, both stating the same +10.5% change:")
print("    national NRSA release (via Graphic): +146 deaths, implying ~1,536")
print("    Ashanti regional NRSA head (via GNA): 626 -> 692 deaths")
print("  Identical percentage, incompatible absolute numbers. This project does")
print("  NOT pick one. The discrepancy is reported as-is; resolving it would")
print("  require the underlying NRSA tables, which are not public.")

print("\n" + BAR)
print("SUMMARY: outcomes vs inputs")
print(BAR)
print("  OUTCOMES (who, where, how many)   : complete, partitioned, reliable")
print("  ATTRIBUTION (why)                 : 2 of 9 causes quantified, overlapping")
print("  INPUT - road condition            : measured for 16/16 regions,")
print("                                      joinable for only 3/16")
print("  INPUT - vehicle age               : 0 metrics linked to crash outcomes")
print("\n  Ghana measures road OUTCOMES well and road INPUTS badly.")
