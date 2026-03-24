"""
CPIC Pharmacogenomics Guidelines seed data.

Based on Clinical Pharmacogenetics Implementation Consortium (CPIC) guidelines.
Source: https://cpicpgx.org/guidelines/

Drug IDs use the MEDGRAPH DrugBank-style IDs present in seed_data.py /
seed_drugs_expanded.py / seed_drugs_extended.py.  See SUPPLEMENTARY_DRUGS
below for drugs that required new entries.
"""

from __future__ import annotations

# Mapping from CPIC drug name -> MEDGRAPH drug_id
# Derived by reading seed_data.py, seed_drugs_expanded.py, seed_drugs_extended.py
_ID = {
    "codeine": "DB00318",
    "tramadol": "DB00715",
    "clopidogrel": "DB00758",
    "omeprazole": "DB00338",
    "warfarin": "DB00682",
    "tamoxifen": "DB00675",
    "voriconazole": "DB00625_vori",
    "paroxetine": "DB00715_par",
    "escitalopram": "DB01175",
    "citalopram": "DB01104_escit",
    "simvastatin": "DB00641",
    "atomoxetine": "DB00289",  # new — see SUPPLEMENTARY_DRUGS
    "fluorouracil": "DB00544",  # new — see SUPPLEMENTARY_DRUGS
    "capecitabine": "DB01101",  # new — see SUPPLEMENTARY_DRUGS
    "azathioprine": "DB00993",  # new — see SUPPLEMENTARY_DRUGS
    "mercaptopurine": "DB01033",  # new — see SUPPLEMENTARY_DRUGS
    "irinotecan": "DB00762",  # new — see SUPPLEMENTARY_DRUGS
    "abacavir": "DB01048",
    "carbamazepine": "DB00564",
    "allopurinol": "DB01014",
    "efavirenz": "DB00625_efv",
    "celecoxib": "DB00461",
    "phenytoin": "DB00252",
}

CPIC_GUIDELINES: list[dict] = [
    # CYP2D6 — Codeine
    {
        "drug_id": _ID["codeine"],
        "gene_id": "CYP2D6",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Avoid codeine. Use non-tramadol analgesic. Poor metabolizers cannot convert "
            "codeine to morphine, resulting in no analgesic effect."
        ),
        "severity_multiplier": 0.3,
    },
    {
        "drug_id": _ID["codeine"],
        "gene_id": "CYP2D6",
        "phenotype": "ultrarapid_metabolizer",
        "recommendation": (
            "Avoid codeine. Ultrarapid metabolizers convert codeine to morphine too quickly, "
            "risking respiratory depression and death."
        ),
        "severity_multiplier": 2.5,
    },
    {
        "drug_id": _ID["codeine"],
        "gene_id": "CYP2D6",
        "phenotype": "normal_metabolizer",
        "recommendation": "Standard dosing appropriate.",
        "severity_multiplier": 1.0,
    },
    {
        "drug_id": _ID["codeine"],
        "gene_id": "CYP2D6",
        "phenotype": "intermediate_metabolizer",
        "recommendation": "Use with caution. Consider reduced dose or alternative analgesic.",
        "severity_multiplier": 0.7,
    },
    # CYP2D6 — Tramadol
    {
        "drug_id": _ID["tramadol"],
        "gene_id": "CYP2D6",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Consider alternative analgesic. Reduced formation of active metabolite "
            "O-desmethyltramadol."
        ),
        "severity_multiplier": 0.5,
    },
    {
        "drug_id": _ID["tramadol"],
        "gene_id": "CYP2D6",
        "phenotype": "ultrarapid_metabolizer",
        "recommendation": (
            "Avoid tramadol. Risk of respiratory depression due to rapid conversion to "
            "active metabolite."
        ),
        "severity_multiplier": 2.0,
    },
    # CYP2C19 — Clopidogrel
    {
        "drug_id": _ID["clopidogrel"],
        "gene_id": "CYP2C19",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Use alternative antiplatelet (e.g., prasugrel, ticagrelor). Poor metabolizers "
            "have significantly reduced clopidogrel activation."
        ),
        "severity_multiplier": 2.0,
    },
    {
        "drug_id": _ID["clopidogrel"],
        "gene_id": "CYP2C19",
        "phenotype": "intermediate_metabolizer",
        "recommendation": (
            "Consider alternative antiplatelet therapy. Reduced but not absent clopidogrel "
            "activation."
        ),
        "severity_multiplier": 1.5,
    },
    {
        "drug_id": _ID["clopidogrel"],
        "gene_id": "CYP2C19",
        "phenotype": "normal_metabolizer",
        "recommendation": "Standard dosing appropriate.",
        "severity_multiplier": 1.0,
    },
    {
        "drug_id": _ID["clopidogrel"],
        "gene_id": "CYP2C19",
        "phenotype": "rapid_metabolizer",
        "recommendation": "Standard dosing appropriate.",
        "severity_multiplier": 1.0,
    },
    # CYP2C19 — Omeprazole / PPIs
    {
        "drug_id": _ID["omeprazole"],
        "gene_id": "CYP2C19",
        "phenotype": "ultrarapid_metabolizer",
        "recommendation": (
            "Increase dose by 100-200% or use alternative PPI. Ultrarapid metabolizers "
            "may have inadequate acid suppression."
        ),
        "severity_multiplier": 1.5,
    },
    {
        "drug_id": _ID["omeprazole"],
        "gene_id": "CYP2C19",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Consider 50% dose reduction for long-term use. Increased exposure may raise "
            "side effect risk."
        ),
        "severity_multiplier": 1.3,
    },
    # CYP2C9 + VKORC1 — Warfarin
    {
        "drug_id": _ID["warfarin"],
        "gene_id": "CYP2C9",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Reduce initial dose by 50-80%. CYP2C9 poor metabolizers clear S-warfarin "
            "slowly, significantly increasing bleeding risk."
        ),
        "severity_multiplier": 2.5,
    },
    {
        "drug_id": _ID["warfarin"],
        "gene_id": "CYP2C9",
        "phenotype": "intermediate_metabolizer",
        "recommendation": ("Reduce initial dose by 20-40%. Monitor INR closely during initiation."),
        "severity_multiplier": 1.5,
    },
    {
        "drug_id": _ID["warfarin"],
        "gene_id": "VKORC1",
        "phenotype": "high_sensitivity",
        "recommendation": (
            "Reduce initial dose. VKORC1 variant associated with increased warfarin "
            "sensitivity and higher bleeding risk."
        ),
        "severity_multiplier": 2.0,
    },
    {
        "drug_id": _ID["warfarin"],
        "gene_id": "VKORC1",
        "phenotype": "low_sensitivity",
        "recommendation": "May require higher doses. Monitor INR and adjust accordingly.",
        "severity_multiplier": 0.8,
    },
    # CYP2D6 — Tamoxifen
    {
        "drug_id": _ID["tamoxifen"],
        "gene_id": "CYP2D6",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Consider aromatase inhibitor instead. Poor metabolizers have reduced conversion "
            "to active endoxifen, potentially reducing efficacy."
        ),
        "severity_multiplier": 2.0,
    },
    {
        "drug_id": _ID["tamoxifen"],
        "gene_id": "CYP2D6",
        "phenotype": "intermediate_metabolizer",
        "recommendation": (
            "Consider higher dose or alternative. Reduced but not absent endoxifen formation."
        ),
        "severity_multiplier": 1.5,
    },
    # CYP2C19 — Voriconazole
    {
        "drug_id": _ID["voriconazole"],
        "gene_id": "CYP2C19",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Use standard dose but monitor for toxicity. Poor metabolizers have 4x higher "
            "voriconazole exposure."
        ),
        "severity_multiplier": 1.8,
    },
    {
        "drug_id": _ID["voriconazole"],
        "gene_id": "CYP2C19",
        "phenotype": "ultrarapid_metabolizer",
        "recommendation": (
            "Use alternative antifungal or titrate to therapeutic drug monitoring. "
            "Risk of subtherapeutic levels."
        ),
        "severity_multiplier": 1.5,
    },
    # CYP2D6 — Paroxetine
    {
        "drug_id": _ID["paroxetine"],
        "gene_id": "CYP2D6",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Consider 50% dose reduction. Significantly increased paroxetine exposure "
            "in poor metabolizers."
        ),
        "severity_multiplier": 1.5,
    },
    {
        "drug_id": _ID["paroxetine"],
        "gene_id": "CYP2D6",
        "phenotype": "ultrarapid_metabolizer",
        "recommendation": (
            "Consider alternative SSRI not primarily metabolized by CYP2D6 "
            "(e.g., sertraline, escitalopram)."
        ),
        "severity_multiplier": 1.3,
    },
    # CYP2C19 — Escitalopram
    {
        "drug_id": _ID["escitalopram"],
        "gene_id": "CYP2C19",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Reduce dose by 50%. Poor metabolizers have significantly increased SSRI exposure."
        ),
        "severity_multiplier": 1.5,
    },
    # CYP2C19 — Citalopram
    {
        "drug_id": _ID["citalopram"],
        "gene_id": "CYP2C19",
        "phenotype": "poor_metabolizer",
        "recommendation": ("Reduce dose by 50%. Do not exceed 20 mg/day. QT prolongation risk."),
        "severity_multiplier": 1.8,
    },
    {
        "drug_id": _ID["citalopram"],
        "gene_id": "CYP2C19",
        "phenotype": "ultrarapid_metabolizer",
        "recommendation": (
            "Consider alternative SSRI. May need higher doses for therapeutic effect."
        ),
        "severity_multiplier": 1.2,
    },
    # CYP3A4 — Simvastatin
    {
        "drug_id": _ID["simvastatin"],
        "gene_id": "CYP3A4",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Reduce dose or use alternative statin (rosuvastatin, pravastatin). "
            "Elevated rhabdomyolysis risk."
        ),
        "severity_multiplier": 2.0,
    },
    # CYP2D6 — Atomoxetine
    {
        "drug_id": _ID["atomoxetine"],
        "gene_id": "CYP2D6",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Reduce initial dose to 0.5 mg/kg/day. Titrate slowly. Poor metabolizers "
            "have 10x higher AUC."
        ),
        "severity_multiplier": 1.8,
    },
    # DPYD — Fluorouracil
    {
        "drug_id": _ID["fluorouracil"],
        "gene_id": "DPYD",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "CONTRAINDICATED. Do not administer. DPYD-deficient patients have extreme "
            "toxicity risk including death."
        ),
        "severity_multiplier": 3.0,
    },
    {
        "drug_id": _ID["fluorouracil"],
        "gene_id": "DPYD",
        "phenotype": "intermediate_metabolizer",
        "recommendation": "Reduce dose by 50%. Monitor closely for toxicity.",
        "severity_multiplier": 2.0,
    },
    # DPYD — Capecitabine
    {
        "drug_id": _ID["capecitabine"],
        "gene_id": "DPYD",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "CONTRAINDICATED. Do not administer. Same DPYD pathway as fluorouracil."
        ),
        "severity_multiplier": 3.0,
    },
    # TPMT — Azathioprine
    {
        "drug_id": _ID["azathioprine"],
        "gene_id": "TPMT",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Reduce dose to 10% of standard or use alternative. High risk of severe "
            "myelosuppression."
        ),
        "severity_multiplier": 3.0,
    },
    {
        "drug_id": _ID["azathioprine"],
        "gene_id": "TPMT",
        "phenotype": "intermediate_metabolizer",
        "recommendation": "Reduce starting dose by 30-70%. Monitor blood counts weekly.",
        "severity_multiplier": 1.8,
    },
    # TPMT — Mercaptopurine
    {
        "drug_id": _ID["mercaptopurine"],
        "gene_id": "TPMT",
        "phenotype": "poor_metabolizer",
        "recommendation": ("Reduce dose to 10% of standard. Same TPMT pathway as azathioprine."),
        "severity_multiplier": 3.0,
    },
    # UGT1A1 — Irinotecan
    {
        "drug_id": _ID["irinotecan"],
        "gene_id": "UGT1A1",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Reduce initial dose by at least 30%. Increased risk of severe neutropenia "
            "and diarrhea."
        ),
        "severity_multiplier": 2.0,
    },
    # HLA-B — Abacavir
    {
        "drug_id": _ID["abacavir"],
        "gene_id": "HLA-B",
        "phenotype": "HLA-B*57:01_positive",
        "recommendation": (
            "CONTRAINDICATED. Do not prescribe. HLA-B*57:01 positive patients have high "
            "risk of hypersensitivity reaction."
        ),
        "severity_multiplier": 3.0,
    },
    # HLA-B — Carbamazepine
    {
        "drug_id": _ID["carbamazepine"],
        "gene_id": "HLA-B",
        "phenotype": "HLA-B*15:02_positive",
        "recommendation": (
            "CONTRAINDICATED in HLA-B*15:02 positive patients. High risk of "
            "Stevens-Johnson syndrome/toxic epidermal necrolysis."
        ),
        "severity_multiplier": 3.0,
    },
    # HLA-B — Allopurinol
    {
        "drug_id": _ID["allopurinol"],
        "gene_id": "HLA-B",
        "phenotype": "HLA-B*58:01_positive",
        "recommendation": (
            "CONTRAINDICATED. Use alternative urate-lowering therapy (febuxostat). "
            "High SJS/TEN risk."
        ),
        "severity_multiplier": 3.0,
    },
    # CYP2B6 — Efavirenz
    {
        "drug_id": _ID["efavirenz"],
        "gene_id": "CYP2B6",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Reduce dose to 400mg or consider alternative. Poor metabolizers have 2-3x "
            "higher exposure with increased CNS side effects."
        ),
        "severity_multiplier": 1.5,
    },
    # CYP2C9 — Celecoxib
    {
        "drug_id": _ID["celecoxib"],
        "gene_id": "CYP2C9",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Reduce initial dose by 50%. Poor metabolizers have significantly increased "
            "celecoxib exposure."
        ),
        "severity_multiplier": 1.5,
    },
    # CYP2C9 — Phenytoin
    {
        "drug_id": _ID["phenytoin"],
        "gene_id": "CYP2C9",
        "phenotype": "poor_metabolizer",
        "recommendation": (
            "Reduce dose by 50%. Monitor levels closely. High risk of phenytoin toxicity "
            "in poor metabolizers."
        ),
        "severity_multiplier": 2.0,
    },
    {
        "drug_id": _ID["phenytoin"],
        "gene_id": "CYP2C9",
        "phenotype": "intermediate_metabolizer",
        "recommendation": "Reduce dose by 25%. Monitor drug levels.",
        "severity_multiplier": 1.5,
    },
]

# Ancestry-based CYP allele frequencies for population-aware PGx scoring.
# Source: PharmGKB + CPIC allele frequency tables.
ANCESTRY_ALLELE_FREQUENCIES: dict[str, dict[str, dict[str, float]]] = {
    "CYP2D6": {
        "poor_metabolizer": {
            "european": 0.07,
            "east_asian": 0.01,
            "african": 0.03,
            "south_asian": 0.02,
            "hispanic": 0.03,
            "middle_eastern": 0.03,
        },
        "ultrarapid_metabolizer": {
            "european": 0.02,
            "east_asian": 0.01,
            "african": 0.20,
            "south_asian": 0.05,
            "hispanic": 0.03,
            "middle_eastern": 0.10,
        },
    },
    "CYP2C19": {
        "poor_metabolizer": {
            "european": 0.02,
            "east_asian": 0.15,
            "african": 0.04,
            "south_asian": 0.12,
            "hispanic": 0.02,
            "middle_eastern": 0.02,
        },
        "ultrarapid_metabolizer": {
            "european": 0.25,
            "east_asian": 0.01,
            "african": 0.15,
            "south_asian": 0.10,
            "hispanic": 0.10,
            "middle_eastern": 0.20,
        },
    },
    "CYP2C9": {
        "poor_metabolizer": {
            "european": 0.01,
            "east_asian": 0.001,
            "african": 0.001,
            "south_asian": 0.005,
            "hispanic": 0.005,
            "middle_eastern": 0.008,
        },
    },
    "DPYD": {
        "poor_metabolizer": {
            "european": 0.01,
            "east_asian": 0.001,
            "african": 0.008,
            "south_asian": 0.005,
            "hispanic": 0.005,
            "middle_eastern": 0.005,
        },
    },
    "HLA-B": {
        "HLA-B*57:01_positive": {
            "european": 0.06,
            "east_asian": 0.01,
            "african": 0.01,
            "south_asian": 0.05,
            "hispanic": 0.02,
            "middle_eastern": 0.03,
        },
        "HLA-B*15:02_positive": {
            "european": 0.001,
            "east_asian": 0.08,
            "african": 0.001,
            "south_asian": 0.04,
            "hispanic": 0.001,
            "middle_eastern": 0.001,
        },
        "HLA-B*58:01_positive": {
            "european": 0.01,
            "east_asian": 0.08,
            "african": 0.03,
            "south_asian": 0.02,
            "hispanic": 0.01,
            "middle_eastern": 0.01,
        },
    },
}

# ---------------------------------------------------------------------------
# Supplementary drug entries for drugs referenced in CPIC_GUIDELINES that
# are NOT present in seed_data.py / seed_drugs_expanded.py / seed_drugs_extended.py.
# These are upserted by DataSeeder._seed_cpic_drugs() before guidelines are inserted.
# ---------------------------------------------------------------------------
SUPPLEMENTARY_DRUGS: list[dict] = [
    {
        "id": "DB00289",
        "name": "Atomoxetine",
        "brand_names": ["Strattera"],
        "description": (
            "Selective norepinephrine reuptake inhibitor for ADHD. Almost exclusively "
            "metabolized by CYP2D6. Poor metabolizers have 10x higher AUC; require "
            "dose adjustment. CYP2D6 inhibitors (fluoxetine, paroxetine) can convert "
            "normal metabolizers to a poor-metabolizer phenotype."
        ),
        "drug_class": "SNRI / ADHD Agent",
        "rxnorm_cui": "129490",
    },
    {
        "id": "DB00544",
        "name": "Fluorouracil",
        "brand_names": ["5-FU", "Adrucil", "Efudex"],
        "description": (
            "Fluoropyrimidine antineoplastic. Catabolized by dihydropyrimidine dehydrogenase "
            "(DPYD). DPYD-deficient patients accumulate toxic metabolites; life-threatening "
            "toxicity including mucositis, neutropenia, and neurotoxicity."
        ),
        "drug_class": "Antineoplastic / Fluoropyrimidine",
        "rxnorm_cui": "4492",
    },
    {
        "id": "DB01101",
        "name": "Capecitabine",
        "brand_names": ["Xeloda"],
        "description": (
            "Oral prodrug of fluorouracil. Converted to 5-FU via thymidine phosphorylase. "
            "Same DPYD-dependent catabolism as fluorouracil; DPYD-deficient patients are "
            "at severe toxicity risk."
        ),
        "drug_class": "Antineoplastic / Fluoropyrimidine Prodrug",
        "rxnorm_cui": "150444",
    },
    {
        "id": "DB00993",
        "name": "Azathioprine",
        "brand_names": ["Imuran", "Azasan"],
        "description": (
            "Purine analog immunosuppressant and prodrug of 6-mercaptopurine. Inactivated "
            "by thiopurine methyltransferase (TPMT). TPMT-deficient patients accumulate "
            "cytotoxic thioguanine nucleotides causing fatal myelosuppression."
        ),
        "drug_class": "Immunosuppressant / Thiopurine",
        "rxnorm_cui": "1223",
    },
    {
        "id": "DB01033",
        "name": "Mercaptopurine",
        "brand_names": ["Purinethol", "Purixan"],
        "description": (
            "Thiopurine antineoplastic and immunosuppressant. Inactivated by TPMT. "
            "TPMT poor metabolizers require drastic dose reductions (10% of standard) "
            "to avoid life-threatening myelosuppression."
        ),
        "drug_class": "Antineoplastic / Thiopurine",
        "rxnorm_cui": "4448",
    },
    {
        "id": "DB00762",
        "name": "Irinotecan",
        "brand_names": ["Camptosar"],
        "description": (
            "Topoisomerase I inhibitor antineoplastic. Active metabolite SN-38 is "
            "glucuronidated by UGT1A1. UGT1A1*28 homozygotes (poor metabolizers) have "
            "higher SN-38 exposure and increased risk of severe neutropenia and diarrhea."
        ),
        "drug_class": "Antineoplastic / Topoisomerase I Inhibitor",
        "rxnorm_cui": "51499",
    },
]
