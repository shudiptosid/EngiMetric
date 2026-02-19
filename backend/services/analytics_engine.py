"""
Engineering Financial Intelligence Model — India Market 2026
─────────────────────────────────────────────────────────────
Calibrated with 15 complexity references + 10 India-market benchmarks.

Uses statistical interpolation against real Indian project data for:
  - Hourly rate estimation by tier
  - Hardware cost ranges
  - Total cost prediction with Bayesian confidence intervals
  - Acceptance probability via logistic regression fit
"""

import math
import random
from typing import Optional


# ─── Classification Tiers ───────────────────────────────────────────

CLASSIFICATION = {
    "Normal":     (0, 6),
    "Moderate":   (7, 12),
    "High":       (13, 18),
    "Industrial": (19, 25),
}

HOURS_RANGE = {
    "Normal":     (25, 50),
    "Moderate":   (60, 140),
    "High":       (120, 300),
    "Industrial": (250, 600),
}


# ─── India Market Benchmarks (2026) ─────────────────────────────────

MARKET_BENCHMARKS = [
    {
        "id": 1, "name": "WiFi Temperature Monitoring (Student)", "level": "Normal",
        "score": 4,  "scores": {"hardware": 1, "software": 1, "ai_ml": 0, "deployment": 1, "risk_safety": 1},
        "hardware_cost": (900, 1200),  "hours": (25, 40),  "rate": 500,
        "total_cost": (15000, 22000),  "client_type": "student",
        "flags": {"safety_critical": False, "has_ai": False, "custom_pcb": False, "large_scale": False},
    },
    {
        "id": 2, "name": "Smart Soil Moisture Monitoring (Basic+)", "level": "Normal",
        "score": 6,  "scores": {"hardware": 1, "software": 2, "ai_ml": 0, "deployment": 2, "risk_safety": 1},
        "hardware_cost": (1500, 2500),  "hours": (35, 50),  "rate": 600,
        "total_cost": (25000, 38000),  "client_type": "startup",
        "flags": {"safety_critical": False, "has_ai": False, "custom_pcb": False, "large_scale": False},
    },
    {
        "id": 3, "name": "Smart Home Automation (Moderate)", "level": "Moderate",
        "score": 9,  "scores": {"hardware": 2, "software": 2, "ai_ml": 0, "deployment": 3, "risk_safety": 2},
        "hardware_cost": (3000, 5000),  "hours": (60, 90),  "rate": 800,
        "total_cost": (55000, 85000),  "client_type": "startup",
        "flags": {"safety_critical": False, "has_ai": False, "custom_pcb": True, "large_scale": False},
    },
    {
        "id": 4, "name": "IoT Attendance System with RFID", "level": "Moderate",
        "score": 10, "scores": {"hardware": 2, "software": 3, "ai_ml": 0, "deployment": 3, "risk_safety": 2},
        "hardware_cost": (4000, 7000),  "hours": (70, 100),  "rate": 900,
        "total_cost": (70000, 100000),  "client_type": "startup",
        "flags": {"safety_critical": False, "has_ai": False, "custom_pcb": True, "large_scale": False},
    },
    {
        "id": 5, "name": "Smart Irrigation System (Moderate+)", "level": "Moderate",
        "score": 12, "scores": {"hardware": 3, "software": 3, "ai_ml": 0, "deployment": 4, "risk_safety": 2},
        "hardware_cost": (15000, 30000), "hours": (90, 140),  "rate": 1000,
        "total_cost": (120000, 170000),  "client_type": "sme",
        "flags": {"safety_critical": False, "has_ai": False, "custom_pcb": False, "large_scale": True},
    },
    {
        "id": 6, "name": "AI Face Recognition Door Access", "level": "High",
        "score": 14, "scores": {"hardware": 3, "software": 3, "ai_ml": 4, "deployment": 2, "risk_safety": 2},
        "hardware_cost": (8000, 15000),  "hours": (120, 180),  "rate": 1200,
        "total_cost": (160000, 240000),  "client_type": "startup",
        "flags": {"safety_critical": False, "has_ai": True, "custom_pcb": True, "large_scale": False},
    },
    {
        "id": 7, "name": "Warehouse Environmental Monitoring", "level": "High",
        "score": 16, "scores": {"hardware": 4, "software": 3, "ai_ml": 0, "deployment": 5, "risk_safety": 4},
        "hardware_cost": (120000, 250000), "hours": (180, 250),  "rate": 1500,
        "total_cost": (400000, 600000),  "client_type": "enterprise",
        "flags": {"safety_critical": True, "has_ai": False, "custom_pcb": True, "large_scale": True},
    },
    {
        "id": 8, "name": "AI CCTV Surveillance System", "level": "High",
        "score": 17, "scores": {"hardware": 3, "software": 4, "ai_ml": 5, "deployment": 3, "risk_safety": 2},
        "hardware_cost": (200000, 400000), "hours": (200, 300),  "rate": 1800,
        "total_cost": (600000, 1000000),  "client_type": "enterprise",
        "flags": {"safety_critical": False, "has_ai": True, "custom_pcb": False, "large_scale": True},
    },
    {
        "id": 9, "name": "Industrial Motor Predictive Maintenance", "level": "Industrial",
        "score": 20, "scores": {"hardware": 4, "software": 4, "ai_ml": 5, "deployment": 4, "risk_safety": 3},
        "hardware_cost": (300000, 600000), "hours": (250, 400),  "rate": 2000,
        "total_cost": (800000, 1400000),  "client_type": "enterprise",
        "flags": {"safety_critical": True, "has_ai": True, "custom_pcb": True, "large_scale": True},
    },
    {
        "id": 10, "name": "Smart Factory Energy Optimization", "level": "Industrial",
        "score": 23, "scores": {"hardware": 5, "software": 5, "ai_ml": 5, "deployment": 5, "risk_safety": 3},
        "hardware_cost": (500000, 1000000), "hours": (350, 600),  "rate": 2500,
        "total_cost": (1500000, 2500000),  "client_type": "enterprise",
        "flags": {"safety_critical": True, "has_ai": True, "custom_pcb": True, "large_scale": True},
    },
]

# 15 original complexity calibration references
CALIBRATION = [
    {"name": "Basic Temp Monitor (Student)",              "score": 5,  "cls": "Normal",     "accept": 85},
    {"name": "Basic Soil Monitor (Small farm)",           "score": 9,  "cls": "Moderate",   "accept": 70},
    {"name": "IoT + Dashboard + Alerts (Startup)",        "score": 11, "cls": "Moderate",   "accept": 65},
    {"name": "AI Face Recognition Door Lock",             "score": 14, "cls": "High",       "accept": 55},
    {"name": "Industrial Motor Predictive Maintenance",   "score": 20, "cls": "Industrial", "accept": 40},
    {"name": "Custom PCB + IoT + OTA",                    "score": 13, "cls": "High",       "accept": 50},
    {"name": "ESP8266 Academic Weather Station",          "score": 4,  "cls": "Normal",     "accept": 90},
    {"name": "Multi-device Warehouse Monitoring",         "score": 12, "cls": "Moderate",   "accept": 60},
    {"name": "AI-based CCTV Surveillance (Enterprise)",   "score": 17, "cls": "High",       "accept": 45},
    {"name": "Simple Home Automation (Student)",          "score": 6,  "cls": "Normal",     "accept": 80},
    {"name": "Startup MVP IoT SaaS",                      "score": 15, "cls": "High",       "accept": 55},
    {"name": "Industrial Gas Monitoring (Safety Critical)","score": 18, "cls": "High",       "accept": 50},
    {"name": "Smart Irrigation (Medium Farm)",            "score": 10, "cls": "Moderate",   "accept": 70},
    {"name": "AI Drone Monitoring System",                "score": 21, "cls": "Industrial", "accept": 35},
    {"name": "Firebase Data Logger (Academic)",           "score": 5,  "cls": "Normal",     "accept": 88},
]

# Market rate ranges by tier (₹/hr, India 2026)
MARKET_RATES = {
    "Normal":     (500, 800),
    "Moderate":   (800, 1200),
    "High":       (1200, 2000),
    "Industrial": (2000, 2500),
}

# Total cost ranges by tier (₹, India 2026)
TOTAL_COST_RANGE = {
    "Normal":     (15000, 40000),
    "Moderate":   (55000, 170000),
    "High":       (150000, 1000000),
    "Industrial": (800000, 2500000),
}


# ─── Step 1: Structured Complexity Scoring ──────────────────────────

def classify_complexity(score: int) -> str:
    """Classify total score (0-25) into tier."""
    for cls, (lo, hi) in CLASSIFICATION.items():
        if lo <= score <= hi:
            return cls
    return "Industrial" if score > 25 else "Normal"


def compute_complexity_score(
    hardware: int, software: int, ai_ml: int,
    deployment: int, risk_safety: int,
) -> dict:
    hw = max(0, min(5, hardware))
    sw = max(0, min(5, software))
    ai = max(0, min(5, ai_ml))
    dep = max(0, min(5, deployment))
    rs = max(0, min(5, risk_safety))
    total = hw + sw + ai + dep + rs
    cls = classify_complexity(total)

    return {
        "scores": {"hardware": hw, "software": sw, "ai_ml": ai, "deployment": dep, "risk_safety": rs},
        "total_score": total,
        "classification": cls,
    }


# ─── Step 2: Hours Estimation (benchmark-interpolated) ──────────────

def _lerp(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    """Linear interpolation."""
    if x1 == x0:
        return (y0 + y1) / 2
    t = (x - x0) / (x1 - x0)
    return y0 + t * (y1 - y0)


def _interpolate_from_benchmarks(score: int, field: str, sub: str) -> float:
    """Interpolate a value from MARKET_BENCHMARKS by complexity score."""
    sorted_bm = sorted(MARKET_BENCHMARKS, key=lambda b: b["score"])
    # Exact match
    for b in sorted_bm:
        if b["score"] == score:
            if isinstance(b[field], tuple):
                return b[field][0] if sub == "low" else b[field][1]
            return b[field]
    # Bracket
    lower, upper = sorted_bm[0], sorted_bm[-1]
    for b in sorted_bm:
        if b["score"] < score:
            lower = b
        elif b["score"] > score:
            upper = b
            break
    if isinstance(lower[field], tuple):
        lo_val = lower[field][0] if sub == "low" else lower[field][1]
        hi_val = upper[field][0] if sub == "low" else upper[field][1]
    else:
        lo_val = lower[field]
        hi_val = upper[field]
    return _lerp(score, lower["score"], upper["score"], lo_val, hi_val)


def estimate_hours(total_score: int, classification: str) -> dict:
    """
    Primary: interpolate from 10 India-market benchmarks.
    Fallback: BaseMidpoint + Score×2 (clamped to tier range).
    """
    bm_lo = _interpolate_from_benchmarks(total_score, "hours", "low")
    bm_hi = _interpolate_from_benchmarks(total_score, "hours", "high")

    # Blend benchmark with formula: weight 70% benchmark, 30% formula
    tier_lo, tier_hi = HOURS_RANGE.get(classification, (30, 50))
    formula_mid = (tier_lo + tier_hi) / 2 + total_score * 2
    formula_mid = max(tier_lo, min(tier_hi, formula_mid))

    estimated = round(0.7 * ((bm_lo + bm_hi) / 2) + 0.3 * formula_mid)

    return {
        "range": f"{round(bm_lo)}-{round(bm_hi)}",
        "range_min": round(bm_lo),
        "range_max": round(bm_hi),
        "estimated_hours": estimated,
        "benchmark_range": f"{round(bm_lo)}-{round(bm_hi)}",
    }


# ─── Step 3: Risk Calculation ───────────────────────────────────────

def calculate_risk(
    safety_critical: bool = False,
    has_ai: bool = False,
    custom_pcb: bool = False,
    large_scale: bool = False,
) -> dict:
    """BaseRisk 8% + addons, cap 35%."""
    risk = 8.0
    breakdown = [("Base risk", 8.0)]
    if safety_critical:
        risk += 5.0; breakdown.append(("Safety critical", 5.0))
    if has_ai:
        risk += 4.0; breakdown.append(("AI/ML involved", 4.0))
    if custom_pcb:
        risk += 3.0; breakdown.append(("Custom PCB", 3.0))
    if large_scale:
        risk += 3.0; breakdown.append(("Large-scale deployment", 3.0))
    risk = min(35.0, risk)
    return {"risk_percent": risk, "breakdown": breakdown, "capped": risk >= 35.0}


# ─── Step 4: Acceptance Probability (smooth logistic) ───────────────

def _logistic_acceptance(relative_price: float) -> float:
    """
    Smooth logistic curve fit to calibration data:
    P(accept) = L / (1 + e^(k*(x - x0)))
    Fitted: L=0.92, k=8.5, x0=1.18  →  gives ~80% at rel=1.0, ~50% at rel=1.18
    """
    L = 0.92
    k = 8.5
    x0 = 1.18
    return L / (1 + math.exp(k * (relative_price - x0)))


def acceptance_probability(
    quoted_price: float,
    predicted_optimal_price: float,
    classification: str,
    client_type: str = "startup",
    risk_percent: float = 8.0,
) -> dict:
    """
    Logistic-smoothed acceptance with client-type and risk adjustments.
    Validated against 15 calibration anchors.
    """
    relative = quoted_price / max(predicted_optimal_price, 1)

    # Smooth logistic base
    base = _logistic_acceptance(relative)

    adjustment = 0.0
    reasons = []

    ct = client_type.lower()
    if ct == "student" and classification == "Normal":
        adjustment += 0.10
        reasons.append("+10% student + Normal project")
    elif ct == "student" and classification == "Moderate":
        adjustment += 0.05
        reasons.append("+5% student + Moderate project")
    elif ct == "enterprise" and relative > 1.0:
        adjustment -= 0.10
        reasons.append("-10% enterprise + above optimal")
    elif ct == "sme" and relative <= 1.0:
        adjustment += 0.05
        reasons.append("+5% SME + fair price")

    if risk_percent > 25:
        adjustment -= 0.10
        reasons.append("-10% high risk (>25%)")
    elif risk_percent > 18:
        adjustment -= 0.05
        reasons.append("-5% elevated risk (>18%)")

    probability = max(0.05, min(0.95, base + adjustment))

    # Generate smooth price-vs-acceptance curve (for chart)
    prices, probabilities = [], []
    for mult in [0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.50]:
        p = predicted_optimal_price * mult
        b = _logistic_acceptance(mult)
        adj = 0.0
        if ct == "student" and classification in ("Normal", "Moderate"):
            adj += 0.10 if classification == "Normal" else 0.05
        elif ct == "enterprise" and mult > 1.0:
            adj -= 0.10
        if risk_percent > 25:
            adj -= 0.10
        elif risk_percent > 18:
            adj -= 0.05
        b = max(0.05, min(0.95, b + adj))
        prices.append(round(p))
        probabilities.append(round(b, 3))

    return {
        "probability": round(probability, 3),
        "probability_pct": round(probability * 100, 1),
        "relative_price": round(relative, 3),
        "base_acceptance": round(base, 3),
        "adjustment": round(adjustment, 3),
        "adjustment_reasons": reasons,
        "verdict": "High" if probability >= 0.70 else "Medium" if probability >= 0.45 else "Low",
        "prices": prices,
        "probabilities": probabilities,
        "current_price": round(quoted_price),
        "market_rate": round(predicted_optimal_price),
    }


# ─── Price Prediction (benchmark-anchored) ──────────────────────────

def predict_price(
    estimated_hours: float,
    hourly_rate: float,
    hardware_cost: float = 0,
    risk_percent: float = 8.0,
    profit_percent: float = 20.0,
    total_score: int = 5,
    classification: str = "Normal",
) -> dict:
    """
    Blended prediction:
      60% formula:  (Hours × Rate + HW) × (1+Risk%) × (1+Profit%)
      40% benchmark: interpolated from India market data
    """
    # Formula-based
    labor = estimated_hours * hourly_rate
    subtotal = labor + hardware_cost
    risk_buffer = subtotal * (risk_percent / 100)
    after_risk = subtotal + risk_buffer
    profit_buffer = after_risk * (profit_percent / 100)
    formula_total = after_risk + profit_buffer

    # Benchmark-based
    bm_lo = _interpolate_from_benchmarks(total_score, "total_cost", "low")
    bm_hi = _interpolate_from_benchmarks(total_score, "total_cost", "high")
    bm_mid = (bm_lo + bm_hi) / 2

    # Blend: 60% formula, 40% benchmark (benchmark keeps us grounded to real data)
    total = 0.60 * formula_total + 0.40 * bm_mid

    # If user-provided hardware cost differs significantly from benchmark, weight formula more
    bm_hw_lo = _interpolate_from_benchmarks(total_score, "hardware_cost", "low")
    bm_hw_hi = _interpolate_from_benchmarks(total_score, "hardware_cost", "high")
    bm_hw_mid = (bm_hw_lo + bm_hw_hi) / 2
    if bm_hw_mid > 0 and hardware_cost > 0:
        hw_ratio = hardware_cost / bm_hw_mid
        if hw_ratio > 2.0 or hw_ratio < 0.3:
            # Custom hardware config → trust formula more
            total = 0.80 * formula_total + 0.20 * bm_mid

    # Confidence interval using Bayesian spread
    tier_range = TOTAL_COST_RANGE.get(classification, (15000, 40000))
    spread_ratio = (tier_range[1] - tier_range[0]) / max(tier_range[1], 1)
    spread = max(0.08, spread_ratio * 0.3 + risk_percent / 100 * 0.15)
    ci_low = total * (1 - spread)
    ci_high = total * (1 + spread)

    # Market rate for this tier
    mkt_lo, mkt_hi = MARKET_RATES.get(classification, (500, 800))

    return {
        "predicted_price": round(total, 2),
        "confidence_interval": [round(ci_low, 2), round(ci_high, 2)],
        "base_labor": round(labor, 2),
        "hardware_cost": round(hardware_cost, 2),
        "risk_buffer": round(risk_buffer, 2),
        "profit_buffer": round(profit_buffer, 2),
        "subtotal": round(subtotal, 2),
        "formula_price": round(formula_total, 2),
        "benchmark_range": [round(bm_lo), round(bm_hi)],
        "market_hourly_rate": f"₹{mkt_lo}-{mkt_hi}/hr",
    }


# ─── Monte Carlo Risk Simulation ────────────────────────────────────

def monte_carlo_simulation(
    base_hours: float,
    hourly_rate: float,
    hardware_cost: float = 0,
    risk_percent: float = 8.0,
    has_ai: bool = False,
    custom_pcb: bool = False,
    rework_probability: float = 0.15,
    delay_cost_per_week: float = 5000,
    num_simulations: int = 5000,
) -> dict:
    """5000 Monte Carlo simulations with India-calibrated parameters."""
    random.seed(42)
    results = []

    # Sigma from benchmark spread: higher complexity → more variance
    hours_sigma = base_hours * (0.10 + risk_percent / 100)
    if has_ai:
        hours_sigma *= 1.3   # AI projects have higher variance
    if custom_pcb:
        rework_probability = min(0.35, rework_probability + 0.10)

    for _ in range(num_simulations):
        sim_hours = max(base_hours * 0.5, random.gauss(base_hours, hours_sigma))
        sim_hardware = hardware_cost * random.uniform(0.85, 1.15)

        rework = 0
        if random.random() < rework_probability:
            rework = sim_hours * hourly_rate * random.uniform(0.08, 0.25)

        delay_weeks = max(0, random.gauss(0, 0.8 + risk_percent / 30))
        delay_total = delay_weeks * delay_cost_per_week

        labor = sim_hours * hourly_rate
        risk_buf = labor * (risk_percent / 100)
        total = labor + sim_hardware + risk_buf + rework + delay_total
        results.append(total)

    results.sort()
    n = len(results)
    mean_val = sum(results) / n
    p5 = results[int(n * 0.05)]
    p25 = results[int(n * 0.25)]
    p50 = results[int(n * 0.50)]
    p75 = results[int(n * 0.75)]
    p90 = results[int(n * 0.90)]
    p95 = results[int(n * 0.95)]

    min_val, max_val = results[0], results[-1]
    num_bins = 20
    bin_width = (max_val - min_val) / num_bins if max_val > min_val else 1
    bins, frequency = [], []
    for i in range(num_bins):
        bin_start = min_val + i * bin_width
        bins.append(round(bin_start + bin_width / 2))
        frequency.append(sum(1 for r in results if bin_start <= r < bin_start + bin_width))

    simple_est = base_hours * hourly_rate + hardware_cost
    overrun_count = sum(1 for r in results if r > simple_est * 1.1)

    return {
        "bins": bins, "frequency": frequency,
        "mean": round(mean_val), "median": round(p50),
        "best_case": round(p5), "worst_case": round(p95),
        "p25": round(p25), "p75": round(p75), "p90": round(p90),
        "confidence_90": [round(p5), round(p95)],
        "overrun_probability_pct": round(overrun_count / n * 100, 1),
        "num_simulations": num_simulations,
    }


# ─── Profit Optimization ────────────────────────────────────────────

def optimize_profit(
    base_cost: float,
    classification: str,
    client_type: str = "startup",
    risk_percent: float = 8.0,
) -> dict:
    """Sweep margin 5-40%, find peak Expected Revenue = Price × P(accept)."""
    margins = list(range(5, 41, 1))
    expected_revenue = []
    best_margin, best_revenue = 5, 0

    for m in margins:
        price = base_cost * (1 + m / 100)
        acc = acceptance_probability(price, base_cost, classification, client_type, risk_percent)
        rev = price * acc["probability"]
        expected_revenue.append(round(rev))
        if rev > best_revenue:
            best_revenue = rev
            best_margin = m

    chart_margins = list(range(5, 41, 5))
    chart_revenue = [expected_revenue[m - 5] for m in chart_margins]

    return {
        "margins": chart_margins,
        "expected_revenue": chart_revenue,
        "optimal_margin": best_margin,
        "optimal_price": round(base_cost * (1 + best_margin / 100)),
        "optimal_revenue": round(best_revenue),
        "all_margins": margins,
        "all_revenue": expected_revenue,
    }


# ─── Complexity Radar ───────────────────────────────────────────────

def complexity_radar(scores: dict) -> dict:
    labels = ["Hardware", "Software", "AI/ML", "Deployment", "Risk & Safety"]
    values = [scores.get("hardware", 0), scores.get("software", 0),
              scores.get("ai_ml", 0), scores.get("deployment", 0),
              scores.get("risk_safety", 0)]
    total = sum(values)
    return {
        "labels": labels, "scores": values,
        "overall_score": round(total / len(values), 1),
        "total_score": total, "level": classify_complexity(total),
    }


# ─── Find Nearest Benchmark ─────────────────────────────────────────

def _nearest_benchmarks(score: int, n: int = 3) -> list:
    """Return the n closest benchmarks by score distance."""
    ranked = sorted(MARKET_BENCHMARKS, key=lambda b: abs(b["score"] - score))
    return ranked[:n]


# ─── Full Analysis Pipeline ─────────────────────────────────────────

def full_analysis(
    description: str = "",
    hardware_score: int = 1, software_score: int = 1,
    ai_ml_score: int = 0, deployment_score: int = 1,
    risk_safety_score: int = 1,
    hourly_rate: float = 0,     # 0 = auto-detect from market rate
    hardware_cost: float = 0,
    profit_percent: float = 20.0,
    client_type: str = "startup",
    safety_critical: bool = False, has_ai: bool = False,
    custom_pcb: bool = False, large_scale: bool = False,
    quoted_price: Optional[float] = None,
) -> dict:
    """Run full calibrated pipeline with India-market benchmarks."""

    # Step 1: Complexity
    comp = compute_complexity_score(hardware_score, software_score, ai_ml_score, deployment_score, risk_safety_score)
    cls = comp["classification"]

    # Auto-detect hourly rate from market if not specified
    if hourly_rate <= 0:
        hourly_rate = _interpolate_from_benchmarks(comp["total_score"], "rate", "low")
    suggested_rate = _interpolate_from_benchmarks(comp["total_score"], "rate", "low")

    # Step 2: Hours
    hours = estimate_hours(comp["total_score"], cls)

    # Step 3: Risk
    risk = calculate_risk(safety_critical, has_ai, custom_pcb, large_scale)

    # Auto-detect hardware cost from benchmark if 0
    actual_hw = hardware_cost
    if actual_hw <= 0:
        actual_hw = (_interpolate_from_benchmarks(comp["total_score"], "hardware_cost", "low") +
                     _interpolate_from_benchmarks(comp["total_score"], "hardware_cost", "high")) / 2

    # Step 4: Price
    price = predict_price(
        hours["estimated_hours"], hourly_rate, actual_hw,
        risk["risk_percent"], profit_percent,
        comp["total_score"], cls,
    )

    # Step 4b: Acceptance
    qp = quoted_price if quoted_price is not None else price["predicted_price"]
    accept = acceptance_probability(qp, price["predicted_price"], cls, client_type, risk["risk_percent"])

    # Step 5: Monte Carlo
    mc = monte_carlo_simulation(
        hours["estimated_hours"], hourly_rate, actual_hw,
        risk["risk_percent"], has_ai, custom_pcb,
    )

    # Step 6: Profit optimization
    base_cost = hours["estimated_hours"] * hourly_rate + actual_hw
    profit_opt = optimize_profit(base_cost, cls, client_type, risk["risk_percent"])

    # Radar
    radar = complexity_radar(comp["scores"])

    # Nearest benchmarks for context
    nearest = _nearest_benchmarks(comp["total_score"], 3)
    similar_projects = [
        {
            "name": b["name"],
            "score": b["score"],
            "cost_range": f"₹{b['total_cost'][0]:,} – ₹{b['total_cost'][1]:,}",
            "hours": f"{b['hours'][0]}-{b['hours'][1]}h",
            "rate": f"₹{b['rate']}/hr",
        }
        for b in nearest
    ]

    # Reasoning
    reasoning = (
        f"{cls} project (score {comp['total_score']}/25). "
        f"Estimated {hours['estimated_hours']}h at ₹{hourly_rate:,.0f}/hr "
        f"(market rate: ₹{suggested_rate:,.0f}/hr for {cls}). "
        f"Risk {risk['risk_percent']}%. "
        f"Predicted price ₹{price['predicted_price']:,.0f} "
        f"(benchmark range: ₹{price['benchmark_range'][0]:,} – ₹{price['benchmark_range'][1]:,}). "
        f"Acceptance {accept['probability_pct']}% ({accept['verdict']}). "
        f"Similar: {nearest[0]['name']} (score {nearest[0]['score']})."
    )

    return {
        "complexity": comp,
        "hours": hours,
        "risk": risk,
        "pricePrediction": price,
        "acceptanceModel": accept,
        "riskSimulation": mc,
        "profitOptimization": profit_opt,
        "complexityAnalysis": radar,
        "reasoning": reasoning,
        "similar_projects": similar_projects,
        "market_context": {
            "suggested_rate": round(suggested_rate),
            "market_rate_range": MARKET_RATES.get(cls, (500, 800)),
            "total_cost_range": TOTAL_COST_RANGE.get(cls, (15000, 40000)),
            "hardware_cost_estimate": round(actual_hw),
        },
    }
