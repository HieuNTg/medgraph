"""
CPIC pharmacogenomics guidelines for CYP2D6 and CYP2C19.

Based on CPIC guidelines (clinpgx.org). Severity multipliers represent
how metabolizer phenotype affects drug interaction risk:
- Poor metabolizer (PM): higher drug levels -> higher toxicity risk
- Ultrarapid metabolizer (UM): lower drug levels -> efficacy risk, OR
  for prodrugs: higher active metabolite -> toxicity risk
"""

GENETIC_GUIDELINES: list[dict] = [
    # --- CYP2D6 Guidelines ---
    # Codeine (prodrug - requires CYP2D6 for morphine conversion)
    {"drug_id": "DB00318", "gene_id": "CYP2D6", "phenotype": "poor",
     "recommendation": "Avoid codeine. CYP2D6 PM cannot convert to morphine — no analgesic effect. Use alternative analgesic.",
     "severity_multiplier": 0.5},  # Lower risk since drug doesn't work, but still flagged
    {"drug_id": "DB00318", "gene_id": "CYP2D6", "phenotype": "intermediate",
     "recommendation": "Reduced codeine efficacy expected. Consider alternative analgesic.",
     "severity_multiplier": 0.8},
    {"drug_id": "DB00318", "gene_id": "CYP2D6", "phenotype": "ultrarapid",
     "recommendation": "AVOID codeine. Ultra-rapid CYP2D6 causes excessive morphine production — risk of fatal respiratory depression.",
     "severity_multiplier": 2.0},

    # Tramadol (prodrug similar to codeine) — DB00715 in seed_data.py
    {"drug_id": "DB00715", "gene_id": "CYP2D6", "phenotype": "poor",
     "recommendation": "Reduced tramadol efficacy. Consider alternative analgesic.",
     "severity_multiplier": 0.7},
    {"drug_id": "DB00715", "gene_id": "CYP2D6", "phenotype": "ultrarapid",
     "recommendation": "Avoid tramadol. Risk of excessive O-desmethyltramadol formation and respiratory depression.",
     "severity_multiplier": 1.8},

    # Fluoxetine (metabolized by CYP2D6)
    {"drug_id": "DB00472", "gene_id": "CYP2D6", "phenotype": "poor",
     "recommendation": "Consider 50% dose reduction for fluoxetine. CYP2D6 PM leads to higher plasma levels.",
     "severity_multiplier": 1.5},
    {"drug_id": "DB00472", "gene_id": "CYP2D6", "phenotype": "ultrarapid",
     "recommendation": "May need dose increase or alternative SSRI. Rapid metabolism reduces efficacy.",
     "severity_multiplier": 0.8},

    # Paroxetine — DB00715_par in seed_drugs_expanded.py
    {"drug_id": "DB00715_par", "gene_id": "CYP2D6", "phenotype": "poor",
     "recommendation": "Consider 50% dose reduction. CYP2D6 PM leads to significantly higher paroxetine levels.",
     "severity_multiplier": 1.5},
    {"drug_id": "DB00715_par", "gene_id": "CYP2D6", "phenotype": "ultrarapid",
     "recommendation": "Consider alternative SSRI not dependent on CYP2D6. Standard doses may be subtherapeutic.",
     "severity_multiplier": 0.7},

    # Tamoxifen (prodrug -> endoxifen via CYP2D6)
    {"drug_id": "DB00675", "gene_id": "CYP2D6", "phenotype": "poor",
     "recommendation": "Avoid tamoxifen. CYP2D6 PM cannot activate to endoxifen — reduced cancer treatment efficacy. Consider aromatase inhibitor.",
     "severity_multiplier": 1.8},
    {"drug_id": "DB00675", "gene_id": "CYP2D6", "phenotype": "intermediate",
     "recommendation": "Reduced tamoxifen efficacy possible. Consider increased monitoring or alternative.",
     "severity_multiplier": 1.3},

    # Metoprolol
    {"drug_id": "DB00264", "gene_id": "CYP2D6", "phenotype": "poor",
     "recommendation": "Reduce metoprolol dose by 50-75%. CYP2D6 PM causes excessive beta-blockade — risk of bradycardia, hypotension.",
     "severity_multiplier": 1.8},
    {"drug_id": "DB00264", "gene_id": "CYP2D6", "phenotype": "ultrarapid",
     "recommendation": "May need higher metoprolol dose or alternative beta-blocker (atenolol).",
     "severity_multiplier": 0.6},

    # Haloperidol — DB00543 in seed_data.py
    {"drug_id": "DB00543", "gene_id": "CYP2D6", "phenotype": "poor",
     "recommendation": "Reduce haloperidol dose. CYP2D6 PM leads to higher levels and increased risk of QT prolongation and EPS.",
     "severity_multiplier": 1.7},

    # Risperidone
    {"drug_id": "DB00734", "gene_id": "CYP2D6", "phenotype": "poor",
     "recommendation": "Reduce risperidone dose. Higher active moiety levels expected in CYP2D6 PM.",
     "severity_multiplier": 1.5},

    # Aripiprazole — DB01246 in seed_drugs_expanded.py
    {"drug_id": "DB01246", "gene_id": "CYP2D6", "phenotype": "poor",
     "recommendation": "Reduce aripiprazole dose to 50-67% of standard. CYP2D6 PM causes elevated levels.",
     "severity_multiplier": 1.5},

    # Dextromethorphan
    {"drug_id": "DB00514", "gene_id": "CYP2D6", "phenotype": "poor",
     "recommendation": "CYP2D6 PM: elevated DXM levels, risk of serotonin-like effects. Use with caution.",
     "severity_multiplier": 1.6},

    # Oxycodone
    {"drug_id": "DB00497", "gene_id": "CYP2D6", "phenotype": "poor",
     "recommendation": "Reduced oxycodone metabolism to oxymorphone. May have altered pain response.",
     "severity_multiplier": 1.3},
    {"drug_id": "DB00497", "gene_id": "CYP2D6", "phenotype": "ultrarapid",
     "recommendation": "Caution with oxycodone — rapid conversion to oxymorphone may increase opioid effects.",
     "severity_multiplier": 1.5},

    # --- CYP2C19 Guidelines ---
    # Clopidogrel (prodrug requiring CYP2C19 activation)
    {"drug_id": "DB00758", "gene_id": "CYP2C19", "phenotype": "poor",
     "recommendation": "AVOID clopidogrel. CYP2C19 PM cannot activate the prodrug — no antiplatelet effect. Use prasugrel or ticagrelor.",
     "severity_multiplier": 2.0},
    {"drug_id": "DB00758", "gene_id": "CYP2C19", "phenotype": "intermediate",
     "recommendation": "Reduced clopidogrel efficacy likely. Consider alternative antiplatelet (prasugrel, ticagrelor).",
     "severity_multiplier": 1.5},
    {"drug_id": "DB00758", "gene_id": "CYP2C19", "phenotype": "ultrarapid",
     "recommendation": "Enhanced clopidogrel activation. Standard dosing appropriate — may have slightly increased bleeding risk.",
     "severity_multiplier": 1.2},

    # Omeprazole (metabolized by CYP2C19)
    {"drug_id": "DB00338", "gene_id": "CYP2C19", "phenotype": "poor",
     "recommendation": "Reduce omeprazole dose by 50%. CYP2C19 PM leads to 5-10x higher drug levels.",
     "severity_multiplier": 1.5},
    {"drug_id": "DB00338", "gene_id": "CYP2C19", "phenotype": "ultrarapid",
     "recommendation": "May need increased omeprazole dose. Rapid metabolism reduces acid suppression efficacy.",
     "severity_multiplier": 0.7},

    # Escitalopram
    {"drug_id": "DB01175", "gene_id": "CYP2C19", "phenotype": "poor",
     "recommendation": "Reduce escitalopram dose by 50%. CYP2C19 PM leads to elevated levels and increased side effects (QT risk).",
     "severity_multiplier": 1.5},

    # Sertraline
    {"drug_id": "DB01104", "gene_id": "CYP2C19", "phenotype": "poor",
     "recommendation": "Consider 50% dose reduction. CYP2C19 PM may lead to higher sertraline levels.",
     "severity_multiplier": 1.3},

    # Voriconazole — DB00625_vori in seed_data.py
    {"drug_id": "DB00625_vori", "gene_id": "CYP2C19", "phenotype": "poor",
     "recommendation": "CYP2C19 PM: voriconazole levels may be 4x higher. Monitor levels closely, consider dose reduction.",
     "severity_multiplier": 1.7},
    {"drug_id": "DB00625_vori", "gene_id": "CYP2C19", "phenotype": "ultrarapid",
     "recommendation": "CYP2C19 UM: voriconazole may be subtherapeutic. Consider alternative antifungal or TDM.",
     "severity_multiplier": 0.6},

    # Phenytoin
    {"drug_id": "DB00252", "gene_id": "CYP2C19", "phenotype": "poor",
     "recommendation": "Reduce phenytoin dose by 25-50%. CYP2C19 PM causes accumulation and toxicity risk.",
     "severity_multiplier": 1.6},
]
