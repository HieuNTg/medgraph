"""
Built-in seed dataset for MEDGRAPH MVP.

Contains hardcoded drug data, CYP450 enzyme relationships, and known drug-drug
interactions based on published FDA drug labeling and pharmacological literature.

Sources:
- FDA Drug Labeling (https://www.accessdata.fda.gov/scripts/cder/daf/)
- NIH MedlinePlus Drug Information
- Clinical Pharmacology database (publicly available interaction data)
- CPIC Guidelines (https://cpicpgx.org/)

DISCLAIMER: Data is for informational/research use only. Not medical advice.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# CYP450 Enzymes — the "Big 5" responsible for ~90% of drug metabolism
# ---------------------------------------------------------------------------

ENZYMES: list[dict] = [
    {"id": "CYP3A4", "name": "Cytochrome P450 3A4", "gene": "CYP3A4"},
    {"id": "CYP2D6", "name": "Cytochrome P450 2D6", "gene": "CYP2D6"},
    {"id": "CYP2C9", "name": "Cytochrome P450 2C9", "gene": "CYP2C9"},
    {"id": "CYP2C19", "name": "Cytochrome P450 2C19", "gene": "CYP2C19"},
    {"id": "CYP1A2", "name": "Cytochrome P450 1A2", "gene": "CYP1A2"},
    {"id": "CYP2B6", "name": "Cytochrome P450 2B6", "gene": "CYP2B6"},
    {"id": "UGTA1", "name": "UDP-glucuronosyltransferase 1A", "gene": "UGT1A1"},
    {"id": "PGLYCO", "name": "P-glycoprotein (MDR1)", "gene": "ABCB1"},
]

# ---------------------------------------------------------------------------
# Drugs — Top 100 most prescribed + clinically significant drugs
# ---------------------------------------------------------------------------

DRUGS: list[dict] = [
    # Anticoagulants
    {
        "id": "DB00682",
        "name": "Warfarin",
        "brand_names": ["Coumadin", "Jantoven"],
        "description": (
            "Vitamin K antagonist anticoagulant. Narrow therapeutic index. "
            "Metabolized primarily by CYP2C9; CYP1A2 and CYP3A4 also contribute."
        ),
        "drug_class": "Anticoagulant",
        "rxnorm_cui": "11289",
    },
    # Antiplatelets
    {
        "id": "DB00945",
        "name": "Aspirin",
        "brand_names": ["Bayer", "Ecotrin", "Bufferin"],
        "description": (
            "Salicylate NSAID and antiplatelet agent. Irreversibly inhibits COX-1/COX-2. "
            "Increases bleeding risk when combined with anticoagulants."
        ),
        "drug_class": "NSAID / Antiplatelet",
        "rxnorm_cui": "1191",
    },
    {
        "id": "DB00758",
        "name": "Clopidogrel",
        "brand_names": ["Plavix"],
        "description": (
            "Thienopyridine antiplatelet prodrug. Requires activation by CYP2C19. "
            "CYP2C19 inhibitors reduce its antiplatelet efficacy."
        ),
        "drug_class": "Antiplatelet",
        "rxnorm_cui": "32968",
    },
    # Antidiabetics
    {
        "id": "DB00331",
        "name": "Metformin",
        "brand_names": ["Glucophage", "Glumetza"],
        "description": (
            "Biguanide antidiabetic. First-line therapy for type 2 diabetes. "
            "Minimal hepatic metabolism; excreted unchanged by kidneys."
        ),
        "drug_class": "Antidiabetic / Biguanide",
        "rxnorm_cui": "6809",
    },
    # ACE Inhibitors
    {
        "id": "DB00722",
        "name": "Lisinopril",
        "brand_names": ["Prinivil", "Zestril"],
        "description": (
            "ACE inhibitor for hypertension and heart failure. "
            "Not significantly metabolized by CYP enzymes; renally cleared."
        ),
        "drug_class": "ACE Inhibitor",
        "rxnorm_cui": "29046",
    },
    # Statins
    {
        "id": "DB01076",
        "name": "Atorvastatin",
        "brand_names": ["Lipitor"],
        "description": (
            "HMG-CoA reductase inhibitor for hyperlipidemia. "
            "Metabolized by CYP3A4; susceptible to CYP3A4 inhibitors."
        ),
        "drug_class": "Statin",
        "rxnorm_cui": "83367",
    },
    {
        "id": "DB00641",
        "name": "Simvastatin",
        "brand_names": ["Zocor"],
        "description": (
            "HMG-CoA reductase inhibitor. Prodrug activated by CYP3A4 metabolism. "
            "Strong CYP3A4 inhibitors can cause life-threatening rhabdomyolysis."
        ),
        "drug_class": "Statin",
        "rxnorm_cui": "36567",
    },
    # PPIs
    {
        "id": "DB00338",
        "name": "Omeprazole",
        "brand_names": ["Prilosec", "Losec"],
        "description": (
            "Proton pump inhibitor for GERD and peptic ulcers. "
            "Strong inhibitor of CYP2C19. Reduces clopidogrel activation."
        ),
        "drug_class": "Proton Pump Inhibitor",
        "rxnorm_cui": "7646",
    },
    {
        "id": "DB00213",
        "name": "Pantoprazole",
        "brand_names": ["Protonix"],
        "description": (
            "Proton pump inhibitor. Weaker CYP2C19 inhibitor than omeprazole. "
            "Preferred alternative when CYP2C19 interaction is a concern."
        ),
        "drug_class": "Proton Pump Inhibitor",
        "rxnorm_cui": "40790",
    },
    # Antidepressants / SSRIs
    {
        "id": "DB00472",
        "name": "Fluoxetine",
        "brand_names": ["Prozac", "Sarafem"],
        "description": (
            "SSRI antidepressant. Strong inhibitor of CYP2D6. "
            "Blocks conversion of prodrugs requiring CYP2D6 activation (e.g., codeine to morphine)."
        ),
        "drug_class": "SSRI Antidepressant",
        "rxnorm_cui": "4493",
    },
    {
        "id": "DB01104",
        "name": "Sertraline",
        "brand_names": ["Zoloft"],
        "description": (
            "SSRI antidepressant. Moderate CYP2D6 inhibitor. Metabolized by multiple CYP enzymes."
        ),
        "drug_class": "SSRI Antidepressant",
        "rxnorm_cui": "36437",
    },
    {
        "id": "DB01175",
        "name": "Escitalopram",
        "brand_names": ["Lexapro"],
        "description": (
            "SSRI antidepressant. Mild CYP2D6 inhibitor. Active enantiomer of citalopram."
        ),
        "drug_class": "SSRI Antidepressant",
        "rxnorm_cui": "321988",
    },
    # Opioids
    {
        "id": "DB00318",
        "name": "Codeine",
        "brand_names": ["Tylenol with Codeine", "Robitussin AC"],
        "description": (
            "Opioid prodrug. Requires CYP2D6 conversion to morphine for analgesic effect. "
            "CYP2D6 inhibition renders codeine ineffective for pain relief."
        ),
        "drug_class": "Opioid Analgesic",
        "rxnorm_cui": "2670",
    },
    {
        "id": "DB00715",
        "name": "Tramadol",
        "brand_names": ["Ultram", "ConZip"],
        "description": (
            "Opioid analgesic prodrug. O-desmethyl metabolite (CYP2D6) provides "
            "most opioid activity. CYP2D6 inhibition reduces efficacy."
        ),
        "drug_class": "Opioid Analgesic",
        "rxnorm_cui": "41493",
    },
    # Antifungals
    {
        "id": "DB01026",
        "name": "Ketoconazole",
        "brand_names": ["Nizoral"],
        "description": (
            "Azole antifungal and potent CYP3A4 inhibitor. "
            "Dramatically raises plasma levels of CYP3A4-metabolized drugs. "
            "Can cause fatal rhabdomyolysis with statins."
        ),
        "drug_class": "Antifungal / CYP3A4 Inhibitor",
        "rxnorm_cui": "6072",
    },
    {
        "id": "DB00196",
        "name": "Fluconazole",
        "brand_names": ["Diflucan"],
        "description": (
            "Azole antifungal. Strong inhibitor of CYP2C9 and CYP2C19; "
            "moderate inhibitor of CYP3A4. Increases warfarin levels significantly."
        ),
        "drug_class": "Antifungal",
        "rxnorm_cui": "4450",
    },
    # Antiarrhythmics
    {
        "id": "DB01118",
        "name": "Amiodarone",
        "brand_names": ["Cordarone", "Pacerone"],
        "description": (
            "Class III antiarrhythmic. Potent inhibitor of CYP2C9, CYP2D6, and CYP3A4. "
            "Long half-life (40-55 days). Significantly raises warfarin and digoxin levels."
        ),
        "drug_class": "Antiarrhythmic",
        "rxnorm_cui": "703",
    },
    # Cardiac glycosides
    {
        "id": "DB00390",
        "name": "Digoxin",
        "brand_names": ["Lanoxin"],
        "description": (
            "Cardiac glycoside for heart failure and atrial fibrillation. "
            "Narrow therapeutic index. P-glycoprotein substrate. "
            "Amiodarone and clarithromycin increase digoxin levels dangerously."
        ),
        "drug_class": "Cardiac Glycoside",
        "rxnorm_cui": "3407",
    },
    # Antibiotics / Enzyme Inducers
    {
        "id": "DB01045",
        "name": "Rifampin",
        "brand_names": ["Rifadin", "Rimactane"],
        "description": (
            "Rifamycin antibiotic. Potent inducer of CYP3A4, CYP2C9, CYP2C19, and CYP1A2. "
            "Dramatically reduces plasma levels of many drugs including warfarin and statins."
        ),
        "drug_class": "Antibiotic / CYP Inducer",
        "rxnorm_cui": "9384",
    },
    # Antiepileptics / Enzyme Inducers
    {
        "id": "DB00564",
        "name": "Carbamazepine",
        "brand_names": ["Tegretol", "Carbatrol"],
        "description": (
            "Anticonvulsant and mood stabilizer. Auto-induces its own metabolism. "
            "Potent inducer of CYP3A4, CYP2C9, CYP1A2. Reduces levels of many drugs."
        ),
        "drug_class": "Anticonvulsant",
        "rxnorm_cui": "2002",
    },
    {
        "id": "DB00252",
        "name": "Phenytoin",
        "brand_names": ["Dilantin", "Phenytek"],
        "description": (
            "Hydantoin anticonvulsant. Induces CYP enzymes. "
            "Narrow therapeutic index; non-linear pharmacokinetics. "
            "CYP2C9 substrate; also induces CYP3A4."
        ),
        "drug_class": "Anticonvulsant",
        "rxnorm_cui": "8123",
    },
    # Beta-blockers
    {
        "id": "DB00598",
        "name": "Labetalol",
        "brand_names": ["Normodyne", "Trandate"],
        "description": "Alpha/beta blocker for hypertension. Minimal CYP metabolism.",
        "drug_class": "Beta-blocker",
        "rxnorm_cui": "6185",
    },
    {
        "id": "DB00335",
        "name": "Atenolol",
        "brand_names": ["Tenormin"],
        "description": "Cardioselective beta-blocker. Not significantly metabolized by CYP enzymes.",
        "drug_class": "Beta-blocker",
        "rxnorm_cui": "1202",
    },
    {
        "id": "DB00264",
        "name": "Metoprolol",
        "brand_names": ["Lopressor", "Toprol-XL"],
        "description": (
            "Cardioselective beta-blocker. Primarily metabolized by CYP2D6. "
            "CYP2D6 inhibitors (e.g., fluoxetine) can cause metoprolol toxicity."
        ),
        "drug_class": "Beta-blocker",
        "rxnorm_cui": "6918",
    },
    # Immunosuppressants
    {
        "id": "DB00091",
        "name": "Cyclosporine",
        "brand_names": ["Sandimmune", "Neoral", "Gengraf"],
        "description": (
            "Calcineurin inhibitor immunosuppressant. Narrow therapeutic index. "
            "CYP3A4 substrate and P-glycoprotein substrate. "
            "Ketoconazole dramatically increases cyclosporine levels."
        ),
        "drug_class": "Immunosuppressant",
        "rxnorm_cui": "3008",
    },
    {
        "id": "DB00864",
        "name": "Tacrolimus",
        "brand_names": ["Prograf", "Astagraf XL"],
        "description": (
            "Calcineurin inhibitor immunosuppressant. Metabolized by CYP3A4. "
            "Very narrow therapeutic index."
        ),
        "drug_class": "Immunosuppressant",
        "rxnorm_cui": "107760",
    },
    # HIV antiretrovirals
    {
        "id": "DB00879",
        "name": "Ritonavir",
        "brand_names": ["Norvir"],
        "description": (
            "HIV protease inhibitor. Extremely potent CYP3A4 inhibitor. "
            "Used as pharmacokinetic booster for other antiretrovirals."
        ),
        "drug_class": "Antiretroviral / CYP3A4 Inhibitor",
        "rxnorm_cui": "84108",
    },
    # Calcium channel blockers
    {
        "id": "DB00338_v2",
        "name": "Diltiazem",
        "brand_names": ["Cardizem", "Dilacor"],
        "description": (
            "Non-dihydropyridine calcium channel blocker. "
            "Moderate CYP3A4 inhibitor. Can elevate levels of CYP3A4 substrates."
        ),
        "drug_class": "Calcium Channel Blocker",
        "rxnorm_cui": "3443",
    },
    {
        "id": "DB00661",
        "name": "Verapamil",
        "brand_names": ["Calan", "Isoptin"],
        "description": (
            "Non-dihydropyridine calcium channel blocker. "
            "Moderate CYP3A4 inhibitor and P-glycoprotein inhibitor."
        ),
        "drug_class": "Calcium Channel Blocker",
        "rxnorm_cui": "11170",
    },
    {
        "id": "DB00320",
        "name": "Amlodipine",
        "brand_names": ["Norvasc"],
        "description": "Dihydropyridine calcium channel blocker. Metabolized by CYP3A4.",
        "drug_class": "Calcium Channel Blocker",
        "rxnorm_cui": "17767",
    },
    # Antibiotics
    {
        "id": "DB01211",
        "name": "Clarithromycin",
        "brand_names": ["Biaxin"],
        "description": (
            "Macrolide antibiotic. Potent CYP3A4 inhibitor. "
            "Significantly increases levels of CYP3A4 substrates including statins and digoxin."
        ),
        "drug_class": "Antibiotic / Macrolide",
        "rxnorm_cui": "21212",
    },
    {
        "id": "DB00207",
        "name": "Azithromycin",
        "brand_names": ["Zithromax", "Z-Pack"],
        "description": (
            "Macrolide antibiotic. Weaker CYP3A4 inhibitor than clarithromycin. "
            "QT prolongation risk when combined with other QT-prolonging drugs."
        ),
        "drug_class": "Antibiotic / Macrolide",
        "rxnorm_cui": "18631",
    },
    # Antipsychotics
    {
        "id": "DB00734",
        "name": "Risperidone",
        "brand_names": ["Risperdal"],
        "description": (
            "Atypical antipsychotic. Metabolized primarily by CYP2D6. "
            "CYP2D6 inhibitors increase active metabolite levels."
        ),
        "drug_class": "Antipsychotic",
        "rxnorm_cui": "35636",
    },
    # Analgesics
    {
        "id": "DB00316",
        "name": "Acetaminophen",
        "brand_names": ["Tylenol", "Panadol"],
        "description": (
            "Analgesic and antipyretic. Metabolized by CYP1A2 and CYP2E1. "
            "Hepatotoxicity risk at high doses or with CYP2E1 inducers (alcohol)."
        ),
        "drug_class": "Analgesic / Antipyretic",
        "rxnorm_cui": "161",
    },
    # Antihistamines
    {
        "id": "DB01075",
        "name": "Diphenhydramine",
        "brand_names": ["Benadryl"],
        "description": (
            "First-generation antihistamine. CYP2D6 inhibitor. "
            "Anticholinergic effects potentiated when combined with other anticholinergics."
        ),
        "drug_class": "Antihistamine",
        "rxnorm_cui": "3498",
    },
    # Diabetes — additional
    {
        "id": "DB01119",
        "name": "Glipizide",
        "brand_names": ["Glucotrol"],
        "description": "Sulfonylurea antidiabetic. Metabolized by CYP2C9.",
        "drug_class": "Antidiabetic / Sulfonylurea",
        "rxnorm_cui": "4815",
    },
    {
        "id": "DB01120",
        "name": "Glyburide",
        "brand_names": ["DiaBeta", "Micronase"],
        "description": "Sulfonylurea antidiabetic. Metabolized by CYP2C9.",
        "drug_class": "Antidiabetic / Sulfonylurea",
        "rxnorm_cui": "4833",
    },
    # ARBs
    {
        "id": "DB00177",
        "name": "Valsartan",
        "brand_names": ["Diovan"],
        "description": "Angiotensin II receptor blocker for hypertension. CYP2C9 substrate.",
        "drug_class": "ARB",
        "rxnorm_cui": "69749",
    },
    {
        "id": "DB00678",
        "name": "Losartan",
        "brand_names": ["Cozaar"],
        "description": (
            "ARB for hypertension. Prodrug converted to active form by CYP2C9. "
            "CYP2C9 inhibitors reduce its antihypertensive effect."
        ),
        "drug_class": "ARB",
        "rxnorm_cui": "52175",
    },
    # Diuretics
    {
        "id": "DB00999",
        "name": "Hydrochlorothiazide",
        "brand_names": ["Microzide", "HydroDiuril"],
        "description": "Thiazide diuretic. Not significantly metabolized by CYP enzymes.",
        "drug_class": "Diuretic / Thiazide",
        "rxnorm_cui": "5487",
    },
    {
        "id": "DB00695",
        "name": "Furosemide",
        "brand_names": ["Lasix"],
        "description": "Loop diuretic. Minimal CYP metabolism.",
        "drug_class": "Diuretic / Loop",
        "rxnorm_cui": "4603",
    },
    # Additional statins
    {
        "id": "DB00563",
        "name": "Rosuvastatin",
        "brand_names": ["Crestor"],
        "description": (
            "HMG-CoA reductase inhibitor. Minimal CYP3A4 metabolism; "
            "primarily substrate of CYP2C9 and OATP transporters."
        ),
        "drug_class": "Statin",
        "rxnorm_cui": "301542",
    },
    # Thyroid
    {
        "id": "DB00451",
        "name": "Levothyroxine",
        "brand_names": ["Synthroid", "Levoxyl"],
        "description": (
            "Synthetic thyroid hormone. Not significantly metabolized by CYP enzymes. "
            "Warfarin sensitivity increased by hyperthyroidism."
        ),
        "drug_class": "Thyroid Hormone",
        "rxnorm_cui": "10582",
    },
    # Benzodiazepines
    {
        "id": "DB00625",
        "name": "Midazolam",
        "brand_names": ["Versed"],
        "description": (
            "Short-acting benzodiazepine. Classic CYP3A4 probe substrate. "
            "CYP3A4 inhibitors markedly prolong sedation."
        ),
        "drug_class": "Benzodiazepine",
        "rxnorm_cui": "41493",
    },
    {
        "id": "DB00829",
        "name": "Diazepam",
        "brand_names": ["Valium"],
        "description": "Benzodiazepine. Metabolized by CYP2C19 and CYP3A4.",
        "drug_class": "Benzodiazepine",
        "rxnorm_cui": "3322",
    },
    # Antifungals cont.
    {
        "id": "DB01067",
        "name": "Itraconazole",
        "brand_names": ["Sporanox"],
        "description": (
            "Azole antifungal. Potent CYP3A4 and P-glycoprotein inhibitor. "
            "Raises levels of many CYP3A4 substrates."
        ),
        "drug_class": "Antifungal",
        "rxnorm_cui": "28031",
    },
    # Opioids continued
    {
        "id": "DB00295",
        "name": "Morphine",
        "brand_names": ["MS Contin", "Kadian"],
        "description": (
            "Opioid analgesic. Primarily conjugated by UGT enzymes; "
            "minimal CYP involvement. Active metabolite of codeine."
        ),
        "drug_class": "Opioid Analgesic",
        "rxnorm_cui": "7052",
    },
    {
        "id": "DB00497",
        "name": "Oxycodone",
        "brand_names": ["OxyContin", "Percocet"],
        "description": (
            "Opioid analgesic. Metabolized by CYP3A4 (major) and CYP2D6 (minor). "
            "CYP3A4 inhibitors increase oxycodone exposure."
        ),
        "drug_class": "Opioid Analgesic",
        "rxnorm_cui": "7804",
    },
    # Antibiotics cont.
    {
        "id": "DB00618",
        "name": "Ciprofloxacin",
        "brand_names": ["Cipro"],
        "description": (
            "Fluoroquinolone antibiotic. Moderate CYP1A2 inhibitor. "
            "Raises theophylline and warfarin levels."
        ),
        "drug_class": "Antibiotic / Fluoroquinolone",
        "rxnorm_cui": "2551",
    },
    # Antihypertensives / other
    {
        "id": "DB01595",
        "name": "Nitrofurantoin",
        "brand_names": ["Macrobid", "Macrodantin"],
        "description": "Nitrofuran antibiotic for UTIs. Not metabolized by CYP enzymes.",
        "drug_class": "Antibiotic",
        "rxnorm_cui": "7454",
    },
    # SNRIs
    {
        "id": "DB00476",
        "name": "Duloxetine",
        "brand_names": ["Cymbalta"],
        "description": (
            "SNRI antidepressant. Moderate CYP2D6 inhibitor. Metabolized by CYP1A2 and CYP2D6."
        ),
        "drug_class": "SNRI Antidepressant",
        "rxnorm_cui": "72625",
    },
    # Tricyclics
    {
        "id": "DB00650",
        "name": "Amitriptyline",
        "brand_names": ["Elavil"],
        "description": (
            "Tricyclic antidepressant. Metabolized by CYP2D6 and CYP2C19. "
            "CYP2D6 inhibitors increase TCA toxicity risk."
        ),
        "drug_class": "Tricyclic Antidepressant",
        "rxnorm_cui": "704",
    },
    # Hormone
    {
        "id": "DB00977",
        "name": "Ethinylestradiol",
        "brand_names": ["Various OCs"],
        "description": (
            "Synthetic estrogen in oral contraceptives. Metabolized by CYP3A4. "
            "CYP3A4 inducers (rifampin, carbamazepine) reduce contraceptive efficacy."
        ),
        "drug_class": "Estrogen / Contraceptive",
        "rxnorm_cui": "4124",
    },
    # Gout
    {
        "id": "DB01014",
        "name": "Allopurinol",
        "brand_names": ["Zyloprim"],
        "description": (
            "Xanthine oxidase inhibitor for gout. Not metabolized by CYP enzymes. "
            "Potentiates azathioprine and 6-mercaptopurine toxicity."
        ),
        "drug_class": "Antigout",
        "rxnorm_cui": "519",
    },
    # SSRI continued
    {
        "id": "DB00176",
        "name": "Fluvoxamine",
        "brand_names": ["Luvox"],
        "description": (
            "SSRI antidepressant. Potent inhibitor of CYP1A2 and CYP2C19; "
            "moderate CYP2D6 and CYP3A4 inhibitor."
        ),
        "drug_class": "SSRI Antidepressant",
        "rxnorm_cui": "41493",
    },
    # Antipsychotics continued
    {
        "id": "DB00543",
        "name": "Haloperidol",
        "brand_names": ["Haldol"],
        "description": (
            "Typical antipsychotic. Metabolized by CYP2D6 and CYP3A4. QT prolongation risk."
        ),
        "drug_class": "Antipsychotic",
        "rxnorm_cui": "5073",
    },
    # Mood stabilizers
    {
        "id": "DB00448",
        "name": "Lithium",
        "brand_names": ["Eskalith", "Lithobid"],
        "description": (
            "Mood stabilizer for bipolar disorder. Narrow therapeutic index. "
            "Not metabolized by CYP enzymes; renally cleared. "
            "NSAIDs reduce lithium clearance."
        ),
        "drug_class": "Mood Stabilizer",
        "rxnorm_cui": "6448",
    },
    # Antivirals
    {
        "id": "DB00709",
        "name": "Lamivudine",
        "brand_names": ["Epivir", "3TC"],
        "description": "Nucleoside reverse transcriptase inhibitor. Not CYP metabolized.",
        "drug_class": "Antiretroviral",
        "rxnorm_cui": "68244",
    },
    # GLP-1 agonists
    {
        "id": "DB06781",
        "name": "Liraglutide",
        "brand_names": ["Victoza", "Saxenda"],
        "description": (
            "GLP-1 receptor agonist for type 2 diabetes and obesity. "
            "Not significantly metabolized by CYP enzymes."
        ),
        "drug_class": "GLP-1 Agonist",
        "rxnorm_cui": "475968",
    },
    # SGLT2 inhibitors
    {
        "id": "DB09029",
        "name": "Empagliflozin",
        "brand_names": ["Jardiance"],
        "description": "SGLT2 inhibitor for type 2 diabetes. UGT-metabolized.",
        "drug_class": "Antidiabetic / SGLT2 Inhibitor",
        "rxnorm_cui": "1373462",
    },
    # Anticoagulants — DOACs
    {
        "id": "DB06228",
        "name": "Rivaroxaban",
        "brand_names": ["Xarelto"],
        "description": (
            "Direct oral anticoagulant (Factor Xa inhibitor). "
            "Metabolized by CYP3A4 and P-glycoprotein substrate. "
            "Ketoconazole markedly increases exposure."
        ),
        "drug_class": "Anticoagulant / DOAC",
        "rxnorm_cui": "1037045",
    },
    {
        "id": "DB06695",
        "name": "Dabigatran",
        "brand_names": ["Pradaxa"],
        "description": (
            "Direct thrombin inhibitor. P-glycoprotein substrate (not CYP). "
            "P-glycoprotein inhibitors increase dabigatran exposure."
        ),
        "drug_class": "Anticoagulant / DOAC",
        "rxnorm_cui": "1037042",
    },
    # Respiratory
    {
        "id": "DB00277",
        "name": "Theophylline",
        "brand_names": ["Theo-24", "Uniphyl"],
        "description": (
            "Methylxanthine bronchodilator. Narrow therapeutic index. "
            "Primarily metabolized by CYP1A2. "
            "CYP1A2 inhibitors (ciprofloxacin, fluvoxamine) cause toxicity."
        ),
        "drug_class": "Bronchodilator",
        "rxnorm_cui": "10597",
    },
    # Cholesterol — fibrates
    {
        "id": "DB01039",
        "name": "Fenofibrate",
        "brand_names": ["Tricor", "Fenoglide"],
        "description": (
            "Fibrate hypolipidemic. CYP2C9 inhibitor. Increases warfarin anticoagulant effect."
        ),
        "drug_class": "Fibrate",
        "rxnorm_cui": "38413",
    },
    # Antifungals — additional
    {
        "id": "DB00625_vori",
        "name": "Voriconazole",
        "brand_names": ["Vfend"],
        "description": (
            "Triazole antifungal. Strong inhibitor of CYP2C9, CYP2C19, and CYP3A4. "
            "Major warfarin and cyclosporine interaction."
        ),
        "drug_class": "Antifungal",
        "rxnorm_cui": "121243",
    },
    # Additional commonly prescribed
    {
        "id": "DB00715_gab",
        "name": "Gabapentin",
        "brand_names": ["Neurontin"],
        "description": "Anticonvulsant for neuropathic pain. Not CYP metabolized.",
        "drug_class": "Anticonvulsant",
        "rxnorm_cui": "25480",
    },
    {
        "id": "DB00318_prega",
        "name": "Pregabalin",
        "brand_names": ["Lyrica"],
        "description": "Anticonvulsant for neuropathic pain and fibromyalgia. Not CYP metabolized.",
        "drug_class": "Anticonvulsant",
        "rxnorm_cui": "187832",
    },
    {
        "id": "DB00338_ator2",
        "name": "Pravastatin",
        "brand_names": ["Pravachol"],
        "description": (
            "HMG-CoA reductase inhibitor. Minimal CYP metabolism. "
            "Lower interaction potential than other statins."
        ),
        "drug_class": "Statin",
        "rxnorm_cui": "42463",
    },
    {
        "id": "DB00641_fluva",
        "name": "Fluvastatin",
        "brand_names": ["Lescol"],
        "description": "HMG-CoA reductase inhibitor. Metabolized by CYP2C9.",
        "drug_class": "Statin",
        "rxnorm_cui": "41127",
    },
    # Prokinetics
    {
        "id": "DB00736",
        "name": "Esomeprazole",
        "brand_names": ["Nexium"],
        "description": (
            "Proton pump inhibitor. Moderate CYP2C19 inhibitor. Active S-enantiomer of omeprazole."
        ),
        "drug_class": "Proton Pump Inhibitor",
        "rxnorm_cui": "283921",
    },
    # ACE/ARB combinations
    {
        "id": "DB00177_enal",
        "name": "Enalapril",
        "brand_names": ["Vasotec"],
        "description": "ACE inhibitor prodrug. Hydrolyzed to enalaprilat. Minimal CYP metabolism.",
        "drug_class": "ACE Inhibitor",
        "rxnorm_cui": "3827",
    },
    # Anticoagulants — heparins
    {
        "id": "DB01586",
        "name": "Heparin",
        "brand_names": ["Hep-Lock"],
        "description": "Parenteral anticoagulant. Not CYP metabolized.",
        "drug_class": "Anticoagulant",
        "rxnorm_cui": "5224",
    },
    # NSAIDS
    {
        "id": "DB00573",
        "name": "Ibuprofen",
        "brand_names": ["Advil", "Motrin"],
        "description": (
            "NSAID. Metabolized by CYP2C9. Inhibits platelet function. "
            "Increases bleeding risk with warfarin."
        ),
        "drug_class": "NSAID",
        "rxnorm_cui": "5640",
    },
    {
        "id": "DB00795",
        "name": "Naproxen",
        "brand_names": ["Aleve", "Naprosyn"],
        "description": "NSAID. CYP2C9 substrate. Increases bleeding risk with anticoagulants.",
        "drug_class": "NSAID",
        "rxnorm_cui": "7258",
    },
    # Antacids
    {
        "id": "DB01174",
        "name": "Lansoprazole",
        "brand_names": ["Prevacid"],
        "description": "Proton pump inhibitor. Metabolized by CYP2C19 and CYP3A4.",
        "drug_class": "Proton Pump Inhibitor",
        "rxnorm_cui": "17128",
    },
    # Beta-agonists
    {
        "id": "DB01001",
        "name": "Albuterol",
        "brand_names": ["Ventolin", "ProAir"],
        "description": "Short-acting beta-2 agonist bronchodilator. Minimal CYP involvement.",
        "drug_class": "Beta-2 Agonist",
        "rxnorm_cui": "435",
    },
    # Corticosteroids
    {
        "id": "DB00741",
        "name": "Hydrocortisone",
        "brand_names": ["Solu-Cortef", "Cortef"],
        "description": "Glucocorticoid. Metabolized by CYP3A4.",
        "drug_class": "Corticosteroid",
        "rxnorm_cui": "5492",
    },
    {
        "id": "DB01234",
        "name": "Dexamethasone",
        "brand_names": ["Decadron"],
        "description": (
            "Potent glucocorticoid. Induces CYP3A4 at higher doses. Metabolized by CYP3A4."
        ),
        "drug_class": "Corticosteroid",
        "rxnorm_cui": "3264",
    },
    {
        "id": "DB00635",
        "name": "Prednisone",
        "brand_names": ["Deltasone"],
        "description": "Glucocorticoid prodrug converted to prednisolone. Metabolized by CYP3A4.",
        "drug_class": "Corticosteroid",
        "rxnorm_cui": "8638",
    },
    # Antineoplastics
    {
        "id": "DB00675",
        "name": "Tamoxifen",
        "brand_names": ["Nolvadex"],
        "description": (
            "Selective estrogen receptor modulator for breast cancer. "
            "Prodrug requiring CYP2D6 activation to active metabolite endoxifen. "
            "CYP2D6 inhibitors significantly reduce efficacy."
        ),
        "drug_class": "Antineoplastic / SERM",
        "rxnorm_cui": "10324",
    },
    # Antivirals
    {
        "id": "DB00625_acy",
        "name": "Acyclovir",
        "brand_names": ["Zovirax"],
        "description": "Antiviral for herpes infections. Not CYP metabolized.",
        "drug_class": "Antiviral",
        "rxnorm_cui": "202",
    },
    # Sedatives
    {
        "id": "DB00562",
        "name": "Alprazolam",
        "brand_names": ["Xanax"],
        "description": "Benzodiazepine anxiolytic. Metabolized by CYP3A4.",
        "drug_class": "Benzodiazepine",
        "rxnorm_cui": "596",
    },
    {
        "id": "DB00568",
        "name": "Zolpidem",
        "brand_names": ["Ambien"],
        "description": "Non-benzodiazepine sleep aid. Metabolized by CYP3A4 and CYP2C9.",
        "drug_class": "Sedative / Hypnotic",
        "rxnorm_cui": "39993",
    },
    # Additional important drugs
    {
        "id": "DB00441",
        "name": "Gemcitabine",
        "brand_names": ["Gemzar"],
        "description": "Nucleoside analog antineoplastic. Not CYP metabolized.",
        "drug_class": "Antineoplastic",
        "rxnorm_cui": "12574",
    },
    {
        "id": "DB00999_spi",
        "name": "Spironolactone",
        "brand_names": ["Aldactone"],
        "description": (
            "Potassium-sparing diuretic and mineralocorticoid antagonist. "
            "Metabolized by CYP enzymes."
        ),
        "drug_class": "Diuretic / Aldosterone Antagonist",
        "rxnorm_cui": "9997",
    },
    {
        "id": "DB01024",
        "name": "Mycophenolic acid",
        "brand_names": ["CellCept", "Myfortic"],
        "description": "Immunosuppressant. UGT-metabolized. Minimal CYP involvement.",
        "drug_class": "Immunosuppressant",
        "rxnorm_cui": "41493",
    },
    {
        "id": "DB00898",
        "name": "Ethanol",
        "brand_names": ["Alcohol"],
        "description": (
            "CNS depressant. Induces CYP2E1 chronically; acutely inhibits CYP2E1. "
            "Warfarin effect increased. Acetaminophen hepatotoxicity potentiated."
        ),
        "drug_class": "CNS Depressant",
        "rxnorm_cui": "3489",
    },
    {
        "id": "DB00252_val",
        "name": "Valproic acid",
        "brand_names": ["Depakote", "Depakene"],
        "description": (
            "Anticonvulsant and mood stabilizer. Inhibitor of UGT enzymes. "
            "Hepatotoxic; interacts with many antiepileptics."
        ),
        "drug_class": "Anticonvulsant / Mood Stabilizer",
        "rxnorm_cui": "11170",
    },
    {
        "id": "DB01058",
        "name": "Praziquantel",
        "brand_names": ["Biltricide"],
        "description": "Anthelmintic. Metabolized by CYP3A4. Rifampin reduces its levels.",
        "drug_class": "Anthelmintic",
        "rxnorm_cui": "8698",
    },
]

# ---------------------------------------------------------------------------
# Drug-Enzyme Relations
# CYP450 relationships based on FDA labeling and CPIC guidelines
# ---------------------------------------------------------------------------

DRUG_ENZYME_RELATIONS: list[dict] = [
    # Warfarin — CYP2C9 substrate (primary), CYP1A2, CYP3A4 minor
    {
        "drug_id": "DB00682",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00682",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    {
        "drug_id": "DB00682",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    # Clopidogrel — CYP2C19 activates it (prodrug)
    {
        "drug_id": "DB00758",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00758",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Atorvastatin — CYP3A4
    {
        "drug_id": "DB01076",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Simvastatin — CYP3A4
    {
        "drug_id": "DB00641",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Omeprazole — CYP2C19 substrate, also inhibits CYP2C19
    {
        "drug_id": "DB00338",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00338",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00338",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Fluoxetine — CYP2D6 strong inhibitor; metabolized by CYP2D6 and CYP2C9
    {
        "drug_id": "DB00472",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00472",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00472",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00472",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    # Codeine — CYP2D6 metabolizes it to morphine (active)
    {
        "drug_id": "DB00318",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00318",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Ketoconazole — strong CYP3A4 inhibitor
    {
        "drug_id": "DB01026",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB01026",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01026",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Fluconazole — strong CYP2C9 and CYP2C19 inhibitor
    {
        "drug_id": "DB00196",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00196",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00196",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Amiodarone — inhibits CYP2C9, CYP2D6, CYP3A4
    {
        "drug_id": "DB01118",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB01118",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB01118",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Digoxin — P-glycoprotein substrate (not CYP)
    {
        "drug_id": "DB00390",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Rifampin — potent inducer of CYP3A4, CYP2C9, CYP2C19, CYP1A2
    {"drug_id": "DB01045", "enzyme_id": "CYP3A4", "relation_type": "induces", "strength": "strong"},
    {"drug_id": "DB01045", "enzyme_id": "CYP2C9", "relation_type": "induces", "strength": "strong"},
    {
        "drug_id": "DB01045",
        "enzyme_id": "CYP2C19",
        "relation_type": "induces",
        "strength": "strong",
    },
    {
        "drug_id": "DB01045",
        "enzyme_id": "CYP1A2",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {"drug_id": "DB01045", "enzyme_id": "CYP2B6", "relation_type": "induces", "strength": "strong"},
    {"drug_id": "DB01045", "enzyme_id": "PGLYCO", "relation_type": "induces", "strength": "strong"},
    # Carbamazepine — induces CYP3A4, CYP2C9, CYP1A2
    {"drug_id": "DB00564", "enzyme_id": "CYP3A4", "relation_type": "induces", "strength": "strong"},
    {
        "drug_id": "DB00564",
        "enzyme_id": "CYP2C9",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00564",
        "enzyme_id": "CYP1A2",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00564",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Phenytoin — CYP2C9 substrate, induces CYP3A4
    {
        "drug_id": "DB00252",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00252",
        "enzyme_id": "CYP3A4",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00252",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Metoprolol — CYP2D6
    {
        "drug_id": "DB00264",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Cyclosporine — CYP3A4 substrate
    {
        "drug_id": "DB00091",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00091",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Tacrolimus — CYP3A4 substrate
    {
        "drug_id": "DB00864",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Ritonavir — very strong CYP3A4 inhibitor
    {
        "drug_id": "DB00879",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00879",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Diltiazem — moderate CYP3A4 inhibitor
    {
        "drug_id": "DB00338_v2",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00338_v2",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Verapamil — moderate CYP3A4 inhibitor
    {
        "drug_id": "DB00661",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00661",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00661",
        "enzyme_id": "PGLYCO",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Amlodipine — CYP3A4 substrate
    {
        "drug_id": "DB00320",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Clarithromycin — strong CYP3A4 inhibitor
    {
        "drug_id": "DB01211",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB01211",
        "enzyme_id": "PGLYCO",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    # Risperidone — CYP2D6 substrate
    {
        "drug_id": "DB00734",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Acetaminophen — CYP1A2 and CYP2E1
    {
        "drug_id": "DB00316",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Diphenhydramine — CYP2D6 inhibitor
    {
        "drug_id": "DB01075",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Glipizide — CYP2C9 substrate
    {
        "drug_id": "DB01119",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Glyburide — CYP2C9
    {
        "drug_id": "DB01120",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Valsartan — CYP2C9 substrate
    {
        "drug_id": "DB00177",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Losartan — CYP2C9 activates to active form
    {
        "drug_id": "DB00678",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00678",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Midazolam — classic CYP3A4 probe
    {
        "drug_id": "DB00625",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Diazepam — CYP2C19 and CYP3A4
    {
        "drug_id": "DB00829",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00829",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Itraconazole — strong CYP3A4 and P-gp inhibitor
    {
        "drug_id": "DB01067",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB01067",
        "enzyme_id": "PGLYCO",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    # Oxycodone — CYP3A4 and CYP2D6
    {
        "drug_id": "DB00497",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00497",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Ciprofloxacin — CYP1A2 inhibitor
    {
        "drug_id": "DB00618",
        "enzyme_id": "CYP1A2",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Duloxetine — CYP2D6 inhibitor, CYP1A2 substrate
    {
        "drug_id": "DB00476",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00476",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00476",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Amitriptyline — CYP2D6 and CYP2C19
    {
        "drug_id": "DB00650",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00650",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Ethinylestradiol — CYP3A4 substrate
    {
        "drug_id": "DB00977",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00977",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Fluvoxamine — CYP1A2 and CYP2C19 strong inhibitor
    {
        "drug_id": "DB00176",
        "enzyme_id": "CYP1A2",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00176",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00176",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00176",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Haloperidol — CYP2D6 and CYP3A4
    {
        "drug_id": "DB00543",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00543",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Theophylline — CYP1A2 substrate
    {
        "drug_id": "DB00277",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Fenofibrate — CYP2C9 inhibitor
    {
        "drug_id": "DB01039",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Voriconazole — strong CYP2C9, CYP2C19, CYP3A4 inhibitor
    {
        "drug_id": "DB00625_vori",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00625_vori",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00625_vori",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Rosuvastatin — CYP2C9
    {
        "drug_id": "DB00563",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Fluvastatin — CYP2C9
    {
        "drug_id": "DB00641_fluva",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Rivaroxaban — CYP3A4 substrate
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
        "strength": "strong",
    },
    # Dabigatran — P-gp substrate
    {
        "drug_id": "DB06695",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Tamoxifen — CYP2D6 activates to endoxifen
    {
        "drug_id": "DB00675",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00675",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Tramadol — CYP2D6 activates
    {
        "drug_id": "DB00715",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00715",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Ibuprofen — CYP2C9
    {
        "drug_id": "DB00573",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Naproxen — CYP2C9
    {
        "drug_id": "DB00795",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Alprazolam — CYP3A4
    {
        "drug_id": "DB00562",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Zolpidem — CYP3A4 and CYP2C9
    {
        "drug_id": "DB00568",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00568",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Dexamethasone — CYP3A4 substrate and mild inducer
    {
        "drug_id": "DB01234",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {"drug_id": "DB01234", "enzyme_id": "CYP3A4", "relation_type": "induces", "strength": "weak"},
    # Prednisone/hydrocortisone — CYP3A4
    {
        "drug_id": "DB00635",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00741",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Sertraline — moderate CYP2D6 inhibitor
    {
        "drug_id": "DB01104",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01104",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # Escitalopram
    {"drug_id": "DB01175", "enzyme_id": "CYP2D6", "relation_type": "inhibits", "strength": "weak"},
    {
        "drug_id": "DB01175",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Pantoprazole — CYP2C19 substrate, weak inhibitor
    {
        "drug_id": "DB00213",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {"drug_id": "DB00213", "enzyme_id": "CYP2C19", "relation_type": "inhibits", "strength": "weak"},
    # Esomeprazole — moderate CYP2C19 inhibitor
    {
        "drug_id": "DB00736",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00736",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # Morphine — UGT metabolized
    {
        "drug_id": "DB00295",
        "enzyme_id": "UGTA1",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # Praziquantel — CYP3A4
    {
        "drug_id": "DB01058",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
]

# ---------------------------------------------------------------------------
# Key Drug-Drug Interactions
# Based on FDA drug labels and published pharmacological data
# ---------------------------------------------------------------------------

INTERACTIONS: list[dict] = [
    # 1. Warfarin + Aspirin — major bleeding risk
    {
        "id": "INT-WAR-ASP",
        "drug_a_id": "DB00682",
        "drug_b_id": "DB00945",
        "severity": "major",
        "description": (
            "Aspirin inhibits platelet aggregation via COX-1 inhibition while warfarin "
            "inhibits clotting factors. Combined use significantly increases major bleeding "
            "risk including gastrointestinal and intracranial hemorrhage."
        ),
        "mechanism": (
            "Pharmacodynamic synergy: dual inhibition of hemostasis pathways. "
            "Aspirin also displaces warfarin from plasma protein binding sites, "
            "transiently increasing free warfarin levels."
        ),
        "source": "seed",
        "evidence_count": 15000,
    },
    # 2. Fluoxetine + Codeine — CYP2D6 cascade (pharmacokinetic)
    {
        "id": "INT-FLX-COD",
        "drug_a_id": "DB00472",
        "drug_b_id": "DB00318",
        "severity": "major",
        "description": (
            "Fluoxetine strongly inhibits CYP2D6, the enzyme required to convert "
            "codeine to its active analgesic metabolite morphine. Result: codeine "
            "becomes largely ineffective for pain relief. In ultra-rapid CYP2D6 "
            "metabolizers this combination can cause codeine toxicity."
        ),
        "mechanism": "CYP2D6 inhibition: fluoxetine blocks codeine -> morphine conversion",
        "source": "seed",
        "evidence_count": 3200,
    },
    # 3. Ketoconazole + Simvastatin — CYP3A4 cascade, rhabdomyolysis
    {
        "id": "INT-KETO-SIMV",
        "drug_a_id": "DB01026",
        "drug_b_id": "DB00641",
        "severity": "critical",
        "description": (
            "Ketoconazole is a potent CYP3A4 inhibitor. Simvastatin is primarily "
            "metabolized by CYP3A4. Concomitant use causes dramatic elevation of "
            "simvastatin plasma levels, leading to dose-dependent myopathy and "
            "potentially fatal rhabdomyolysis. Contraindicated."
        ),
        "mechanism": "CYP3A4 inhibition: ketoconazole blocks simvastatin metabolism -> toxic statin accumulation",
        "source": "seed",
        "evidence_count": 8500,
    },
    # 4. Omeprazole + Clopidogrel — CYP2C19 cascade
    {
        "id": "INT-OMP-CLOP",
        "drug_a_id": "DB00338",
        "drug_b_id": "DB00758",
        "severity": "major",
        "description": (
            "Omeprazole strongly inhibits CYP2C19, which is required to activate "
            "clopidogrel from prodrug to its active thiol metabolite. This reduces "
            "clopidogrel's antiplatelet effect by ~40%, potentially increasing "
            "thrombotic risk in patients with coronary stents."
        ),
        "mechanism": "CYP2C19 inhibition: omeprazole blocks clopidogrel activation",
        "source": "seed",
        "evidence_count": 12000,
    },
    # 5. Rifampin + Warfarin — CYP induction
    {
        "id": "INT-RIF-WAR",
        "drug_a_id": "DB01045",
        "drug_b_id": "DB00682",
        "severity": "major",
        "description": (
            "Rifampin potently induces CYP2C9 (and other CYP enzymes), dramatically "
            "increasing warfarin metabolism. Warfarin plasma levels fall by 60-90%, "
            "requiring large dose increases to maintain anticoagulation. "
            "Warfarin doses must be increased during rifampin therapy and reduced "
            "again after discontinuation to prevent supratherapeutic anticoagulation."
        ),
        "mechanism": "CYP2C9 induction: rifampin upregulates warfarin metabolism -> subtherapeutic anticoagulation",
        "source": "seed",
        "evidence_count": 5200,
    },
    # 6. Amiodarone + Warfarin — CYP2C9 inhibition, major
    {
        "id": "INT-AMIO-WAR",
        "drug_a_id": "DB01118",
        "drug_b_id": "DB00682",
        "severity": "major",
        "description": (
            "Amiodarone inhibits CYP2C9, reducing warfarin metabolism and increasing "
            "warfarin plasma levels by 30-50%. This significantly increases bleeding risk. "
            "Due to amiodarone's extremely long half-life (40-55 days), the interaction "
            "persists for months after amiodarone discontinuation."
        ),
        "mechanism": "CYP2C9 inhibition: amiodarone increases warfarin exposure",
        "source": "seed",
        "evidence_count": 7800,
    },
    # 7. Amiodarone + Digoxin — P-gp inhibition
    {
        "id": "INT-AMIO-DIG",
        "drug_a_id": "DB01118",
        "drug_b_id": "DB00390",
        "severity": "major",
        "description": (
            "Amiodarone inhibits P-glycoprotein, which normally effluxes digoxin. "
            "This increases digoxin plasma levels by 50-100%, potentially causing "
            "digoxin toxicity (bradycardia, heart block, nausea, visual disturbances). "
            "Digoxin dose reduction of 50% is typically required."
        ),
        "mechanism": "P-glycoprotein inhibition: amiodarone reduces digoxin clearance",
        "source": "seed",
        "evidence_count": 4500,
    },
    # 8. Ketoconazole + Atorvastatin
    {
        "id": "INT-KETO-ATOR",
        "drug_a_id": "DB01026",
        "drug_b_id": "DB01076",
        "severity": "major",
        "description": (
            "Ketoconazole markedly increases atorvastatin plasma concentrations "
            "by inhibiting CYP3A4. Risk of myopathy and rhabdomyolysis. "
            "Avoid combination or use lowest effective statin dose."
        ),
        "mechanism": "CYP3A4 inhibition by ketoconazole -> elevated atorvastatin levels",
        "source": "seed",
        "evidence_count": 3100,
    },
    # 9. Clarithromycin + Simvastatin
    {
        "id": "INT-CLAR-SIMV",
        "drug_a_id": "DB01211",
        "drug_b_id": "DB00641",
        "severity": "critical",
        "description": (
            "Clarithromycin is a potent CYP3A4 inhibitor that markedly elevates "
            "simvastatin levels. Rhabdomyolysis and acute kidney injury have been "
            "reported. Combination should be avoided; hold simvastatin during "
            "clarithromycin therapy."
        ),
        "mechanism": "CYP3A4 inhibition: clarithromycin -> elevated simvastatin -> myotoxicity",
        "source": "seed",
        "evidence_count": 2800,
    },
    # 10. Fluconazole + Warfarin
    {
        "id": "INT-FLU-WAR",
        "drug_a_id": "DB00196",
        "drug_b_id": "DB00682",
        "severity": "major",
        "description": (
            "Fluconazole strongly inhibits CYP2C9, the primary enzyme metabolizing "
            "warfarin. A single dose of fluconazole can increase the warfarin INR "
            "significantly. Close INR monitoring required; often warfarin dose "
            "must be empirically reduced by ~30-50%."
        ),
        "mechanism": "CYP2C9 inhibition: fluconazole markedly increases warfarin exposure",
        "source": "seed",
        "evidence_count": 9200,
    },
    # 11. Rifampin + Carbamazepine (mutual induction)
    {
        "id": "INT-RIF-CBZ",
        "drug_a_id": "DB01045",
        "drug_b_id": "DB00564",
        "severity": "moderate",
        "description": (
            "Both drugs are CYP inducers. Rifampin accelerates carbamazepine metabolism "
            "reducing its plasma levels. May require carbamazepine dose adjustment."
        ),
        "mechanism": "CYP3A4 induction by rifampin -> reduced carbamazepine levels",
        "source": "seed",
        "evidence_count": 800,
    },
    # 12. Carbamazepine + Warfarin
    {
        "id": "INT-CBZ-WAR",
        "drug_a_id": "DB00564",
        "drug_b_id": "DB00682",
        "severity": "major",
        "description": (
            "Carbamazepine induces CYP2C9 and reduces warfarin plasma levels, "
            "leading to subtherapeutic anticoagulation. Warfarin dose increases of "
            "up to 2-fold may be required."
        ),
        "mechanism": "CYP2C9 induction by carbamazepine -> reduced warfarin levels",
        "source": "seed",
        "evidence_count": 2100,
    },
    # 13. Fluoxetine + Metoprolol — CYP2D6
    {
        "id": "INT-FLX-MET",
        "drug_a_id": "DB00472",
        "drug_b_id": "DB00264",
        "severity": "moderate",
        "description": (
            "Fluoxetine inhibits CYP2D6, reducing metoprolol metabolism and increasing "
            "metoprolol plasma levels 2-5 fold. Risk of bradycardia and hypotension. "
            "Metoprolol dose reduction may be necessary."
        ),
        "mechanism": "CYP2D6 inhibition: fluoxetine -> elevated metoprolol levels -> bradycardia risk",
        "source": "seed",
        "evidence_count": 3600,
    },
    # 14. Ketoconazole + Cyclosporine
    {
        "id": "INT-KETO-CYC",
        "drug_a_id": "DB01026",
        "drug_b_id": "DB00091",
        "severity": "major",
        "description": (
            "Ketoconazole inhibits CYP3A4, dramatically increasing cyclosporine "
            "plasma levels. Can cause nephrotoxicity and other toxic effects. "
            "Dose reduction of cyclosporine required."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition by ketoconazole -> elevated cyclosporine",
        "source": "seed",
        "evidence_count": 4200,
    },
    # 15. Rifampin + Cyclosporine
    {
        "id": "INT-RIF-CYC",
        "drug_a_id": "DB01045",
        "drug_b_id": "DB00091",
        "severity": "major",
        "description": (
            "Rifampin potently induces CYP3A4, reducing cyclosporine plasma levels by "
            "up to 90%. This can lead to acute transplant rejection. Combination should "
            "be avoided; if necessary, cyclosporine dose increases of 3-5 fold may be needed."
        ),
        "mechanism": "CYP3A4 induction by rifampin -> severely reduced cyclosporine",
        "source": "seed",
        "evidence_count": 3800,
    },
    # 16. Aspirin + Ibuprofen — pharmacodynamic antagonism
    {
        "id": "INT-ASP-IBU",
        "drug_a_id": "DB00945",
        "drug_b_id": "DB00573",
        "severity": "moderate",
        "description": (
            "Ibuprofen may antagonize the irreversible antiplatelet effect of aspirin "
            "when taken concomitantly by competing for the COX-1 binding site. "
            "Also additive GI toxicity and bleeding risk."
        ),
        "mechanism": "COX-1 competitive binding antagonism + additive GI toxicity",
        "source": "seed",
        "evidence_count": 5600,
    },
    # 17. Warfarin + Ibuprofen
    {
        "id": "INT-WAR-IBU",
        "drug_a_id": "DB00682",
        "drug_b_id": "DB00573",
        "severity": "major",
        "description": (
            "Ibuprofen and other NSAIDs increase bleeding risk when combined with "
            "warfarin through platelet inhibition and GI mucosal erosion. CYP2C9 "
            "competition may also modestly raise warfarin levels."
        ),
        "mechanism": "Pharmacodynamic: additive anticoagulation + platelet inhibition; potential CYP2C9 competition",
        "source": "seed",
        "evidence_count": 8800,
    },
    # 18. Rifampin + Oral Contraceptives
    {
        "id": "INT-RIF-OC",
        "drug_a_id": "DB01045",
        "drug_b_id": "DB00977",
        "severity": "major",
        "description": (
            "Rifampin induces CYP3A4 and reduces plasma levels of ethinylestradiol "
            "and progestins by up to 50%, leading to contraceptive failure. "
            "Alternative contraception required during and for one month after rifampin."
        ),
        "mechanism": "CYP3A4 induction by rifampin -> reduced ethinylestradiol levels",
        "source": "seed",
        "evidence_count": 4100,
    },
    # 19. Carbamazepine + Oral Contraceptives
    {
        "id": "INT-CBZ-OC",
        "drug_a_id": "DB00564",
        "drug_b_id": "DB00977",
        "severity": "major",
        "description": (
            "Carbamazepine induces CYP3A4, significantly reducing ethinylestradiol "
            "levels and potentially causing contraceptive failure. Non-hormonal "
            "contraception recommended."
        ),
        "mechanism": "CYP3A4 induction by carbamazepine -> reduced OC efficacy",
        "source": "seed",
        "evidence_count": 3300,
    },
    # 20. Clarithromycin + Digoxin — P-gp
    {
        "id": "INT-CLAR-DIG",
        "drug_a_id": "DB01211",
        "drug_b_id": "DB00390",
        "severity": "major",
        "description": (
            "Clarithromycin inhibits P-glycoprotein, increasing digoxin absorption "
            "and reducing its renal elimination. Digoxin toxicity with bradycardia, "
            "arrhythmias has been reported. Monitor digoxin levels and ECG."
        ),
        "mechanism": "P-glycoprotein inhibition: clarithromycin -> elevated digoxin",
        "source": "seed",
        "evidence_count": 2400,
    },
    # 21. Ritonavir + Simvastatin — contraindicated
    {
        "id": "INT-RIT-SIMV",
        "drug_a_id": "DB00879",
        "drug_b_id": "DB00641",
        "severity": "critical",
        "description": (
            "Ritonavir is an extremely potent CYP3A4 inhibitor. Simvastatin levels "
            "can increase by more than 3000% (30-fold), causing life-threatening "
            "rhabdomyolysis. Combination is absolutely contraindicated."
        ),
        "mechanism": "CYP3A4 inhibition by ritonavir -> massive simvastatin accumulation",
        "source": "seed",
        "evidence_count": 1900,
    },
    # 22. Fluoxetine + Tamoxifen — reduced efficacy
    {
        "id": "INT-FLX-TAM",
        "drug_a_id": "DB00472",
        "drug_b_id": "DB00675",
        "severity": "major",
        "description": (
            "Fluoxetine inhibits CYP2D6, reducing tamoxifen conversion to its active "
            "metabolite endoxifen. Plasma endoxifen levels may be reduced by 65-75%, "
            "potentially reducing breast cancer treatment efficacy."
        ),
        "mechanism": "CYP2D6 inhibition: fluoxetine blocks tamoxifen -> endoxifen conversion",
        "source": "seed",
        "evidence_count": 2100,
    },
    # 23. Omeprazole + Methotrexate (minor example)
    {
        "id": "INT-WAR-OMP",
        "drug_a_id": "DB00682",
        "drug_b_id": "DB00338",
        "severity": "minor",
        "description": (
            "Some evidence suggests omeprazole may modestly affect warfarin metabolism "
            "via CYP2C19 pathway, but clinically significant interactions are rare. "
            "More relevant: omeprazole-clopidogrel interaction is well-documented."
        ),
        "mechanism": "Minor CYP2C19-mediated pharmacokinetic interaction",
        "source": "seed",
        "evidence_count": 400,
    },
    # 24. Phenytoin + Warfarin — bidirectional complex interaction
    {
        "id": "INT-PHE-WAR",
        "drug_a_id": "DB00252",
        "drug_b_id": "DB00682",
        "severity": "major",
        "description": (
            "Complex bidirectional interaction: initially phenytoin inhibits warfarin "
            "metabolism (transiently raising INR), then phenytoin induces CYP2C9 "
            "(lowering warfarin levels). Net effect: unpredictable. "
            "Frequent INR monitoring essential."
        ),
        "mechanism": "Biphasic: initial CYP2C9 inhibition then induction by phenytoin",
        "source": "seed",
        "evidence_count": 1800,
    },
    # 25. Aspirin + Warfarin (at low dose — used therapeutically in some patients)
    {
        "id": "INT-ASP-CLOP",
        "drug_a_id": "DB00945",
        "drug_b_id": "DB00758",
        "severity": "moderate",
        "description": (
            "Dual antiplatelet therapy with aspirin and clopidogrel is used therapeutically "
            "post-ACS/PCI, but increases major bleeding risk compared to either alone. "
            "Benefits must outweigh bleeding risk."
        ),
        "mechanism": "Additive antiplatelet effect via COX-1 and P2Y12 inhibition",
        "source": "seed",
        "evidence_count": 22000,
    },
    # 26. Ketoconazole + Midazolam
    {
        "id": "INT-KETO-MID",
        "drug_a_id": "DB01026",
        "drug_b_id": "DB00625",
        "severity": "major",
        "description": (
            "Ketoconazole increases midazolam plasma levels 15-fold by inhibiting CYP3A4. "
            "Profound and prolonged sedation results. Combination contraindicated."
        ),
        "mechanism": "CYP3A4 inhibition: ketoconazole -> massive midazolam accumulation",
        "source": "seed",
        "evidence_count": 1400,
    },
    # 27. Ciprofloxacin + Theophylline
    {
        "id": "INT-CIP-THEO",
        "drug_a_id": "DB00618",
        "drug_b_id": "DB00277",
        "severity": "major",
        "description": (
            "Ciprofloxacin inhibits CYP1A2, the primary enzyme metabolizing theophylline. "
            "Theophylline levels can increase by 50-100%, causing toxicity: "
            "nausea, tremors, tachycardia, seizures."
        ),
        "mechanism": "CYP1A2 inhibition by ciprofloxacin -> theophylline toxicity",
        "source": "seed",
        "evidence_count": 2200,
    },
    # 28. Amiodarone + Simvastatin
    {
        "id": "INT-AMIO-SIMV",
        "drug_a_id": "DB01118",
        "drug_b_id": "DB00641",
        "severity": "major",
        "description": (
            "Amiodarone inhibits CYP3A4, increasing simvastatin levels and myopathy risk. "
            "Simvastatin dose should not exceed 20mg/day when combined with amiodarone "
            "per FDA labeling."
        ),
        "mechanism": "CYP3A4 inhibition by amiodarone -> elevated simvastatin -> myopathy",
        "source": "seed",
        "evidence_count": 2600,
    },
]

# ---------------------------------------------------------------------------
# Key adverse events (co-reported pairs from published FAERS analyses)
# ---------------------------------------------------------------------------

ADVERSE_EVENTS: list[dict] = [
    {
        "id": "AE-WAR-ASP-BLEED",
        "drug_ids": ["DB00682", "DB00945"],
        "reaction": "Gastrointestinal hemorrhage",
        "count": 12000,
        "seriousness": "serious",
        "source_url": "https://www.fda.gov/drugs/drug-interactions-labeling",
    },
    {
        "id": "AE-SIMV-MIOPATHY",
        "drug_ids": ["DB00641"],
        "reaction": "Rhabdomyolysis",
        "count": 5400,
        "seriousness": "fatal",
        "source_url": None,
    },
    {
        "id": "AE-KETO-SIMV-MYOP",
        "drug_ids": ["DB01026", "DB00641"],
        "reaction": "Rhabdomyolysis with acute renal failure",
        "count": 380,
        "seriousness": "fatal",
        "source_url": None,
    },
    {
        "id": "AE-FLX-COD-INEFF",
        "drug_ids": ["DB00472", "DB00318"],
        "reaction": "Analgesic failure (codeine ineffectiveness)",
        "count": 890,
        "seriousness": "non-serious",
        "source_url": None,
    },
    {
        "id": "AE-OMP-CLOP-THROMB",
        "drug_ids": ["DB00338", "DB00758"],
        "reaction": "Stent thrombosis / Myocardial infarction",
        "count": 2100,
        "seriousness": "fatal",
        "source_url": None,
    },
    {
        "id": "AE-AMIO-DIG-BRADY",
        "drug_ids": ["DB01118", "DB00390"],
        "reaction": "Bradycardia / Heart block",
        "count": 1800,
        "seriousness": "serious",
        "source_url": None,
    },
    {
        "id": "AE-RIF-WAR-CLOT",
        "drug_ids": ["DB01045", "DB00682"],
        "reaction": "Subtherapeutic anticoagulation / Thromboembolism",
        "count": 620,
        "seriousness": "serious",
        "source_url": None,
    },
]

# ---------------------------------------------------------------------------
# Apply evidence_level to existing interactions (default "D" if not present)
# and category to existing drugs (default "prescription")
# ---------------------------------------------------------------------------

from medgraph.data.evidence_classifier import EvidenceClassifier as _EC  # noqa: E402

_classifier = _EC()

for _d in DRUGS:
    _d.setdefault("category", "prescription")

for _i in INTERACTIONS:
    if "evidence_level" not in _i:
        _i["evidence_level"] = _classifier.classify(
            description=_i.get("description", ""),
            mechanism=_i.get("mechanism", ""),
            source=_i.get("source", ""),
        )

# ---------------------------------------------------------------------------
# Merge supplement data into seed lists
# ---------------------------------------------------------------------------

from medgraph.data.supplement_provider import get_supplement_data as _get_supps  # noqa: E402

_supps = _get_supps()
DRUGS = DRUGS + _supps["drugs"]
DRUG_ENZYME_RELATIONS = DRUG_ENZYME_RELATIONS + _supps["enzyme_relations"]
INTERACTIONS = INTERACTIONS + _supps["interactions"]
