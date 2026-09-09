from typing import Dict, List
from app.models.enums import ContentType, ContentStatus, DifficultyLevel, SourceType
from app.models.content import (
    ContentEnvelope,
    MaterialMetadata,
    HeatTreatmentRecipe,
    ProjectMetadata,
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


async def seed_initial_data(repository: BaseRepository) -> Dict[str, int]:
    """Populates local storage with baseline fixtures."""
    counts = {"materials": 0, "projects": 0}

    for item in SEED_MATERIALS:
        await repository.create("content", item.id, item.model_dump())
        counts["materials"] += 1

    for item in SEED_PROJECTS:
        await repository.create("content", item.id, item.model_dump())
        counts["projects"] += 1

    return counts
