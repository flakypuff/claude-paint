# Estimates audit 2: #321 charcoal and #322 wet pastel

Compiled 2026-11-15. A ledger of every constant that is still marked as an estimate, or behaves as one without being labelled, in the two open PR branches `feat/charcoal` (#321) and `feat/wet-pastel` (#322). It was read from `git diff origin/main...fork/<branch>`, the research notes each branch adds (notes/research/charcoal.md, charcoal_optics.py, wet_pastel.md), and each PR's own list of remaining estimates. I checked those lists against the code.

**Classes.**
- **A:** derivable from first principles (the derivation is sketched).
- **B:** settable from published measurements (the source is one I searched for and found).
- **C:** measurable by us from available data (images, micrographs, spectra, datasheets, product listings).
- **D:** truly needs a bench measurement. For these I give the tightest physical bounds and where the value should sit.

Every A, B and C row gives a concrete replacement value. The arithmetic is in `notes/research/estimates_audit_2.py` (run it with `uv run`; it uses the repository's own Mie code). File:line references are to the PR branch named in each table's heading.

**Impact** is how much the picture depends on the constant, estimated from the code path:
- **high:** it sets the darkness or amount of every mark of that medium, or decides whether a whole mechanism happens;
- **medium:** a visible change in one gesture or in a transient;
- **low:** under about 1 ΔL* or confined to a rare path.

## Summary

| | A | B | C | D | total |
|---|---|---|---|---|---|
| #321 charcoal | 4 | 5 | 4 | 4 | 17 |
| #322 wet pastel | 9 | 8 | 2 | 4 | 23 |
| **both** | **13** | **13** | **6** | **8** | **40** |

**Only 8 of 40 need the bench.** The largest single faults are in #322, not in the constants either PR body lists:
- **Water sinks into the paper about 10⁴× too fast** (W1). It goes in at the Washburn rate of the geometric pore size, with no limit at the sheet's own pore volume. Measured uptake by real papers is far slower, even for unsized filter paper.
- **The soaked stick's hardness uses a metal's factor** (W2). Tabor's 3 is for a metal. A wet chalk compact is a soil, and soil mechanics has measured its strength against water content.

**In #321**, the largest are:
- **The first-surface veil drawn over a bare carbon bed** (C1). The PR's own note says it double-counts the facets.
- **Vine's coverage per volume** (C3). It takes pastel's 6 µm particle thickness, but a stick that is 80 % pores lays splinters that cover as about 14 µm.

**Searched and not found** (listed so nobody repeats them):
- a measured whole-stick particle size distribution for any pastel;
- a binder assay (wt %) of any pastel stick;
- the clay, gum and soot shares of a compressed charcoal stick (SDSs give "carbon" only);
- a measured hardness or wear rate of a charcoal stick;
- the Young's modulus of a kneaded eraser;
- the water capacity of a sable brush;
- Cobb values of artists' drawing or pastel papers;
- ΔE of spray fixative on pastels;
- the indoor humidity of a 19th-century studio;
- the full text of Duncan et al. 2023 (kneaded eraser on lamp black).

## #321 charcoal (branch `feat/charcoal`), by impact

| # | Constant | Where | Value | Controls (impact) | Class | Replacement and source or derivation |
|---|---|---|---|---|---|---|
| C1 | First-surface veil over a carbon bed | `canvas.rs:14` `SURFACE_REFLECTANCE` 0.04, added over `CarbonBed::color` | seen Y 0.060 (L* 29.5) for R∞ 0.021 | The black level of every charcoal mark (**high**: L* 29.5 against about 16 without the veil) | **A** | **No veil over a loose or bound particle bed: seen = R∞.** Mie's scattering of each opaque particle already holds its facet (first-surface) reflection, and KM's R∞ is the whole bed's diffuse return. A powder has no smooth interface for a second veil. charcoal.md §2 says so itself ("the veil double-counts the facets the Mie already holds"). Keep the veil only over a continuous film (paint, a glossy fixative film). Check against measured charcoal powder below 5 % (arXiv 2110.05832) and against the FORS spectra of charcoal in Redon's noirs (Heritage Science 2019, s40494-019-0286-6). This is engine-wide; see fault 4. |
| C2 | Vine hardness σp | `charcoal.rs:59` | 4 MPa | Archard deposit V = K F s/σp: how much every vine stroke lays (**high**, V ∝ 1/σp) | **B** | **3 MPa** (range 2–4). Wood charcoal after pyrolysis at 450 °C has a dynamic hardness of about 3.25 MPa, down from about 29 MPa for the wood ("Effect of final temperature on charcoal stiffness and its correlation with wood density and hardness", via its abstract; the page refused fetching). Charcoal is fired at 450–500 °C (FAO 1987). The abstract doesn't name the species. Willow (0.35–0.45 g/cm³) is lighter than most, and cellular solids scale as ρ^1.5 (Gibson–Ashby), so 3 is the upper middle of the range. The strength review (Wood Sci. Technol. 2016, s00226-016-0812-6) finds charcoal's mechanics rise again only above 500 °C. |
| C3 | Coverage thickness of what vine lays | `pastel.rs:89` `PARTICLE_UM` 6 µm, used by `lay_into`/`Cell::reflectance` for charcoal unchanged | 6 µm | How much area a volume of worn stick covers (**high**: q = 1 − e^(−dv/t)) | **A** (B inputs) | **14 µm** for vine (12–16). The engine counts a deposit in stick volume (`Cell::loose`). Willow charcoal is about 80 % pores: an apparent density of 0.27–0.35 g/cm³ (Cerne, charcoal at 400–750 °C; the rule ρ_char ≈ 0.68 ρ_wood applied to willow's 0.35–0.45) against willow char's true density of 1.44 g/cm³ (Wood and Fiber Science density note). A worn stick volume therefore yields only 0.2 of its volume as cell-wall splinters about 3 µm thick, which cover as 3/(1 − ε) ≈ 14 µm. Compressed (a 60 %-solids compact) covers as d/(1.5 × 0.6) ≈ 3–4 µm for 3 µm crumbs. With C2, a vine stroke covers ×0.57 what it does now, which is the grey "vine reads grey" the practitioners describe. |
| C4 | Compressed's lift | `charcoal.rs:51` | 0.42 | Share the kneaded eraser takes from compressed (**high**: erase share 0.23 in the PR's test) | **D** | **0.70**, bounds 0.42–0.98, set by the deposit's share of fines f: lift ≈ 0.42 f + 0.98 (1 − f). 0.42 holds only if the whole mark were sub-0.3 µm grains, which would be all soot. The historic recipe is "burned birch, clay, lamp black" (Wikipedia, *Charcoal (art)*), and SEM puts carbon-black particles about 7× smaller than charcoal's (the pyrotechnics study). With roughly half soot by volume, f ≈ 0.5 gives 0.70. That still keeps the practitioners' order vine > graphite > compressed (erase share ≈ 0.38 against graphite's 0.49). The bench measurement is f, from an SEM of a compressed mark. |
| C5 | Compressed R∞ | `dry.rs:179` `COMPRESSED_CHARCOAL` | 0.010 | Compressed's black (**high**) | **D** (A bounds) | **0.016**, bounds 0.010–0.021. The effective medium (Bruggeman) that gives 0.010 needs the compact's primary particles to be ≪ λ. That holds for lamp black (tens of nm) but not for ground charcoal of 1–10 µm, whose crumbs are a bed of opaque splinters like vine's (0.021). Half of each, mixed by KM, gives about 0.016 (the PR's own "half the carbon lamp black" case is 0.013 inside the effective medium). The bench needs the stick's soot share; no SDS or analysis gives it (searched the General's, cr630 and ESPO SDSs and CAMEO). |
| C6 | Vine R∞ by firing temperature | `dry.rs:168`; `charcoal_optics.py:40` `T_FIRE` 500 °C | 0.021 (0.018 at 400 °C, 0.028 at 600 °C) | Vine's black (**medium**: ±25 % over the plausible firing range) | **C** | **Keep 0.021 (500 °C)** until the firing temperature is read from published Raman. Daly et al. 2018 (*J. Raman Spectrosc.*, 14 black drawing media including natural charcoals) publishes spectra whose H_D/H_G can be placed on the 532 nm Raman thermometer (PMC13198549; Deldicque et al. 2016). The thermometer can't resolve 350–450 °C, so a ratio at its low end means ≤ 450 °C, which gives R∞ 0.018–0.020. Cross-check: Yang et al. 2012 (vis-NIR of biochars by pyrolysis temperature, doi 10.5402/2012/712837). |
| C7 | Vine lift | `charcoal.rs:46` | 0.98 | Erasing vine (**medium**) | **A** | **0.85.** The PR's force balance (JKR eraser against 10–150 nN rough-particle hold) leaves out capillary condensation. Char fired at ≥ 500 °C is hydrophilic: contact angles could not be read on 500 °C chars because water soaked in (Soil Systems 2019, 3:27; Kinney et al. 2012, minimum hydrophobicity at 400–600 °C). At 50 % RH the Kelvin radius is about 1.5 nm, so a bridge forms at each asperity contact: F ≈ 4πγa. With a ≈ 0.1 µm, an R = 1.5 µm splinter is taken 0.85; with a = 0.05–0.2, 0.92–0.72 (script §C7). This also uses carbon's Hamaker constant of 6.0 (carbon fibres 5.2–6.2 ×10⁻²⁰ J, via Maurer et al. 2001) in place of 6.4. |
| C8 | Compressed σp and K | `charcoal.rs:71–72` | 5 MPa, 0.07 | Compressed's deposit per force (**medium**) | **D** | **Keep.** σp bounds 2–10 MPa: pressed charcoal briquettes crush at 0.13–3.8 MPa compressive (mangrove briquettes; cotton-stalk 2.2 MPa), and indentation sits at about 3–20× compressive for a frictional compact. K bounds 0.01–0.1 (friable compacts). For comparison, graphite pencil on paper measures K ≈ 10⁻³–10⁻² (Bertin et al. 2025, "The physics of pencil drawing"), so a gum-bound char compact should sit above graphite. The ratio K/σp is what is needed: draw a known force and length on the bench and weigh the stick. |
| C9 | Vine K | `charcoal.rs:60` | 0.05 | Vine's deposit per force (**medium**) | **D** | **Keep 0.05**, bounds 0.01–0.1. Same method as C8. A cellular char crumbles by wall fracture, so it sits at the friable end, above graphite's 10⁻³–10⁻². |
| C10 | Lift of charcoal the finger re-lays | `pastel.rs:1221` (rub → `add_pastel` → `PASTEL_LIFT` 0.55) | 0.55 | Erasing smudged charcoal (**medium**) | **A** | **Carry the source cell's `lift` with what the finger moves.** Lift is a property of the particles (their size and wettability, C4 and C7), not of the gesture. Pressing them into the hollows is already in `erase`'s `reach` term (`graphite.rs:832`). Applying pastel's 0.55 counts the pressing twice and gives charcoal another medium's number. |
| C11 | Fixative wet share | `draw_pencil.rs:539` | 0.15 | How much a light spray darkens and binds (**low** for charcoal, about ΔL* 0.2–0.6; **medium** for pastel) | **C** | **The wet share = resin thickness ÷ the pores' volume, with a light spray laying 1.5 µm of resin.** A can of Krylon Workable Fixatif (11 oz, 5.25 % non-volatile by the SDS) covers 15–20 ft² per coat (retail listings). That is 8–11 µm of resin per coat at ρ 1.07, about 4–5 µm at 50 % transfer, and a light third of a coat is ≈ 1.5 µm. Into the pores (ε 0.55) of 10, 20 and 30 µm of loose pastel, it wets 0.27, 0.14 and 0.09. So 0.15 is right for a middling 20 µm layer, but the share should fall with thickness. |
| C12 | Compressed's grip removed (gum glassy) | charcoal.md §3 | grip 0 | Whether compressed binds to the sheet (**medium**) | **B** (confirmed) | **Keep 0**, with a stated limit. Righetto & Netto 2005 measured *pure* gum arabic (Tg 62 °C at aw 0.33, 42.6 °C at aw 0.54), not only the juice mix, so the citation stands. Extrapolated (92 K per unit aw), Tg reaches 25 °C at aw 0.73 and 20 °C at aw 0.78. Grip returns only in a room above about 75 % RH: Paris outdoor air (annual 76 %), not a heated studio (W6). |
| C13 | Stick sizes | `charcoal.rs:58,61,70,73`; `draw_pencil.rs:953–954` | vine Ø6 × 150 mm; compressed 7 mm square × 70 | Line width and how long a stick lasts (**low**) | **C** | **Vine: 140 mm long, Ø 5 / 8 / 10 mm (thin / medium / thick), default 8.** Winsor & Newton Artists' Willow lists 14 cm (The Range, Artlounge, Artist & Craftsman); the diameters come from Artlounge, and natural sticks vary. **Compressed: 6.35 mm square × 76 mm.** General's lists 3″ × ¼″ × ¼″ (manufacturer and Blick); its rectangular stick is 3 × ½ × ¼ in. |
| C14 | Vine splinter size | `charcoal_optics.py:108` | 3 µm | R∞ (under 5 %) and lift (insensitive above 1 µm) (**low**); C3's wall thickness (**medium**) | **C** | **Keep 3 µm** and read it from published micrographs. CAMEO calls charcoal-black particles "small, elongated and splintery". SEM of charcoal underdrawing reconstructions (Heritage Science 2022, s40494-022-00649-x) shows fragments that can be measured, and willow fibre walls are 2–4 µm thick. |
| C15 | Hamaker constants and eraser modulus | `charcoal_optics.py:189`; charcoal.md §4 | A_char 6.4, A_eraser 6.5 ×10⁻²⁰ J; E 0.1 MPa | Lift (**low**: the ratio is ×11 or more) | **B** (E: D) | **A_char 6.0** (carbon fibres 5.2–6.2, activated carbon 5.0–7.8; Maurer, Mersmann & Peukert 2001 and the Morra values they cite). **A_eraser 6.5, kept.** Kneaded erasers are polyisobutylene with vegetable or mineral oil, CaCO₃ and TiO₂ fillers (General's MSDS; Derwent SDS 2020; ESPO SDS), a hydrocarbon polymer in the 6–7 range. **Cellulose–CaCO₃ is 7.4**, not cellulose's 5.8, for pastel's filler (AFM review, *Int. J. Mol. Sci.* 2012, 13:12773). E is unmeasured: 0.03–0.3 MPa for a putty, and the JKR conformity condition holds throughout, so keep 0.1. |
| C16 | Gum's refractive index (compressed's binder) | `charcoal_optics.py:45` | 1.47 | Compressed R∞ (**low**, binder 5 %) | **B** | **1.52**: gum arabic films measure 1.51–1.54 (dry_pigment_optics.md §1). #322 already uses 1.52 (`wet_pastel.rs:67`), so the two PRs disagree. |
| C17 | Fixative resin index and density | `charcoal_optics.py:47,172` | 1.5; 1.15 g/cm³ | The resin-wetted R∞ and the SDS volume share (**low**) | **B** | **n 1.49, ρ 1.07.** Krylon 1301 has been found to resemble poly(n-butyl methacrylate) (AIC Conservation Wiki, BPG Adhesives); PBMA n_D 1.483, Paraloid B-72 1.487, PMMA 1.4905. PBMA ≈ 1.05–1.07 g/cm³. |

Not physics, so left out of the counts: `Stick::round`'s eased-edge facets for a twig (a cut or broken end is a gesture), and the easel's clamp ranges.

## #322 wet pastel (branch `feat/wet-pastel`), by impact

| # | Constant | Where | Value | Controls (impact) | Class | Replacement and source or derivation |
|---|---|---|---|---|---|---|
| W1 | Water into the sheet: Washburn at the paper's geometric pore height, angle by Cassie from `absorbent`, no cap | `wet_pastel.rs:249–258`, `:90–91` (105°, 0°); `paper.rs:116` `absorbent` 0.8 | D = rγcosθ/2η = 163 mm²/s on the default sheet: 6.4 mm of water in the first second | Whether standing water sinks or stays, and so how much gum leaves and how much pastel binds (0.15 against 1.0), and drying time (**high**) | **B** | **Uptake U(t) = min(ε·caliper, C₆₀·√(t/60 s)).** C₆₀ is the sheet's Cobb60: **25 g/m² for the default sized drawing paper** (sized writing and bond grades 22–30 g/m², unsized 50+, TAPPI values via paperonweb; Mi-Teintes is gelatin-sized, by retail listings). For an unsized sheet use **D = 14 mm²/s**, as measured for Whatman filter paper (Washburn K = 0.38 cm/s^½; *Sci. Rep.* 2019, s41598-019-52202-9). The engine's cos θ = 1 gives 218 mm²/s, 15× faster than that. **Cap** the total at the sheet's pore volume, ε × caliper = 150 µm for the default sheet. Map `absorbent` 0→1 to C₆₀ 20→150 g/m² log-linearly, and drop the Cassie angle: the kinetics of a sized sheet is the size's slow wetting, which an angle can't give. With C₆₀ 25, a 40 µm wash loses about 3 µm in its first second and 25 µm in a minute, and stands for about 2.5 minutes, so much of it evaporates and keeps its gum instead. |
| W2 | Wet tip hardness: Schubert capillary state × Tabor 3, linear in saturation | `wet_pastel.rs:265–268`; `pastel.rs:482,492` | 0.29 MPa soaked (≈ 1/13 of a soft stick) | How much a wet stick lays (the PR's test: 3.5×) (**high**) | **B** | **Remoulded strength by liquidity index** (Wroth & Wood 1978, *Can. Geotech. J.* 15:137): s_u = 170 kPa · e^(−4.6 LI), and H = 5.14 s_u (Prandtl, undrained). LI comes from the stick's water content w = S ε ρ_w/((1−ε) ρ_s), and the Atterberg limits come from the filler: remoulded chalk PL 0.244, LL 0.310 (Bialowas, Diambra & Nash 2016); kaolinite PL 0.25–0.40, LL 0.30–0.75 (White 1949, *Am. Mineral.* 34:508). For a chalk stick (ε 0.55):<br>• below S 0.53 it is brittle and keeps its dry σp (or the drained bound below);<br>• S 0.6 → 0.09 MPa; S 0.7 → 3.6 kPa;<br>• a soaked tip (S 1, LI 3.3) is a slurry, so lay it as a paste (see W17), not by Archard.<br>A kaolin-rich stick is still plastic at S 1 (0.16 MPa). Tabor's 3 is for a frictionless plastic metal. The drained upper bound is Prandtl's c·N_c with c = σ_t tan φ, φ 29–34° for remoulded chalk: 15–28 × σ_t = 2.2–4.1 MPa. Vardanega & Haigh 2014 find the 100× ratio between PL and LL too high (their smaller ratio was cut off in the search excerpt, and I haven't verified it). That changes only the plastic range. |
| W3 | Particle size | `wet_pastel.rs:56` `PARTICLE_D_UM` | 3 µm | Wet strength ∝ 1/d, tip spreading ∝ d, paste cover ∝ d (**high**) | **B** | **1.7 µm (Sauter mean d₃₂).** The historic pastel filler is Champagne/Meudon whiting: d50 2.4–2.7 µm, D97 13–15 µm, 44–47 % below 2 µm (Art-Chimie *Blanc de Meudon* specification; "average 2 µm", Couleur Pigments). A volume lognormal through d50 and D97 gives σ_ln 0.87–0.94 and d₃₂ 1.64–1.75 µm. Capillary strength (Rumpf, Schubert), the Kozeny hydraulic radius and coverage per volume all scale with d₃₂, not d50. |
| W4 | Wet darkening's Mie table size, and no filler | `dry.rs:95` `scatter_in` (d = 1 µm); `palette.rs` `dry_index`; `wet_pastel.rs:70` `DEFAULT_INDEX` 1.9 | S_water/S_air: ultramarine 0.137, lead white 0.69 | How dark each wet pastel goes (**high**) | **A** (B inputs) | **Regenerate the table at d = 1.7 µm** (W3): ultramarine 0.214, Prussian blue 0.359, bone black 0.495, lead white 0.659, chrome yellow 0.720, vermilion 0.817. The 1 µm table contradicts the PR's own 3 µm. **Give sticks their filler:** a tint is pigment let down with whiting, so take the filler share that reproduces the stick's dry color by KM against whiting's S (dry_pigment_optics.md table 2.2). Mix the index by S × volume, not by volume. Whiting in water keeps 0.41 of its scattering at 1.7 µm (calcite n 1.59), so a pale tint darkens by its chalk whatever its pigment. **`DEFAULT_INDEX` → 1.59** (calcite, birefringence mean). |
| W5 | Dried binding = share of gum kept (linear) | `graphite.rs` `Cell::gum_set`; wet_pastel.md §3 | 0.15 of the pastel bound on the default sheet | Whether a dried wet passage resists the finger (**high**) | **D** (A structure) | **A threshold, not a share.** The kept gum stays in solution through all the pores, and it dries into bridges at every contact, smaller ones. A bridge's strength goes as its volume^(2/3), so with a share g left, every contact holds g^(2/3) of a stick's. The pastel is bound wherever g^(2/3) σ_t,stick exceeds the finger's shear (about 10–30 kPa [estimate: skin friction μ ≈ 0.5 under a light press of 20–60 kPa; not looked up]). The bench number is a dry stick's tensile strength σ_t (bounds 0.1–1 MPa for a gum-bound chalk compact). That puts g* between 0.001 and 0.1, so W1's 25 g/m² sheet binds a soaked passage fully. Evaporation also carries gum to the drying top (as with fixative), which strengthens the crust. |
| W6 | Studio air | `wet_pastel.rs:78–79` | 20 °C, 50 % RH | Evaporation 0.71 µm/min, and so drying time (**medium**: ×0.6–1.2 over the seasons) | **A** (B inputs) | **Keep 20 °C / 0.50 as the default and add a log-head room setting.** Heating Paris's outdoor air without adding moisture: annual mean 12.3 °C at 76 % RH (Montsouris, Infoclimat 1961–90) gives **46 %** at 20 °C, January 35 % at 18 °C, and an unheated July 68 %. Evaporation at those is 0.71, 0.86 and 0.46 µm/min. The museum band (40–60 %) is for storage, not studios. No measured historic studio record was found. The same RH sets C7's capillary hold and C12's gum Tg. |
| W7 | Porosity | `wet_pastel.rs:51` | 0.60 | Pore water, paste water, the wet strength factor (1−ε)/ε, paste cover (**medium**) | **C** | **0.55** (0.50–0.61). One listed Sennelier stick weighs 9.07 g. At its listed 2.65 × 0.45 in it is ρ 1.32 g/cm³, so ε 0.50 (solids 2.65) to 0.54 (2.9). At the nominal ½ × 2½ in it is 1.13, so 0.57–0.61. A white's denser pigments push toward 0.6. |
| W8 | Shed falls linearly with saturation | `pastel.rs:493` | SHED × (1 − S) | Crumbs from a wet tip (**medium**) | **B** | **Full shed below the plastic limit, none above the liquid limit, linear between:** for chalk at ε 0.55, S_PL 0.53 and S_LL 0.67 (W2's Atterberg limits; kaolin 0.76 and 1.41). Brittle fracture makes crumbs below PL, the plastic range smears, and above LL the paste flows. |
| W9 | Dip depth | `wet_pastel.rs:94` `DIP_MM` | 1 mm | The water a dip loads (`tip_capacity_mm3`) (**medium**) | **A** (immersion depth is a gesture) | **1 mm + √(D t_dip) ≈ 3.6 mm** for a 0.5 s dip, with D from W11. The water wicks up while the tip is in the jar, so the wetted length can't be the immersion depth. |
| W10 | Surface tension and viscosity of the pore water | `wet_pastel.rs:73–74` | 72.8 mN/m, 1.002 mPa·s (pure water) | Wet strength ∝ γ, tip and sheet Washburn ∝ γ/η (**medium**) | **B** (η: A) | **γ 50 mN/m, η 1.3 mPa·s.** The pores dissolve the stick's gum to about 2.6 % (1.5 % of 1.06 g solids per 0.6 g water per cm³). Gum arabic is surface-active: 52.5 mN/m at 1 % w/v (*Food Hydrocoll.*, S0268005X19322544) and 46.9 mN/m at equilibrium for A. senegal at 0.5 % (the *A. tortuosa* study). η comes from the intrinsic viscosity 0.19 dL/g (Huggins), ≈ 1.2–1.5 mPa·s at 2–3 %. That the gum is arabic, not tragacanth, is supported by GC/MS of a commercial early-20th-century pastel (Boccioni drawing, *J. Cult. Herit.*, S1296207417307501). Water on paper (W1) keeps γ 72.8 only if it carries no gum. |
| W11 | The tip's Washburn spreading | `wet_pastel.rs:283–286` | 54 mm²/s | How fast a dip's water leaves the drawing end (**medium**) | **A** | **13 mm²/s**: the same law with d 1.7 (W3), ε 0.55 (W7), γ 50, η 1.3 (W10). A dip then serves a few strokes rather than one (after 1 s, before evaporation, the 1 mm zone keeps 0.26 of its water, not 0.13). |
| W12 | Paste coverage thickness | `wet_pastel.rs:275–277` | 0.83 of 6 µm | Coverage of a wet stick's or a brush's paste (**medium**) | **A** | **0.42**: d/(1.5 (1 − ε)) / 6 µm with d 1.7 and ε 0.55. |
| W13 | Partly filled pores: Bruggeman air/water | `wet_pastel.rs:115–141` | half filled n_med 1.16 (lead white 0.82 of dry S) | The look while drying (**medium**, transient) | **B** | **Darkening exponential in saturation**, f(S) = (1 − e^(−S/S₀))/(1 − e^(−1/S₀)) with **S₀ ≈ 0.2**. Soil reflectance falls exponentially with moisture and fits one curve across soils in degree of saturation (Lobell & Asner 2002, *SSSAJ* 66:722). The visible saturates at about 20 % volumetric water (Hick et al. 2026, restating it), i.e. S ≈ 0.4 for soils of ε 0.45–0.5. Water wets the grains' surfaces and contacts before it fills the pores. S₀ needs their fitted constant (full text not retrieved). |
| W14 | Brush water capacity = a full paint load | `bristle.rs:560` | 0.14 mL (10 mm sable) | Water and paste a brush lays (**medium**) | **C** | **≈ 0.2 mL for a 10 mm round** (0.15–0.25). Take the belly as a cone of the brush's diameter and its hair length out, with liquid filling about 0.6 of the bundle's volume, using Rosemary & Co Series 33's published diameter and hair-length table per size. No gravimetric measurement of a sable was found (retailers give only "3× a synthetic"). |
| W15 | Compaction of a drying paste | wet_pastel.md §2 | none (dries at the stick's ε) | Coverage and scattering of a dried paste (**medium**) | **A** | **Dries to ε ≈ 0.40.** Gum arabic is a steric dispersant, so the paste is dispersed, not flocculated. The drying menisci pull at 2γ/r ≈ 100 kPa (r ≈ 1 µm), well above a dispersed bed's yield, so it packs toward random close packing (ε 0.36). Dependent scattering at d ≈ λ isn't in the Mie, so leave S per volume as is and change only the volume. |
| W16 | Pressure → 0.5–1.5 of the water | `wet_pastel.rs:453` | linear | How much a wash lays (**low–medium**) | **A** (reuse) | **Use the bristle model's own pressure law,** the one paint strokes use for contact and lay. A water-loaded belly is the same mechanics. |
| W17 | Archard K unchanged wet | `pastel.rs` (`wear` kept) | dry K | A wet stick's deposit (**medium**) | **D** | **Keep K below the plastic limit** (0.01–0.06, the dry range). **Above the liquid limit drop Archard:** the slurry transfers as wet paint does (the tool's `lay`/`pickup`, as #322 already does for the brush), limited by the wetted tip's volume. Between PL and LL, interpolate. The bench measures the weight laid per force and length at known S. |
| W18 | Convective coefficient | `wet_pastel.rs:84` | 2.5 W/m²K | Evaporation (**medium**) | **A** (confirmed) | **Keep.** Churchill–Chu for a vertical plate 0.3–0.5 m, 3.7 K below the air, gives 2.5–2.7 W/m²K. A sheet worked flat (heat flow up) is ISO 6946's 5.0: a gesture, a later setting. |
| W19 | Emissivity of water | `wet_pastel.rs:85` | 0.95 | Surface temperature (**low**) | **B** (confirmed) | **Keep** (water 0.95–0.96, handbook). |
| W20 | Gum index and density | `wet_pastel.rs:63–67` | 1.52; 1.4 g/cm³ | Dried darkening (**low**) | **B** (confirmed) | **Keep** (films 1.51–1.54; 1.35–1.49 g/cm³). |
| W21 | Falling rate D_v ε^1.5 | `wet_pastel.rs:202–205` | a = 3.3e-4 /µm | The last water (**low**) | **A** (confirmed) | **Keep** (Bruggeman tortuosity). Under 1 % of a thin layer's time. |
| W22 | Gum share of the stick | `wet_pastel.rs:60` | 1.5 wt % | Only the dried gum's pore share (0.019), so dried color under 1 % (**low**). Binding is relative (W5). | **D** | **Keep**, bounds 0.3–3 %. No assay found (Boccioni's GC/MS identifies the gum but doesn't quantify it; recipes give 1:30 solutions). Ash or TGA weight loss of a commercial stick would set it. |
| W23 | The brush's `lay`, `pickup`, `run` | `wet_pastel.rs:343–345` | the tool's | Wash transport (**medium**) | **D** (inherited) | Reused from the brush model, so they are that model's estimates. Not re-audited here. |

Not physics, so not counted: `STEP_PX` (the numerics), `b:dip`'s default `amount` 0.5 and `b:wash`'s default pressure 0.5 (`api.rs:887, 931`; gestures), and hand time (`RELOAD`, `REMIX`; pacing).

## The engine-wide faults found by the #321 revision

### 1. Pastel in the tooth mixed by averaging reflectance

**The fault is right.** The engine already contradicts itself: a stick's own color is built from its tubes by Kubelka–Munk (`dry.rs`), but two sticks in the tooth are mixed by averaging R∞ by volume (`Cell::add_pastel`, `graphite.rs:201`).
- **Measured.** Intimate powder mixtures darken far beyond linear: "a few percent of dark grains can drastically reduce the reflectance, much more than their weight fraction". Clark 1983 (*JGR* 88:10635) measured montmorillonite with charcoal and carbon grains, and Clark 1999 restates the finding. Linear mixing holds only where the components lie side by side or one on top of the other: charcoal *spread over* soils mixes linearly (USDA Forest Service, *Spectral analysis of charcoal on soils*).
- **I reproduced #321's numbers.** A yellow (0.75, 0.6, 0.1) with S = 0.55 µm⁻¹ and 5 % vine charcoal gives G 0.571 by averaging against 0.549 by KM.

**Proposed physical fix,** behind a switch:
- **Intimate mixing by KM.** Store one more f32 per cell: the loose layer's volume-weighted scattering S per unit stick volume, gray. Pastels' S is nearly flat (chalk, pigments in air), and so is carbon's. Mix (K/S) weighted by S × volume:
  - (K/S)_mix = Σ vᵢ Sᵢ (K/S)ᵢ / Σ vᵢ Sᵢ, then R∞ from it;
  - each stick carries its S: from `mie_air` for pastels (with filler, W4); `CarbonBed::s_air` × (1 − ε_stick) for charcoal, since `loose` counts stick volume (vine's ε ≈ 0.8, C3).
  - Use this where the mixing is intimate: the finger, crumbs into a loose bed, a wet brush's paste.
- **Layering by Kubelka's two-layer formula.** A new stroke over an existing loose layer is layered rather than mixed: R = R₁ + T₁² R₂ / (1 − R₁ R₂), with R₁ and T₁ from the new layer's KM at its thickness. That keeps the over-loose versus over-fixed muddying physical without overstating it.
- Areal partition stays in coverage `a`.

### 2. Pastel's eraser lift of 0.55 against an adhesion figure of 0.88–1

**Half right.** 0.55 is not derived from anything, but the claim that "adhesion gives 0.88–1" isn't established either. The force balance (charcoal.md §4) misses three things:
1. **Capillary condensation.** Chalk, kaolin and cellulose are hydrophilic. Above about 30 % RH the capillary force exceeds van der Waals for such pairs (AFM review, *Int. J. Mol. Sci.* 2012; colloidal-probe adhesion to a cellulose fibre rises with RH, arXiv 2012.10207). A bridge at one asperity of a = 0.1–0.2 µm adds 90–180 nN. With it, a 1.5 µm particle is taken 0.72–0.85 rather than 0.98, and a 0.5 µm one 0.36–0.54 (script §C7).
2. **Fines.** Whiting is 44–47 % by volume below 2 µm (W3).
3. **Hamaker for cellulose–CaCO₃** is 7.4 ×10⁻²⁰ J, not cellulose's 5.8.

Integrated roughly over whiting's distribution at 50 % RH (asperity a 0.1 µm, by volume), pastel's lift comes to about **0.6–0.75**; a full integration needs the paper's asperity size. 0.55 sits just below that range, not far outside the physics. Vine at 500 °C gets the same capillary term (C7, 0.85), and the practitioners' order vine > pastel follows from vine's coarser splinters.

**Proposed fix:**
- Compute `lift` per stick from its size distribution: the eraser's JKR pull against the vdW hold (rough-particle above the asperity scale, DMT below) plus the capillary bridge at the studio RH (W6). The lift then varies with the room's humidity.
- Keep `reach` for the hollows.
- Check the result against Duncan, Vicenzi, Lam & Brogdon-Grantham 2023 (*JAIC* 62:152), who measured kneaded-eraser removal of lamp black from papers of three roughnesses by spectrophotometry. That is a published measurement to calibrate the eraser-pull side, not the engine's own output; the full text wasn't retrieved.
- Proposed value at 50 % RH: **0.70.**

### 3. Fixative darkening that can't tell carbon from pastel

**Right, and understated.** The rule divides K/S by (1 − w + w/5) for every particle (`graphite.rs:222`, `pastel.rs` `fix_pastel`), and its comment says "to about a fifth, for particles of n ≈ 2 in resin". By the repository's own Mie that is wrong for n ≈ 2:
- `mie_air`'s own table gives S_air/S_oil = 1.9 at n 2.0 (oil 1.48 ≈ resin 1.49). That is a factor of 0.53, not 0.2.
- My run at resin 1.49, d 1.7 µm gives 0.49 for n 2.0, 0.61 for 2.4, 0.72 for 3.0, 0.30 for 1.74, 0.14 for 1.65, 0.056 for whiting (1.59), 0.027 for 1.56 and about 0 for ultramarine.

So the ÷5 is right only near n ≈ 1.7:
- It **over-darkens** every high-index pigment: lead and zinc whites, the cadmiums, chromes, earths and vermilion, the bulk of a palette.
- It **under-darkens** the low-index ones: ultramarine, Prussian blue, the lakes, and the chalk that makes up a tint.
- Carbon is the small case (×1.0–1.6, ΔL* under 0.5).

**Proposed fix:**
- Store a per-cell resin scattering ratio: u16, S-weighted, set when the pastel is laid. Its sources:
  - #322's `Cell::index` through `mie_air`'s S_air/S_oil for pigments and filler;
  - `CarbonBed` s_resin/s_air for charcoal.
- Mix the ratio by S × volume, as in fault 1.
- Set the wet share from resin thickness over pore volume (C11), not a constant 0.15.

This doesn't need the carbon flag #321 thought new state would require: the index (or the ratio) is that state, and #322 already adds it.

### 4. Two more engine-wide faults the audit turned up

- **The 4 % first-surface veil over particle beds** (C1). For a bare powder it double-counts the facets that Mie already holds. It matters most for the blacks (charcoal L* 29.5 against about 16) and little for pale pastel. Fix: apply the veil only over a continuous film.
- **Three things that hang on the room's humidity:** evaporation (W6), capillary adhesion (fault 2) and gum's glass transition (C12). One room-climate setting in the log head should feed all three, so they can't disagree.

## Searches made

Each search ran with the reformulations noted in its row.

| Topic | Found | Not found |
|---|---|---|
| Charcoal reflectance against pyrolysis temperature | microscope %Ro rises with temperature; biochar vis-NIR (Yang 2012) | bulk visible albedo by temperature |
| Raman firing temperature of drawing charcoal | thermometers (Deldicque 2016, PMC13198549); Daly 2018 spectra of drawing media | a direct study of artists' charcoal |
| Compressed charcoal composition (SDS, conservation) | SDSs give 100 % carbon (cr630, ESPO); one 80.4 % carbon-black mixture (likely fuel); CAMEO; Heritage Science 2022 | clay, gum or soot shares of an art stick |
| Gum arabic Tg | pure gum: Righetto & Netto 2005 confirmed | the anhydrous Tg |
| Willow charcoal density and porosity | true density 1.44; ρ_char ≈ 0.68 ρ_wood; 0.27–0.35 apparent | a measured willow apparent density |
| Charcoal hardness and strength | 3.25 MPa dynamic hardness at 450 °C; 6.9–8.8 MPa compression (eucalyptus) | a charcoal stick's hardness or wear |
| Pastel particle size (SEM, laser) | whiting supplier specification (d50, D97) | any pastel stick's distribution |
| Pastel binder content | GC/MS identifies the gum (Boccioni) | wt % assays |
| Dry-cleaning erasers on soot | Duncan et al. 2023; Microscopy Today 2021; JAIC 22:1 | the ΔL values (full text) |
| Kneaded eraser composition | General's MSDS, Derwent and ESPO SDSs | modulus |
| Capillary adhesion and RH | AFM review; fibre colloidal probe; Hamaker for cellulose–CaCO₃ | calcite on cellulose against RH |
| Cobb of artists' papers | ISO 535 and TAPPI bands; Mi-Teintes gelatin-sized | any artist paper's Cobb |
| Washburn in paper | Whatman K = 0.38 cm/s^½; JFM review | — |
| Gum solution γ and η | 52.5 mN/m at 1 %; 46.9 at 0.5 % | measured η at 1–5 % |
| Soil reflectance against moisture | Lobell & Asner 2002 (exponential) | its fitted constant |
| Atterberg limits | kaolinite (White 1949); remoulded chalk (Bialowas 2016; Jardine) | chalk putty in CIRIA C574 itself |
| Strength against liquidity index | Wroth & Wood 1978; Vardanega & Haigh 2014 | — |
| Studio climate | Montsouris RH normals | a measured historic interior |
| Stick sizes | W&N willow; General's compressed | — |
| Fixative resin and coverage | Krylon resembles PBMA (AIC wiki); 15–20 ft² per can | ΔE on pastels |
| Pastel stick mass | Sennelier 9.07 g | a maker's density |
| Brush water capacity | Rosemary & Co dimension table | a gravimetric measurement |
| Graphite and pencil wear | Bertin et al. 2025 (K 10⁻³–10⁻² on paper) | charcoal |
| Biochar wettability | Kinney 2012; Soil Systems 2019 | the 500 °C angle (soaks in) |

## Sources

- Bertin et al., "The physics of pencil drawing" (preprint 2025, Research Square rs-10448967).
- Bialowas, Diambra & Nash 2016, "Small strain stiffness of chalk" (remoulded Margate chalk: LL 31.0 %, PL 24.4 %); Jardine et al., "Ageing and cyclic behaviour of axially loaded piles driven in chalk" (LL 30–31 %); remoulded chalk φ′ 29–34° (Clayton 1978; Razoaki 2000; Bundy 2013, as cited there).
- Boccioni pastel GC/MS: "The chemistry of pastels: Investigation of the organic materials in a drawing by Umberto Boccioni", *J. Cult. Herit.* (S1296207417307501).
- Clark, R. N. 1983, *JGR* 88(B12):10635; Clark 1999, *Spectroscopy of Rocks and Minerals*, clarkvision.com; USDA Forest Service, *Spectral analysis of charcoal on soils* (treesearch 37497).
- Duncan, Vicenzi, Lam & Brogdon-Grantham 2023, *JAIC* 62(2):152–167; Microscopy Today 2021, doi 10.1017/S1551929521001516.
- "Effect of final temperature on charcoal stiffness and its correlation with wood density and hardness" (ResearchGate 341169690); "Factors affecting the mechanics of carbonized wood", *Wood Sci. Technol.* 2016 (s00226-016-0812-6); Eucalyptus charcoal compression (ResearchGate 330121984).
- Cerne (Brazil), "Higroscopicity of charcoal produced in different temperatures" (apparent density 0.346–0.268 g/cm³); "A note on density change patterns in charred wood", *Wood and Fiber Science* (willow char 1.44 g/cm³).
- Art-Chimie, *Carbonate de calcium, Blanc de Meudon* (D50 2.4–2.7 µm, D97 13–15 µm); Couleur Pigments, *White from Meudon*.
- Gum arabic surface tension: *Food Hydrocolloids* (S0268005X19322544, native gum 52.5 mN/m at 1 %); *A. tortuosa* gum study (A. senegal 46.9 mN/m at 0.5 %).
- Hamaker constants: Maurer, Mersmann & Peukert 2001, *Chem. Eng. Sci.* (S0009250901000331); AFM surface-forces review, *Int. J. Mol. Sci.* 2012, 13:12773 (cellulose–CaCO₃ 7.40).
- Kinney et al. 2012, "Hydrologic properties of biochars produced at different temperatures", *Biomass Bioenergy*; "Pyrolysis temperature effects on biochar–water interactions", *Soil Systems* 2019, 3:27.
- Kneaded eraser: General Pencil MSDS (Blick #21587); Derwent Kneadable Eraser SDS (2020); ESPO Kneadable Art Eraser SDS.
- Krylon: CAMEO (MFA), *Krylon*; AIC Conservation Wiki, *BPG Adhesives*; Workable Fixatif coverage 15–20 ft² per 11 oz (retail listings: Hobby Lobby, Walmart, Amazon).
- Lobell & Asner 2002, *SSSAJ* 66:722; Hick et al. 2026, *Eur. J. Soil Sci.* (ejss.70319).
- Paper: ISO 535; TAPPI T 441; paperonweb, *Properties of Paper* (Cobb by grade); "Paper stacks for uniform rehydration…", *Sci. Rep.* 2019 (s41598-019-52202-9), Whatman K = 0.38 cm/s^½.
- Paris climate: *Climate of Paris* (Wikipedia; Montsouris RH 1961–90 from Infoclimat).
- Raman thermometry: Deldicque et al. 2016, *Carbon*; automated 532 nm calibration (PMC13198549); Daly et al. 2018, *J. Raman Spectrosc.* (jrs.5417); Redon's noirs, *Heritage Science* 2019 (s40494-019-0286-6); "Charcoal or black stone?", *Heritage Science* 2022 (s40494-022-00649-x).
- Righetto & Netto 2005, *Int. J. Food Prop.* 8(2), doi 10.1081/JFP-200060262.
- Sennelier stick: retail listing (White 525, 9.07 g, 2.65 × 0.45 in).
- Stick sizes: Winsor & Newton willow charcoal (The Range; Artlounge; Artist & Craftsman Supply); General Pencil 957ABP and Blick (3″ × ¼″ × ¼″).
- White 1949, "Atterberg plastic limits of clay minerals", *Am. Mineral.* 34:508.
- Wroth & Wood 1978, *Can. Geotech. J.* 15(2):137; Vardanega & Haigh 2014, "The undrained strength–liquidity index relationship" (Cambridge repository).
- Yang et al. 2012, "Characterization of biochar properties … using visible-near-infrared spectroscopy", doi 10.5402/2012/712837.
- In this repository: notes/research/charcoal.md, charcoal_optics.py, wet_pastel.md, dry_pigment_optics.md and dry_pigment_mie.py (on the PR branches).
