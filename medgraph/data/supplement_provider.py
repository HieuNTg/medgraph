"""Top supplements with known CYP450 and drug-drug interactions.

Returns structured data compatible with MEDGRAPH seed format.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Supplement drug records  (category = "supplement")
# ---------------------------------------------------------------------------

SUPPLEMENT_DRUGS: list[dict] = [
    {
        "id": "SUPP-SJW",
        "name": "St. John's Wort",
        "brand_names": ["Hypericum", "Kira", "Perika"],
        "description": (
            "Herbal antidepressant. Potent inducer of CYP3A4, CYP2C9, CYP1A2, and P-glycoprotein. "
            "Dramatically reduces plasma levels of many drugs."
        ),
        "drug_class": "Herbal / Antidepressant",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": "N06AP",
    },
    {
        "id": "SUPP-GIN",
        "name": "Ginkgo biloba",
        "brand_names": ["Ginkgold", "Ginkoba"],
        "description": (
            "Herbal cognitive enhancer. Inhibits platelet activating factor. "
            "May inhibit CYP2C19 and induce CYP2C9. Increases bleeding risk with anticoagulants."
        ),
        "drug_class": "Herbal / Nootropic",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-TUR",
        "name": "Turmeric / Curcumin",
        "brand_names": ["Meriva", "CurcuWIN"],
        "description": (
            "Anti-inflammatory spice supplement. Inhibits CYP1A2, CYP3A4, and P-glycoprotein "
            "at high doses. May increase bioavailability of CYP3A4 substrates."
        ),
        "drug_class": "Herbal / Anti-inflammatory",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-GRF",
        "name": "Grapefruit",
        "brand_names": [],
        "description": (
            "Food/supplement. Potent intestinal CYP3A4 inhibitor via furanocoumarins. "
            "Can raise plasma levels of CYP3A4 substrates by 2–15x. Effect lasts 24–72 hours."
        ),
        "drug_class": "Food / CYP3A4 Inhibitor",
        "rxnorm_cui": None,
        "category": "food",
        "atc_code": None,
    },
    {
        "id": "SUPP-GAR",
        "name": "Garlic",
        "brand_names": ["Kwai", "Kyolic"],
        "description": (
            "Herbal supplement. Mild CYP3A4 inducer. Has antiplatelet properties; "
            "may increase bleeding risk with warfarin."
        ),
        "drug_class": "Herbal / Antiplatelet",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-GNS",
        "name": "Ginseng",
        "brand_names": ["Ginsana", "Panax ginseng"],
        "description": (
            "Adaptogenic herbal supplement. May inhibit CYP3A4 and CYP2D6. "
            "Antiplatelet effects increase bleeding risk with warfarin and NSAIDs."
        ),
        "drug_class": "Herbal / Adaptogen",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-ECH",
        "name": "Echinacea",
        "brand_names": ["Echinacea purpurea", "EchinaGuard"],
        "description": (
            "Immunostimulant herb. Inhibits CYP3A4 and CYP1A2. May reduce "
            "bioavailability of some immunosuppressants. Can attenuate "
            "immunosuppressive therapy (e.g., cyclosporine)."
        ),
        "drug_class": "Herbal / Immunostimulant",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-VAL",
        "name": "Valerian",
        "brand_names": ["Valeriana officinalis"],
        "description": (
            "Herbal sedative. May inhibit CYP3A4 and potentiate CNS depressants. "
            "Additive sedation with benzodiazepines, alcohol, and opioids."
        ),
        "drug_class": "Herbal / Sedative",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-KAV",
        "name": "Kava",
        "brand_names": ["Piper methysticum", "Kavatrol"],
        "description": (
            "Anxiolytic herbal supplement. Inhibits CYP2E1, CYP1A2, CYP3A4, and CYP2D6. "
            "Hepatotoxic potential; potentiates CNS depressants."
        ),
        "drug_class": "Herbal / Anxiolytic",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-MLK",
        "name": "Milk Thistle",
        "brand_names": ["Silymarin", "Legalon"],
        "description": (
            "Hepatoprotective herb. Inhibits CYP2C9 and CYP3A4 at high doses. "
            "May modestly increase levels of drugs metabolized by these enzymes."
        ),
        "drug_class": "Herbal / Hepatoprotective",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-BCO",
        "name": "Black Cohosh",
        "brand_names": ["Remifemin", "Actaea racemosa"],
        "description": (
            "Herbal menopause supplement. Inhibits CYP3A4 and may have estrogenic effects. "
            "Potential interaction with hormone therapies and tamoxifen."
        ),
        "drug_class": "Herbal / Phytoestrogen",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-SAW",
        "name": "Saw Palmetto",
        "brand_names": ["Serenoa repens"],
        "description": (
            "Herbal BPH supplement. Mild CYP2D6 inhibitor. Antiplatelet activity "
            "may increase bleeding risk with anticoagulants."
        ),
        "drug_class": "Herbal / Urologic",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-COQ",
        "name": "Coenzyme Q10",
        "brand_names": ["CoQ10", "Ubiquinol"],
        "description": (
            "Mitochondrial cofactor supplement. Structurally similar to vitamin K; "
            "may reduce warfarin anticoagulant effect. Generally well tolerated."
        ),
        "drug_class": "Supplement / Antioxidant",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-VIT-E",
        "name": "Vitamin E",
        "brand_names": ["Alpha-tocopherol"],
        "description": (
            "Fat-soluble antioxidant vitamin. At high doses (>400 IU/day) inhibits "
            "platelet aggregation and may potentiate warfarin anticoagulation."
        ),
        "drug_class": "Supplement / Vitamin",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-FISH",
        "name": "Fish Oil / Omega-3",
        "brand_names": ["Lovaza", "Nordic Naturals"],
        "description": (
            "Omega-3 fatty acid supplement. Antiplatelet at high doses (>3 g/day). "
            "May increase bleeding time; monitor with anticoagulants."
        ),
        "drug_class": "Supplement / Fatty Acid",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-MEL",
        "name": "Melatonin",
        "brand_names": [],
        "description": (
            "Endogenous sleep hormone. Metabolized by CYP1A2. Fluvoxamine and other "
            "CYP1A2 inhibitors dramatically raise melatonin levels."
        ),
        "drug_class": "Supplement / Hormone",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-KAVA2",
        "name": "5-HTP",
        "brand_names": ["Griffonia simplicifolia"],
        "description": (
            "Serotonin precursor supplement. Risk of serotonin syndrome when combined "
            "with SSRIs, SNRIs, MAOIs, or triptans."
        ),
        "drug_class": "Supplement / Serotonergic",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-MACA",
        "name": "Maca",
        "brand_names": ["Lepidium meyenii"],
        "description": (
            "Andean adaptogen supplement. May inhibit CYP3A4 mildly. "
            "Limited clinical data on drug interactions."
        ),
        "drug_class": "Herbal / Adaptogen",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
    {
        "id": "SUPP-POME",
        "name": "Pomegranate",
        "brand_names": [],
        "description": (
            "Food supplement. Inhibits CYP3A4 and CYP2C9. May increase plasma levels "
            "of statins, warfarin, and other substrates similarly to grapefruit."
        ),
        "drug_class": "Food / CYP Inhibitor",
        "rxnorm_cui": None,
        "category": "food",
        "atc_code": None,
    },
    {
        "id": "SUPP-GREE",
        "name": "Green Tea Extract",
        "brand_names": ["EGCG", "Camellia sinensis"],
        "description": (
            "Polyphenol antioxidant supplement. Inhibits CYP3A4 and P-glycoprotein at high doses. "
            "May reduce bioavailability of some drugs."
        ),
        "drug_class": "Herbal / Antioxidant",
        "rxnorm_cui": None,
        "category": "supplement",
        "atc_code": None,
    },
]

# ---------------------------------------------------------------------------
# Supplement enzyme relations
# ---------------------------------------------------------------------------

SUPPLEMENT_ENZYME_RELATIONS: list[dict] = [
    # St. John's Wort — strong CYP3A4 inducer
    {
        "drug_id": "SUPP-SJW",
        "enzyme_id": "CYP3A4",
        "relation_type": "induces",
        "strength": "strong",
    },
    {
        "drug_id": "SUPP-SJW",
        "enzyme_id": "CYP2C9",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "SUPP-SJW",
        "enzyme_id": "CYP1A2",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "SUPP-SJW",
        "enzyme_id": "PGLYCO",
        "relation_type": "induces",
        "strength": "strong",
    },
    # Ginkgo biloba
    {
        "drug_id": "SUPP-GIN",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {"drug_id": "SUPP-GIN", "enzyme_id": "CYP2C9", "relation_type": "induces", "strength": "weak"},
    # Turmeric / Curcumin
    {
        "drug_id": "SUPP-TUR",
        "enzyme_id": "CYP1A2",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {"drug_id": "SUPP-TUR", "enzyme_id": "CYP3A4", "relation_type": "inhibits", "strength": "weak"},
    {
        "drug_id": "SUPP-TUR",
        "enzyme_id": "PGLYCO",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Grapefruit — potent intestinal CYP3A4 inhibitor
    {
        "drug_id": "SUPP-GRF",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    # Garlic
    {"drug_id": "SUPP-GAR", "enzyme_id": "CYP3A4", "relation_type": "induces", "strength": "weak"},
    # Ginseng
    {"drug_id": "SUPP-GNS", "enzyme_id": "CYP3A4", "relation_type": "inhibits", "strength": "weak"},
    {"drug_id": "SUPP-GNS", "enzyme_id": "CYP2D6", "relation_type": "inhibits", "strength": "weak"},
    # Echinacea
    {
        "drug_id": "SUPP-ECH",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {"drug_id": "SUPP-ECH", "enzyme_id": "CYP1A2", "relation_type": "inhibits", "strength": "weak"},
    # Valerian
    {"drug_id": "SUPP-VAL", "enzyme_id": "CYP3A4", "relation_type": "inhibits", "strength": "weak"},
    # Kava
    {
        "drug_id": "SUPP-KAV",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "SUPP-KAV",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "SUPP-KAV",
        "enzyme_id": "CYP1A2",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Milk Thistle
    {"drug_id": "SUPP-MLK", "enzyme_id": "CYP2C9", "relation_type": "inhibits", "strength": "weak"},
    {"drug_id": "SUPP-MLK", "enzyme_id": "CYP3A4", "relation_type": "inhibits", "strength": "weak"},
    # Saw Palmetto
    {"drug_id": "SUPP-SAW", "enzyme_id": "CYP2D6", "relation_type": "inhibits", "strength": "weak"},
    # Melatonin — CYP1A2 substrate
    {
        "drug_id": "SUPP-MEL",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Green Tea Extract
    {
        "drug_id": "SUPP-GREE",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "weak",
    },
    {
        "drug_id": "SUPP-GREE",
        "enzyme_id": "PGLYCO",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Pomegranate
    {
        "drug_id": "SUPP-POME",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "SUPP-POME",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
]

# ---------------------------------------------------------------------------
# Supplement-drug interactions
# ---------------------------------------------------------------------------

SUPPLEMENT_INTERACTIONS: list[dict] = [
    # St. John's Wort + Warfarin — CYP induction, reduced anticoagulation
    {
        "id": "INT-SJW-WAR",
        "drug_a_id": "SUPP-SJW",
        "drug_b_id": "DB00682",
        "severity": "major",
        "description": (
            "St. John's Wort induces CYP2C9 and P-glycoprotein, dramatically reducing "
            "warfarin plasma levels by 25–50%. Subtherapeutic anticoagulation and thromboembolic "
            "events have been reported. Combination should be avoided."
        ),
        "mechanism": "CYP2C9 and P-gp induction by St. John's Wort -> reduced warfarin AUC",
        "source": "seed",
        "evidence_count": 1800,
        "evidence_level": "B",
        "clinical_significance": "Avoid combination; monitor INR closely if unavoidable",
    },
    # St. John's Wort + Cyclosporine — organ rejection risk
    {
        "id": "INT-SJW-CYCLO",
        "drug_a_id": "SUPP-SJW",
        "drug_b_id": "DB00091",
        "severity": "critical",
        "description": (
            "St. John's Wort dramatically reduces cyclosporine levels via CYP3A4 and P-gp induction, "
            "risking acute transplant rejection. Multiple case reports of organ rejection documented."
        ),
        "mechanism": "CYP3A4 and P-gp induction -> 50-70% reduction in cyclosporine AUC",
        "source": "seed",
        "evidence_count": 420,
        "evidence_level": "B",
        "clinical_significance": "Contraindicated in transplant patients",
    },
    # Ginkgo + Warfarin — bleeding risk
    {
        "id": "INT-GIN-WAR",
        "drug_a_id": "SUPP-GIN",
        "drug_b_id": "DB00682",
        "severity": "major",
        "description": (
            "Ginkgo biloba inhibits platelet activating factor and may inhibit CYP2C19. "
            "Case reports of spontaneous bleeding (intracranial, ocular) with concurrent warfarin use."
        ),
        "mechanism": "Pharmacodynamic: additive antiplatelet + possible PK interaction via CYP2C19",
        "source": "seed",
        "evidence_count": 310,
        "evidence_level": "C",
        "clinical_significance": "Monitor INR; use with caution",
    },
    # Grapefruit + Simvastatin — rhabdomyolysis risk
    {
        "id": "INT-GRF-SIMV",
        "drug_a_id": "SUPP-GRF",
        "drug_b_id": "DB00641",
        "severity": "major",
        "description": (
            "Grapefruit furanocoumarins inhibit intestinal CYP3A4, increasing simvastatin AUC "
            "by up to 15-fold. Risk of myopathy and rhabdomyolysis. FDA labeling warns against "
            "consuming large quantities of grapefruit juice with simvastatin."
        ),
        "mechanism": "Intestinal CYP3A4 inhibition by furanocoumarins -> marked statin accumulation",
        "source": "seed",
        "evidence_count": 2200,
        "evidence_level": "A",
        "clinical_significance": "Avoid grapefruit with simvastatin; use pravastatin or rosuvastatin",
    },
    # Grapefruit + Atorvastatin
    {
        "id": "INT-GRF-ATOR",
        "drug_a_id": "SUPP-GRF",
        "drug_b_id": "DB01076",
        "severity": "moderate",
        "description": (
            "Grapefruit inhibits CYP3A4, increasing atorvastatin AUC by ~1.5–2.5x. "
            "Modest increase in myopathy risk. Occasional consumption unlikely to cause harm; "
            "large daily quantities should be avoided."
        ),
        "mechanism": "CYP3A4 inhibition -> increased atorvastatin exposure",
        "source": "seed",
        "evidence_count": 1200,
        "evidence_level": "B",
        "clinical_significance": "Avoid large amounts of grapefruit; single servings generally acceptable",
    },
    # Grapefruit + Midazolam
    {
        "id": "INT-GRF-MID",
        "drug_a_id": "SUPP-GRF",
        "drug_b_id": "DB00625",
        "severity": "major",
        "description": (
            "Grapefruit significantly increases midazolam bioavailability via CYP3A4 inhibition. "
            "Prolonged and unpredictable sedation may result."
        ),
        "mechanism": "Intestinal CYP3A4 inhibition -> midazolam accumulation",
        "source": "seed",
        "evidence_count": 650,
        "evidence_level": "B",
        "clinical_significance": "Avoid grapefruit around midazolam administration",
    },
    # Garlic + Warfarin — bleeding
    {
        "id": "INT-GAR-WAR",
        "drug_a_id": "SUPP-GAR",
        "drug_b_id": "DB00682",
        "severity": "moderate",
        "description": (
            "Garlic supplements have antiplatelet properties and may mildly reduce warfarin "
            "metabolism via CYP3A4 induction at high doses. Monitor INR with high-dose garlic."
        ),
        "mechanism": "Antiplatelet pharmacodynamics + possible CYP3A4 modulation",
        "source": "seed",
        "evidence_count": 280,
        "evidence_level": "C",
        "clinical_significance": "Monitor INR with high-dose garlic supplements",
    },
    # Valerian + Benzodiazepines — additive CNS depression
    {
        "id": "INT-VAL-DIAZ",
        "drug_a_id": "SUPP-VAL",
        "drug_b_id": "DB00829",
        "severity": "moderate",
        "description": (
            "Valerian enhances GABA-A receptor activity. Concurrent use with benzodiazepines "
            "may produce additive CNS depression, excessive sedation, and respiratory depression risk."
        ),
        "mechanism": "Pharmacodynamic synergy at GABA-A receptors",
        "source": "seed",
        "evidence_count": 160,
        "evidence_level": "C",
        "clinical_significance": "Caution: additive sedation; avoid in elderly or respiratory compromised",
    },
    # Kava + CNS depressants
    {
        "id": "INT-KAV-DIAZ",
        "drug_a_id": "SUPP-KAV",
        "drug_b_id": "DB00829",
        "severity": "major",
        "description": (
            "Kava inhibits multiple CYP enzymes and has intrinsic CNS depressant activity. "
            "Potentiates benzodiazepines and alcohol. Cases of coma reported."
        ),
        "mechanism": "CYP2D6/3A4 inhibition + pharmacodynamic CNS synergy",
        "source": "seed",
        "evidence_count": 95,
        "evidence_level": "C",
        "clinical_significance": "Avoid combination; especially in patients on multiple CNS depressants",
    },
    # 5-HTP + SSRIs — serotonin syndrome
    {
        "id": "INT-5HTP-FLX",
        "drug_a_id": "SUPP-KAVA2",
        "drug_b_id": "DB00472",
        "severity": "major",
        "description": (
            "5-HTP is a direct serotonin precursor. Combined with SSRIs like fluoxetine, "
            "excess serotonergic activity may lead to serotonin syndrome: "
            "hyperthermia, agitation, clonus, and autonomic instability."
        ),
        "mechanism": "Pharmacodynamic: excess serotonin synthesis + SSRI-mediated serotonin retention",
        "source": "seed",
        "evidence_count": 140,
        "evidence_level": "C",
        "clinical_significance": "Avoid; risk of serotonin syndrome",
    },
    # Vitamin E + Warfarin
    {
        "id": "INT-VITE-WAR",
        "drug_a_id": "SUPP-VIT-E",
        "drug_b_id": "DB00682",
        "severity": "moderate",
        "description": (
            "High-dose vitamin E (>400 IU/day) has antiplatelet activity and may potentiate "
            "warfarin anticoagulation. Case reports of elevated INR with supplementation."
        ),
        "mechanism": "Antiplatelet pharmacodynamics + possible vitamin K antagonism at high doses",
        "source": "seed",
        "evidence_count": 380,
        "evidence_level": "C",
        "clinical_significance": "Monitor INR if starting high-dose vitamin E with warfarin",
    },
    # Fish Oil + Warfarin
    {
        "id": "INT-FISH-WAR",
        "drug_a_id": "SUPP-FISH",
        "drug_b_id": "DB00682",
        "severity": "minor",
        "description": (
            "Omega-3 fatty acids at doses >3 g/day may modestly increase bleeding time "
            "and potentiate warfarin. Clinical significance at typical supplement doses is low."
        ),
        "mechanism": "Antiplatelet pharmacodynamics at high doses",
        "source": "seed",
        "evidence_count": 520,
        "evidence_level": "B",
        "clinical_significance": "Monitor INR with doses >3 g/day; typical dietary intake is low risk",
    },
    # Echinacea + Cyclosporine
    {
        "id": "INT-ECH-CYCLO",
        "drug_a_id": "SUPP-ECH",
        "drug_b_id": "DB00091",
        "severity": "major",
        "description": (
            "Echinacea immunostimulation may counteract cyclosporine immunosuppression. "
            "Additionally, echinacea inhibits CYP3A4, potentially altering cyclosporine levels."
        ),
        "mechanism": "Pharmacodynamic antagonism + CYP3A4 inhibition",
        "source": "seed",
        "evidence_count": 75,
        "evidence_level": "C",
        "clinical_significance": "Contraindicated in transplant or immunosuppressed patients",
    },
    # Turmeric + Warfarin
    {
        "id": "INT-TUR-WAR",
        "drug_a_id": "SUPP-TUR",
        "drug_b_id": "DB00682",
        "severity": "moderate",
        "description": (
            "High-dose curcumin inhibits CYP1A2 and has antiplatelet effects, "
            "potentially potentiating warfarin anticoagulation. Monitor INR with high-dose supplementation."
        ),
        "mechanism": "CYP1A2 inhibition + antiplatelet pharmacodynamics",
        "source": "seed",
        "evidence_count": 210,
        "evidence_level": "C",
        "clinical_significance": "Monitor INR with high-dose curcumin supplements",
    },
    # CoQ10 + Warfarin — may reduce effect
    {
        "id": "INT-COQ-WAR",
        "drug_a_id": "SUPP-COQ",
        "drug_b_id": "DB00682",
        "severity": "moderate",
        "description": (
            "CoQ10 is structurally similar to vitamin K and may reduce warfarin's anticoagulant effect. "
            "Case reports of decreased INR requiring warfarin dose increases."
        ),
        "mechanism": "Possible vitamin K-like activity reducing anticoagulant response",
        "source": "seed",
        "evidence_count": 175,
        "evidence_level": "C",
        "clinical_significance": "Monitor INR when starting or stopping CoQ10 supplementation",
    },
    # Melatonin + Fluvoxamine — massive melatonin increase
    {
        "id": "INT-MEL-FLV",
        "drug_a_id": "SUPP-MEL",
        "drug_b_id": "DB00196",
        "severity": "moderate",
        "description": (
            "Fluvoxamine is a potent CYP1A2 inhibitor. Melatonin is primarily metabolized by CYP1A2. "
            "Concurrent use raises melatonin plasma levels 17-fold. "
            "Profound sedation and circadian disruption may result."
        ),
        "mechanism": "CYP1A2 inhibition by fluvoxamine -> massive melatonin accumulation",
        "source": "seed",
        "evidence_count": 290,
        "evidence_level": "B",
        "clinical_significance": "Reduce melatonin dose substantially or avoid with fluvoxamine",
    },
    # Pomegranate + Warfarin
    {
        "id": "INT-POME-WAR",
        "drug_a_id": "SUPP-POME",
        "drug_b_id": "DB00682",
        "severity": "moderate",
        "description": (
            "Pomegranate juice inhibits CYP2C9, the primary enzyme metabolizing warfarin. "
            "May significantly increase warfarin plasma levels and INR."
        ),
        "mechanism": "CYP2C9 inhibition -> reduced warfarin clearance",
        "source": "seed",
        "evidence_count": 180,
        "evidence_level": "C",
        "clinical_significance": "Monitor INR; limit pomegranate consumption",
    },
    # Black Cohosh + Tamoxifen
    {
        "id": "INT-BCO-TAM",
        "drug_a_id": "SUPP-BCO",
        "drug_b_id": "DB00675",
        "severity": "moderate",
        "description": (
            "Black cohosh may have estrogenic effects and inhibit CYP3A4. "
            "Theoretical risk of reducing tamoxifen efficacy in hormone-receptor positive breast cancer."
        ),
        "mechanism": "Possible estrogenic agonism + CYP3A4 inhibition altering tamoxifen metabolism",
        "source": "seed",
        "evidence_count": 120,
        "evidence_level": "D",
        "clinical_significance": "Avoid in hormone-receptor positive breast cancer patients on tamoxifen",
    },
    # Ginseng + Warfarin
    {
        "id": "INT-GNS-WAR",
        "drug_a_id": "SUPP-GNS",
        "drug_b_id": "DB00682",
        "severity": "moderate",
        "description": (
            "Ginseng has antiplatelet properties and may reduce warfarin plasma levels. "
            "One clinical study showed 34% reduction in warfarin AUC with Panax ginseng."
        ),
        "mechanism": "Antiplatelet effect + possible CYP2C9 induction",
        "source": "seed",
        "evidence_count": 340,
        "evidence_level": "B",
        "clinical_significance": "Monitor INR; some studies show reduced warfarin efficacy",
    },
    # Milk Thistle + Warfarin (minor)
    {
        "id": "INT-MLK-WAR",
        "drug_a_id": "SUPP-MLK",
        "drug_b_id": "DB00682",
        "severity": "minor",
        "description": (
            "Milk thistle mildly inhibits CYP2C9 at high doses. Clinical studies show minimal "
            "effect on warfarin pharmacokinetics at standard supplement doses."
        ),
        "mechanism": "Weak CYP2C9 inhibition at high doses",
        "source": "seed",
        "evidence_count": 195,
        "evidence_level": "C",
        "clinical_significance": "Low clinical significance at typical doses; monitor INR at high doses",
    },
    # Green Tea + Warfarin
    {
        "id": "INT-GREE-WAR",
        "drug_a_id": "SUPP-GREE",
        "drug_b_id": "DB00682",
        "severity": "minor",
        "description": (
            "Green tea contains vitamin K, which may antagonize warfarin. High-volume "
            "consumption or extract supplements may reduce anticoagulant effect."
        ),
        "mechanism": "Vitamin K content antagonizing warfarin mechanism",
        "source": "seed",
        "evidence_count": 260,
        "evidence_level": "C",
        "clinical_significance": "Consistent moderate intake acceptable; avoid large quantity changes",
    },
]


def get_supplement_data() -> dict[str, list[dict]]:
    return {
        "drugs": SUPPLEMENT_DRUGS,
        "enzyme_relations": SUPPLEMENT_ENZYME_RELATIONS,
        "interactions": SUPPLEMENT_INTERACTIONS,
    }
