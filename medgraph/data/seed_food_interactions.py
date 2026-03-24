"""
Seed data for drug-food interactions affecting CYP450 metabolism.
Sources: FDA drug labels, clinical pharmacology references.
"""

FOOD_ITEMS = [
    {"id": "food_grapefruit", "name": "Grapefruit / Grapefruit juice", "category": "food", "mechanism": "Irreversible inhibition of intestinal CYP3A4", "affected_enzymes": ["CYP3A4"]},
    {"id": "food_st_johns_wort", "name": "St. John's Wort", "category": "supplement", "mechanism": "Potent CYP3A4 inducer via PXR activation", "affected_enzymes": ["CYP3A4", "CYP2C9", "CYP1A2"]},
    {"id": "food_tobacco_smoke", "name": "Tobacco smoke", "category": "environmental", "mechanism": "Polycyclic aromatic hydrocarbons induce CYP1A2", "affected_enzymes": ["CYP1A2"]},
    {"id": "food_cruciferous", "name": "Cruciferous vegetables (broccoli, Brussels sprouts)", "category": "food", "mechanism": "Indole-3-carbinol induces CYP1A2", "affected_enzymes": ["CYP1A2"]},
    {"id": "food_charbroiled_meat", "name": "Charbroiled/grilled meat", "category": "food", "mechanism": "PAH compounds induce CYP1A2", "affected_enzymes": ["CYP1A2"]},
    {"id": "food_alcohol", "name": "Alcohol (ethanol)", "category": "food", "mechanism": "Acute: inhibits CYP2E1. Chronic: induces CYP2E1 and CYP3A4", "affected_enzymes": ["CYP2E1", "CYP3A4"]},
    {"id": "food_cranberry", "name": "Cranberry juice", "category": "food", "mechanism": "Flavonoids inhibit CYP2C9", "affected_enzymes": ["CYP2C9"]},
    {"id": "food_turmeric", "name": "Turmeric / Curcumin", "category": "supplement", "mechanism": "Inhibits CYP3A4, CYP1A2, CYP2D6", "affected_enzymes": ["CYP3A4", "CYP1A2", "CYP2D6"]},
    {"id": "food_green_tea", "name": "Green tea (high doses)", "category": "food", "mechanism": "EGCG inhibits CYP3A4 and CYP1A2", "affected_enzymes": ["CYP3A4", "CYP1A2"]},
    {"id": "food_pomegranate", "name": "Pomegranate juice", "category": "food", "mechanism": "Inhibits CYP3A4 and CYP2C9", "affected_enzymes": ["CYP3A4", "CYP2C9"]},
    {"id": "food_black_pepper", "name": "Black pepper (piperine)", "category": "food", "mechanism": "Inhibits CYP3A4, CYP2D6, and P-glycoprotein", "affected_enzymes": ["CYP3A4", "CYP2D6"]},
    {"id": "food_milk_thistle", "name": "Milk thistle (silymarin)", "category": "supplement", "mechanism": "Inhibits CYP2C9 and CYP3A4", "affected_enzymes": ["CYP2C9", "CYP3A4"]},
]

# Known clinically significant drug-food interaction pairs
FOOD_DRUG_INTERACTIONS = [
    {"food_id": "food_grapefruit", "drug_name": "Simvastatin", "severity": "critical", "description": "Grapefruit juice irreversibly inhibits intestinal CYP3A4, increasing simvastatin AUC by 260%. Risk of rhabdomyolysis.", "evidence_level": "A"},
    {"food_id": "food_grapefruit", "drug_name": "Cyclosporine", "severity": "critical", "description": "Grapefruit inhibits CYP3A4-mediated first-pass metabolism of cyclosporine. Plasma levels increase 20-200%. Risk of nephrotoxicity.", "evidence_level": "A"},
    {"food_id": "food_grapefruit", "drug_name": "Felodipine", "severity": "major", "description": "Grapefruit juice increases felodipine bioavailability 3-fold via CYP3A4 inhibition. Risk of hypotension.", "evidence_level": "A"},
    {"food_id": "food_grapefruit", "drug_name": "Atorvastatin", "severity": "major", "description": "Grapefruit juice increases atorvastatin AUC by 80% via CYP3A4 inhibition. Monitor for myopathy.", "evidence_level": "A"},
    {"food_id": "food_grapefruit", "drug_name": "Buspirone", "severity": "major", "description": "Grapefruit juice increases buspirone plasma levels 9-fold via CYP3A4 inhibition.", "evidence_level": "B"},
    {"food_id": "food_st_johns_wort", "drug_name": "Cyclosporine", "severity": "critical", "description": "St. John's Wort induces CYP3A4, reducing cyclosporine levels by 40-60%. Risk of organ rejection.", "evidence_level": "A"},
    {"food_id": "food_st_johns_wort", "drug_name": "Warfarin", "severity": "critical", "description": "St. John's Wort induces CYP2C9 and CYP3A4, reducing warfarin efficacy. INR drops significantly.", "evidence_level": "A"},
    {"food_id": "food_st_johns_wort", "drug_name": "Simvastatin", "severity": "major", "description": "CYP3A4 induction by St. John's Wort reduces simvastatin efficacy by ~50%.", "evidence_level": "B"},
    {"food_id": "food_tobacco_smoke", "drug_name": "Theophylline", "severity": "major", "description": "Tobacco smoke induces CYP1A2, increasing theophylline clearance by 50-100%. Dose adjustment needed.", "evidence_level": "A"},
    {"food_id": "food_tobacco_smoke", "drug_name": "Clozapine", "severity": "critical", "description": "CYP1A2 induction by smoking reduces clozapine levels. Smoking cessation can cause toxic levels.", "evidence_level": "A"},
    {"food_id": "food_alcohol", "drug_name": "Metronidazole", "severity": "major", "description": "Disulfiram-like reaction. Alcohol with metronidazole causes nausea, vomiting, flushing.", "evidence_level": "A"},
    {"food_id": "food_alcohol", "drug_name": "Warfarin", "severity": "major", "description": "Acute alcohol inhibits warfarin metabolism. Chronic alcohol induces CYP2E1. Both alter INR.", "evidence_level": "B"},
    {"food_id": "food_cranberry", "drug_name": "Warfarin", "severity": "moderate", "description": "Cranberry juice may inhibit CYP2C9, potentially increasing warfarin effect and INR.", "evidence_level": "C"},
    {"food_id": "food_turmeric", "drug_name": "Warfarin", "severity": "moderate", "description": "Curcumin inhibits CYP2C9 and has antiplatelet properties. May potentiate warfarin.", "evidence_level": "C"},
    {"food_id": "food_green_tea", "drug_name": "Warfarin", "severity": "moderate", "description": "Green tea contains vitamin K (antagonizes warfarin) and EGCG (inhibits CYP). Conflicting effects.", "evidence_level": "C"},
]
