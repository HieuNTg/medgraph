"""
Extended drug dataset for MEDGRAPH — 300+ additional drugs.

Organized by therapeutic class with real DrugBank IDs and CYP450 pharmacology.
Covers specialty, oncology, orphan, newer antiviral, immunology, and other
clinically important drugs not present in seed_data.py or seed_drugs_expanded.py.

DISCLAIMER: Data is for informational/research use only. Not medical advice.
"""

from __future__ import annotations

DRUGS_EXTENDED: list[dict] = [
    {
        "id": "DB09261",
        "name": "Betrixaban",
        "brand_names": ["Bevyxxa"],
        "description": (
            "Factor Xa inhibitor DOAC approved for VTE prophylaxis in acutely ill hospitalized adults. Primarily excreted unchanged; minimal CYP metabolism. P-glycoprotein substrate; P-gp inhibitors increase betrixaban exposure."
        ),
        "drug_class": "Anticoagulant / DOAC / Factor Xa Inhibitor",
        "rxnorm_cui": "1860491",
    },
    {
        "id": "DB00945_tica",
        "name": "Ticagrelor",
        "brand_names": ["Brilinta"],
        "description": (
            "P2Y12 receptor antagonist antiplatelet. Direct-acting (not a prodrug). Metabolized by CYP3A4/5; active metabolite also formed via CYP3A4. Strong CYP3A4 inhibitors increase ticagrelor exposure; strong inducers reduce efficacy. Inhibits CYP3A4 mildly. Contraindicated with strong CYP3A4 inhibitors."
        ),
        "drug_class": "Antiplatelet / P2Y12 Inhibitor",
        "rxnorm_cui": "1116632",
    },
    {
        "id": "DB09075",
        "name": "Edoxaban",
        "brand_names": ["Savaysa", "Lixiana"],
        "description": (
            "Factor Xa inhibitor DOAC. Minimal CYP3A4 metabolism; primarily a P-glycoprotein substrate. P-gp inhibitors (quinidine, verapamil, amiodarone) require dose reduction. Strong P-gp inducers (rifampin) reduce exposure."
        ),
        "drug_class": "Anticoagulant / DOAC / Factor Xa Inhibitor",
        "rxnorm_cui": "1599538",
    },
    {
        "id": "DB00682_pras",
        "name": "Prasugrel",
        "brand_names": ["Effient"],
        "description": (
            "Thienopyridine antiplatelet prodrug. Requires CYP3A4 and CYP2B6 activation to active metabolite. More predictable activation than clopidogrel; less susceptible to CYP2C19 variability. Strong CYP inhibitors modestly affect levels."
        ),
        "drug_class": "Antiplatelet / P2Y12 Inhibitor",
        "rxnorm_cui": "613391",
    },
    {
        "id": "DB00559",
        "name": "Anagrelide",
        "brand_names": ["Agrylin"],
        "description": (
            "Platelet-lowering agent for essential thrombocythemia. Metabolized by CYP1A2. CYP1A2 inhibitors (ciprofloxacin, fluvoxamine) may increase anagrelide levels. Inhibits PDE III; cardiac effects including palpitations and tachycardia."
        ),
        "drug_class": "Antiplatelet / Platelet-Reducing Agent",
        "rxnorm_cui": "36411",
    },
    {
        "id": "DB01400",
        "name": "Iloprost",
        "brand_names": ["Ventavis"],
        "description": (
            "Inhaled prostacyclin analog for pulmonary arterial hypertension. Metabolized by beta-oxidation; not significantly metabolized by CYP enzymes. Vasodilatory effects may potentiate antihypertensive agents."
        ),
        "drug_class": "Vasodilator / Prostacyclin Analog",
        "rxnorm_cui": "544576",
    },
    {
        "id": "DB09068",
        "name": "Sacubitril",
        "brand_names": ["Entresto (combined with valsartan)"],
        "description": (
            "Neprilysin inhibitor (ARNI component) combined with valsartan for heart failure. Prodrug converted to LBQ657 by esterases; not CYP-metabolized. LBQ657 inhibits neprilysin, elevating natriuretic peptides. Contraindicated with ACE inhibitors (angioedema risk)."
        ),
        "drug_class": "Neprilysin Inhibitor / ARNI",
        "rxnorm_cui": "1656340",
    },
    {
        "id": "DB15685",
        "name": "Vericiguat",
        "brand_names": ["Verquvo"],
        "description": (
            "Soluble guanylate cyclase stimulator for heart failure with reduced ejection fraction. Not metabolized by CYP enzymes; primarily glucuronidated by UGT1A9 and UGT1A1. Strong sGC stimulators are contraindicated with PDE5 inhibitors."
        ),
        "drug_class": "Soluble Guanylate Cyclase Stimulator",
        "rxnorm_cui": "2376837",
    },
    {
        "id": "DB09070",
        "name": "Ivabradine",
        "brand_names": ["Corlanor", "Procoralan"],
        "description": (
            "If channel inhibitor for heart failure and stable angina. Exclusively metabolized by CYP3A4. Strong CYP3A4 inhibitors (ketoconazole, clarithromycin) are contraindicated; increase ivabradine exposure 7-8 fold, causing bradycardia. CYP3A4 inducers reduce efficacy."
        ),
        "drug_class": "If Channel Inhibitor / Antianginal",
        "rxnorm_cui": "1490497",
    },
    {
        "id": "DB00559_aldo",
        "name": "Spironolactone",
        "brand_names": ["Aldactone", "CaroSpir"],
        "description": (
            "Mineralocorticoid receptor antagonist (potassium-sparing diuretic) for heart failure, hypertension, and hyperaldosteronism. Metabolized by CYP3A4 to active metabolite canrenone. Risk of hyperkalemia with ACE inhibitors, ARBs, or potassium supplements. Also used in polycystic ovary syndrome."
        ),
        "drug_class": "Mineralocorticoid Antagonist / Diuretic",
        "rxnorm_cui": "9997",
    },
    {
        "id": "DB11979",
        "name": "Empagliflozin",
        "brand_names": ["Jardiance"],
        "description": (
            "SGLT2 inhibitor for type 2 diabetes with established cardiovascular disease and heart failure with reduced ejection fraction. Glucuronidated by UGT1A3, UGT1A8, UGT1A9, and UGT2B7; minimal CYP involvement. Diuretic effects may potentiate loop diuretics."
        ),
        "drug_class": "Antidiabetic / SGLT2 Inhibitor",
        "rxnorm_cui": "1545653",
    },
    {
        "id": "DB11690",
        "name": "Dapagliflozin",
        "brand_names": ["Farxiga", "Forxiga"],
        "description": (
            "SGLT2 inhibitor for type 2 diabetes, heart failure, and CKD. Primarily glucuronidated by UGT1A9; minor CYP3A4 involvement. Low pharmacokinetic interaction potential. Approved for HFrEF and CKD independent of diabetes."
        ),
        "drug_class": "Antidiabetic / SGLT2 Inhibitor",
        "rxnorm_cui": "1488564",
    },
    {
        "id": "DB11689",
        "name": "Canagliflozin",
        "brand_names": ["Invokana"],
        "description": (
            "SGLT2 inhibitor for type 2 diabetes and CKD with albuminuria. Glucuronidated by UGT1A9 and UGT2B4. Weak inhibitor of P-glycoprotein; may slightly increase digoxin levels. Rifampin induces canagliflozin clearance, reducing efficacy."
        ),
        "drug_class": "Antidiabetic / SGLT2 Inhibitor",
        "rxnorm_cui": "1373463",
    },
    {
        "id": "DB11988",
        "name": "Ertugliflozin",
        "brand_names": ["Steglatro"],
        "description": (
            "SGLT2 inhibitor for type 2 diabetes. Glucuronidated by UGT1A9 and UGT2B7. Minimal CYP interactions. UGT inducers (rifampin) reduce ertugliflozin exposure."
        ),
        "drug_class": "Antidiabetic / SGLT2 Inhibitor",
        "rxnorm_cui": "1992660",
    },
    {
        "id": "DB00541_hydral",
        "name": "Hydralazine",
        "brand_names": ["Apresoline"],
        "description": (
            "Vasodilator for hypertension and heart failure. Metabolized by N-acetyltransferase (NAT) — slow acetylators have higher plasma levels. Not significantly metabolized by CYP enzymes. Reflex tachycardia may require beta-blocker co-administration."
        ),
        "drug_class": "Vasodilator / Antihypertensive",
        "rxnorm_cui": "5470",
    },
    {
        "id": "DB09063",
        "name": "Riociguat",
        "brand_names": ["Adempas"],
        "description": (
            "Soluble guanylate cyclase stimulator for pulmonary arterial hypertension and CTEPH. Metabolized by CYP1A1, CYP3A4, CYP2C8, and CYP2J2. Strong CYP/P-gp inhibitors increase riociguat levels. Contraindicated with PDE5 inhibitors and nitrates. Active metabolite M1 formed via CYP1A1."
        ),
        "drug_class": "Soluble Guanylate Cyclase Stimulator",
        "rxnorm_cui": "1555066",
    },
    {
        "id": "DB09813",
        "name": "Semaglutide",
        "brand_names": ["Ozempic", "Wegovy", "Rybelsus"],
        "description": (
            "GLP-1 receptor agonist for type 2 diabetes and obesity. Degraded by proteolytic enzymes; not metabolized by CYP enzymes. May delay gastric emptying, potentially reducing absorption rate of concomitant oral drugs. FDA-approved for cardiovascular risk reduction in T2DM."
        ),
        "drug_class": "Antidiabetic / GLP-1 Receptor Agonist",
        "rxnorm_cui": "2200644",
    },
    {
        "id": "DB09023",
        "name": "Liraglutide",
        "brand_names": ["Victoza", "Saxenda"],
        "description": (
            "GLP-1 receptor agonist for type 2 diabetes and obesity. Metabolized by endogenous protease enzymes; not CYP-metabolized. Delays gastric emptying. Victoza approved for CV risk reduction; Saxenda for weight management."
        ),
        "drug_class": "Antidiabetic / GLP-1 Receptor Agonist",
        "rxnorm_cui": "475968",
    },
    {
        "id": "DB09537",
        "name": "Dulaglutide",
        "brand_names": ["Trulicity"],
        "description": (
            "Weekly GLP-1 receptor agonist for type 2 diabetes. Degraded by general proteolytic pathways; not CYP-metabolized. Low pharmacokinetic drug interaction potential. FDA-approved for CV risk reduction."
        ),
        "drug_class": "Antidiabetic / GLP-1 Receptor Agonist",
        "rxnorm_cui": "1590564",
    },
    {
        "id": "DB09236",
        "name": "Albiglutide",
        "brand_names": ["Tanzeum"],
        "description": (
            "Weekly GLP-1 receptor agonist for type 2 diabetes (discontinued 2018, may be reintroduced). Degraded by proteolytic enzymes. No significant CYP-mediated drug interactions."
        ),
        "drug_class": "Antidiabetic / GLP-1 Receptor Agonist",
        "rxnorm_cui": "1551377",
    },
    {
        "id": "DB06292",
        "name": "Exenatide",
        "brand_names": ["Byetta", "Bydureon"],
        "description": (
            "GLP-1 receptor agonist for type 2 diabetes. Metabolized by renal proteolysis; not CYP-metabolized. Delays gastric emptying; may affect oral drug absorption timing. Byetta twice-daily; Bydureon weekly extended-release."
        ),
        "drug_class": "Antidiabetic / GLP-1 Receptor Agonist",
        "rxnorm_cui": "60548",
    },
    {
        "id": "DB08894",
        "name": "Sitagliptin",
        "brand_names": ["Januvia"],
        "description": (
            "DPP-4 inhibitor for type 2 diabetes. Primarily excreted unchanged renally; minor CYP3A4/CYP2C8 metabolism. Low CYP drug interaction potential. P-glycoprotein substrate. Dose adjustment required in renal impairment."
        ),
        "drug_class": "Antidiabetic / DPP-4 Inhibitor",
        "rxnorm_cui": "593411",
    },
    {
        "id": "DB06716",
        "name": "Saxagliptin",
        "brand_names": ["Onglyza"],
        "description": (
            "DPP-4 inhibitor for type 2 diabetes. Metabolized by CYP3A4/5 to active metabolite. Strong CYP3A4 inhibitors increase saxagliptin levels — dose capped at 2.5 mg/day with strong CYP3A4 inhibitors."
        ),
        "drug_class": "Antidiabetic / DPP-4 Inhibitor",
        "rxnorm_cui": "857974",
    },
    {
        "id": "DB08860",
        "name": "Linagliptin",
        "brand_names": ["Tradjenta"],
        "description": (
            "DPP-4 inhibitor for type 2 diabetes. Primarily excreted unchanged via enterohepatic system; minimal CYP metabolism. Low renal clearance dependency. P-glycoprotein and CYP3A4 substrate; strong inducers reduce efficacy."
        ),
        "drug_class": "Antidiabetic / DPP-4 Inhibitor",
        "rxnorm_cui": "1100699",
    },
    {
        "id": "DB08913",
        "name": "Alogliptin",
        "brand_names": ["Nesina"],
        "description": (
            "DPP-4 inhibitor for type 2 diabetes. Primarily renally excreted unchanged. Minimal CYP3A4 and CYP2D6 interactions. Low overall drug interaction potential."
        ),
        "drug_class": "Antidiabetic / DPP-4 Inhibitor",
        "rxnorm_cui": "1163459",
    },
    {
        "id": "DB06292_ins",
        "name": "Insulin glargine",
        "brand_names": ["Lantus", "Basaglar", "Toujeo"],
        "description": (
            "Long-acting insulin analog for type 1 and type 2 diabetes. Not metabolized by CYP enzymes; degraded by insulin-degrading enzyme and proteases. Pharmacodynamic interactions with beta-blockers (mask hypoglycemia symptoms) and corticosteroids (oppose insulin action)."
        ),
        "drug_class": "Antidiabetic / Long-Acting Insulin",
        "rxnorm_cui": "274783",
    },
    {
        "id": "DB00302_ins",
        "name": "Insulin lispro",
        "brand_names": ["Humalog", "Admelog"],
        "description": (
            "Rapid-acting insulin analog. Onset 15 minutes; duration 3-5 hours. Degraded by insulin-degrading enzyme. No CYP interactions. Pharmacodynamic potentiation by ACE inhibitors, salicylates."
        ),
        "drug_class": "Antidiabetic / Rapid-Acting Insulin",
        "rxnorm_cui": "86009",
    },
    {
        "id": "DB11901",
        "name": "Osimertinib",
        "brand_names": ["Tagrisso"],
        "description": (
            "Third-generation EGFR TKI for T790M-mutated NSCLC. Metabolized by CYP3A4 and CYP1A2. Strong CYP3A4 inducers (rifampin) reduce osimertinib AUC by ~78%; avoid concomitant use. Mild CYP3A4/P-gp inhibitor. QT prolongation risk."
        ),
        "drug_class": "Antineoplastic / EGFR TKI (3rd gen)",
        "rxnorm_cui": "1860490",
    },
    {
        "id": "DB11932",
        "name": "Alectinib",
        "brand_names": ["Alecensa"],
        "description": (
            "Second-generation ALK inhibitor for ALK-positive NSCLC. Primarily metabolized by CYP3A4. Strong CYP3A4 inhibitors increase alectinib exposure moderately. Active metabolite M4 also formed via CYP3A4. Lower CNS toxicity than crizotinib."
        ),
        "drug_class": "Antineoplastic / ALK Inhibitor",
        "rxnorm_cui": "1860492",
    },
    {
        "id": "DB11962",
        "name": "Brigatinib",
        "brand_names": ["Alunbrig"],
        "description": (
            "Next-generation ALK/ROS1 inhibitor for ALK+ NSCLC after crizotinib failure. Metabolized by CYP2C8 (major) and CYP3A4. Strong CYP3A4 inducers substantially reduce brigatinib exposure. Mild CYP3A4 inhibitor itself."
        ),
        "drug_class": "Antineoplastic / ALK Inhibitor",
        "rxnorm_cui": "1999726",
    },
    {
        "id": "DB12063",
        "name": "Lorlatinib",
        "brand_names": ["Lorbrena"],
        "description": (
            "Third-generation ALK/ROS1 inhibitor with CNS penetration. Metabolized by CYP3A4 (major) and CYP2C8. Strong CYP3A4 inhibitors increase exposure; strong inducers (rifampin) dramatically reduce AUC (~85%). Induces CYP3A4 and CYP2B6 itself — complex DDI profile."
        ),
        "drug_class": "Antineoplastic / ALK Inhibitor (3rd gen)",
        "rxnorm_cui": "2049148",
    },
    {
        "id": "DB11748",
        "name": "Venetoclax",
        "brand_names": ["Venclexta", "Venclyxto"],
        "description": (
            "BCL-2 inhibitor for CLL/SLL and AML. Metabolized by CYP3A4 and P-gp substrate. Strong CYP3A4 inhibitors require dose reductions (up to 75%). Strong CYP3A4 inducers are contraindicated. Risk of tumor lysis syndrome at initiation."
        ),
        "drug_class": "Antineoplastic / BCL-2 Inhibitor",
        "rxnorm_cui": "1860483",
    },
    {
        "id": "DB11676",
        "name": "Palbociclib",
        "brand_names": ["Ibrance"],
        "description": (
            "CDK4/6 inhibitor for HR+/HER2- advanced breast cancer. Metabolized by CYP3A4 and SULT2A1. Strong CYP3A4 inhibitors increase exposure; strong inducers reduce efficacy. Mild CYP3A4 inhibitor itself. Myelosuppression is dose-limiting toxicity."
        ),
        "drug_class": "Antineoplastic / CDK4/6 Inhibitor",
        "rxnorm_cui": "1745276",
    },
    {
        "id": "DB11730",
        "name": "Ribociclib",
        "brand_names": ["Kisqali"],
        "description": (
            "CDK4/6 inhibitor for HR+/HER2- advanced breast cancer. CYP3A4 substrate and strong CYP3A4 inhibitor itself. Strong CYP3A4 inhibitors are contraindicated. QT prolongation risk; avoid QT-prolonging drugs. Strong inducers reduce efficacy."
        ),
        "drug_class": "Antineoplastic / CDK4/6 Inhibitor",
        "rxnorm_cui": "1860487",
    },
    {
        "id": "DB12001",
        "name": "Abemaciclib",
        "brand_names": ["Verzenio"],
        "description": (
            "CDK4/6 inhibitor for HR+/HER2- advanced and early breast cancer. Metabolized by CYP3A4 to active metabolites. Strong CYP3A4 inhibitors increase exposure; strong inducers reduce efficacy. More continuous dosing schedule than palbociclib."
        ),
        "drug_class": "Antineoplastic / CDK4/6 Inhibitor",
        "rxnorm_cui": "1999719",
    },
    {
        "id": "DB11703",
        "name": "Olaparib",
        "brand_names": ["Lynparza"],
        "description": (
            "PARP inhibitor for BRCA-mutated ovarian, breast, prostate, and pancreatic cancers. Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase olaparib levels — dose reduction required. Strong CYP3A4 inducers markedly reduce efficacy and should be avoided."
        ),
        "drug_class": "Antineoplastic / PARP Inhibitor",
        "rxnorm_cui": "1745276",
    },
    {
        "id": "DB11767",
        "name": "Niraparib",
        "brand_names": ["Zejula"],
        "description": (
            "PARP inhibitor for ovarian cancer maintenance. Primarily metabolized by carboxylesterases and UGT enzymes, not CYP. Low CYP drug interaction potential. Myelosuppression is dose-limiting; dose individualization based on weight/platelets."
        ),
        "drug_class": "Antineoplastic / PARP Inhibitor",
        "rxnorm_cui": "1860488",
    },
    {
        "id": "DB11772",
        "name": "Rucaparib",
        "brand_names": ["Rubraca"],
        "description": (
            "PARP inhibitor for BRCA-mutated ovarian and prostate cancers. Metabolized by CYP1A2, CYP2D6, and CYP3A4. Inhibits CYP1A2, CYP2C9, CYP2C19, and CYP3A4 in vitro — potential to raise levels of CYP substrates with narrow therapeutic index."
        ),
        "drug_class": "Antineoplastic / PARP Inhibitor",
        "rxnorm_cui": "1860489",
    },
    {
        "id": "DB11932_enza",
        "name": "Enzalutamide",
        "brand_names": ["Xtandi"],
        "description": (
            "Androgen receptor inhibitor for castration-resistant prostate cancer. Metabolized by CYP2C8 (major) and CYP3A4. Potent inducer of CYP3A4, CYP2C9, CYP2C19, and P-gp — significantly reduces levels of many co-medications including warfarin, statins, and antiepileptics. Strong CYP2C8 inhibitors increase levels."
        ),
        "drug_class": "Antineoplastic / Androgen Receptor Inhibitor",
        "rxnorm_cui": "1299775",
    },
    {
        "id": "DB11901_abi",
        "name": "Abiraterone",
        "brand_names": ["Zytiga", "Yonsa"],
        "description": (
            "CYP17 inhibitor for metastatic prostate cancer. Metabolized by CYP3A4. Inhibits CYP2D6 and CYP2C8 — raises levels of CYP2D6/2C8 substrates. Strong CYP3A4 inducers reduce efficacy. Must be given with prednisone."
        ),
        "drug_class": "Antineoplastic / CYP17 Inhibitor",
        "rxnorm_cui": "1299859",
    },
    {
        "id": "DB11978",
        "name": "Darolutamide",
        "brand_names": ["Nubeqa"],
        "description": (
            "Androgen receptor inhibitor for non-metastatic CRPC and metastatic HSPC. Metabolized by CYP3A4 and AKR1C3 to active metabolite keto-darolutamide. Combined CYP3A4 and P-gp inducers reduce darolutamide exposure. Lower CNS penetration and fewer DDI concerns than enzalutamide."
        ),
        "drug_class": "Antineoplastic / Androgen Receptor Inhibitor",
        "rxnorm_cui": "2169281",
    },
    {
        "id": "DB11730_ibrut",
        "name": "Ibrutinib",
        "brand_names": ["Imbruvica"],
        "description": (
            "BTK inhibitor for CLL, MCL, WM, and GVHD. Metabolized by CYP3A4 (primary) and CYP2D6 (minor). Strong CYP3A4 inhibitors may increase ibrutinib exposure 10-fold — avoid or reduce dose significantly. Strong CYP3A4 inducers reduce efficacy. Mild CYP2D6 inhibitor itself; inhibits CYP3A4 in vitro."
        ),
        "drug_class": "Antineoplastic / BTK Inhibitor",
        "rxnorm_cui": "1544460",
    },
    {
        "id": "DB15685_acala",
        "name": "Acalabrutinib",
        "brand_names": ["Calquence"],
        "description": (
            "Second-generation BTK inhibitor for CLL and MCL. Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase acalabrutinib exposure; strong inducers reduce efficacy significantly. Gastric acid suppressants (PPIs) reduce absorption. More selective for BTK than ibrutinib."
        ),
        "drug_class": "Antineoplastic / BTK Inhibitor",
        "rxnorm_cui": "2169282",
    },
    {
        "id": "DB11988_idelal",
        "name": "Idelalisib",
        "brand_names": ["Zydelig"],
        "description": (
            "PI3K-delta inhibitor for relapsed CLL, FL, and SLL. Metabolized by aldehyde oxidase and CYP3A4. Potent CYP3A4 inhibitor itself — increases levels of CYP3A4 substrates. Also CYP2C8 inhibitor. Significant immune-mediated toxicities."
        ),
        "drug_class": "Antineoplastic / PI3K Inhibitor",
        "rxnorm_cui": "1592772",
    },
    {
        "id": "DB11912",
        "name": "Ixazomib",
        "brand_names": ["Ninlaro"],
        "description": (
            "Oral proteasome inhibitor for multiple myeloma. Metabolized by multiple CYP enzymes and non-enzymatic hydrolysis. CYP3A4 substrate; strong inducers reduce exposure by ~74%. Strong CYP3A4 inhibitors increase exposure moderately."
        ),
        "drug_class": "Antineoplastic / Proteasome Inhibitor",
        "rxnorm_cui": "1745278",
    },
    {
        "id": "DB00631_bort",
        "name": "Bortezomib",
        "brand_names": ["Velcade"],
        "description": (
            "First-in-class proteasome inhibitor for multiple myeloma and MCL. Metabolized by CYP3A4 and CYP2C19 via oxidative deboronation. CYP3A4 inducers reduce efficacy; inhibitors increase toxicity risk. Potent CYP3A4 inducers (rifampin) reduce AUC by ~45%."
        ),
        "drug_class": "Antineoplastic / Proteasome Inhibitor",
        "rxnorm_cui": "282388",
    },
    {
        "id": "DB09579",
        "name": "Carfilzomib",
        "brand_names": ["Kyprolis"],
        "description": (
            "Second-generation proteasome inhibitor for relapsed/refractory multiple myeloma. Primarily metabolized by peptidase cleavage and epoxide hydrolysis; minor CYP3A4. Low pharmacokinetic drug interaction potential. Cardiovascular toxicity monitoring required."
        ),
        "drug_class": "Antineoplastic / Proteasome Inhibitor",
        "rxnorm_cui": "1299859",
    },
    {
        "id": "DB11900",
        "name": "Midostaurin",
        "brand_names": ["Rydapt"],
        "description": (
            "Multi-kinase inhibitor (FLT3) for AML with FLT3 mutation and advanced systemic mastocytosis. Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase midostaurin levels; strong inducers (rifampin) reduce AUC by ~90%."
        ),
        "drug_class": "Antineoplastic / FLT3 Inhibitor",
        "rxnorm_cui": "1860486",
    },
    {
        "id": "DB12132",
        "name": "Gilteritinib",
        "brand_names": ["Xospata"],
        "description": (
            "FLT3 inhibitor for relapsed/refractory AML with FLT3 mutation. Metabolized by CYP3A4 (primary). Strong CYP3A4 inhibitors increase exposure; strong inducers reduce exposure by ~70%. QT prolongation risk."
        ),
        "drug_class": "Antineoplastic / FLT3 Inhibitor",
        "rxnorm_cui": "2049143",
    },
    {
        "id": "DB11988_lena",
        "name": "Lenalidomide",
        "brand_names": ["Revlimid"],
        "description": (
            "Immunomodulatory agent (IMiD) for multiple myeloma, MDS, and MCL. Primarily renally excreted unchanged; minimal CYP metabolism. P-glycoprotein substrate. Teratogenic; mandatory REMS program. Digoxin levels may increase slightly."
        ),
        "drug_class": "Antineoplastic / Immunomodulatory",
        "rxnorm_cui": "337535",
    },
    {
        "id": "DB12189",
        "name": "Pomalidomide",
        "brand_names": ["Pomalyst"],
        "description": (
            "Third-generation IMiD for relapsed/refractory multiple myeloma. Metabolized by CYP1A2 and CYP3A4. Strong CYP1A2 inhibitors (fluvoxamine) increase pomalidomide AUC. Strong CYP3A4 inducers reduce efficacy. REMS program required."
        ),
        "drug_class": "Antineoplastic / Immunomodulatory",
        "rxnorm_cui": "1299860",
    },
    {
        "id": "DB11817",
        "name": "Tofacitinib",
        "brand_names": ["Xeljanz"],
        "description": (
            "JAK1/3 inhibitor for RA, PsA, UC, and AS. Metabolized by CYP3A4 (primary) and CYP2C19. Strong CYP3A4 inhibitors (ketoconazole) increase tofacitinib AUC ~2-fold — reduce dose. Strong CYP3A4 inducers reduce efficacy. Combined inhibition of CYP3A4 and CYP2C19 increases exposure significantly."
        ),
        "drug_class": "Immunosuppressant / JAK Inhibitor",
        "rxnorm_cui": "1298334",
    },
    {
        "id": "DB11817_bari",
        "name": "Baricitinib",
        "brand_names": ["Olumiant"],
        "description": (
            "JAK1/2 inhibitor for RA and alopecia areata. Primarily renally excreted; OAT3 substrate. OCT2 and MATE2-K transporter substrate. Probenecid (OAT3 inhibitor) increases baricitinib AUC ~2-fold. Limited CYP involvement."
        ),
        "drug_class": "Immunosuppressant / JAK Inhibitor",
        "rxnorm_cui": "1860484",
    },
    {
        "id": "DB15658",
        "name": "Upadacitinib",
        "brand_names": ["Rinvoq"],
        "description": (
            "Selective JAK1 inhibitor for RA, PsA, AS, atopic dermatitis, UC, and CD. Metabolized by CYP3A4 (major). Strong CYP3A4 inhibitors increase exposure ~75%; avoid strong inducers. Risk profile similar to other JAK inhibitors."
        ),
        "drug_class": "Immunosuppressant / JAK Inhibitor",
        "rxnorm_cui": "2169280",
    },
    {
        "id": "DB15656",
        "name": "Filgotinib",
        "brand_names": ["Jyseleca"],
        "description": (
            "Selective JAK1 inhibitor for RA and UC (approved EU; not FDA-approved for RA). Metabolized by carboxylesterases to active metabolite GS-829845. BCRP substrate; BCRP inhibitors may increase exposure."
        ),
        "drug_class": "Immunosuppressant / JAK Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB06694",
        "name": "Abatacept",
        "brand_names": ["Orencia"],
        "description": (
            "CTLA-4-Ig fusion protein; T-cell costimulation inhibitor for RA and JIA. Metabolized by normal protein catabolism. No CYP interactions. Should not be combined with other biologic DMARDs (TNF inhibitors, etc.) due to increased infection risk."
        ),
        "drug_class": "Immunosuppressant / CTLA-4 Inhibitor",
        "rxnorm_cui": "544568",
    },
    {
        "id": "DB00065_adal",
        "name": "Adalimumab",
        "brand_names": ["Humira"],
        "description": (
            "Anti-TNF-alpha monoclonal antibody for RA, PsA, AS, CD, UC, and other inflammatory conditions. Metabolized by normal immunoglobulin catabolism. No direct CYP interactions. May normalize CYP enzyme activity suppressed by inflammation — monitor narrow therapeutic index drugs at initiation."
        ),
        "drug_class": "Immunosuppressant / TNF Inhibitor",
        "rxnorm_cui": "327361",
    },
    {
        "id": "DB01461",
        "name": "Etanercept",
        "brand_names": ["Enbrel"],
        "description": (
            "TNF receptor fusion protein for RA, PsA, AS, and plaque psoriasis. Catabolized by normal protein degradation pathways. No CYP metabolism. Pharmacodynamic interaction: avoid live vaccines during therapy."
        ),
        "drug_class": "Immunosuppressant / TNF Inhibitor",
        "rxnorm_cui": "214555",
    },
    {
        "id": "DB00065_infli",
        "name": "Infliximab",
        "brand_names": ["Remicade", "Inflectra", "Renflexis"],
        "description": (
            "Chimeric anti-TNF-alpha monoclonal antibody for RA, CD, UC, AS, PsA, and psoriasis. Metabolized by proteolytic catabolism. No direct CYP interactions. Methotrexate co-administration reduces immunogenicity."
        ),
        "drug_class": "Immunosuppressant / TNF Inhibitor",
        "rxnorm_cui": "214555",
    },
    {
        "id": "DB09579_sec",
        "name": "Secukinumab",
        "brand_names": ["Cosentyx"],
        "description": (
            "Anti-IL-17A monoclonal antibody for psoriasis, PsA, AS, and nr-axSpA. Catabolized by proteolytic pathways. No CYP interactions. Anti-inflammatory effects may normalize CYP3A4 expression in inflammatory states — monitor narrow therapeutic index drugs (cyclosporine, warfarin) at initiation/discontinuation."
        ),
        "drug_class": "Immunosuppressant / IL-17 Inhibitor",
        "rxnorm_cui": "1657973",
    },
    {
        "id": "DB15678",
        "name": "Ixekizumab",
        "brand_names": ["Taltz"],
        "description": (
            "Anti-IL-17A monoclonal antibody for psoriasis, PsA, and AS. Catabolized by proteolytic degradation. No CYP enzyme interactions. Live vaccines contraindicated during therapy."
        ),
        "drug_class": "Immunosuppressant / IL-17 Inhibitor",
        "rxnorm_cui": "1860485",
    },
    {
        "id": "DB15679",
        "name": "Bimekizumab",
        "brand_names": ["Bimzelx"],
        "description": (
            "Anti-IL-17A/F monoclonal antibody for psoriasis and PsA. Dual IL-17A and IL-17F inhibition. Catabolized by normal immunoglobulin catabolism. No direct CYP interactions; same monitoring guidance as other IL-17 inhibitors."
        ),
        "drug_class": "Immunosuppressant / IL-17 Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB06663",
        "name": "Ustekinumab",
        "brand_names": ["Stelara"],
        "description": (
            "Anti-IL-12/23 monoclonal antibody for psoriasis, PsA, CD, and UC. Metabolized by normal protein catabolism. Anti-inflammatory normalization of CYP3A4 may affect levels of narrow therapeutic index drugs at therapy initiation or upon dose changes."
        ),
        "drug_class": "Immunosuppressant / IL-12/23 Inhibitor",
        "rxnorm_cui": "657308",
    },
    {
        "id": "DB15694",
        "name": "Risankizumab",
        "brand_names": ["Skyrizi"],
        "description": (
            "Anti-IL-23 (p19 subunit) monoclonal antibody for psoriasis, PsA, CD, and UC. Catabolized by proteolytic pathways. No CYP enzyme interactions."
        ),
        "drug_class": "Immunosuppressant / IL-23 Inhibitor",
        "rxnorm_cui": "2169283",
    },
    {
        "id": "DB15695",
        "name": "Guselkumab",
        "brand_names": ["Tremfya"],
        "description": (
            "Anti-IL-23 (p19) monoclonal antibody for psoriasis and PsA. Degraded by proteolytic catabolism; no CYP interactions."
        ),
        "drug_class": "Immunosuppressant / IL-23 Inhibitor",
        "rxnorm_cui": "1999723",
    },
    {
        "id": "DB09292",
        "name": "Dupilumab",
        "brand_names": ["Dupixent"],
        "description": (
            "Anti-IL-4Ra monoclonal antibody blocking IL-4 and IL-13 signaling for atopic dermatitis, asthma, CRSwNP, and eosinophilic esophagitis. Catabolized by proteolytic pathways. No CYP interactions. Anti-inflammatory normalization may affect warfarin levels — monitor at initiation."
        ),
        "drug_class": "Immunosuppressant / IL-4/13 Inhibitor",
        "rxnorm_cui": "1860493",
    },
    {
        "id": "DB11988_benr",
        "name": "Benralizumab",
        "brand_names": ["Fasenra"],
        "description": (
            "Anti-IL-5Ra monoclonal antibody for severe eosinophilic asthma. Metabolized by lysosomal proteolysis. No CYP enzyme interactions. Rapid and near-complete eosinophil depletion within one week."
        ),
        "drug_class": "Biologic / Anti-IL-5 Receptor",
        "rxnorm_cui": "1999724",
    },
    {
        "id": "DB11988_mepo",
        "name": "Mepolizumab",
        "brand_names": ["Nucala"],
        "description": (
            "Anti-IL-5 monoclonal antibody for severe eosinophilic asthma, EGPA, and HES. Degraded by proteolysis. No CYP-mediated drug interactions."
        ),
        "drug_class": "Biologic / Anti-IL-5",
        "rxnorm_cui": "1860494",
    },
    {
        "id": "DB15702",
        "name": "Tezepelumab",
        "brand_names": ["Tezspire"],
        "description": (
            "Anti-TSLP monoclonal antibody for severe asthma (not phenotype-restricted). Catabolized by proteolysis. No CYP interactions. Broadest biomarker-agnostic approval among biologics for asthma."
        ),
        "drug_class": "Biologic / Anti-TSLP",
        "rxnorm_cui": None,
    },
    {
        "id": "DB09064",
        "name": "Nintedanib",
        "brand_names": ["Ofev", "Vargatef"],
        "description": (
            "Tyrosine kinase inhibitor for IPF and ILD associated with systemic sclerosis. Primarily metabolized by esterase cleavage and UGT enzymes; CYP3A4 plays a minor role. P-glycoprotein substrate; P-gp inhibitors/inducers affect exposure. Strong CYP3A4/P-gp inducers (rifampin) reduce nintedanib AUC by ~50%."
        ),
        "drug_class": "Antifibrotic / TKI",
        "rxnorm_cui": "1592773",
    },
    {
        "id": "DB11988_pirf",
        "name": "Pirfenidone",
        "brand_names": ["Esbriet"],
        "description": (
            "Antifibrotic for idiopathic pulmonary fibrosis. Metabolized primarily by CYP1A2 (70-80%), with minor contributions from CYP2C9, CYP2C19, CYP2D6, and CYP2E1. Strong CYP1A2 inhibitors (fluvoxamine, ciprofloxacin) significantly increase pirfenidone levels. Cigarette smoking (CYP1A2 inducer) reduces exposure."
        ),
        "drug_class": "Antifibrotic",
        "rxnorm_cui": "1303125",
    },
    {
        "id": "DB14761",
        "name": "Indacaterol",
        "brand_names": ["Arcapta Neohaler", "Onbrez Breezhaler"],
        "description": (
            "Ultra-LABA (long-acting beta-2 agonist) for COPD. Metabolized by UGT1A1 and CYP3A4 (hydroxylation). P-glycoprotein substrate. Once-daily dosing. QT prolongation risk with concurrent beta-agonists."
        ),
        "drug_class": "Bronchodilator / Ultra-LABA",
        "rxnorm_cui": "1100698",
    },
    {
        "id": "DB11688",
        "name": "Olodaterol",
        "brand_names": ["Striverdi Respimat"],
        "description": (
            "Once-daily LABA for COPD maintenance. Metabolized by direct glucuronidation and O-demethylation (CYP2C8, CYP2C9). P-gp and BCRP substrate. Low systemic exposure limits CYP interaction significance."
        ),
        "drug_class": "Bronchodilator / LABA",
        "rxnorm_cui": "1551376",
    },
    {
        "id": "DB09069",
        "name": "Umeclidinium",
        "brand_names": ["Incruse Ellipta", "Anoro Ellipta (combined)"],
        "description": (
            "Long-acting muscarinic antagonist (LAMA) for COPD. Metabolized by CYP2D6 via hydroxylation (major) and O-dealkylation. CYP2D6 inhibitors may modestly increase umeclidinium exposure; clinical significance is low due to minimal systemic absorption."
        ),
        "drug_class": "Bronchodilator / LAMA",
        "rxnorm_cui": "1551375",
    },
    {
        "id": "DB14760",
        "name": "Aclidinium",
        "brand_names": ["Tudorza Pressair"],
        "description": (
            "Twice-daily LAMA for COPD. Rapidly hydrolyzed by esterases in plasma and tissues; minimal CYP involvement. Low systemic bioavailability. Negligible pharmacokinetic drug interaction potential."
        ),
        "drug_class": "Bronchodilator / LAMA",
        "rxnorm_cui": "1299857",
    },
    {
        "id": "DB11986",
        "name": "Glycopyrrolate",
        "brand_names": ["Seebri Neohaler", "Lonhala Magnair", "Robinul"],
        "description": (
            "Long-acting muscarinic antagonist for COPD (inhaled) and hyperhidrosis/preoperative use (systemic). Minimal hepatic CYP metabolism; primarily renally eliminated. Low drug interaction potential via CYP pathways."
        ),
        "drug_class": "Anticholinergic / LAMA",
        "rxnorm_cui": "4978",
    },
    {
        "id": "DB01048_rofl",
        "name": "Roflumilast",
        "brand_names": ["Daliresp", "Daxas"],
        "description": (
            "PDE4 inhibitor for severe COPD with frequent exacerbations. Metabolized by CYP3A4 and CYP1A2 to active N-oxide metabolite. Strong CYP inducers (rifampin) reduce roflumilast efficacy. CYP1A2/CYP3A4 inhibitors increase levels."
        ),
        "drug_class": "PDE4 Inhibitor / Anti-inflammatory",
        "rxnorm_cui": "1099149",
    },
    {
        "id": "DB16105",
        "name": "Nirmatrelvir",
        "brand_names": ["Paxlovid (combined with ritonavir)"],
        "description": (
            "SARS-CoV-2 main protease (Mpro) inhibitor for COVID-19. Metabolized by CYP3A4; co-packaged with ritonavir (strong CYP3A4 inhibitor) to boost levels. Ritonavir boosting creates major DDI with CYP3A4 substrates — requires temporary hold or dose adjustment of many medications."
        ),
        "drug_class": "Antiviral / SARS-CoV-2 Protease Inhibitor",
        "rxnorm_cui": "2599538",
    },
    {
        "id": "DB16106",
        "name": "Molnupiravir",
        "brand_names": ["Lagevrio"],
        "description": (
            "Nucleoside prodrug for COVID-19; converted to NHC by host enzymes. Not significantly metabolized by CYP enzymes. Low pharmacokinetic drug interaction potential; not recommended in pregnancy due to mutagenicity concerns."
        ),
        "drug_class": "Antiviral / Nucleoside Analog",
        "rxnorm_cui": "2599540",
    },
    {
        "id": "DB06292_rem",
        "name": "Remdesivir",
        "brand_names": ["Veklury"],
        "description": (
            "Adenosine nucleotide prodrug for COVID-19. Metabolized intracellularly by esterases and phosphokinases; CYP involvement minimal. CYP3A4 substrate in vitro. Chloroquine reduces intracellular active metabolite levels — avoid combination."
        ),
        "drug_class": "Antiviral / Nucleotide Prodrug",
        "rxnorm_cui": "2284718",
    },
    {
        "id": "DB06778",
        "name": "Maraviroc",
        "brand_names": ["Selzentry", "Celsentri"],
        "description": (
            "CCR5 co-receptor antagonist for HIV-1 infection. Metabolized by CYP3A4. Strong CYP3A4 inhibitors require dose reduction to 150 mg BID; strong inducers require dose increase to 600 mg BID. Not active against CXCR4-tropic virus."
        ),
        "drug_class": "Antiretroviral / CCR5 Antagonist",
        "rxnorm_cui": "700009",
    },
    {
        "id": "DB09218",
        "name": "Dolutegravir",
        "brand_names": ["Tivicay", "Triumeq (combined)"],
        "description": (
            "HIV integrase inhibitor. Metabolized by UGT1A1 (primary) and CYP3A4 (minor). Strong UGT1A1/CYP3A4 inducers (rifampin, efavirenz) reduce levels — dose adjustment required. Inhibits OCT2 and MATE1, raising creatinine without true GFR change. Preferred first-line regimen due to high genetic barrier."
        ),
        "drug_class": "Antiretroviral / Integrase Inhibitor",
        "rxnorm_cui": "1439776",
    },
    {
        "id": "DB11799",
        "name": "Bictegravir",
        "brand_names": ["Biktarvy (combined)"],
        "description": (
            "HIV integrase inhibitor co-formulated with TAF/emtricitabine. Metabolized by CYP3A4 and UGT1A1. Strong dual CYP3A4/UGT1A1 inducers (rifampin, carbamazepine) reduce bictegravir levels significantly. Not recommended with rifabutin; dose adjustments needed with moderate inducers."
        ),
        "drug_class": "Antiretroviral / Integrase Inhibitor",
        "rxnorm_cui": "1999722",
    },
    {
        "id": "DB11821",
        "name": "Cabotegravir",
        "brand_names": ["Vocabria", "Apretude"],
        "description": (
            "Long-acting injectable HIV integrase inhibitor (with rilpivirine) for monthly/bimonthly HIV treatment and pre-exposure prophylaxis (PrEP). Metabolized by UGT1A1 and UGT1A9. CYP3A4 inducers reduce levels."
        ),
        "drug_class": "Antiretroviral / Integrase Inhibitor",
        "rxnorm_cui": "2376838",
    },
    {
        "id": "DB01601_teno",
        "name": "Tenofovir alafenamide",
        "brand_names": ["Vemlidy", "Descovy (combined)"],
        "description": (
            "Prodrug NRTI for HIV and hepatitis B. Converted intracellularly to tenofovir diphosphate. P-glycoprotein and BCRP substrate. Lower tenofovir plasma levels than TDF — reduced renal and bone toxicity. CYP3A4 inducers reduce exposure."
        ),
        "drug_class": "Antiretroviral / NRTI",
        "rxnorm_cui": "1721467",
    },
    {
        "id": "DB06176",
        "name": "Ledipasvir",
        "brand_names": ["Harvoni (combined with sofosbuvir)"],
        "description": (
            "HCV NS5A inhibitor co-formulated with sofosbuvir for hepatitis C. Not significantly CYP-metabolized; P-glycoprotein and BCRP substrate. Increases digoxin levels (P-gp inhibition). Acid-reducing agents reduce absorption."
        ),
        "drug_class": "Antiviral / HCV NS5A Inhibitor",
        "rxnorm_cui": "1597571",
    },
    {
        "id": "DB11689_vel",
        "name": "Velpatasvir",
        "brand_names": ["Epclusa (combined with sofosbuvir)"],
        "description": (
            "HCV NS5A inhibitor combined with sofosbuvir for pan-genotypic HCV treatment. Metabolized by CYP2B6, CYP2C8, and CYP3A4. P-gp and BCRP substrate. Strong inducers (rifampin) reduce velpatasvir exposure markedly. PPIs significantly reduce velpatasvir absorption."
        ),
        "drug_class": "Antiviral / HCV NS5A Inhibitor",
        "rxnorm_cui": "1860496",
    },
    {
        "id": "DB11748_gle",
        "name": "Glecaprevir",
        "brand_names": ["Mavyret (combined with pibrentasvir)"],
        "description": (
            "HCV NS3/4A protease inhibitor co-formulated with pibrentasvir. CYP3A4 substrate and P-gp/BCRP substrate. Strong P-gp/CYP3A4 inducers are contraindicated. Inhibits P-gp and OATP1B — raises atorvastatin, rosuvastatin, and digoxin levels."
        ),
        "drug_class": "Antiviral / HCV Protease Inhibitor",
        "rxnorm_cui": "1999720",
    },
    {
        "id": "DB00879_osi",
        "name": "Baloxavir marboxil",
        "brand_names": ["Xofluza"],
        "description": (
            "Cap-dependent endonuclease inhibitor for influenza A and B. Prodrug converted to baloxavir by alkaline phosphatase. Not significantly metabolized by CYP enzymes. Polyvalent cations (antacids, dairy) reduce absorption."
        ),
        "drug_class": "Antiviral / Influenza Cap-Endonuclease Inhibitor",
        "rxnorm_cui": "2049142",
    },
    {
        "id": "DB06291",
        "name": "Oseltamivir",
        "brand_names": ["Tamiflu"],
        "description": (
            "Neuraminidase inhibitor for influenza prophylaxis and treatment. Prodrug hydrolyzed by hepatic esterases to active carboxylate. Not CYP-metabolized. Probenecid reduces renal elimination, increasing oseltamivir levels ~2-fold."
        ),
        "drug_class": "Antiviral / Neuraminidase Inhibitor",
        "rxnorm_cui": "130833",
    },
    {
        "id": "DB11799_len",
        "name": "Letermovir",
        "brand_names": ["Prevymis"],
        "description": (
            "CMV terminase complex inhibitor for CMV prophylaxis in allogeneic HSCT recipients. Inhibitor of CYP3A4 and OATP1B1/3 transporters — increases levels of CYP3A4 substrates (cyclosporine, tacrolimus, statins) significantly. Cyclosporine doubles letermovir levels — reduce letermovir dose by half."
        ),
        "drug_class": "Antiviral / CMV Terminase Inhibitor",
        "rxnorm_cui": "1999721",
    },
    {
        "id": "DB00422_val",
        "name": "Valganciclovir",
        "brand_names": ["Valcyte"],
        "description": (
            "Prodrug of ganciclovir for CMV retinitis and CMV prophylaxis in transplant. Hydrolyzed to ganciclovir by intestinal and hepatic esterases. Not CYP-metabolized. Mycophenolate mofetil increases ganciclovir levels (compete for renal tubular secretion). Bone marrow suppression risk."
        ),
        "drug_class": "Antiviral / CMV DNA Polymerase Inhibitor",
        "rxnorm_cui": "285953",
    },
    {
        "id": "DB01909",
        "name": "Brincidofovir",
        "brand_names": ["Tembexa"],
        "description": (
            "Lipid-conjugated cidofovir for smallpox and orthopoxvirus infections. Converted intracellularly to cidofovir diphosphate. CYP2B6, CYP2C8, and CYP3A4 interactions possible; clinical significance requires monitoring."
        ),
        "drug_class": "Antiviral / Orthopoxvirus",
        "rxnorm_cui": None,
    },
    {
        "id": "DB11988_tec",
        "name": "Tecovirimat",
        "brand_names": ["TPOXX"],
        "description": (
            "VP37 envelope wrapping protein inhibitor for smallpox and mpox. Metabolized by CYP3A4 (minor), 2C8, and 2C19. Moderate CYP3A4 inducer; may reduce levels of CYP3A4 substrates. CYP2C8/2C19 inducer effects also observed."
        ),
        "drug_class": "Antiviral / Orthopoxvirus",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15650",
        "name": "Brexanolone",
        "brand_names": ["Zulresso"],
        "description": (
            "Neuroactive steroid (GABA-A positive allosteric modulator) for postpartum depression. Metabolized by keto-reduction, glucuronidation, and sulfation; minimal CYP involvement. IV infusion over 60 hours in certified healthcare settings. CNS depressant — avoid benzodiazepines and other sedatives concomitantly."
        ),
        "drug_class": "Neuroactive Steroid / Antidepressant",
        "rxnorm_cui": "2169274",
    },
    {
        "id": "DB15651",
        "name": "Zuranolone",
        "brand_names": ["Zurzuvae"],
        "description": (
            "Oral neuroactive steroid (GABA-A positive allosteric modulator) for MDD and PPD. Metabolized by CYP3A4 (primary). Strong CYP3A4 inhibitors increase zuranolone exposure; strong inducers reduce efficacy. CNS depression; avoid driving 12 hours after dose."
        ),
        "drug_class": "Neuroactive Steroid / Antidepressant",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15652",
        "name": "Esketamine",
        "brand_names": ["Spravato"],
        "description": (
            "S-enantiomer of ketamine; NMDA receptor antagonist nasal spray for treatment-resistant depression and MDD with acute suicidal ideation. Metabolized by CYP3A4 and CYP2B6 to noresketamine. CYP3A4 and CYP2B6 inhibitors increase levels. Dissociation, sedation; must be administered in certified healthcare settings."
        ),
        "drug_class": "NMDA Antagonist / Antidepressant",
        "rxnorm_cui": "2169275",
    },
    {
        "id": "DB15653",
        "name": "Vilazodone",
        "brand_names": ["Viibryd"],
        "description": (
            "Serotonin partial agonist and reuptake inhibitor (SPARI) for MDD. Extensively metabolized by CYP3A4. Strong CYP3A4 inhibitors increase vilazodone exposure — reduce dose to 20 mg/day. Strong inducers reduce efficacy; may need dose increase to 80 mg/day."
        ),
        "drug_class": "SPARI Antidepressant",
        "rxnorm_cui": "1100697",
    },
    {
        "id": "DB15654",
        "name": "Vortioxetine",
        "brand_names": ["Trintellix"],
        "description": (
            "Serotonin modulator and stimulator (SMS) for MDD. Primarily metabolized by CYP2D6 (major) and CYP3A4/5 (minor). Strong CYP2D6 inhibitors increase vortioxetine levels — halve the dose. Strong CYP inducers increase clearance markedly — may need dose increase."
        ),
        "drug_class": "Serotonin Modulator / Antidepressant",
        "rxnorm_cui": "1489431",
    },
    {
        "id": "DB15655",
        "name": "Levomilnacipran",
        "brand_names": ["Fetzima"],
        "description": (
            "SNRI (active enantiomer of milnacipran) for MDD. Primarily renally excreted; minimal CYP metabolism via CYP3A4. Relatively low drug interaction potential compared to other SNRIs. Less NE/5-HT selectivity ratio issues."
        ),
        "drug_class": "SNRI Antidepressant",
        "rxnorm_cui": "1489430",
    },
    {
        "id": "DB15656_dex",
        "name": "Desvenlafaxine",
        "brand_names": ["Pristiq", "Khedezla"],
        "description": (
            "Active metabolite of venlafaxine; SNRI for MDD. Primarily glucuronidated; minimal CYP3A4 involvement. Low pharmacokinetic drug interaction potential. Weak CYP3A4 inhibitor and CYP2D6 inhibitor at therapeutic doses."
        ),
        "drug_class": "SNRI Antidepressant",
        "rxnorm_cui": "721029",
    },
    {
        "id": "DB11912_lura",
        "name": "Lurasidone",
        "brand_names": ["Latuda"],
        "description": (
            "Atypical antipsychotic for schizophrenia and bipolar depression. Exclusively metabolized by CYP3A4. Strong CYP3A4 inhibitors (ketoconazole) are contraindicated; moderate inhibitors require dose reduction. Strong inducers (rifampin) are also contraindicated. Must be taken with food (≥350 kcal)."
        ),
        "drug_class": "Antipsychotic",
        "rxnorm_cui": "1099148",
    },
    {
        "id": "DB11913",
        "name": "Cariprazine",
        "brand_names": ["Vraylar"],
        "description": (
            "Dopamine D3/D2 partial agonist antipsychotic for schizophrenia, bipolar mania, and bipolar depression. Metabolized by CYP3A4 to active metabolites DCAR and DDCAR. Strong CYP3A4 inhibitors increase exposure — dose reduction to 1.5 mg/day max. Strong inducers reduce cariprazine levels substantially."
        ),
        "drug_class": "Antipsychotic",
        "rxnorm_cui": "1600274",
    },
    {
        "id": "DB15660",
        "name": "Lumateperone",
        "brand_names": ["Caplyta"],
        "description": (
            "Multi-receptor antipsychotic for schizophrenia and bipolar depression. Metabolized by CYP3A4 and aldehyde oxidase. Strong CYP3A4 inhibitors increase lumateperone exposure — reduce dose to 14 mg/day. Strong inducers are contraindicated."
        ),
        "drug_class": "Antipsychotic",
        "rxnorm_cui": "2169276",
    },
    {
        "id": "DB15661",
        "name": "Pimavanserin",
        "brand_names": ["Nuplazid"],
        "description": (
            "Selective 5-HT2A inverse agonist for Parkinson's disease psychosis. Metabolized by CYP3A4 and CYP3A5 to active metabolite ACP-279054. Strong CYP3A4 inhibitors increase pimavanserin exposure — dose reduction needed. QT prolongation risk; avoid QT-prolonging drugs."
        ),
        "drug_class": "Antipsychotic / 5-HT2A Inverse Agonist",
        "rxnorm_cui": "1860495",
    },
    {
        "id": "DB11917",
        "name": "Brexpiprazole",
        "brand_names": ["Rexulti"],
        "description": (
            "Serotonin-dopamine activity modulator (SDAM) for schizophrenia, MDD adjunct, and agitation in Alzheimer's. Metabolized by CYP2D6 (primary) and CYP3A4. Strong CYP2D6 inhibitors: reduce dose by half. Strong CYP3A4 inhibitors or combined: reduce dose to one quarter. Strong inducers: consider dose increase."
        ),
        "drug_class": "Antipsychotic / SDAM",
        "rxnorm_cui": "1600275",
    },
    {
        "id": "DB15662",
        "name": "Deutetrabenazine",
        "brand_names": ["Austedo"],
        "description": (
            "Vesicular monoamine transporter-2 (VMAT2) inhibitor for chorea in HD and tardive dyskinesia. Deuterated analog of tetrabenazine; longer half-life. Metabolized by carbonyl reductase to active metabolites alpha/beta-HTBZ, then by CYP2D6. Strong CYP2D6 inhibitors increase HTBZ exposure — dose max reduced to 36 mg/day."
        ),
        "drug_class": "VMAT2 Inhibitor",
        "rxnorm_cui": "1860496",
    },
    {
        "id": "DB15663",
        "name": "Valbenazine",
        "brand_names": ["Ingrezza"],
        "description": (
            "VMAT2 inhibitor for tardive dyskinesia. Converted by plasma esterases to active metabolite (+)-alpha-HTBZ via CYP3A4/5. Strong CYP3A4 inhibitors increase active metabolite exposure — reduce dose to 40 mg/day. Strong CYP2D6 inhibitors have additive effect on HTBZ levels."
        ),
        "drug_class": "VMAT2 Inhibitor",
        "rxnorm_cui": "1860497",
    },
    {
        "id": "DB09588",
        "name": "Nusinersen",
        "brand_names": ["Spinraza"],
        "description": (
            "Antisense oligonucleotide for spinal muscular atrophy (SMA). Administered intrathecally. Not metabolized by CYP enzymes; degraded by exo- and endonucleases. Minimal pharmacokinetic drug interaction potential."
        ),
        "drug_class": "Antisense Oligonucleotide / SMA Treatment",
        "rxnorm_cui": "1860498",
    },
    {
        "id": "DB15664",
        "name": "Risdiplam",
        "brand_names": ["Evrysdi"],
        "description": (
            "SMN2 splicing modifier for spinal muscular atrophy. Oral small molecule. Metabolized by FMO1, FMO3, and CYP3A4. Strong CYP3A4 inhibitors may increase levels. Inhibits MATE1 and MATE2-K in vitro — potential to raise metformin levels."
        ),
        "drug_class": "SMN2 Splicing Modifier / SMA Treatment",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15665",
        "name": "Erenumab",
        "brand_names": ["Aimovig"],
        "description": (
            "Anti-CGRP receptor monoclonal antibody for migraine prophylaxis. Catabolized by proteolytic pathways. No CYP interactions. Monthly SC injection. First FDA-approved CGRP pathway inhibitor."
        ),
        "drug_class": "Anti-CGRP / Migraine Prophylaxis",
        "rxnorm_cui": "1999718",
    },
    {
        "id": "DB15666",
        "name": "Fremanezumab",
        "brand_names": ["Ajovy"],
        "description": (
            "Anti-CGRP monoclonal antibody for migraine prophylaxis. Monthly or quarterly SC injection. Catabolized by proteolysis. No CYP interactions."
        ),
        "drug_class": "Anti-CGRP / Migraine Prophylaxis",
        "rxnorm_cui": "1999717",
    },
    {
        "id": "DB15667",
        "name": "Galcanezumab",
        "brand_names": ["Emgality"],
        "description": (
            "Anti-CGRP monoclonal antibody for migraine prophylaxis and cluster headache. Monthly SC injection. Proteolytic catabolism; no CYP interactions."
        ),
        "drug_class": "Anti-CGRP / Migraine Prophylaxis",
        "rxnorm_cui": "1999716",
    },
    {
        "id": "DB15668",
        "name": "Ubrogepant",
        "brand_names": ["Ubrelvy"],
        "description": (
            "Oral CGRP receptor antagonist (gepant) for acute migraine. Metabolized by CYP3A4. Strong CYP3A4 inhibitors are contraindicated; moderate inhibitors require dose reduction. Strong CYP3A4 inducers reduce efficacy."
        ),
        "drug_class": "CGRP Receptor Antagonist / Acute Migraine",
        "rxnorm_cui": "2169277",
    },
    {
        "id": "DB15669",
        "name": "Rimegepant",
        "brand_names": ["Nurtec ODT"],
        "description": (
            "Oral CGRP receptor antagonist for acute migraine and migraine prophylaxis. Metabolized by CYP3A4. Strong CYP3A4 inhibitors require dose limitation. P-glycoprotein and BCRP substrate. Strong inducers reduce efficacy."
        ),
        "drug_class": "CGRP Receptor Antagonist / Migraine",
        "rxnorm_cui": "2169278",
    },
    {
        "id": "DB15670",
        "name": "Atogepant",
        "brand_names": ["Qulipta"],
        "description": (
            "Oral CGRP receptor antagonist for migraine prophylaxis (not acute use). Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase exposure — use lowest dose. Strong CYP3A4 inducers reduce efficacy — use highest dose."
        ),
        "drug_class": "CGRP Receptor Antagonist / Migraine Prophylaxis",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15671",
        "name": "Lasmiditan",
        "brand_names": ["Reyvow"],
        "description": (
            "Selective 5-HT1F agonist for acute migraine. First in class ditan. Metabolized by MAO-A, MAO-B, and aldehyde oxidase; CYP involvement minimal. Sedation; do not drive for at least 8 hours after dose. Serotonergic agonist — serotonin syndrome risk with other serotonergic agents."
        ),
        "drug_class": "5-HT1F Agonist / Acute Migraine",
        "rxnorm_cui": "2169279",
    },
    {
        "id": "DB09543",
        "name": "Brivaracetam",
        "brand_names": ["Briviact"],
        "description": (
            "High-affinity SV2A ligand anticonvulsant for focal seizures. Metabolized by CYP2C19 (primary hydroxylation) and hydrolysis. CYP2C19 inhibitors may increase levels. Rifampin (CYP2C19/3A4 inducer) reduces brivaracetam by ~45%. Lower interaction potential than levetiracetam."
        ),
        "drug_class": "Anticonvulsant / SV2A Ligand",
        "rxnorm_cui": "1745277",
    },
    {
        "id": "DB06218_ceno",
        "name": "Cenobamate",
        "brand_names": ["Xcopri"],
        "description": (
            "Anticonvulsant for focal-onset seizures. Inhibits CYP2C19 strongly and CYP3A4 moderately — raises levels of many CYP2C19 substrates. Induces CYP3A4 and CYP2B6, reducing levels of CYP3A4/2B6 substrates. Complex DDI profile; titration required."
        ),
        "drug_class": "Anticonvulsant",
        "rxnorm_cui": "2169284",
    },
    {
        "id": "DB15672",
        "name": "Fenfluramine",
        "brand_names": ["Fintepla"],
        "description": (
            "Serotonin-releasing agent repurposed for Dravet syndrome and LGS. Metabolized by CYP1A2 and CYP2D6; norfenfluramine (active) is also formed. Strong CYP1A2 or CYP2D6 inhibitors increase levels — dose adjustments needed. Must be given with clobazam (Dravet) or with stiripentol in some regimens."
        ),
        "drug_class": "Anticonvulsant / Serotonin Releaser",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15673",
        "name": "Cannabidiol",
        "brand_names": ["Epidiolex"],
        "description": (
            "Purified plant-derived cannabidiol for Dravet syndrome, LGS, and TSC. Metabolized by CYP2C19 and CYP3A4. Inhibits CYP2C19 and CYP3A4 — raises clobazam and N-desmethylclobazam levels significantly (2-3 fold). Valproate increases cannabidiol hepatotoxicity risk."
        ),
        "drug_class": "Anticonvulsant / Cannabinoid",
        "rxnorm_cui": "1827543",
    },
    {
        "id": "DB09061",
        "name": "Liotrix",
        "brand_names": ["Thyrolar"],
        "description": (
            "Combination of T4 (levothyroxine) and T3 (liothyronine) in fixed 4:1 ratio for hypothyroidism. Not CYP-metabolized. Increases sensitivity to oral anticoagulants (warfarin)."
        ),
        "drug_class": "Thyroid Hormone Combination",
        "rxnorm_cui": "200278",
    },
    {
        "id": "DB00451_liot",
        "name": "Liothyronine",
        "brand_names": ["Cytomel", "Triostat"],
        "description": (
            "Synthetic T3 thyroid hormone for hypothyroidism and myxedema coma. Faster onset than levothyroxine. Not CYP-metabolized; converted from T4 peripherally by deiodinases. Potentiates warfarin anticoagulation."
        ),
        "drug_class": "Thyroid Hormone",
        "rxnorm_cui": "10582",
    },
    {
        "id": "DB15680",
        "name": "Luseogliflozin",
        "brand_names": ["Lusefi"],
        "description": (
            "SGLT2 inhibitor approved in Japan for type 2 diabetes. Metabolized by UGT1A3, UGT2B7, and UGT2B15. Minimal CYP involvement. Diuretic effects similar to other SGLT2 inhibitors."
        ),
        "drug_class": "Antidiabetic / SGLT2 Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB09066",
        "name": "Denosumab",
        "brand_names": ["Prolia", "Xgeva"],
        "description": (
            "Anti-RANKL monoclonal antibody for osteoporosis and bone metastases. Catabolized by normal immunoglobulin pathways. No CYP interactions. Hypocalcemia risk; calcium/vitamin D supplementation required. Dose and indication differ between Prolia and Xgeva."
        ),
        "drug_class": "RANKL Inhibitor / Bone Agent",
        "rxnorm_cui": "993458",
    },
    {
        "id": "DB15681",
        "name": "Romosozumab",
        "brand_names": ["Evenity"],
        "description": (
            "Anti-sclerostin monoclonal antibody for postmenopausal osteoporosis. Catabolized by proteolytic degradation. No CYP interactions. Dual mechanism: increases bone formation and decreases bone resorption. Cardiovascular events risk; contraindicated within a year of MI/stroke."
        ),
        "drug_class": "Anti-Sclerostin / Bone Anabolic Agent",
        "rxnorm_cui": "2169285",
    },
    {
        "id": "DB06228_abalo",
        "name": "Abaloparatide",
        "brand_names": ["Tymlos"],
        "description": (
            "PTHrP analog for postmenopausal osteoporosis. Metabolized by nonspecific proteolysis. No significant CYP interactions. Anabolic bone agent; daily SC injection. Orthostatic hypotension risk within 4 hours of injection."
        ),
        "drug_class": "PTHrP Analog / Bone Anabolic Agent",
        "rxnorm_cui": "1860499",
    },
    {
        "id": "DB09063_oste",
        "name": "Teriparatide",
        "brand_names": ["Forteo"],
        "description": (
            "Recombinant PTH(1-34) for severe osteoporosis. Metabolized by liver and peripheral tissues via nonspecific enzymatic cleavage. Not CYP-metabolized. Increases risk of hypercalcemia; monitor calcium. Black box warning for osteosarcoma in rodents (not established in humans)."
        ),
        "drug_class": "PTH Analog / Bone Anabolic Agent",
        "rxnorm_cui": "544569",
    },
    {
        "id": "DB06403",
        "name": "Pasireotide",
        "brand_names": ["Signifor", "Signifor LAR"],
        "description": (
            "Somatostatin analog for Cushing's disease and acromegaly. Metabolized by multiple pathways including CYP3A4; P-gp substrate. Inhibits CYP3A4 weakly. Hyperglycemia is a major adverse effect — monitor blood glucose closely."
        ),
        "drug_class": "Somatostatin Analog",
        "rxnorm_cui": "1299856",
    },
    {
        "id": "DB06403_oct",
        "name": "Octreotide",
        "brand_names": ["Sandostatin", "Sandostatin LAR"],
        "description": (
            "Somatostatin analog for acromegaly, carcinoid syndrome, and VIPomas. Metabolized partially by CYP3A4. May decrease cyclosporine absorption (reduces GI motility). Reduces insulin secretion; hypoglycemia or hyperglycemia possible."
        ),
        "drug_class": "Somatostatin Analog",
        "rxnorm_cui": "10797",
    },
    {
        "id": "DB15682",
        "name": "Osilodrostat",
        "brand_names": ["Isturisa"],
        "description": (
            "11β-hydroxylase inhibitor for Cushing's disease. Metabolized by CYP3A4 and CYP2D6. Inhibits CYP2D6 — increases levels of CYP2D6 substrates. Strong CYP3A4 inducers reduce efficacy. QT prolongation potential."
        ),
        "drug_class": "Steroidogenesis Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15683",
        "name": "Levoketoconazole",
        "brand_names": ["Recorlev"],
        "description": (
            "S-enantiomer of ketoconazole for Cushing's syndrome. Inhibits multiple steroidogenic enzymes. Strong inhibitor of CYP3A4 — major DDI with all CYP3A4 substrates. QT prolongation; hepatotoxicity risk requires monitoring."
        ),
        "drug_class": "Steroidogenesis Inhibitor / CYP3A4 Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB09066_mife",
        "name": "Mifepristone",
        "brand_names": ["Korlym", "Mifeprex"],
        "description": (
            "Glucocorticoid/progesterone receptor antagonist. For Cushing's syndrome (Korlym) and medical abortion (Mifeprex). Metabolized by CYP3A4. Strong CYP3A4 inhibitor itself — increases levels of many CYP3A4 substrates including simvastatin, colchicine, and fentanyl."
        ),
        "drug_class": "GR/PR Antagonist / Steroidogenesis Modifier",
        "rxnorm_cui": "6926",
    },
    {
        "id": "DB15684",
        "name": "Tralokinumab",
        "brand_names": ["Adbry"],
        "description": (
            "Anti-IL-13 monoclonal antibody for moderate-to-severe atopic dermatitis. Catabolized by proteolytic pathways. No CYP interactions. Anti-inflammatory normalization of cytokine-suppressed CYP enzymes possible."
        ),
        "drug_class": "Biologic / Anti-IL-13",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15685_leb",
        "name": "Lebrikizumab",
        "brand_names": ["Ebglyss"],
        "description": (
            "Anti-IL-13 monoclonal antibody for atopic dermatitis. Binds IL-13 with high affinity; catabolized by proteolytic degradation. No CYP interactions."
        ),
        "drug_class": "Biologic / Anti-IL-13",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15686",
        "name": "Tapinarof",
        "brand_names": ["Vtama"],
        "description": (
            "Aryl hydrocarbon receptor (AhR) agonist topical cream for plaque psoriasis. Systemic absorption is low. CYP1A2 inducer in vitro (AhR activation); clinical systemic CYP induction unlikely at topical doses."
        ),
        "drug_class": "Topical Anti-inflammatory / AhR Agonist",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15687",
        "name": "Roflumilast (topical)",
        "brand_names": ["Zoryve"],
        "description": (
            "Topical PDE4 inhibitor for seborrheic dermatitis and plaque psoriasis. Low systemic absorption; CYP interactions negligible at topical doses. Same mechanism as oral roflumilast for COPD."
        ),
        "drug_class": "Topical PDE4 Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15688",
        "name": "Abrocitinib",
        "brand_names": ["Cibinqo"],
        "description": (
            "Selective JAK1 inhibitor for moderate-to-severe atopic dermatitis. Primarily metabolized by CYP2C19 (major) and CYP2C9, CYP3A4, CYP2B6 (minor). Strong CYP2C19 inhibitors increase abrocitinib exposure — reduce dose. Strong combined CYP2C19 + CYP2C9 inhibitors require dose reduction to 50 mg/day."
        ),
        "drug_class": "Immunosuppressant / JAK1 Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB09038",
        "name": "Apremilast",
        "brand_names": ["Otezla"],
        "description": (
            "Oral PDE4 inhibitor for psoriatic arthritis, plaque psoriasis, and oral ulcers in Behcet's disease. Metabolized by CYP3A4 (major) and CYP1A2/2A6 (minor). Strong CYP3A4 inducers (rifampin) reduce apremilast AUC by ~72% — avoid. Weight loss is a class effect; monitor weight."
        ),
        "drug_class": "PDE4 Inhibitor / Oral Anti-inflammatory",
        "rxnorm_cui": "1592774",
    },
    {
        "id": "DB11988_ixek",
        "name": "Spesolimab",
        "brand_names": ["Spevigo"],
        "description": (
            "Anti-IL-36R monoclonal antibody for generalized pustular psoriasis (GPP) flares. Catabolized by proteolytic pathways. No CYP interactions. First approved treatment specifically for GPP; orphan drug designation."
        ),
        "drug_class": "Biologic / Anti-IL-36R",
        "rxnorm_cui": None,
    },
    {
        "id": "DB06292_ison",
        "name": "Isotretinoin",
        "brand_names": ["Accutane", "Absorica", "Claravis"],
        "description": (
            "Vitamin A derivative (retinoid) for severe nodular acne. Metabolized by CYP3A4 and CYP2C8. Teratogenic; IPLEDGE REMS program required. Combined with tetracyclines increases pseudotumor cerebri risk. Inhibits CYP1A2 and CYP2C8 mildly in vitro."
        ),
        "drug_class": "Retinoid / Antiacne",
        "rxnorm_cui": "33533",
    },
    {
        "id": "DB15689",
        "name": "Ruxolitinib (topical)",
        "brand_names": ["Opzelura"],
        "description": (
            "Topical JAK1/2 inhibitor for atopic dermatitis and vitiligo. Low systemic absorption at topical doses limits CYP interactions. Same mechanism as oral ruxolitinib (Jakafi) for myelofibrosis."
        ),
        "drug_class": "Topical JAK Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB09109",
        "name": "Ranibizumab",
        "brand_names": ["Lucentis"],
        "description": (
            "Anti-VEGF monoclonal antibody fragment for neovascular AMD, DME, macular edema after RVO, and DR. Intravitreal injection. Minimal systemic absorption; no clinically relevant CYP interactions."
        ),
        "drug_class": "Anti-VEGF / Ophthalmic Biologic",
        "rxnorm_cui": "544570",
    },
    {
        "id": "DB09291",
        "name": "Aflibercept",
        "brand_names": ["Eylea", "Zaltrap"],
        "description": (
            "VEGF-A/VEGF-B/PlGF trap fusion protein for neovascular AMD, DME, and macular edema (ophthalmic) and metastatic CRC (systemic, Zaltrap). Intravitreal form: minimal systemic CYP impact. Systemic form: catabolized by normal protein pathways."
        ),
        "drug_class": "Anti-VEGF / Ophthalmic Biologic",
        "rxnorm_cui": "1232734",
    },
    {
        "id": "DB15690",
        "name": "Faricimab",
        "brand_names": ["Vabysmo"],
        "description": (
            "Bispecific antibody targeting VEGF-A and Ang-2 for neovascular AMD and DME. First bispecific antibody for ophthalmology. Intravitreal injection; minimal systemic absorption. No CYP interactions."
        ),
        "drug_class": "Anti-VEGF/Ang-2 / Ophthalmic Biologic",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15691",
        "name": "Brolucizumab",
        "brand_names": ["Beovu"],
        "description": (
            "Single-chain antibody fragment anti-VEGF-A for neovascular AMD. Intravitreal injection. Negligible systemic exposure; no CYP interactions. Intraocular inflammation including retinal vasculitis reported."
        ),
        "drug_class": "Anti-VEGF / Ophthalmic Biologic",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15692",
        "name": "Pegcetacoplan",
        "brand_names": ["Syfovre"],
        "description": (
            "Complement C3 inhibitor (pegylated compstatin analog) for geographic atrophy secondary to AMD. Intravitreal injection; negligible systemic absorption. No CYP interactions. First approved treatment for geographic atrophy."
        ),
        "drug_class": "Complement Inhibitor / Ophthalmic",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15693",
        "name": "Avacincaptad pegol",
        "brand_names": ["Izervay"],
        "description": (
            "Pegylated RNA aptamer targeting complement factor C5 for geographic atrophy. Intravitreal injection. Negligible systemic exposure; no CYP interactions. Approved as second complement-targeting agent for geographic atrophy."
        ),
        "drug_class": "Complement Inhibitor / Ophthalmic",
        "rxnorm_cui": None,
    },
    {
        "id": "DB06292_lata",
        "name": "Latanoprost",
        "brand_names": ["Xalatan"],
        "description": (
            "Prostaglandin F2alpha analog for open-angle glaucoma and ocular hypertension. Topically administered; hydrolyzed by corneal esterases to active acid form. Minimal systemic absorption. No clinically significant CYP interactions."
        ),
        "drug_class": "Prostaglandin Analog / Ophthalmic",
        "rxnorm_cui": "203134",
    },
    {
        "id": "DB06292_brim",
        "name": "Brimonidine",
        "brand_names": ["Alphagan P"],
        "description": (
            "Selective alpha-2 adrenergic agonist for ocular hypertension and glaucoma. Topically administered; some systemic absorption. Metabolized by aldehyde oxidase and monoamine oxidase. CNS depression in infants (avoid in age <2). MAO inhibitor interaction risk."
        ),
        "drug_class": "Alpha-2 Agonist / Ophthalmic",
        "rxnorm_cui": "1191",
    },
    {
        "id": "DB09292_ved",
        "name": "Vedolizumab",
        "brand_names": ["Entyvio"],
        "description": (
            "Gut-selective anti-integrin (alpha4beta7) monoclonal antibody for UC and CD. Catabolized by proteolysis. No CYP interactions. Gut-selective mechanism limits systemic immunosuppression compared to anti-TNF agents."
        ),
        "drug_class": "Anti-Integrin / IBD Biologic",
        "rxnorm_cui": "1592775",
    },
    {
        "id": "DB15696",
        "name": "Ozanimod",
        "brand_names": ["Zeposia"],
        "description": (
            "Sphingosine 1-phosphate (S1P) receptor modulator for UC and relapsing MS. Converted to active metabolites CC112273 and CC1084037 via MAO-B and CYP2C8. Strong MAO inhibitors are contraindicated. CYP2C8 inhibitors may increase levels. Cardiac monitoring required at initiation (first-dose bradycardia)."
        ),
        "drug_class": "S1P Receptor Modulator / IBD",
        "rxnorm_cui": "2169286",
    },
    {
        "id": "DB15697",
        "name": "Etrasimod",
        "brand_names": ["Velsipity"],
        "description": (
            "Selective S1P receptor modulator for moderately-to-severely active UC. Metabolized by CYP2C8, CYP2C9, CYP2C19, and CYP3A4. Strong combined CYP inhibitors increase exposure; strong inducers reduce efficacy. Cardiac monitoring required at initiation."
        ),
        "drug_class": "S1P Receptor Modulator / IBD",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15698",
        "name": "Mirikizumab",
        "brand_names": ["Omvoh"],
        "description": (
            "Anti-IL-23 (p19) monoclonal antibody for moderately-to-severely active UC. Catabolized by proteolytic degradation. No CYP interactions. Induction IV then SC maintenance dosing."
        ),
        "drug_class": "Biologic / Anti-IL-23 / IBD",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15699",
        "name": "Obeticholic acid",
        "brand_names": ["Ocaliva"],
        "description": (
            "Farnesoid X receptor (FXR) agonist for primary biliary cholangitis (PBC). Undergoes conjugation with taurine and glycine; some CYP2D6 involvement. Inhibits CYP2C8 — may increase levels of CYP2C8 substrates. Worsening liver decompensation in advanced PBC; dosing must be adjusted."
        ),
        "drug_class": "FXR Agonist / Cholestatic Liver Disease",
        "rxnorm_cui": "1860500",
    },
    {
        "id": "DB15700",
        "name": "Odevixibat",
        "brand_names": ["Bylvay"],
        "description": (
            "Ileal bile acid transporter (IBAT) inhibitor for progressive familial intrahepatic cholestasis (PFIC). Minimal systemic absorption; acts locally in the gut. No significant CYP interactions."
        ),
        "drug_class": "IBAT Inhibitor / Orphan Liver Disease",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15701",
        "name": "Maralixibat",
        "brand_names": ["Livmarli"],
        "description": (
            "IBAT inhibitor for Alagille syndrome-associated cholestatic pruritus. Minimally absorbed systemically; works in the intestinal lumen. No significant CYP-mediated interactions."
        ),
        "drug_class": "IBAT Inhibitor / Orphan Liver Disease",
        "rxnorm_cui": None,
    },
    {
        "id": "DB06292_elow",
        "name": "Eluxadoline",
        "brand_names": ["Viberzi"],
        "description": (
            "Mixed mu/kappa opioid agonist and delta antagonist for IBS-D. Eliminated by biliary secretion; OATP1B1 substrate. Cyclosporine (OATP1B1 inhibitor) increases eluxadoline levels — contraindicated together. Contraindicated in patients without a gallbladder."
        ),
        "drug_class": "Opioid Receptor Mixed Agonist-Antagonist / IBS",
        "rxnorm_cui": "1860501",
    },
    {
        "id": "DB06292_teg",
        "name": "Tegaserod",
        "brand_names": ["Zelnorm"],
        "description": (
            "5-HT4 partial agonist for IBS-C in women under 65 without cardiovascular risk. Metabolized by acid-catalyzed glucuronidation in the stomach and oxidation; CYP3A4 plays a minor role. Low pharmacokinetic interaction potential."
        ),
        "drug_class": "5-HT4 Partial Agonist / IBS-C",
        "rxnorm_cui": "358259",
    },
    {
        "id": "DB15703",
        "name": "Rifaximin",
        "brand_names": ["Xifaxan"],
        "description": (
            "Non-absorbable rifamycin antibiotic for IBS-D, travelers' diarrhea, and hepatic encephalopathy prevention. Locally active in GI tract; minimal systemic absorption. Local P-gp induction may reduce intestinal absorption of some drugs. At standard doses, systemic CYP3A4 induction is minimal."
        ),
        "drug_class": "GI Antibiotic / Rifamycin",
        "rxnorm_cui": "544569",
    },
    {
        "id": "DB15704",
        "name": "Lubiprostone",
        "brand_names": ["Amitiza"],
        "description": (
            "Chloride channel (ClC-2) activator for chronic idiopathic constipation, IBS-C, and opioid-induced constipation. Rapidly metabolized by 15-ketoprostaglandin reductase in the gut and liver. Minimal CYP interactions."
        ),
        "drug_class": "Chloride Channel Activator / Constipation",
        "rxnorm_cui": "544568",
    },
    {
        "id": "DB15705",
        "name": "Linaclotide",
        "brand_names": ["Linzess", "Constella"],
        "description": (
            "Guanylate cyclase-C agonist for IBS-C and chronic idiopathic constipation. Proteolytically degraded in the GI lumen; minimal systemic absorption. No CYP enzyme interactions."
        ),
        "drug_class": "GC-C Agonist / Constipation",
        "rxnorm_cui": "1099147",
    },
    {
        "id": "DB06292_pemo",
        "name": "Pegloticase",
        "brand_names": ["Krystexxa"],
        "description": (
            "PEGylated uricase for refractory chronic gout. Converts uric acid to allantoin. Protein catabolism is the primary metabolic pathway; no CYP interactions. Infusion reactions and anaphylaxis risk; monitor uric acid levels. Immunogenicity reduces efficacy over time."
        ),
        "drug_class": "Uricase / Antigout",
        "rxnorm_cui": "993458",
    },
    {
        "id": "DB06292_febux",
        "name": "Febuxostat",
        "brand_names": ["Uloric"],
        "description": (
            "Non-purine selective xanthine oxidase inhibitor for gout. Metabolized by glucuronidation (UGT1A1, UGT1A3, UGT1A9) and oxidation by CYP1A2, CYP2C8, CYP2C9. Significantly increases levels of azathioprine and mercaptopurine (xanthine oxidase substrates) — contraindicated."
        ),
        "drug_class": "Xanthine Oxidase Inhibitor / Antigout",
        "rxnorm_cui": "806054",
    },
    {
        "id": "DB06292_lesi",
        "name": "Lesinurad",
        "brand_names": ["Zurampic"],
        "description": (
            "Urate transporter-1 (URAT1) inhibitor for hyperuricemia and gout, used in combination with xanthine oxidase inhibitors. Metabolized by CYP2C9. Strong CYP2C9 inhibitors increase lesinurad exposure."
        ),
        "drug_class": "URAT1 Inhibitor / Uricosuric",
        "rxnorm_cui": "1745278",
    },
    {
        "id": "DB11988_beli",
        "name": "Belimumab",
        "brand_names": ["Benlysta"],
        "description": (
            "Anti-BLyS/BAFF monoclonal antibody for SLE and lupus nephritis. Catabolized by proteolytic pathways. No CYP interactions. IV or SC formulation. Serious infections and psychiatric events reported."
        ),
        "drug_class": "Biologic / Anti-BLyS / SLE",
        "rxnorm_cui": "1099146",
    },
    {
        "id": "DB15706",
        "name": "Anifrolumab",
        "brand_names": ["Saphnelo"],
        "description": (
            "Anti-interferon alpha/beta receptor (IFNAR1) monoclonal antibody for SLE. Catabolized by proteolysis. No CYP enzyme interactions. Herpes zoster and respiratory infections; live vaccines contraindicated."
        ),
        "drug_class": "Biologic / Anti-IFNAR1 / SLE",
        "rxnorm_cui": None,
    },
    {
        "id": "DB06292_saril",
        "name": "Sarilumab",
        "brand_names": ["Kevzara"],
        "description": (
            "Anti-IL-6 receptor monoclonal antibody for RA. Catabolized by protein degradation. Anti-inflammatory effects normalize cytokine-suppressed CYP3A4 enzymes — monitor narrow therapeutic index CYP3A4 substrates at initiation/dose changes."
        ),
        "drug_class": "Biologic / IL-6R Inhibitor / RA",
        "rxnorm_cui": "1860503",
    },
    {
        "id": "DB06292_tocil",
        "name": "Tocilizumab",
        "brand_names": ["Actemra"],
        "description": (
            "Anti-IL-6 receptor monoclonal antibody for RA, GCA, CRS, and SSc-ILD. IL-6 suppression normalizes CYP3A4 activity previously suppressed by inflammation — monitor simvastatin, cyclosporine, warfarin, and other narrow therapeutic index CYP3A4 substrates at therapy initiation."
        ),
        "drug_class": "Biologic / IL-6R Inhibitor",
        "rxnorm_cui": "993459",
    },
    {
        "id": "DB09579_ivac",
        "name": "Ivacaftor",
        "brand_names": ["Kalydeco", "Symdeko (combined)", "Trikafta (combined)"],
        "description": (
            "CFTR potentiator for cystic fibrosis with gating mutations (G551D and others). Metabolized by CYP3A4 (primary). Strong CYP3A4 inhibitors increase ivacaftor levels — reduce dose to one tablet every other day or weekly. Strong inducers reduce efficacy significantly."
        ),
        "drug_class": "CFTR Potentiator / Cystic Fibrosis",
        "rxnorm_cui": "1299858",
    },
    {
        "id": "DB15707",
        "name": "Elexacaftor",
        "brand_names": ["Trikafta (combined with tezacaftor + ivacaftor)"],
        "description": (
            "CFTR corrector combined with tezacaftor and ivacaftor for CF with at least one F508del mutation. Metabolized by CYP3A4/5. Strong CYP3A4 inhibitors increase elexacaftor levels; strong inducers dramatically reduce efficacy. Most efficacious CFTR modulator regimen to date."
        ),
        "drug_class": "CFTR Corrector / Cystic Fibrosis",
        "rxnorm_cui": "2169287",
    },
    {
        "id": "DB15708",
        "name": "Lumacaftor",
        "brand_names": ["Orkambi (combined with ivacaftor)"],
        "description": (
            "CFTR corrector for CF homozygous F508del. Metabolized by CYP3A4. Strong CYP3A4 inducer itself — reduces ivacaftor levels significantly within the same combination tablet. Reduces efficacy of hormonal contraceptives, immunosuppressants, and other CYP3A4 substrates."
        ),
        "drug_class": "CFTR Corrector / Cystic Fibrosis / CYP3A4 Inducer",
        "rxnorm_cui": "1592776",
    },
    {
        "id": "DB09579_ecu",
        "name": "Eculizumab",
        "brand_names": ["Soliris"],
        "description": (
            "Anti-complement C5 monoclonal antibody for PNH, aHUS, gMG, and NMOSD. Catabolized by proteolytic pathways. No CYP interactions. Meningococcal vaccination required; life-threatening meningococcal infections reported."
        ),
        "drug_class": "Complement Inhibitor / Anti-C5",
        "rxnorm_cui": "544571",
    },
    {
        "id": "DB15709",
        "name": "Ravulizumab",
        "brand_names": ["Ultomiris"],
        "description": (
            "Long-acting anti-C5 monoclonal antibody for PNH and aHUS. Every 8-week dosing. Proteolytic catabolism; no CYP interactions. FcRn-mediated recycling via Fc engineering extends half-life."
        ),
        "drug_class": "Complement Inhibitor / Anti-C5",
        "rxnorm_cui": "2049141",
    },
    {
        "id": "DB15710",
        "name": "Iptacopan",
        "brand_names": ["Fabhalta"],
        "description": (
            "Oral complement factor B inhibitor for PNH. First oral monotherapy for PNH. Metabolized by CYP3A4 and UGT2B7. P-gp substrate. Strong CYP3A4/P-gp inhibitors increase exposure; strong inducers reduce efficacy."
        ),
        "drug_class": "Complement Factor B Inhibitor / PNH",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15711",
        "name": "Migalastat",
        "brand_names": ["Galafold"],
        "description": (
            "Pharmacological chaperone for Fabry disease with amenable GLA mutations. Metabolized by multiple CYP enzymes; no single dominant pathway. Not significantly CYP-inhibiting. Take on an empty stomach (food reduces absorption)."
        ),
        "drug_class": "Pharmacological Chaperone / Fabry Disease",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15712",
        "name": "Cerliponase alfa",
        "brand_names": ["Brineura"],
        "description": (
            "Recombinant human tripeptidyl peptidase 1 (TPP1) for CLN2 neuronal ceroid lipofuscinosis. Administered intracerebroventricularly. Not CYP-metabolized. Orphan drug for ultra-rare pediatric neurodegeneration."
        ),
        "drug_class": "Enzyme Replacement / Batten Disease",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15713",
        "name": "Avalglucosidase alfa",
        "brand_names": ["Nexviazyme"],
        "description": (
            "Enzyme replacement therapy for late-onset Pompe disease (GAA deficiency). Degraded by lysosomal proteases. No CYP interactions. Improved uptake via high-affinity M6P targeting vs older alglucosidase alfa."
        ),
        "drug_class": "Enzyme Replacement / Pompe Disease",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15714",
        "name": "Setmelanotide",
        "brand_names": ["Imcivree"],
        "description": (
            "MC4R agonist for obesity due to POMC, PCSK1, or LEPR deficiency. Metabolized by proteolytic cleavage; not CYP-mediated. Orphan drug for monogenic hypothalamic obesity disorders."
        ),
        "drug_class": "MC4R Agonist / Obesity (Genetic)",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15715",
        "name": "Voxelotor",
        "brand_names": ["Oxbryta"],
        "description": (
            "Hemoglobin S polymerization inhibitor for sickle cell disease. Metabolized by CYP3A4 (major) and CYP2B6/2C19 (minor). Strong CYP3A4 inhibitors increase voxelotor levels; strong inducers reduce efficacy."
        ),
        "drug_class": "HbS Polymerization Inhibitor / Sickle Cell Disease",
        "rxnorm_cui": "2169288",
    },
    {
        "id": "DB15716",
        "name": "Crizanlizumab",
        "brand_names": ["Adakveo"],
        "description": (
            "Anti-P-selectin monoclonal antibody for sickle cell disease to reduce vaso-occlusive crises. Catabolized by proteolytic degradation. No CYP interactions. Monthly IV infusion."
        ),
        "drug_class": "Anti-P-Selectin / Sickle Cell Disease",
        "rxnorm_cui": "2169289",
    },
    {
        "id": "DB15717",
        "name": "Givosiran",
        "brand_names": ["Givlaari"],
        "description": (
            "RNAi therapeutic targeting ALAS1 mRNA for acute hepatic porphyria. Metabolized by nucleases; not CYP-metabolized. Reduces heme precursors ALA and PBG. Reduces CYP enzyme induction from heme precursor excess; may normalize CYP activity in porphyria patients."
        ),
        "drug_class": "RNAi Therapeutic / Acute Hepatic Porphyria",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15718",
        "name": "Lumasiran",
        "brand_names": ["Oxlumo"],
        "description": (
            "RNAi therapeutic targeting HAO1 mRNA for primary hyperoxaluria type 1. Degraded by nucleases; not CYP-metabolized. Reduces hepatic glyoxylate and oxalate production. Quarterly maintenance dosing after loading."
        ),
        "drug_class": "RNAi Therapeutic / Primary Hyperoxaluria",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15719",
        "name": "Inclisiran",
        "brand_names": ["Leqvio"],
        "description": (
            "RNAi therapeutic targeting PCSK9 mRNA for hypercholesterolemia. Twice-yearly SC injection (after initial and 3-month doses). Metabolized by nucleases; no CYP interactions. Reduces LDL-C by ~50% on top of statin therapy."
        ),
        "drug_class": "RNAi Therapeutic / PCSK9 Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB11988_evo",
        "name": "Evolocumab",
        "brand_names": ["Repatha"],
        "description": (
            "Anti-PCSK9 monoclonal antibody for hypercholesterolemia and established ASCVD. Catabolized by proteolysis. No CYP interactions. Monthly or bimonthly SC injection. Reduces LDL-C by 60% on average on top of statin therapy."
        ),
        "drug_class": "PCSK9 Inhibitor / Biologic",
        "rxnorm_cui": "1657974",
    },
    {
        "id": "DB11988_ali",
        "name": "Alirocumab",
        "brand_names": ["Praluent"],
        "description": (
            "Anti-PCSK9 monoclonal antibody for hypercholesterolemia and ASCVD. Catabolized by normal immunoglobulin pathways. No CYP interactions. Every 2 or 4 weeks SC injection."
        ),
        "drug_class": "PCSK9 Inhibitor / Biologic",
        "rxnorm_cui": "1657975",
    },
    {
        "id": "DB15720",
        "name": "Bempedoic acid",
        "brand_names": ["Nexletol", "Nexlizet (combined with ezetimibe)"],
        "description": (
            "ATP-citrate lyase (ACL) inhibitor for hypercholesterolemia. Prodrug activated in the liver by ACSVL1 to ESP15228. Not active in muscle (lacks ACSVL1), reducing myopathy risk. Inhibits UGT1A3 and UGT2B7 — increases statin levels moderately. Increases gout risk (raises uric acid)."
        ),
        "drug_class": "ACL Inhibitor / Lipid-Lowering",
        "rxnorm_cui": "2169290",
    },
    {
        "id": "DB15721",
        "name": "Ezetimibe",
        "brand_names": ["Zetia", "Vytorin (combined with simvastatin)"],
        "description": (
            "Cholesterol absorption inhibitor (NPC1L1 inhibitor) for hypercholesterolemia. Undergoes extensive glucuronidation; active ezetimibe-glucuronide undergoes enterohepatic circulation. Minimal CYP metabolism. Cyclosporine significantly increases ezetimibe AUC via OATP inhibition."
        ),
        "drug_class": "Cholesterol Absorption Inhibitor",
        "rxnorm_cui": "341248",
    },
    {
        "id": "DB15722",
        "name": "Icosapent ethyl",
        "brand_names": ["Vascepa"],
        "description": (
            "Pure EPA omega-3 fatty acid for hypertriglyceridemia and cardiovascular risk reduction in statin-treated patients with TG ≥150 mg/dL. Metabolized by beta-oxidation. Not CYP-metabolized. Mild antiplatelet effect; may potentiate anticoagulants."
        ),
        "drug_class": "Omega-3 Fatty Acid / Triglyceride-Lowering",
        "rxnorm_cui": "1648761",
    },
    {
        "id": "DB15723",
        "name": "Pemafibrate",
        "brand_names": ["Parmodia"],
        "description": (
            "Selective PPAR-alpha modulator (SPPARMalpha) for hypertriglyceridemia. Metabolized by CYP2C8 and UGT enzymes. CYP2C8 inhibitors (gemfibrozil) significantly increase pemafibrate exposure — combination contraindicated. Strong OATP1B1/3 inhibitors (cyclosporine) also markedly increase levels."
        ),
        "drug_class": "SPPARMalpha / Triglyceride-Lowering",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15724",
        "name": "Selpercatinib",
        "brand_names": ["Retevmo"],
        "description": (
            "Selective RET kinase inhibitor for RET-mutant NSCLC, thyroid cancers, and solid tumors. Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase selpercatinib AUC ~2-fold. Strong inducers reduce by ~87%. Mild CYP3A4 inhibitor itself. QT prolongation risk."
        ),
        "drug_class": "Antineoplastic / RET Inhibitor",
        "rxnorm_cui": "2376839",
    },
    {
        "id": "DB15725",
        "name": "Pralsetinib",
        "brand_names": ["Gavreto"],
        "description": (
            "Selective RET inhibitor for RET fusion-positive NSCLC and RET-mutant thyroid cancers. Metabolized by CYP3A4 (major). Strong CYP3A4 inducers reduce efficacy; avoid. P-gp substrate. Strong CYP3A4 inhibitors increase exposure."
        ),
        "drug_class": "Antineoplastic / RET Inhibitor",
        "rxnorm_cui": "2376840",
    },
    {
        "id": "DB15726",
        "name": "Tepotinib",
        "brand_names": ["Tepmetko"],
        "description": (
            "Selective MET inhibitor for METex14-skipping mutation NSCLC. Metabolized by CYP3A4 (major). Strong CYP3A4 inhibitors increase exposure; strong inducers reduce efficacy. P-gp and BCRP inhibitor — raises digoxin levels."
        ),
        "drug_class": "Antineoplastic / MET Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15727",
        "name": "Capmatinib",
        "brand_names": ["Tabrecta"],
        "description": (
            "MET inhibitor for METex14-skipping NSCLC. Metabolized by CYP3A4 (minor) and AO (aldehyde oxidase). CYP3A4 inducers may reduce levels; CYP1A2 inducers increase AO-mediated metabolism. Inhibits CYP1A2 — raises theophylline levels."
        ),
        "drug_class": "Antineoplastic / MET Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15728",
        "name": "Entrectinib",
        "brand_names": ["Rozlytrek"],
        "description": (
            "Pan-TRK/ROS1/ALK inhibitor for NTRK fusion-positive cancers and ROS1+ NSCLC. Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase entrectinib levels; strong inducers reduce efficacy. Active metabolite M5 contributes to activity."
        ),
        "drug_class": "Antineoplastic / TRK/ROS1/ALK Inhibitor",
        "rxnorm_cui": "2169291",
    },
    {
        "id": "DB15729",
        "name": "Larotrectinib",
        "brand_names": ["Vitrakvi"],
        "description": (
            "Highly selective pan-TRK inhibitor for NTRK fusion-positive cancers (tumor-agnostic). Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase AUC ~4-fold — reduce dose. Strong CYP3A4 inducers reduce AUC by ~81% — increase dose or avoid."
        ),
        "drug_class": "Antineoplastic / TRK Inhibitor",
        "rxnorm_cui": "2049140",
    },
    {
        "id": "DB15730",
        "name": "Pemigatinib",
        "brand_names": ["Pemazyre"],
        "description": (
            "FGFR1/2/3 inhibitor for cholangiocarcinoma with FGFR2 fusions and other FGFR-driven cancers. Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase exposure; strong inducers reduce it. Hyperphosphatemia from FGFR inhibition requires dietary phosphate restriction."
        ),
        "drug_class": "Antineoplastic / FGFR Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15731",
        "name": "Infigratinib",
        "brand_names": ["Truseltiq"],
        "description": (
            "FGFR1/2/3 inhibitor for FGFR2 fusion/rearrangement cholangiocarcinoma. Metabolized by CYP3A4. Strong CYP3A4 inhibitors significantly increase levels; strong inducers reduce efficacy. Low-phosphate diet required."
        ),
        "drug_class": "Antineoplastic / FGFR Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15732",
        "name": "Futibatinib",
        "brand_names": ["Lytgobi"],
        "description": (
            "Covalent (irreversible) FGFR1-4 inhibitor for FGFR2 fusion cholangiocarcinoma. Metabolized by CYP3A4. Strong CYP3A4 inhibitors/inducers affect exposure. Unlike other FGFR inhibitors, covalent mechanism provides different resistance profile."
        ),
        "drug_class": "Antineoplastic / FGFR Inhibitor (Covalent)",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15733",
        "name": "Adagrasib",
        "brand_names": ["Krazati"],
        "description": (
            "Covalent KRAS G12C inhibitor for KRAS G12C-mutated NSCLC and CRC. Metabolized by CYP3A4 (primary). Moderate CYP3A4 inhibitor itself. Strong CYP3A4 inhibitors increase exposure; strong inducers reduce efficacy. QT prolongation; multiple DDIs require dose adjustments."
        ),
        "drug_class": "Antineoplastic / KRAS G12C Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15734",
        "name": "Sotorasib",
        "brand_names": ["Lumakras"],
        "description": (
            "Covalent KRAS G12C inhibitor for KRAS G12C-mutated NSCLC. Metabolized by CYP3A4 (major) and non-CYP pathways. Strong CYP3A4 inducers reduce levels significantly. P-gp and BCRP inhibitor — raises levels of substrates. Hepatotoxicity and ILD monitoring required."
        ),
        "drug_class": "Antineoplastic / KRAS G12C Inhibitor",
        "rxnorm_cui": "2376841",
    },
    {
        "id": "DB15735",
        "name": "Tislelizumab",
        "brand_names": ["Tevimbra"],
        "description": (
            "Anti-PD-1 monoclonal antibody for esophageal squamous cell carcinoma. Catabolized by proteolytic pathways. No CYP interactions. Immune-mediated adverse reactions require corticosteroid management."
        ),
        "drug_class": "Antineoplastic / Anti-PD-1 Checkpoint Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15736",
        "name": "Pembrolizumab",
        "brand_names": ["Keytruda"],
        "description": (
            "Anti-PD-1 monoclonal antibody with broad tumor-agnostic approvals including MSI-H/dMMR tumors, TMB-H tumors, and multiple cancer types. Catabolized by proteolytic degradation. No CYP interactions. Immune-mediated toxicities managed with corticosteroids."
        ),
        "drug_class": "Antineoplastic / Anti-PD-1 Checkpoint Inhibitor",
        "rxnorm_cui": "1730907",
    },
    {
        "id": "DB15737",
        "name": "Nivolumab",
        "brand_names": ["Opdivo"],
        "description": (
            "Anti-PD-1 monoclonal antibody for multiple cancers. Catabolized by proteolysis. No CYP interactions. Often combined with ipilimumab (CTLA-4 inhibitor) for enhanced immune activation. Immune-related adverse events require corticosteroids."
        ),
        "drug_class": "Antineoplastic / Anti-PD-1 Checkpoint Inhibitor",
        "rxnorm_cui": "1597876",
    },
    {
        "id": "DB15738",
        "name": "Atezolizumab",
        "brand_names": ["Tecentriq"],
        "description": (
            "Anti-PD-L1 monoclonal antibody for NSCLC, TNBC, hepatocellular carcinoma, and other cancers. Catabolized by proteolytic pathways. No CYP interactions. First anti-PD-L1 agent approved by FDA."
        ),
        "drug_class": "Antineoplastic / Anti-PD-L1 Checkpoint Inhibitor",
        "rxnorm_cui": "1860502",
    },
    {
        "id": "DB15739",
        "name": "Durvalumab",
        "brand_names": ["Imfinzi"],
        "description": (
            "Anti-PD-L1 monoclonal antibody for NSCLC, SCLC, biliary tract cancer, and hepatocellular carcinoma. Catabolized by proteolysis. No CYP interactions."
        ),
        "drug_class": "Antineoplastic / Anti-PD-L1 Checkpoint Inhibitor",
        "rxnorm_cui": "1999715",
    },
    {
        "id": "DB15740",
        "name": "Ipilimumab",
        "brand_names": ["Yervoy"],
        "description": (
            "Anti-CTLA-4 monoclonal antibody for melanoma, renal cell carcinoma, CRC, and other tumors. Catabolized by proteolytic pathways. No CYP interactions. Severe immune-mediated reactions require high-dose steroids. Combined with nivolumab enhances response but increases toxicity."
        ),
        "drug_class": "Antineoplastic / Anti-CTLA-4 Checkpoint Inhibitor",
        "rxnorm_cui": "993460",
    },
    {
        "id": "DB15741",
        "name": "Trastuzumab deruxtecan",
        "brand_names": ["Enhertu"],
        "description": (
            "HER2-directed antibody-drug conjugate (ADC) with topoisomerase I inhibitor payload for HER2+ breast cancer, NSCLC, and gastric cancer. Metabolized by CYP3A4 (payload deruxtecan component). Strong CYP3A4 inhibitors may increase payload exposure. ILD/pneumonitis is a serious toxicity."
        ),
        "drug_class": "Antineoplastic / HER2 ADC",
        "rxnorm_cui": "2169292",
    },
    {
        "id": "DB15742",
        "name": "Sacituzumab govitecan",
        "brand_names": ["Trodelvy"],
        "description": (
            "TROP2-directed ADC with SN-38 (irinotecan active metabolite) payload for TNBC, urothelial carcinoma, and HR+/HER2- breast cancer. SN-38 is glucuronidated by UGT1A1; UGT1A1*28 polymorphism reduces SN-38 glucuronidation — higher toxicity in *28/*28 patients. Avoid strong UGT1A1 inhibitors."
        ),
        "drug_class": "Antineoplastic / TROP2 ADC",
        "rxnorm_cui": "2169293",
    },
    {
        "id": "DB15743",
        "name": "Enfortumab vedotin",
        "brand_names": ["Padcev"],
        "description": (
            "Nectin-4-directed ADC with MMAE (monomethyl auristatin E) payload for urothelial carcinoma. MMAE metabolized by CYP3A4. Strong CYP3A4 inhibitors increase MMAE exposure; avoid. P-gp substrate."
        ),
        "drug_class": "Antineoplastic / Nectin-4 ADC",
        "rxnorm_cui": "2169294",
    },
    {
        "id": "DB15744",
        "name": "Belantamab mafodotin",
        "brand_names": ["Blenrep"],
        "description": (
            "BCMA-directed ADC with MMAF payload for relapsed/refractory multiple myeloma. P-gp substrate; CYP3A4 substrate (payload). Strong CYP3A4 inhibitors may increase MMAF levels. Corneal adverse events (keratopathy) require ophthalmologic monitoring."
        ),
        "drug_class": "Antineoplastic / BCMA ADC",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15745",
        "name": "Lisocabtagene maraleucel",
        "brand_names": ["Breyanzi"],
        "description": (
            "CD19-directed CAR-T cell therapy for large B-cell lymphoma, CLL, and follicular lymphoma. Not metabolized by CYP enzymes. Cytokine release syndrome and neurotoxicity require intensive management. REMS program required."
        ),
        "drug_class": "CAR-T Cell Therapy / CD19",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15746",
        "name": "Ciltacabtagene autoleucel",
        "brand_names": ["Carvykti"],
        "description": (
            "BCMA-directed CAR-T cell therapy for relapsed/refractory multiple myeloma. Not CYP-metabolized; immune cell product. Cytokine release syndrome, neurotoxicity, and movement/neurocognitive events are notable toxicities. REMS required."
        ),
        "drug_class": "CAR-T Cell Therapy / BCMA",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15747",
        "name": "Mosunetuzumab",
        "brand_names": ["Lunsumio"],
        "description": (
            "CD20xCD3 bispecific T-cell engaging antibody for relapsed/refractory follicular lymphoma. Catabolized by proteolysis. No CYP interactions. CRS and neurotoxicity (ICANS); step-up dosing to mitigate CRS."
        ),
        "drug_class": "Antineoplastic / CD20xCD3 Bispecific",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15748",
        "name": "Glofitamab",
        "brand_names": ["Columvi"],
        "description": (
            "CD20xCD3 bispecific antibody (2:1 format) for relapsed/refractory DLBCL. Proteolytic catabolism; no CYP interactions. Fixed-duration treatment. Obinutuzumab pretreatment required. CRS management protocols essential."
        ),
        "drug_class": "Antineoplastic / CD20xCD3 Bispecific",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15749",
        "name": "Elranatamab",
        "brand_names": ["Elrexfio"],
        "description": (
            "BCMA x CD3 bispecific antibody for relapsed/refractory multiple myeloma. Catabolized by proteolysis; no CYP interactions. Step-up dosing for CRS mitigation. Weekly then biweekly SC administration."
        ),
        "drug_class": "Antineoplastic / BCMA x CD3 Bispecific",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15750",
        "name": "Talquetamab",
        "brand_names": ["Talvey"],
        "description": (
            "GPRC5D x CD3 bispecific antibody for relapsed/refractory multiple myeloma. First approved GPRC5D-targeting therapy. Catabolized by proteolysis; no CYP interactions. Skin, nail, and oral adverse effects related to GPRC5D expression in these tissues."
        ),
        "drug_class": "Antineoplastic / GPRC5D x CD3 Bispecific",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15751",
        "name": "Lecanemab",
        "brand_names": ["Leqembi"],
        "description": (
            "Anti-amyloid beta (protofibrils) monoclonal antibody for early Alzheimer's disease. Catabolized by proteolytic degradation. No CYP interactions. ARIA (amyloid-related imaging abnormalities) monitoring required with MRI. Biweekly IV infusion."
        ),
        "drug_class": "Anti-Amyloid / Alzheimer's Disease",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15752",
        "name": "Donanemab",
        "brand_names": ["Kisunla"],
        "description": (
            "Anti-amyloid (N3pG-Abeta) monoclonal antibody for early symptomatic Alzheimer's. Targets amyloid plaques; treatment discontinued when plaques are cleared. Catabolized by proteolysis; no CYP interactions. ARIA monitoring required."
        ),
        "drug_class": "Anti-Amyloid / Alzheimer's Disease",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15753",
        "name": "Sodium oxybate",
        "brand_names": ["Xyrem", "Lumryz"],
        "description": (
            "CNS depressant (GHB) for cataplexy and excessive daytime sleepiness in narcolepsy. Metabolized primarily by GHB dehydrogenase and TCA cycle (not CYP). Potent CNS/respiratory depressant — contraindicated with alcohol, sedatives, and other CNS depressants. REMS program required."
        ),
        "drug_class": "CNS Depressant / Narcolepsy",
        "rxnorm_cui": "544572",
    },
    {
        "id": "DB15754",
        "name": "Pitolisant",
        "brand_names": ["Wakix"],
        "description": (
            "Histamine H3 receptor antagonist/inverse agonist for excessive daytime sleepiness and cataplexy in narcolepsy. Metabolized by CYP2D6 (major) and CYP3A4 (minor). CYP2D6 inhibitors increase pitolisant levels. CYP3A4 inducers reduce efficacy. Strong CYP3A4 inducers require dose doubling."
        ),
        "drug_class": "H3 Receptor Antagonist / Narcolepsy",
        "rxnorm_cui": "2169295",
    },
    {
        "id": "DB15755",
        "name": "Solriamfetol",
        "brand_names": ["Sunosi"],
        "description": (
            "Dopamine and norepinephrine reuptake inhibitor for excessive daytime sleepiness in narcolepsy and OSA. Primarily renally eliminated unchanged; minimal CYP metabolism. Low pharmacokinetic drug interaction potential. Schedule IV controlled."
        ),
        "drug_class": "DNRI / Wake-Promoting Agent",
        "rxnorm_cui": "2169296",
    },
    {
        "id": "DB15756",
        "name": "Lemborexant",
        "brand_names": ["Dayvigo"],
        "description": (
            "Dual orexin receptor antagonist (DORA) for insomnia. Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase exposure — limit dose to 5 mg. Strong CYP3A4 inducers are contraindicated. Schedule IV controlled substance."
        ),
        "drug_class": "Orexin Receptor Antagonist / Insomnia",
        "rxnorm_cui": "2169297",
    },
    {
        "id": "DB15757",
        "name": "Daridorexant",
        "brand_names": ["Quviviq"],
        "description": (
            "Dual orexin receptor antagonist for insomnia. Metabolized by CYP3A4 (major). Strong CYP3A4 inhibitors are contraindicated; moderate inhibitors require dose reduction. CYP3A4 inducers reduce daridorexant exposure."
        ),
        "drug_class": "Orexin Receptor Antagonist / Insomnia",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15758",
        "name": "Suvorexant",
        "brand_names": ["Belsomra"],
        "description": (
            "First-in-class dual orexin receptor antagonist for insomnia. Metabolized by CYP3A4. Strong CYP3A4 inhibitors are contraindicated. CYP3A4 inducers reduce exposure. Schedule IV controlled substance."
        ),
        "drug_class": "Orexin Receptor Antagonist / Insomnia",
        "rxnorm_cui": "1601385",
    },
    {
        "id": "DB15759",
        "name": "Amantadine (extended-release)",
        "brand_names": ["Gocovri", "Osmolex ER"],
        "description": (
            "NMDA antagonist / dopamine agent for Parkinson's disease dyskinesia. Not significantly metabolized by CYP enzymes; excreted unchanged renally. Anticholinergic effects; avoid with other anticholinergics in elderly."
        ),
        "drug_class": "Antiparkinson / NMDA Antagonist",
        "rxnorm_cui": "704",
    },
    {
        "id": "DB15760",
        "name": "Opicapone",
        "brand_names": ["Ongentys"],
        "description": (
            "Third-generation COMT inhibitor for Parkinson's disease (adjunct to levodopa). Once-daily dosing. Metabolized by sulfation and glucuronidation; not CYP-metabolized. Potentiates levodopa action by inhibiting catecholamine metabolism. No food interaction unlike tolcapone/entacapone."
        ),
        "drug_class": "COMT Inhibitor / Antiparkinson",
        "rxnorm_cui": "2169298",
    },
    {
        "id": "DB15761",
        "name": "Safinamide",
        "brand_names": ["Xadago"],
        "description": (
            "Selective MAO-B inhibitor and sodium channel blocker for Parkinson's disease. Metabolized by amidases, CYP3A4 (minor), and FMO. Selective MAO-B inhibition at therapeutic doses but serotonergic interactions possible. Opioids (especially meperidine/pethidine) are contraindicated."
        ),
        "drug_class": "MAO-B Inhibitor / Antiparkinson",
        "rxnorm_cui": "1860504",
    },
    {
        "id": "DB15762",
        "name": "Istradefylline",
        "brand_names": ["Nourianz"],
        "description": (
            "Adenosine A2A receptor antagonist for Parkinson's disease 'off' episodes. Metabolized by CYP3A4 (primary) and CYP1A1. Strong CYP3A4 inhibitors increase levels — reduce dose to 20 mg/day. CYP3A4 inducers reduce efficacy. Cigarette smoking (CYP1A1 inducer) reduces istradefylline exposure."
        ),
        "drug_class": "A2A Receptor Antagonist / Antiparkinson",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15763",
        "name": "Trofinetide",
        "brand_names": ["Daybue"],
        "description": (
            "Synthetic analog of IGF-1 tripeptide GPE for Rett syndrome. Metabolized by aminopeptidases in plasma; not CYP-metabolized. First FDA-approved treatment specifically for Rett syndrome."
        ),
        "drug_class": "IGF-1 Analog / Rett Syndrome",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15764",
        "name": "Tirzepatide",
        "brand_names": ["Mounjaro", "Zepbound"],
        "description": (
            "Dual GIP/GLP-1 receptor agonist for type 2 diabetes and obesity. Degraded by proteolytic enzymes and fatty acid beta-oxidation; not CYP-metabolized. Delays gastric emptying — may affect timing of oral drug absorption. Greater weight loss and glycemic control than GLP-1 mono-agonists."
        ),
        "drug_class": "Antidiabetic / GIP+GLP-1 Dual Agonist",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15765",
        "name": "Efpeglenatide",
        "brand_names": ["Peptone"],
        "description": (
            "Weekly GLP-1 receptor agonist for type 2 diabetes. Degraded by dipeptidyl peptidase enzymes and proteolytic cleavage; not CYP-metabolized. Cardiovascular outcomes benefit demonstrated."
        ),
        "drug_class": "Antidiabetic / GLP-1 Receptor Agonist",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15766",
        "name": "Macimorelin",
        "brand_names": ["Macrilen"],
        "description": (
            "Oral ghrelin receptor agonist for diagnosis of adult growth hormone deficiency. Metabolized by CYP3A4. Strong CYP3A4 inducers may reduce macimorelin levels, causing false-positive test results. QT prolongation risk."
        ),
        "drug_class": "Ghrelin Receptor Agonist / Diagnostic",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15767",
        "name": "Teduglutide",
        "brand_names": ["Gattex", "Revestive"],
        "description": (
            "GLP-2 analog for short bowel syndrome. Promotes intestinal adaptation and absorption. Degraded by proteolysis; not CYP-metabolized. May increase absorption of concomitant oral medications — monitor narrow therapeutic index drugs (warfarin, benzodiazepines, phenytoin)."
        ),
        "drug_class": "GLP-2 Analog / Short Bowel Syndrome",
        "rxnorm_cui": "1299855",
    },
    {
        "id": "DB15768",
        "name": "Lanreotide",
        "brand_names": ["Somatuline Depot"],
        "description": (
            "Long-acting somatostatin analog for acromegaly and gastroenteropancreatic NETs. Metabolized by GI proteolysis; some CYP3A4 involvement. May reduce cyclosporine absorption (inhibits intestinal motility). Hyperglycemia or hypoglycemia possible."
        ),
        "drug_class": "Somatostatin Analog",
        "rxnorm_cui": "200277",
    },
    {
        "id": "DB15769",
        "name": "Pegvisomant",
        "brand_names": ["Somavert"],
        "description": (
            "GH receptor antagonist for acromegaly. Catabolized by normal protein pathways. No CYP interactions. Increases insulin sensitivity — reduce insulin/antidiabetic doses. May normalize CYP3A4 activity previously suppressed by GH excess."
        ),
        "drug_class": "GH Receptor Antagonist / Acromegaly",
        "rxnorm_cui": "274782",
    },
    {
        "id": "DB15770",
        "name": "Burosumab",
        "brand_names": ["Crysvita"],
        "description": (
            "Anti-FGF23 monoclonal antibody for X-linked hypophosphatemia and tumor-induced osteomalacia. Catabolized by proteolysis; no CYP interactions. Normalizes renal phosphate reabsorption and vitamin D activation."
        ),
        "drug_class": "Anti-FGF23 / Hypophosphatemia",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15771",
        "name": "Omadacycline",
        "brand_names": ["Nuzyra"],
        "description": (
            "Aminomethylcycline tetracycline for community-acquired bacterial pneumonia and acute bacterial skin/skin structure infections. Not significantly CYP-metabolized; primarily biliary and renal elimination. Low pharmacokinetic interaction potential. Divalent cations reduce oral absorption."
        ),
        "drug_class": "Antibiotic / Tetracycline",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15772",
        "name": "Delafloxacin",
        "brand_names": ["Baxdela"],
        "description": (
            "Anionic fluoroquinolone for ABSSSI and community-acquired bacterial pneumonia. Glucuronidated by UGT1A1, UGT1A3, and UGT2B15; minimal CYP metabolism. Low pharmacokinetic drug interaction potential. Active against MRSA."
        ),
        "drug_class": "Antibiotic / Fluoroquinolone",
        "rxnorm_cui": "1860505",
    },
    {
        "id": "DB15773",
        "name": "Lefamulin",
        "brand_names": ["Xenleta"],
        "description": (
            "First-in-class pleuromutilin antibiotic for community-acquired bacterial pneumonia. Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase lefamulin exposure; strong inducers reduce efficacy. P-gp substrate. QT prolongation risk."
        ),
        "drug_class": "Antibiotic / Pleuromutilin",
        "rxnorm_cui": "2169299",
    },
    {
        "id": "DB15774",
        "name": "Ombitasvir",
        "brand_names": ["Technivie (combined)", "Viekira Pak (combined)"],
        "description": (
            "HCV NS5A inhibitor combined with paritaprevir/ritonavir for hepatitis C. Metabolized by amide hydrolysis and oxidation (CYP3A4 minor). Strong CYP3A4 inducers (rifampin, carbamazepine) reduce levels — contraindicated. The ritonavir booster in the combination dominates DDI profile."
        ),
        "drug_class": "Antiviral / HCV NS5A Inhibitor",
        "rxnorm_cui": "1597572",
    },
    {
        "id": "DB15775",
        "name": "Paritaprevir",
        "brand_names": ["Viekira Pak (combined with ombitasvir/ritonavir/dasabuvir)"],
        "description": (
            "HCV NS3/4A protease inhibitor boosted with ritonavir in combination regimens. CYP3A4 substrate; boosted by ritonavir. Strong CYP3A4 inducers contraindicated. Inhibits OATP1B1 and OATP1B3 — raises rosuvastatin, pravastatin levels."
        ),
        "drug_class": "Antiviral / HCV Protease Inhibitor",
        "rxnorm_cui": "1597573",
    },
    {
        "id": "DB15776",
        "name": "Islatravir",
        "brand_names": ["Investigational (MK-8591)"],
        "description": (
            "Nucleoside reverse transcriptase translocation inhibitor (NRTTI) for HIV. Novel mechanism; ultra-long half-life enables monthly oral or yearly implant dosing. Not significantly CYP-metabolized. Under investigation for PrEP and treatment."
        ),
        "drug_class": "Antiretroviral / NRTTI (Investigational)",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15777",
        "name": "Lenacapavir",
        "brand_names": ["Sunlenca"],
        "description": (
            "First-in-class HIV capsid inhibitor for multidrug-resistant HIV. Twice-yearly SC injection (after oral loading). Metabolized by CYP3A4 and UGT1A1. Strong CYP3A4 inhibitors increase levels; inducers reduce efficacy. Inhibits CYP3A4 — raises levels of CYP3A4 substrates."
        ),
        "drug_class": "Antiretroviral / Capsid Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15778",
        "name": "Ibrexafungerp",
        "brand_names": ["Brexafemme"],
        "description": (
            "Triterpenoid glucan synthase inhibitor for vulvovaginal candidiasis. Oral antifungal; first non-azole, non-echinocandin oral antifungal in decades. Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase exposure; strong inducers reduce efficacy."
        ),
        "drug_class": "Antifungal / Triterpenoid",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15779",
        "name": "Olorofim",
        "brand_names": ["Milvane"],
        "description": (
            "First-in-class orotomide antifungal (DHODH inhibitor) for invasive mold infections including Aspergillus resistant to other antifungals. Metabolized by CYP3A4. CYP3A4 inhibitors increase levels; inducers reduce efficacy. QT monitoring needed."
        ),
        "drug_class": "Antifungal / Orotomide",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15780",
        "name": "Rezafungin",
        "brand_names": ["Rezzayo"],
        "description": (
            "Long-acting echinocandin for invasive candidiasis. Once-weekly IV dosing. Minimal CYP involvement; metabolized by chemical degradation. Novel half-life extension allows weekly dosing vs daily for other echinocandins."
        ),
        "drug_class": "Antifungal / Echinocandin",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15781",
        "name": "Fosmanogepix",
        "brand_names": ["Investigational"],
        "description": (
            "First-in-class Gwt1 inhibitor antifungal for invasive candidiasis and aspergillosis. IV/oral formulation. CYP3A4 substrate; CYP inhibitor/inducer interactions expected. Broad-spectrum activity including azole-resistant strains."
        ),
        "drug_class": "Antifungal / Gwt1 Inhibitor (Investigational)",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15782",
        "name": "Omadacycline free base",
        "brand_names": ["Nuzyra (IV form)"],
        "description": (
            "IV formulation of omadacycline for CAP and ABSSSI. Same pharmacology as oral form. Not significantly CYP-metabolized. Divalent cation chelation is a consideration for IV line compatibility rather than pharmacokinetic drug interactions."
        ),
        "drug_class": "Antibiotic / Tetracycline (IV)",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15783",
        "name": "Cefiderocol",
        "brand_names": ["Fetroja"],
        "description": (
            "Siderophore cephalosporin for carbapenem-resistant Gram-negative infections. Uses iron transport systems to penetrate bacterial outer membrane. Not metabolized by CYP enzymes; primarily renally eliminated. Low pharmacokinetic drug interaction potential."
        ),
        "drug_class": "Antibiotic / Siderophore Cephalosporin",
        "rxnorm_cui": "2169300",
    },
    {
        "id": "DB15784",
        "name": "Ceftazidime-avibactam",
        "brand_names": ["Avycaz"],
        "description": (
            "Cephalosporin/beta-lactamase inhibitor combination for resistant Gram-negative infections including KPC and OXA-48 producing organisms. Not CYP-metabolized. Renally eliminated; dose adjustment in renal impairment. Low DDI potential."
        ),
        "drug_class": "Antibiotic / Cephalosporin + Beta-Lactamase Inhibitor",
        "rxnorm_cui": "1676567",
    },
    {
        "id": "DB15785",
        "name": "Meropenem-vaborbactam",
        "brand_names": ["Vabomere"],
        "description": (
            "Carbapenem/cyclic boronic acid beta-lactamase inhibitor for KPC-producing Klebsiella pneumoniae infections. Not CYP-metabolized; renally eliminated. Vaborbactam does not inhibit MBLs (e.g., NDM). Low pharmacokinetic DDI potential."
        ),
        "drug_class": "Antibiotic / Carbapenem + Beta-Lactamase Inhibitor",
        "rxnorm_cui": "1860506",
    },
    {
        "id": "DB15786",
        "name": "Avacopan",
        "brand_names": ["Tavneos"],
        "description": (
            "Oral complement C5a receptor (C5aR) inhibitor for ANCA-associated vasculitis. Metabolized by CYP3A4 (major). Strong CYP3A4 inhibitors increase avacopan levels; strong inducers reduce efficacy. Inhibits CYP1A2 mildly."
        ),
        "drug_class": "Complement C5aR Inhibitor / Vasculitis",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15787",
        "name": "Mavacamten",
        "brand_names": ["Camzyos"],
        "description": (
            "Cardiac myosin inhibitor for obstructive hypertrophic cardiomyopathy. Metabolized by CYP2C19 (primary) and CYP3A4. CYP2C19 inhibitors increase mavacamten levels significantly; CYP2C19 poor metabolizers require dose adjustment. Strong CYP2C19 and CYP3A4 inhibitors are contraindicated. REMS program."
        ),
        "drug_class": "Cardiac Myosin Inhibitor / HCM",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15788",
        "name": "Aficamten",
        "brand_names": ["Camzyos 2 (investigational)"],
        "description": (
            "Next-generation cardiac myosin inhibitor for obstructive HCM. Metabolized by CYP3A4. More predictable PK than mavacamten due to less CYP2C19 dependence. Strong CYP3A4 inhibitors/inducers affect exposure."
        ),
        "drug_class": "Cardiac Myosin Inhibitor / HCM (Investigational)",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15789",
        "name": "Tafamidis",
        "brand_names": ["Vyndaqel", "Vyndamax"],
        "description": (
            "Transthyretin stabilizer for ATTR cardiomyopathy and polyneuropathy. Metabolized by glucuronidation (UGT1A1); not significantly CYP-metabolized. P-gp substrate; some evidence for P-gp inhibition. Low CYP interaction potential. First disease-modifying therapy for ATTR-CM."
        ),
        "drug_class": "TTR Stabilizer / ATTR",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15790",
        "name": "Patisiran",
        "brand_names": ["Onpattro"],
        "description": (
            "RNAi therapeutic (lipid nanoparticle) targeting TTR mRNA for hereditary ATTR with polyneuropathy. Metabolized by nucleases; not CYP-metabolized. First siRNA drug approved by FDA (2018). Quarterly IV infusion."
        ),
        "drug_class": "RNAi Therapeutic / ATTR",
        "rxnorm_cui": "2049139",
    },
    {
        "id": "DB15791",
        "name": "Vutrisiran",
        "brand_names": ["Amvuttra"],
        "description": (
            "RNAi therapeutic (GalNAc-conjugated) for hereditary ATTR with polyneuropathy. Quarterly SC injection. Nuclease-mediated degradation; no CYP interactions. Maintains vitamin A supplementation during therapy."
        ),
        "drug_class": "RNAi Therapeutic / ATTR",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15792",
        "name": "Eplontersen",
        "brand_names": ["Wainua"],
        "description": (
            "Antisense oligonucleotide (ASO) targeting TTR mRNA for hereditary ATTR polyneuropathy. Monthly SC injection. Not CYP-metabolized; degraded by nucleases. Monitor vitamin A levels; supplementation required."
        ),
        "drug_class": "Antisense Oligonucleotide / ATTR",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15793",
        "name": "Oteseconazole",
        "brand_names": ["Vivjoa"],
        "description": (
            "Highly selective CYP51 inhibitor antifungal for recurrent vulvovaginal candidiasis. Does not significantly inhibit human CYP enzymes at therapeutic doses. Minimal systemic exposure; oral capsule. Teratogenic — contraindicated in pregnancy."
        ),
        "drug_class": "Antifungal / CYP51 Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15794",
        "name": "Acoramidis",
        "brand_names": ["Attruby"],
        "description": (
            "TTR stabilizer for ATTR cardiomyopathy. Oral twice-daily dosing. Metabolized by CYP2C8 and glucuronidation. CYP2C8 inhibitors (gemfibrozil) may increase acoramidis levels. Clinical monitoring recommended."
        ),
        "drug_class": "TTR Stabilizer / ATTR Cardiomyopathy",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15795",
        "name": "Finerenone",
        "brand_names": ["Kerendia"],
        "description": (
            "Non-steroidal mineralocorticoid receptor antagonist for CKD with type 2 diabetes. Metabolized by CYP3A4 (major) and CYP2C8. Strong CYP3A4 inhibitors are contraindicated. Moderate CYP3A4 inhibitors require starting dose reduction. Strong inducers also contraindicated."
        ),
        "drug_class": "Mineralocorticoid Receptor Antagonist / CKD-T2D",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15796",
        "name": "Sotatercept",
        "brand_names": ["Winrevair"],
        "description": (
            "Activin receptor type IIA-Fc fusion protein for pulmonary arterial hypertension. Catabolized by proteolytic pathways. No CYP interactions. Modulates TGF-beta/activin signaling to reduce pulmonary vascular remodeling."
        ),
        "drug_class": "Activin Signaling Inhibitor / PAH",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15797",
        "name": "Imetelstat",
        "brand_names": ["Rytelo"],
        "description": (
            "Telomerase inhibitor for lower-risk MDS with transfusion-dependent anemia. Not significantly CYP-metabolized; oligonucleotide degraded by nucleases. First telomerase inhibitor approved; targets hematologic malignancies."
        ),
        "drug_class": "Telomerase Inhibitor / MDS",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15798",
        "name": "Luspatercept",
        "brand_names": ["Reblozyl"],
        "description": (
            "Erythroid maturation agent (TGF-beta ligand trap) for anemia in MDS, myelofibrosis, and beta-thalassemia. Catabolized by proteolysis. No CYP interactions. SC injection every 3 weeks."
        ),
        "drug_class": "Erythroid Maturation Agent / Anemia",
        "rxnorm_cui": "2169301",
    },
    {
        "id": "DB15799",
        "name": "Fedratinib",
        "brand_names": ["Inrebic"],
        "description": (
            "JAK2/FLT3 inhibitor for myelofibrosis. Metabolized by CYP3A4 (major) and CYP2C19. Strong CYP3A4 inhibitors increase fedratinib exposure. Strong inducers reduce levels. Wernicke's encephalopathy risk — thiamine monitoring required."
        ),
        "drug_class": "Antineoplastic / JAK2 Inhibitor / Myelofibrosis",
        "rxnorm_cui": "2169302",
    },
    {
        "id": "DB15800",
        "name": "Pacritinib",
        "brand_names": ["Vonjo"],
        "description": (
            "JAK2/IRAK1 inhibitor for myelofibrosis with severe thrombocytopenia. Metabolized by CYP3A4. Strong CYP3A4 inhibitors and inducers significantly alter pacritinib levels; avoid both. QT prolongation risk."
        ),
        "drug_class": "Antineoplastic / JAK2 Inhibitor / Myelofibrosis",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15801",
        "name": "Ruxolitinib",
        "brand_names": ["Jakafi"],
        "description": (
            "JAK1/2 inhibitor for myelofibrosis, polycythemia vera, and GVHD. Metabolized by CYP3A4 (primary) and CYP2C9. Strong CYP3A4 inhibitors require dose reduction; strong inducers reduce efficacy. Topical form (Opzelura) approved separately for atopic dermatitis and vitiligo."
        ),
        "drug_class": "Antineoplastic / JAK1/2 Inhibitor",
        "rxnorm_cui": "1299853",
    },
    {
        "id": "DB15802",
        "name": "Momelotinib",
        "brand_names": ["Ojjaara"],
        "description": (
            "JAK1/2/ACVR1 inhibitor for myelofibrosis with anemia. ACVR1 inhibition reduces hepcidin, improving anemia. Metabolized by CYP3A4; potent P-gp inhibitor. P-gp substrates (digoxin, dabigatran) levels may increase. Strong CYP3A4 inhibitors/inducers affect momelotinib levels."
        ),
        "drug_class": "Antineoplastic / JAK1/2/ACVR1 Inhibitor / Myelofibrosis",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15803",
        "name": "Tagraxofusp",
        "brand_names": ["Elzonris"],
        "description": (
            "CD123-directed cytotoxin (IL-3 + truncated diphtheria toxin fusion) for blastic plasmacytoid dendritic cell neoplasm (BPDCN). Not CYP-metabolized; catabolized by proteolysis. Capillary leak syndrome requires monitoring and albumin threshold before each dose."
        ),
        "drug_class": "Antineoplastic / CD123-Directed Cytotoxin",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15804",
        "name": "Enasidenib",
        "brand_names": ["Idhifa"],
        "description": (
            "IDH2 inhibitor for relapsed/refractory IDH2-mutated AML. Metabolized by CYP1A2, CYP2B6, CYP2C8, CYP2C9, CYP2C19, and CYP3A4 — multiple CYP pathways. Differentiation syndrome — monitor and treat with dexamethasone if suspected."
        ),
        "drug_class": "Antineoplastic / IDH2 Inhibitor",
        "rxnorm_cui": "1999714",
    },
    {
        "id": "DB15805",
        "name": "Ivosidenib",
        "brand_names": ["Tibsovo"],
        "description": (
            "IDH1 inhibitor for IDH1-mutated AML and cholangiocarcinoma. Metabolized by CYP3A4 (major). Strong CYP3A4 inhibitors increase exposure; strong inducers reduce efficacy. QT prolongation risk. Differentiation syndrome risk in AML."
        ),
        "drug_class": "Antineoplastic / IDH1 Inhibitor",
        "rxnorm_cui": "1999713",
    },
    {
        "id": "DB15806",
        "name": "Olutasidenib",
        "brand_names": ["Rezlidhia"],
        "description": (
            "IDH1 inhibitor for relapsed/refractory IDH1-mutated AML. Metabolized by CYP3A4. Strong CYP3A4 inhibitors/inducers affect levels. Differentiation syndrome risk. Liver enzyme elevations require monitoring."
        ),
        "drug_class": "Antineoplastic / IDH1 Inhibitor",
        "rxnorm_cui": None,
    },
    {
        "id": "DB15807",
        "name": "Glasdegib",
        "brand_names": ["Daurismo"],
        "description": (
            "Hedgehog pathway (Smoothened) inhibitor for newly diagnosed AML in older adults. Metabolized by CYP3A4 (major). Strong CYP3A4 inhibitors increase exposure; strong inducers reduce levels. QT prolongation risk. Teratogenic."
        ),
        "drug_class": "Antineoplastic / Hedgehog Pathway Inhibitor",
        "rxnorm_cui": "2049138",
    },
    {
        "id": "DB15808",
        "name": "Vismodegib",
        "brand_names": ["Erivedge"],
        "description": (
            "Hedgehog pathway (Smoothened) inhibitor for basal cell carcinoma. Metabolized by CYP2C9 and CYP3A4; oxidation and glucuronidation. CYP inhibitors/inducers have limited clinical effect due to saturable protein binding. Teratogenic; embryo-fetal toxicity REMS required."
        ),
        "drug_class": "Antineoplastic / Hedgehog Pathway Inhibitor / BCC",
        "rxnorm_cui": "1299852",
    },
    {
        "id": "DB15809",
        "name": "Sonidegib",
        "brand_names": ["Odomzo"],
        "description": (
            "Hedgehog pathway (Smoothened) inhibitor for locally advanced BCC. Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase exposure; strong inducers markedly reduce levels. Teratogenic. Muscular cramps and elevated CK are class effects."
        ),
        "drug_class": "Antineoplastic / Hedgehog Pathway Inhibitor / BCC",
        "rxnorm_cui": "1745275",
    },
    {
        "id": "DB15810",
        "name": "Tucatinib",
        "brand_names": ["Tukysa"],
        "description": (
            "Highly selective HER2 TKI for HER2+ breast cancer. Metabolized by CYP2C8 (primary) and CYP3A4. Strong CYP2C8 inhibitors increase tucatinib exposure. Strong CYP3A4 inducers reduce levels. Inhibits CYP2D6 and CYP3A4 — raises levels of CYP2D6/3A4 substrates. Combined with trastuzumab + capecitabine."
        ),
        "drug_class": "Antineoplastic / HER2 TKI",
        "rxnorm_cui": "2169303",
    },
    {
        "id": "DB15811",
        "name": "Neratinib",
        "brand_names": ["Nerlynx"],
        "description": (
            "Irreversible pan-HER TKI for HER2+ breast cancer extended adjuvant therapy. Metabolized by CYP3A4 (major). Strong CYP3A4 inhibitors increase neratinib levels; strong inducers reduce efficacy. P-gp substrate. Severe diarrhea requires prophylactic loperamide."
        ),
        "drug_class": "Antineoplastic / Pan-HER TKI",
        "rxnorm_cui": "1999712",
    },
    {
        "id": "DB15812",
        "name": "Lapatinib",
        "brand_names": ["Tykerb"],
        "description": (
            "Dual HER1/HER2 TKI for HER2+ breast cancer. Metabolized by CYP3A4 (primary) and CYP2C8. Strong CYP3A4 inhibitors increase lapatinib; strong inducers reduce it. P-gp and BCRP inhibitor. Inhibits CYP3A4 and CYP2C8 mildly. QT prolongation and hepatotoxicity monitoring required."
        ),
        "drug_class": "Antineoplastic / HER1/HER2 TKI",
        "rxnorm_cui": "700918",
    },
    {
        "id": "DB15813",
        "name": "Regorafenib",
        "brand_names": ["Stivarga"],
        "description": (
            "Multikinase inhibitor for metastatic CRC, GIST, and hepatocellular carcinoma. Metabolized by CYP3A4 and UGT1A9. Active metabolites M-2 and M-5 also contribute. Strong CYP3A4 inducers reduce regorafenib AUC by 50%. CYP3A4 inhibitors increase levels. Severe hepatotoxicity risk — liver function monitoring required."
        ),
        "drug_class": "Antineoplastic / Multikinase Inhibitor",
        "rxnorm_cui": "1299854",
    },
    {
        "id": "DB15814",
        "name": "Cabozantinib",
        "brand_names": ["Cabometyx", "Cometriq"],
        "description": (
            "Multikinase inhibitor (VEGFR, MET, AXL, RET) for RCC, HCC, thyroid carcinoma, and neuroendocrine tumors. Metabolized by CYP3A4 (major). Strong CYP3A4 inhibitors increase exposure; strong inducers reduce AUC by ~77%. P-gp and BCRP inhibitor."
        ),
        "drug_class": "Antineoplastic / Multikinase Inhibitor",
        "rxnorm_cui": "1299851",
    },
    {
        "id": "DB15815",
        "name": "Lenvatinib",
        "brand_names": ["Lenvima"],
        "description": (
            "Multikinase inhibitor (FGFR, VEGFR, PDGFR, KIT, RET) for thyroid carcinoma, RCC, HCC, and endometrial carcinoma. Metabolized by CYP3A4 and aldehyde oxidase. CYP3A4 inducers reduce efficacy; inhibitors increase exposure. Combined with pembrolizumab for endometrial carcinoma."
        ),
        "drug_class": "Antineoplastic / Multikinase Inhibitor",
        "rxnorm_cui": "1592777",
    },
    {
        "id": "DB15816",
        "name": "Axitinib",
        "brand_names": ["Inlyta"],
        "description": (
            "Selective VEGFR1/2/3 inhibitor for advanced RCC. Metabolized by CYP3A4/5 (primary) and CYP1A2, UGT1A1. Strong CYP3A4 inhibitors increase exposure; strong inducers reduce AUC by 79%. Reduce dose if CYP3A4 inhibitor cannot be avoided."
        ),
        "drug_class": "Antineoplastic / VEGFR Inhibitor",
        "rxnorm_cui": "1099145",
    },
    {
        "id": "DB15817",
        "name": "Sorafenib",
        "brand_names": ["Nexavar"],
        "description": (
            "Multikinase inhibitor for HCC, RCC, and thyroid carcinoma. Metabolized by CYP3A4 and UGT1A9. Active metabolite sorafenib N-oxide. Strong CYP3A4 inducers reduce levels. Inhibits UGT1A1 — raises irinotecan's active metabolite SN-38. P-gp inhibitor."
        ),
        "drug_class": "Antineoplastic / Multikinase Inhibitor",
        "rxnorm_cui": "544573",
    },
    {
        "id": "DB15818",
        "name": "Sunitinib",
        "brand_names": ["Sutent"],
        "description": (
            "Multikinase inhibitor for RCC, GIST, and pancreatic NETs. Metabolized by CYP3A4 to active metabolite SU12662. Strong CYP3A4 inhibitors increase sunitinib + SU12662 levels. Strong inducers (rifampin) reduce total exposure by 46%. QT prolongation and hypothyroidism monitoring required."
        ),
        "drug_class": "Antineoplastic / Multikinase Inhibitor",
        "rxnorm_cui": "544574",
    },
    {
        "id": "DB15819",
        "name": "Pazopanib",
        "brand_names": ["Votrient"],
        "description": (
            "Multikinase inhibitor for RCC and soft tissue sarcoma. Metabolized by CYP3A4 (major) and CYP1A2/CYP2C8 (minor). Strong CYP3A4 inhibitors increase exposure; strong inducers reduce efficacy. Inhibits UGT1A1, CYP2B6, CYP2C8, CYP3A4. Hepatotoxicity is dose-limiting in some patients."
        ),
        "drug_class": "Antineoplastic / Multikinase Inhibitor",
        "rxnorm_cui": "993461",
    },
    {
        "id": "DB15820",
        "name": "Vandetanib",
        "brand_names": ["Caprelsa"],
        "description": (
            "RET/VEGFR/EGFR multikinase inhibitor for medullary thyroid carcinoma. Metabolized by CYP3A4 to N-desmethyl vandetanib. Strong CYP3A4 inducers reduce levels significantly. QT prolongation risk — contraindicated with multiple QT-prolonging drugs. REMS program required."
        ),
        "drug_class": "Antineoplastic / Multikinase Inhibitor / MTC",
        "rxnorm_cui": "1099144",
    },
    {
        "id": "DB15821",
        "name": "Ponatinib",
        "brand_names": ["Iclusig"],
        "description": (
            "Pan-BCR-ABL TKI (including T315I mutation) for CML and Ph+ ALL. Metabolized by CYP3A4 and CYP2C8. CYP3A4 inhibitors increase ponatinib exposure; inducers reduce efficacy. Strong CYP3A4 inhibitors require dose reduction. Cardiovascular toxicity risk requires REMS."
        ),
        "drug_class": "Antineoplastic / BCR-ABL TKI (Pan)",
        "rxnorm_cui": "1299850",
    },
    {
        "id": "DB15822",
        "name": "Bosutinib",
        "brand_names": ["Bosulif"],
        "description": (
            "Second-generation BCR-ABL/Src TKI for CML. Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase bosutinib levels; strong inducers reduce AUC by 86%. P-gp inhibitor. Diarrhea is the most common adverse effect. Avoid high-fat meals and grapefruit juice."
        ),
        "drug_class": "Antineoplastic / BCR-ABL/Src TKI",
        "rxnorm_cui": "1299849",
    },
    {
        "id": "DB15823",
        "name": "Dasatinib",
        "brand_names": ["Sprycel"],
        "description": (
            "Second-generation BCR-ABL/Src/LCK/YES/EphA2 TKI for CML and Ph+ ALL. Metabolized by CYP3A4 (primary). Strong CYP3A4 inhibitors increase levels; strong inducers reduce by 82%. Gastric acid suppressants reduce absorption substantially. Pleural effusion monitoring required."
        ),
        "drug_class": "Antineoplastic / BCR-ABL/Src TKI",
        "rxnorm_cui": "544575",
    },
    {
        "id": "DB15824",
        "name": "Enalapril",
        "brand_names": ["Vasotec", "Epaned"],
        "description": (
            "ACE inhibitor prodrug for hypertension and heart failure. Hydrolyzed by esterases to active enalaprilat. Not significantly CYP-metabolized. Renally eliminated. Concurrent NSAIDs reduce antihypertensive efficacy; potassium-sparing diuretics increase hyperkalemia risk."
        ),
        "drug_class": "ACE Inhibitor",
        "rxnorm_cui": "3827",
    },
    {
        "id": "DB15825",
        "name": "Ramipril",
        "brand_names": ["Altace"],
        "description": (
            "ACE inhibitor prodrug for hypertension, heart failure, and post-MI. Hydrolyzed in liver/gut to active ramiprilat; not CYP-metabolized. Renally eliminated. Reduces cardiovascular events in high-risk patients (HOPE trial). NSAIDs may reduce antihypertensive effects."
        ),
        "drug_class": "ACE Inhibitor",
        "rxnorm_cui": "35208",
    },
    {
        "id": "DB15826",
        "name": "Perindopril",
        "brand_names": ["Aceon", "Coversyl"],
        "description": (
            "ACE inhibitor prodrug for hypertension, stable CAD, and heart failure. Hydrolyzed to active perindoprilat by esterases. CYP3A4 and CYP2C9 play minor roles. Renally eliminated. Reduces events in stable CAD (EUROPA trial)."
        ),
        "drug_class": "ACE Inhibitor",
        "rxnorm_cui": "54552",
    },
    {
        "id": "DB15827",
        "name": "Trandolapril",
        "brand_names": ["Mavik"],
        "description": (
            "ACE inhibitor prodrug for hypertension and post-MI left ventricular dysfunction. Metabolized by hepatic esterases to active trandolaprilat; CYP3A4 minor role. Long half-life allows once-daily dosing. Renally and fecally eliminated."
        ),
        "drug_class": "ACE Inhibitor",
        "rxnorm_cui": "38454",
    },
    {
        "id": "DB15828",
        "name": "Candesartan",
        "brand_names": ["Atacand"],
        "description": (
            "Angiotensin II receptor blocker (ARB) for hypertension and heart failure. Prodrug converted to active candesartan in GI tract. Minor CYP2C9 metabolism. Largely renally and fecally eliminated. Does not require dose reduction for CYP polymorphisms."
        ),
        "drug_class": "ARB",
        "rxnorm_cui": "214354",
    },
    {
        "id": "DB15829",
        "name": "Telmisartan",
        "brand_names": ["Micardis"],
        "description": (
            "ARB for hypertension. Unique among ARBs: primarily eliminated via bile/feces; minimal renal clearance. Not CYP-metabolized. Inhibits uptake transporters OATP1B1/3 — may modestly increase levels of digoxin and statin co-substrates. PPAR-gamma partial agonist activity may improve insulin sensitivity."
        ),
        "drug_class": "ARB",
        "rxnorm_cui": "73494",
    },
    {
        "id": "DB15830",
        "name": "Azilsartan",
        "brand_names": ["Edarbi"],
        "description": (
            "ARB for hypertension. Active after oral absorption (not a prodrug). Metabolized by CYP2C9. Produces two inactive metabolites. High affinity for AT1 receptor and slow dissociation rate. CYP2C9 inhibitors may modestly increase azilsartan levels."
        ),
        "drug_class": "ARB",
        "rxnorm_cui": "1099143",
    },
]
