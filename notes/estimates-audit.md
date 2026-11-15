# Estimates audit: PRs #316–#320

This is a ledger of every constant that is still an estimate, or behaves like one, in five open PR branches. Each constant is classified, and a value is proposed where the physics or the literature supports one. Compiled 2026-11-15. No engine code was changed and nothing was built. Every number below comes from reading the branches' diffs and research notes, from arithmetic shown here, or from the sources cited.

| PR | branch | head read |
|---|---|---|
| #316 | `fix/pastel-pencil-sharpen` | 2a377889 |
| #317 | `feat/sanded-paper` | b7acc753 |
| #318 | `fix/dry-lake-color` | bd9bff01 |
| #319 | `feat/paper-mounts-presets` | afe88a20 |
| #320 | `feat/pastel-area-strokes` | 25e0ed9e |

`feat/charcoal` (#321) and `feat/wet-pastel` (#322) are not covered; they will be audited after their revision.

**Classes**
- **A** can be derived from first principles; the derivation is sketched.
- **B** can be set from a published measurement; the source is named.
- **C** we can measure ourselves from available data (museum images, datasheets, spectral databases, anthropometric tables).
- **D** needs a bench measurement; physical bounds are given, with where the value should sit inside them.

**Impact** is judged from the code: how much of the output depends on the constant. *Image*: it changes the pixels of every affected stroke. *Local*: it changes a few pixels or a narrow case. *Clock*: it changes only the painting's tally of hand time. *Check-only*: it is used in a research script's consistency check, not in the engine.

A file:line is the line on that PR's branch. "(main)" marks a constant that already exists on main but that the PR newly depends on or exposes.

## Summary

| PR | A | B | C | D | rows |
|---|---|---|---|---|---|
| #316 pencil sharpening | 2 | 4 | 1 | 0 | 7 |
| #317 sanded paper | 1 | 5 | 1 | 1 | 8 |
| #318 dry lakes | 1 | 8 | 5 | 0 | 14 |
| #319 mounts and presets | 1 | 6 | 3 | 2 | 12 |
| #320 area strokes | 2 | 5 | 5 | 0 | 12 |
| **total** | **7** | **28** | **15** | **3** | **53** |

Of the 53 rows, **23 propose a change**, 26 keep their value (already sourced or measured, now with bounds), and 4 leave a measurement to do (two C, two D).

Only three constants truly need a bench measurement:
- the compaction of a paste-filled painting linen (#319);
- the absorbency of Cassatt-type papers (#319);
- the wet level of a sanded paper's binder coat (#317).

Every other estimate can be set from physics, from published data, or from data we already hold.

The biggest corrections:
1. **The grit's wear on a stick** (`GRIT_WEAR`) drops from 4.5 to about 3.0. Measured grain angularity puts it there, not a cube corner.
2. **Laid-on pressure and the strainer's drum** (#319) were taken at ultrasonic and fresh-canvas values. A slower, quasi-static touch and a canvas that has relaxed on its strainer both make the support give more.
3. **The pastel pencil is 120 mm long** in the engine. Real ones are 175 mm, which matters once sharpening shortens them.

### Searches that found nothing usable
These are listed so the next pass doesn't repeat them:
- profilometry or pore volume of artists' sanded papers;
- whether UART's grades follow FEPA or CAMI;
- measured attack-angle distributions on SiC paper (Mulhearn & Samuels 1962 is the source, but it is paywalled);
- a minimum pencil length from ergonomics literature (only informal sources);
- a dry-powder L* in titanium datasheets (Kronos gives L* only in test coatings);
- ANSUR II index-finger length (ANSUR II has hand length; finger data come from other studies);
- quasi-static z-modulus of paper at a few kPa (Stenberg gives the board's initial modulus);
- 19th-century strainer bar widths for a 60 × 80 cm canvas;
- measured thickness or grammage of Cassatt's papers;
- mean pen azimuth (the values are in a patent table not reached);
- the fitted constants of Cao & Zhai's line-time power law (the paper was not reached; the constants quoted from memory are marked unverified).

---

## #316 Sharpening a pastel pencil

| # | constant | file:line | value | controls (impact) | class | replacement and source |
|---|---|---|---|---|---|---|
| S1 | a pencil's length | `crates/paint/src/pastel.rs:157` (main's value, now consumed by sharpening) | 120 mm | How much core there is to sharpen before `PENCIL_HOLD_MM` refuses: 70 mm of budget now. *Local, but it decides when a painting must take a new pencil.* | **B** | **175 mm.** Faber-Castell Pitt Pastel: 17.5 cm (Jerry's Artarama listings). Stabilo CarbOthello: 7.05 in ≈ 179 mm (Amazon single-pencil listing). With S2 the budget becomes 100 mm. |
| S2 | `PENCIL_HOLD_MM` | `crates/easel/src/draw_pencil.rs:113` | 50 mm | Below this, sharpening is refused. *Local.* | **C** | **75 mm**, from anthropometry (derivation below); bounds 45–95 mm. |
| S3 | `PENCIL_TAPER` | `crates/paint/src/pastel.rs:114` | 0.22 rad (12.6°) | How wide a fresh point's line is, and how much each sharpening costs: the cut scales as 1/tan τ. *Image, for pencil lines.* | **B** | **0.20 rad (11.6°).** Practitioners expose "a little over a centimetre" (Derwent, Martin Aveling) or half an inch (Emily Rose) of core. On a 4.4 mm core, exposed lengths of 10–12.7 mm give τ = atan(2.2/L) = 0.17–0.22. Taking 11 mm, "a little over" 1 cm, gives 0.20. |
| S4 | the pencil's core diameter (default `dia`) | `crates/easel/src/draw_pencil.rs:701` (main) | 4.5 mm | A pencil line's width and its taper geometry. *Image (small).* | **B** | **4.4 mm.** Stabilo lists the CarbOthello lead at 4.4 mm (stabilo.com). The Art Gear Guide's Pitt review measured 4.3 mm. The tribology note's own range is 4.3–4.7. |
| S5 | `SHARPEN_FLAT` | `crates/paint/src/pastel.rs:119` | 0.1745 rad (10°) | Which wear facets the blade leaves alone (side wear from `q:side`). *Local.* | **A** | **= `PENCIL_TAPER`.** The blade cuts planes at τ to the axis. A wear facet at φ > τ is blunter than the cut, so moving the point back by `sharpen_cut_mm` removes it. A facet at φ < τ lies more along the side than any cut: reaching it would take a cut of (h − d)/sin φ, which grows without bound as φ → 0 and runs past the exposed cone (r/tan τ ≈ 11 mm). The knife reshapes the cone and leaves the flat on the round side. The natural threshold is therefore the taper itself, not a separate 10°. |
| S6 | `PENCIL_BLUNT_MM` | `crates/paint/src/pastel.rs:116` | 0.15 mm up the axis (a flat of radius 0.034 mm) | A fresh point's first contact. The model's own wear crushes it within the first millimetre of a stroke. *Local, negligible.* | **A** | **0.26 mm** (0.23 mm if τ stays 0.22). A cut point crumbles until its contact pressure equals the core's hardness: r = √(F_min/(πH)). With H = 11.6 MPa (`Stick::mechanics(0.35)`) and the lightest touch, 0.1 N (pastel_stick_tribology.md §5), r = 0.052 mm. The blunt height is then r/tan τ. This also stays above the core's particle size (1–20 µm), so a blade can cut it. |
| S7 | `SHARPEN_SECS` | `crates/easel/src/draw_pencil.rs:117` | 10 s | The painting's hand-time tally. *Clock only.* | **B** | **20 s** (bounds 10–40 s), built up from MTM-1 predetermined motion times (1 TMU = 0.036 s): picking up and laying down the knife, about 40 TMU each way (≈ 3 s); about 16 cuts shaving the wood round, then 8 shaping the core, each a resisted 2–3 cm move plus a turn of the pencil (about 20 TMU ≈ 0.7 s, so ≈ 17 s); 4–5 strokes on sandpaper (≈ 2 s). That totals ≈ 22 s; round to 20. The cut counts follow Aveling's method (wood round, then the core). The only timing found (ten minutes per pencil, drawing-pencils.com) is a beginner's. |

**S2: the shortest pencil a hand still holds** [C, anthropometry]
- A tripod grip pinches the pencil at the pads of the thumb, index and middle fingers, 10–20 mm back from a pastel pencil's point (it is held close for control). The shaft then rests on the web between thumb and index finger.
- The distance from the index fingertip's pad to that web is the index finger's length less about 10 mm for the pad. Index-finger length is 79.3 ± 2.7 mm in women and 86.6 ± 3.4 mm in men (training-data means quoted on ResearchGate, fig. 2 of publication 5798067). A hand-surgery series gives 8.7 ± 0.5 cm and 9.5 ± 0.5 cm (PMC12309929; it measures from a different landmark).
- So a grip resting on the web needs about 15 + (70 to 77) ≈ 85–92 mm of pencil.
- Without the web, a stub can be pinched by the pads alone: the point's 15 mm plus about 25–30 mm of pad contact gives 40–45 mm. That is the absolute floor.
- Informal sources put the extender or discard point at 65–80 mm overall, and 5–6 cm of usable shaft (Quora answer; AliExpress article).
- **Take 75 mm.** At that length a pencil can still just reach the web for a small hand: the 5th-percentile woman's index finger is about 75 mm.
- ANSUR 1988 (Gordon et al. 1989) has the digit lengths needed to make this a percentile choice. A builder should check the exact figures there.

---

## #317 Sanded paper

| # | constant | file:line | value | controls (impact) | class | replacement and source |
|---|---|---|---|---|---|---|
| G1 | `GRIT_WEAR` | `crates/paint/src/paper.rs:130` | 4.5 | It multiplies the stick's wear wherever grit touches above the fill. So it sets how much each stroke lays and how fast the tooth fills. *Image: every stroke on grit, roughly linear.* | **B** | **3.0** (bounds 2.3–3.7). Derivation below. |
| G2 | the grade's micron reading (`grit=true` and default `size`) | `crates/easel/src/api.rs:2607`, `:2610` | 35 µm (P400 read as FEPA) | The tooth scales with grain size, and every grade a painter names goes through this reading. *Image: tooth ±37 %.* | **C** | **Keep 35 µm (FEPA), with the reason recorded.** UART is made in Germany at 300 g/m² (Dakota Art Pastels), and European coated abrasives are graded on FEPA's P scale. The missing "P" is the US retailers' naming, so it is not evidence for CAMI. A CAMI reading would give 22–23 µm and a 37 % smaller tooth. The datasheet check below (G4) is consistent with a FEPA-sized coat. The way to settle it is a micrograph of a UART or Pastel Premier surface at a known scale (C); none was found published. |
| G3 | `GRIT_FACE` | `crates/paint/src/paper.rs:111` | 0.02 | The level the stick rests at, and so the tooth's depth. At P400 in acrylic: face 1 % → 24.4 µm, 2 % → 21.0, 5 % → 16.4. *Image: tooth ±16 %.* | **A** | **0.01** as a constant, or better F/(H·A₀) per stroke. The real-contact share is the force over the hardness and the apparent face. The default soft stick (`soft` 0.75) has H = 30^0.25 · 2^0.75 = 3.9 MPa; its default force is 0.45 × `FORCE_AT_FULL` = 2.25 N. A₀ runs from a fresh crescent (20–50 mm², tribology §4) to a fully worn facet (148 mm², the #319 reference patch): F/(H·A₀) = 2.9 %, 1.1 % and 0.39 %. A stick wears flat at once (tribology §4), so the geometric middle, about 1 %, is the typical value. The engine already knows F, H and the contact area at every step, so computing this per stroke removes the constant entirely. |
| G4 | the wet binder's level (= the median grain's top) | `crates/paint/src/paper.rs:187` (`let binder = solids * (d50 - at(d50))`) | level with d50 | How much of the coat between the grains the binder fills. A wet coat 1.3 d50 deep gives 16.6 µm against 21.0. *Image: tooth −20 % at worst.* | **D** | **Keep d50, the leanest coat that carries its grains; bounds d50–1.3 d50.** One measured constraint exists [C]. Colourfix is 340 g/m² coated on a 300 g/m² base (Jerry's Artarama; Talas), so its coat weighs 40 g/m². The model's coat at a cover of 0.6 holds grains of 0.6 · (2/3) · E[d³]/E[d²] = 13.6 µm³/µm² at P400 (E[d³]/E[d²] = 0.85 d50 · e^(2.5σ²) = 33.9 µm), plus about 11 µm of dry binder. That is 48 g/m² with quartz or marble grit (2.65 g/cm³) and 65 g/m² with alumina. Since the coat weight scales with d, 40 g/m² means a quartz coat of d50 ≈ 29 µm (between P500 and P600) at the model's binder level, or a thinner binder at P400. That bounds how lean the coat can be, but it cannot separate grain size from binder level. A cross-section micrograph would. |
| G5 | `ACRYLIC_SOLIDS` | `crates/paint/src/paper.rs:106` | 0.45 | The binder's dry share. *Image: 0.35 → 23.2 µm, 0.55 → 18.8 µm.* | **B** | Keep. Rhoplex AC-33: 46–47 % solids by weight at 1.04 g/cm³ (MFA CAMEO). |
| G6 | `GLUE_SOLIDS` | `crates/paint/src/paper.rs:107` | 0.07 | The same, for a glue binder. *Small: under 4 % over 0.05–0.10.* | **B** | Keep. A glue size is mixed 1:10–1:20 by weight (Natural Pigments). |
| G7 | `GRIT_SPREAD` | `crates/paint/src/paper.rs:100` | 0.23 | The coarse tail the stick rests on. *Image: σ 0.20 → 19.5 µm, 0.27 → 23.2 µm.* | **B** | Keep. A lognormal fit to the FEPA 43-2 ds3/ds50/ds94 limits at P400 and P500 gives 0.21–0.28. |
| G8 | default `cover` | `crates/easel/src/api.rs:2607`, `:2610` | 0.6 | The tooth, weakly: 0.3 → 21.4 µm, 0.85 → 19.5 µm. *Small.* | **B** | Keep. Random sequential adsorption jams at 0.547 (Feder 1980), and coated-abrasive coat weights give 0.69 (US 5,417,726); 0.6 lies between them. |

**G1: the wear ratio from measured grain angularity** [B]
- The PR's 4.5 assumes a crushed grain cuts with a cube's corner: an attack angle of 45°, K = 0.64. That is an estimate.
- Measured angularity is available. Hamblin & Stachowiak's spike parameter SPQ is the mean of cos(θ/2) over a particle's protruding corners, θ being the corner's apex angle. For abrasives of 0.25–0.3 mm (glass, silica sand, garnet, quartz, alumina, SiC) it runs from 0.023 to 0.60, with SiC and alumina at the angular end (Stachowiak, *Wear* 241 (2000) 214, as quoted in *Proc. Estonian Acad. Sci. Eng.* 7 (2001) 22–34). For reference, a square has SPQ 0.707 and an equilateral triangle 0.866 (same paper, table 3). Freshly fractured WC-Co powder measures 0.58–0.65.
- **Why this measurement fits pastel.** Hamblin & Stachowiak chose **chalk** as the worn body because it gives pure two-body abrasion, and found its wear rate nearly linear in SPQ (*Tribol. Trans.* 39 (1996) 803–810, as cited in *Wear* (2001) S0043164801005579). Chalk is the closest measured proxy for a pastel compact anywhere in the tribology literature. It confirms that wear here scales with the corners' slope, as Rabinowicz's model assumes.
- **The arithmetic.** An apex of half-angle θ/2 attacks at 90° − θ/2:
  - SPQ 0.50 gives 30.0°, K = (2/π) tan = 0.37;
  - SPQ 0.55 gives 33.4°, K = 0.42;
  - SPQ 0.60 gives 36.9°, K = 0.48.
- Over the PR's fiber-crossing K of 0.13–0.16 (its middle is 0.145), the ratio is 2.3–3.7. **At SPQ 0.55 and the middle fiber value it is 2.9; take 3.0.**
- The PR's test band (2.3–5.1) still contains 3.0, but the test's model result (4.6) will drop to about 3.
- **To make it fully measured,** read the per-abrasive SPQ table and the chalk wear rates in the 1996 *Tribology Transactions* paper. Its glass-bead (rounded) and SiC (angular) wear rates against chalk would give a measured angular-to-rounded ratio that can check the fiber side of the derivation too.

---

## #318 Dry lakes

| # | constant | file:line | value | controls (impact) | class | replacement and source |
|---|---|---|---|---|---|---|
| L1 | magenta's `dye_loading` (yellow lake's, as an estimate) | `crates/paint/src/dry.rs:110` | 12.2 | Pure dry magenta: 175 50 134 now, with no measured target. *Image, for every magenta pastel, pulp or tint.* | **B** | **Fit a so that the pure lake's dry K/S at 545 nm is 7** (bounds 4.8–11.2). Derivation below. |
| L2 | rose madder's loading | `crates/paint/src/dry.rs:108` | 35.7 | Pure and tinted dry madder. *Image.* | **C** | Keep: it is fitted to the CHSOS/Cosentino powder and agrees with dye chemistry (1–9 wt % alizarin). Bounds 31.5–40.8 over the correction's black and white anchors. |
| L3 | carmine's loading | `crates/paint/src/dry.rs:109` | 3.01 | Dry carmine. *Image.* | **C** | Keep (bounds 1.9–4.1). The remaining ΔE of 9.9 is the oil K's spectral shape, not the loading. |
| L4 | yellow lake's loading | `crates/paint/src/dry.rs:110` | 12.2 | Dry yellow lake. *Image.* | **C** | Keep (bounds 10.6–14.0). |
| L5 | `BLACK_TRUE` | `notes/research/dry_lake_fit.py:59` | 0.04 (0.03–0.05) | The powder correction's floor, and so every fitted loading. *Indirect: madder's L\* ±1.8.* | **B** | Keep. A carbon black powder's total reflectance is 3–5 % (SPIE *Photonics Focus*, 2026). |
| L6 | `TITANIUM_TRUE` | `notes/research/dry_lake_fit.py:60` | 0.945 (0.90–0.99) | The correction's gain. *Indirect.* | **B** | Keep. Corroborated by Kronos's rutile grades in test coatings, L\* 97–98, Y ≈ 0.92–0.95 (Kronos List of Grades, Oct 2026). No datasheet gives a dry-powder L\*. |
| L7 | `LAKE_SUBSTRATE_INDEX` | `crates/paint/src/dry.rs:90` | 1.57 | A lake's dry scattering, at the Mie ratio for that index. *Image.* | **B** | Keep (gibbsite). |
| L8 | `measured_index`: PV19 2.03, green earth 1.62, verdigris 1.545, lead-tin yellow 2.30, goethite 2.35 | `crates/paint/src/dry.rs:124–128` | as listed | Their dry scattering. *Image.* | **B** | Keep (CAMEO, Natural Pigments, SSHADE, Gettens & Stout). |
| L9 | Mars yellow's index, left at 2.2 | main's `dry::refractive_index`; listed as left alone in dry_pigment_optics.md §6.4 | 2.2 | Dry Mars yellow. *Image (small).* | **B** | **2.35**, added to `measured_index` behind the same switch. It is synthetic goethite, the same mineral as transparent oxide yellow (SSHADE; α 2.26, β 2.39, γ 2.40). The PR itself calls 2.2 "7 % low". |
| L10 | Rinmann's green, at the 1.9 fallback | main's `dry::refractive_index` fallback | 1.9 | Dry Rinmann's green. *Image (small).* | **B** | **2.0**, behind the same switch. It is a cobalt-doped ZnO host, and zincite's index is 2.00–2.02 (CAMEO "Zinc oxide"; Gettens & Stout). |
| L11 | green earth's and verdigris's K per volume dry (the oil-table K, used unloaded) | §6.4 of dry_pigment_optics.md (no constant yet) | a = 1 implicitly | Dry they come out 34 and 59 ΔE from their own powders, 30–50 L\* too light. *Image.* | **C** | **Fit a loading to each, exactly as for the lakes**, with dry_lake_fit.py's `fit()` and the PR's corrected CHSOS powders as targets: green earth 56.1 / −1.9 / 11.3, verdigris 33.6 / −27.2 / −13.6. Both powders are already in the PR's corrected set. Grain size (1–30 µm) is the other half: the size-aware S the note proposes is A (table 2.2's σ′ against d). |
| L12 | `PACKING` | `notes/research/dry_lake_fit.py:248` | 0.5–1 | The dye-chemistry check only. *Check-only.* | **A** | Percus–Yevick hard-sphere structure factor at a loose powder's volume fraction of 0.4–0.55, integrated over the Mie phase function at x = π d n/λ ≈ 9. This dependent-scattering reduction can be computed rather than bracketed; expect 0.6–0.9. |
| L13 | ε of alizarin–Al, lower end | `notes/research/dry_lake_fit.py:250–253` | 5×10³ L mol⁻¹ cm⁻¹ | The check only. *Check-only.* | **B** | Keep the bracket. The upper value (alizarin red S–Al, 1.70×10⁴ at 510 nm) is measured. A measured ε of the alizarin–Al lake chelate itself would close it; it was not searched further. |
| L14 | `D_UM` (a lake's grain size) | `notes/research/dry_lake_fit.py:246` | 1 µm | The package effect in the check. *Check-only.* | **C** | Keep. SEM of madder and cochineal lakes in Kirby, Spring & Higgitt (*NG Tech. Bull.* 26, 28) shows aggregates of sub-µm particles, which a builder can read off those plates. |

**L1: a magenta loading from dye chemistry** [B]
- The tube is "fuchsine (aniline) lake on alumina" (`palette.rs:593`). Its oil K is a proxy built from a catalog masstone.
- Basic fuchsin has ε = 8.06×10⁴ L mol⁻¹ cm⁻¹ at 543 nm (PhotochemCAD L04, in PBS). HiMedia's specific absorbance, converted, gives 7.97–9.16×10⁴. The molar mass is 337.8 g/mol.
- Run through dry_lake_fit.py's own `ks_dye` (μ_a = ln 10 · ε · w ρ/M; the package effect for 1 µm grains; S of the n = 1.57 substrate at 0.71 µm⁻¹; packing 0.5–1; ρ 2.0–2.4 g/cm³), K/S at 545 nm is:

  | dye content | 1 wt % | 3 wt % | 5 wt % | 10 wt % | 20 wt % |
  |---|---|---|---|---|---|
  | K/S | 2.8–6.8 | 4.8–10.2 | 5.3–10.9 | 5.5–11.2 | 5.6–11.2 |

- Fuchsine's absorptivity is so high that above about 3 wt % the package effect saturates the result. So K/S at the band hardly depends on the unknown dye content: 5–11 for any normal lake.
- **To implement:** dump the engine's dry K and S for magenta (the PR's `dump_dry_lake_fit_input`), then set a = 7 / (K/S at 545 nm with a = 1). This replaces "yellow lake's loading" with a number set by the dye.

---

## #319 Mounts and named papers

| # | constant | file:line | value | controls (impact) | class | replacement and source |
|---|---|---|---|---|---|---|
| M1 | the cloth's compaction law (`CLOTH_COMPACTION_EXP`) | `crates/paint/src/paper.rs:217` | B = 0.0764 (dry flax) | The give of canvas, and of a strainer over its bars: 0.00055 MPa/µm, the cloth dominating the series. *Image, for every stroke on a canvas or strainer mount.* | **D** | **Keep 0.0764 (k = 0.00055 MPa/µm) until a bench test; it is the soft bound.** The stiff bound is a weave fully filled with dried paste and size, which compacts like paperboard: E_z ≥ 17 MPa (the lowest whole-board value, M6) over 0.4 mm, so k ≤ 0.04 MPa/µm. A thin paste layer leaves most of the weave's interstices open, so the true value should sit near the soft end, within a factor of a few of dry flax. The only data are dry-flax composite preforms; the paste-filled weave needs an indentation test (see below). |
| M2 | the reference patch (`REF_STICK_MM` 6, `REF_ALTITUDE_DEG` 50; the full worn facet) | `crates/paint/src/paper.rs:185`, `:188` | a = 6.86 mm, 148 mm² | The give of board and drum. The drum's give goes as about 1/(a² h(β)), so a 50 mm² fresh face would make it about 2.5× firmer. *Image, for strainer and board.* | **A** | **Compute the patch per stroke from the stick's actual contact**, which the engine already has. As a constant, keep the worn facet (tribology §4: a stick wears flat at once). The altitude of 50° is measured for a pen (Schomaker & Plamondon 1990). Note that #320's `HAND` holds the stick at 60° (R3), so the same hand has two altitudes across the two PRs; both should be 50. |
| M3 | `PAPER_SPECIFIC_MODULUS` | `crates/paint/src/paper.rs:207` | 5070/700 = 7.24 MN·m/kg | The sheet's bending stiffness D, and so the bending length ℓ = √(D/T) and the drum's give. *Image, for strainer.* | **B** | **5.6 MN·m/kg**, i.e. 7.24 divided by 1.3. E₁₁ and E₂₂ come from Mann, Baum & Habeger's **ultrasonic** measurements. Paper's ultrasonic modulus is 25–40 % above the mechanical one, from viscoelasticity and time scale (IPST review, Georgia Tech repository; Habeger's theory). A stroke loads the sheet over tens of ms, so the quasi-static value applies. Then D = 6.7 N·mm for the drawing sheet (8.7 before) and ℓ = 5.8 mm. A generic tensile stiffness index of 4–7 kN·m/g for printing papers is consistent with this (unverified secondary figure). |
| M4 | `CANVAS_TENSION_N_PER_MM` | `crates/paint/src/paper.rs:210` | 0.2 | The drum: the membrane part goes as T. *Image, for strainer.* | **B** | **0.13 N/mm.** A canvas loses 30–50 % of its tension in the first 48 h (Berger & Russell, JAIC 29(1), 1990). A pastel is worked days after the sheet is tacked, so 0.2 × (1 − 0.35) ≈ 0.13 applies. That lies inside the measured working band of paintings, 0.12–0.24 kN/m (*Heritage Science* 2022). |
| M5 | `BOARD_MM` | `crates/paint/src/paper.rs:222` | 3 mm | Board's give: 1.5 mm → 0.026, 3 mm → 0.014 MPa/µm. *Image, for board.* | **C** | **2.3 mm.** Cassatt's board mounts are "illustration board" (Met 10424) and "cardboard" (Met 10404). A heavyweight illustration board (Crescent No. 100, 24-ply) is 0.09 in = 2.3 mm; a medium one (No. 300) is 1.4 mm (Blick, Binders, United Now). Board's give rises to about 0.018 MPa/µm. Degas's 5–7 mm boards are a separate case. |
| M6 | `BOARD_EZ_MPA` | `crates/paint/src/paper.rs:223` | 39 MPa | Board's Winkler spring E_z/t. *Image, for board.* | **B** | **34 MPa.** Stenberg's quasi-static through-thickness fit for paperboard has E_initial = 34 MPa (*Int. J. Solids Struct.* 2003; used again as E33 = 35 MPa by Xia, Boyce & Parks). The 39 MPa is the ultrasonic reading. Whole-board values run as low as 17 MPa (Persson, quoted in the KTH thesis diva2:1738574), which is a lower bound. |
| M7 | `BOARD_GXZ_MPA` | `crates/paint/src/paper.rs:224` | 50 MPa | Board's spreading length L = t√(G/3E). *Small.* | **B** | **32 MPa**: G_initial from the same Stenberg (2003) fit, so that E and G come from one board. It lies inside Nygårds's 30–85 MPa. |
| M8 | `CLOTH_MM` | `crates/paint/src/paper.rs:212` | 0.4 mm | The cloth's spring, k ∝ 1/t. *Image, for canvas.* | **B** | Keep; painting canvas is 0.3–0.6 mm. |
| M9 | `STRAINER_BAR_MM` | `crates/paint/src/paper.rs:175` | 40 mm | The band near the bars that is as firm as canvas. *Local (edges).* | **B** | **50 mm.** Measured original rectangular strainers of about 60 × 50 cm paintings have bars 4–6 cm wide, and a presumed original French strainer 6.2 cm (Jens Juel strainers study, ResearchGate 363090756). Vermeer's are narrower (2.1–2.7 cm, RKD) but two centuries earlier. A 60 × 80 cm sheet is a No. 25 *paysage* (81 × 60 cm). |
| M10 | preset dials: wove 130 g/m², fiber 1.6 mm, felt 0.7 mm/14 µm, calender 0.25; brown wove; cream laid | `crates/paint/src/paper.rs:357–384` | as listed | Each named sheet's texture and tooth. *Image, when a preset is used.* | **C** | **No change yet; a lead to follow.** Sarah Bertalan, "Cassatt's Paper: Finding the Right Sheet", in *Mary Cassatt: Prints and Drawings from the Collection of Ambroise Vollard* (Adelson / Marc Rosen, 2008), is the cited technical description of her papers (via Dirda, BPG Annual 35, 2016). Shelley (1989) describes *Woman on a Bench* as "green laminated paperboard" (BPG Annual 16), so the green preset may want a board, not a 130 g/m² sheet. The felt, laid and texture dials can be measured from raking-light museum images at a known scale (the same method as #320's). Japan paper's dials are already B (CAMEO; Melbourne fibre atlas). |
| M11 | preset tones that are estimates (blue, gray-blue, buff, brown, cream laid, japan as made) | `crates/paint/src/paper.rs:376–386`; cassatt_papers.md §2 | fitted to estimated targets | Each named sheet's color. *Image.* | **C** | **Measure bare reserves** with the same median-patch method the PR used for tan and green, on the Met/AIC/NGA open-access images of sheets catalogued as blue or blue-gray (the AIC's 1922.421 and 1968.81 are faded; look for an unfaded edge under a former mat line). Until then they stay estimates. |
| M12 | presets keep drawing paper's absorbency (0.8) | `crates/paint/src/paper.rs` (`..Paper::drawing`) | 0.8 | Oil and water uptake on a named sheet. *Local.* | **D** | Keep. A Cobb test (ISO 535) on period-type papers would set it; nothing published was found for these sheets. Bounds: from a hard-sized sheet to a waterleaf one; Cobb values for these were not searched, so the dial's 0–1 range is the only bound given here. |

**M1: the bench test that would settle the cloth.** Paste a 300 µm drawing sheet onto glue-sized linen with wheat starch paste, let it dry, and press a flat 13.7 mm indenter (the reference patch's diameter) at 2.5 N on a hard table. The sink (expect 10–40 µm) gives k directly, and the same rig on board (M5–M7) would check the derivation. This is the single most useful measurement on the list.

---

## #320 Strokes over an area

| # | constant | file:line | value | controls (impact) | class | replacement and source |
|---|---|---|---|---|---|---|
| R1 | a stick's plain `p:hatch` defaults: spacing 1.5 mm, length 12 mm | `crates/easel/src/draw_pencil.rs:325`, `:327` | 1.5 / 12 mm | The default look of every stick hatching: lines 1.5 mm apart under a 12 mm soft stick overlap about 8×. *Image, large.* | **C** | **spacing 8 mm, length 50 mm.** The PR's own measurements of Cassatt's open passages: distinct strokes 5–10 mm apart (Margot, 1902) and 10–20 mm (Kelekian, 1908); strokes 30–60 and 40–80 mm long. The PR keeps the pencil's defaults on purpose, so this is the lead's call. Physically, a pencil-scale default under a stick is not either measurement. |
| R2 | `HAND.speed` (and its use in `area_hatch`) | `crates/easel/src/draw_pencil.rs:225` (main's 80, now a default) | 80 mm/s | How long the land and lift ramps are (`LAND_S` × v = 4 mm, `LIFT_S` × v = 3.2 mm), so a short mark's ends, plus hand time. *Image, at ends.* | **B** | **v = 80 · (L / 12 mm)^0.53 mm/s**, which is 170 mm/s for a 50 mm slash. A 12 mm mark at 80 mm/s takes 150 ms, the measured duration of a single stroke (100–150 ms, JFDE review of handwriting timing). Longer marks are drawn faster but not in the same time: isochrony is only partial (Viviani & McCollum, *Neuroscience* 10 (1983) 211). Cao & Zhai (CHI 2007) fit straight-line drawing time as T = m·Lⁿ, longer lines faster. **n = 0.47 is quoted from memory and must be checked in the paper (doi 10.1145/1240624.1240850) before use.** A zigzag's legs (about 10.8 mm) at 150 ms give 72 mm/s along the path, so 80 stays right for zigzags. |
| R3 | `HAND.alt` | `crates/easel/src/draw_pencil.rs:225` | 60° | The facet the stroke wears and its contact. *Image.* | **B** | **50°**: the measured pen altitude (Schomaker & Plamondon 1990), already #319's reference altitude. |
| R4 | `HAND.azimuth` | `crates/easel/src/draw_pencil.rs:225` | 45° | Which edge leads. *Image.* | **B** | **Keep 45° pending the table.** Measured right-hand azimuth means, minima, maxima and SDs for five writers on a Wacom Intuos at 100 Hz are in US 8,090,203 (and siblings 7,894,671 / 7,630,553), table 2; the thesis at kochi-tech.ac.jp also has the distribution. The table was not reached. |
| R5 | `ZIGZAG_ROUND` | `crates/easel/src/draw_pencil.rs:250` | 0.4 | The corners' shape. *Local: invisible at these sizes.* | **A** | **1.0, a sine.** A continuous back-and-forth is a hand oscillating across the run while drifting along it, which Hollerbach's oscillation model of handwriting describes as near-sinusoidal. At the defaults (swing 5 mm, period 8 mm) a sine's turning radius at its peaks is P²/(4π²A) = 0.32 mm, far under the stick's 1.5–3 mm line. So the turns already look sharp, as the "ladder" does in the photographs, with no extra dial. |
| R6 | zigzag swing 5 mm, period 8 mm, run 40 mm | `crates/easel/src/draw_pencil.rs:246`, `:248`, `:252` | as listed | The zigzag passage. *Image.* | **C** | Keep (measured on *Nurse Reading*, 1895). |
| R7 | `JITTER_LENGTH` 0.3, `JITTER_ANGLE` 0.17 | `crates/easel/src/draw_pencil.rs:254–255` | ±30 %, ±10° | The spread within a passage. *Image.* | **C** | Keep. They come from the spread of lengths and angles within single passages (cassatt_pastel_strokes.md §2–3). |
| R8 | a mark's bow, `rng.range(-0.06, 0.06) * (b - a)` | `crates/paint/src/area_strokes.rs:379` (the same as main's graphite hatching) | random ±6 % of the length | Each mark's curve. *Image (small).* | **A** | **A fixed-sign arc of sagitta L²/(8R)**, i.e. a bow of L/(8R) of the length, concave toward the pivot (lower right for a right hand). A stroke swung about the wrist is an arc of radius R = hand length = 189 mm (ANSUR II, men and women combined). That gives 0.8 % at 12 mm, 4 % at 60 mm and 5.6 % at 80 mm. Strokes longer than the wrist's range swing from the elbow, R about 450 mm (forearm plus hand), giving about 2 %. The same pivot explains the fan the PR measured (steeper at the left, flatter at upper right), so a pivot-driven bow and angle would replace two random draws with one measured length. |
| R9 | mark ends `(-0.08..0.1)`, pressure `(0.85..1.12)`, profile `[0.8, 1, 0.8, 0.25]` | `crates/paint/src/area_strokes.rs:374`, `:392`, `:394` (copied from main's `hatch_marks_graded`) | as listed | Variation among marks, and each mark's force profile. *Image (moderate).* | **C** | **Keep pending measurement.** The pressure profile and its stroke-to-stroke spread are measurable from public pen-force recordings (Schomaker's pen-force study, ai.rug.nl; any signature dataset with pressure channels). The landing rise is already `LAND_S` / `LIFT_S`. |
| R10 | `FORCE_AT_FULL` × default pressure 0.45 | `crates/easel/src/draw_pencil.rs:46` (main), `:328` | 2.25 N | The stroke's force. *Image.* | **B** | Keep: inside the measured 2–3 N for drawing (Xin, Bi & Ren 2012). |
| R11 | default angle −0.9 rad | `crates/paint/src/area_strokes.rs:434`; `crates/easel/src/draw_pencil.rs` (`Direction::Fixed(-0.9)`) | 51.6° rising right | Default direction. *Image.* | **C** | Keep: Cassatt's backgrounds measure 40–65° (median about 51°). |
| R12 | Jobard–Lefer d_test = 0.5 d_sep | `crates/paint/src/area_strokes.rs:298` | 0.5 | Streamline density. *Algorithmic.* | **B** | Keep: Jobard & Lefer (1997) recommend d_test = 0.5 d_sep. |

---

## Ranked by impact

These are the ten that move the most output and have a replacement ready:

| rank | id | constant | now → proposed | why it matters |
|---|---|---|---|---|
| 1 | G1 | `GRIT_WEAR` | 4.5 → **3.0** | Every stroke on grit: wear, laid volume and fill rate scale linearly. |
| 2 | R1 | stick hatch spacing, length | 1.5 / 12 → **8 / 50 mm** | The default look of every stick hatching. |
| 3 | L1 | magenta's loading | 12.2 (yellow lake's) → **K/S 7 at 545 nm** | Every dry magenta; the only lake with no target. |
| 4 | M4 | canvas tension | 0.2 → **0.13 N/mm** | The strainer drum's give. |
| 5 | M3 | specific modulus | 7.24 → **5.6 MN·m/kg** | The strainer drum, through D and ℓ. |
| 6 | G3 | `GRIT_FACE` | 0.02 → **0.01** (or per stroke) | The grit's tooth: about +16 %. |
| 7 | M5, M6 | board thickness, E_z | 3 mm, 39 → **2.3 mm, 34 MPa** | Board's give: about +25 % and −13 %. |
| 8 | S1 | pencil length | 120 → **175 mm** | How many sharpenings a pencil allows. |
| 9 | R2, R3 | hand speed, altitude | 80 fixed, 60° → **v(L), 50°** | Mark ends, worn facets, and agreement with #319. |
| 10 | S2, S3 | hold length, taper | 50 mm, 0.22 → **75 mm, 0.20** | When a pencil is used up; a fresh pencil line's width. |

The other proposed changes have little effect on the image: S4–S7, L9–L10, M7, M9, R5 and R8.

## Sources found in this audit
Sources not already cited in the PRs' own research notes:
- Faber-Castell Pitt Pastel, 17.5 cm: Jerry's Artarama, https://www.jerrysartarama.com/faber-castell-pitt-pastel-pencils. Core 4.3 mm: The Art Gear Guide, http://www.theartgearguide.com/home/faber-castell-pitt-pastel-pencils.
- Stabilo CarbOthello, lead 4.4 mm: https://www.stabilo.com/us/products/coloring-drawing/chalk-pastel-pencil-stabilo-carbothello/. Length: Amazon listing B0013LB6S0.
- Finger lengths: ResearchGate fig. 2 of publication 5798067; PMC12309929. Hand length, ANSUR II: https://www.sota2.com/research/sota/hand-anthropometry-on-ansur-ii-combined-male-and-female.
- Informal pencil-stub thresholds: https://www.quora.com/How-short-is-too-short-a-pencil-graphite-grey-lead-colour-etc.
- Particle angularity: Stachowiak, *Wear* 241 (2000) 214; Hamblin & Stachowiak, *Tribol. Trans.* 39 (1996) 803; quoted in *Proc. Estonian Acad. Sci. Eng.* 7 (2001) 22–34, https://kirj.ee/wp-content/plugins/kirj/pub/eng-1-2001-22-34_20230304173220.pdf; chalk linearity cited in https://www.sciencedirect.com/science/article/abs/pii/S0043164801005579.
- Mulhearn & Samuels, *Wear* 5 (1962) 478 (attack angles on SiC paper; not reached).
- UART made in Germany, 300 g/m²: https://dakotapastels.com/products/Sanded-UArt.
- Colourfix 340 g/m² on a 300 g/m² base: https://www.jerrysartarama.com/art-spectrum-colourfix-smooth-pastel-paper; https://www.talasonline.com/Colorfix-Pastel-Paper.
- Kronos rutile L\* in test coatings: https://www.kronosww.com/wp-content/uploads/2026/10/KRONOS_ListofGrades_October_2026.pdf.
- Basic fuchsin ε: PhotochemCAD, https://www.photochemcad.com/databases/common-compounds/arylmethane-dyes/p-fuchsin; HiMedia, https://www.himedialabs.com/us/grm1089-basic-fuchsin-practical-grade.html.
- Paperboard through-thickness: Stenberg, *Int. J. Solids Struct.* (2003), https://www.researchgate.net/publication/223388379; KTH thesis, https://www.diva-portal.org/smash/get/diva2:1738574/FULLTEXT01.pdf.
- Ultrasonic against mechanical modulus: IPST review, https://repository.gatech.edu/server/api/core/bitstreams/487753d4-9757-43d1-9979-3f26bec5a8fa/content.
- Illustration board thickness: Blick, https://www.dickblick.com/products/crescent-no-300-cold-press-illustration-board/; United Now, https://www.unitednow.com/Crescent-100-Illustration-Board-24-Ply-Cold-Press-15x20.
- Strainer bars: Jens Juel strainers, https://www.researchgate.net/publication/363090756; RKD, Counting Vermeer §2.5.
- Stroke timing: JFDE review, https://jfde.org/index.php/jfde/article/download/255/131; Viviani & McCollum (1983); Cao & Zhai, CHI 2007, doi 10.1145/1240624.1240850 (exponent unverified).
- Pen azimuth: US 8,090,203, table 2, https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8090203.
- Cassatt's papers: Dirda, BPG Annual 35 (2016), https://cool.culturalheritage.org/coolaic/sg/bpg/annual/v35/bpga35-18.pdf (citing Bertalan 2008); "Construction Paper", BPG Annual 16, https://cool.culturalheritage.org/coolaic/sg/bpg/annual/v16/bp16-07.html (citing Shelley 1989).
- MTM-1 predetermined motion times (1 TMU = 0.036 s): the MTM Association's published tables.
