"""Recompute every numerical answer in papers.py and check it against the stated value.
Run: python3 verify_papers.py   (exits with an error if any check fails)"""
import math
import sys

from papers import PAPERS, total_marks

H, C_, O, N = 1.008, 12.01, 16.00, 14.01
g, c_w = 9.81, 4.18
checks = []


def check(label, value, expected, tol=0.006):
    ok = abs(value - expected) <= tol * max(1, abs(expected))
    checks.append(ok)
    print(f"{'OK ' if ok else 'BAD'} {label}: computed {value:.6g}, stated {expected}")


# ---- 2026 Senior, Part A
check("S26 A1 solar kWh", 1.6 * 0.20 * 1000 * 4.5 / 1000, 1.44)
check("S26 A3 Betz", 16 / 27, 0.593)
check("S26 A4 wind", (9 / 6) ** 3, 3.375)
check("S26 A5 pH", (10 ** 0.1 - 1) * 100, 26, tol=0.02)
check("S26 A6 pyramid", 50000 * 0.1 ** 3, 50)
check("S26 A9 Carnot %", (1 - 303.15 / 453.15) * 100, 33, tol=0.01)
check("S26 A9 distractor C-scale", 30 / 180 * 100, 17, tol=0.02)
check("S26 A10 heat extracted", 14 - 14 / 3.5, 10)
# ---- 2026 Senior, Part B
gas_t = 108000 / 0.9 * 0.20 / 1000
hp_t = 108000 / 3.0 * 0.25 / 1000
check("S26 B1a gas t", gas_t, 24)
check("S26 B1b HP t", hp_t, 9.0)
check("S26 B1c reduction %", (gas_t - hp_t) / gas_t * 100, 62.5)
check("S26 B1d break-even", 24000 / 36000, 0.67)
M_oct = 8 * C_ + 18 * H
M_co2 = C_ + 2 * O
co2_oct = 1000 / M_oct * 8 * M_co2 / 1000
check("S26 B2b CO2 kg per kg octane", co2_oct, 3.08)
check("S26 B2c g/km", 0.060 * 0.74 * co2_oct * 1000, 137)
M_eth = 2 * C_ + 6 * H + O
co2_eth = 1000 / M_eth * 2 * M_co2 / 1000
check("S26 B2d ethanol kg/kg", co2_eth, 1.91)
check("S26 B2d octane g/MJ", co2_oct / 44.4 * 1000, 69, tol=0.01)
check("S26 B2d ethanol g/MJ", co2_eth / 26.8 * 1000, 71, tol=0.01)
check("S26 B3a Lincoln", 60 * 75 / 15, 300)
check("S26 B3c Chapman", 61 * 76 / 16 - 1, 288.75)
check("S26 B3d dN/dt", 0.4 * 300 * (1 - 300 / 500), 48)
check("S26 B3d max", 0.4 * 250 * 0.5, 50)
vol = 450 * 0.750 * 0.85
check("S26 B4a m3", vol, 287, tol=0.01)
check("S26 B4b %", vol / (600 * 2 * 6 * 190 / 1000) * 100, 21, tol=0.01)
check("S26 B4c kWh", vol * 1000 * g * 12 / 0.5 / 3.6e6, 18.8)
dF = 5.35 * math.log(420 / 280)
check("S26 B5a dF", dF, 2.17)
check("S26 B5a dT", 0.8 * dF, 1.7, tol=0.03)
check("S26 B5b 2xCO2", 0.8 * 5.35 * math.log(2), 3.0, tol=0.02)
check("S26 B5c ppm", 280 * math.exp(1.5 / 0.8 / 5.35), 398)

# ---- 2026 Junior
check("J26 A1 kWh", 52 * 5 * 365 / 1000, 94.9)
check("J26 A4 hawk", 100000 * 0.1 ** 4, 10)
check("J26 A8 kg", 2 * 1450 * 0.15, 435)
wasted = 12 * 60 * 18 / 1000
check("J26 B1a kWh/day", wasted, 12.96)
check("J26 B1b kWh/yr", wasted * 190, 2462.4)
check("J26 B1c EUR", wasted * 190 * 0.20, 492.48)
check("J26 B1d kg", wasted * 190 * 0.25, 615.6)
check("J26 B2a kg", 15 * 190, 2850)
check("J26 B2b compost", 2850 * 0.4, 1140)
check("J26 B2c CO2e", 2850 * 0.05 * 28, 3990)
check("J26 B3a kg", 8 * 190 * 0.120, 182.4)
check("J26 B3b kg", 30 * 8 * 190 * 0.120, 5472)
check("J26 B3c extra min", (8 / 15 - 8 / 30) * 60, 16)
check("J26 B4a r1", (339 - 317) / 20, 1.10)
check("J26 B4a r2", (370 - 339) / 20, 1.55)
check("J26 B4a r3", (414 - 370) / 20, 2.20)
check("J26 B4c 2030", 414 + 10 * 2.2, 436)

# ---- 2025 Senior
check("S25 A1 kWh in", 13.5 / 0.9, 15.0)
check("S25 A2 nm", 6.63e-34 * 3.00e8 / (1.12 * 1.60e-19) * 1e9, 1110)
check("S25 A6 MWh", 1.0e9 * g * 300 / 3.6e9, 818)
check("S25 A7 years", math.log(2) / math.log(1.07), 10.2, tol=0.01)
T = (1361 * 0.70 / (4 * 5.67e-8)) ** 0.25
check("S25 A8 K", T, 255)
check("S25 A8 C", T - 273.15, -18, tol=0.04)
check("S25 A9 kWh", 150 * c_w * 40 / 3600, 6.97)
check("S25 B1a break-even n", 0.40 / (0.17 - 0.03), 2.86)
check("S25 B1b per use", (0.40 + 20 * 0.03) / 20, 0.050)
check("S25 B1b saving %", (0.17 - 0.05) / 0.17 * 100, 71, tol=0.01)
p = 0.9
expected_uses = sum(k * p ** (k - 1) * (1 - p) for k in range(1, 2000))
check("S25 B1c E[uses] (series)", expected_uses, 10)
check("S25 B1c per use", (0.40 + 10 * 0.03) / 10, 0.070)
E = 50 * 8760 * 0.18
check("S25 B2a GWh", E / 1000, 78.8)
check("S25 B2b households", E * 1000 / 3500, 22500, tol=0.01)
check("S25 B2c t", E * 1000 * 0.95 / 1000, 74900)
check("S25 B3a BOD", (4 * 2 + 0.5 * 60) / 4.5, 8.4, tol=0.01)
check("S25 B3b DO", (4 * 9 + 0.5 * 2) / 4.5, 8.2, tol=0.01)
x = (37 - 5 * 4.5 - 8) / 0.5
check("S25 B3d max BOD", x, 13)
check("S25 B3d DO at limit", (4 * 9 + 0.5 * 2) / 4.5 - (4 * 2 + 0.5 * x) / 4.5, 5.0)
M_an = 2 * N + 4 * H + 3 * O
M_urea = C_ + O + 2 * N + 4 * H
check("S25 B4a %N AN", 2 * N / M_an * 100, 35.0)
check("S25 B4a %N urea", 2 * N / M_urea * 100, 46.7)
check("S25 B4b urea kg", 1800 / (2 * N / M_urea), 3858)
n2o = 18 * (2 * N + O) / (2 * N)
check("S25 B4c N2O kg", n2o, 28.3)
check("S25 B4c CO2e kg", n2o * 273, 7720)
check("S25 B5a static", 880 / 26, 33.8)
check("S25 B5b years", math.log(1 + 0.03 * 880 / 26) / 0.03, 23, tol=0.02)

# ---- 2025 Junior
check("J25 A1 kWh", 2.0 * 3 / 60, 0.1)
check("J25 A5 t", 0.4 * 540 - 0.3 * 600, 36)
check("J25 A6 L", 30 * 2 * 2700, 162000)
check("J25 A9 ha", 1.5 * 1.0 * 100, 150)
check("J25 B1a L", 8 * 12 - 5 * 8, 56)
check("J25 B1b L", 56 * 365, 20440)
check("J25 B1c kWh", 20440 * c_w * 25 / 3600, 593)
check("J25 B2a trees", math.ceil(7500 / 22), 341)
check("J25 B2b ha", 341 / 400, 0.85)
check("J25 B3b mean", sum([4, 7, 3, 0, 6, 5, 8, 2, 5, 10]) / 10, 5.0)
check("J25 B3c total", 5.0 * 2000, 10000)
check("J25 B4c EUR", 120 * (10.80 - 3.52), 873.60)

# ---- Structure: answers valid, marks totals
for pp in PAPERS:
    for i, q in enumerate(pp["part_a"]):
        ok = len(q["options"]) == 4 and q["answer"] in "ABCD"
        checks.append(ok)
        if not ok:
            print("BAD structure", pp["id"], i)
    print(f"{pp['id']}: total {total_marks(pp)} marks")

print(f"\n{sum(checks)}/{len(checks)} checks passed")
sys.exit(0 if all(checks) else 1)
