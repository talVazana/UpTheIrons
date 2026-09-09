from typing import Dict, List
from app.models.enums import ContentType, ContentStatus, DifficultyLevel, SourceType, TrustLabel
from app.models.content import (
    ContentEnvelope,
    MaterialMetadata,
    HeatTreatmentRecipe,
    ProjectMetadata,
    GuideMetadata,
    SourceReference,
    SafetyPrecaution,
    RelatedContentLink,
)
from app.models.source import SourceProvenance
from app.repositories.base import BaseRepository

SEED_MATERIALS: List[ContentEnvelope] = [
    ContentEnvelope(
        id="mat-1084",
        type=ContentType.MATERIAL,
        title="1084 High Carbon Steel",
        slug="1084",
        summary="Eutectoid carbon steel (~0.84% C). Highly forgiving, standard recommendation for beginner knife makers.",
        category="materials",
        tags=["steel", "carbon-steel", "eutectoid", "beginner-friendly"],
        difficulty=DifficultyLevel.BEGINNER,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="metallurgy-standard",
            source_name="ASM International Handbook",
            source_url="https://www.asminternational.org",
        ),
        metadata=MaterialMetadata(
            classification="High Carbon Steel (AISI 1084)",
            carbon_pct=0.84,
            alloying_elements={"manganese": 0.75, "phosphorus": 0.03, "sulfur": 0.05},
            forging_temp_range_f="1650°F – 2100°F",
            heat_treatment=HeatTreatmentRecipe(
                normalizing_temp_f=1600,
                annealing_temp_f=1450,
                hardening_temp_f=1500,
                quench_medium="Fast or medium speed quench oil (e.g. Parks 50 or canola warmed to 130°F)",
                tempering_range_f="400°F – 450°F (2x 2 hours)",
                target_hardness_hrc="58 – 61 HRC",
                notes="Simple thermal cycle: soak at 1500°F for 5 minutes, quench immediately, temper twice.",
            ),
            beginner_suitability=True,
            common_applications=["Hand-forged knives", "Punches", "Drifts", "Small hand tools"],
            common_mistakes=["Overheating in forge past yellow heat causes rapid grain growth."],
            source_reference="ASM Handbook Vol 1: Properties and Selection of Irons, Steels, and High-Performance Alloys",
        ).model_dump(),
    ),
    ContentEnvelope(
        id="mat-1095",
        type=ContentType.MATERIAL,
        title="1095 High Carbon Steel",
        slug="1095",
        summary="Hypereutectoid carbon steel (~0.95% C). Exceptional edge retention and hamon activity, but requires fast quench.",
        category="materials",
        tags=["steel", "high-carbon", "hypereutectoid", "hamon"],
        difficulty=DifficultyLevel.INTERMEDIATE,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="metallurgy-standard",
            source_name="ASM International Handbook",
            source_url="https://www.asminternational.org",
        ),
        metadata=MaterialMetadata(
            classification="High Carbon Steel (AISI 1095)",
            carbon_pct=0.95,
            alloying_elements={"manganese": 0.40, "phosphorus": 0.03, "sulfur": 0.05},
            forging_temp_range_f="1600°F – 2050°F",
            heat_treatment=HeatTreatmentRecipe(
                normalizing_temp_f=1650,
                annealing_temp_f=1475,
                hardening_temp_f=1475,
                quench_medium="Fast quench oil (Parks 50 required; canola often fails to beat the 0.8 sec pearlite nose)",
                tempering_range_f="400°F – 450°F (2x 2 hours)",
                target_hardness_hrc="60 – 63 HRC",
                notes="Requires fast quench to avoid soft nose. Demands precise temperature control.",
            ),
            beginner_suitability=False,
            common_applications=["Fine cutting knives", "Straight razors", "Woodworking chisels"],
            common_mistakes=["Slow quench speed produces low hardness; overheating causes brittle retained austenite."],
            source_reference="ASM Handbook Vol 4: Heat Treating",
        ).model_dump(),
    ),
    ContentEnvelope(
        id="mat-5160",
        type=ContentType.MATERIAL,
        title="5160 Spring Steel",
        slug="5160",
        summary="Chromium alloy spring steel (~0.60% C, ~0.80% Cr). Outstanding toughness and impact resistance.",
        category="materials",
        tags=["steel", "spring-steel", "alloy", "high-toughness"],
        difficulty=DifficultyLevel.BEGINNER,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="metallurgy-standard",
            source_name="SAE International Standards",
            source_url="https://www.sae.org",
        ),
        metadata=MaterialMetadata(
            classification="Alloy Spring Steel (AISI 5160)",
            carbon_pct=0.60,
            alloying_elements={"chromium": 0.80, "manganese": 0.85, "silicon": 0.25},
            forging_temp_range_f="1700°F – 2150°F",
            heat_treatment=HeatTreatmentRecipe(
                normalizing_temp_f=1650,
                annealing_temp_f=1525,
                hardening_temp_f=1525,
                quench_medium="Medium quench oil or warmed canola oil (130°F)",
                tempering_range_f="375°F – 425°F for knives, 500°F – 600°F for springs",
                target_hardness_hrc="56 – 59 HRC",
                notes="Deep hardening due to chromium content. Very forgiving during quench.",
            ),
            beginner_suitability=True,
            common_applications=["Large chopping blades", "Swords", "Axes", "Hardy tools", "Leaf springs"],
            common_mistakes=["Forging below red heat induces hidden micro-fissures in alloy matrix."],
            source_reference="SAE Standard J403",
        ).model_dump(),
    ),
]

SEED_PROJECTS: List[ContentEnvelope] = [
    ContentEnvelope(
        id="proj-s-hook",
        type=ContentType.PROJECT,
        title="Classic Blacksmith's S-Hook",
        slug="classic-s-hook",
        summary="The foundation of hand forging: tapers, square-to-round drawing, and smooth horn bends.",
        category="projects",
        tags=["beginner", "fundamentals", "drawing-out", "bending"],
        difficulty=DifficultyLevel.BEGINNER,
        metadata=ProjectMetadata(
            level=1,
            estimated_time_minutes=45,
            required_tools=["Anvil", "2 lb cross-peen hammer", "Tongs", "Wire brush"],
            required_materials=["3/8 inch round or square mild steel (8 inches)"],
            skills_learned=["Square-to-round transition", "Tapering", "Scroll forming over horn"],
            steps=[
                "Heat 3 inches of bar to bright orange heat.",
                "Draw out a clean 4-sided square taper on both ends.",
                "Octagonalize and then round the tapers over the anvil face.",
                "Turn the scroll tips over the far edge of the anvil.",
                "Bend the first loop over the anvil horn to create half the 'S'.",
                "Reverse the bar, bend the opposite loop in the reverse direction.",
                "Wire brush scale vigorously while hot and apply beeswax finish.",
            ],
            safety_warnings=["Always keep tongs cool by quenching between heats."],
        ).model_dump(),
    )
]


SEED_GUIDES: List[ContentEnvelope] = [
    ContentEnvelope(
        id="guide-anvil-selection-mounting",
        type=ContentType.GUIDE,
        title="The Anvil: Anatomy, Selection, Rebound Testing, and Workshop Mounting",
        slug="anvil-anatomy-selection-mounting",
        summary="A comprehensive reference for amateur blacksmiths on anvil anatomy, cast steel vs cast iron identification, ball-bearing rebound testing, and noise-dampened workshop mounting.",
        category="tools",
        tags=["anvil", "tools", "workshop", "rebound", "hardy", "blacksmithing", "equipment"],
        difficulty=DifficultyLevel.BEGINNER,
        status=ContentStatus.PUBLISHED,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="editorial-guild",
            source_name="Blacksmith Knight Guild",
            source_url="https://blacksmithknight.local/guides/anvil-anatomy-selection-mounting",
        ),
        metadata=GuideMetadata(
            reading_time_minutes=12,
            trust_label=TrustLabel.SOURCE_BACKED,
            author="Master Knight Blacksmith",
            version="1.0",
            table_of_contents=[
                {"id": "introduction", "title": "1. Introduction: The Heart of the Forge"},
                {"id": "anatomy", "title": "2. Anvil Anatomy & Geometry"},
                {"id": "materials-construction", "title": "3. Construction: Cast Steel vs. Wrought Iron vs. The ASO Trap"},
                {"id": "rebound-testing", "title": "4. Empirical Testing: The Ball-Bearing Rebound Test"},
                {"id": "acoustic-diagnosis", "title": "5. Acoustic Diagnosis: Ring vs. Thud"},
                {"id": "ergonomics-height", "title": "6. Ergonomics: Determining Proper Anvil Working Height"},
                {"id": "workshop-mounting", "title": "7. Workshop Mounting & Sound Dampening"},
                {"id": "common-mistakes", "title": "8. Fatal Beginner Mistakes"},
            ],
            safety_precautions=[
                SafetyPrecaution(
                    level="critical",
                    hazard="High-Frequency Acoustic Trauma: An un-dampened anvil generates acoustic peaks exceeding 115 dB, leading to permanent inner-ear hair cell damage.",
                    mitigation="Always wear dual hearing protection (NRR 28+ earmuffs over foam plugs) during active striking. Bed the anvil base in a continuous bead of 100% silicone caulk and secure heavy high-tensile link chain around the waist.",
                    ppe=["NRR 28+ Earmuffs or Earplugs", "ANSI Z87.1 Approved Safety Glasses"],
                ),
                SafetyPrecaution(
                    level="warning",
                    hazard="High-Velocity Fragment Ejection: Striking a work-hardened, chipped anvil face edge directly with a hardened hammer face can shatter high-carbon steel shards at bullet velocities.",
                    mitigation="Dress chipped or razor-sharp anvil edges with a smooth 1/8-inch to 3/16-inch radius. Never strike an empty anvil face with full force.",
                    ppe=["ANSI Z87.1 Impact Resistant Eye Protection", "Heavy Split-Cowhide Leather Apron"],
                ),
                SafetyPrecaution(
                    level="caution",
                    hazard="Crush and Musculoskeletal Strain: Transporting or shifting anvils weighing 100 to 300+ lbs causes severe back strain or crushed toes.",
                    mitigation="Employ a two-person lift protocol or mechanical hand truck. Anchor the mounting stand firmly to the floor to prevent tipping during heavy lateral sledging.",
                    ppe=["Steel-Toe Leather Work Boots", "Heavy Leather Work Gloves"],
                ),
            ],
            source_references=[
                SourceReference(
                    title="Anvils in America",
                    author="Richard A. Postman",
                    publication="Postman Publishing",
                    year=1998,
                    url="https://www.anvilfire.com/bookrev/postman/",
                    trust_label=TrustLabel.FACT,
                    citation_key="Postman1998",
                ),
                SourceReference(
                    title="The Complete Modern Blacksmith",
                    author="Alexander G. Weygers",
                    publication="Ten Speed Press",
                    year=1997,
                    url="https://archive.org/details/the-complete-modern-blacksmith",
                    trust_label=TrustLabel.CRAFT_PRACTICE,
                    citation_key="Weygers1997",
                ),
                SourceReference(
                    title="ASM Handbook, Volume 1: Properties and Selection: Irons, Steels, and High-Performance Alloys",
                    author="ASM International Handbook Committee",
                    publication="ASM International",
                    year=1990,
                    url="https://www.asminternational.org",
                    trust_label=TrustLabel.SOURCE_BACKED,
                    citation_key="ASM1990",
                ),
            ],
            related_content=[
                RelatedContentLink(
                    content_id="mat-1084",
                    title="1084 High Carbon Steel",
                    type=ContentType.MATERIAL,
                    slug="1084",
                    relationship="requires_material",
                ),
                RelatedContentLink(
                    content_id="proj-s-hook",
                    title="Classic Blacksmith's S-Hook",
                    type=ContentType.PROJECT,
                    slug="classic-s-hook",
                    relationship="prerequisite_project",
                ),
            ],
            content_markdown="""# The Anvil: Anatomy, Selection, Rebound Testing, and Workshop Mounting

The anvil is the immovable heart of the forge. Every calorie of mechanical energy exerted by your hammer travels through the glowing steel and into the mass of the anvil. If the anvil absorbs that energy like a block of lead, your arm tires quickly, your steel cools before moving, and your forging rhythm suffers. If the anvil returns that energy cleanly, the steel yields with authority.

This technical guide provides amateur blacksmiths with the foundational physics, anatomical nomenclature, diagnostic evaluation techniques, and workshop mounting protocols needed to acquire, test, and mount a lifelong forging partner.

---

## 1. Introduction: The Heart of the Forge

For centuries, an anvil was a craftsman's most expensive capital investment. Today, the modern amateur faces a fractured market ranging from magnificent antique forged wrought-iron anvils with tool-steel plates to premium modern cast-steel tools, down to cheap cast-iron decorative ornaments marketed deceptively as functional shop equipment.

Understanding what makes an anvil functional comes down to three physical principles:
1. **Inertial Mass:** Resisting the impulse of the hammer stroke.
2. **Surface Hardness (HRC):** Preventing indentation and ensuring elastic rebound.
3. **Internal Integrity:** Solid, non-porous structure without voids, cold shuts, or delaminating weld seams.

---

## 2. Anvil Anatomy & Geometry

The London-pattern anvil, standardized in the 19th century, remains the most versatile geometry for the general blacksmith:

```text
┌─────────────────────────────────────────────────────────────┐
│                       THE ANVIL                             │
│                                                             │
│       HORN / BICK      STEP        FACE        HEEL         │
│         ╭─────────╮     ╭─╮ ╭────────────────╮  ╭───╮       │
│        ╱           ╲____│ │ │                │  │ ▢ │Hardy  │
│       ╱                 │ │ │                │  │ O │Pritchel
│      ╱                  ╰─╯ ╰────────────────╯  ╰───╯       │
│     ╰────────────────────┬─────────────────────┬────╯       │
│                          │        WAIST        │            │
│                          │                     │            │
│                      ╭───┴─────────────────────┴───╮        │
│                      │            FEET             │        │
│                      ╰─────────────────────────────╯        │
└─────────────────────────────────────────────────────────────┘
```

- **The Face:** The hardened top working flat (typically 50 to 58 HRC on genuine anvils). This is where 85% of flat drawing, planishing, and squaring occurs.
- **The Horn (Bick):** The conical unhardened horn. Used for drawing curved stock, forming rings, scrolling, and expanding collars. Because it is unhardened, miss-hits here will not chip the horn.
- **The Step (Cutting Table):** The small unhardened shoulder between horn and face. Designed for chisel cutting so hardened cold chisels do not score the hardened face.
- **The Hardy Hole:** The square vertical socket (commonly 3/4", 7/8", or 1" square) positioned through the heel. Holds bottom tooling such as hot cuts, swages, fullers, and bending forks.
- **The Pritchel Hole:** The round hole (typically 1/2" to 5/8") near the end of the heel. Supports stock during punching and drifting operations without allowing the slug to jam.
- **The Waist and Feet:** The structural body that directs impact shock into the foundation. Wide feet provide critical lateral stability against angled blows.

---

## 3. Construction: Cast Steel vs. Wrought Iron vs. The ASO Trap

Before spending money, determine which metallurgical class you are evaluating:

### A. Modern Cast Steel (Top Recommendation)
Cast from 4140, 8640, or proprietary manganese-chromium alloy steels, fully heat treated.
- **Characteristics:** Solid monolithic construction. No weld seams. Superb rebound (80% to 90%+). Clean edges.
- **Examples:** Peddinghaus, Nimba, TFS, Fontanini, Kanca, Atlas.

### B. Antique Forged Wrought Iron with Tool-Steel Plate
The classic 18th to early 20th century construction (e.g. Peter Wright, Mousehole, Trenton, Hay-Budden).
- **Characteristics:** Tough, ductile wrought-iron body forge-welded to a 1/2-inch shear-steel or crucible-steel faceplate.
- **Pros:** Excellent rebound over the central mass.
- **Caution:** Prone to faceplate delamination or heel break-off if abused by heavy sledgehammers.

### C. Cast Ductile / Spheroidal Graphite (SG) Iron
Ductile iron has nodular graphite that provides reasonable toughness compared to gray iron.
- **Characteristics:** Acceptable for beginners on a strict budget, but faces indent more readily (typically 45–50 HRC).

### D. The ASO Trap (Cast Gray Iron)
> [!CAUTION]
> Avoid hardware-store cast iron "anvils" (often cast in gray iron with blue or gray enamel paint). Gray iron contains flake graphite with virtually zero tensile strength. Striking glowing steel on gray iron creates indentations immediately; the horn breaks off under moderate blows; rebound is less than 30%. This is an **Anvil Shaped Object (ASO)**, not a tool for hot steel.

---

## 4. Empirical Testing: The Ball-Bearing Rebound Test

Never purchase a used anvil without performing the **Ball-Bearing Rebound Test** [Postman1998].

### Protocol:
1. Bring a **1-inch steel ball bearing** (standard chrome-steel 52100 bearing) and a 12-inch non-magnetic ruler.
2. Hold the ruler vertically on the center of the anvil face.
3. Drop the bearing freely from the 10-inch mark (do not throw or push down).
4. Measure the height of the first bounce at the apex of its rebound.

```text
Rebound % = (First Bounce Height / Drop Height) × 100
```

### Evaluation Benchmark:
- **80% to 95% (8.0" to 9.5" bounce):** Exceptional. Solid cast steel or pristine welded tool steel face. Maximum energy returned to the workpiece.
- **70% to 79% (7.0" to 7.9" bounce):** Good functional working anvil. Standard for many vintage forged tools.
- **50% to 69% (5.0" to 6.9" bounce):** Marginal. Acceptable for light decorative work, but sluggish under heavy forgings.
- **Under 50% (Under 5.0" bounce):** Soft face or cracked internal body. Reject.
- **Under 30%:** Cast gray iron ASO. Unusable.

> [!TIP]
> Perform the drop test across five distinct zones: near the step, dead center, over the waist, near the hardy hole, and out on the horn. Variation over 20% on the face indicates localized faceplate delamination.

---

## 5. Acoustic Diagnosis: Ring vs. Thud

Acoustics reveal internal structural health:

- **Sustained Bell-like Ring:** Indicates an intact, hardened tool-steel face with zero delamination and no internal cast voids.
- **Dead Dull "Thud":** If localized to one area of the face, indicates the tool-steel faceplate has separated from the wrought iron body beneath. Striking over this "dead spot" will crack the plate.
- **Vulcan / Fisher Anvils Exception:** Fisher & Norris anvils were cast iron with a tool steel face cast in-situ. They are engineered to produce a quiet dead thud rather than a ring, yet yield 75%+ rebound.

---

## 6. Ergonomics: Determining Proper Anvil Working Height

Working at the wrong height causes severe shoulder impingement, tennis elbow (lateral epicondylitis), and lower back spasms.

### The Knuckle Rule (Traditional):
Stand upright in your shop boots with your hands hanging relaxed at your sides. Make a loose fist. The top surface of your anvil face should touch the bottom knuckles of your fist.
- **Best for:** Heavy forging, sledging, drawing out thick stock (2-inch billet or greater).

### The Wrist Rule (Modern Craft / Detail):
The anvil face aligns with the break of your wrist when arms hang loose.
- **Best for:** Bladesmithing, detail scrolling, bevel setting, and planishing where visual inspection of the line is critical.

---

## 7. Workshop Mounting & Sound Dampening

A securely mounted anvil is twice as efficient and vastly quieter than a loose tool.

### Mounting Stand Types:
1. **End-Grain Timber Block:** A solid hardwood log (white oak, elm, or ash) cut square with chainsaw or router sled. Natural grain absorbs shock.
2. **Laminated 4x4 or 2x10 Stand:** Multiple dimensional timbers glued, screwed, and banded together vertically. Consistent, flat, and resistant to splitting.
3. **Steel Tripod Stand:** Fabricated heavy square tubing filled with dry sand or lead shot. Exceptional stability on uneven shop floors.

### Noise Elimination Protocol:
1. Apply a continuous 3/8-inch bed of **100% silicone architectural caulk** between the timber stand and the anvil base before securing. The silicone cures into an elastomeric shock gasket that absorbs acoustic vibrations.
2. Wrap two loops of **3/8-inch welded high-tensile link chain** tightly around the waist, secured with a turnbuckle or heavy neodymium magnet.
3. Place a 100 lb pull-strength ceramic or neodymium magnet under the heel.

> [!NOTE]
> This combined silicone-and-chain protocol routinely reduces anvil strike noise from 118 dB down to 92 dB, transforming an unbearable piercing scream into a tolerable workshop clink.

---

## 8. Fatal Beginner Mistakes

1. **Grinding the Face Flat with an Angle Grinder:** Never use a grinding wheel on an antique anvil face. The hardened faceplate is often only 3/8" thick; grinding removes irreplaceable hardened steel and overheats the temper.
2. **Welding Cold With Ordinary Mild Steel Electrodes:** Arc-welding damaged edges with E6013 or E7018 creates soft divots and introduces thermal shock micro-cracks. Edge repair requires preheating to 450°F and specialized hardfacing rod.
3. **Using Hardened Steel Chisels on the Hardened Face:** Always position chisel cuts over the soft cutting step or use a sacrificial copper or mild steel sheet under the workpiece.
""",
        ).model_dump(),
    ),
    ContentEnvelope(
        id="guide-heat-treatment-fundamentals",
        type=ContentType.GUIDE,
        title="Fundamentals of Heat Treatment: Normalizing, Hardening, and Tempering High-Carbon Steel",
        slug="fundamentals-of-heat-treatment-high-carbon-steel",
        summary="An essential metallurgical handbook explaining the phase transformations of carbon steel, thermal stress cycling, decalescence visual detection, and precision oil quenching.",
        category="heat-treatment",
        tags=["heat-treatment", "metallurgy", "quenching", "tempering", "normalizing", "hardening", "carbon-steel"],
        difficulty=DifficultyLevel.INTERMEDIATE,
        status=ContentStatus.PUBLISHED,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="editorial-guild",
            source_name="Blacksmith Knight Guild",
            source_url="https://blacksmithknight.local/guides/fundamentals-of-heat-treatment-high-carbon-steel",
        ),
        metadata=GuideMetadata(
            reading_time_minutes=14,
            trust_label=TrustLabel.FACT,
            author="Master Metallurgist Knight",
            version="1.0",
            table_of_contents=[
                {"id": "thermal-foundation", "title": "1. The Thermal Foundation"},
                {"id": "phase-transformations", "title": "2. Crystal Phase Transformations"},
                {"id": "decalescence", "title": "3. Decalescence: The Physical Shadow Line"},
                {"id": "normalizing", "title": "4. Thermal Stress Cycling & Grain Refinement"},
                {"id": "the-quench", "title": "5. The Critical Quench: Beating the Pearlite Nose"},
                {"id": "tempering", "title": "6. Stress Relief & Tempering Cycles"},
            ],
            safety_precautions=[
                SafetyPrecaution(
                    level="critical",
                    hazard="Quench Oil Flash Fire: Plunging hot steel (>1500°F) into petroleum or vegetable oil creates flammable vapor plumes prone to immediate flash-back.",
                    mitigation="Always keep a solid steel tank cover nearby to smother oxygen starvation fires instantly. Keep a certified Class B chemical fire extinguisher within 10 feet. Never lean directly over the quench tank.",
                    ppe=["Full Face Shield", "Long Leather Welding Gauntlets", "Heavy Leather Split-Cowhide Apron"],
                ),
            ],
            source_references=[
                SourceReference(
                    title="Knife Engineering: Steel, Heat Treating, and Geometry",
                    author="Dr. Larrin Thomas",
                    publication="Independently Published",
                    year=2020,
                    trust_label=TrustLabel.FACT,
                    citation_key="Thomas2020",
                ),
                SourceReference(
                    title="ASM Handbook Volume 4: Heat Treating",
                    author="ASM International",
                    publication="ASM International",
                    year=1991,
                    trust_label=TrustLabel.SOURCE_BACKED,
                    citation_key="ASM1991",
                ),
            ],
            related_content=[
                RelatedContentLink(
                    content_id="mat-1084",
                    title="1084 High Carbon Steel",
                    type=ContentType.MATERIAL,
                    slug="1084",
                    relationship="requires_material",
                ),
                RelatedContentLink(
                    content_id="mat-1095",
                    title="1095 High Carbon Steel",
                    type=ContentType.MATERIAL,
                    slug="1095",
                    relationship="requires_material",
                ),
            ],
            content_markdown="""# Fundamentals of Heat Treatment: Normalizing, Hardening, and Tempering High-Carbon Steel

Forging shapes the silhouette; heat treatment bestows the soul. You can hammer the most exquisite blade or tool from virgin high-carbon steel, but without sound thermal cycles, it remains either as fragile as glass or as ductile as an old horseshoe nail.

This master guide dissects the physical metallurgy behind the three stages of heat treatment: **Normalizing**, **Hardening (Austenitizing + Quenching)**, and **Tempering**.

---

## 1. The Thermal Foundation

Steel is an iron-carbon alloy. At ambient temperature, carbon steel (like 1084 or 1095) consists of two microscopic phases:
- **Ferrite (Pure Iron):** Ductile, body-centered cubic (BCC) iron crystal lattice.
- **Cementite (Iron Carbide, Fe3C):** An intensely hard, brittle ceramic-like chemical compound.

When combined at the eutectoid ratio (~0.84% Carbon), they arrange in alternating microscopic lamellae known as **Pearlite**. The goal of heat treatment is to dismantle this soft pearlite structure and freeze the carbon inside a strained, razor-hard tetrahedral lattice called **Martensite**.

---

## 2. Crystal Phase Transformations

```text
SOFT FERRITE + CEMENTITE (Room Temp)
          ↓ (Heat past ~1333°F - A1 Critical Temp)
AUSTENITE (Face-Centered Cubic lattice dissolves carbon)
          ↓ (RAPID OIL QUENCH - Cool in under 1 second)
MARTENSITE (Untempered - Glass-brittle, intensely hard, 66+ HRC)
          ↓ (TEMPERING at 400°F - Relieve atomic strain)
TEMPERED MARTENSITE (Tough, resilient, 58–61 HRC cutting edge)
```

---

## 3. Decalescence: The Physical Shadow Line

While modern electric kilns allow exact thermocouple programming, traditional blacksmiths can identify austenitizing visually through **decalescence**.

As steel heats through its Curie point (~1414°F), it loses ferromagnetism. As it passes through the upper critical temperature (~1450°F–1500°F depending on alloy), the internal lattice rearrangement absorbs thermal energy without increasing in temperature.

In a darkened shop, as the steel glows deep red, you will observe a dark, shadowy wave sweep across the steel. This shadow is **decalescence**—the steel absorbing heat to transform into austenite. Once the shadow passes and the color harmonizes into a uniform glowing peach-orange, austenitization is complete.

---

## 4. Thermal Stress Cycling & Grain Refinement

Hammering steel at high yellow temperatures produces coarse, enlarged crystal grains. Large grain boundaries act as fracture highways. Before hardening, you must refine the grain through **Thermal Cycling (Normalizing)**:

1. **Cycle 1 (Structural Reset):** Heat to 1600°F (bright orange). Air cool to black.
2. **Cycle 2 (Grain Refinement):** Heat to 1500°F (mid orange). Air cool to black.
3. **Cycle 3 (Stress Relief):** Heat to 1425°F (dull cherry red). Air cool to room temperature.

With each thermal cycle, fine new austenite nuclei crystallize, shrinking grain size from macroscopic chunks down to ASTM Grain Size 10 or finer, boosting fracture toughness by over 300%.

---

## 5. The Critical Quench: Beating the Pearlite Nose

Once heated to the hardening temperature (~1500°F for 1084), you have approximately **0.8 to 1.0 seconds** to cool the steel below 900°F (the "pearlite nose" on the Time-Temperature-Transformation diagram).

- If cooling is too slow: Carbon escapes and forms soft pearlite.
- If cooling is rapid enough: Carbon is trapped in solution, producing 100% martensite.

### Recommended Quenchants:
- **Parks 50 / Fast Quench Oil:** Formulated for hypereutectoid simple steels (1095, W2) that demand an ultra-fast 7–9 second quench.
- **Warmed Canola / AAA Oil:** Preheated to 130°F (viscosity drops, allowing rapid heat conduction). Ideal for 1084 and 5160 spring steel.

---

## 6. Stress Relief & Tempering Cycles

Freshly quenched martensite is under violent internal atomic shear stress. If dropped onto an anvil, it will shatter like porcelain.

Immediately following the quench (as soon as the blade cools to 125°F and can be handled safely with bare hands), transfer it into a calibrated tempering oven:
- **Temperature:** 400°F to 425°F
- **Duration:** Two cycles of 2 hours each, cooling to room temperature between cycles.
- **Result:** Yields a balanced 59–61 HRC knife edge with maximum toughness and zero catastrophic brittleness.
""",
        ).model_dump(),
    ),
]


async def seed_initial_data(repository: BaseRepository) -> Dict[str, int]:
    """Populates local storage with baseline fixtures."""
    counts = {"materials": 0, "projects": 0, "guides": 0}

    for item in SEED_MATERIALS:
        await repository.create("content", item.id, item.model_dump())
        counts["materials"] += 1

    for item in SEED_PROJECTS:
        await repository.create("content", item.id, item.model_dump())
        counts["projects"] += 1

    for item in SEED_GUIDES:
        await repository.create("content", item.id, item.model_dump())
        counts["guides"] += 1

    return counts

