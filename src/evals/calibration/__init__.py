"""Calibration tasks — edge-test node decision boundaries against the
corpus fixtures grid and emit threshold recommendations.

Shared machinery lives in ``base.py`` (fixture loading, confidence binning,
reliability tables, ECE, threshold sweeps, bootstrap CIs, report writing).
Per-node modules register the probing logic; all of them are REPORT-ONLY —
recommended thresholds are written to ``reports/calibration/<task>/``, never
applied to pipeline configs.
"""
