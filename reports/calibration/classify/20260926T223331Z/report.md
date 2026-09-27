# Calibration report — classify

| Key | Value |
|---|---|
| generated_at | 2026-09-26T22:33:31+00:00 |
| n_cases | 1 |
| errors | 0 |
| ece | 0.025 |

## Calibration-cell confusion

| cell | n | agreed | agreement |
|---|---|---|---|
| correct_high | 1 | 1 | 1 |

## Reliability (confidence bin → accuracy)

| bin | n | accuracy |
|---|---|---|
| 0.95-1.00 | 1 | 1 |

## Threshold sweep

| threshold | tp | fp | fn | precision | recall | f2 |
|---|---|---|---|---|---|---|
| 0.05 | 0 | 1 | 0 | 0 | — | — |
| 0.1 | 0 | 1 | 0 | 0 | — | — |
| 0.15 | 0 | 1 | 0 | 0 | — | — |
| 0.2 | 0 | 1 | 0 | 0 | — | — |
| 0.25 | 0 | 1 | 0 | 0 | — | — |
| 0.3 | 0 | 1 | 0 | 0 | — | — |
| 0.35 | 0 | 1 | 0 | 0 | — | — |
| 0.4 | 0 | 1 | 0 | 0 | — | — |
| 0.45 | 0 | 1 | 0 | 0 | — | — |
| 0.5 | 0 | 1 | 0 | 0 | — | — |
| 0.55 | 0 | 1 | 0 | 0 | — | — |
| 0.6 | 0 | 1 | 0 | 0 | — | — |
| 0.65 | 0 | 1 | 0 | 0 | — | — |
| 0.7 | 0 | 1 | 0 | 0 | — | — |
| 0.75 | 0 | 1 | 0 | 0 | — | — |
| 0.8 | 0 | 1 | 0 | 0 | — | — |
| 0.85 | 0 | 1 | 0 | 0 | — | — |
| 0.9 | 0 | 1 | 0 | 0 | — | — |
| 0.95 | 0 | 1 | 0 | 0 | — | — |

## Caveats

- small fixture sample (n=1) — CIs are wide; extend fixtures before trusting thresholds
