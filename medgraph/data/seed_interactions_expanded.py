"""
Expanded interaction dataset for MEDGRAPH.

80+ new drug-drug interactions and 80+ drug-enzyme relations covering:
- All major CYP3A4 inhibitor + substrate pairs
- CYP2D6 inhibitor + substrate pairs
- CYP2C19, CYP1A2, CYP2C9 interactions
- Food-drug interactions (grapefruit, St. John's Wort)
- DOAC interactions
- Serotonin syndrome risks
- P-glycoprotein-mediated interactions

Drug IDs reference drugs in seed_data.py (original) OR seed_drugs_expanded.py (new).
Enzyme IDs: CYP3A4 | CYP2D6 | CYP2C9 | CYP2C19 | CYP1A2 | CYP2B6 | UGTA1 | PGLYCO

Sources:
- FDA Drug Labeling
- CPIC Guidelines (https://cpicpgx.org/)
- Clinical Pharmacology Database

DISCLAIMER: Data is for informational/research use only. Not medical advice.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Expanded Interactions — 80+ clinically significant drug-drug interactions
# ---------------------------------------------------------------------------

INTERACTIONS_EXPANDED: list[dict] = [
    # =========================================================================
    # CYP3A4 Inhibitor + Substrate Interactions
    # =========================================================================
    # --- Itraconazole (strong CYP3A4 inhibitor, already in seed_data.py) ---
    {
        "id": "INT-expanded-001",
        "drug_a_id": "DB01067",  # Itraconazole
        "drug_b_id": "DB00641",  # Simvastatin
        "severity": "critical",
        "description": (
            "Itraconazole is a potent CYP3A4 and P-glycoprotein inhibitor that markedly "
            "increases simvastatin plasma concentrations, raising the risk of life-threatening "
            "rhabdomyolysis. This combination is contraindicated."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition by itraconazole -> massive simvastatin accumulation",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-002",
        "drug_a_id": "DB01067",  # Itraconazole
        "drug_b_id": "DB00091",  # Cyclosporine
        "severity": "major",
        "description": (
            "Itraconazole inhibits CYP3A4 and P-glycoprotein, increasing cyclosporine "
            "plasma levels by approximately 50%. Nephrotoxicity and other cyclosporine "
            "toxicities may occur. Monitor cyclosporine trough levels and reduce dose as needed."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition by itraconazole -> elevated cyclosporine",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-003",
        "drug_a_id": "DB01067",  # Itraconazole
        "drug_b_id": "DB01394",  # Colchicine
        "severity": "critical",
        "description": (
            "Itraconazole inhibits both CYP3A4 and P-gp, which are the primary clearance "
            "pathways for colchicine. Colchicine levels increase dramatically, causing "
            "life-threatening toxicity including multi-organ failure and bone marrow suppression. "
            "Contraindicated in patients with renal or hepatic impairment."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition -> massive colchicine accumulation -> toxicity",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-004",
        "drug_a_id": "DB01067",  # Itraconazole
        "drug_b_id": "DB00877",  # Sirolimus
        "severity": "major",
        "description": (
            "Itraconazole markedly increases sirolimus exposure via CYP3A4 and P-gp "
            "inhibition. Sirolimus levels may increase several-fold, requiring significant "
            "dose reduction and close therapeutic drug monitoring."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition -> elevated sirolimus -> toxicity risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-005",
        "drug_a_id": "DB01067",  # Itraconazole
        "drug_b_id": "DB00897",  # Triazolam
        "severity": "critical",
        "description": (
            "Itraconazole is contraindicated with triazolam. CYP3A4 inhibition increases "
            "triazolam AUC up to 27-fold, causing prolonged and profound sedation and "
            "respiratory depression."
        ),
        "mechanism": "CYP3A4 inhibition -> massive triazolam accumulation",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-006",
        "drug_a_id": "DB00834",  # Posaconazole
        "drug_b_id": "DB00864",  # Tacrolimus
        "severity": "critical",
        "description": (
            "Posaconazole is a strong CYP3A4 inhibitor that markedly increases tacrolimus "
            "plasma concentrations. Tacrolimus AUC can increase 4.6-fold. Tacrolimus dose "
            "reduction of approximately 66% with intensive TDM is required."
        ),
        "mechanism": "CYP3A4 inhibition by posaconazole -> dramatically elevated tacrolimus",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-007",
        "drug_a_id": "DB00834",  # Posaconazole
        "drug_b_id": "DB00877",  # Sirolimus
        "severity": "critical",
        "description": (
            "Posaconazole markedly increases sirolimus exposure. Concomitant use is "
            "contraindicated. If use is unavoidable, reduce sirolimus dose by 90% and "
            "monitor levels frequently."
        ),
        "mechanism": "Strong CYP3A4 inhibition by posaconazole -> extreme sirolimus accumulation",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-008",
        "drug_a_id": "DB00834",  # Posaconazole
        "drug_b_id": "DB00641",  # Simvastatin
        "severity": "major",
        "description": (
            "Posaconazole inhibits CYP3A4, significantly increasing simvastatin exposure. "
            "Avoid combination or use lowest effective simvastatin dose with close monitoring "
            "for muscle toxicity."
        ),
        "mechanism": "CYP3A4 inhibition by posaconazole -> elevated simvastatin",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-009",
        "drug_a_id": "DB01072",  # Atazanavir
        "drug_b_id": "DB00497",  # Oxycodone
        "severity": "major",
        "description": (
            "Atazanavir inhibits CYP3A4, increasing oxycodone plasma concentrations and "
            "risk of respiratory depression and sedation. Opioid dose reduction and close "
            "monitoring are required when used concomitantly."
        ),
        "mechanism": "CYP3A4 inhibition by atazanavir -> elevated oxycodone levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-010",
        "drug_a_id": "DB01601",  # Lopinavir/ritonavir
        "drug_b_id": "DB00562",  # Alprazolam
        "severity": "major",
        "description": (
            "Lopinavir/ritonavir (a potent CYP3A4 inhibitor combination) substantially "
            "increases alprazolam plasma concentrations, causing prolonged sedation and "
            "respiratory depression. Concomitant use should be avoided or dose markedly reduced."
        ),
        "mechanism": "CYP3A4 inhibition by lopinavir/ritonavir -> elevated alprazolam",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-011",
        "drug_a_id": "DB01068",  # Cobicistat
        "drug_b_id": "DB01590",  # Everolimus
        "severity": "major",
        "description": (
            "Cobicistat is a potent CYP3A4 inhibitor. Everolimus is a sensitive CYP3A4 "
            "substrate. Co-administration markedly increases everolimus exposure, requiring "
            "significant dose reduction and therapeutic drug monitoring."
        ),
        "mechanism": "CYP3A4 inhibition by cobicistat -> elevated everolimus",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-012",
        "drug_a_id": "DB01068",  # Cobicistat
        "drug_b_id": "DB00813",  # Fentanyl
        "severity": "major",
        "description": (
            "Cobicistat substantially increases fentanyl exposure via CYP3A4 inhibition. "
            "Risk of life-threatening respiratory depression. Use with extreme caution "
            "with close monitoring; consider alternative opioid analgesics."
        ),
        "mechanism": "CYP3A4 inhibition by cobicistat -> elevated fentanyl -> respiratory depression",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-013",
        "drug_a_id": "DB00879",  # Ritonavir (already in seed_data.py)
        "drug_b_id": "DB00203",  # Sildenafil
        "severity": "critical",
        "description": (
            "Ritonavir dramatically increases sildenafil plasma concentrations (AUC 11-fold) "
            "via CYP3A4 inhibition. Severe hypotension and visual disturbances have been "
            "reported. Sildenafil for pulmonary arterial hypertension (Revatio) is "
            "contraindicated with ritonavir."
        ),
        "mechanism": "CYP3A4 inhibition by ritonavir -> 11-fold increase in sildenafil AUC",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-014",
        "drug_a_id": "DB00879",  # Ritonavir
        "drug_b_id": "DB01299",  # Tadalafil
        "severity": "major",
        "description": (
            "Ritonavir substantially increases tadalafil exposure via CYP3A4 inhibition. "
            "For erectile dysfunction, the maximum tadalafil dose is 10mg per 72 hours. "
            "For pulmonary arterial hypertension, a specific dose reduction regimen is required."
        ),
        "mechanism": "CYP3A4 inhibition by ritonavir -> elevated tadalafil",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-015",
        "drug_a_id": "DB00879",  # Ritonavir
        "drug_b_id": "DB00813",  # Fentanyl
        "severity": "critical",
        "description": (
            "Ritonavir markedly increases fentanyl exposure via CYP3A4 inhibition. "
            "Life-threatening respiratory depression reported. Combination requires "
            "significant dose reduction and intensive monitoring or should be avoided."
        ),
        "mechanism": "CYP3A4 inhibition by ritonavir -> dramatically elevated fentanyl",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-016",
        "drug_a_id": "DB01111",  # Erythromycin
        "drug_b_id": "DB00641",  # Simvastatin
        "severity": "major",
        "description": (
            "Erythromycin inhibits CYP3A4, significantly increasing simvastatin "
            "plasma concentrations and rhabdomyolysis risk. Avoid concomitant use; "
            "consider temporary discontinuation of simvastatin during erythromycin therapy."
        ),
        "mechanism": "CYP3A4 inhibition by erythromycin -> elevated simvastatin -> myopathy risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-017",
        "drug_a_id": "DB01111",  # Erythromycin
        "drug_b_id": "DB00390",  # Digoxin
        "severity": "major",
        "description": (
            "Erythromycin inhibits P-glycoprotein and alters gut flora that metabolize "
            "digoxin. Digoxin levels can increase significantly, causing toxicity "
            "(bradycardia, nausea, arrhythmias). Monitor digoxin levels."
        ),
        "mechanism": "P-gp inhibition + altered gut flora metabolism -> elevated digoxin",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-018",
        "drug_a_id": "DB01111",  # Erythromycin
        "drug_b_id": "DB00625",  # Midazolam
        "severity": "major",
        "description": (
            "Erythromycin significantly increases midazolam AUC (3-4 fold) via CYP3A4 "
            "inhibition. Prolonged sedation and respiratory depression result. "
            "Dose reduction required when used together."
        ),
        "mechanism": "CYP3A4 inhibition by erythromycin -> elevated midazolam",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-019",
        "drug_a_id": "DB01111",  # Erythromycin
        "drug_b_id": "DB01394",  # Colchicine
        "severity": "critical",
        "description": (
            "Erythromycin inhibits CYP3A4 and P-glycoprotein, dramatically increasing "
            "colchicine levels. Fatal colchicine toxicity has been reported with this "
            "combination. Contraindicated in patients with renal or hepatic impairment."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition by erythromycin -> fatal colchicine toxicity",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-020",
        "drug_a_id": "DB00338_v2",  # Diltiazem (already in seed_data.py)
        "drug_b_id": "DB00813",  # Fentanyl
        "severity": "major",
        "description": (
            "Diltiazem moderately inhibits CYP3A4, increasing fentanyl plasma concentrations "
            "and risk of respiratory depression. Enhanced monitoring required; consider "
            "reducing fentanyl dose."
        ),
        "mechanism": "CYP3A4 inhibition by diltiazem -> elevated fentanyl levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-021",
        "drug_a_id": "DB00338_v2",  # Diltiazem
        "drug_b_id": "DB01590",  # Everolimus
        "severity": "major",
        "description": (
            "Diltiazem moderately inhibits CYP3A4, increasing everolimus exposure. "
            "Everolimus trough levels should be monitored and dose adjusted accordingly "
            "to maintain therapeutic concentrations without toxicity."
        ),
        "mechanism": "CYP3A4 inhibition by diltiazem -> elevated everolimus",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-022",
        "drug_a_id": "DB00661",  # Verapamil (already in seed_data.py)
        "drug_b_id": "DB06695",  # Dabigatran (already in seed_data.py)
        "severity": "major",
        "description": (
            "Verapamil inhibits P-glycoprotein, increasing dabigatran bioavailability "
            "and plasma concentrations by approximately 25-50%. Bleeding risk is increased. "
            "Administer dabigatran 2 hours before verapamil if co-administration is necessary."
        ),
        "mechanism": "P-gp inhibition by verapamil -> increased dabigatran absorption",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-023",
        "drug_a_id": "DB00661",  # Verapamil
        "drug_b_id": "DB01030",  # Imatinib
        "severity": "moderate",
        "description": (
            "Verapamil (CYP3A4 and P-gp inhibitor) may increase imatinib plasma "
            "concentrations modestly. Clinical significance is uncertain but monitoring "
            "for imatinib adverse effects is advisable."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition by verapamil -> modestly elevated imatinib",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-024",
        "drug_a_id": "DB00519",  # Dronedarone
        "drug_b_id": "DB00641",  # Simvastatin
        "severity": "major",
        "description": (
            "Dronedarone (moderate CYP3A4 inhibitor) increases simvastatin AUC approximately "
            "4-fold. The simvastatin dose should not exceed 10mg/day when used with dronedarone "
            "due to increased rhabdomyolysis risk."
        ),
        "mechanism": "CYP3A4 inhibition by dronedarone -> elevated simvastatin",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-025",
        "drug_a_id": "DB00519",  # Dronedarone
        "drug_b_id": "DB00390",  # Digoxin
        "severity": "major",
        "description": (
            "Dronedarone inhibits P-glycoprotein, increasing digoxin levels by approximately "
            "2.5-fold. Digoxin toxicity risk is increased. If used together, reduce digoxin "
            "dose by 50% and monitor digoxin levels and signs of toxicity."
        ),
        "mechanism": "P-gp inhibition by dronedarone -> elevated digoxin levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # CYP2D6 Inhibitor + Substrate Interactions
    # =========================================================================
    {
        "id": "INT-expanded-026",
        "drug_a_id": "DB00715_par",  # Paroxetine
        "drug_b_id": "DB00318",  # Codeine (already in seed_data.py)
        "severity": "critical",
        "description": (
            "Paroxetine is one of the most potent CYP2D6 inhibitors available. It converts "
            "extensive CYP2D6 metabolizers to poor metabolizers, abolishing codeine's "
            "conversion to morphine and rendering it largely ineffective for analgesia. "
            "In ultra-rapid metabolizers, the interaction risk is particularly complex. "
            "Alternative analgesia should be used."
        ),
        "mechanism": "Potent CYP2D6 inhibition by paroxetine -> codeine analgesic failure",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-027",
        "drug_a_id": "DB00715_par",  # Paroxetine
        "drug_b_id": "DB00715",  # Tramadol (already in seed_data.py)
        "severity": "major",
        "description": (
            "Paroxetine inhibits CYP2D6, reducing tramadol conversion to its active opioid "
            "metabolite O-desmethyltramadol. Tramadol efficacy is reduced. Additionally, "
            "both drugs have serotonergic activity, raising the risk of serotonin syndrome."
        ),
        "mechanism": "CYP2D6 inhibition + additive serotonergic activity -> reduced efficacy + serotonin syndrome risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-028",
        "drug_a_id": "DB00715_par",  # Paroxetine
        "drug_b_id": "DB00675",  # Tamoxifen (already in seed_data.py)
        "severity": "major",
        "description": (
            "Paroxetine, a potent CYP2D6 inhibitor, dramatically reduces tamoxifen conversion "
            "to its active metabolite endoxifen. Plasma endoxifen levels may be reduced by "
            "65-75%, significantly compromising breast cancer treatment efficacy. "
            "Paroxetine is the CYP2D6 inhibitor of greatest concern with tamoxifen."
        ),
        "mechanism": "CYP2D6 inhibition by paroxetine -> markedly reduced endoxifen levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-029",
        "drug_a_id": "DB00715_par",  # Paroxetine
        "drug_b_id": "DB00264",  # Metoprolol (already in seed_data.py)
        "severity": "moderate",
        "description": (
            "Paroxetine (potent CYP2D6 inhibitor) increases metoprolol plasma concentrations "
            "3-5 fold. Risk of bradycardia, heart block, and hypotension. Consider dose "
            "reduction of metoprolol or use a beta-blocker not metabolized by CYP2D6."
        ),
        "mechanism": "CYP2D6 inhibition by paroxetine -> elevated metoprolol",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-030",
        "drug_a_id": "DB00715_par",  # Paroxetine
        "drug_b_id": "DB01136",  # Carvedilol
        "severity": "moderate",
        "description": (
            "Paroxetine inhibits CYP2D6, the primary metabolizing enzyme for carvedilol. "
            "Carvedilol plasma concentrations increase significantly, raising risk of "
            "excessive bradycardia and hypotension. Monitor heart rate and blood pressure."
        ),
        "mechanism": "CYP2D6 inhibition by paroxetine -> elevated carvedilol",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-031",
        "drug_a_id": "DB01156",  # Bupropion
        "drug_b_id": "DB00318",  # Codeine
        "severity": "major",
        "description": (
            "Bupropion is a potent CYP2D6 inhibitor that abolishes codeine conversion "
            "to morphine, rendering codeine ineffective for analgesia. This interaction "
            "is clinically equivalent to the CYP2D6 poor metabolizer phenotype."
        ),
        "mechanism": "CYP2D6 inhibition by bupropion -> codeine analgesic failure",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-032",
        "drug_a_id": "DB01156",  # Bupropion
        "drug_b_id": "DB00675",  # Tamoxifen
        "severity": "major",
        "description": (
            "Bupropion is a potent CYP2D6 inhibitor. Significantly reduces tamoxifen "
            "conversion to active metabolite endoxifen, potentially compromising breast "
            "cancer treatment efficacy. Avoid combination; select alternative antidepressants."
        ),
        "mechanism": "CYP2D6 inhibition by bupropion -> reduced endoxifen levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-033",
        "drug_a_id": "DB00857",  # Terbinafine
        "drug_b_id": "DB00715",  # Tramadol
        "severity": "major",
        "description": (
            "Terbinafine is a potent CYP2D6 inhibitor. Reduces tramadol conversion to "
            "its active opioid metabolite, decreasing analgesic efficacy. Concomitant "
            "serotonergic activity also raises serotonin syndrome risk."
        ),
        "mechanism": "CYP2D6 inhibition by terbinafine -> reduced tramadol opioid activity",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-034",
        "drug_a_id": "DB00857",  # Terbinafine
        "drug_b_id": "DB00540",  # Nortriptyline
        "severity": "major",
        "description": (
            "Terbinafine potently inhibits CYP2D6, the primary enzyme metabolizing "
            "nortriptyline. Nortriptyline plasma levels increase substantially, raising "
            "risk of TCA toxicity including arrhythmias, anticholinergic effects, and "
            "CNS toxicity. Monitor TCA levels."
        ),
        "mechanism": "CYP2D6 inhibition by terbinafine -> elevated nortriptyline -> TCA toxicity",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-035",
        "drug_a_id": "DB00857",  # Terbinafine
        "drug_b_id": "DB01151",  # Desipramine
        "severity": "major",
        "description": (
            "Terbinafine dramatically increases desipramine plasma levels by inhibiting "
            "CYP2D6. A 4-6 fold increase in desipramine AUC has been documented. "
            "Risk of life-threatening cardiac arrhythmias. Avoid combination."
        ),
        "mechanism": "CYP2D6 inhibition by terbinafine -> 4-6 fold increase in desipramine AUC",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-036",
        "drug_a_id": "DB00476",  # Duloxetine (already in seed_data.py)
        "drug_b_id": "DB00540",  # Nortriptyline
        "severity": "moderate",
        "description": (
            "Duloxetine moderately inhibits CYP2D6, increasing nortriptyline plasma levels "
            "and risk of TCA toxicity. Monitor TCA plasma levels and for signs of toxicity "
            "such as arrhythmias and anticholinergic effects."
        ),
        "mechanism": "CYP2D6 inhibition by duloxetine -> elevated nortriptyline",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-037",
        "drug_a_id": "DB00476",  # Duloxetine
        "drug_b_id": "DB00734",  # Risperidone (already in seed_data.py)
        "severity": "moderate",
        "description": (
            "Duloxetine inhibits CYP2D6, the primary metabolizing enzyme for risperidone. "
            "Risperidone plasma levels may increase, raising risk of adverse effects "
            "including extrapyramidal symptoms and QT prolongation."
        ),
        "mechanism": "CYP2D6 inhibition by duloxetine -> elevated risperidone",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-038",
        "drug_a_id": "DB01246",  # Aripiprazole
        "drug_b_id": "DB00472",  # Fluoxetine (already in seed_data.py)
        "severity": "moderate",
        "description": (
            "Fluoxetine (CYP2D6 inhibitor) increases aripiprazole plasma concentrations "
            "by approximately 2-fold. FDA labeling recommends reducing aripiprazole dose "
            "by 50% when initiating fluoxetine therapy."
        ),
        "mechanism": "CYP2D6 inhibition by fluoxetine -> elevated aripiprazole",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # CYP2C19 Inhibitor + Substrate Interactions
    # =========================================================================
    {
        "id": "INT-expanded-039",
        "drug_a_id": "DB00176",  # Fluvoxamine (already in seed_data.py)
        "drug_b_id": "DB00829",  # Diazepam (already in seed_data.py)
        "severity": "major",
        "description": (
            "Fluvoxamine strongly inhibits CYP2C19 and moderately inhibits CYP3A4, "
            "both of which metabolize diazepam. Diazepam AUC increases approximately "
            "3-fold. Prolonged sedation, respiratory depression, and impaired motor "
            "function result. Use a benzodiazepine metabolized by UGT (lorazepam) instead."
        ),
        "mechanism": "CYP2C19 + CYP3A4 inhibition by fluvoxamine -> elevated diazepam",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-040",
        "drug_a_id": "DB00176",  # Fluvoxamine
        "drug_b_id": "DB00363",  # Clozapine
        "severity": "major",
        "description": (
            "Fluvoxamine is a potent CYP1A2 inhibitor, and clozapine is primarily "
            "metabolized by CYP1A2. Fluvoxamine increases clozapine plasma levels "
            "3-5 fold, causing toxicity including seizures, excessive sedation, "
            "and anticholinergic effects. The combination requires significant dose "
            "reduction of clozapine (by up to 66%) or avoidance."
        ),
        "mechanism": "CYP1A2 inhibition by fluvoxamine -> dramatic clozapine accumulation",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-041",
        "drug_a_id": "DB00176",  # Fluvoxamine
        "drug_b_id": "DB00334",  # Olanzapine
        "severity": "moderate",
        "description": (
            "Fluvoxamine inhibits CYP1A2, increasing olanzapine plasma concentrations "
            "by approximately 50-100%. Risk of enhanced olanzapine adverse effects "
            "including sedation, weight gain, and metabolic effects. Monitor and adjust dose."
        ),
        "mechanism": "CYP1A2 inhibition by fluvoxamine -> elevated olanzapine",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-042",
        "drug_a_id": "DB01051",  # Isoniazid
        "drug_b_id": "DB00252",  # Phenytoin (already in seed_data.py)
        "severity": "major",
        "description": (
            "Isoniazid inhibits CYP2C9 and CYP2C19, reducing phenytoin metabolism and "
            "dramatically increasing phenytoin plasma levels. Phenytoin toxicity (nystagmus, "
            "ataxia, altered mental status) can occur within days of starting isoniazid. "
            "Phenytoin levels should be monitored closely."
        ),
        "mechanism": "CYP2C9 + CYP2C19 inhibition by isoniazid -> phenytoin toxicity",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-043",
        "drug_a_id": "DB01051",  # Isoniazid
        "drug_b_id": "DB00682",  # Warfarin (already in seed_data.py)
        "severity": "major",
        "description": (
            "Isoniazid inhibits CYP2C9, reducing warfarin metabolism and increasing "
            "warfarin exposure. INR increases and bleeding risk rises. Close INR "
            "monitoring required when isoniazid is started or stopped."
        ),
        "mechanism": "CYP2C9 inhibition by isoniazid -> elevated warfarin levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-044",
        "drug_a_id": "DB01142",  # Metronidazole
        "drug_b_id": "DB00682",  # Warfarin
        "severity": "major",
        "description": (
            "Metronidazole inhibits CYP2C9, increasing warfarin plasma concentrations and "
            "INR by 30-60%. A clinically significant interaction that may require warfarin "
            "dose reduction by 25-50% during metronidazole therapy. INR monitoring is essential."
        ),
        "mechanism": "CYP2C9 inhibition by metronidazole -> elevated warfarin levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-045",
        "drug_a_id": "DB01015",  # Sulfamethoxazole
        "drug_b_id": "DB00682",  # Warfarin
        "severity": "major",
        "description": (
            "Sulfamethoxazole (especially as TMP-SMX) inhibits CYP2C9, reducing warfarin "
            "metabolism and significantly increasing INR. Warfarin dose reduction of 25-50% "
            "is often required. This is one of the most common antibiotic-warfarin interactions."
        ),
        "mechanism": "CYP2C9 inhibition by sulfamethoxazole -> elevated warfarin -> bleeding risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # CYP1A2 Interactions
    # =========================================================================
    {
        "id": "INT-expanded-046",
        "drug_a_id": "DB00176",  # Fluvoxamine
        "drug_b_id": "DB00277",  # Theophylline (already in seed_data.py)
        "severity": "major",
        "description": (
            "Fluvoxamine is a potent CYP1A2 inhibitor. Theophylline is a narrow therapeutic "
            "index drug primarily metabolized by CYP1A2. Fluvoxamine increases theophylline "
            "AUC 3-fold. Theophylline toxicity (seizures, tachycardia, tremor) can result. "
            "Monitor theophylline levels; dose reduction typically required."
        ),
        "mechanism": "CYP1A2 inhibition by fluvoxamine -> theophylline toxicity",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-047",
        "drug_a_id": "DB00618",  # Ciprofloxacin (already in seed_data.py)
        "drug_b_id": "DB00277_ami",  # Aminophylline
        "severity": "major",
        "description": (
            "Ciprofloxacin inhibits CYP1A2, reducing aminophylline (theophylline) clearance. "
            "Theophylline plasma levels increase 50-100%, risking toxicity with tachycardia, "
            "tremors, nausea, and seizures. Reduce aminophylline dose by 30-50% or monitor "
            "theophylline levels closely."
        ),
        "mechanism": "CYP1A2 inhibition by ciprofloxacin -> elevated aminophylline/theophylline",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-048",
        "drug_a_id": "DB00500",  # Levofloxacin
        "drug_b_id": "DB00277",  # Theophylline
        "severity": "moderate",
        "description": (
            "Levofloxacin mildly inhibits CYP1A2, which may modestly increase theophylline "
            "plasma concentrations. The interaction is clinically less significant than with "
            "ciprofloxacin. Monitor theophylline levels when starting or stopping levofloxacin."
        ),
        "mechanism": "Mild CYP1A2 inhibition by levofloxacin -> modest theophylline increase",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-049",
        "drug_a_id": "DB00363",  # Clozapine
        "drug_b_id": "DB00898",  # Ethanol (already in seed_data.py)
        "severity": "moderate",
        "description": (
            "Cigarette smoke (not listed separately) induces CYP1A2 which dramatically "
            "reduces clozapine levels. When patients stop smoking, CYP1A2 induction ceases "
            "and clozapine levels rise significantly (50-100%), causing toxicity. "
            "Ethanol potentiates CNS depression with clozapine."
        ),
        "mechanism": "Additive CNS depression; CYP1A2 induction reversal relevant to clozapine",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Food-Drug Interactions (Grapefruit, St. John's Wort)
    # =========================================================================
    {
        "id": "INT-expanded-050",
        "drug_a_id": "DB_GRAPE",  # Grapefruit
        "drug_b_id": "DB00641",  # Simvastatin
        "severity": "major",
        "description": (
            "Grapefruit juice inhibits intestinal CYP3A4 irreversibly via furanocoumarins. "
            "A single glass increases simvastatin AUC 7-fold and Cmax 16-fold. "
            "The interaction persists for >24 hours. Risk of rhabdomyolysis is "
            "significantly elevated. Patients should avoid grapefruit when taking simvastatin."
        ),
        "mechanism": "Irreversible intestinal CYP3A4 inhibition by grapefruit furanocoumarins -> massive simvastatin increase",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-051",
        "drug_a_id": "DB_GRAPE",  # Grapefruit
        "drug_b_id": "DB01076",  # Atorvastatin (already in seed_data.py)
        "severity": "moderate",
        "description": (
            "Grapefruit juice inhibits CYP3A4, increasing atorvastatin levels approximately "
            "2.5-fold. While less severe than simvastatin, the interaction still raises "
            "myopathy risk. Patients should limit grapefruit intake while taking atorvastatin."
        ),
        "mechanism": "Intestinal CYP3A4 inhibition by grapefruit -> elevated atorvastatin",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-052",
        "drug_a_id": "DB_GRAPE",  # Grapefruit
        "drug_b_id": "DB00625",  # Midazolam (already in seed_data.py)
        "severity": "major",
        "description": (
            "Grapefruit juice substantially increases midazolam oral bioavailability "
            "via CYP3A4 inhibition. AUC increases approximately 3-fold. Risk of prolonged "
            "sedation and respiratory depression. Avoid combination."
        ),
        "mechanism": "CYP3A4 inhibition by grapefruit -> elevated oral midazolam levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-053",
        "drug_a_id": "DB_GRAPE",  # Grapefruit
        "drug_b_id": "DB01107",  # Nifedipine
        "severity": "major",
        "description": (
            "Grapefruit juice inhibits CYP3A4, increasing nifedipine bioavailability "
            "by up to 2-fold. Risk of excessive hypotension, reflex tachycardia, and "
            "peripheral edema. Patients should avoid grapefruit with nifedipine."
        ),
        "mechanism": "CYP3A4 inhibition by grapefruit -> elevated nifedipine -> excessive hypotension",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-054",
        "drug_a_id": "DB_GRAPE",  # Grapefruit
        "drug_b_id": "DB00091",  # Cyclosporine (already in seed_data.py)
        "severity": "major",
        "description": (
            "Grapefruit juice increases cyclosporine bioavailability via CYP3A4 and "
            "P-gp inhibition. Cyclosporine AUC increases 1.4-1.6 fold. Risk of "
            "nephrotoxicity and other dose-related toxicities. Consistent avoidance of "
            "grapefruit is recommended."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition by grapefruit -> elevated cyclosporine",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-055",
        "drug_a_id": "DB_GRAPE",  # Grapefruit
        "drug_b_id": "DB06605",  # Apixaban
        "severity": "moderate",
        "description": (
            "Grapefruit juice may modestly increase apixaban plasma concentrations via "
            "CYP3A4 and P-gp inhibition, potentially increasing bleeding risk. The "
            "clinical significance is less established than with other CYP3A4 substrates; "
            "moderation is advised."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition by grapefruit -> modestly elevated apixaban",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-056",
        "drug_a_id": "DB_STJ",  # St. John's Wort
        "drug_b_id": "DB00091",  # Cyclosporine
        "severity": "critical",
        "description": (
            "St. John's Wort is a potent inducer of CYP3A4 and P-glycoprotein. "
            "It dramatically reduces cyclosporine plasma levels by up to 50-60%, "
            "causing acute transplant rejection. Multiple cases of kidney and heart "
            "transplant rejection have been reported. This combination is contraindicated."
        ),
        "mechanism": "CYP3A4 + P-gp induction by St. John's Wort -> severe cyclosporine reduction -> rejection",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-057",
        "drug_a_id": "DB_STJ",  # St. John's Wort
        "drug_b_id": "DB00682",  # Warfarin
        "severity": "major",
        "description": (
            "St. John's Wort induces CYP2C9 and CYP3A4, reducing warfarin plasma levels "
            "and anticoagulant effect. INR decreases substantially, raising thrombosis risk. "
            "Multiple thrombosis events (PE, stroke) have been linked to this interaction. "
            "Avoid combination; if used, monitor INR closely."
        ),
        "mechanism": "CYP enzyme induction by St. John's Wort -> reduced warfarin levels -> thrombosis",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-058",
        "drug_a_id": "DB_STJ",  # St. John's Wort
        "drug_b_id": "DB00977",  # Ethinylestradiol (already in seed_data.py)
        "severity": "major",
        "description": (
            "St. John's Wort induces CYP3A4 and P-glycoprotein, reducing plasma levels of "
            "oral contraceptive hormones. Contraceptive failure and breakthrough bleeding "
            "have been reported. Alternative non-hormonal contraception should be used."
        ),
        "mechanism": "CYP3A4 + P-gp induction by St. John's Wort -> reduced OC levels -> contraceptive failure",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-059",
        "drug_a_id": "DB_STJ",  # St. John's Wort
        "drug_b_id": "DB00877",  # Sirolimus
        "severity": "critical",
        "description": (
            "St. John's Wort potently induces CYP3A4 and P-gp, reducing sirolimus levels "
            "by approximately 50%, which can lead to organ rejection in transplant patients. "
            "This combination is contraindicated."
        ),
        "mechanism": "CYP3A4 + P-gp induction by St. John's Wort -> severe sirolimus reduction",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-060",
        "drug_a_id": "DB_STJ",  # St. John's Wort
        "drug_b_id": "DB06290",  # Sofosbuvir
        "severity": "major",
        "description": (
            "St. John's Wort is a strong P-glycoprotein inducer and reduces sofosbuvir "
            "plasma concentrations, potentially compromising hepatitis C treatment efficacy. "
            "This combination is contraindicated per FDA labeling."
        ),
        "mechanism": "P-gp induction by St. John's Wort -> reduced sofosbuvir exposure -> HCV treatment failure",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # DOAC Interactions (Apixaban, Rivaroxaban, Dabigatran, Edoxaban)
    # =========================================================================
    {
        "id": "INT-expanded-061",
        "drug_a_id": "DB01026",  # Ketoconazole (already in seed_data.py)
        "drug_b_id": "DB06605",  # Apixaban
        "severity": "major",
        "description": (
            "Ketoconazole inhibits both CYP3A4 and P-glycoprotein, increasing apixaban "
            "AUC approximately 2-fold and Cmax 1.6-fold. This substantially increases "
            "bleeding risk. Combined strong CYP3A4/P-gp inhibitors should be avoided "
            "or used with dose reduction of apixaban to 2.5mg twice daily."
        ),
        "mechanism": "Dual CYP3A4 + P-gp inhibition by ketoconazole -> elevated apixaban",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-062",
        "drug_a_id": "DB01026",  # Ketoconazole
        "drug_b_id": "DB06228",  # Rivaroxaban (already in seed_data.py)
        "severity": "major",
        "description": (
            "Ketoconazole inhibits CYP3A4 and P-glycoprotein, increasing rivaroxaban "
            "AUC 2.6-fold and Cmax 1.7-fold. This combination is contraindicated in the "
            "EU and should be used with caution in the US due to significantly increased "
            "bleeding risk."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition by ketoconazole -> elevated rivaroxaban -> bleeding risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-063",
        "drug_a_id": "DB01045",  # Rifampin (already in seed_data.py)
        "drug_b_id": "DB06605",  # Apixaban
        "severity": "major",
        "description": (
            "Rifampin induces CYP3A4 and P-glycoprotein, reducing apixaban AUC by "
            "approximately 54%. This may lead to therapeutic failure with increased "
            "thromboembolic risk. Avoid combination; use a different anticoagulant."
        ),
        "mechanism": "CYP3A4 + P-gp induction by rifampin -> reduced apixaban -> thrombosis risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-064",
        "drug_a_id": "DB01045",  # Rifampin
        "drug_b_id": "DB06294",  # Edoxaban
        "severity": "major",
        "description": (
            "Rifampin potently induces P-glycoprotein, dramatically reducing edoxaban "
            "systemic exposure. The anticoagulant effect is substantially reduced. "
            "Avoid combination; use alternative anticoagulant therapy."
        ),
        "mechanism": "P-gp induction by rifampin -> reduced edoxaban exposure -> anticoagulant failure",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-065",
        "drug_a_id": "DB01067",  # Itraconazole
        "drug_b_id": "DB06695",  # Dabigatran (already in seed_data.py)
        "severity": "major",
        "description": (
            "Itraconazole inhibits P-glycoprotein, increasing dabigatran bioavailability "
            "and plasma concentrations significantly. Bleeding risk is increased. "
            "In patients with renal impairment, this combination should be avoided."
        ),
        "mechanism": "P-gp inhibition by itraconazole -> increased dabigatran absorption -> bleeding risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-066",
        "drug_a_id": "DB00564",  # Carbamazepine (already in seed_data.py)
        "drug_b_id": "DB06605",  # Apixaban
        "severity": "major",
        "description": (
            "Carbamazepine induces CYP3A4 and P-glycoprotein, reducing apixaban exposure "
            "by approximately 50%. Anticoagulant effect is substantially decreased, "
            "raising thromboembolic risk. Avoid combination or consider alternative agents."
        ),
        "mechanism": "CYP3A4 + P-gp induction by carbamazepine -> reduced apixaban levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Serotonin Syndrome Interactions
    # =========================================================================
    {
        "id": "INT-expanded-067",
        "drug_a_id": "DB00601",  # Linezolid
        "drug_b_id": "DB00472",  # Fluoxetine (already in seed_data.py)
        "severity": "critical",
        "description": (
            "Linezolid is a reversible, non-selective MAO inhibitor. Combined with fluoxetine "
            "(SSRI), there is high risk of life-threatening serotonin syndrome with "
            "symptoms including hyperthermia, agitation, tremor, clonus, and diaphoresis. "
            "This combination is contraindicated. Allow 5 weeks washout after fluoxetine "
            "before starting linezolid."
        ),
        "mechanism": "MAO inhibition by linezolid + SSRI -> serotonin syndrome",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-068",
        "drug_a_id": "DB00601",  # Linezolid
        "drug_b_id": "DB01104",  # Sertraline (already in seed_data.py)
        "severity": "critical",
        "description": (
            "Linezolid (MAO inhibitor) combined with sertraline (SSRI) creates high risk "
            "of serotonin syndrome. Multiple fatal cases reported. Contraindicated. "
            "If linezolid is urgently needed, serotonergic drugs should be stopped and "
            "monitoring instituted."
        ),
        "mechanism": "MAO inhibition + SSRI serotonin reuptake inhibition -> serotonin syndrome",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-069",
        "drug_a_id": "DB00601",  # Linezolid
        "drug_b_id": "DB00715",  # Tramadol (already in seed_data.py)
        "severity": "critical",
        "description": (
            "Tramadol has serotonergic activity (serotonin reuptake inhibition) and combined "
            "with linezolid (MAO inhibitor) creates a high risk of serotonin syndrome. "
            "Additionally, linezolid may inhibit tramadol metabolism. Combination is "
            "contraindicated."
        ),
        "mechanism": "MAO inhibition by linezolid + serotonergic activity of tramadol -> serotonin syndrome",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-070",
        "drug_a_id": "DB00601",  # Linezolid
        "drug_b_id": "DB00831",  # Venlafaxine
        "severity": "critical",
        "description": (
            "Venlafaxine (SNRI) combined with linezolid (MAO inhibitor) carries high risk "
            "of serotonin syndrome and is contraindicated. Allow appropriate washout periods "
            "when transitioning between these agents."
        ),
        "mechanism": "MAO inhibition by linezolid + SNRI action -> serotonin syndrome",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-071",
        "drug_a_id": "DB00472",  # Fluoxetine (already in seed_data.py)
        "drug_b_id": "DB00715",  # Tramadol
        "severity": "major",
        "description": (
            "Fluoxetine (SSRI) combined with tramadol (serotonergic opioid) increases "
            "the risk of serotonin syndrome. Additionally, fluoxetine inhibits CYP2D6, "
            "reducing tramadol conversion to its active opioid metabolite, decreasing "
            "analgesic efficacy. Both mechanisms contribute to this clinically significant interaction."
        ),
        "mechanism": "Additive serotonergic activity + CYP2D6 inhibition reducing tramadol efficacy",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-072",
        "drug_a_id": "DB00476",  # Duloxetine
        "drug_b_id": "DB00715",  # Tramadol
        "severity": "major",
        "description": (
            "Duloxetine (SNRI) combined with tramadol increases serotonin syndrome risk "
            "through additive serotonergic mechanisms. Duloxetine also inhibits CYP2D6, "
            "reducing tramadol analgesic efficacy. Monitor for signs of serotonin excess "
            "and use with caution."
        ),
        "mechanism": "Additive serotonergic activity + moderate CYP2D6 inhibition",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # CYP Enzyme Inducers + Substrates
    # =========================================================================
    {
        "id": "INT-expanded-073",
        "drug_a_id": "DB00625_efv",  # Efavirenz
        "drug_b_id": "DB00864",  # Tacrolimus
        "severity": "major",
        "description": (
            "Efavirenz induces CYP3A4, dramatically reducing tacrolimus plasma levels. "
            "Significant dose increases of tacrolimus (often 3-5 fold) may be needed. "
            "Intensive therapeutic drug monitoring is mandatory."
        ),
        "mechanism": "CYP3A4 induction by efavirenz -> reduced tacrolimus levels -> rejection risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-074",
        "drug_a_id": "DB00238",  # Nevirapine
        "drug_b_id": "DB00682",  # Warfarin
        "severity": "major",
        "description": (
            "Nevirapine induces CYP2C9 and CYP3A4, reducing warfarin plasma levels. "
            "The anticoagulant effect of warfarin decreases, raising thromboembolic risk. "
            "Close INR monitoring and warfarin dose adjustments are required."
        ),
        "mechanism": "CYP2C9 + CYP3A4 induction by nevirapine -> reduced warfarin levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-075",
        "drug_a_id": "DB00949",  # Oxcarbazepine
        "drug_b_id": "DB00977",  # Ethinylestradiol
        "severity": "major",
        "description": (
            "Oxcarbazepine induces CYP3A4 and reduces plasma levels of oral contraceptive "
            "hormones by approximately 50%, leading to contraceptive failure. Non-hormonal "
            "contraception is recommended for women taking oxcarbazepine."
        ),
        "mechanism": "CYP3A4 induction by oxcarbazepine -> reduced OC hormone levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-076",
        "drug_a_id": "DB00752",  # Topiramate
        "drug_b_id": "DB00977",  # Ethinylestradiol
        "severity": "moderate",
        "description": (
            "Topiramate at doses >200mg/day induces CYP3A4 and reduces ethinylestradiol "
            "plasma levels by up to 30%, potentially reducing contraceptive efficacy. "
            "FDA advises using alternative or additional contraception."
        ),
        "mechanism": "Mild CYP3A4 induction by topiramate -> reduced OC hormone levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-077",
        "drug_a_id": "DB00564",  # Carbamazepine (already in seed_data.py)
        "drug_b_id": "DB01224",  # Quetiapine
        "severity": "major",
        "description": (
            "Carbamazepine is a potent CYP3A4 inducer that reduces quetiapine plasma levels "
            "approximately 6-fold. This may lead to therapeutic failure. Avoid combination "
            "or use higher quetiapine doses with close monitoring."
        ),
        "mechanism": "CYP3A4 induction by carbamazepine -> ~6-fold reduction in quetiapine levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-078",
        "drug_a_id": "DB01045",  # Rifampin
        "drug_b_id": "DB00877",  # Sirolimus
        "severity": "critical",
        "description": (
            "Rifampin is one of the most potent CYP3A4 and P-gp inducers. It reduces "
            "sirolimus AUC by approximately 82% and Cmax by 71%. This causes catastrophic "
            "loss of immunosuppression in transplant patients. Combination is contraindicated."
        ),
        "mechanism": "Potent CYP3A4 + P-gp induction by rifampin -> ~82% reduction in sirolimus exposure",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-079",
        "drug_a_id": "DB01045",  # Rifampin
        "drug_b_id": "DB01030",  # Imatinib
        "severity": "major",
        "description": (
            "Rifampin induces CYP3A4, reducing imatinib AUC by approximately 70%. "
            "This dramatically reduces imatinib efficacy in cancer treatment. "
            "Avoid combination; use alternative antibiotics or consider dose doubling "
            "with monitoring if rifampin is unavoidable."
        ),
        "mechanism": "CYP3A4 induction by rifampin -> 70% reduction in imatinib AUC",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-080",
        "drug_a_id": "DB01111",  # Erythromycin
        "drug_b_id": "DB01409",  # Eplerenone
        "severity": "major",
        "description": (
            "Erythromycin (moderate CYP3A4 inhibitor) increases eplerenone exposure "
            "approximately 2-fold. Eplerenone is exclusively metabolized by CYP3A4 and "
            "has a narrow therapeutic window. Increased risk of hyperkalemia and associated "
            "cardiac arrhythmias. Dose reduction of eplerenone to 25mg/day may be necessary."
        ),
        "mechanism": "CYP3A4 inhibition by erythromycin -> elevated eplerenone -> hyperkalemia risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-081",
        "drug_a_id": "DB01026",  # Ketoconazole (already in seed_data.py)
        "drug_b_id": "DB01409",  # Eplerenone
        "severity": "critical",
        "description": (
            "Ketoconazole (strong CYP3A4 inhibitor) increases eplerenone AUC 5.4-fold. "
            "This combination is contraindicated due to the risk of severe hyperkalemia "
            "and potentially fatal cardiac arrhythmias."
        ),
        "mechanism": "Strong CYP3A4 inhibition by ketoconazole -> 5.4-fold eplerenone increase -> hyperkalemia",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-082",
        "drug_a_id": "DB06290",  # Sofosbuvir
        "drug_b_id": "DB01118",  # Amiodarone (already in seed_data.py)
        "severity": "critical",
        "description": (
            "Concomitant use of sofosbuvir-containing regimens with amiodarone causes "
            "serious and potentially fatal bradycardia and heart block. The mechanism is "
            "not fully understood but may involve pharmacodynamic interaction. "
            "This combination is contraindicated; amiodarone's long half-life means the "
            "interaction risk persists months after amiodarone discontinuation."
        ),
        "mechanism": "Unknown mechanism (not CYP-mediated) -> serious symptomatic bradycardia",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-083",
        "drug_a_id": "DB00228",  # Lamotrigine
        "drug_b_id": "DB00252_val",  # Valproic acid (already in seed_data.py)
        "severity": "major",
        "description": (
            "Valproic acid inhibits UGT enzymes responsible for lamotrigine glucuronidation. "
            "Lamotrigine half-life doubles and plasma levels increase approximately 2-fold. "
            "Risk of lamotrigine toxicity (rash, Stevens-Johnson syndrome, ataxia). "
            "Lamotrigine starting dose and escalation rate must be halved when added to valproic acid."
        ),
        "mechanism": "UGT inhibition by valproic acid -> lamotrigine accumulation",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-084",
        "drug_a_id": "DB01156",  # Bupropion
        "drug_b_id": "DB01246",  # Aripiprazole
        "severity": "moderate",
        "description": (
            "Bupropion inhibits CYP2D6, increasing aripiprazole plasma concentrations "
            "approximately 2-fold. FDA labeling recommends reducing aripiprazole dose by "
            "50% when bupropion is added. Monitor for enhanced antipsychotic effects and side effects."
        ),
        "mechanism": "CYP2D6 inhibition by bupropion -> elevated aripiprazole",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-085",
        "drug_a_id": "DB00857",  # Terbinafine
        "drug_b_id": "DB00571",  # Propranolol
        "severity": "moderate",
        "description": (
            "Terbinafine strongly inhibits CYP2D6, the primary metabolizing enzyme for "
            "propranolol. Propranolol plasma levels increase significantly, increasing risk "
            "of bradycardia, hypotension, and bronchospasm. Monitor heart rate and blood pressure."
        ),
        "mechanism": "CYP2D6 inhibition by terbinafine -> elevated propranolol",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-086",
        "drug_a_id": "DB01211",  # Clarithromycin (already in seed_data.py)
        "drug_b_id": "DB01394",  # Colchicine
        "severity": "critical",
        "description": (
            "Clarithromycin inhibits both CYP3A4 and P-glycoprotein, causing dangerous "
            "accumulation of colchicine. Multiple fatalities from this combination have "
            "been reported, particularly in patients with renal impairment. "
            "This combination is contraindicated in patients with renal or hepatic impairment; "
            "extreme caution and dose reduction are required in all patients."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition by clarithromycin -> fatal colchicine toxicity",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-087",
        "drug_a_id": "DB01211",  # Clarithromycin
        "drug_b_id": "DB00877",  # Sirolimus
        "severity": "major",
        "description": (
            "Clarithromycin inhibits CYP3A4 and P-glycoprotein, significantly increasing "
            "sirolimus plasma concentrations. Sirolimus dose reduction of 50-90% may be "
            "required. Intensive therapeutic drug monitoring is necessary."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition by clarithromycin -> elevated sirolimus",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-088",
        "drug_a_id": "DB00625_vori",  # Voriconazole (already in seed_data.py)
        "drug_b_id": "DB00813",  # Fentanyl
        "severity": "major",
        "description": (
            "Voriconazole strongly inhibits CYP3A4, significantly increasing fentanyl "
            "plasma concentrations. Risk of respiratory depression and sedation is increased. "
            "Reduce fentanyl dose and monitor closely for opioid toxicity."
        ),
        "mechanism": "Strong CYP3A4 inhibition by voriconazole -> elevated fentanyl",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-089",
        "drug_a_id": "DB00625_vori",  # Voriconazole
        "drug_b_id": "DB00921",  # Buprenorphine
        "severity": "moderate",
        "description": (
            "Voriconazole inhibits CYP3A4, increasing buprenorphine plasma concentrations "
            "and risk of CNS depression. Monitor for enhanced opioid effects and consider "
            "dose reduction of buprenorphine."
        ),
        "mechanism": "CYP3A4 inhibition by voriconazole -> elevated buprenorphine",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "INT-expanded-090",
        "drug_a_id": "DB01030",  # Imatinib
        "drug_b_id": "DB00682",  # Warfarin
        "severity": "moderate",
        "description": (
            "Imatinib inhibits CYP2D6 and CYP3A4. It also inhibits CYP2C9, the primary "
            "enzyme metabolizing warfarin. Warfarin plasma levels and INR may increase. "
            "Monitor INR closely; use low-molecular-weight heparin as preferred anticoagulant "
            "in patients on imatinib where possible."
        ),
        "mechanism": "CYP2C9 inhibition by imatinib -> elevated warfarin -> bleeding risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
]


# ---------------------------------------------------------------------------
# Expanded Drug-Enzyme Relations — 80+ new entries for expanded drugs
# ---------------------------------------------------------------------------

DRUG_ENZYME_RELATIONS_EXPANDED: list[dict] = [
    # -------------------------------------------------------------------------
    # Antifungals
    # -------------------------------------------------------------------------
    # Posaconazole — strong CYP3A4 inhibitor
    {
        "drug_id": "DB00834",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00834",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Terbinafine — potent CYP2D6 inhibitor
    {
        "drug_id": "DB00857",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00857",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00857",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00857",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    # -------------------------------------------------------------------------
    # Antibiotics
    # -------------------------------------------------------------------------
    # Erythromycin — moderate-strong CYP3A4 inhibitor
    {
        "drug_id": "DB01111",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB01111",
        "enzyme_id": "PGLYCO",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01111",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Levofloxacin — mild CYP1A2 inhibitor
    {"drug_id": "DB00500", "enzyme_id": "CYP1A2", "relation_type": "inhibits", "strength": "weak"},
    # Doxycycline — minimal CYP involvement
    # (no significant enzyme relations)
    # Metronidazole — CYP2C9 inhibitor
    {
        "drug_id": "DB01142",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {"drug_id": "DB01142", "enzyme_id": "CYP3A4", "relation_type": "inhibits", "strength": "weak"},
    # Trimethoprim — CYP2C8 and OCT2 (no listed enzymes in our set)
    # No matching enzyme IDs for CYP2C8 — skip
    # Sulfamethoxazole — CYP2C9 inhibitor
    {
        "drug_id": "DB01015",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Linezolid — minimal CYP metabolism
    # (no significant CYP enzyme relations)
    # Isoniazid — CYP2C9 and CYP2C19 inhibitor
    {
        "drug_id": "DB01051",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01051",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {"drug_id": "DB01051", "enzyme_id": "CYP3A4", "relation_type": "inhibits", "strength": "weak"},
    # -------------------------------------------------------------------------
    # Antivirals / Antiretrovirals
    # -------------------------------------------------------------------------
    # Atazanavir — strong CYP3A4 and UGT1A1 inhibitor
    {
        "drug_id": "DB01072",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {"drug_id": "DB01072", "enzyme_id": "UGTA1", "relation_type": "inhibits", "strength": "strong"},
    {
        "drug_id": "DB01072",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Lopinavir — strong CYP3A4 inhibitor (boosted with ritonavir)
    {
        "drug_id": "DB01601",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB01601",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Sofosbuvir — P-gp substrate
    {
        "drug_id": "DB06290",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Cobicistat — strong CYP3A4 inhibitor
    {
        "drug_id": "DB01068",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    # Efavirenz — CYP3A4 and CYP2B6 inducer; CYP2B6 substrate
    {
        "drug_id": "DB00625_efv",
        "enzyme_id": "CYP3A4",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00625_efv",
        "enzyme_id": "CYP2B6",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00625_efv",
        "enzyme_id": "CYP2B6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00625_efv",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00625_efv",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "weak",
    },
    {
        "drug_id": "DB00625_efv",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "weak",
    },
    # Nevirapine — moderate CYP3A4 and CYP2B6 inducer
    {
        "drug_id": "DB00238",
        "enzyme_id": "CYP3A4",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00238",
        "enzyme_id": "CYP2B6",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00238",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00238",
        "enzyme_id": "CYP2B6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # Cardiovascular
    # -------------------------------------------------------------------------
    # Nifedipine — CYP3A4 substrate
    {
        "drug_id": "DB01107",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Dronedarone — moderate CYP3A4 inhibitor; CYP3A4 substrate; P-gp inhibitor
    {
        "drug_id": "DB00519",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00519",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00519",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00519",
        "enzyme_id": "PGLYCO",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Propranolol — CYP2D6 and CYP1A2 substrate
    {
        "drug_id": "DB00571",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00571",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Carvedilol — CYP2D6 and CYP2C9 substrate; P-gp substrate
    {
        "drug_id": "DB01136",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01136",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01136",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Bisoprolol — CYP3A4 substrate (partial)
    {
        "drug_id": "DB00612",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Eplerenone — exclusive CYP3A4 substrate
    {
        "drug_id": "DB01409",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # -------------------------------------------------------------------------
    # Antidepressants
    # -------------------------------------------------------------------------
    # Paroxetine — potent CYP2D6 inhibitor and substrate
    {
        "drug_id": "DB00715_par",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00715_par",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Bupropion — potent CYP2D6 inhibitor; CYP2B6 substrate
    {
        "drug_id": "DB01156",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB01156",
        "enzyme_id": "CYP2B6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Venlafaxine — CYP2D6 substrate (primary); mild CYP2D6 inhibitor
    {
        "drug_id": "DB00831",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00831",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {"drug_id": "DB00831", "enzyme_id": "CYP2D6", "relation_type": "inhibits", "strength": "weak"},
    # Mirtazapine — CYP1A2, CYP2D6, CYP3A4 substrates
    {
        "drug_id": "DB00370",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00370",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00370",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Nortriptyline — CYP2D6 primary substrate
    {
        "drug_id": "DB00540",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00540",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Desipramine — CYP2D6 primary substrate
    {
        "drug_id": "DB01151",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Trazodone — CYP3A4 substrate
    {
        "drug_id": "DB00656",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # -------------------------------------------------------------------------
    # Antipsychotics
    # -------------------------------------------------------------------------
    # Aripiprazole — CYP2D6 (primary) and CYP3A4 substrates
    {
        "drug_id": "DB01246",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01246",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Quetiapine — CYP3A4 exclusive substrate
    {
        "drug_id": "DB01224",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Olanzapine — CYP1A2 primary; UGT conjugation
    {
        "drug_id": "DB00334",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00334",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Clozapine — CYP1A2 primary; CYP3A4 secondary
    {
        "drug_id": "DB00363",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00363",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00363",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    # Ziprasidone — mainly aldehyde oxidase; minor CYP3A4
    {
        "drug_id": "DB00246",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    # -------------------------------------------------------------------------
    # Anticonvulsants
    # -------------------------------------------------------------------------
    # Topiramate — mild CYP3A4 inducer; CYP2C19 inhibitor
    {"drug_id": "DB00752", "enzyme_id": "CYP3A4", "relation_type": "induces", "strength": "weak"},
    {"drug_id": "DB00752", "enzyme_id": "CYP2C19", "relation_type": "inhibits", "strength": "weak"},
    # Levetiracetam — minimal CYP metabolism
    # (no significant enzyme relations)
    # Lamotrigine — UGT-metabolized (UGT1A4 primarily)
    {
        "drug_id": "DB00228",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Oxcarbazepine — moderate CYP3A4 inducer; CYP2C19 inhibitor
    {
        "drug_id": "DB00949",
        "enzyme_id": "CYP3A4",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00949",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Lacosamide — CYP2C19 substrate
    {
        "drug_id": "DB06218",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # Benzodiazepines
    # -------------------------------------------------------------------------
    # Triazolam — exclusively CYP3A4
    {
        "drug_id": "DB00897",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Lorazepam — UGT-metabolized
    {
        "drug_id": "DB00183",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Clonazepam — CYP3A4 (nitro reduction)
    {
        "drug_id": "DB00564_clz",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # Opioids
    # -------------------------------------------------------------------------
    # Hydrocodone — CYP2D6 and CYP3A4
    {
        "drug_id": "DB00956",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00956",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Fentanyl — exclusively CYP3A4
    {
        "drug_id": "DB00813",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Buprenorphine — primarily CYP3A4
    {
        "drug_id": "DB00921",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00921",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Naloxone — UGT-metabolized
    {
        "drug_id": "DB01183",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # -------------------------------------------------------------------------
    # Immunosuppressants
    # -------------------------------------------------------------------------
    # Sirolimus — CYP3A4 and P-gp substrate
    {
        "drug_id": "DB00877",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00877",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Everolimus — CYP3A4 and P-gp substrate
    {
        "drug_id": "DB01590",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01590",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Mycophenolate mofetil — UGT-metabolized
    {
        "drug_id": "DB00864_myco",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # -------------------------------------------------------------------------
    # Oncology
    # -------------------------------------------------------------------------
    # Imatinib — CYP3A4 (primary); inhibits CYP2D6 and CYP3A4
    {
        "drug_id": "DB01030",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01030",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {"drug_id": "DB01030", "enzyme_id": "CYP3A4", "relation_type": "inhibits", "strength": "weak"},
    # Erlotinib — CYP3A4 primary; CYP1A2 secondary
    {
        "drug_id": "DB00530",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00530",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Crizotinib — CYP3A4 substrate and moderate inhibitor
    {
        "drug_id": "DB08865",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB08865",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # -------------------------------------------------------------------------
    # Food / Supplements
    # -------------------------------------------------------------------------
    # Grapefruit — intestinal CYP3A4 inhibitor
    {
        "drug_id": "DB_GRAPE",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {"drug_id": "DB_GRAPE", "enzyme_id": "PGLYCO", "relation_type": "inhibits", "strength": "weak"},
    # St. John's Wort — CYP3A4 and P-gp inducer
    {"drug_id": "DB_STJ", "enzyme_id": "CYP3A4", "relation_type": "induces", "strength": "strong"},
    {"drug_id": "DB_STJ", "enzyme_id": "PGLYCO", "relation_type": "induces", "strength": "strong"},
    {
        "drug_id": "DB_STJ",
        "enzyme_id": "CYP2C9",
        "relation_type": "induces",
        "strength": "moderate",
    },
    # Turmeric/Curcumin — mild inhibitor at high doses
    {
        "drug_id": "DB_TURMERIC",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "weak",
    },
    {
        "drug_id": "DB_TURMERIC",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "weak",
    },
    {
        "drug_id": "DB_TURMERIC",
        "enzyme_id": "CYP1A2",
        "relation_type": "inhibits",
        "strength": "weak",
    },
    # -------------------------------------------------------------------------
    # Others
    # -------------------------------------------------------------------------
    # Dextromethorphan — CYP2D6 primary; CYP3A4 secondary
    {
        "drug_id": "DB00514",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00514",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Aminophylline -> theophylline: CYP1A2
    {
        "drug_id": "DB00277_ami",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Sildenafil — CYP3A4 primary; CYP2C9 secondary
    {
        "drug_id": "DB00203",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00203",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Tadalafil — exclusively CYP3A4
    {
        "drug_id": "DB01299",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Colchicine — CYP3A4 and P-gp substrate
    {
        "drug_id": "DB01394",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01394",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Apixaban — CYP3A4 and P-gp substrate
    {
        "drug_id": "DB06605",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB06605",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Edoxaban — P-gp substrate (minimal CYP)
    {
        "drug_id": "DB06294",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # -------------------------------------------------------------------------
    # Additional drugs (second batch)
    # -------------------------------------------------------------------------
    # Lovastatin — CYP3A4
    {
        "drug_id": "DB00694",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Rabeprazole — CYP2C19 (minor)
    {
        "drug_id": "DB00213_rabep",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    # Irbesartan — CYP2C9
    {
        "drug_id": "DB00722_irbe",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Pioglitazone — CYP2C8 (no matching enzyme), CYP3A4 secondary
    {
        "drug_id": "DB01132",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    # Ranolazine — CYP3A4 primary; mild inhibitor
    {
        "drug_id": "DB00612_ranola",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00612_ranola",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00612_ranola",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "weak",
    },
    # Nilotinib — CYP3A4 substrate and strong inhibitor
    {
        "drug_id": "DB04896",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB04896",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    # Dasatinib — CYP3A4 substrate
    {
        "drug_id": "DB05765",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Zolmitriptan — CYP1A2
    {
        "drug_id": "DB00315",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Caffeine — CYP1A2 primary substrate
    {
        "drug_id": "DB00316_caffe",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Donepezil — CYP2D6 and CYP3A4
    {
        "drug_id": "DB00843",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00843",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Celecoxib — CYP2C9 primary
    {
        "drug_id": "DB00461",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Meloxicam — CYP2C9 and CYP3A4
    {
        "drug_id": "DB00814",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00814",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    # Ondansetron — CYP1A2, CYP2D6, CYP3A4
    {
        "drug_id": "DB00489",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00489",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00489",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Chlorpromazine — CYP2D6
    {
        "drug_id": "DB00477",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00477",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Citalopram — CYP2C19 and CYP3A4
    {
        "drug_id": "DB01104_escit",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01104_escit",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01104_escit",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "weak",
    },
    # Tamsulosin — CYP3A4 and CYP2D6
    {
        "drug_id": "DB00374",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00374",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Hydroxychloroquine — CYP2D6 inhibitor; CYP2C8 and CYP3A4 substrate
    {
        "drug_id": "DB01611",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01611",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Torsemide — CYP2C9
    {
        "drug_id": "DB00999_tors",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Buspirone — CYP3A4 exclusive
    {
        "drug_id": "DB00448_benzo",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Modafinil — mild CYP3A4 inducer; CYP2C19 inhibitor
    {"drug_id": "DB00580", "enzyme_id": "CYP3A4", "relation_type": "induces", "strength": "weak"},
    {"drug_id": "DB00580", "enzyme_id": "CYP2C19", "relation_type": "inhibits", "strength": "weak"},
    # Estradiol — CYP3A4
    {
        "drug_id": "DB01196",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Finasteride — CYP3A4
    {
        "drug_id": "DB00288",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Sunitinib — CYP3A4
    {
        "drug_id": "DB01268",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Tolterodine — CYP2D6 and CYP3A4
    {
        "drug_id": "DB01036",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01036",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Clobazam — CYP2C19 and CYP3A4; inhibits CYP2D6
    {
        "drug_id": "DB00349",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00349",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00349",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Bedaquiline — CYP3A4
    {
        "drug_id": "DB01051_bed",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Methadone — CYP3A4 primary, CYP2D6, CYP2B6
    {
        "drug_id": "DB00316_metam",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00316_metam",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00316_metam",
        "enzyme_id": "CYP2B6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Phenobarbital — CYP2C9 substrate; potent inducer
    {
        "drug_id": "DB00564_pen",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00564_pen",
        "enzyme_id": "CYP3A4",
        "relation_type": "induces",
        "strength": "strong",
    },
    {
        "drug_id": "DB00564_pen",
        "enzyme_id": "CYP2C9",
        "relation_type": "induces",
        "strength": "strong",
    },
    {
        "drug_id": "DB00564_pen",
        "enzyme_id": "CYP2C19",
        "relation_type": "induces",
        "strength": "strong",
    },
    {
        "drug_id": "DB00564_pen",
        "enzyme_id": "CYP1A2",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00564_pen",
        "enzyme_id": "CYP2B6",
        "relation_type": "induces",
        "strength": "strong",
    },
    # Hydromorphone — UGT-metabolized
    {
        "drug_id": "DB00295_hydro",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Betrixaban — P-gp substrate
    {
        "drug_id": "DB00682_apix2",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Venetoclax — CYP3A4 and P-gp
    {
        "drug_id": "DB09102",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB09102",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Ibrutinib — CYP3A4
    {
        "drug_id": "DB09141",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Olaparib — CYP3A4
    {
        "drug_id": "DB01048_olapar",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Methylprednisolone — CYP3A4
    {
        "drug_id": "DB00616",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Budesonide — CYP3A4
    {
        "drug_id": "DB01234_budes",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Clindamycin — CYP3A4
    {
        "drug_id": "DB01190",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Montelukast — CYP3A4 and CYP2C9 (note: CYP2C8 is primary but not in our enzyme set)
    {
        "drug_id": "DB01048_mont",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01048_mont",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
]
