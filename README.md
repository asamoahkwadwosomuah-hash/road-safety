# Ghana Road Safety: Outcomes Are Measured Well, Inputs Are Not

**A data-quality analysis — Python, pandas, matplotlib — showing that Ghana records *who* dies on its roads with real rigour, but cannot say *why*, because the causes and the physical inputs to a crash are either unquantified, unjoinable, or unpublished.**

## Background

2025 was Ghana's deadliest year on the roads in 35 years: **2,949 people killed** across 14,743 reported crashes, an 18.2% rise in deaths over 2024. Cumulative road deaths since 1991 exceed 63,000.

This project started as a straightforward analysis of that data. It became a data-quality project because three separate attempts to explain the deaths — by stated cause, by road condition, and by vehicle age — each ran into the same wall from a different direction.

The distinction matters because road safety budgets are allocated against stated causes. If speeding is the only cause with a number attached, speeding is what gets funded.

## The central finding

| Layer | What it covers | Quality |
|---|---|---|
| **Outcomes** | Crashes, deaths, injuries, casualty demographics | Complete. Shares form proper partitions summing to 100%. |
| **Attribution** | Stated causes of crashes | 2 of 9 named causes carry any figure. The two overlap. |
| **Input: road condition** | Road surface quality by region | Well measured for **16/16** regions — joinable to crash outcomes for only **3/16**. |
| **Input: vehicle age** | Age of vehicles involved in crashes | **Not published at all.** Zero metrics link vehicle age to crash outcomes. |

Ghana knows precisely who is dying. It cannot say what is killing them.

## Research questions

1. Did deaths rise faster than crashes in 2025 — did crashes become deadlier, not just more frequent?
2. Does crash volume tell you where people actually die?
3. **Outcomes:** who dies, and how completely is that recorded?
4. **Attribution:** why do they die, and how completely is *that* recorded?
5. **Input:** does road condition explain where crashes are deadliest?
6. **Input:** does vehicle age explain crash outcomes?
7. Do official sources agree with each other?

## Key findings

### Outcomes — reliable

- **Crashes got deadlier, not just more numerous.** Crashes rose 9.3% in 2025 but deaths rose 18.2% — roughly twice as fast. The fatality rate moved from 18.5 to 20.0 deaths per 100 crashes. A headline of "more crashes" understates what changed.

- **Crash volume actively misleads about where people die.** Over January–May 2025, Greater Accra recorded the most crashes (1,908) but only 161 deaths. Eastern recorded fewer than half as many crashes (842) yet 268 deaths. Per 100 crashes that is **31.8 deaths in Eastern against 8.4 in Greater Accra — Eastern is 3.8× deadlier to crash in.** Ranking regions by crash count puts Greater Accra first and hides this entirely. (This mirrors the rate-versus-absolute-numbers tension found in the Youth NEET and Literacy projects in this portfolio.)

- **Casualty records are genuinely good.** 2025 deaths break down as 2,352 male (79.8%) and 597 female (20.2%); 328 under 18 (11.1%) and 2,621 adults (88.9%). Both dimensions total exactly 2,949 — complete, non-overlapping partitions.

### Attribution — incomplete

- **Only 2 of 9 named causes carry any published figure**: speeding/reckless driving at over 60%, and alcohol at around 20% (2022). Those two overlap — a speeding drunk driver falls in both — so they cannot be charted as slices of a whole. The seven never quantified are wrongful overtaking, overloading, driver fatigue, drug use, vehicle defects, road infrastructure defects, and low seatbelt/helmet use.

- **The unquantified causes are systematically the non-human ones.** Vehicle defects and road infrastructure defects require inspection and engineering assessment to establish; a roadside officer can record "speeding" immediately. The attribution process is biased toward driver blame — not because driver behaviour isn't real, but because it is the only factor cheap enough to record at scale.

### Inputs — untestable

- **Road condition cannot explain the fatality gap.** The three regions with published crash *and* death figures have an **identical poor-road share of 10%**. Greater Accra and Eastern have *completely identical* condition mixes — 43% good, 47% fair, 10% poor — yet Eastern is 3.8× deadlier per crash. Holding road quality constant does not close the gap.

- **But the road-condition test is not a real test.** Three reasons: n = 3 regions, so no correlation coefficient is meaningful; the data is missing precisely where it would matter, since the worst-road regions — Upper West (54% poor), Western (43%), Upper East (39%), North East (37%) — have no published crash breakdown at all; and GHA surveys **trunk roads only**, about 15,360 km of a ~94,203 km national network (~16%), which is a particular problem for Greater Accra, whose crashes are overwhelmingly on urban roads the survey does not cover.

- **Vehicle age cannot be tested at all.** NRSA records vehicles involved by *category* — private, commercial, motorcycle, tricycle — never by age. Fleet context exists (roughly 4 million registered vehicles, about 90% used imports, over 100,000 used vehicles imported annually, a 10-year import age limit under GS 4510:2022 with CIF penalties of 12.5% at 10–12 years and 20% at 12–15 years), but **zero** of it is linked to crash outcomes. Ghana is running age-based import policy without measuring whether vehicle age drives Ghanaian crash outcomes.

- **The one Ghanaian figure that touches vehicle condition is unreliable for the same reason as the cause data.** The largest available study, covering 200,528 driver/rider cases from BRRI data 2001–2011, reports that 87.46% of accidents could not be linked to the fault of the vehicle. A Monash review of this literature notes the real difficulty of detecting defects in crashed vehicles and concludes that this suggests under-reporting of the contribution of defects. An 87% "no vehicle fault" rate produced by scene attribution is a statement about what was not inspected. For contrast, NHTSA finds drivers of vehicles 18+ years old **71% more likely to be fatally injured** than drivers of vehicles three years or newer.

### Data integrity

- **Two official NRSA sources disagree on Ashanti.** The national release reports Ashanti deaths up by 146 (+10.5%); the Ashanti regional NRSA head reports 626 → 692 (also +10.5%). Identical percentage, incompatible absolute figures — likely different scopes (administrative region vs police region), but this project does not guess. The discrepancy is reported as-is.

## Limitations

- **Underreporting is documented.** A peer-reviewed study found 345 deaths across combined sources against 148 in hospital data alone, so single-source counts can miss more than half. All figures here are floors, not true counts.
- **The 2025 rise has a confound.** NRSA's Director of Research attributed part of the increase to the authority's own inactivity in 2024 due to logistical constraints, with some regional offices virtually closed. How much of the rise is more crashes versus better capture is not separable from published data.
- **Road condition is measured by length, not exposure.** A poor 50 km road carrying almost no traffic counts the same as a poor 50 km road carrying the Accra–Kumasi freight load. Without traffic volume, condition share is a weak proxy for risk.
- **Timing mismatch.** Road condition is 2023; crash data is 2025.
- **No machine-readable source.** The NRSA domain currently resolves to an unrelated municipal page and the legacy NRSC statistics page blocks automated access, so NRSA figures were transcribed from official releases and cross-checked across outlets. GHA figures come directly from its published quarterly report PDF.
- **The road-user-class breakdown is historical.** `road_user_class_historical.csv` predates 2019 (it reports "Brong Ahafo", split into three regions in 2018). It is labelled as such and never combined with 2025 figures.
- **Reporting windows differ.** NRSA published Q1, Jan–May, H1, Jan–Aug and full-year cuts for 2025. Each analysis states its window; windows are never mixed.

## What would fix this

The outcome side of Ghana's road data is already strong. Three specific gaps block causal analysis:

1. **Publish crash and death counts for all 16 regions**, not three. The current coverage excludes every one of the worst-road regions, making the road-quality question structurally unanswerable.
2. **Record vehicle age at the crash scene.** DVLA already holds registration year; linking it to crash records costs nothing new to collect and would immediately test a policy Ghana is already enforcing.
3. **Investigate a sample of fatal crashes in depth** — vehicle inspection and road-condition assessment, not scene attribution — and report causes as mutually exclusive categories summing to 100%. Without this, "speeding causes 60% of crashes" is a statement about what is easy to observe, not a measured share.

## Repo structure

```
data/           six datasets kept deliberately separate by tier:
                national_annual, regional_rate, casualty_demographics_2025,
                stated_causes, road_condition_by_region,
                vehicle_age_availability (+ historical road-user file)
notebooks/      data compilation, analysis, and dashboard scripts
outputs/        dashboard.png (6 panels)
```

## Sources

- National Road Safety Authority (NRSA) 2025 annual crash statistics, via Graphic Online (Jan 2026)
- NRSA National Road Traffic Crash and Casualty Situation Statistics, Jan–May 2025, via Ghana News Agency (Jun 2025)
- NRSA Ashanti regional data, via Ghana News Agency and Ghana Business News (Feb 2026)
- NRSA H1 and Jan–Aug 2025 figures, via GhanaWeb (Jul 2025) and Ghana News Agency (Oct 2025)
- NRSA alcohol attribution (2022), via CUTS Accra
- **Ghana Highway Authority, 1st Quarter Report 2024 — Table 8, 2023 Road Condition Survey (all 16 regions)**
- Driver and Vehicle Licensing Authority fleet figures, via Graphic Online; Ghana Standard GS 4510:2022 via US ITA
- "The Influences of Drivers/Riders in Road Traffic Crashes in Ghana between 2001 and 2011" (BRRI data)
- Monash University Accident Research Centre, "The effect of vehicle roadworthiness on crash incidence and severity"
- NHTSA, "How Vehicle Age and Model Year Relate to Driver Injury Severity" (FARS 2005–2011)
- "Lessons written in blood: Ghana's road safety crisis", B&FT (Oct 2025)

## Tools used

Python (pandas, matplotlib), multi-source transcription and cross-checking, rate-versus-count analysis, cross-dataset joins, data-availability and completeness assessment.

---
*This project analyses officially published road safety statistics. It is not affiliated with or endorsed by the NRSA or GHA. Figures are as published and have not been independently audited.*
