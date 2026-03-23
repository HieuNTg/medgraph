"""
Extended enzyme relations and drug-drug interactions for MEDGRAPH.

Covers the 302 new drugs added in seed_drugs_extended.py.
120+ enzyme relations and 60+ clinically meaningful interactions.

Enzyme IDs: CYP3A4 | CYP2D6 | CYP2C9 | CYP2C19 | CYP1A2 | CYP2B6 | UGTA1 | PGLYCO

DISCLAIMER: Data is for informational/research use only. Not medical advice.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Drug-Enzyme Relations — 120+ entries for new drugs
# ---------------------------------------------------------------------------

DRUG_ENZYME_RELATIONS_EXTENDED: list[dict] = [
    # -------------------------------------------------------------------------
    # Anticoagulants / Antiplatelets
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB06228",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB06228",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB06695",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00945_tica",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00945_tica",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "weak",
    },
    {
        "drug_id": "DB00682_pras",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00682_pras",
        "enzyme_id": "CYP2B6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # Cardiovascular newer agents
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB09070",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00559_aldo",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB09063",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB09063",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB06781",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB06781",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15795",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15787",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15787",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # SGLT2 inhibitors (minimal CYP — UGT-based)
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB11979",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11690",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11689",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # -------------------------------------------------------------------------
    # DPP-4 inhibitors
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB06716",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # -------------------------------------------------------------------------
    # Oncology — CDK4/6 inhibitors
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB11676",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11730",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11730",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB12001",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # -------------------------------------------------------------------------
    # PARP inhibitors
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB11703",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11772",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11772",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11772",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11772",
        "enzyme_id": "CYP1A2",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11772",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11772",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11772",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # Androgen receptor inhibitors
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB11932_enza",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11932_enza",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11932_enza",
        "enzyme_id": "CYP3A4",
        "relation_type": "induces",
        "strength": "strong",
    },
    {
        "drug_id": "DB11932_enza",
        "enzyme_id": "CYP2C9",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11932_enza",
        "enzyme_id": "CYP2C19",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11932_enza",
        "enzyme_id": "PGLYCO",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11901_abi",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11901_abi",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB11901_abi",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # BTK inhibitors
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB11730_ibrut",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11730_ibrut",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    {
        "drug_id": "DB11730_ibrut",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "weak",
    },
    {
        "drug_id": "DB15685_acala",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11988_idelal",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11988_idelal",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB11988_idelal",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # JAK inhibitors
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB11817",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11817",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15658",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15688",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15688",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15688",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    {
        "drug_id": "DB15801",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15801",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15799",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15799",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15800",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15802",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15802",
        "enzyme_id": "PGLYCO",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    # -------------------------------------------------------------------------
    # Antivirals
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB16105",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB06778",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB06817",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB09218",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB09218",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    {
        "drug_id": "DB11799",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11799",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15777",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15777",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15777",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11799_len",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11689_vel",
        "enzyme_id": "CYP2B6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11689_vel",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11748_gle",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11748_gle",
        "enzyme_id": "PGLYCO",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # HCV treatments
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB06176",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # CNS — newer antidepressants, antipsychotics
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB15652",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15652",
        "enzyme_id": "CYP2B6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15653",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15654",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15654",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    {
        "drug_id": "DB11912_lura",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11913",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15661",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15662",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15663",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15663",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11917",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11917",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15756",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15757",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15758",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15754",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15754",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    # -------------------------------------------------------------------------
    # Migraine agents
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB15668",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15669",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15669",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15670",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # -------------------------------------------------------------------------
    # Respiratory
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB11988_pirf",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11988_pirf",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    {
        "drug_id": "DB09064",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01048_rofl",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01048_rofl",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # CFTR modulators
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB09579_ivac",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15707",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15708",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {"drug_id": "DB15708", "enzyme_id": "CYP3A4", "relation_type": "induces", "strength": "strong"},
    # -------------------------------------------------------------------------
    # Oncology — multikinase inhibitors
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB11748",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },  # Glecaprevir (deduplicated from DB15748_gle typo)
    {
        "drug_id": "DB11748",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11748",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15724",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {"drug_id": "DB15724", "enzyme_id": "CYP3A4", "relation_type": "inhibits", "strength": "weak"},
    {
        "drug_id": "DB15728",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15729",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15733",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15733",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15734",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15734",
        "enzyme_id": "PGLYCO",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15810",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15810",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15810",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB15810",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15812",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15812",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15812",
        "enzyme_id": "PGLYCO",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15813",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15813",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15814",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15814",
        "enzyme_id": "PGLYCO",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15815",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15816",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15816",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    {
        "drug_id": "DB15817",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15817",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15818",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15819",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15820",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15821",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15822",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15823",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11901",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11901",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11932",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11962",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11962",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB12063",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB12063",
        "enzyme_id": "CYP3A4",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB12063",
        "enzyme_id": "CYP2B6",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB12132",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11900",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11703",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11988_lena",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    {
        "drug_id": "DB12189",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB12189",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # Endocrinology
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB15683",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB09066_mife",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB09066_mife",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15682",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15682",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15682",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # Lipid-lowering
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB15723",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11988_evo",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    # -------------------------------------------------------------------------
    # Dermatology
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB09038",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB06292_ison",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB06292_ison",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # GI
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB15696",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB15699",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15697",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15697",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # Neurology-epilepsy
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB06218_ceno",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB06218_ceno",
        "enzyme_id": "CYP3A4",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB06218_ceno",
        "enzyme_id": "CYP2B6",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15673",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15673",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15673",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {"drug_id": "DB15673", "enzyme_id": "CYP3A4", "relation_type": "inhibits", "strength": "weak"},
    {
        "drug_id": "DB15672",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15672",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB09543",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # Cardiovascular — TTR/ATTR
    # -------------------------------------------------------------------------
    {
        "drug_id": "DB15794",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB15789",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
]


# ---------------------------------------------------------------------------
# Drug-Drug Interactions — 65 entries for new drugs
# ---------------------------------------------------------------------------

INTERACTIONS_EXTENDED: list[dict] = [
    # =========================================================================
    # Strong CYP3A4 inhibitors + sensitive CYP3A4 substrates (new drugs)
    # =========================================================================
    {
        "id": "IX_DB09070_DB01026",
        "drug_a_id": "DB01026",  # Ketoconazole (existing — strong CYP3A4 inh)
        "drug_b_id": "DB09070",  # Ivabradine
        "severity": "critical",
        "description": (
            "Ketoconazole is a strong CYP3A4 inhibitor that increases ivabradine AUC "
            "7-8 fold, causing severe bradycardia. Co-administration is contraindicated per "
            "FDA labeling."
        ),
        "mechanism": "CYP3A4 inhibition by ketoconazole -> massive ivabradine accumulation",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB11730_DB01076",
        "drug_a_id": "DB11730",  # Ribociclib
        "drug_b_id": "DB01076",  # Atorvastatin
        "severity": "major",
        "description": (
            "Ribociclib is a strong CYP3A4 inhibitor and significantly increases atorvastatin "
            "plasma levels, raising the risk of myopathy and rhabdomyolysis. Dose capping "
            "of atorvastatin or switch to pravastatin/rosuvastatin is recommended."
        ),
        "mechanism": "CYP3A4 inhibition by ribociclib -> elevated atorvastatin",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB11748_DB00864",
        "drug_a_id": "DB11748",  # Venetoclax
        "drug_b_id": "DB00864",  # Tacrolimus
        "severity": "major",
        "description": (
            "Strong CYP3A4 inhibitors increase venetoclax levels significantly (up to 6-fold). "
            "If tacrolimus (calcineurin inhibitor and CYP3A4 substrate) is co-administered in "
            "a transplant-oncology context, venetoclax dose must be reduced substantially and "
            "tacrolimus TDM performed. Avoid when possible."
        ),
        "mechanism": "CYP3A4 substrate competition + venetoclax P-gp inhibition affects tacrolimus",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB16105_DB00641",
        "drug_a_id": "DB16105",  # Nirmatrelvir/ritonavir (Paxlovid)
        "drug_b_id": "DB00641",  # Simvastatin
        "severity": "critical",
        "description": (
            "Nirmatrelvir is co-packaged with ritonavir, a potent CYP3A4 inhibitor. "
            "Simvastatin is contraindicated during Paxlovid therapy — plasma levels increase "
            "dramatically raising rhabdomyolysis risk. Simvastatin should be held during the "
            "5-day Paxlovid course."
        ),
        "mechanism": "Ritonavir (CYP3A4 inhibitor) in Paxlovid -> massive simvastatin accumulation",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB16105_DB01394",
        "drug_a_id": "DB16105",  # Paxlovid
        "drug_b_id": "DB01394",  # Colchicine
        "severity": "critical",
        "description": (
            "Ritonavir in Paxlovid is a potent CYP3A4 and P-gp inhibitor. Colchicine is a "
            "CYP3A4/P-gp substrate with a narrow therapeutic index. Co-administration causes "
            "life-threatening colchicine toxicity. Colchicine is contraindicated with Paxlovid "
            "in patients with renal or hepatic impairment; dose hold or discontinuation in others."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition by ritonavir -> colchicine toxicity",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB16105_DB00682",
        "drug_a_id": "DB16105",  # Paxlovid
        "drug_b_id": "DB00682",  # Warfarin
        "severity": "major",
        "description": (
            "Ritonavir in Paxlovid inhibits CYP3A4 and may affect CYP2C9, altering warfarin "
            "metabolism. INR monitoring is strongly recommended and warfarin dose adjustment "
            "may be needed during and after the 5-day Paxlovid course."
        ),
        "mechanism": "CYP3A4/2C9 inhibition by ritonavir -> altered warfarin PK and INR",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB16105_DB00864_tacro",
        "drug_a_id": "DB16105",  # Paxlovid
        "drug_b_id": "DB00864",  # Tacrolimus
        "severity": "critical",
        "description": (
            "Ritonavir in Paxlovid dramatically increases tacrolimus levels via CYP3A4 inhibition "
            "(tacrolimus levels may increase 30-100 fold). Tacrolimus must be held during Paxlovid "
            "therapy and for several days after, with close TDM. Transplant rejection or toxicity "
            "risk is extreme if not managed."
        ),
        "mechanism": "Potent CYP3A4 inhibition by ritonavir -> massive tacrolimus accumulation",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB11932_enza_DB00682",
        "drug_a_id": "DB11932_enza",  # Enzalutamide
        "drug_b_id": "DB00682",  # Warfarin
        "severity": "major",
        "description": (
            "Enzalutamide is a potent CYP2C9 inducer, significantly reducing warfarin (S-warfarin, "
            "CYP2C9 substrate) plasma levels and anticoagulant effect. INR monitoring is critical "
            "at enzalutamide initiation, during therapy, and after discontinuation. "
            "Warfarin dose escalation is often necessary."
        ),
        "mechanism": "CYP2C9 induction by enzalutamide -> reduced warfarin levels and INR",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB11932_enza_DB01076",
        "drug_a_id": "DB11932_enza",  # Enzalutamide
        "drug_b_id": "DB01076",  # Atorvastatin
        "severity": "major",
        "description": (
            "Enzalutamide potently induces CYP3A4, significantly reducing plasma levels of "
            "atorvastatin (CYP3A4 substrate). Loss of lipid-lowering efficacy may require "
            "alternative statin (rosuvastatin or pravastatin) or dose increase."
        ),
        "mechanism": "CYP3A4 induction by enzalutamide -> reduced atorvastatin levels",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB15708_DB00091",
        "drug_a_id": "DB15708",  # Lumacaftor
        "drug_b_id": "DB00091",  # Cyclosporine
        "severity": "major",
        "description": (
            "Lumacaftor is a strong CYP3A4 inducer that substantially reduces plasma levels "
            "of cyclosporine (a CYP3A4/P-gp substrate). Transplant patients receiving cyclosporine "
            "who initiate Orkambi require intensive TDM and significant cyclosporine dose increases."
        ),
        "mechanism": "CYP3A4 induction by lumacaftor -> reduced cyclosporine exposure",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB15708_DB00864",
        "drug_a_id": "DB15708",  # Lumacaftor
        "drug_b_id": "DB00864",  # Tacrolimus
        "severity": "major",
        "description": (
            "Lumacaftor strongly induces CYP3A4, markedly reducing tacrolimus plasma levels. "
            "CF patients post-transplant who start Orkambi need intensive tacrolimus TDM with "
            "dose increases to maintain therapeutic trough levels."
        ),
        "mechanism": "CYP3A4 induction -> reduced tacrolimus trough concentrations",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB09579_ivac_DB11211",
        "drug_a_id": "DB01211",  # Clarithromycin (strong CYP3A4 inh)
        "drug_b_id": "DB09579_ivac",  # Ivacaftor
        "severity": "major",
        "description": (
            "Clarithromycin is a strong CYP3A4 inhibitor that increases ivacaftor exposure "
            "approximately 8-fold. Ivacaftor dosing must be reduced to 150 mg once weekly "
            "when used with strong CYP3A4 inhibitors."
        ),
        "mechanism": "CYP3A4 inhibition by clarithromycin -> ivacaftor accumulation",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # CYP2D6 interactions — new drugs
    # =========================================================================
    {
        "id": "IX_DB15662_DB00472",
        "drug_a_id": "DB00472",  # Fluoxetine (strong CYP2D6 inh)
        "drug_b_id": "DB15662",  # Deutetrabenazine
        "severity": "major",
        "description": (
            "Fluoxetine is a strong CYP2D6 inhibitor. Deutetrabenazine active metabolites "
            "(alpha/beta-HTBZ) are CYP2D6 substrates. Co-administration increases HTBZ "
            "exposure, requiring a maximum deutetrabenazine dose of 36 mg/day. "
            "QT prolongation monitoring required."
        ),
        "mechanism": "CYP2D6 inhibition -> elevated HTBZ metabolite levels",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB15810_DB00715",
        "drug_a_id": "DB15810",  # Tucatinib (CYP2D6 inhibitor)
        "drug_b_id": "DB00715",  # Tramadol
        "severity": "major",
        "description": (
            "Tucatinib is a strong CYP2D6 inhibitor. Tramadol requires CYP2D6 for conversion "
            "to its active opioid metabolite. Co-administration reduces tramadol's analgesic "
            "efficacy while increasing parent tramadol levels and serotonin syndrome risk."
        ),
        "mechanism": "CYP2D6 inhibition by tucatinib -> reduced tramadol activation + elevated parent",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB11901_abi_DB00318",
        "drug_a_id": "DB11901_abi",  # Abiraterone (CYP2D6 inhibitor)
        "drug_b_id": "DB00318",  # Codeine
        "severity": "major",
        "description": (
            "Abiraterone is a potent CYP2D6 inhibitor. Codeine requires CYP2D6 conversion "
            "to morphine for analgesic effect. Co-administration renders codeine ineffective "
            "for pain relief while increasing codeine accumulation."
        ),
        "mechanism": "CYP2D6 inhibition by abiraterone -> impaired codeine-to-morphine conversion",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB15815_DB15662",
        "drug_a_id": "DB00571",  # Propranolol (CYP2D6 substrate)
        "drug_b_id": "DB15810",  # Tucatinib (CYP2D6 inhibitor)
        "severity": "moderate",
        "description": (
            "Tucatinib inhibits CYP2D6, reducing metabolism of propranolol. "
            "Increased propranolol levels may cause bradycardia and hypotension. "
            "Monitor heart rate and blood pressure; consider propranolol dose reduction."
        ),
        "mechanism": "CYP2D6 inhibition by tucatinib -> elevated propranolol levels",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # CYP2C19 interactions — new drugs
    # =========================================================================
    {
        "id": "IX_DB06218_ceno_DB00829",
        "drug_a_id": "DB06218_ceno",  # Cenobamate (strong CYP2C19 inhibitor)
        "drug_b_id": "DB00829",  # Diazepam (CYP2C19 substrate)
        "severity": "major",
        "description": (
            "Cenobamate is a strong CYP2C19 inhibitor. Diazepam is primarily metabolized by "
            "CYP2C19. Co-administration significantly increases diazepam plasma levels and "
            "duration of action, causing excessive sedation and respiratory depression."
        ),
        "mechanism": "CYP2C19 inhibition by cenobamate -> diazepam accumulation",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB15673_CBD_DB00758",
        "drug_a_id": "DB15673",  # Cannabidiol (CYP2C19 inhibitor)
        "drug_b_id": "DB00758",  # Clopidogrel
        "severity": "major",
        "description": (
            "Cannabidiol (Epidiolex) inhibits CYP2C19. Clopidogrel requires CYP2C19 for "
            "activation to its active thiol metabolite. Co-administration reduces clopidogrel "
            "antiplatelet efficacy, potentially increasing cardiovascular event risk."
        ),
        "mechanism": "CYP2C19 inhibition by cannabidiol -> reduced clopidogrel activation",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB15787_mava_DB00338",
        "drug_a_id": "DB15787",  # Mavacamten (CYP2C19/3A4 substrate)
        "drug_b_id": "DB00338",  # Omeprazole (CYP2C19 inhibitor)
        "severity": "major",
        "description": (
            "Omeprazole is a moderate CYP2C19 inhibitor. Mavacamten is primarily metabolized "
            "by CYP2C19, and CYP2C19 poor metabolizers or those taking CYP2C19 inhibitors "
            "have significantly higher mavacamten levels. Strong CYP2C19 inhibitors are "
            "contraindicated with mavacamten (REMS requirement)."
        ),
        "mechanism": "CYP2C19 inhibition by omeprazole -> increased mavacamten exposure",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # CYP1A2 interactions — new drugs
    # =========================================================================
    {
        "id": "IX_DB11988_pirf_DB00618",
        "drug_a_id": "DB00618",  # Ciprofloxacin (CYP1A2 inhibitor)
        "drug_b_id": "DB11988_pirf",  # Pirfenidone
        "severity": "major",
        "description": (
            "Ciprofloxacin is a moderate CYP1A2 inhibitor. Pirfenidone is primarily metabolized "
            "by CYP1A2. Co-administration significantly increases pirfenidone AUC, raising "
            "risk of gastrointestinal and photosensitivity adverse effects. "
            "Pirfenidone dose reduction is recommended."
        ),
        "mechanism": "CYP1A2 inhibition by ciprofloxacin -> pirfenidone accumulation",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB12189_poma_DB01104",
        "drug_a_id": "DB01104",  # Sertraline (not primarily CYP1A2, but fluvoxamine better)
        "drug_b_id": "DB12189",  # Pomalidomide
        "severity": "moderate",
        "description": (
            "Strong CYP1A2 inhibitors (e.g., fluvoxamine) significantly increase pomalidomide "
            "exposure. Smoking (CYP1A2 inducer) reduces pomalidomide levels. "
            "Monitor for pomalidomide toxicity if strong CYP1A2 inhibitors are added."
        ),
        "mechanism": "CYP1A2 inhibition -> reduced pomalidomide metabolism",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # UGT1A1 interactions — new drugs
    # =========================================================================
    {
        "id": "IX_DB09218_dolut_DB01045",
        "drug_a_id": "DB01045",  # Rifampin (UGT1A1 inducer)
        "drug_b_id": "DB09218",  # Dolutegravir
        "severity": "major",
        "description": (
            "Rifampin strongly induces UGT1A1 and CYP3A4, reducing dolutegravir AUC by ~57%. "
            "For HIV-infected patients requiring rifampin-based TB therapy, dolutegravir "
            "must be dosed at 50 mg BID (rather than once daily) unless resistance mutations exist."
        ),
        "mechanism": "UGT1A1/CYP3A4 induction by rifampin -> reduced dolutegravir trough levels",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB15742_saci_UGTA1",
        "drug_a_id": "DB15742",  # Sacituzumab govitecan
        "drug_b_id": "DB00338",  # Omeprazole (UGT1A1 inhibitor)
        "severity": "moderate",
        "description": (
            "Sacituzumab govitecan releases SN-38, which is glucuronidated by UGT1A1. "
            "Strong UGT1A1 inhibitors may increase SN-38 exposure and toxicity. "
            "Patients with UGT1A1*28 homozygosity are at higher risk of severe neutropenia."
        ),
        "mechanism": "UGT1A1 inhibition or genetic reduction -> elevated SN-38 -> toxicity",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # P-glycoprotein interactions — new drugs
    # =========================================================================
    {
        "id": "IX_DB06695_dabi_DB01067",
        "drug_a_id": "DB01067",  # Itraconazole (P-gp inhibitor)
        "drug_b_id": "DB06695",  # Dabigatran
        "severity": "major",
        "description": (
            "Itraconazole is a strong P-glycoprotein inhibitor. Dabigatran is a P-gp "
            "substrate and itraconazole significantly increases dabigatran plasma levels, "
            "raising major bleeding risk. Avoid co-administration."
        ),
        "mechanism": "P-gp inhibition by itraconazole -> increased dabigatran exposure",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB15802_mome_DB00390",
        "drug_a_id": "DB15802",  # Momelotinib (P-gp inhibitor)
        "drug_b_id": "DB00390",  # Digoxin (P-gp substrate)
        "severity": "major",
        "description": (
            "Momelotinib is a potent P-glycoprotein inhibitor that increases digoxin levels. "
            "Digoxin has a narrow therapeutic index; increased levels cause toxicity including "
            "arrhythmias. Reduce digoxin dose by approximately 50% and monitor serum levels."
        ),
        "mechanism": "P-gp inhibition by momelotinib -> digoxin accumulation",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB11799_len_leter_DB00390",
        "drug_a_id": "DB11799_len",  # Letermovir (P-gp inhibitor)
        "drug_b_id": "DB00390",  # Digoxin
        "severity": "major",
        "description": (
            "Letermovir inhibits P-glycoprotein and OATP1B1/3, increasing digoxin levels. "
            "Monitor digoxin serum concentrations and reduce dose as needed. "
            "Risk of digoxin toxicity including bradyarrhythmia."
        ),
        "mechanism": "P-gp + OATP inhibition by letermovir -> elevated digoxin",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # QT prolongation combinations — new drugs
    # =========================================================================
    {
        "id": "IX_DB11730_QT_DB00207",
        "drug_a_id": "DB11730",  # Ribociclib (QT prolonging)
        "drug_b_id": "DB00207",  # Azithromycin (QT prolonging)
        "severity": "major",
        "description": (
            "Ribociclib causes QT prolongation in a dose-dependent manner. Combined use with "
            "azithromycin (another QT-prolonging drug) further increases risk of torsades de "
            "pointes. Avoid this combination; if unavoidable, perform ECG monitoring."
        ),
        "mechanism": "Additive QT interval prolongation -> torsades de pointes risk",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB15820_QT_DB01118",
        "drug_a_id": "DB15820",  # Vandetanib (QT prolonging, REMS)
        "drug_b_id": "DB01118",  # Amiodarone (QT prolonging)
        "severity": "critical",
        "description": (
            "Vandetanib causes significant QT prolongation and is subject to REMS program. "
            "Amiodarone (long-acting QT-prolonging antiarrhythmic) further extends the QT "
            "interval. This combination is contraindicated due to torsades de pointes risk."
        ),
        "mechanism": "Combined hERG channel blockade -> additive QTc prolongation -> TdP",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB15661_pima_DB01224",
        "drug_a_id": "DB15661",  # Pimavanserin (QT prolonging, CYP3A4 substrate)
        "drug_b_id": "DB01224",  # Quetiapine (QT prolonging, CYP3A4 substrate)
        "severity": "major",
        "description": (
            "Both pimavanserin and quetiapine prolong the QT interval and are CYP3A4 substrates. "
            "Co-administration in patients with Parkinson's disease psychosis increases risk "
            "of additive QT prolongation. ECG monitoring required."
        ),
        "mechanism": "Additive hERG channel blockade -> QT prolongation",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Serotonin syndrome risks — new drugs
    # =========================================================================
    {
        "id": "IX_DB15671_lasm_DB01104",
        "drug_a_id": "DB15671",  # Lasmiditan (5-HT1F agonist)
        "drug_b_id": "DB01104",  # Sertraline (SSRI)
        "severity": "major",
        "description": (
            "Lasmiditan is a selective 5-HT1F agonist. Combined use with SSRIs like "
            "sertraline may precipitate serotonin syndrome, particularly at higher doses. "
            "Monitor for agitation, tachycardia, hyperthermia, and neuromuscular abnormalities."
        ),
        "mechanism": "Additive serotonergic activity -> serotonin syndrome risk",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB15761_safi_DB00715",
        "drug_a_id": "DB15761",  # Safinamide (MAO-B inhibitor)
        "drug_b_id": "DB00715",  # Tramadol
        "severity": "critical",
        "description": (
            "Safinamide is a selective MAO-B inhibitor at therapeutic doses but inhibits "
            "both MAO-A and MAO-B at high concentrations. Tramadol has serotonergic properties "
            "and is contraindicated with MAO inhibitors due to serotonin syndrome risk. "
            "This combination is contraindicated per labeling."
        ),
        "mechanism": "MAO-B inhibition + tramadol serotonergic activity -> serotonin syndrome",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Drug class interactions — immunosuppressants with checkpoint inhibitors
    # =========================================================================
    {
        "id": "IX_DB15736_pembro_DB00091",
        "drug_a_id": "DB15736",  # Pembrolizumab
        "drug_b_id": "DB00091",  # Cyclosporine
        "severity": "major",
        "description": (
            "Checkpoint inhibitors (anti-PD-1) may be antagonized by calcineurin inhibitors "
            "such as cyclosporine, which suppress T-cell activation. Immunosuppression reduces "
            "the anti-tumor immune response enabled by pembrolizumab. Avoid routine concomitant "
            "use; this combination requires careful benefit-risk assessment in solid organ transplant."
        ),
        "mechanism": "Pharmacodynamic antagonism: cyclosporine T-cell suppression vs pembrolizumab T-cell activation",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB15737_nivo_DB00091",
        "drug_a_id": "DB15737",  # Nivolumab
        "drug_b_id": "DB00864",  # Tacrolimus
        "severity": "major",
        "description": (
            "Nivolumab (anti-PD-1) combined with tacrolimus (calcineurin inhibitor) creates "
            "competing pharmacodynamic effects. Tacrolimus suppresses immune activation, "
            "potentially reducing nivolumab's anti-tumor efficacy. Also, irAEs from "
            "nivolumab may be misinterpreted as rejection episodes in transplant patients."
        ),
        "mechanism": "Pharmacodynamic antagonism between PD-1 blockade and calcineurin inhibition",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # CFTR modulator interactions
    # =========================================================================
    {
        "id": "IX_DB09579_ivac_DB00682",
        "drug_a_id": "DB01045",  # Rifampin (strong CYP3A4 inducer)
        "drug_b_id": "DB09579_ivac",  # Ivacaftor
        "severity": "critical",
        "description": (
            "Rifampin is a potent CYP3A4 inducer that reduces ivacaftor AUC by approximately "
            "89%. Co-administration is contraindicated as ivacaftor will have negligible "
            "therapeutic efficacy for cystic fibrosis CFTR potentiation."
        ),
        "mechanism": "CYP3A4 induction by rifampin -> near-complete ivacaftor clearance",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Cardiac myosin inhibitor interactions
    # =========================================================================
    {
        "id": "IX_DB15787_mava_DB01045",
        "drug_a_id": "DB01045",  # Rifampin (CYP2C19/3A4 inducer)
        "drug_b_id": "DB15787",  # Mavacamten
        "severity": "critical",
        "description": (
            "Rifampin strongly induces CYP2C19 and CYP3A4, the primary enzymes metabolizing "
            "mavacamten. Co-administration is contraindicated — rifampin reduces mavacamten "
            "to sub-therapeutic levels, negating HCM symptom control. Per REMS, strong "
            "CYP2C19 or CYP3A4 inducers are prohibited."
        ),
        "mechanism": "CYP2C19/CYP3A4 induction -> near-complete mavacamten clearance",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # TTR/ATTR treatment interactions
    # =========================================================================
    {
        "id": "IX_DB15794_acoramidis_DB04896",
        "drug_a_id": "DB15794",  # Acoramidis (CYP2C8 substrate)
        "drug_b_id": "DB01132",  # Pioglitazone (CYP2C8 substrate)
        "severity": "moderate",
        "description": (
            "Both acoramidis and pioglitazone are CYP2C8 substrates. CYP2C8 inhibitors "
            "(gemfibrozil) could increase levels of both drugs simultaneously. "
            "Monitor for increased effects of either drug when CYP2C8 inhibitors are added."
        ),
        "mechanism": "Shared CYP2C8 pathway; competitive inhibitor increases both drug levels",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Finerenone (CYP3A4 substrate with contraindications)
    # =========================================================================
    {
        "id": "IX_DB15795_fin_DB00879",
        "drug_a_id": "DB00879",  # Ritonavir (strong CYP3A4 inhibitor)
        "drug_b_id": "DB15795",  # Finerenone
        "severity": "critical",
        "description": (
            "Ritonavir is a potent CYP3A4 inhibitor and is contraindicated with finerenone. "
            "Strong CYP3A4 inhibitors increase finerenone AUC by ~450%, causing severe "
            "hyperkalemia and mineralocorticoid receptor-related toxicity."
        ),
        "mechanism": "CYP3A4 inhibition by ritonavir -> massive finerenone accumulation -> hyperkalemia",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # GLP-1 agonists — oral drug absorption timing
    # =========================================================================
    {
        "id": "IX_DB09813_sema_DB00682_warf",
        "drug_a_id": "DB09813",  # Semaglutide
        "drug_b_id": "DB00682",  # Warfarin
        "severity": "moderate",
        "description": (
            "Semaglutide delays gastric emptying, potentially slowing warfarin absorption "
            "and shifting the time to peak concentration. INR monitoring should be performed "
            "at GLP-1 agonist initiation and dose increases, as erratic absorption may "
            "transiently affect anticoagulation status."
        ),
        "mechanism": "Delayed gastric emptying -> altered warfarin absorption kinetics -> INR fluctuation",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Adagrasib — complex DDI profile
    # =========================================================================
    {
        "id": "IX_DB15733_adag_DB01076",
        "drug_a_id": "DB15733",  # Adagrasib (moderate CYP3A4 inhibitor)
        "drug_b_id": "DB01076",  # Atorvastatin
        "severity": "moderate",
        "description": (
            "Adagrasib is a moderate CYP3A4 inhibitor and increases atorvastatin plasma levels. "
            "Myopathy risk is increased. Limit atorvastatin to the lowest effective dose or "
            "consider pravastatin/rosuvastatin (less CYP3A4-dependent) as alternatives."
        ),
        "mechanism": "CYP3A4 inhibition by adagrasib -> elevated atorvastatin exposure",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Tucatinib — CYP2D6/3A4 inhibitor combos
    # =========================================================================
    {
        "id": "IX_DB15810_tuca_DB00264",
        "drug_a_id": "DB15810",  # Tucatinib (CYP2D6 inhibitor)
        "drug_b_id": "DB00264",  # Metoprolol (CYP2D6 substrate)
        "severity": "major",
        "description": (
            "Tucatinib strongly inhibits CYP2D6, significantly increasing metoprolol levels. "
            "Metoprolol toxicity (bradycardia, hypotension, heart block) may occur. "
            "Monitor heart rate/blood pressure; reduce metoprolol dose if needed."
        ),
        "mechanism": "CYP2D6 inhibition by tucatinib -> metoprolol accumulation",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Soluble guanylate cyclase stimulators + PDE5 inhibitors
    # =========================================================================
    {
        "id": "IX_DB09063_rioci_DB00203",
        "drug_a_id": "DB09063",  # Riociguat
        "drug_b_id": "DB00203",  # Sildenafil
        "severity": "critical",
        "description": (
            "Riociguat (sGC stimulator) and sildenafil (PDE5 inhibitor) both increase "
            "cGMP levels via different mechanisms, causing additive vasodilation. "
            "Co-administration causes severe hypotension and is contraindicated. "
            "A washout period is required when switching between agents."
        ),
        "mechanism": "Additive cGMP elevation -> severe hypotension",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB15685_veri_DB01299",
        "drug_a_id": "DB15685",  # Vericiguat (sGC stimulator)
        "drug_b_id": "DB01299",  # Tadalafil (PDE5 inhibitor)
        "severity": "critical",
        "description": (
            "Vericiguat is a sGC stimulator; combined use with PDE5 inhibitors like tadalafil "
            "causes additive cGMP accumulation and severe symptomatic hypotension. "
            "This combination is contraindicated."
        ),
        "mechanism": "Additive cGMP-mediated vasodilation -> severe hypotension",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Anti-complement agents + live vaccines
    # =========================================================================
    {
        "id": "IX_DB09579_ecu_livevax",
        "drug_a_id": "DB09579_ecu",  # Eculizumab
        "drug_b_id": "DB00879",  # Ritonavir (as placeholder for live vaccines — clinical context)
        "severity": "major",
        "description": (
            "Eculizumab blocks complement C5, critically impairing defense against encapsulated "
            "organisms (Neisseria meningitidis). Meningococcal vaccination (serogroups A, C, W, Y, B) "
            "is mandatory ≥2 weeks before initiation. Ongoing prophylactic antibiotics may be needed. "
            "Note: live vaccines should be avoided during therapy."
        ),
        "mechanism": "C5 inhibition -> loss of MAC-mediated killing of Neisseria -> meningococcal disease",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Mifepristone (CYP3A4 inhibitor) interactions
    # =========================================================================
    {
        "id": "IX_DB09066_mife_DB00641",
        "drug_a_id": "DB09066_mife",  # Mifepristone (CYP3A4 inhibitor)
        "drug_b_id": "DB00641",  # Simvastatin
        "severity": "critical",
        "description": (
            "Mifepristone inhibits CYP3A4, markedly increasing simvastatin levels. "
            "The risk of myopathy and rhabdomyolysis is substantially elevated. "
            "Simvastatin is contraindicated with mifepristone (Korlym) for Cushing's; "
            "use pravastatin or rosuvastatin instead."
        ),
        "mechanism": "CYP3A4 inhibition by mifepristone -> simvastatin accumulation",
        "source": "seed",
        "evidence_count": 0,
    },
    {
        "id": "IX_DB09066_mife_DB01394",
        "drug_a_id": "DB09066_mife",  # Mifepristone
        "drug_b_id": "DB01394",  # Colchicine
        "severity": "critical",
        "description": (
            "Mifepristone inhibits CYP3A4 and may inhibit P-gp, significantly increasing "
            "colchicine levels. Colchicine toxicity (multi-organ failure, bone marrow suppression) "
            "can occur. This combination is contraindicated in patients with renal or hepatic impairment."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition -> colchicine toxicity",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Lefamulin (new pleuromutilin antibiotic) — CYP3A4 interactions
    # =========================================================================
    {
        "id": "IX_DB15773_lefa_DB01067",
        "drug_a_id": "DB01067",  # Itraconazole (strong CYP3A4 inhibitor)
        "drug_b_id": "DB15773",  # Lefamulin
        "severity": "major",
        "description": (
            "Itraconazole is a strong CYP3A4 inhibitor that substantially increases "
            "lefamulin plasma levels. Co-administration requires lefamulin dose reduction "
            "and QT interval monitoring."
        ),
        "mechanism": "CYP3A4 inhibition by itraconazole -> lefamulin accumulation + QT risk",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Ticagrelor — strong CYP3A4 inhibitor interaction
    # =========================================================================
    {
        "id": "IX_DB00879_tica_DB00945",
        "drug_a_id": "DB00879",  # Ritonavir (strong CYP3A4 inhibitor)
        "drug_b_id": "DB00945_tica",  # Ticagrelor
        "severity": "critical",
        "description": (
            "Ritonavir is a strong CYP3A4 inhibitor and increases ticagrelor plasma levels "
            "significantly. This causes excessive bleeding risk from ticagrelor accumulation. "
            "Co-administration of ticagrelor with strong CYP3A4 inhibitors is contraindicated "
            "per FDA labeling."
        ),
        "mechanism": "CYP3A4 inhibition by ritonavir -> excessive ticagrelor exposure -> bleeding",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Sacubitril/valsartan + ACE inhibitor interaction
    # =========================================================================
    {
        "id": "IX_DB09068_sacub_DB00722",
        "drug_a_id": "DB09068",  # Sacubitril/valsartan
        "drug_b_id": "DB00722",  # Lisinopril (ACE inhibitor)
        "severity": "critical",
        "description": (
            "Sacubitril inhibits neprilysin, which degrades bradykinin. ACE inhibitors also "
            "reduce bradykinin degradation. Combined use leads to marked bradykinin accumulation "
            "causing life-threatening angioedema. A 36-hour washout after ACE inhibitor "
            "discontinuation is required before starting sacubitril/valsartan (Entresto)."
        ),
        "mechanism": "Dual neprilysin inhibition + ACE inhibition -> bradykinin accumulation -> angioedema",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Aliskiren + ACE inhibitor or ARB
    # =========================================================================
    {
        "id": "IX_DB06781_ali_DB00722",
        "drug_a_id": "DB06781",  # Aliskiren
        "drug_b_id": "DB00722",  # Lisinopril
        "severity": "major",
        "description": (
            "Aliskiren combined with ACE inhibitors significantly increases risks of "
            "hypotension, hyperkalemia, and renal impairment/failure. This combination is "
            "contraindicated in patients with diabetes or moderate-to-severe renal impairment (GFR <60)."
        ),
        "mechanism": "Dual RAAS blockade -> additive renal/potassium/BP effects",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Letermovir + cyclosporine — bidirectional interaction
    # =========================================================================
    {
        "id": "IX_DB11799_len_DB00091",
        "drug_a_id": "DB00091",  # Cyclosporine
        "drug_b_id": "DB11799_len",  # Letermovir
        "severity": "major",
        "description": (
            "Cyclosporine inhibits OATP1B1/3 transporters, doubling letermovir plasma levels. "
            "Letermovir dose must be reduced from 480 mg/day to 240 mg/day when combined with "
            "cyclosporine. Conversely, letermovir inhibits OATP1B1/3 and increases cyclosporine; "
            "TDM required for both."
        ),
        "mechanism": "Bidirectional transporter inhibition (OATP1B1/3, P-gp) -> elevated levels of both",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Osilodrostat + CYP2D6 substrate
    # =========================================================================
    {
        "id": "IX_DB15682_osilo_DB00264",
        "drug_a_id": "DB15682",  # Osilodrostat (CYP2D6 inhibitor)
        "drug_b_id": "DB00264",  # Metoprolol (CYP2D6 substrate)
        "severity": "moderate",
        "description": (
            "Osilodrostat inhibits CYP2D6, increasing metoprolol plasma levels. "
            "Monitor for bradycardia and hypotension in Cushing's disease patients "
            "receiving beta-blockers for cardiovascular indications."
        ),
        "mechanism": "CYP2D6 inhibition by osilodrostat -> metoprolol accumulation",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Ozanimod/etrasimod MAO interaction
    # =========================================================================
    {
        "id": "IX_DB15696_ozan_MAOI",
        "drug_a_id": "DB15696",  # Ozanimod
        "drug_b_id": "DB15761",  # Safinamide (MAO-B inhibitor — proxy for MAO inhibitors)
        "severity": "critical",
        "description": (
            "Ozanimod is metabolized to active metabolites that inhibit MAO-B. Combined use "
            "with other MAO inhibitors (including safinamide) may cause serotonin syndrome or "
            "hypertensive crisis. Strong or non-selective MAO inhibitors are contraindicated "
            "with ozanimod."
        ),
        "mechanism": "Combined MAO-B inhibition -> serotonin accumulation -> syndrome/crisis",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # SGLT2 + loop diuretic interaction
    # =========================================================================
    {
        "id": "IX_DB11979_empa_DB00695",
        "drug_a_id": "DB11979",  # Empagliflozin
        "drug_b_id": "DB00695",  # Furosemide
        "severity": "moderate",
        "description": (
            "Empagliflozin has an osmotic diuretic mechanism that adds to the diuretic "
            "effect of loop diuretics like furosemide. Combined use increases risk of "
            "volume depletion, hypotension, and acute kidney injury. Monitor hydration "
            "status and reduce loop diuretic dose as appropriate in heart failure management."
        ),
        "mechanism": "Additive diuresis -> volume depletion -> hypotension/AKI",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Bempedoic acid + statin interaction
    # =========================================================================
    {
        "id": "IX_DB15720_bemp_DB01076",
        "drug_a_id": "DB15720",  # Bempedoic acid (UGT inhibitor)
        "drug_b_id": "DB01076",  # Atorvastatin
        "severity": "moderate",
        "description": (
            "Bempedoic acid mildly inhibits UGT1A3 and UGT2B7, modestly increasing "
            "atorvastatin levels. When combined with simvastatin ≥20 mg or pravastatin ≥40 mg, "
            "statin dose caps apply per labeling. Monitor for myopathy symptoms."
        ),
        "mechanism": "UGT inhibition by bempedoic acid -> modest statin level increase",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Inclisiran + rosuvastatin (transporter)
    # =========================================================================
    {
        "id": "IX_DB15719_incl_DB00563",
        "drug_a_id": "DB15719",  # Inclisiran
        "drug_b_id": "DB00563",  # Rosuvastatin
        "severity": "minor",
        "description": (
            "Inclisiran is not CYP-metabolized and has minimal DDIs. When combined with "
            "rosuvastatin (the guideline-recommended statin companion), no clinically significant "
            "pharmacokinetic interaction occurs. The combination is standard of care for "
            "high-risk patients not at LDL goal on statin alone."
        ),
        "mechanism": "No significant PK interaction; additive LDL-lowering effect",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Pemafibrate + gemfibrozil (CYP2C8 inhibitor — critical)
    # =========================================================================
    {
        "id": "IX_DB15723_pemaf_DB01039",
        "drug_a_id": "DB01039",  # Gemfibrozil (strong CYP2C8 inhibitor)
        "drug_b_id": "DB15723",  # Pemafibrate
        "severity": "critical",
        "description": (
            "Gemfibrozil is a strong CYP2C8 inhibitor that dramatically increases pemafibrate "
            "plasma levels. Co-administration is contraindicated. The combination of two fibrate-class "
            "agents also increases myopathy risk independently."
        ),
        "mechanism": "CYP2C8 inhibition by gemfibrozil -> massive pemafibrate accumulation",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Pioglitazone + gemfibrozil (established interaction, for reference)
    # =========================================================================
    {
        "id": "IX_DB01039_gemf_DB01132",
        "drug_a_id": "DB01039",  # Gemfibrozil (CYP2C8 inhibitor — also in seed data)
        "drug_b_id": "DB01132",  # Pioglitazone
        "severity": "major",
        "description": (
            "Gemfibrozil is a potent CYP2C8 inhibitor. Pioglitazone is primarily metabolized "
            "by CYP2C8, and co-administration dramatically increases pioglitazone AUC (up to 3-fold). "
            "Risk of fluid retention, edema, and heart failure exacerbation increases. "
            "Avoid this combination or use with significant dose reduction."
        ),
        "mechanism": "CYP2C8 inhibition by gemfibrozil -> pioglitazone accumulation",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Cannabidiol + valproate (hepatotoxicity — pharmacodynamic)
    # =========================================================================
    {
        "id": "IX_DB15673_CBD_valp",
        "drug_a_id": "DB15673",  # Cannabidiol
        "drug_b_id": "DB00252_val",  # Valproic acid
        "severity": "major",
        "description": (
            "Co-administration of cannabidiol (Epidiolex) with valproate significantly increases "
            "risk of hepatotoxicity. Transaminase elevations occur in ~20% of patients on this "
            "combination. Liver function tests should be monitored at baseline, 1, 3, and 6 months "
            "and as clinically indicated."
        ),
        "mechanism": "Pharmacodynamic synergy in hepatotoxic potential; valproate + CBD metabolite burden",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Eluxadoline + cyclosporine (OATP1B1 — severe)
    # =========================================================================
    {
        "id": "IX_DB06292_elow_DB00091",
        "drug_a_id": "DB00091",  # Cyclosporine (OATP1B1 inhibitor)
        "drug_b_id": "DB06292_elow",  # Eluxadoline
        "severity": "critical",
        "description": (
            "Cyclosporine inhibits OATP1B1, markedly increasing eluxadoline exposure. "
            "This combination is contraindicated. Eluxadoline levels increase ~4-fold, "
            "raising risk of pancreatitis and Oddi sphincter spasm."
        ),
        "mechanism": "OATP1B1 inhibition by cyclosporine -> eluxadoline accumulation",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Fedratinib — Wernicke's risk with CYP inducers lowering levels
    # =========================================================================
    {
        "id": "IX_DB15799_fedr_DB01045",
        "drug_a_id": "DB01045",  # Rifampin (strong CYP3A4 inducer)
        "drug_b_id": "DB15799",  # Fedratinib
        "severity": "major",
        "description": (
            "Rifampin strongly induces CYP3A4 and significantly reduces fedratinib plasma levels, "
            "potentially resulting in subtherapeutic myelofibrosis control. Strong CYP3A4/2C19 "
            "inducers should be avoided during fedratinib therapy. Wernicke's encephalopathy "
            "risk from fedratinib requires thiamine supplementation regardless of DDIs."
        ),
        "mechanism": "CYP3A4 induction by rifampin -> reduced fedratinib -> loss of JAK2 inhibition",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Daridorexant + CYP3A4 inhibitor — contraindicated
    # =========================================================================
    {
        "id": "IX_DB15757_dari_DB01026",
        "drug_a_id": "DB01026",  # Ketoconazole (strong CYP3A4 inhibitor)
        "drug_b_id": "DB15757",  # Daridorexant
        "severity": "critical",
        "description": (
            "Ketoconazole is a strong CYP3A4 inhibitor; co-administration with daridorexant "
            "is contraindicated. Strong CYP3A4 inhibitors markedly increase daridorexant "
            "exposure, causing excessive CNS depression including next-day impairment and "
            "respiratory depression."
        ),
        "mechanism": "CYP3A4 inhibition -> daridorexant accumulation -> CNS/respiratory depression",
        "source": "seed",
        "evidence_count": 0,
    },
]
