from typing import Dict, List
from app.models.enums import ContentType, ContentStatus, DifficultyLevel, SourceType, TrustLabel, ToolCategory
from app.models.content import (
    ContentEnvelope,
    MaterialMetadata,
    HeatTreatmentRecipe,
    ProjectMetadata,
    ProjectStep,
    GuideMetadata,
    ToolMetadata,
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
        summary="Eutectoid carbon steel (~0.84% C). Highly forgiving, standard recommendation for beginner knife makers and tool forgers.",
        category="materials",
        tags=["steel", "carbon-steel", "eutectoid", "beginner-friendly", "knife-making"],
        difficulty=DifficultyLevel.BEGINNER,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="metallurgy-standard",
            source_name="ASM International Handbook",
            source_url="https://www.asminternational.org",
        ),
        metadata=MaterialMetadata(
            classification="High Carbon Steel (AISI 1084 / UNS G10840)",
            carbon_pct=0.84,
            alloying_elements={"manganese": 0.75, "phosphorus": 0.03, "sulfur": 0.05},
            steel_category="carbon_steel",
            forging_temp_range_f="1650°F – 2100°F",
            heat_treatment=HeatTreatmentRecipe(
                normalizing_temp_f=1600,
                annealing_temp_f=1450,
                hardening_temp_f=1500,
                decalescence_temp_f=1425,
                soak_time_minutes=5,
                quench_medium="Fast or medium speed quench oil (Parks 50 or warmed canola oil to 130°F)",
                tempering_range_f="400°F – 450°F (2x 2 hours)",
                target_hardness_hrc="58 – 61 HRC",
                tempering_table=[
                    {"temp_f": 375, "hrc": "61", "toughness": "medium", "color": "pale_straw"},
                    {"temp_f": 400, "hrc": "60", "toughness": "high", "color": "straw"},
                    {"temp_f": 450, "hrc": "58", "toughness": "maximum", "color": "dark_straw"},
                ],
                notes="Simple thermal cycle: soak at 1500°F for 5 minutes, quench immediately, temper twice.",
            ),
            spark_testing_profile="Dense burst of moderately branching sparks with bright yellow starbursts close to the grinding wheel.",
            grinding_characteristics="Grinds cleanly with ceramic and aluminum oxide belts; low burr formation.",
            weldability="High forge weldability; standard partner with 15N20 in Damascus billets.",
            corrosion_resistance="Low (develops natural patina; protect with mineral or camellia oil).",
            confidence_score=0.99,
            confidence_level="handbook_verified",
            beginner_suitability=True,
            common_applications=["Hand-forged knives", "Punches", "Drifts", "Small hand tools", "Wood carving gouges"],
            common_mistakes=["Overheating in forge past bright yellow heat causes rapid austenite grain growth."],
            source_reference="ASM Handbook Vol 1: Properties and Selection of Irons, Steels, and High-Performance Alloys",
            source_metadata={"standard": "AISI/SAE 1084", "uns": "G10840", "source_publisher": "ASM International"},
        ).model_dump(),
    ),
    ContentEnvelope(
        id="mat-1095",
        type=ContentType.MATERIAL,
        title="1095 High Carbon Steel",
        slug="1095",
        summary="Hypereutectoid carbon steel (~0.95% C). Exceptional edge retention and hamon line activity, but requires fast oil quench.",
        category="materials",
        tags=["steel", "high-carbon", "hypereutectoid", "hamon", "razor"],
        difficulty=DifficultyLevel.INTERMEDIATE,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="metallurgy-standard",
            source_name="ASM International Handbook",
            source_url="https://www.asminternational.org",
        ),
        metadata=MaterialMetadata(
            classification="High Carbon Steel (AISI 1095 / UNS G10950)",
            carbon_pct=0.95,
            alloying_elements={"manganese": 0.40, "phosphorus": 0.03, "sulfur": 0.05},
            steel_category="carbon_steel",
            forging_temp_range_f="1600°F – 2050°F",
            heat_treatment=HeatTreatmentRecipe(
                normalizing_temp_f=1650,
                annealing_temp_f=1475,
                hardening_temp_f=1475,
                decalescence_temp_f=1450,
                soak_time_minutes=5,
                quench_medium="Fast quench oil (Parks 50 required; canola often fails to beat the 0.8 sec nose)",
                tempering_range_f="400°F – 450°F (2x 2 hours)",
                target_hardness_hrc="60 – 63 HRC",
                tempering_table=[
                    {"temp_f": 400, "hrc": "62", "toughness": "medium", "color": "straw"},
                    {"temp_f": 450, "hrc": "60", "toughness": "high", "color": "dark_straw"},
                    {"temp_f": 500, "hrc": "57", "toughness": "maximum", "color": "purple"},
                ],
                notes="Requires fast quench to avoid soft nose. Demands precise temperature control.",
            ),
            spark_testing_profile="Brilliant, highly complex fireworks-like starburst explosions with very high density of spark breaks.",
            grinding_characteristics="Grinds cleanly, but highly sensitive to temper burnout; keep water dunk bucket adjacent.",
            weldability="Moderate; demands clean forge atmospheres and high temperature to avoid weld inclusions.",
            corrosion_resistance="Low; patinas rapidly in acidic food contact.",
            confidence_score=0.98,
            confidence_level="handbook_verified",
            beginner_suitability=False,
            common_applications=["Fine cutting knives", "Straight razors", "Woodworking chisels", "Kitchen cutlery"],
            common_mistakes=["Slow quench speed produces soft pearlite nose; overheating causes brittle retained austenite."],
            source_reference="ASM Handbook Vol 4: Heat Treating",
            source_metadata={"standard": "AISI 1095", "uns": "G10950"},
        ).model_dump(),
    ),
    ContentEnvelope(
        id="mat-5160",
        type=ContentType.MATERIAL,
        title="5160 Spring Steel",
        slug="5160",
        summary="Chromium alloy spring steel (~0.60% C, ~0.80% Cr). Outstanding toughness, deep hardenability, and shock resistance.",
        category="materials",
        tags=["steel", "spring-steel", "alloy", "high-toughness", "choppers"],
        difficulty=DifficultyLevel.BEGINNER,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="metallurgy-standard",
            source_name="SAE International Standards",
            source_url="https://www.sae.org",
        ),
        metadata=MaterialMetadata(
            classification="Alloy Spring Steel (AISI 5160 / UNS G51600)",
            carbon_pct=0.60,
            alloying_elements={"chromium": 0.80, "manganese": 0.85, "silicon": 0.25},
            steel_category="spring_steel",
            forging_temp_range_f="1700°F – 2150°F",
            heat_treatment=HeatTreatmentRecipe(
                normalizing_temp_f=1650,
                annealing_temp_f=1525,
                hardening_temp_f=1525,
                decalescence_temp_f=1475,
                soak_time_minutes=5,
                quench_medium="Medium quench oil or warmed canola oil (130°F)",
                tempering_range_f="375°F – 425°F for knives, 500°F – 600°F for springs",
                target_hardness_hrc="56 – 59 HRC",
                tempering_table=[
                    {"temp_f": 375, "hrc": "60", "toughness": "high", "color": "pale_straw"},
                    {"temp_f": 425, "hrc": "58", "toughness": "very_high", "color": "straw"},
                    {"temp_f": 500, "hrc": "55", "toughness": "maximum", "color": "purple"},
                ],
                notes="Deep hardening due to chromium content. Extremely forgiving during quench.",
            ),
            spark_testing_profile="Longer orange carrier lines with moderate bursts, distinctive curved reddish tails due to chromium.",
            grinding_characteristics="Slightly more belt wear than plain carbon steel; smooth surface finish.",
            weldability="Moderate; chromium forms stubborn refractory oxides, requiring anhydrous borax flux.",
            corrosion_resistance="Moderate-low (improved over plain carbon steel by chromium addition).",
            confidence_score=0.96,
            confidence_level="handbook_verified",
            beginner_suitability=True,
            common_applications=["Large chopping blades", "Swords", "Camp axes", "Hardy tools", "Leaf springs"],
            common_mistakes=["Forging below dull red heat introduces hidden micro-fissures in alloy matrix."],
            source_reference="SAE Standard J403 & ASM Handbook Vol 1",
            source_metadata={"standard": "AISI/SAE 5160", "uns": "G51600"},
        ).model_dump(),
    ),
    ContentEnvelope(
        id="mat-o1",
        type=ContentType.MATERIAL,
        title="O1 Tool Steel",
        slug="o1",
        summary="Oil-hardening cold work tool steel (~0.90% C, with W, V, Cr). Renowned for dimensional stability, wear resistance, and clean keeness.",
        category="materials",
        tags=["steel", "tool-steel", "oil-hardening", "precision", "high-wear"],
        difficulty=DifficultyLevel.INTERMEDIATE,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="metallurgy-standard",
            source_name="AISI Tool Steel Specifications",
            source_url="https://www.astm.org",
        ),
        metadata=MaterialMetadata(
            classification="Oil-Hardening Cold Work Tool Steel (AISI O1 / UNS T31501)",
            carbon_pct=0.90,
            alloying_elements={"manganese": 1.20, "chromium": 0.50, "tungsten": 0.50, "vanadium": 0.20, "silicon": 0.30},
            steel_category="tool_steel",
            forging_temp_range_f="1800°F – 2050°F",
            heat_treatment=HeatTreatmentRecipe(
                normalizing_temp_f=1600,
                annealing_temp_f=1450,
                hardening_temp_f=1485,
                decalescence_temp_f=1460,
                soak_time_minutes=10,
                quench_medium="Medium-speed quench oil (warmed to 125°F – 140°F). NEVER water quench.",
                tempering_range_f="350°F – 450°F (2x 2 hours)",
                target_hardness_hrc="60 – 62 HRC",
                tempering_table=[
                    {"temp_f": 350, "hrc": "62", "toughness": "medium", "color": "pale_straw"},
                    {"temp_f": 400, "hrc": "60", "toughness": "high", "color": "straw"},
                    {"temp_f": 450, "hrc": "58", "toughness": "maximum", "color": "dark_straw"},
                ],
                notes="Soak at 1485°F for 10 minutes to dissolve tungsten and vanadium carbides into austenite.",
            ),
            spark_testing_profile="Dark orange/reddish carrier lines with short, bushy bursts and tiny star points.",
            grinding_characteristics="Holds sharp dimensions exceptionally well with minimal wheel loading.",
            weldability="Difficult in forge; sensitive to hot cracking below 1800°F.",
            corrosion_resistance="Low; requires mineral oil or paste wax protection.",
            confidence_score=0.97,
            confidence_level="handbook_verified",
            beginner_suitability=False,
            common_applications=["Woodworking chisels", "Planer blades", "Hardy hot-cuts", "Punches", "Precision knives"],
            common_mistakes=["Quenching without required soak time results in incomplete carbide dissolution and soft matrix."],
            source_reference="ASTM A681 Standard Specification for Tool Steels & ASM Handbook Vol 16",
            source_metadata={"standard": "ASTM A681 / AISI O1", "uns": "T31501"},
        ).model_dump(),
    ),
    ContentEnvelope(
        id="mat-w1",
        type=ContentType.MATERIAL,
        title="W1 Tool Steel",
        slug="w1",
        summary="Water/fast-oil hardening simple carbon tool steel (~1.00% C). Creates shallow hardening with tough core and intense razor hardness.",
        category="materials",
        tags=["steel", "tool-steel", "shallow-hardening", "hamon", "high-carbon"],
        difficulty=DifficultyLevel.BEGINNER,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="metallurgy-standard",
            source_name="ASTM Tool Steel Standards",
            source_url="https://www.astm.org",
        ),
        metadata=MaterialMetadata(
            classification="Water-Hardening Carbon Tool Steel (AISI W1 / UNS T72301)",
            carbon_pct=1.00,
            alloying_elements={"manganese": 0.25, "silicon": 0.20},
            steel_category="tool_steel",
            forging_temp_range_f="1650°F – 2050°F",
            heat_treatment=HeatTreatmentRecipe(
                normalizing_temp_f=1600,
                annealing_temp_f=1450,
                hardening_temp_f=1460,
                decalescence_temp_f=1440,
                soak_time_minutes=5,
                quench_medium="Fast quench oil (Parks 50) or agitated brine for thick cross sections",
                tempering_range_f="350°F – 450°F (2x 2 hours)",
                target_hardness_hrc="62 – 64 HRC",
                tempering_table=[
                    {"temp_f": 350, "hrc": "64", "toughness": "medium", "color": "pale_straw"},
                    {"temp_f": 400, "hrc": "62", "toughness": "high", "color": "straw"},
                    {"temp_f": 450, "hrc": "59", "toughness": "maximum", "color": "dark_straw"},
                ],
                notes="Shallow hardening depth creates a shock-absorbing unhardened core with glass-hard case.",
            ),
            spark_testing_profile="Intense, blinding white fireworks starburst cluster directly off the wheel.",
            grinding_characteristics="Fast stock removal, clean edge definition, easy to dress.",
            weldability="High forge weldability; forge welds cleanly at bright yellow heat.",
            corrosion_resistance="Low; highly reactive carbon surface.",
            confidence_score=0.96,
            confidence_level="handbook_verified",
            beginner_suitability=True,
            common_applications=["Punches", "Drifts", "Center punches", "Cold chisels", "Straight razors", "Files"],
            common_mistakes=["Over-soaking or overheating past 1500°F causes rapid grain coarsening and brittleness."],
            source_reference="ASTM A686 Standard Specification for Tool Steel, Carbon",
            source_metadata={"standard": "ASTM A686 / AISI W1", "uns": "T72301"},
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
            difficulty_level=DifficultyLevel.BEGINNER,
            estimated_time_minutes=45,
            required_tools=["Anvil", "2 lb cross-peen hammer", "Tongs", "Wire brush"],
            required_materials=["3/8 inch round or square mild steel (8 inches)"],
            skills_learned=["Square-to-round transition", "Tapering", "Scroll forming over horn"],
            steps=[
                ProjectStep(title="Heating", description="Heat 3 inches of bar to bright orange heat.", duration_minutes=5),
                ProjectStep(title="Tapering", description="Draw out a clean 4-sided square taper on both ends.", duration_minutes=10),
                ProjectStep(title="Rounding", description="Octagonalize and then round the tapers over the anvil face.", duration_minutes=5),
                ProjectStep(title="Scrolling", description="Turn the scroll tips over the far edge of the anvil.", duration_minutes=5),
                ProjectStep(title="Bending 1", description="Bend the first loop over the anvil horn to create half the 'S'.", duration_minutes=10),
                ProjectStep(title="Bending 2", description="Reverse the bar, bend the opposite loop in the reverse direction.", duration_minutes=5),
                ProjectStep(title="Finishing", description="Wire brush scale vigorously while hot and apply beeswax finish.", duration_minutes=5),
            ],
            safety_precautions=[
                SafetyPrecaution(
                    level="warning",
                    hazard="Hot tongs can burn the hand.",
                    mitigation="Always keep tongs cool by quenching between heats.",
                    ppe=["Leather gloves"]
                )
            ],
            troubleshooting=["If the S-hook is uneven, re-heat and adjust the loops over the horn. Keep material at forging temp."],
            variations=["Add a twisted center section", "Reverse the scrolls"],
            source_references=[]
        ).model_dump(),
    ),
    ContentEnvelope(
        id="proj-wolf-jaw-tongs",
        type=ContentType.PROJECT,
        title="Forging Wolf Jaw Tongs",
        slug="wolf-jaw-tongs",
        summary="An essential intermediate project: forging a pair of versatile wolf jaw tongs from medium carbon steel.",
        category="projects",
        tags=["intermediate", "tongs", "tool-making", "riveting"],
        difficulty=DifficultyLevel.INTERMEDIATE,
        metadata=ProjectMetadata(
            difficulty_level=DifficultyLevel.INTERMEDIATE,
            estimated_time_minutes=180,
            required_tools=["Anvil", "2.5 lb cross-peen hammer", "Tongs", "Rivet buck", "Punch or drill"],
            required_materials=["5/8 inch round or square 1045 or mild steel (two 18-inch pieces)", "1/4 inch mild steel rivet"],
            skills_learned=["Isolating mass", "Forging the boss", "Drawing out reins", "Riveting"],
            steps=[
                ProjectStep(title="Isolating the boss", description="Set down half the material on the near edge of the anvil.", duration_minutes=15),
                ProjectStep(title="Forging the jaw", description="Draw out the jaw and shape it with a V-notch or fuller.", duration_minutes=30),
                ProjectStep(title="Drawing the reins", description="Draw out the long handles (reins) smoothly and evenly.", duration_minutes=45),
                ProjectStep(title="Punching the hole", description="Hot punch a 1/4 inch hole through the center of the boss.", duration_minutes=15),
                ProjectStep(title="Riveting", description="Align both halves, insert the rivet, and upset the rivet hot.", duration_minutes=15),
                ProjectStep(title="Adjusting", description="Heat the jaws and grab the stock you intend to hold to set the jaw shape.", duration_minutes=10),
            ],
            safety_precautions=[
                SafetyPrecaution(
                    level="warning",
                    hazard="Misaligned hammer strikes during riveting can send the rivet flying.",
                    mitigation="Ensure flat, deliberate strikes when upsetting the rivet.",
                    ppe=["Safety glasses"]
                )
            ],
            troubleshooting=["If tongs are stiff, heat the rivet joint to a dull red and work them open and closed until cool."],
            variations=["Flat jaws", "V-bit jaws"],
            source_references=[]
        ).model_dump(),
    ),
    ContentEnvelope(
        id="proj-camp-knife",
        type=ContentType.PROJECT,
        title="Forging a High Carbon Camp Knife",
        slug="camp-knife",
        summary="A comprehensive advanced project: forging, heat treating, and finishing a rugged camp knife from 1084 steel.",
        category="projects",
        tags=["advanced", "bladesmithing", "knife-making", "heat-treatment"],
        difficulty=DifficultyLevel.ADVANCED,
        metadata=ProjectMetadata(
            difficulty_level=DifficultyLevel.ADVANCED,
            estimated_time_minutes=480,
            required_tools=["Anvil", "Hammer", "Tongs", "Belt grinder or files", "Quench tank", "Oven for tempering"],
            required_materials=["1084 high carbon steel bar", "Quench oil (Parks 50 or canola)", "Handle material (wood/micarta)", "Epoxy and pins"],
            skills_learned=["Forging bevels", "Distal taper", "Normalizing", "Quenching", "Tempering", "Handle fitting"],
            steps=[
                ProjectStep(title="Forging the tip", description="Forge the tip down to shape.", duration_minutes=20),
                ProjectStep(title="Forging bevels", description="Hammer in the edge bevels, being careful to keep the spine straight.", duration_minutes=60),
                ProjectStep(title="Forging the tang", description="Isolate and draw out the tang for the handle.", duration_minutes=30),
                ProjectStep(title="Normalizing", description="Heat to non-magnetic and let air cool three times for grain refinement.", duration_minutes=45),
                ProjectStep(title="Quenching", description="Heat evenly to critical temp (1500°F) and plunge vertically into warm quench oil.", duration_minutes=10),
                ProjectStep(title="Tempering", description="Temper in an oven at 400°F for two cycles of 2 hours each.", duration_minutes=240),
                ProjectStep(title="Grinding and Finishing", description="Grind the final edge, attach handle scales, and shape handle.", duration_minutes=120),
            ],
            safety_precautions=[
                SafetyPrecaution(
                    level="critical",
                    hazard="Oil quench fire flare-up.",
                    mitigation="Always have a tight-fitting lid nearby to smother flames. Never use water to extinguish oil fires.",
                    ppe=["Leather apron", "Respirator", "Safety glasses", "Fire extinguisher"]
                )
            ],
            troubleshooting=["If the blade warps during quench, straighten during tempering or using a specialized straightening jig.", "If file bites after quench, the blade didn't harden; re-normalize and try again."],
            variations=["Hidden tang", "Drop point vs clip point"],
            source_references=[]
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

SEED_TOOLS: List[ContentEnvelope] = [
    ContentEnvelope(
        id="tool-london-pattern-anvil",
        type=ContentType.TOOL,
        title="London-Pattern Cast Steel Anvil",
        slug="london-pattern-anvil",
        summary="The definitive blacksmithing foundation. Features a hardened continuous face, conical horn for scrolling, cutting step, square hardy hole, and round pritchel hole.",
        category="workshop",
        tags=["anvil", "forging", "london-pattern", "foundation", "hardy", "rebound"],
        difficulty=DifficultyLevel.BEGINNER,
        status=ContentStatus.PUBLISHED,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="workshop-guild",
            source_name="Blacksmith Knight Guild",
            source_url="https://blacksmithknight.local/workshop/london-pattern-anvil",
        ),
        metadata=ToolMetadata(
            tool_category=ToolCategory.FORGING,
            primary_purpose="The primary rebound mass and striking anvil upon which glowing steel is forged, drawn, bent, and planished.",
            essential_for=["Drawing out bar stock", "Upsetting tenons and shoulders", "Forming rings on the horn", "Holding bottom hardy tooling"],
            selection_criteria=[
                "Monolithic cast alloy steel (4140, 8640) or forged wrought body with forge-welded tool steel faceplate.",
                "Empirical ball-bearing rebound score of 75% to 90%+ across the central mass.",
                "Unbroken, crisp edges with gentle 1/8-inch dressing radius (avoid chipped or jagged corners).",
                "Clear, sustained bell-like ring indicating zero internal delamination voids.",
            ],
            beginner_guidance="For a personal workshop, target an anvil between 100 and 150 lbs (45–70 kg). Never buy hardware-store cast gray iron 'Anvil Shaped Objects' (ASOs)—gray iron shatters and has under 30% rebound.",
            beginner_friendly=True,
            diy_buildable=False,
            diy_alternatives=[
                "Vertical railroad track section (mounted on end so the entire head mass sits directly beneath hammer blows)",
                "Solid 4140 forklift tine billet cut to 18 inches and embedded into end-grain timber",
                "100 lb steel crane rail or drop-forge die block",
            ],
            maintenance_protocols=[
                "Never grind an antique face flat with an abrasive grinding cup; you will overheat and destroy the paper-thin temper.",
                "Dress working edges with an 80-grit flap disc to establish smooth 1/8-inch to 3/16-inch blending radii.",
                "Bed the base in 100% silicone architectural caulk and wrap chains around the waist to eliminate deafening 118 dB ring.",
            ],
            safety_precautions=[
                SafetyPrecaution(
                    level="critical",
                    hazard="High-velocity spalling steel chips: Striking a hardened hammer directly against a hardened anvil face can shatter glass-hard steel shards at bullet velocity.",
                    mitigation="Never strike the anvil face directly with a steel hammer without glowing hot workpiece in between. Use soft brass, copper, or mild steel drifts.",
                    ppe=["ANSI Z87.1 Approved Safety Glasses with Side Shields", "Full Face Shield for heavy striking"],
                ),
                SafetyPrecaution(
                    level="warning",
                    hazard="Deafening high-frequency acoustic shock: Bare anvil strikes exceed 115 dB, causing irreversible sensorineural hearing loss within minutes.",
                    mitigation="Mount on silicone caulk bed, wrap waist tightly with link chain, and wear certified hearing protection.",
                    ppe=["NRR 28+ dB Earmuffs or Molded Silicone Earplugs"],
                ),
            ],
            specifications={
                "optimal_weight_lbs": "110 – 160 lbs for amateur home forge, 250+ lbs for two-person striking",
                "face_hardness": "54 – 58 HRC on high-grade cast steel",
                "hardy_hole_size": "Standard 1.0 inch (or 3/4 inch on European patterns)",
                "pritchel_hole_size": "1/2 inch to 5/8 inch cylindrical hole",
                "working_height": "Knuckle height rule: top of face aligns with bottom of closed fist standing in shop boots",
            },
            related_tools=[
                RelatedContentLink(
                    content_id="tool-cross-peen-hammer",
                    title="Swedish Cross-Peen Blacksmith Hammer",
                    type=ContentType.TOOL,
                    slug="cross-peen-hammer",
                    relationship="recommended_tool",
                ),
                RelatedContentLink(
                    content_id="tool-blacksmith-leg-vise",
                    title="Solid Wrought-Iron Post Leg Vise",
                    type=ContentType.TOOL,
                    slug="blacksmith-leg-vise",
                    relationship="prerequisite_project",
                ),
            ],
            source_references=[
                SourceReference(
                    title="Anvils in America",
                    author="Richard A. Postman",
                    publication="Postman Publishing",
                    year=1998,
                    trust_label=TrustLabel.FACT,
                    citation_key="Postman1998",
                ),
            ],
        ).model_dump(),
    ),
    ContentEnvelope(
        id="tool-cross-peen-hammer",
        type=ContentType.TOOL,
        title="Swedish Cross-Peen Blacksmith Hammer",
        slug="cross-peen-hammer",
        summary="The fundamental forging hammer for every blacksmith. The crowned square face provides clean planishing while the horizontal wedge peen draws hot steel outward directionally.",
        category="workshop",
        tags=["hammer", "forging", "cross-peen", "swedish-pattern", "hand-tool"],
        difficulty=DifficultyLevel.BEGINNER,
        status=ContentStatus.PUBLISHED,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="workshop-guild",
            source_name="Blacksmith Knight Guild",
            source_url="https://blacksmithknight.local/workshop/cross-peen-hammer",
        ),
        metadata=ToolMetadata(
            tool_category=ToolCategory.FORGING,
            primary_purpose="The hand extension that converts physical arm energy into directed plastic deformation of hot incandescent metal.",
            essential_for=["Directional drawing out of billets", "Planishing hammer marks smooth", "Forging bevels and tapers", "Fullering and texturing"],
            selection_criteria=[
                "Weight between 2.0 and 2.5 lbs (0.9 to 1.1 kg) for general forging and joint longevity.",
                "Drop-forged medium carbon or alloy steel (1045 or 4140), differentially hardened with faces at 50–55 HRC.",
                "Straight-grain hickory or ash handle with grain running parallel to the line of strike.",
                "Both wooden wedge and cross metal wedge securing the eye firmly.",
            ],
            beginner_guidance="Resist the urge to forge with a 3.5 or 4 lb sledge hammer as a beginner. A 2.2 lb hammer swinging rhythmically with gravity will move metal faster and save you from crippling elbow tendonitis.",
            beginner_friendly=True,
            diy_buildable=True,
            diy_alternatives=[
                "Dressed 2.5 lb engineer's drilling hammer with ground radius",
                "Ball-peen machinist hammer (16 oz to 24 oz) for small decorative work",
                "Repurposed vintage sledgehammer head reshaped on the forge",
            ],
            maintenance_protocols=[
                "Crown the square face: radius the sharp outer edges to prevent cutting crescent scars ('half-moons') into the workpiece.",
                "Sand the handle clean of factory polyurethane varnish; wipe with boiled linseed oil to prevent hand blisters.",
                "Inspect the eye wedge before every heat; soak in linseed oil or replace wood wedge if the head exhibits slight play.",
            ],
            safety_precautions=[
                SafetyPrecaution(
                    level="warning",
                    hazard="Mushroomed edges chipping off hammer face: Hardened tool steel striking mushroomed rims sends razor fragments flying.",
                    mitigation="Immediately dress any mushroomed edges on a grinder before beginning forging operations.",
                    ppe=["ANSI Z87.1 Safety Glasses", "Sturdy Natural-Fiber Workshop Attire"],
                ),
            ],
            specifications={
                "recommended_head_weight": "2.0 – 2.5 lbs (1000g)",
                "face_geometry": "Slightly crowned square flat with blended radiused perimeter",
                "peen_geometry": "Horizontal cross-peen with 1/8-inch smooth contact crown",
                "handle_length": "14 to 16 inches",
                "handle_wood": "Flame-treated second-growth American Hickory",
            },
            related_tools=[
                RelatedContentLink(
                    content_id="tool-london-pattern-anvil",
                    title="London-Pattern Cast Steel Anvil",
                    type=ContentType.TOOL,
                    slug="london-pattern-anvil",
                    relationship="recommended_tool",
                ),
            ],
            source_references=[
                SourceReference(
                    title="The Blacksmith's Craft",
                    author="Charles McRaven",
                    publication="Storey Publishing",
                    year=2005,
                    trust_label=TrustLabel.CRAFT_PRACTICE,
                    citation_key="McRaven2005",
                ),
            ],
        ).model_dump(),
    ),
    ContentEnvelope(
        id="tool-2x72-belt-grinder",
        type=ContentType.TOOL,
        title="2x72 Variable Speed Industrial Belt Grinder",
        slug="2x72-belt-grinder",
        summary="The undisputed powerhouse of modern bladesmithing and tool fabrication. Rapidly profiles billets, bevels blades, hollow grinds, and cleans scale with ceramic abrasive belts.",
        category="workshop",
        tags=["grinder", "grinding", "2x72", "abrasives", "profiling", "beveling"],
        difficulty=DifficultyLevel.INTERMEDIATE,
        status=ContentStatus.PUBLISHED,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="workshop-guild",
            source_name="Blacksmith Knight Guild",
            source_url="https://blacksmithknight.local/workshop/2x72-belt-grinder",
        ),
        metadata=ToolMetadata(
            tool_category=ToolCategory.GRINDING,
            primary_purpose="Precision stock removal, bevel geometry shaping, scale grinding, and satin abrasive finishing of heat-treated blades and forged tools.",
            essential_for=["Hogging forge scale from normalized stock", "Precision flat and hollow bevel grinding", "Handle contouring and shaping", "Post-heat-treat finish grinding"],
            selection_criteria=[
                "Minimum 2.0 HP industrial TEFC (Totally Enclosed Fan Cooled) motor to resist metallic dust short-circuits.",
                "Variable Frequency Drive (VFD) offering smooth control from 400 to 4500+ Surface Feet Per Minute (SFPM).",
                "Solid tooling arm system accommodating flat platens, small wheel attachments, and contact wheels (8 to 10 inch).",
                "Quick-release gas-strut or tension spring for rapid 2-second belt changes.",
            ],
            beginner_guidance="A 2x72 grinder is an investment. If budget is tight, begin with a 1x30 or 2x42 grinder, or master high-quality bastard cut mill files before investing in a high-power industrial machine.",
            beginner_friendly=False,
            diy_buildable=True,
            diy_alternatives=[
                "DIY welded steel chassis kit (e.g. Revolution, KMG clone, or Gen-2 grinder kits)",
                "2x42 belt and 6-inch disc sander with upgraded ceramic belts",
                "Quality 14-inch mill bastard file with draw filing wooden jig",
            ],
            maintenance_protocols=[
                "Vacuum aluminum tracking wheels and platen daily; metal dust accumulation creates belt tracking wobble.",
                "True the platen liner: replace worn ceramic platen glass when grooves exceed 0.010 inches.",
                "Blow out the motor housing periodically with dry compressed air.",
            ],
            safety_precautions=[
                SafetyPrecaution(
                    level="critical",
                    hazard="Toxic Inhalation Hazard: Inhaling airborne metal swarf, toxic alloying oxides (chromium, manganese), and ceramic abrasive particles causes irreversible lung damage and silicosis.",
                    mitigation="Mandatory tight-fitting NIOSH P100 or N95 half-mask respirator during all grinding operations. Install spark-trap water trough below grinding wheel.",
                    ppe=["NIOSH P100 Half-Mask Respirator", "Full Polycarbonate Face Shield (ANSI Z87+)", "Ear Protection (grinder whine exceeds 95 dB)"],
                ),
                SafetyPrecaution(
                    level="critical",
                    hazard="Rotational entanglement hazard: Wearing loose gloves near a 4000 SFPM abrasive belt can grab fingers into the contact pinch point instantly.",
                    mitigation="Never wear loose cloth gloves or dangling clothing when operating rotating belt grinders. Keep fingers clear of pinch zones.",
                    ppe=["Tight-fitting workshop leather apron", "Tied-back hair"],
                ),
            ],
            specifications={
                "motor_power": "2.0 to 3.0 HP 3-phase motor with single-phase VFD converter",
                "belt_size": "2 inches wide × 72 inches long (industry standard)",
                "speed_range": "400 to 5000 Surface Feet Per Minute (SFPM)",
                "platen_type": "Hardened tool steel or ceramic glass-faced 8-inch flat platen",
            },
            related_tools=[
                RelatedContentLink(
                    content_id="tool-cross-peen-hammer",
                    title="Swedish Cross-Peen Blacksmith Hammer",
                    type=ContentType.TOOL,
                    slug="cross-peen-hammer",
                    relationship="related_technique",
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
            ],
        ).model_dump(),
    ),
    ContentEnvelope(
        id="tool-atmospheric-propane-forge",
        type=ContentType.TOOL,
        title="Atmospheric Dual-Burner Propane Forge",
        slug="atmospheric-propane-forge",
        summary="A clean, versatile heating chamber powered by LPG/propane venturi burners. Capable of consistent thermal control up to 2400°F for general forging and solid-state forge welding.",
        category="workshop",
        tags=["forge", "heating", "propane", "burner", "insulation", "refractory"],
        difficulty=DifficultyLevel.BEGINNER,
        status=ContentStatus.PUBLISHED,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="workshop-guild",
            source_name="Blacksmith Knight Guild",
            source_url="https://blacksmithknight.local/workshop/atmospheric-propane-forge",
        ),
        metadata=ToolMetadata(
            tool_category=ToolCategory.HEATING,
            primary_purpose="Heats steel billets to forging temperature (1600°F–2150°F) in a controllable atmospheric fire without producing coal smoke or sulfur contamination.",
            essential_for=["Heating bar stock uniformly", "Thermal cycle soaking for normalization and hardening", "Damascus billet forge welding"],
            selection_criteria=[
                "High-density ceramic blanket insulation (minimum 2-inch thickness, 8 lb/cu ft rating).",
                "Insulation rigidized with colloidal silica and sealed with high-temperature refractory mortar (e.g. Satanite or Kast-O-Lite 30).",
                "Adjustable air choke plates on atmospheric venturi burners for managing oxidation scale.",
                "UL-certified high-pressure propane regulator (0–30 PSI) with braided stainless steel line.",
            ],
            beginner_guidance="Ensure your propane forge has pass-through doors at both front and back so you can heat long bars anywhere along their length. Always keep a refractory firebrick on the chamber floor to catch flux.",
            beginner_friendly=True,
            diy_buildable=True,
            diy_alternatives=[
                "Single-burner 'coffee can' mini-forge for small knives and punches",
                "Brake-drum coal forge built with black iron plumbing pipes and hair dryer blower",
                "Refractory firebrick chamber with handheld MAPP gas torch",
            ],
            maintenance_protocols=[
                "Inspect ceramic fiber lining: patch any flaking mortar immediately with damp Satanite to prevent airborne fiber release.",
                "Perform soapy bubble leak tests on all brass gas fittings before turning on tank valves.",
                "Clean burner nozzles of insect nests and carbon soot every season.",
            ],
            safety_precautions=[
                SafetyPrecaution(
                    level="critical",
                    hazard="Ceramic fiber inhalation (Refractory Ceramic Fiber Fibrosis): Exposed, unsealed ceramic blanket sheds microscopic needles that permanently lodge in lung alveoli.",
                    mitigation="Never operate a forge with exposed ceramic fiber. Coat 100% of internal insulation in rigidizer and refractory wash.",
                    ppe=["NIOSH N95 / P100 Respirator", "Long Leather Welding Gauntlets"],
                ),
                SafetyPrecaution(
                    level="critical",
                    hazard="Carbon Monoxide (CO) poisoning: Combustion consumed indoors exhausts deadly odorless CO gas.",
                    mitigation="Operate only with roll-up doors open or dedicated fume exhaust hood. Install digital CO alarm at waist level.",
                    ppe=["Digital Carbon Monoxide Alarm within 6 feet"],
                ),
            ],
            specifications={
                "burner_type": "2× 3/4-inch Venturi atmospheric burners with brass 0.035 Mig contact tips",
                "maximum_operating_temp": "2350°F – 2450°F",
                "fuel_consumption": "1.5 to 2.5 lbs LPG per hour at 8 PSI",
                "insulation_type": "2-inch 2600°F Ceramic Fiber sealed with Satanite",
            },
            related_tools=[
                RelatedContentLink(
                    content_id="tool-london-pattern-anvil",
                    title="London-Pattern Cast Steel Anvil",
                    type=ContentType.TOOL,
                    slug="london-pattern-anvil",
                    relationship="recommended_tool",
                ),
                RelatedContentLink(
                    content_id="tool-cross-peen-hammer",
                    title="Swedish Cross-Peen Blacksmith Hammer",
                    type=ContentType.TOOL,
                    slug="cross-peen-hammer",
                    relationship="recommended_tool",
                ),
            ],
            source_references=[
                SourceReference(
                    title="Gas Burners for Forges, Furnaces, and Kilns",
                    author="Michael Porter",
                    publication="Artisan Ideas",
                    year=2004,
                    trust_label=TrustLabel.SOURCE_BACKED,
                    citation_key="Porter2004",
                ),
            ],
        ).model_dump(),
    ),
    ContentEnvelope(
        id="tool-blacksmith-leg-vise",
        type=ContentType.TOOL,
        title="Solid Wrought-Iron Post Leg Vise",
        slug="blacksmith-leg-vise",
        summary="An indispensable heavy-duty clamping post engineered specifically for hot bending, twisting, chiseling, and heavy sledge hammering.",
        category="workshop",
        tags=["vise", "infrastructure", "leg-vise", "post-vise", "bending", "twisting"],
        difficulty=DifficultyLevel.BEGINNER,
        status=ContentStatus.PUBLISHED,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="workshop-guild",
            source_name="Blacksmith Knight Guild",
            source_url="https://blacksmithknight.local/workshop/blacksmith-leg-vise",
        ),
        metadata=ToolMetadata(
            tool_category=ToolCategory.INFRASTRUCTURE,
            primary_purpose="Securely grips hot steel during violent torsional bending, hot filing, chisel parting, and heavy sledge hammer blows.",
            essential_for=["Hot scroll bending and bar twisting", "Chisel hot-cutting and punching", "Heavy hand filing and planishing", "Holding hardy tools and bending forks"],
            selection_criteria=[
                "Forged wrought iron or ductile cast body—machinist bench vises made from gray cast iron will crack instantly under hammer blows.",
                "Long solid support leg that transfers all downward striking forces directly into the shop floor.",
                "Unbroken box and screw threads (check for stripped square-thread lead screws).",
                "Original or properly fitted leaf spring that pushes jaws open smoothly as screw turns.",
            ],
            beginner_guidance="Look for a 4.5 to 6-inch jaw width post vise at antique auctions, farm sales, or tailgate swap meets. It is one of the only tools in the world that cannot be broken by heavy forging.",
            beginner_friendly=True,
            diy_buildable=False,
            diy_alternatives=[
                "Heavy-duty forged steel mechanics vise (ductile iron only; never strike gray iron)",
                "Fabricated heavy floor clamp stand with heavy C-clamps",
            ],
            maintenance_protocols=[
                "Grease the acme or square box screw threads with heavy lithium grease or anti-seize compound twice yearly.",
                "Check pivot pin cotter key for wear or slop.",
                "Ensure leg floor plate is firmly bolted or nestled into a recessed dimple in shop floor.",
            ],
            safety_precautions=[
                SafetyPrecaution(
                    level="warning",
                    hazard="Crush and pinch point: High-leverage screw generates tons of force; spring release can snap jaws shut on finger flesh.",
                    mitigation="Keep hands on outer crank handle; use aluminum or copper jaw pads when clamping delicate blades.",
                    ppe=["Sturdy Work Gloves", "Steel-toe Shop Boots"],
                ),
            ],
            specifications={
                "jaw_width": "5.0 to 6.0 inches",
                "overall_height": "38 to 42 inches (designed to match elbow height for filing)",
                "weight_lbs": "65 to 110 lbs",
                "body_material": "Forged wrought iron with tool-steel jaw inserts",
            },
            related_tools=[
                RelatedContentLink(
                    content_id="tool-cross-peen-hammer",
                    title="Swedish Cross-Peen Blacksmith Hammer",
                    type=ContentType.TOOL,
                    slug="cross-peen-hammer",
                    relationship="recommended_tool",
                ),
            ],
            source_references=[
                SourceReference(
                    title="The Blacksmith's Guide",
                    author="J. F. Sallows",
                    publication="Technical Press",
                    year=1907,
                    trust_label=TrustLabel.HISTORICAL_INTERPRETATION,
                    citation_key="Sallows1907",
                ),
            ],
        ).model_dump(),
    ),
]


async def seed_initial_data(repository: BaseRepository) -> Dict[str, int]:
    """Populates local storage with baseline fixtures."""
    counts = {"materials": 0, "projects": 0, "guides": 0, "tools": 0}

    for item in SEED_MATERIALS:
        await repository.create("content", item.id, item.model_dump())
        counts["materials"] += 1

    for item in SEED_PROJECTS:
        await repository.create("content", item.id, item.model_dump())
        counts["projects"] += 1

    for item in SEED_GUIDES:
        await repository.create("content", item.id, item.model_dump())
        counts["guides"] += 1

    for item in SEED_TOOLS:
        await repository.create("content", item.id, item.model_dump())
        counts["tools"] += 1

    return counts

