#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
# The arithmetic behind notes/estimates-audit-2.md (the ledger of estimates
# left in #321 charcoal and #322 wet pastel). Each block prints the number a
# ledger row proposes. Mie is the repository's own (dry_pigment_mie.py).
# Run: uv run notes/research/estimates_audit_2.py
import importlib.util, math, os

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("dry_pigment_mie_audit", os.path.join(here, "dry_pigment_mie.py"))
mie = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mie)


def ratio(n, nmed, d):
    """Transport scattering in a medium nmed over the same in air (sizeavg, sigma_ln 0.5)."""
    return mie.sizeavg(n, nmed, d)[0] / mie.sizeavg(n, 1.0, d)[0]


print("== W4. S(water)/S(air) by the size the table is computed at")
print("   (dry.rs scatter_in is tabled at d = 1 um; wet_pastel.rs uses 3 um; whiting's d32 is about 1.7 um)")
for n, name in ((1.50, "ultramarine"), (1.56, "Prussian blue / kaolin"), (1.59, "calcite (whiting), birefringence mean"), (1.65, "bone black"), (2.0, "lead white"), (2.4, "chrome yellow"), (3.0, "vermilion")):
    print(f"  n {n:4.2f} {name:38s} d1 {ratio(n, 1.333, 1.0):.3f}  d1.7 {ratio(n, 1.333, 1.7):.3f}  d3 {ratio(n, 1.333, 3.0):.3f}")

print("\n== Engine-wide fault 3. S(resin n 1.49)/S(air): the engine's fixative takes 0.2 for every particle")
for n in (1.50, 1.56, 1.59, 1.65, 1.74, 2.0, 2.4, 3.0):
    print(f"  n {n:4.2f}: d1 {ratio(n, 1.49, 1.0):.3f}  d1.7 {ratio(n, 1.49, 1.7):.3f}  d3 {ratio(n, 1.49, 3.0):.3f}")

print("\n== W3. Whiting's surface-weighted (Sauter) diameter")
# Blanc de Meudon / Champagne whiting (Art-Chimie spec sheet): d50 2.4-2.7 um,
# D97 13-15 um, 44-47 % under 2 um. Lognormal by volume: sigma from D97.
d50 = 2.55
for d97 in (13.0, 15.0):
    s = math.log(d97 / d50) / 1.881  # z(0.97) = 1.881
    d32 = d50 * math.exp(-s * s / 2)  # Sauter mean of a volume-lognormal
    print(f"  D97 {d97}: sigma_ln {s:.2f}, d32 {d32:.2f} um")
D_P, EPS = 1.7, 0.55

print("\n== W7. Porosity of a Sennelier stick (one listed stick, 9.07 g)")
for dmm, L in ((11.4, 67.3), (12.7, 63.5)):
    V = math.pi / 4 * (dmm / 10) ** 2 * (L / 10)
    rho = 9.07 / V
    print(f"  {dmm} x {L} mm: V {V:.2f} cm3, rho {rho:.2f} g/cm3, porosity {1 - rho / 2.65:.2f} (solids 2.65) .. {1 - rho / 2.9:.2f} (2.9)")

print("\n== W6. The studio: outdoor air warmed indoors (Paris-Montsouris, Infoclimat 1961-90 RH)")


def psat(t):
    return 611.21 * math.exp((18.678 - t / 234.5) * (t / (257.14 + t)))


for label, to, rh, ti in (("annual", 12.3, 0.76, 20.0), ("January", 5.0, 0.83, 18.0), ("July, unheated", 20.5, 0.68, 20.5)):
    print(f"  {label:15s}: outdoor {to} C RH {rh:.2f} -> indoor {ti} C RH {rh * psat(to) / psat(ti):.2f}")


def evap(ta, rh, hc=2.5):
    dv = 2.178e-5 * ((ta + 273.15) / 273.15) ** 1.81
    hm = hc / (1.204 * 1006) * (2.15e-5 / dv) ** (-2 / 3)
    MR = 0.018015 / 8.314462
    rho = lambda t: psat(t) * MR / (t + 273.15)
    air, hr = rh * rho(ta), 4 * 0.95 * 5.670374e-8 * (ta + 273.15) ** 3
    lo, hi = ta - 25, ta
    for _ in range(60):
        ts = (lo + hi) / 2
        if 2.454e6 * hm * (rho(ts) - air) > (hc + hr) * (ta - ts):
            hi = ts
        else:
            lo = ts
    return hm * (rho(ts) - air) * 1e3 * 60


for ta, rh in ((20, 0.5), (18, 0.35), (20.5, 0.68)):
    print(f"  evaporation at {ta} C, RH {rh}: {evap(ta, rh):.2f} um/min")

print("\n== W18. Natural convection, vertical sheet (Churchill-Chu), surface 3.7 K below the air")
for L in (0.3, 0.5):
    nu, a = 1.5e-5, 2.15e-5
    Ra = 9.81 / 293 * 3.7 * L ** 3 / (nu * a)
    Nu = (0.825 + 0.387 * Ra ** (1 / 6) / (1 + (0.492 / (nu / a)) ** (9 / 16)) ** (8 / 27)) ** 2
    print(f"  L {L} m: h {Nu * 0.0257 / L:.2f} W/m2K (ISO 6946: 2.5)")

print("\n== W2/W8. The wet tip: undrained strength by liquidity index (Wroth & Wood 1978)")
# Remoulded chalk: PL 0.244, LL 0.310 (Bialowas, Diambra & Nash 2016); kaolinite PL 0.35, LL 0.65.
for name, pl, ll in (("chalk", 0.244, 0.310), ("kaolin", 0.35, 0.65)):
    to_s = lambda w: w * 2.65 * (1 - EPS) / EPS  # water content (mass) -> saturation
    print(f"  {name}: PL at saturation {to_s(pl):.2f}, LL at {to_s(ll):.2f}")
    for S in (0.4, 0.5, 0.6, 0.7, 0.8, 1.0):
        w = S * EPS / (2.65 * (1 - EPS))
        li = (w - pl) / (ll - pl)
        if li < 0:
            print(f"    S {S:.1f}: w {w:.3f}, LI {li:5.2f}: below the plastic limit, brittle (the correlation doesn't apply; H stays the dry stick's or the drained bound below)")
            continue
        su = 170e3 * math.exp(-4.6 * li)
        print(f"    S {S:.1f}: w {w:.3f}, LI {li:5.2f}, s_u {su / 1e3:8.2f} kPa, H = 5.14 s_u {5.14 * su / 1e6:.4f} MPa")
print("  (PR: Schubert capillary state x Tabor 3 = 0.29 MPa at any saturation)")


def prandtl(phi):
    p = math.radians(phi)
    nq = math.exp(math.pi * math.tan(p)) * math.tan(math.pi / 4 + p / 2) ** 2
    return (nq - 1) / math.tan(p) * math.tan(p)


sig = 6 * (1 - EPS) / EPS * 0.050 / (D_P * 1e-6)
print(f"  drained bound: Schubert sigma_t {sig / 1e6:.3f} MPa (gamma 50 mN/m, d {D_P} um), x Nc tan(phi) {prandtl(29):.0f}-{prandtl(34):.0f} (phi 29-34 deg): {prandtl(29) * sig / 1e6:.1f}-{prandtl(34) * sig / 1e6:.1f} MPa")

print("\n== W9/W11. The tip's water: Washburn up the stick, and how far a dip wets it")
for d, g, eta, eps in ((3.0, 0.0728, 1.002e-3, 0.6), (D_P, 0.050, 1.3e-3, EPS)):
    r = 2 * eps * d * 1e-6 / (6 * (1 - eps))
    D = r * g / (2 * eta) * 1e6
    print(f"  d {d} gamma {g} eta {eta} eps {eps}: D {D:.1f} mm2/s; 1 mm dipped for 0.5 s wets {1 + math.sqrt(D * 0.5):.1f} mm")

print("\n== W12. Paste coverage thickness over a dry deposit's 6 um")
for d, eps in ((3.0, 0.6), (D_P, EPS)):
    print(f"  d {d} eps {eps}: {d / (1.5 * (1 - eps)) / 6:.2f}")

print("\n== W1. Water into the sheet")
cov = 160e-3 * 25e-3 / 0.16e-3
cal = cov * 6 / 0.5
print(f"  default sheet caliper {cal:.0f} um, its pores hold {0.5 * cal:.0f} um of water")
D_engine = 6e-6 * 0.0728 * 0.748 / (2 * 1.002e-3)
print(f"  engine (absorbent 0.8): D {D_engine * 1e6:.0f} mm2/s, {0.5 * math.sqrt(D_engine) * 1e6:.0f} um in the first second")
print(f"  engine, cos 1: D {6e-6 * 0.0728 / (2 * 1.002e-3) * 1e6:.0f} mm2/s; measured filter paper K 0.38 cm/s^0.5: D {0.38 ** 2 * 100:.1f} mm2/s")
for c60 in (20, 25, 40):
    print(f"  Cobb60 {c60} g/m2: {c60} um in a minute, D_eff (eps 0.5) {(c60e := c60 * 1e-6 / 0.5) ** 2 / 60 * 1e6:.2e} mm2/s")

print("\n== C2/C3. Vine charcoal: hardness and the coverage of what it lays")
for rho in (0.27, 0.30, 0.35):
    e = 1 - rho / 1.44
    print(f"  stick rho {rho}: porosity {e:.2f}; 3 um walls cover as {3 / (1 - e):.0f} um per stick volume (engine 6)")
print(f"  deposit coverage per force ~ (1/H)/t: was (1/4)/6; proposed (1/3)/14 -> x{(1 / 3 / 14) / (1 / 4 / 6):.2f}")

print("\n== C7/fault 2. Kneaded eraser vs the paper hold, with a capillary bridge at one asperity (radius a)")
A_e, A_c = 6.5e-20, 6.0e-20
D0 = 0.165e-9
W = math.sqrt(A_e * A_c) / (12 * math.pi * D0 ** 2)
Fr = math.sqrt(10e-9 * 150e-9)
sg = math.log(10) / 2
P = lambda x: 0.5 * (1 + math.erf(math.log(x) / (sg * math.sqrt(2))))
for R in (0.5, 1.5, 3.0, 5.0):
    Fe = 1.5 * math.pi * W * R * 1e-6
    row = [f"a {a}: {P(Fe / (Fr + 4 * math.pi * 0.072 * a * 1e-6)):.2f}" for a in (0.05, 0.1, 0.2, 0.5)]
    print(f"  R {R} um: eraser {Fe * 1e9:.0f} nN; taken, vdW only {P(Fe / Fr):.2f}; with a bridge " + ", ".join(row))

print("\n== C11. Fixative resin per area (Krylon Workable Fixatif: 5.25 % non-volatile, 11 oz covers 15-20 ft2)")
resin_g = 312 * 0.0525
for ft2 in (15, 20):
    t = resin_g / (ft2 * 0.0929) / 1.07  # PBMA ~1.07 g/cm3 -> um
    print(f"  one labelled coat over {ft2} ft2: {t:.1f} um of resin; at 50 % transfer {t / 2:.1f} um; a light third of it {t / 6:.1f} um")
for loose in (10, 20, 30):
    print(f"  1.5 um of resin into {loose} um of loose pastel (pores {EPS * loose:.1f} um): wets {1.5 / (EPS * loose):.2f}")

print("\n== C12. Gum arabic glass transition (Righetto & Netto 2005): where it reaches room temperature")
slope = (62 - 42.6) / (0.54 - 0.33)
print(f"  {slope:.0f} K per unit aw: Tg 25 C at aw {0.54 + (42.6 - 25) / slope:.2f}, 20 C at aw {0.54 + (42.6 - 20) / slope:.2f}")
