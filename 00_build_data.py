"""
00_build_data.py
------------------
Compiles Ghana road traffic crash data from National Road Safety Authority
(NRSA) publications and reporting, into FOUR deliberately separate datasets.

The separation is the point of this project. NRSA data has two very
different tiers of quality:

  TIER 1 - MEASURED. Counts of crashes, deaths, injuries, and the
  demographic/road-user breakdown of casualties. These come from casualty
  records and form proper partitions (shares sum to 100%).

  TIER 2 - ATTRIBUTED. Stated *causes* of crashes. These are assigned at
  the scene by police/authority officials, are published only as a couple
  of headline percentages, use overlapping categories that do NOT sum to
  100%, and are skewed toward human-factor explanations.

  TIER 3 - INPUTS. Road condition and vehicle age. Road condition IS well
  measured (GHA surveys all 16 regions) but cannot be joined to crash
  outcomes for 13 of them. Vehicle age is not published against crash
  outcomes at all. So the physical inputs to a crash are either
  unjoinable or unmeasured.

Mixing these two tiers into one chart would imply the cause data is as
solid as the casualty data. It is not. See README.

Sources: NRSA via Graphic Online, Ghana News Agency, GhanaWeb, Ghana
Business News, B&FT, CUTS Accra. Full citations in README.
"""

import pandas as pd

# ---------------------------------------------------------------- TIER 1
# National annual totals (NRSA, reported Jan 2026)
national = pd.DataFrame([
    {"year": 2024, "crashes": 13489, "deaths": 2494, "injuries": 15607},
    {"year": 2025, "crashes": 14743, "deaths": 2949, "injuries": 16711},
])
national["deaths_per_100_crashes"] = (national.deaths / national.crashes * 100).round(1)
national.to_csv("../data/national_annual.csv", index=False)

# Regional: Jan-May 2025. This is the cleanest regional cut available
# because it reports crashes AND deaths separately for the same window,
# which is what makes a fatality *rate* computable.
regional = pd.DataFrame([
    {"region": "Greater Accra", "crashes": 1908, "deaths": 161},
    {"region": "Ashanti",       "crashes": 1850, "deaths": 325},
    {"region": "Eastern",       "crashes": 842,  "deaths": 268},
])
regional["deaths_per_100_crashes"] = (regional.deaths / regional.crashes * 100).round(1)
regional["period"] = "Jan-May 2025"
regional.to_csv("../data/regional_rate.csv", index=False)

# Casualty demographics, full-year 2025 — a proper partition
demographics = pd.DataFrame([
    {"dimension": "Sex", "category": "Male",      "deaths": 2352},
    {"dimension": "Sex", "category": "Female",    "deaths": 597},
    {"dimension": "Age", "category": "Under 18",  "deaths": 328},
    {"dimension": "Age", "category": "18 and over","deaths": 2621},
])
demographics.to_csv("../data/casualty_demographics_2025.csv", index=False)

# Road user class share of fatalities.
# CAUTION: this breakdown comes from an older NRSC statistics release, NOT
# from 2025. It is datable to before 2019 because it reports "Brong Ahafo",
# a region split into Bono / Bono East / Ahafo in 2018. It is included only
# as a labelled historical reference and is never combined with 2025 figures.
road_user = pd.DataFrame([
    {"road_user_class": "Pedestrians",     "deaths": 824, "share_pct": 39.5},
    {"road_user_class": "Motorcycle users","deaths": 437, "share_pct": 21.0},
    {"road_user_class": "Bus occupants",   "deaths": 364, "share_pct": 17.5},
])
road_user["source_period"] = "pre-2019 (NRSC release; predates Brong Ahafo split)"
road_user.to_csv("../data/road_user_class_historical.csv", index=False)

# ---------------------------------------------------------------- TIER 2
# Stated causes. Note the 'overlaps' and 'quantified' columns — these exist
# precisely because this data cannot be treated as a clean breakdown.
causes = pd.DataFrame([
    {"stated_cause": "Speeding / reckless driving (bundled)", "share_pct": 60.0,
     "quantified": True,  "note": "Published as a single combined category; the two are not separable"},
    {"stated_cause": "Alcohol", "share_pct": 20.0,
     "quantified": True,  "note": "NRSA figure for 2022; overlaps with speeding category"},
    {"stated_cause": "Wrongful overtaking", "share_pct": None,
     "quantified": False, "note": "Repeatedly named by NRSA officials; never quantified"},
    {"stated_cause": "Overloading", "share_pct": None,
     "quantified": False, "note": "Named as worsening crash severity; never quantified"},
    {"stated_cause": "Driver fatigue", "share_pct": None,
     "quantified": False, "note": "Named especially for commercial drivers; never quantified"},
    {"stated_cause": "Drug use", "share_pct": None,
     "quantified": False, "note": "Tramadol specifically named by NRSA; never quantified"},
    {"stated_cause": "Vehicle defects (brakes, tyres, lighting)", "share_pct": None,
     "quantified": False, "note": "Requires inspection to establish; never quantified"},
    {"stated_cause": "Road infrastructure defects", "share_pct": None,
     "quantified": False, "note": "Requires engineering assessment to establish; never quantified"},
    {"stated_cause": "Low seatbelt / helmet use", "share_pct": None,
     "quantified": False, "note": "Named as a severity factor; never quantified"},
])
causes.to_csv("../data/stated_causes.csv", index=False)

# ---------------------------------------------------------------- TIER 3
# Road condition by region. Ghana Highway Authority 2023 Road Condition
# Survey, Table 8 (all paved and unpaved trunk roads), % of surveyed length.
# NOTE: GHA covers TRUNK roads only - 15,360km of a ~94,203km national
# network (~16%). Urban roads sit with the Dept of Urban Roads and feeder
# roads with the Dept of Feeder Roads, neither of which publishes an
# equivalent regional condition survey. This matters most for Greater
# Accra, whose crashes are overwhelmingly urban.
road_condition = pd.DataFrame([
    ("Ahafo",18,63,19),("Ashanti",48,42,10),("Bono",10,78,12),("Bono East",19,58,23),
    ("Central",36,42,22),("Eastern",43,47,10),("Greater Accra",43,47,10),("North East",22,41,37),
    ("Northern",66,25,8),("Oti",51,33,16),("Savannah",44,52,4),("Upper East",7,55,39),
    ("Upper West",25,20,54),("Volta",24,61,15),("Western",31,27,43),("Western North",75,14,11),
], columns=["region","pct_good","pct_fair","pct_poor"])
road_condition["source"] = "GHA Road Condition Survey 2023, Table 8 (trunk roads only)"
road_condition.to_csv("../data/road_condition_by_region.csv", index=False)

# Vehicle age. Fleet-level context exists; crash-linked age data does not.
vehicle_age = pd.DataFrame([
    {"metric": "Registered vehicles (DVLA)", "value": "~4,000,000", "crash_linked": False},
    {"metric": "Share of fleet that is used imports", "value": "~90%", "crash_linked": False},
    {"metric": "Used vehicles imported annually (2024 est.)", "value": ">100,000", "crash_linked": False},
    {"metric": "Import age limit (GS 4510:2022)", "value": "10 years", "crash_linked": False},
    {"metric": "CIF penalty, 10-12 year old vehicles", "value": "12.5%", "crash_linked": False},
    {"metric": "CIF penalty, 12-15 year old vehicles", "value": "20%", "crash_linked": False},
    {"metric": "Crashes broken down by vehicle age", "value": "NOT PUBLISHED", "crash_linked": False},
    {"metric": "Fatality rate by vehicle age", "value": "NOT PUBLISHED", "crash_linked": False},
])
vehicle_age.to_csv("../data/vehicle_age_availability.csv", index=False)

print("TIER 1 (measured):")
print(national.to_string(index=False))
print()
print(regional.to_string(index=False))
print()
print("TIER 3 (inputs):")
print(f"  regions with road-condition data: {len(road_condition)}/16")
merged = regional.merge(road_condition, on="region")
print(f"  regions with BOTH condition and crash+death data: {len(merged)}/16")
print(merged[["region","pct_good","pct_fair","pct_poor","deaths_per_100_crashes"]].to_string(index=False))
print(f"  vehicle-age metrics available: {len(vehicle_age)}, "
      f"of which linked to crash outcomes: {vehicle_age.crash_linked.sum()}")
print()
print("TIER 2 (attributed):")
print(f"  causes listed: {len(causes)}")
print(f"  of which quantified: {causes.quantified.sum()}")
print(f"  quantified shares sum to: {causes.share_pct.sum():.0f}% "
      f"(NOT 100% - categories overlap and are incomplete)")
