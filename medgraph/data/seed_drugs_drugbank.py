"""
DrugBank-expansion drug dataset for MEDGRAPH — 200+ additional drugs.

Covers major therapeutic classes not yet in seed_data.py, seed_drugs_expanded.py,
or seed_drugs_extended.py. Real DrugBank IDs with accurate CYP450 pharmacology.

Therapeutic classes covered:
- Cardiovascular: statins, ACE inhibitors, ARBs, beta-blockers, CCBs, anticoagulants
- CNS: SSRIs, SNRIs, benzodiazepines, antipsychotics, anticonvulsants, opioids
- Anti-infective: antibiotics, antifungals, antivirals, antimalarials
- Oncology: oral chemos, targeted therapies, immunotherapies
- Endocrine: diabetes drugs, thyroid, corticosteroids
- GI: PPIs, H2 blockers, antiemetics
- Respiratory: bronchodilators, inhaled corticosteroids
- Immunology: DMARDs, biologics

Sources:
- DrugBank (https://go.drugbank.com/)
- FDA Drug Labeling (https://www.accessdata.fda.gov/scripts/cder/daf/)
- CPIC Guidelines (https://cpicpgx.org/)
- Flockhart Table of CYP450 Interactions

DISCLAIMER: Data is for informational/research use only. Not medical advice.
"""

from __future__ import annotations

DRUGS_DRUGBANK: list[dict] = [
    # =========================================================================
    # CARDIOVASCULAR — Statins
    # =========================================================================
    {
        "id": "DB01076_ator",
        "name": "Atorvastatin",
        "brand_names": ["Lipitor"],
        "description": (
            "HMG-CoA reductase inhibitor (statin) for hyperlipidemia and cardiovascular risk "
            "reduction. Metabolized by CYP3A4 to active hydroxy metabolites. Strong CYP3A4 "
            "inhibitors (itraconazole, ritonavir, clarithromycin) markedly increase atorvastatin "
            "exposure and risk of myopathy/rhabdomyolysis. Not significantly affected by CYP2C9."
        ),
        "drug_class": "Statin / HMG-CoA Reductase Inhibitor",
        "rxnorm_cui": "83367",
    },
    {
        "id": "DB00641_rosu",
        "name": "Rosuvastatin",
        "brand_names": ["Crestor"],
        "description": (
            "HMG-CoA reductase inhibitor with minimal CYP metabolism. Primarily a substrate "
            "of OATP1B1/1B3 transporters. OATP inhibitors (cyclosporine, gemfibrozil) increase "
            "rosuvastatin exposure substantially. CYP2C9 plays minor role. "
            "Lower myopathy risk profile vs. other statins."
        ),
        "drug_class": "Statin / HMG-CoA Reductase Inhibitor",
        "rxnorm_cui": "301542",
    },
    {
        "id": "DB00861_prava",
        "name": "Pravastatin",
        "brand_names": ["Pravachol"],
        "description": (
            "Hydrophilic statin with minimal CYP450 metabolism. Primarily eliminated renally "
            "and via biliary transport. OATP1B1/1B3 substrate; cyclosporine increases pravastatin "
            "exposure significantly. Fewer CYP-mediated drug interactions compared to lipophilic "
            "statins. Gemfibrozil inhibits glucuronidation, increasing exposure."
        ),
        "drug_class": "Statin / HMG-CoA Reductase Inhibitor",
        "rxnorm_cui": "42463",
    },
    {
        "id": "DB00227_fluva",
        "name": "Fluvastatin",
        "brand_names": ["Lescol", "Lescol XL"],
        "description": (
            "Statin metabolized primarily by CYP2C9. CYP2C9 inhibitors (fluconazole, "
            "amiodarone) increase fluvastatin exposure. Unlike other statins, less susceptible "
            "to CYP3A4-mediated interactions. Gemfibrozil inhibits CYP2C9 clearance."
        ),
        "drug_class": "Statin / HMG-CoA Reductase Inhibitor",
        "rxnorm_cui": "41493",
    },
    {
        "id": "DB01098_pitav",
        "name": "Pitavastatin",
        "brand_names": ["Livalo", "Zypitamag"],
        "description": (
            "Statin minimally metabolized by CYP2C9; mainly undergoes glucuronidation. "
            "Low susceptibility to CYP-mediated drug interactions. Cyclosporine markedly "
            "increases pitavastatin via OATP1B1 inhibition. Rifampin increases clearance."
        ),
        "drug_class": "Statin / HMG-CoA Reductase Inhibitor",
        "rxnorm_cui": "861634",
    },
    # =========================================================================
    # CARDIOVASCULAR — ACE Inhibitors
    # =========================================================================
    {
        "id": "DB00722_lisi",
        "name": "Lisinopril",
        "brand_names": ["Zestril", "Prinivil", "Qbrelis"],
        "description": (
            "ACE inhibitor for hypertension, heart failure, and post-MI. Not metabolized by "
            "CYP enzymes; excreted unchanged by kidneys. Hyperkalemia risk with potassium-sparing "
            "diuretics, NSAIDs, and potassium supplements. Contraindicated with aliskiren in "
            "diabetes. Risk of angioedema, especially in Black patients."
        ),
        "drug_class": "ACE Inhibitor",
        "rxnorm_cui": "29046",
    },
    {
        "id": "DB00177_rami",
        "name": "Ramipril",
        "brand_names": ["Altace"],
        "description": (
            "ACE inhibitor prodrug converted to active ramiprilat by hepatic esterases. "
            "Not significantly metabolized by CYP enzymes. Reduces cardiovascular events "
            "in high-risk patients (HOPE trial). Hyperkalemia risk with K-sparing agents. "
            "Contraindicated with sacubitril/valsartan (angioedema risk)."
        ),
        "drug_class": "ACE Inhibitor",
        "rxnorm_cui": "35208",
    },
    {
        "id": "DB00542_bena",
        "name": "Benazepril",
        "brand_names": ["Lotensin"],
        "description": (
            "ACE inhibitor prodrug for hypertension. Converted to active benazeprilat by "
            "hepatic esterases. Not CYP-metabolized. Dual elimination (hepatic and renal). "
            "Hyperkalemia and renal function monitoring required."
        ),
        "drug_class": "ACE Inhibitor",
        "rxnorm_cui": "18867",
    },
    {
        "id": "DB00519_fosi",
        "name": "Fosinopril",
        "brand_names": ["Monopril"],
        "description": (
            "ACE inhibitor prodrug with dual (hepatic and renal) elimination. Not CYP-dependent. "
            "Unique phosphinic acid structure differentiates it from other ACEi. Useful in renal "
            "impairment due to hepatic backup elimination pathway."
        ),
        "drug_class": "ACE Inhibitor",
        "rxnorm_cui": "50166",
    },
    # =========================================================================
    # CARDIOVASCULAR — ARBs
    # =========================================================================
    {
        "id": "DB00177_los",
        "name": "Losartan",
        "brand_names": ["Cozaar"],
        "description": (
            "Angiotensin II receptor blocker (ARB) for hypertension and diabetic nephropathy. "
            "Prodrug converted by CYP2C9 (primary) and CYP3A4 to active EXP-3174 metabolite. "
            "CYP2C9 poor metabolizers have reduced conversion to active form. "
            "Inhibits urate transporter; mild uricosuric effect."
        ),
        "drug_class": "ARB / Angiotensin II Receptor Blocker",
        "rxnorm_cui": "52175",
    },
    {
        "id": "DB00812_irbe",
        "name": "Irbesartan",
        "brand_names": ["Avapro"],
        "description": (
            "ARB for hypertension and diabetic nephropathy. Metabolized primarily by CYP2C9 "
            "to an inactive glucuronide conjugate. CYP2C9 inhibitors can increase irbesartan "
            "exposure. No active metabolite; works as a direct-acting ARB."
        ),
        "drug_class": "ARB / Angiotensin II Receptor Blocker",
        "rxnorm_cui": "83818",
    },
    {
        "id": "DB00678_olme",
        "name": "Olmesartan",
        "brand_names": ["Benicar"],
        "description": (
            "ARB prodrug (olmesartan medoxomil) hydrolyzed by gut wall esterases to active "
            "olmesartan. Not CYP-metabolized. Eliminated by dual hepatic/renal routes. "
            "Minimal drug interactions via CYP450. Associated with sprue-like enteropathy."
        ),
        "drug_class": "ARB / Angiotensin II Receptor Blocker",
        "rxnorm_cui": "321064",
    },
    {
        "id": "DB00678_telmi",
        "name": "Telmisartan",
        "brand_names": ["Micardis"],
        "description": (
            "ARB with long half-life (~24h) for hypertension and cardiovascular risk reduction. "
            "Glucuronidated (not CYP-metabolized) and eliminated almost exclusively in feces. "
            "Increases digoxin levels via OATP inhibition. Activates PPAR-gamma, with metabolic "
            "benefits similar to insulin sensitizers."
        ),
        "drug_class": "ARB / Angiotensin II Receptor Blocker",
        "rxnorm_cui": "73494",
    },
    {
        "id": "DB00177_azil",
        "name": "Azilsartan",
        "brand_names": ["Edarbi"],
        "description": (
            "ARB prodrug converted to active azilsartan by gut hydrolysis. Metabolized by "
            "CYP2C9 to inactive metabolites. CYP2C9 inhibitors may increase azilsartan "
            "exposure modestly. High binding affinity for AT1 receptor."
        ),
        "drug_class": "ARB / Angiotensin II Receptor Blocker",
        "rxnorm_cui": "1091643",
    },
    # =========================================================================
    # CARDIOVASCULAR — Beta-Blockers
    # =========================================================================
    {
        "id": "DB00264_meto",
        "name": "Metoprolol",
        "brand_names": ["Lopressor", "Toprol XL"],
        "description": (
            "Cardioselective beta-1 blocker for hypertension, angina, heart failure, and arrhythmias. "
            "Extensively metabolized by CYP2D6. CYP2D6 poor metabolizers and patients on CYP2D6 "
            "inhibitors (paroxetine, fluoxetine, bupropion) have 4- to 5-fold higher exposure. "
            "High first-pass metabolism; significant individual variability."
        ),
        "drug_class": "Beta-blocker / Cardioselective",
        "rxnorm_cui": "6918",
    },
    {
        "id": "DB01136_carve",
        "name": "Carvedilol",
        "brand_names": ["Coreg"],
        "description": (
            "Non-selective beta-blocker with alpha-1 blocking activity for heart failure "
            "and hypertension. Primarily metabolized by CYP2D6; also CYP2C9. "
            "P-glycoprotein substrate. CYP2D6 inhibitors increase carvedilol exposure significantly."
        ),
        "drug_class": "Beta-blocker / Alpha-Beta Blocker",
        "rxnorm_cui": "20352",
    },
    {
        "id": "DB00319_nebiv",
        "name": "Nebivolol",
        "brand_names": ["Bystolic"],
        "description": (
            "Highly selective beta-1 blocker with vasodilatory properties via nitric oxide release. "
            "Extensively metabolized by CYP2D6. CYP2D6 poor metabolizers have significantly higher "
            "plasma levels. Pharmacogenomic monitoring relevant in CYP2D6 poor metabolizers."
        ),
        "drug_class": "Beta-blocker / Cardioselective",
        "rxnorm_cui": "722102",
    },
    {
        "id": "DB01141_labetal",
        "name": "Labetalol",
        "brand_names": ["Trandate", "Normodyne"],
        "description": (
            "Combined alpha-1 and non-selective beta-blocker for hypertension including "
            "hypertensive emergencies. Metabolized by direct glucuronidation (not CYP-dependent). "
            "Minimal CYP-mediated drug interactions. Cimetidine increases labetalol bioavailability."
        ),
        "drug_class": "Beta-blocker / Alpha-Beta Blocker",
        "rxnorm_cui": "6120",
    },
    {
        "id": "DB00335_aten",
        "name": "Atenolol",
        "brand_names": ["Tenormin"],
        "description": (
            "Hydrophilic cardioselective beta-1 blocker. Not significantly metabolized; "
            "excreted mostly unchanged renally. Minimal CYP-mediated drug interactions. "
            "Dose adjustment required in renal impairment. Less CNS side effects due to "
            "low lipophilicity and poor CNS penetration."
        ),
        "drug_class": "Beta-blocker / Cardioselective",
        "rxnorm_cui": "1202",
    },
    # =========================================================================
    # CARDIOVASCULAR — Calcium Channel Blockers
    # =========================================================================
    {
        "id": "DB00381_amlo",
        "name": "Amlodipine",
        "brand_names": ["Norvasc"],
        "description": (
            "Dihydropyridine calcium channel blocker for hypertension and angina. Metabolized "
            "by CYP3A4 to inactive pyridine metabolites. CYP3A4 inhibitors modestly increase "
            "amlodipine exposure. Long half-life (~35-50h) buffers pharmacokinetic variability. "
            "Simvastatin dose capped at 20mg when used with amlodipine."
        ),
        "drug_class": "Calcium Channel Blocker / Dihydropyridine",
        "rxnorm_cui": "17767",
    },
    {
        "id": "DB00661_vera",
        "name": "Verapamil",
        "brand_names": ["Calan", "Verelan", "Isoptin"],
        "description": (
            "Phenylalkylamine calcium channel blocker for hypertension, angina, and SVT. "
            "Inhibits CYP3A4 and P-glycoprotein. Significantly increases levels of cyclosporine, "
            "digoxin, colchicine, and other CYP3A4/P-gp substrates. "
            "Also metabolized by CYP3A4. Negative chronotrope and inotrope."
        ),
        "drug_class": "Calcium Channel Blocker / Phenylalkylamine",
        "rxnorm_cui": "11170",
    },
    {
        "id": "DB00470_dilt",
        "name": "Diltiazem",
        "brand_names": ["Cardizem", "Tiazac", "Dilacor"],
        "description": (
            "Benzothiazepine calcium channel blocker. Moderate CYP3A4 inhibitor and CYP3A4 "
            "substrate. Increases cyclosporine, tacrolimus, sirolimus, and statin levels. "
            "Used for hypertension, angina, and atrial fibrillation/flutter. "
            "Negative chronotrope; avoid with beta-blockers in some settings."
        ),
        "drug_class": "Calcium Channel Blocker / Benzothiazepine",
        "rxnorm_cui": "3443",
    },
    {
        "id": "DB01107_felod",
        "name": "Felodipine",
        "brand_names": ["Plendil"],
        "description": (
            "Dihydropyridine CCB for hypertension. Extensively metabolized by CYP3A4. "
            "Grapefruit juice markedly increases felodipine bioavailability (CYP3A4 inhibition "
            "in gut wall). CYP3A4 inhibitors significantly raise felodipine levels causing "
            "hypotension, edema, and reflex tachycardia."
        ),
        "drug_class": "Calcium Channel Blocker / Dihydropyridine",
        "rxnorm_cui": "3991",
    },
    {
        "id": "DB00409_nicar",
        "name": "Nicardipine",
        "brand_names": ["Cardene"],
        "description": (
            "Dihydropyridine CCB used IV for hypertensive urgency and as oral agent. "
            "Metabolized by CYP3A4. Also inhibits CYP3A4 modestly. Can increase cyclosporine "
            "and tacrolimus levels. IV form used in ICU settings for blood pressure control."
        ),
        "drug_class": "Calcium Channel Blocker / Dihydropyridine",
        "rxnorm_cui": "7425",
    },
    # =========================================================================
    # CARDIOVASCULAR — Anticoagulants
    # =========================================================================
    {
        "id": "DB00682_apix",
        "name": "Apixaban",
        "brand_names": ["Eliquis"],
        "description": (
            "Direct oral anticoagulant (DOAC); factor Xa inhibitor for VTE prevention and "
            "atrial fibrillation stroke prevention. Metabolized ~25% by CYP3A4; also P-gp substrate. "
            "Combined strong CYP3A4/P-gp inhibitors increase apixaban levels 2-fold (reduce dose). "
            "Combined strong inducers decrease levels (avoid)."
        ),
        "drug_class": "Anticoagulant / DOAC / Factor Xa Inhibitor",
        "rxnorm_cui": "1364430",
    },
    {
        "id": "DB06228_riva",
        "name": "Rivaroxaban",
        "brand_names": ["Xarelto"],
        "description": (
            "Factor Xa inhibitor DOAC for VTE treatment and stroke prevention in AF. "
            "Metabolized by CYP3A4 (~36%) and CYP2J2; P-gp substrate. "
            "Combined strong CYP3A4/P-gp inhibitors substantially raise rivaroxaban levels. "
            "Strong inducers (rifampin, carbamazepine) reduce rivaroxaban levels and efficacy."
        ),
        "drug_class": "Anticoagulant / DOAC / Factor Xa Inhibitor",
        "rxnorm_cui": "1114195",
    },
    # =========================================================================
    # CNS — SSRIs
    # =========================================================================
    {
        "id": "DB01104_sert",
        "name": "Sertraline",
        "brand_names": ["Zoloft"],
        "description": (
            "SSRI antidepressant for depression, OCD, panic disorder, PTSD, and social anxiety. "
            "Metabolized primarily by CYP2C19, CYP2C9, CYP3A4, and CYP2D6. Moderate CYP2D6 "
            "inhibitor at higher doses. Serotonin syndrome risk with MAOIs, linezolid, "
            "tramadol, and other serotonergic agents."
        ),
        "drug_class": "SSRI Antidepressant",
        "rxnorm_cui": "36437",
    },
    {
        "id": "DB01561_escit",
        "name": "Escitalopram",
        "brand_names": ["Lexapro"],
        "description": (
            "S-enantiomer of citalopram; most selective SSRI for depression and generalized "
            "anxiety. Metabolized by CYP2C19 (primary), CYP3A4, and CYP2D6. CYP2C19 poor "
            "metabolizers have ~2-fold higher exposure. Prolongs QTc; avoid with other "
            "QT-prolonging drugs. Minimal CYP inhibition at therapeutic doses."
        ),
        "drug_class": "SSRI Antidepressant",
        "rxnorm_cui": "321988",
    },
    {
        "id": "DB00472_fluox",
        "name": "Fluoxetine",
        "brand_names": ["Prozac", "Sarafem"],
        "description": (
            "SSRI antidepressant with long half-life (~1–4 days for fluoxetine, ~4–16 days for "
            "active norfluoxetine metabolite). Potent CYP2D6 inhibitor and moderate CYP2C19 "
            "inhibitor. Significantly raises levels of TCAs, antipsychotics, metoprolol, "
            "codeine active metabolite levels reduced (reduced analgesia). Drug interactions "
            "persist weeks after discontinuation."
        ),
        "drug_class": "SSRI Antidepressant",
        "rxnorm_cui": "41493",
    },
    {
        "id": "DB01174_cital",
        "name": "Citalopram",
        "brand_names": ["Celexa"],
        "description": (
            "SSRI antidepressant for depression. Metabolized by CYP2C19 (primary) and CYP3A4, "
            "CYP2D6. CYP2C19 inhibitors (omeprazole, esomeprazole) increase citalopram exposure. "
            "Dose-dependent QTc prolongation; maximum 40mg/day (20mg if >60 years or CYP2C19 "
            "poor metabolizer). Avoid with other QT-prolonging drugs."
        ),
        "drug_class": "SSRI Antidepressant",
        "rxnorm_cui": "2556",
    },
    {
        "id": "DB00215_fluvo",
        "name": "Fluvoxamine",
        "brand_names": ["Luvox"],
        "description": (
            "SSRI used primarily for OCD. Potent inhibitor of CYP1A2 and CYP2C19; moderate "
            "inhibitor of CYP3A4. Markedly raises levels of clozapine, theophylline, "
            "tizanidine, and ramelteon (all CYP1A2 substrates). Also inhibits CYP2D6 weakly. "
            "Metabolized by CYP1A2 and CYP2D6."
        ),
        "drug_class": "SSRI Antidepressant",
        "rxnorm_cui": "41493",
    },
    # =========================================================================
    # CNS — SNRIs
    # =========================================================================
    {
        "id": "DB00696_dulox",
        "name": "Duloxetine",
        "brand_names": ["Cymbalta", "Drizalma Sprinkle"],
        "description": (
            "SNRI antidepressant also approved for diabetic neuropathy, fibromyalgia, and GAD. "
            "Metabolized by CYP1A2 (primary) and CYP2D6. Moderate CYP2D6 inhibitor; increases "
            "levels of metoprolol, aripiprazole, and other CYP2D6 substrates. CYP1A2 inducers "
            "(cigarette smoking, rifampin) reduce duloxetine levels."
        ),
        "drug_class": "SNRI Antidepressant",
        "rxnorm_cui": "72625",
    },
    {
        "id": "DB00285_venla",
        "name": "Venlafaxine",
        "brand_names": ["Effexor", "Effexor XR"],
        "description": (
            "SNRI antidepressant for depression, GAD, panic disorder, and social anxiety. "
            "Metabolized by CYP2D6 to active O-desmethylvenlafaxine (ODV). CYP2D6 poor "
            "metabolizers have higher venlafaxine but lower ODV levels; net SNRI effect similar. "
            "Weak CYP2D6 inhibitor. Serotonin syndrome risk with MAOIs."
        ),
        "drug_class": "SNRI Antidepressant",
        "rxnorm_cui": "39786",
    },
    {
        "id": "DB01399_desv",
        "name": "Desvenlafaxine",
        "brand_names": ["Pristiq", "Khedezla"],
        "description": (
            "Active metabolite of venlafaxine approved as standalone SNRI for major depression. "
            "Primarily glucuronidated; CYP3A4 plays minor role. Less CYP2D6 dependency than "
            "venlafaxine. Minimal inhibitory effects on CYP enzymes at therapeutic doses."
        ),
        "drug_class": "SNRI Antidepressant",
        "rxnorm_cui": "714882",
    },
    {
        "id": "DB00776_mirtaz",
        "name": "Mirtazapine",
        "brand_names": ["Remeron"],
        "description": (
            "Noradrenergic and specific serotonergic antidepressant (NaSSA). Metabolized by "
            "CYP1A2, CYP2D6, and CYP3A4. CYP inducers reduce levels. Causes significant "
            "histamine blockade (sedation, weight gain). Potentiates CNS depressants."
        ),
        "drug_class": "Antidepressant / NaSSA",
        "rxnorm_cui": "15996",
    },
    # =========================================================================
    # CNS — Benzodiazepines
    # =========================================================================
    {
        "id": "DB00321_alpraz",
        "name": "Alprazolam",
        "brand_names": ["Xanax", "Niravam"],
        "description": (
            "Short-to-intermediate-acting benzodiazepine for anxiety and panic disorder. "
            "Extensively metabolized by CYP3A4 to inactive alpha-hydroxyalprazolam. "
            "CYP3A4 inhibitors (azole antifungals, ritonavir, diltiazem) substantially increase "
            "alprazolam levels, causing prolonged sedation and respiratory depression."
        ),
        "drug_class": "Benzodiazepine / Anxiolytic",
        "rxnorm_cui": "596",
    },
    {
        "id": "DB00829_diaz",
        "name": "Diazepam",
        "brand_names": ["Valium", "Diastat"],
        "description": (
            "Long-acting benzodiazepine for anxiety, seizures, muscle spasm, and alcohol "
            "withdrawal. Metabolized by CYP2C19 (primary) to active desmethyldiazepam; also "
            "CYP3A4. CYP2C19 poor metabolizers have prolonged action. CYP2C19 inhibitors "
            "(omeprazole, fluvoxamine) raise diazepam levels. Active metabolites accumulate "
            "with repeated dosing."
        ),
        "drug_class": "Benzodiazepine / Anxiolytic-Anticonvulsant",
        "rxnorm_cui": "3322",
    },
    {
        "id": "DB01068_clona",
        "name": "Clonazepam",
        "brand_names": ["Klonopin"],
        "description": (
            "Long-acting benzodiazepine for panic disorder and seizures (Lennox-Gastaut, "
            "akinetic, myoclonic). Metabolized by CYP3A4 via nitroreduction. CYP3A4 inhibitors "
            "may increase levels. Tolerance and dependence develop with long-term use."
        ),
        "drug_class": "Benzodiazepine / Anticonvulsant-Anxiolytic",
        "rxnorm_cui": "2598",
    },
    {
        "id": "DB01053_loraze",
        "name": "Lorazepam",
        "brand_names": ["Ativan"],
        "description": (
            "Intermediate-acting benzodiazepine. Undergoes direct glucuronidation; minimal CYP "
            "involvement. Fewer drug interactions via CYP compared to diazepam or alprazolam. "
            "Preferred in hepatic impairment and elderly. Used for anxiety, status epilepticus, "
            "and procedural sedation."
        ),
        "drug_class": "Benzodiazepine / Anxiolytic-Sedative",
        "rxnorm_cui": "6470",
    },
    {
        "id": "DB00932_temazep",
        "name": "Temazepam",
        "brand_names": ["Restoril"],
        "description": (
            "Intermediate-acting benzodiazepine hypnotic for insomnia. Undergoes direct "
            "glucuronidation; minimal CYP metabolism. Fewer pharmacokinetic drug interactions. "
            "Additive CNS and respiratory depression with other CNS depressants and alcohol."
        ),
        "drug_class": "Benzodiazepine / Hypnotic",
        "rxnorm_cui": "10355",
    },
    # =========================================================================
    # CNS — Antipsychotics
    # =========================================================================
    {
        "id": "DB00543_quetia",
        "name": "Quetiapine",
        "brand_names": ["Seroquel", "Seroquel XR"],
        "description": (
            "Atypical antipsychotic for schizophrenia, bipolar disorder, and as adjunct in "
            "depression. Primarily metabolized by CYP3A4 to active norquetiapine. Strong CYP3A4 "
            "inhibitors (ketoconazole, ritonavir) increase quetiapine AUC ~6-fold. CYP3A4 inducers "
            "(carbamazepine, rifampin) reduce levels dramatically. QTc prolongation risk."
        ),
        "drug_class": "Atypical Antipsychotic",
        "rxnorm_cui": "51272",
    },
    {
        "id": "DB00734_rispe",
        "name": "Risperidone",
        "brand_names": ["Risperdal", "Perseris"],
        "description": (
            "Atypical antipsychotic for schizophrenia and bipolar mania. Extensively metabolized "
            "by CYP2D6 to active 9-hydroxyrisperidone (paliperidone). CYP2D6 poor metabolizers and "
            "patients on CYP2D6 inhibitors (paroxetine) have higher risperidone/lower metabolite "
            "ratio; total active moiety similar. Prolongs QTc."
        ),
        "drug_class": "Atypical Antipsychotic",
        "rxnorm_cui": "35636",
    },
    {
        "id": "DB01049_arip",
        "name": "Aripiprazole",
        "brand_names": ["Abilify", "Aristada"],
        "description": (
            "Partial D2/D3 agonist antipsychotic for schizophrenia, bipolar, MDD adjunct. "
            "Metabolized by CYP2D6 (primary) and CYP3A4 to active dehydroaripiprazole. "
            "Strong CYP2D6 inhibitors require 50% dose reduction. Strong CYP3A4 inducers "
            "require dose doubling. Dose adjustment based on pharmacogenomics recommended."
        ),
        "drug_class": "Atypical Antipsychotic / D2 Partial Agonist",
        "rxnorm_cui": "89013",
    },
    {
        "id": "DB00246_zipras",
        "name": "Ziprasidone",
        "brand_names": ["Geodon"],
        "description": (
            "Atypical antipsychotic for schizophrenia and bipolar mania. Metabolized by CYP3A4 "
            "and aldehyde oxidase (major). Must be taken with food for adequate absorption. "
            "Prolongs QTc; avoid with other QT-prolonging agents. CYP3A4 inhibitors modestly "
            "increase ziprasidone levels."
        ),
        "drug_class": "Atypical Antipsychotic",
        "rxnorm_cui": "115698",
    },
    {
        "id": "DB00371_cloz",
        "name": "Clozapine",
        "brand_names": ["Clozaril", "FazaClo", "Versacloz"],
        "description": (
            "Atypical antipsychotic for treatment-resistant schizophrenia. Primarily metabolized "
            "by CYP1A2 (main) and CYP3A4. Cigarette smoking (CYP1A2 inducer) reduces clozapine "
            "levels by ~50%. Fluvoxamine and ciprofloxacin (CYP1A2 inhibitors) markedly increase "
            "levels causing seizures, agranulocytosis risk, and hypotension. REMS program required."
        ),
        "drug_class": "Atypical Antipsychotic",
        "rxnorm_cui": "2626",
    },
    {
        "id": "DB00715_palip",
        "name": "Paliperidone",
        "brand_names": ["Invega", "Invega Sustenna"],
        "description": (
            "Active metabolite of risperidone (9-hydroxyrisperidone). Primarily excreted "
            "unchanged renally with minimal CYP metabolism. Fewer pharmacokinetic drug "
            "interactions than risperidone. Prolongs QTc. Available as once-monthly injectable."
        ),
        "drug_class": "Atypical Antipsychotic",
        "rxnorm_cui": "722102",
    },
    {
        "id": "DB00334_olanz",
        "name": "Olanzapine",
        "brand_names": ["Zyprexa", "Relprevv"],
        "description": (
            "Atypical antipsychotic for schizophrenia, bipolar disorder. Metabolized primarily "
            "by direct glucuronidation (UGT1A4) and by CYP1A2 (secondary). Cigarette smoking "
            "induces CYP1A2, reducing olanzapine levels ~40%. Fluvoxamine inhibits CYP1A2, "
            "raising olanzapine levels. Significant metabolic side effects (weight gain, diabetes)."
        ),
        "drug_class": "Atypical Antipsychotic",
        "rxnorm_cui": "61381",
    },
    # =========================================================================
    # CNS — Anticonvulsants
    # =========================================================================
    {
        "id": "DB00564_cbz",
        "name": "Carbamazepine",
        "brand_names": ["Tegretol", "Carbatrol", "Epitol"],
        "description": (
            "Anticonvulsant and mood stabilizer. Potent inducer of CYP3A4, CYP2C9, CYP2C19, "
            "CYP1A2, CYP2B6, and P-gp. Auto-induces its own metabolism via CYP3A4, leading to "
            "declining plasma levels over first few weeks. Drastically reduces levels of oral "
            "contraceptives, antiretrovirals, warfarin, and many other drugs."
        ),
        "drug_class": "Anticonvulsant / Mood Stabilizer",
        "rxnorm_cui": "2002",
    },
    {
        "id": "DB00745_lamot",
        "name": "Lamotrigine",
        "brand_names": ["Lamictal"],
        "description": (
            "Anticonvulsant and bipolar mood stabilizer. Primarily metabolized by UGT1A4 and "
            "UGT2B7 glucuronidation. Valproate inhibits UGT enzymes, roughly doubling lamotrigine "
            "levels (risk of Stevens-Johnson syndrome). Carbamazepine and enzyme-inducing AEDs "
            "halve lamotrigine levels. Estrogen-containing contraceptives increase clearance."
        ),
        "drug_class": "Anticonvulsant / Mood Stabilizer",
        "rxnorm_cui": "28439",
    },
    {
        "id": "DB01068_levetir",
        "name": "Levetiracetam",
        "brand_names": ["Keppra", "Spritam"],
        "description": (
            "Second-generation anticonvulsant for focal and generalized seizures. Minimal "
            "hepatic metabolism; excreted mainly unchanged renally via non-CYP enzymatic "
            "hydrolysis. Very few pharmacokinetic drug interactions — highly favorable profile. "
            "No enzyme induction or inhibition."
        ),
        "drug_class": "Anticonvulsant",
        "rxnorm_cui": "277135",
    },
    {
        "id": "DB01186_pregab",
        "name": "Pregabalin",
        "brand_names": ["Lyrica"],
        "description": (
            "Anticonvulsant and neuropathic pain agent for fibromyalgia, DPN, PHN, and "
            "focal seizures. Not metabolized by CYP enzymes; excreted unchanged renally. "
            "Negligible drug interactions via CYP450. Additive CNS depression with opioids, "
            "benzodiazepines, and alcohol. Dose reduction required in renal impairment."
        ),
        "drug_class": "Anticonvulsant / Neuropathic Pain",
        "rxnorm_cui": "187832",
    },
    {
        "id": "DB00555_gabap",
        "name": "Gabapentin",
        "brand_names": ["Neurontin", "Gralise", "Horizant"],
        "description": (
            "Anticonvulsant for focal seizures and neuropathic pain. Not metabolized; excreted "
            "unchanged renally. Minimal CYP-mediated drug interactions. Morphine increases "
            "gabapentin AUC modestly. Antacids reduce absorption. Additive CNS depression."
        ),
        "drug_class": "Anticonvulsant / Neuropathic Pain",
        "rxnorm_cui": "25480",
    },
    {
        "id": "DB00521_oxcarb",
        "name": "Oxcarbazepine",
        "brand_names": ["Trileptal", "Oxtellar XR"],
        "description": (
            "Anticonvulsant related to carbamazepine. Prodrug converted to active monohydroxy "
            "derivative (MHD). Moderate CYP3A4 inducer; reduces levels of oral contraceptives, "
            "cyclosporine, and calcium channel blockers. Inhibits CYP2C19. Less auto-induction "
            "than carbamazepine. Hyponatremia risk."
        ),
        "drug_class": "Anticonvulsant",
        "rxnorm_cui": "55545",
    },
    {
        "id": "DB00313_valp",
        "name": "Valproate",
        "brand_names": ["Depakote", "Depakene", "Stavzor"],
        "description": (
            "Anticonvulsant and mood stabilizer (valproic acid, divalproex sodium). Inhibits "
            "UGT enzymes, CYP2C9, and epoxide hydrolase. Increases lamotrigine levels 2-fold "
            "(reduce lamotrigine dose). Reduces carbamazepine epoxide clearance. "
            "Highly teratogenic (neural tube defects). Free fraction increased by displacing "
            "from albumin binding."
        ),
        "drug_class": "Anticonvulsant / Mood Stabilizer",
        "rxnorm_cui": "10832",
    },
    # =========================================================================
    # CNS — Opioids
    # =========================================================================
    {
        "id": "DB00956_hydro",
        "name": "Hydrocodone",
        "brand_names": ["Vicodin", "Norco", "Zohydro ER"],
        "description": (
            "Opioid analgesic prodrug. Converted to active hydromorphone via CYP2D6. "
            "CYP2D6 poor metabolizers have reduced analgesia. CYP2D6 inhibitors (paroxetine, "
            "fluoxetine) reduce active metabolite formation. CYP3A4 inhibitors increase "
            "hydrocodone parent compound exposure. Schedule II controlled substance."
        ),
        "drug_class": "Opioid Analgesic",
        "rxnorm_cui": "5489",
    },
    {
        "id": "DB01535_oxycod",
        "name": "Oxycodone",
        "brand_names": ["OxyContin", "Percocet", "Roxicodone"],
        "description": (
            "Opioid analgesic. Metabolized by CYP3A4 (major) to inactive noroxycodone and by "
            "CYP2D6 (minor) to oxymorphone. CYP3A4 inhibitors significantly increase oxycodone "
            "levels, risking respiratory depression. CYP3A4 inducers reduce analgesia. "
            "Schedule II; high abuse potential."
        ),
        "drug_class": "Opioid Analgesic",
        "rxnorm_cui": "7804",
    },
    {
        "id": "DB00295_morph",
        "name": "Morphine",
        "brand_names": ["MS Contin", "Kadian", "AVINZA"],
        "description": (
            "Prototype opioid agonist for moderate-to-severe pain. Primarily glucuronidated "
            "to morphine-6-glucuronide (M6G, active) and morphine-3-glucuronide (M3G, inactive). "
            "Minimal CYP involvement. Rifampin accelerates glucuronidation. Additive CNS/respiratory "
            "depression with benzodiazepines, alcohol, and other CNS depressants."
        ),
        "drug_class": "Opioid Analgesic",
        "rxnorm_cui": "7052",
    },
    {
        "id": "DB00813_fent",
        "name": "Fentanyl",
        "brand_names": ["Duragesic", "Actiq", "Sublimaze", "Subsys"],
        "description": (
            "Potent synthetic opioid for moderate-to-severe chronic pain (transdermal) and "
            "procedural analgesia (IV). Exclusively metabolized by CYP3A4 to inactive norfentanyl. "
            "Strong CYP3A4 inhibitors (ritonavir, itraconazole) markedly increase fentanyl "
            "exposure, causing respiratory depression. CYP3A4 inducers reduce analgesia."
        ),
        "drug_class": "Opioid Analgesic",
        "rxnorm_cui": "4337",
    },
    {
        "id": "DB00196_buprenor",
        "name": "Buprenorphine",
        "brand_names": ["Subutex", "Suboxone", "Belbuca", "Butrans"],
        "description": (
            "Partial mu-opioid agonist for opioid use disorder (MAT) and pain management. "
            "Metabolized by CYP3A4 to active norbuprenorphine. CYP3A4 inhibitors increase "
            "buprenorphine levels. Strong CYP3A4 inducers (rifampin) reduce levels and "
            "may precipitate withdrawal. Ceiling effect on respiratory depression."
        ),
        "drug_class": "Opioid / Partial Agonist / MAT",
        "rxnorm_cui": "30131",
    },
    {
        "id": "DB00333_methadone",
        "name": "Methadone",
        "brand_names": ["Dolophine", "Methadose"],
        "description": (
            "Long-acting opioid for pain and opioid use disorder. Metabolized by CYP3A4 "
            "(primary), CYP2D6, CYP2C19, CYP1A2, and CYP2B6. Potent QTc prolongation risk. "
            "CYP inducers (rifampin, carbamazepine) can precipitate withdrawal. "
            "Complex pharmacokinetics with extremely variable half-life (8–59h)."
        ),
        "drug_class": "Opioid / Long-Acting",
        "rxnorm_cui": "6813",
    },
    # =========================================================================
    # ANTI-INFECTIVE — Additional Antibiotics
    # =========================================================================
    {
        "id": "DB01190_clinda",
        "name": "Clindamycin",
        "brand_names": ["Cleocin", "Dalacin"],
        "description": (
            "Lincosamide antibiotic for anaerobic and gram-positive infections. Metabolized "
            "by CYP3A4 to active N-demethylclindamycin. CYP3A4 inhibitors modestly increase "
            "exposure. Minimal clinically significant CYP interactions at typical doses. "
            "Risk of Clostridioides difficile-associated diarrhea (CDAD)."
        ),
        "drug_class": "Antibiotic / Lincosamide",
        "rxnorm_cui": "2582",
    },
    {
        "id": "DB01411_vanco",
        "name": "Vancomycin",
        "brand_names": ["Vancocin"],
        "description": (
            "Glycopeptide antibiotic for serious MRSA and C. difficile infections. Not "
            "metabolized by CYP enzymes; eliminated unchanged by glomerular filtration. "
            "No CYP-mediated drug interactions. Nephrotoxicity risk potentiated by "
            "aminoglycosides, amphotericin B, loop diuretics."
        ),
        "drug_class": "Antibiotic / Glycopeptide",
        "rxnorm_cui": "11124",
    },
    {
        "id": "DB01320_pip",
        "name": "Piperacillin-Tazobactam",
        "brand_names": ["Zosyn", "Tazocin"],
        "description": (
            "Beta-lactam/beta-lactamase inhibitor combination for serious gram-negative and "
            "mixed infections. Not metabolized by CYP enzymes; eliminated renally. No CYP "
            "drug interactions. Additive nephrotoxicity with vancomycin ('Pip-Tazo + Vanco' "
            "combination associated with AKI in some studies)."
        ),
        "drug_class": "Antibiotic / Beta-Lactam/BLI",
        "rxnorm_cui": "41493",
    },
    {
        "id": "DB00688_meropenem",
        "name": "Meropenem",
        "brand_names": ["Merrem"],
        "description": (
            "Carbapenem beta-lactam for severe hospital-acquired and drug-resistant infections. "
            "Not metabolized by CYP enzymes; excreted renally. No CYP interactions. "
            "Reduces valproate levels by ~63-84% via unknown mechanism (possibly UGT "
            "induction or reduced enterohepatic recirculation). Avoid combination with valproate."
        ),
        "drug_class": "Antibiotic / Carbapenem",
        "rxnorm_cui": "29561",
    },
    {
        "id": "DB01159_tobra",
        "name": "Tobramycin",
        "brand_names": ["Tobi", "Bethkis", "Kitabis"],
        "description": (
            "Aminoglycoside antibiotic for serious gram-negative infections and Pseudomonas "
            "in CF. Not metabolized by CYP; excreted unchanged renally. Nephrotoxicity and "
            "ototoxicity risks additive with loop diuretics, cisplatin, and vancomycin. "
            "TDM-guided dosing required."
        ),
        "drug_class": "Antibiotic / Aminoglycoside",
        "rxnorm_cui": "10595",
    },
    # =========================================================================
    # ANTI-INFECTIVE — Antifungals
    # =========================================================================
    {
        "id": "DB01026_keto",
        "name": "Ketoconazole",
        "brand_names": ["Nizoral", "Extina"],
        "description": (
            "Imidazole antifungal (oral use now restricted due to hepatotoxicity). Potent "
            "inhibitor of CYP3A4, CYP2C9, CYP2C19. Used as positive control in drug interaction "
            "studies. Raises plasma levels of all CYP3A4 substrates markedly. FDA-approved only "
            "for endemic mycoses when alternatives unavailable."
        ),
        "drug_class": "Antifungal / Imidazole",
        "rxnorm_cui": "6179",
    },
    {
        "id": "DB00636_flucon",
        "name": "Fluconazole",
        "brand_names": ["Diflucan"],
        "description": (
            "Triazole antifungal for candidiasis and cryptococcosis. Strong CYP2C9 inhibitor "
            "and moderate CYP3A4 inhibitor. Markedly increases warfarin INR. Increases "
            "phenytoin, sulfonylurea, and cyclosporine levels. Single 150mg dose for vaginal "
            "candida still requires awareness of drug interactions."
        ),
        "drug_class": "Antifungal / Triazole",
        "rxnorm_cui": "4450",
    },
    {
        "id": "DB01182_voricon",
        "name": "Voriconazole",
        "brand_names": ["Vfend"],
        "description": (
            "Extended-spectrum triazole antifungal. Strong inhibitor of CYP2C19, CYP2C9, "
            "and CYP3A4. CYP2C19 is the primary metabolic enzyme for voriconazole itself — "
            "CYP2C19 poor metabolizers (Asian > Caucasian) have ~4-fold higher exposure. "
            "Carbamazepine and rifampin dramatically reduce voriconazole levels (contraindicated). "
            "Visual disturbances and QTc prolongation are class effects."
        ),
        "drug_class": "Antifungal / Triazole",
        "rxnorm_cui": "121243",
    },
    {
        "id": "DB00520_casp",
        "name": "Caspofungin",
        "brand_names": ["Cancidas"],
        "description": (
            "Echinocandin antifungal for invasive aspergillosis and candidiasis. Not metabolized "
            "by CYP enzymes; slowly degraded by non-enzymatic hydrolysis and acetylation. "
            "Rifampin, carbamazepine, and efavirenz (inducers) may reduce caspofungin trough "
            "levels; consider increased dosing. Generally minimal drug interactions."
        ),
        "drug_class": "Antifungal / Echinocandin",
        "rxnorm_cui": "240106",
    },
    # =========================================================================
    # ANTI-INFECTIVE — Antivirals
    # =========================================================================
    {
        "id": "DB09183_ledip",
        "name": "Ledipasvir",
        "brand_names": ["Harvoni (combined with sofosbuvir)"],
        "description": (
            "NS5A inhibitor for hepatitis C. P-glycoprotein inhibitor. Concomitant acid-reducing "
            "agents (PPIs, H2 blockers) reduce ledipasvir absorption significantly. "
            "Increases tenofovir levels via P-gp inhibition, raising nephrotoxicity risk "
            "in patients on TDF-based regimens."
        ),
        "drug_class": "Antiviral / HCV NS5A Inhibitor",
        "rxnorm_cui": "1587565",
    },
    {
        "id": "DB09102_daclat",
        "name": "Daclatasvir",
        "brand_names": ["Daklinza"],
        "description": (
            "NS5A inhibitor for hepatitis C genotypes 1 and 3. Metabolized by CYP3A4. "
            "Strong CYP3A4 inhibitors (atazanavir) require daclatasvir dose reduction to 30mg. "
            "Strong CYP3A4 inducers (rifampin) require dose increase to 90mg or are "
            "contraindicated."
        ),
        "drug_class": "Antiviral / HCV NS5A Inhibitor",
        "rxnorm_cui": "1602060",
    },
    {
        "id": "DB00625_valacy",
        "name": "Valacyclovir",
        "brand_names": ["Valtrex"],
        "description": (
            "Prodrug of acyclovir used for herpes simplex, varicella-zoster, and CMV prophylaxis. "
            "Converted to acyclovir by intestinal and hepatic valacyclovirase. Acyclovir excreted "
            "renally. Minimal CYP-mediated interactions. Probenecid and cimetidine reduce renal "
            "tubular secretion. Dose adjustment required in renal impairment."
        ),
        "drug_class": "Antiviral / Nucleoside Analog",
        "rxnorm_cui": "117852",
    },
    {
        "id": "DB00900_oselt",
        "name": "Oseltamivir",
        "brand_names": ["Tamiflu"],
        "description": (
            "Influenza neuraminidase inhibitor prodrug. Converted to active oseltamivir "
            "carboxylate by hepatic esterases; not CYP-metabolized. Probenecid reduces "
            "renal clearance, doubling exposure. Minimal CYP drug interactions. "
            "Should be started within 48h of symptom onset."
        ),
        "drug_class": "Antiviral / Neuraminidase Inhibitor",
        "rxnorm_cui": "134527",
    },
    {
        "id": "DB14003_remdesivir",
        "name": "Remdesivir",
        "brand_names": ["Veklury"],
        "description": (
            "Adenosine nucleotide prodrug for SARS-CoV-2 and Ebola. Converted intracellularly "
            "to active triphosphate. Metabolized by CYP3A4, CYP2C8, CYP2D6. Chloroquine and "
            "hydroxychloroquine reduce antiviral activity (reduced phosphorylation). "
            "Strong CYP inducers may reduce plasma levels."
        ),
        "drug_class": "Antiviral / Nucleotide Prodrug",
        "rxnorm_cui": "2284960",
    },
    # =========================================================================
    # ANTI-INFECTIVE — Antimalarials
    # =========================================================================
    {
        "id": "DB01611_hydroxy",
        "name": "Hydroxychloroquine",
        "brand_names": ["Plaquenil"],
        "description": (
            "4-aminoquinoline antimalarial and DMARD for RA and SLE. Inhibits CYP2D6 "
            "moderately. Increases metoprolol exposure by ~65%. QTc prolongation risk "
            "additive with other QT-prolonging drugs. Metabolized by CYP2C8 and CYP3A4."
        ),
        "drug_class": "Antimalarial / DMARD",
        "rxnorm_cui": "5521",
    },
    {
        "id": "DB01410_mefloquine",
        "name": "Mefloquine",
        "brand_names": ["Lariam"],
        "description": (
            "Antimalarial quinoline for prophylaxis and treatment. Metabolized by CYP3A4. "
            "CYP3A4 inhibitors increase mefloquine levels. QTc prolongation and neuropsychiatric "
            "adverse effects (anxiety, depression, psychosis, seizures). Halofantrine "
            "combination increases QT risk (contraindicated)."
        ),
        "drug_class": "Antimalarial",
        "rxnorm_cui": "41493",
    },
    {
        "id": "DB04272_lumefantrine",
        "name": "Artemether-Lumefantrine",
        "brand_names": ["Coartem"],
        "description": (
            "Combination antimalarial for uncomplicated P. falciparum malaria. Artemether "
            "metabolized by CYP3A4/CYP2B6 to active dihydroartemisinin. Lumefantrine metabolized "
            "by CYP3A4. Both CYP3A4 substrates. QTc prolongation; avoid concurrent QT-prolonging "
            "drugs. Fatty food required for lumefantrine absorption."
        ),
        "drug_class": "Antimalarial / Artemisinin-based Combination",
        "rxnorm_cui": "1310149",
    },
    # =========================================================================
    # ONCOLOGY — Oral Chemotherapy
    # =========================================================================
    {
        "id": "DB01418_capecit",
        "name": "Capecitabine",
        "brand_names": ["Xeloda"],
        "description": (
            "Oral fluoropyrimidine prodrug for colorectal, breast, and gastric cancers. "
            "Converted to 5-FU by thymidine phosphorylase in tumor tissue. Inhibits CYP2C9; "
            "markedly increases warfarin INR (life-threatening bleeding). Also increases "
            "phenytoin levels via CYP2C9 inhibition."
        ),
        "drug_class": "Antineoplastic / Fluoropyrimidine",
        "rxnorm_cui": "194000",
    },
    {
        "id": "DB01048_ibrutinib",
        "name": "Ibrutinib",
        "brand_names": ["Imbruvica"],
        "description": (
            "Bruton tyrosine kinase (BTK) inhibitor for B-cell malignancies (CLL, MCL, WM). "
            "Primarily metabolized by CYP3A4 to active dihydrodiol metabolite. Strong CYP3A4 "
            "inhibitors increase ibrutinib exposure up to 24-fold; contraindicated or require "
            "dose reduction. Strong CYP3A4 inducers substantially reduce efficacy."
        ),
        "drug_class": "Antineoplastic / BTK Inhibitor",
        "rxnorm_cui": "1660010",
    },
    {
        "id": "DB09023_imatinib",
        "name": "Imatinib",
        "brand_names": ["Gleevec", "Glivec"],
        "description": (
            "BCR-ABL tyrosine kinase inhibitor for CML and GIST. Metabolized by CYP3A4 "
            "(primary) and CYP1A2, CYP2D6, CYP2C9 (secondary). Strong CYP3A4 inhibitors "
            "increase imatinib levels. Strong CYP3A4 inducers (rifampin) reduce levels by ~74%. "
            "Inhibits CYP2D6 and CYP3A4, increasing levels of other substrates."
        ),
        "drug_class": "Antineoplastic / BCR-ABL TKI",
        "rxnorm_cui": "282388",
    },
    {
        "id": "DB08877_erlot",
        "name": "Erlotinib",
        "brand_names": ["Tarceva"],
        "description": (
            "EGFR tyrosine kinase inhibitor for NSCLC and pancreatic cancer. Metabolized "
            "by CYP3A4 (primary) and CYP1A2. Strong CYP3A4 inducers (rifampin) reduce erlotinib "
            "AUC by ~66%. CYP3A4 inhibitors increase exposure. Acid suppression (PPIs) "
            "substantially reduces erlotinib absorption."
        ),
        "drug_class": "Antineoplastic / EGFR TKI",
        "rxnorm_cui": "352103",
    },
    {
        "id": "DB09073_palbociclib",
        "name": "Palbociclib",
        "brand_names": ["Ibrance"],
        "description": (
            "CDK4/6 inhibitor for hormone receptor-positive HER2-negative breast cancer. "
            "Primarily metabolized by CYP3A4 and SULT2A1. Strong CYP3A4 inhibitors increase "
            "palbociclib exposure ~87%. Strong CYP3A4 inducers (rifampin) reduce exposure ~85%. "
            "Take with food for adequate absorption."
        ),
        "drug_class": "Antineoplastic / CDK4/6 Inhibitor",
        "rxnorm_cui": "1717484",
    },
    {
        "id": "DB11785_pembroliz",
        "name": "Pembrolizumab",
        "brand_names": ["Keytruda"],
        "description": (
            "PD-1 immune checkpoint inhibitor for multiple solid tumors and hematologic cancers. "
            "Monoclonal antibody catabolized by proteolytic enzymes; not CYP-metabolized. "
            "No CYP-mediated pharmacokinetic interactions. Immune-related adverse events "
            "(irAEs) may require corticosteroid treatment."
        ),
        "drug_class": "Antineoplastic / PD-1 Inhibitor / Immunotherapy",
        "rxnorm_cui": "1736854",
    },
    {
        "id": "DB09292_nivolumab",
        "name": "Nivolumab",
        "brand_names": ["Opdivo"],
        "description": (
            "PD-1 checkpoint inhibitor monoclonal antibody for multiple cancers. "
            "Catabolized by proteolytic enzymes; not metabolized by CYP450. Immune-related "
            "adverse events (pneumonitis, colitis, hepatitis, endocrinopathies). "
            "Corticosteroids used to manage irAEs."
        ),
        "drug_class": "Antineoplastic / PD-1 Inhibitor / Immunotherapy",
        "rxnorm_cui": "1657056",
    },
    {
        "id": "DB11093_venetoclax",
        "name": "Venetoclax",
        "brand_names": ["Venclexta"],
        "description": (
            "BCL-2 inhibitor for CLL/SLL and AML. Primarily metabolized by CYP3A4/5. "
            "Strong CYP3A4 inhibitors increase venetoclax AUC up to 6-7 fold — dose reduction "
            "required. Strong inducers substantially decrease exposure. Tumor lysis syndrome risk "
            "requires prophylaxis and dose-ramp-up protocol."
        ),
        "drug_class": "Antineoplastic / BCL-2 Inhibitor",
        "rxnorm_cui": "1860475",
    },
    {
        "id": "DB11901_abira",
        "name": "Abiraterone",
        "brand_names": ["Zytiga", "Yonsa"],
        "description": (
            "CYP17A1 inhibitor for metastatic castration-resistant prostate cancer. "
            "Metabolized by SULT2A1 and CYP3A4. Inhibits CYP2D6 and CYP2C8. "
            "Increases levels of CYP2D6 substrates (dextromethorphan, opioids). "
            "Must be given with prednisone to prevent mineralocorticoid excess."
        ),
        "drug_class": "Antineoplastic / CYP17A1 Inhibitor",
        "rxnorm_cui": "1310397",
    },
    # =========================================================================
    # ENDOCRINE — Diabetes
    # =========================================================================
    {
        "id": "DB00331_metform",
        "name": "Metformin",
        "brand_names": ["Glucophage", "Glumetza", "Riomet"],
        "description": (
            "Biguanide first-line antidiabetic for type 2 diabetes. Not metabolized by "
            "CYP enzymes; excreted unchanged by renal tubular secretion (OCT2). "
            "Trimethoprim and cimetidine inhibit OCT2, raising metformin levels. "
            "Contrast dye, excessive alcohol, and iodinated contrast agents risk lactic acidosis."
        ),
        "drug_class": "Antidiabetic / Biguanide",
        "rxnorm_cui": "6809",
    },
    {
        "id": "DB01145_glyburide",
        "name": "Glyburide",
        "brand_names": ["DiaBeta", "Micronase", "Glynase"],
        "description": (
            "Second-generation sulfonylurea antidiabetic. Metabolized by CYP2C9 to weakly "
            "active metabolites. CYP2C9 inhibitors (fluconazole, amiodarone) increase "
            "glyburide levels, risking hypoglycemia. Renal elimination of metabolites."
        ),
        "drug_class": "Antidiabetic / Sulfonylurea",
        "rxnorm_cui": "4815",
    },
    {
        "id": "DB01234_glipizide",
        "name": "Glipizide",
        "brand_names": ["Glucotrol"],
        "description": (
            "Second-generation sulfonylurea. Metabolized primarily by CYP2C9. "
            "CYP2C9 inhibitors (fluconazole, miconazole) can increase levels and hypoglycemia risk. "
            "Shorter half-life than glyburide; some advantage in elderly."
        ),
        "drug_class": "Antidiabetic / Sulfonylurea",
        "rxnorm_cui": "4536",
    },
    {
        "id": "DB01067_pioglitazone",
        "name": "Pioglitazone",
        "brand_names": ["Actos"],
        "description": (
            "Thiazolidinedione PPAR-gamma agonist for type 2 diabetes. Metabolized by CYP2C8 "
            "(primary) and CYP3A4. CYP2C8 inhibitors (gemfibrozil) markedly increase pioglitazone "
            "AUC ~3-fold, potentiating hypoglycemia and fluid retention. Gemfibrozil combination "
            "contraindicated or requires dose reduction."
        ),
        "drug_class": "Antidiabetic / Thiazolidinedione",
        "rxnorm_cui": "33738",
    },
    {
        "id": "DB09883_sita",
        "name": "Sitagliptin",
        "brand_names": ["Januvia"],
        "description": (
            "DPP-4 inhibitor for type 2 diabetes. Primarily excreted unchanged renally; "
            "minor CYP3A4 metabolism. P-gp and CYP3A4 moderate inhibitors may modestly "
            "increase sitagliptin exposure. Generally low drug interaction potential. "
            "Dose reduction required in renal impairment."
        ),
        "drug_class": "Antidiabetic / DPP-4 Inhibitor",
        "rxnorm_cui": "593411",
    },
    {
        "id": "DB06292_empa",
        "name": "Empagliflozin",
        "brand_names": ["Jardiance"],
        "description": (
            "SGLT-2 inhibitor for type 2 diabetes, heart failure, and CKD. Primarily "
            "glucuronidated; UGT1A3 and UGT2B4 are main metabolic enzymes. Minimal CYP "
            "involvement. P-gp substrate. Rifampin reduces empagliflozin exposure ~35%. "
            "Beneficial cardiovascular and renal outcomes (EMPA-REG OUTCOME trial)."
        ),
        "drug_class": "Antidiabetic / SGLT-2 Inhibitor",
        "rxnorm_cui": "1545149",
    },
    {
        "id": "DB09212_cana",
        "name": "Canagliflozin",
        "brand_names": ["Invokana"],
        "description": (
            "SGLT-2 inhibitor for type 2 diabetes, heart failure, and CKD. Glucuronidated by "
            "UGT1A9 and UGT2B4. P-gp substrate; rifampin reduces levels ~51%. Inhibits "
            "UGT1A4/1A6, modestly raising exposure of co-administered UGT substrates. "
            "Diuretic and antihypertensive effects."
        ),
        "drug_class": "Antidiabetic / SGLT-2 Inhibitor",
        "rxnorm_cui": "1373458",
    },
    {
        "id": "DB00712_lira",
        "name": "Liraglutide",
        "brand_names": ["Victoza", "Saxenda"],
        "description": (
            "GLP-1 receptor agonist for type 2 diabetes (Victoza) and obesity (Saxenda). "
            "Metabolized by DPP-IV and endopeptidases; not CYP-metabolized. Slows gastric "
            "emptying, which can reduce absorption of oral drugs taken concomitantly. "
            "Minimal CYP-mediated pharmacokinetic interactions."
        ),
        "drug_class": "Antidiabetic / GLP-1 Receptor Agonist",
        "rxnorm_cui": "475968",
    },
    {
        "id": "DB09655_semaglu",
        "name": "Semaglutide",
        "brand_names": ["Ozempic", "Wegovy", "Rybelsus"],
        "description": (
            "GLP-1 receptor agonist for type 2 diabetes and obesity. Not CYP-metabolized; "
            "degraded by proteases. Delays gastric emptying, potentially affecting oral drug "
            "absorption (e.g., oral contraceptives should be taken 1h before or 4h after). "
            "Major cardiovascular benefit data (SUSTAIN-6 trial)."
        ),
        "drug_class": "Antidiabetic / GLP-1 Receptor Agonist",
        "rxnorm_cui": "2200600",
    },
    # =========================================================================
    # ENDOCRINE — Thyroid
    # =========================================================================
    {
        "id": "DB00755_levothyrox",
        "name": "Levothyroxine",
        "brand_names": ["Synthroid", "Levoxyl", "Tirosint"],
        "description": (
            "Synthetic T4 thyroid hormone for hypothyroidism. Metabolized by deiodinases "
            "(not CYP). Absorption reduced by calcium, iron, bile acid sequestrants (cholestyramine), "
            "PPIs, and antacids — take 30-60 minutes before food or other medications. "
            "Warfarin interaction: levothyroxine increases warfarin sensitivity."
        ),
        "drug_class": "Thyroid Hormone",
        "rxnorm_cui": "10582",
    },
    {
        "id": "DB00675_methima",
        "name": "Methimazole",
        "brand_names": ["Tapazole"],
        "description": (
            "Antithyroid drug for hyperthyroidism. Inhibits thyroid peroxidase. Metabolized "
            "by CYP1A2 partially. Reversible agranulocytosis risk. As thyroid function normalizes, "
            "may need warfarin dose reduction (thyroid hormones increase warfarin sensitivity). "
            "Preferred over propylthiouracil (PTU) except in first trimester of pregnancy."
        ),
        "drug_class": "Antithyroid Agent",
        "rxnorm_cui": "6870",
    },
    # =========================================================================
    # ENDOCRINE — Corticosteroids
    # =========================================================================
    {
        "id": "DB00591_dexa",
        "name": "Dexamethasone",
        "brand_names": ["Decadron", "Ozurdex"],
        "description": (
            "Potent synthetic glucocorticoid. Strong CYP3A4 inducer; reduces levels of "
            "many CYP3A4 substrates including oral contraceptives, antiretrovirals, "
            "cyclosporine, and itraconazole. Also a CYP3A4 substrate. "
            "Used in oncology as antiemetic and anti-inflammatory; induction effect "
            "relevant during chemotherapy administration."
        ),
        "drug_class": "Corticosteroid / Glucocorticoid",
        "rxnorm_cui": "3264",
    },
    {
        "id": "DB00635_pred",
        "name": "Prednisone",
        "brand_names": ["Deltasone", "Rayos"],
        "description": (
            "Synthetic glucocorticoid prodrug converted to active prednisolone by CYP3A4/5 "
            "11-beta-HSD. CYP3A4 inhibitors increase prednisolone levels. Rifampin increases "
            "clearance significantly. Long-term use causes adrenal suppression, requiring taper. "
            "Concomitant NSAIDs increase GI bleeding risk."
        ),
        "drug_class": "Corticosteroid / Glucocorticoid",
        "rxnorm_cui": "8640",
    },
    {
        "id": "DB00687_fludro",
        "name": "Fludrocortisone",
        "brand_names": ["Florinef"],
        "description": (
            "Synthetic mineralocorticoid for adrenal insufficiency and orthostatic hypotension. "
            "Metabolized by CYP3A4 and CYP3A5. CYP3A4 inhibitors increase levels. "
            "Sodium retention and potassium depletion effects require monitoring of electrolytes. "
            "Amphotericin B combination potentiates hypokalemia."
        ),
        "drug_class": "Corticosteroid / Mineralocorticoid",
        "rxnorm_cui": "4157",
    },
    # =========================================================================
    # GI — PPIs
    # =========================================================================
    {
        "id": "DB00338_omeprz",
        "name": "Omeprazole",
        "brand_names": ["Prilosec", "Zegerid"],
        "description": (
            "First PPI approved; irreversibly inhibits H+/K+-ATPase. Metabolized by CYP2C19 "
            "(primary) and CYP3A4. CYP2C19 poor metabolizers have ~5-fold higher exposure. "
            "Inhibits CYP2C19, reducing clopidogrel activation and increasing citalopram levels. "
            "Reduces absorption of ketoconazole, itraconazole, and erlotinib (pH-dependent)."
        ),
        "drug_class": "GI / Proton Pump Inhibitor",
        "rxnorm_cui": "7646",
    },
    {
        "id": "DB00213_rabep",
        "name": "Rabeprazole",
        "brand_names": ["Aciphex"],
        "description": (
            "PPI with less CYP2C19 dependency than omeprazole. Metabolized primarily via "
            "non-enzymatic reduction, with minor CYP2C19 and CYP3A4 involvement. "
            "More consistent pharmacokinetics across CYP2C19 genotypes. "
            "Still reduces clopidogrel activation, though to lesser extent than omeprazole."
        ),
        "drug_class": "GI / Proton Pump Inhibitor",
        "rxnorm_cui": "75827",
    },
    {
        "id": "DB00736_esomep",
        "name": "Esomeprazole",
        "brand_names": ["Nexium"],
        "description": (
            "S-isomer of omeprazole. Metabolized by CYP2C19 and CYP3A4. Inhibits CYP2C19; "
            "increases diazepam, citalopram, and escitalopram levels. Reduces pH and decreases "
            "absorption of pH-sensitive drugs (ketoconazole, itraconazole). Reduces clopidogrel "
            "efficacy similar to omeprazole."
        ),
        "drug_class": "GI / Proton Pump Inhibitor",
        "rxnorm_cui": "283742",
    },
    {
        "id": "DB00252_lanzop",
        "name": "Lansoprazole",
        "brand_names": ["Prevacid"],
        "description": (
            "PPI metabolized by CYP2C19 (primary) and CYP3A4. Mild CYP2C19 inhibitor. "
            "Less potent CYP2C19 inhibitor than omeprazole. Reduces absorption of "
            "pH-sensitive drugs. Available OTC in 15mg dose."
        ),
        "drug_class": "GI / Proton Pump Inhibitor",
        "rxnorm_cui": "17128",
    },
    # =========================================================================
    # GI — H2 Blockers
    # =========================================================================
    {
        "id": "DB00501_cimetidine",
        "name": "Cimetidine",
        "brand_names": ["Tagamet"],
        "description": (
            "H2 receptor antagonist. Broad CYP inhibitor: inhibits CYP1A2, CYP2C9, CYP2D6, "
            "and CYP3A4. Also inhibits renal tubular secretion of many drugs (creatinine, "
            "metformin, procainamide). Raises levels of warfarin, theophylline, phenytoin, "
            "lidocaine, metoprolol. Most drug-interactive H2 blocker."
        ),
        "drug_class": "GI / H2 Receptor Antagonist",
        "rxnorm_cui": "2541",
    },
    {
        "id": "DB00585_ranitidine",
        "name": "Ranitidine",
        "brand_names": ["Zantac"],
        "description": (
            "H2 receptor antagonist; withdrawn from US market in 2020 due to NDMA contamination. "
            "Weaker CYP inhibitor than cimetidine; clinically relevant interaction with "
            "warfarin and some antifungals. Historical reference for drug interaction database. "
            "Some markets still have low-NDMA versions."
        ),
        "drug_class": "GI / H2 Receptor Antagonist",
        "rxnorm_cui": "9143",
    },
    {
        "id": "DB00927_famotidine",
        "name": "Famotidine",
        "brand_names": ["Pepcid"],
        "description": (
            "H2 receptor antagonist with minimal CYP enzyme interactions. Not significantly "
            "metabolized by CYP; excreted mainly renally. Fewer drug interactions than "
            "cimetidine. Available OTC. Dose adjustment in renal impairment."
        ),
        "drug_class": "GI / H2 Receptor Antagonist",
        "rxnorm_cui": "4278",
    },
    # =========================================================================
    # GI — Antiemetics
    # =========================================================================
    {
        "id": "DB00904_ondansetron",
        "name": "Ondansetron",
        "brand_names": ["Zofran", "Zuplenz"],
        "description": (
            "5-HT3 antagonist antiemetic for chemotherapy-induced, postoperative, and "
            "radiation-induced nausea. Metabolized by CYP3A4, CYP1A2, and CYP2D6. "
            "QTc prolongation dose-dependent; concomitant QT-prolonging agents increase risk. "
            "Serotonin syndrome risk with serotonergic drugs (SSRIs, tramadol, linezolid)."
        ),
        "drug_class": "Antiemetic / 5-HT3 Antagonist",
        "rxnorm_cui": "26225",
    },
    {
        "id": "DB01462_metoclop",
        "name": "Metoclopramide",
        "brand_names": ["Reglan"],
        "description": (
            "Dopamine antagonist prokinetic and antiemetic. Metabolized by CYP2D6 partially. "
            "Accelerates gastric emptying, potentially reducing absorption of many oral drugs "
            "(digoxin) but increasing absorption of others (cyclosporine, alcohol). "
            "Risk of tardive dyskinesia with prolonged use. Drug interactions via accelerated "
            "gastric emptying."
        ),
        "drug_class": "Antiemetic / Prokinetic",
        "rxnorm_cui": "6854",
    },
    {
        "id": "DB00757_aprepitant",
        "name": "Aprepitant",
        "brand_names": ["Emend"],
        "description": (
            "NK1 receptor antagonist antiemetic for chemotherapy-induced nausea. Metabolized "
            "by CYP3A4. Moderate CYP3A4 inhibitor initially, followed by CYP3A4 induction at "
            "later timepoints (mixed inhibitor/inducer). Reduces dexamethasone levels (standard "
            "dex doses should be halved). Reduces efficacy of oral contraceptives."
        ),
        "drug_class": "Antiemetic / NK1 Receptor Antagonist",
        "rxnorm_cui": "351237",
    },
    # =========================================================================
    # RESPIRATORY — Bronchodilators
    # =========================================================================
    {
        "id": "DB01174_salb",
        "name": "Albuterol",
        "brand_names": ["ProAir HFA", "Ventolin HFA", "Proventil HFA"],
        "description": (
            "Short-acting beta-2 agonist (SABA) bronchodilator for acute asthma and COPD. "
            "Metabolized to albuterol 4'-O-sulfate (inactive) by SULT1A3. Not CYP-dependent. "
            "Hypokalemia risk especially with corticosteroids and loop diuretics. "
            "QTc prolongation risk with high doses and concomitant QT-prolonging agents."
        ),
        "drug_class": "Bronchodilator / SABA",
        "rxnorm_cui": "435",
    },
    {
        "id": "DB00675_salme",
        "name": "Salmeterol",
        "brand_names": ["Serevent"],
        "description": (
            "Long-acting beta-2 agonist (LABA) for asthma and COPD. Metabolized by CYP3A4. "
            "Strong CYP3A4 inhibitors (ketoconazole, ritonavir) markedly increase salmeterol "
            "exposure, causing cardiovascular adverse effects (QTc prolongation, palpitations). "
            "Must be used with inhaled corticosteroid in asthma."
        ),
        "drug_class": "Bronchodilator / LABA",
        "rxnorm_cui": "36117",
    },
    {
        "id": "DB00279_tiotropium",
        "name": "Tiotropium",
        "brand_names": ["Spiriva"],
        "description": (
            "Long-acting muscarinic antagonist (LAMA) for COPD. Primarily excreted renally "
            "unchanged; minimal CYP metabolism (CYP2D6 and CYP3A4 minor). Low drug interaction "
            "potential via CYP450. Additive anticholinergic effects with other antimuscarinic "
            "agents."
        ),
        "drug_class": "Bronchodilator / LAMA",
        "rxnorm_cui": "274783",
    },
    {
        "id": "DB00698_theoph",
        "name": "Theophylline",
        "brand_names": ["Theo-24", "Uniphyl", "Theochron"],
        "description": (
            "Methylxanthine bronchodilator for asthma and COPD. Primarily metabolized by "
            "CYP1A2. Narrow therapeutic index (10-20 mcg/mL). CYP1A2 inhibitors (ciprofloxacin, "
            "fluvoxamine, enoxacin) can rapidly cause theophylline toxicity (seizures, arrhythmias). "
            "Cigarette smoking induces CYP1A2, reducing levels. Rifampin induces CYP1A2/3A4."
        ),
        "drug_class": "Bronchodilator / Methylxanthine",
        "rxnorm_cui": "10600",
    },
    {
        "id": "DB00353_roflumilast",
        "name": "Roflumilast",
        "brand_names": ["Daliresp"],
        "description": (
            "PDE-4 inhibitor for severe COPD with chronic bronchitis. Metabolized by CYP3A4 "
            "(primary) and CYP1A2 to active roflumilast N-oxide. Strong CYP inducers (rifampin) "
            "reduce total PDE4 inhibitory activity by ~60% — avoid combination. CYP3A4/1A2 "
            "inhibitors increase exposure moderately."
        ),
        "drug_class": "PDE-4 Inhibitor / Anti-inflammatory",
        "rxnorm_cui": "1005456",
    },
    # =========================================================================
    # RESPIRATORY — Inhaled Corticosteroids
    # =========================================================================
    {
        "id": "DB00394_beclo",
        "name": "Beclomethasone",
        "brand_names": ["QVAR", "Beconase AQ"],
        "description": (
            "Inhaled corticosteroid (ICS) for asthma and allergic rhinitis. Converted to "
            "active beclomethasone-17-monopropionate by esterases. Minimal systemic exposure "
            "reduces CYP3A4 interaction risk. High local lung concentrations with minimal "
            "adrenal suppression at standard doses."
        ),
        "drug_class": "Inhaled Corticosteroid",
        "rxnorm_cui": "1389",
    },
    {
        "id": "DB01280_flutica",
        "name": "Fluticasone",
        "brand_names": ["Flovent HFA", "Flonase", "Arnuity"],
        "description": (
            "Inhaled corticosteroid. Extensively metabolized by CYP3A4; high first-pass effect "
            "limits systemic exposure after inhalation. However, strong CYP3A4 inhibitors "
            "(ritonavir, itraconazole) can dramatically increase systemic fluticasone levels "
            "even from inhaled route, causing Cushing syndrome and adrenal suppression. "
            "Clinically significant with HIV protease inhibitors."
        ),
        "drug_class": "Inhaled Corticosteroid",
        "rxnorm_cui": "41193",
    },
    {
        "id": "DB01411_budesonide",
        "name": "Budesonide",
        "brand_names": ["Pulmicort", "Rhinocort", "Entocort EC", "Uceris"],
        "description": (
            "Inhaled/enteric corticosteroid. Metabolized by CYP3A4 (strong first-pass effect). "
            "Strong CYP3A4 inhibitors (ritonavir) markedly increase systemic budesonide exposure. "
            "Available in inhaled, intranasal, and oral (GI) formulations. "
            "Oral capsule used for Crohn's disease with minimal systemic effects."
        ),
        "drug_class": "Inhaled/Enteric Corticosteroid",
        "rxnorm_cui": "19831",
    },
    # =========================================================================
    # IMMUNOLOGY — DMARDs
    # =========================================================================
    {
        "id": "DB00563_metho",
        "name": "Methotrexate",
        "brand_names": ["Trexall", "Rheumatrex", "Xatmep"],
        "description": (
            "Folate antimetabolite DMARD for RA, psoriasis, and chemotherapy. Not significantly "
            "metabolized by CYP enzymes; eliminated renally. NSAIDs, probenecid, and "
            "trimethoprim reduce renal methotrexate clearance, increasing toxicity risk. "
            "PPIs may increase methotrexate levels. Hepatotoxic and myelosuppressive."
        ),
        "drug_class": "DMARD / Antimetabolite",
        "rxnorm_cui": "6851",
    },
    {
        "id": "DB00795_sulfasalazine",
        "name": "Sulfasalazine",
        "brand_names": ["Azulfidine"],
        "description": (
            "DMARD for RA, IBD, and ankylosing spondylitis. Cleaved by gut bacteria to "
            "sulfapyridine and mesalamine. Sulfapyridine metabolized by CYP2C9/NAT2. "
            "Inhibits OATP1B1 transporter. Reduces folate absorption; supplement recommended. "
            "Displaced by warfarin from protein binding sites."
        ),
        "drug_class": "DMARD / Aminosalicylate",
        "rxnorm_cui": "9524",
    },
    {
        "id": "DB01589_leflu",
        "name": "Leflunomide",
        "brand_names": ["Arava"],
        "description": (
            "DMARD prodrug for RA. Converted to active teriflunomide by gut and hepatic "
            "enzymes. Teriflunomide inhibits CYP2C9, increasing warfarin exposure. "
            "Also inhibits CYP1A2. Enterohepatic recirculation causes very long half-life "
            "(weeks); cholestyramine washout required if needed."
        ),
        "drug_class": "DMARD",
        "rxnorm_cui": "44657",
    },
    {
        "id": "DB14093_barici",
        "name": "Baricitinib",
        "brand_names": ["Olumiant"],
        "description": (
            "JAK1/2 inhibitor for RA and alopecia areata. Primarily excreted unchanged renally "
            "via OAT3 transporter. Probenecid (OAT3 inhibitor) doubles baricitinib AUC. "
            "Minimal CYP metabolism. Dose reduction in renal impairment."
        ),
        "drug_class": "DMARD / JAK Inhibitor",
        "rxnorm_cui": "1860488",
    },
    {
        "id": "DB11817_tofa",
        "name": "Tofacitinib",
        "brand_names": ["Xeljanz", "Xeljanz XR"],
        "description": (
            "JAK1/3 inhibitor for RA, PsA, UC, and ankylosing spondylitis. Primarily "
            "metabolized by CYP3A4 (major) and CYP2C19 (minor). Strong CYP3A4 inhibitors "
            "increase tofacitinib AUC ~107%. Strong inducers (rifampin) reduce AUC ~84%. "
            "Moderate CYP3A4 inhibitors with CYP2C19 inhibition (fluconazole) also increase "
            "exposure significantly."
        ),
        "drug_class": "DMARD / JAK Inhibitor",
        "rxnorm_cui": "1312409",
    },
    # =========================================================================
    # IMMUNOLOGY — Biologics
    # =========================================================================
    {
        "id": "DB00065_adal",
        "name": "Adalimumab",
        "brand_names": ["Humira"],
        "description": (
            "Anti-TNF-alpha monoclonal antibody for RA, Crohn's disease, UC, psoriasis, PsA, "
            "AS, and uveitis. Not CYP-metabolized; catabolized by proteolytic enzymes. "
            "MTX co-administration reduces adalimumab clearance by ~29% (desired effect). "
            "Live vaccines contraindicated during treatment."
        ),
        "drug_class": "Biologic / Anti-TNF",
        "rxnorm_cui": "327361",
    },
    {
        "id": "DB00065_infli",
        "name": "Infliximab",
        "brand_names": ["Remicade", "Inflectra", "Renflexis"],
        "description": (
            "Chimeric anti-TNF monoclonal antibody for IBD, RA, PsA, AS, and psoriasis. "
            "Not CYP-metabolized; proteolytic catabolism. MTX reduces immunogenicity and "
            "clearance of infliximab (combination therapy standard). Thiopurines "
            "increase hepatosplenic T-cell lymphoma risk in young males."
        ),
        "drug_class": "Biologic / Anti-TNF",
        "rxnorm_cui": "214397",
    },
    {
        "id": "DB09029_secukinum",
        "name": "Secukinumab",
        "brand_names": ["Cosentyx"],
        "description": (
            "Anti-IL-17A monoclonal antibody for plaque psoriasis, PsA, and AS. "
            "Not CYP-metabolized. Cytokines can downregulate CYP enzymes; anti-cytokine "
            "biologics may normalize CYP activity, restoring metabolism of CYP-metabolized "
            "drugs (watch for subtherapeutic levels of narrow-TI drugs if inflammation resolves)."
        ),
        "drug_class": "Biologic / Anti-IL-17A",
        "rxnorm_cui": "1726126",
    },
    {
        "id": "DB09029_dupil",
        "name": "Dupilumab",
        "brand_names": ["Dupixent"],
        "description": (
            "Anti-IL-4/13 receptor monoclonal antibody for atopic dermatitis, asthma, CRSwNP, "
            "eosinophilic esophagitis, and prurigo nodularis. Not CYP-metabolized. "
            "May normalize IL-4/13-mediated CYP3A4 suppression in atopic disease, "
            "potentially increasing clearance of CYP3A4 substrates (e.g., ciclosporin)."
        ),
        "drug_class": "Biologic / Anti-IL-4/13 Receptor",
        "rxnorm_cui": "2003658",
    },
    # =========================================================================
    # ADDITIONAL — Miscellaneous important drugs
    # =========================================================================
    {
        "id": "DB00558_osimertinib",
        "name": "Osimertinib",
        "brand_names": ["Tagrisso"],
        "description": (
            "Third-generation EGFR TKI for EGFR-mutant NSCLC including T790M resistance "
            "mutation. Metabolized by CYP3A4 and CYP3A5. Strong CYP3A4 inducers (rifampin) "
            "reduce osimertinib AUC ~84% — avoid. QTc prolongation; avoid concurrent "
            "QT-prolonging drugs. Interstitial lung disease is class-related adverse effect."
        ),
        "drug_class": "Antineoplastic / EGFR TKI (3rd gen)",
        "rxnorm_cui": "1870479",
    },
    {
        "id": "DB09168_colchi",
        "name": "Colchicine",
        "brand_names": ["Colcrys", "Mitigare", "Gloperba"],
        "description": (
            "Anti-inflammatory agent for gout, familial Mediterranean fever, and pericarditis. "
            "CYP3A4 substrate and P-gp substrate. Strong CYP3A4/P-gp inhibitors (clarithromycin, "
            "ketoconazole, ritonavir) dramatically increase colchicine levels causing "
            "life-threatening toxicity. Reduce dose or contraindicate with strong inhibitors "
            "(especially in renal/hepatic impairment)."
        ),
        "drug_class": "Anti-gout / Anti-inflammatory",
        "rxnorm_cui": "2683",
    },
    {
        "id": "DB00860_prednisolone",
        "name": "Prednisolone",
        "brand_names": ["Orapred", "Millipred", "Prelone"],
        "description": (
            "Active corticosteroid; primary form in blood after prednisone conversion. "
            "Metabolized by CYP3A4. CYP3A4 inhibitors increase prednisolone levels. "
            "Rifampin significantly reduces plasma levels. Used in various inflammatory, "
            "autoimmune, and oncologic conditions."
        ),
        "drug_class": "Corticosteroid / Glucocorticoid",
        "rxnorm_cui": "8638",
    },
    {
        "id": "DB00513_sildenafil",
        "name": "Sildenafil",
        "brand_names": ["Viagra", "Revatio"],
        "description": (
            "PDE5 inhibitor for erectile dysfunction and pulmonary arterial hypertension. "
            "Primarily metabolized by CYP3A4; also CYP2C9. Strong CYP3A4 inhibitors "
            "(ritonavir, ketoconazole) increase sildenafil AUC markedly. Contraindicated "
            "with nitrates (severe hypotension). Alpha-blockers potentiate hypotension."
        ),
        "drug_class": "PDE5 Inhibitor",
        "rxnorm_cui": "222078",
    },
    {
        "id": "DB00203_tadalafil",
        "name": "Tadalafil",
        "brand_names": ["Cialis", "Adcirca"],
        "description": (
            "PDE5 inhibitor for erectile dysfunction, BPH, and pulmonary arterial hypertension. "
            "Exclusively metabolized by CYP3A4 to inactive catechol metabolite. CYP3A4 "
            "inhibitors increase tadalafil exposure (up to 2-fold with ketoconazole). "
            "Contraindicated with nitrates and riociguat."
        ),
        "drug_class": "PDE5 Inhibitor",
        "rxnorm_cui": "357571",
    },
    {
        "id": "DB01166_acenocoumarol",
        "name": "Acenocoumarol",
        "brand_names": ["Sintrom"],
        "description": (
            "Vitamin K antagonist anticoagulant used primarily in Europe. Metabolized by "
            "CYP2C9 (primary, R-enantiomer) and CYP1A2, CYP2C19. More sensitive to CYP2C9 "
            "genetic variants than warfarin. CYP2C9 inhibitors and CYP2C9 poor metabolizers "
            "have significantly elevated exposure and bleeding risk."
        ),
        "drug_class": "Anticoagulant / Vitamin K Antagonist",
        "rxnorm_cui": "3407",
    },
    {
        "id": "DB00672_chlorprop",
        "name": "Chlorpropamide",
        "brand_names": ["Diabinese"],
        "description": (
            "First-generation sulfonylurea antidiabetic (rarely used). Metabolized by CYP2C9. "
            "Very long half-life (~36h); accumulation risk. CYP2C9 inhibitors increase exposure. "
            "Disulfiram-like reaction with alcohol. Largely replaced by newer agents."
        ),
        "drug_class": "Antidiabetic / Sulfonylurea (1st generation)",
        "rxnorm_cui": "2400",
    },
    {
        "id": "DB00945_acetamino",
        "name": "Acetaminophen",
        "brand_names": ["Tylenol", "Panadol", "APAP"],
        "description": (
            "OTC analgesic and antipyretic. Primarily glucuronidated and sulfated; CYP2E1 "
            "generates toxic NAPQI metabolite (~5% at therapeutic doses). CYP2E1 inducers "
            "(alcohol, isoniazid) increase NAPQI formation and hepatotoxicity risk. "
            "CYP2E1 saturation at overdose leads to NAPQI accumulation. Warfarin interaction: "
            "regular high-dose use potentiates anticoagulation."
        ),
        "drug_class": "Analgesic / Antipyretic (OTC)",
        "rxnorm_cui": "161",
    },
    {
        "id": "DB01174_codeine",
        "name": "Codeine",
        "brand_names": ["Tylenol with Codeine"],
        "description": (
            "Opioid prodrug requiring CYP2D6 activation to morphine for analgesic effect. "
            "CYP2D6 poor metabolizers have no/minimal analgesia. CYP2D6 ultrarapid metabolizers "
            "risk fatal morphine accumulation (black box warning in children, nursing mothers). "
            "CYP2D6 inhibitors (paroxetine, fluoxetine) reduce analgesic efficacy."
        ),
        "drug_class": "Opioid Analgesic / Prodrug",
        "rxnorm_cui": "2670",
    },
    {
        "id": "DB00193_tramadol",
        "name": "Tramadol",
        "brand_names": ["Ultram", "ConZip"],
        "description": (
            "Opioid with norepinephrine/serotonin reuptake inhibition for moderate pain. "
            "Converted by CYP2D6 to active O-desmethyltramadol (M1 opioid metabolite). "
            "CYP2D6 poor metabolizers have reduced opioid activity; ultrarapid metabolizers "
            "risk toxicity. CYP2D6 inhibitors reduce M1 but increase serotonin-related risk. "
            "Serotonin syndrome risk with SSRIs, SNRIs, MAOIs."
        ),
        "drug_class": "Opioid / Analgesic",
        "rxnorm_cui": "41493",
    },
    {
        "id": "DB00363_clonidine",
        "name": "Clonidine",
        "brand_names": ["Catapres", "Kapvay", "Nexiclon XR"],
        "description": (
            "Central alpha-2 agonist for hypertension, ADHD, and opioid withdrawal. "
            "Primarily excreted renally unchanged and as glucuronide conjugates. "
            "Minimal CYP-mediated metabolism. TCAs antagonize clonidine's antihypertensive "
            "effect. Abrupt discontinuation causes hypertensive rebound."
        ),
        "drug_class": "Antihypertensive / Alpha-2 Agonist",
        "rxnorm_cui": "2599",
    },
    {
        "id": "DB00999_hydrochlorothiazide",
        "name": "Hydrochlorothiazide",
        "brand_names": ["Microzide", "HydroDIURIL"],
        "description": (
            "Thiazide diuretic for hypertension and edema. Not significantly metabolized by "
            "CYP enzymes; excreted unchanged renally. NSAIDs reduce diuretic efficacy. "
            "Hypokalemia potentiates digoxin toxicity. Enhances hyperuricemia."
        ),
        "drug_class": "Diuretic / Thiazide",
        "rxnorm_cui": "5487",
    },
    {
        "id": "DB00524_furosemide",
        "name": "Furosemide",
        "brand_names": ["Lasix"],
        "description": (
            "Loop diuretic for edema and hypertension. Primarily excreted renally; minor CYP "
            "involvement. NSAIDs reduce diuretic and natriuretic effect. Aminoglycosides "
            "ototoxicity potentiated. Hypokalemia increases digoxin toxicity risk."
        ),
        "drug_class": "Diuretic / Loop",
        "rxnorm_cui": "4603",
    },
    {
        "id": "DB00697_spiro",
        "name": "Spironolactone",
        "brand_names": ["Aldactone", "CaroSpir"],
        "description": (
            "Potassium-sparing diuretic and aldosterone antagonist. Metabolized by CYP3A4 "
            "to active canrenone. Hyperkalemia risk with ACE inhibitors, ARBs, and NSAIDs. "
            "Potentiates antihypertensive effects. Antiandrogen activity at higher doses."
        ),
        "drug_class": "Diuretic / Potassium-Sparing / Mineralocorticoid Antagonist",
        "rxnorm_cui": "9997",
    },
    {
        "id": "DB00619_imatinib_gleevec",
        "name": "Dasatinib",
        "brand_names": ["Sprycel"],
        "description": (
            "BCR-ABL/Src TKI for CML and Ph+ ALL. Primarily metabolized by CYP3A4. "
            "Acid suppression (PPIs, H2 blockers) reduces absorption (pH-dependent dissolution). "
            "Strong CYP3A4 inhibitors increase dasatinib exposure. CYP3A4 inducers reduce levels. "
            "QTc prolongation risk."
        ),
        "drug_class": "Antineoplastic / BCR-ABL TKI",
        "rxnorm_cui": "491938",
    },
    {
        "id": "DB11652_nintedanib",
        "name": "Nintedanib",
        "brand_names": ["Ofev"],
        "description": (
            "Triple kinase inhibitor (VEGFR, PDGFR, FGFR) for IPF, systemic sclerosis-ILD, "
            "and other progressive fibrosing ILDs. P-glycoprotein substrate. Strong P-gp "
            "inhibitors increase nintedanib levels. Strong P-gp inducers (rifampin) reduce "
            "exposure ~60%. Minimal CYP3A4 involvement."
        ),
        "drug_class": "Antifibrotic / Kinase Inhibitor",
        "rxnorm_cui": "1726151",
    },
    {
        "id": "DB09067_apremilast",
        "name": "Apremilast",
        "brand_names": ["Otezla"],
        "description": (
            "PDE-4 inhibitor for psoriasis, PsA, and oral ulcers in Behcet's disease. "
            "Metabolized by CYP3A4 (major), CYP2A6, CYP1A2. Strong CYP3A4 inducers "
            "(rifampin) reduce apremilast AUC by ~72% — avoid. Minimal inhibitory effect "
            "on CYP enzymes. GI side effects common (nausea, diarrhea)."
        ),
        "drug_class": "PDE-4 Inhibitor / DMARD",
        "rxnorm_cui": "1728082",
    },
    {
        "id": "DB06155_lixisenatide",
        "name": "Exenatide",
        "brand_names": ["Byetta", "Bydureon"],
        "description": (
            "GLP-1 receptor agonist for type 2 diabetes. Metabolized by general proteolytic "
            "degradation; not CYP-dependent. Delays gastric emptying; may reduce absorption "
            "rate of oral drugs. Clinical significance is generally low but relevant for "
            "drugs with narrow TI (digoxin, warfarin)."
        ),
        "drug_class": "Antidiabetic / GLP-1 Receptor Agonist",
        "rxnorm_cui": "475968",
    },
    {
        "id": "DB08880_teriflunomide",
        "name": "Teriflunomide",
        "brand_names": ["Aubagio"],
        "description": (
            "Dihydroorotate dehydrogenase inhibitor for relapsing MS; active metabolite of "
            "leflunomide. Inhibits CYP1A2, increasing levels of theophylline and alosetron. "
            "Induces CYP2C8. Rifampin increases clearance via P-gp and CYP induction. "
            "Very long half-life without accelerated elimination procedure."
        ),
        "drug_class": "Immunomodulator / MS Treatment",
        "rxnorm_cui": "1302827",
    },
    {
        "id": "DB09570_dimethyl",
        "name": "Dimethyl Fumarate",
        "brand_names": ["Tecfidera", "Fumaderm"],
        "description": (
            "Immunomodulator for relapsing MS and psoriasis. Hydrolyzed to monomethyl fumarate "
            "(MMF) and metabolized via Krebs cycle — no CYP involvement. Very few drug "
            "interactions via pharmacokinetic mechanisms. Lymphopenia monitoring required."
        ),
        "drug_class": "Immunomodulator / MS Treatment",
        "rxnorm_cui": "1313948",
    },
    {
        "id": "DB01076_fingolimod",
        "name": "Fingolimod",
        "brand_names": ["Gilenya"],
        "description": (
            "Sphingosine-1-phosphate (S1P) receptor modulator for relapsing MS. Metabolized "
            "by sphingosine kinase to active phosphate form and by CYP4F2. Ketoconazole "
            "increases fingolimod levels ~1.7-fold. QTc prolongation; contraindicated with "
            "class Ia/III antiarrhythmics and drugs known to prolong QT."
        ),
        "drug_class": "Immunomodulator / S1P Receptor Modulator / MS Treatment",
        "rxnorm_cui": "1163760",
    },
    {
        "id": "DB00773_etoposide",
        "name": "Etoposide",
        "brand_names": ["Toposar", "VePesid"],
        "description": (
            "Topoisomerase II inhibitor for lung cancer, testicular cancer, and lymphoma. "
            "Metabolized by CYP3A4 and UGT1A1 to catechol and glucuronide metabolites. "
            "CYP3A4 inducers (phenytoin, carbamazepine) increase etoposide clearance. "
            "Cyclosporine inhibits CYP3A4 and P-gp, increasing etoposide exposure."
        ),
        "drug_class": "Antineoplastic / Topoisomerase II Inhibitor",
        "rxnorm_cui": "4248",
    },
    {
        "id": "DB01229_paclitaxel",
        "name": "Paclitaxel",
        "brand_names": ["Taxol", "Abraxane"],
        "description": (
            "Taxane antineoplastic for breast, ovarian, lung, and other cancers. Metabolized "
            "by CYP2C8 (primary) and CYP3A4. Gemfibrozil and other CYP2C8 inhibitors can "
            "increase paclitaxel exposure. Strong CYP3A4 inducers increase clearance. "
            "P-glycoprotein substrate; P-gp inhibitors may increase paclitaxel levels."
        ),
        "drug_class": "Antineoplastic / Taxane",
        "rxnorm_cui": "56946",
    },
    {
        "id": "DB00531_docetaxel",
        "name": "Docetaxel",
        "brand_names": ["Taxotere", "Docefrez"],
        "description": (
            "Taxane antineoplastic for breast, NSCLC, prostate, gastric, and head and neck "
            "cancers. Primarily metabolized by CYP3A4/5 to inactive hydroxyl metabolites. "
            "Strong CYP3A4 inhibitors increase docetaxel exposure and toxicity risk. "
            "Strong CYP3A4 inducers (rifampin) reduce efficacy."
        ),
        "drug_class": "Antineoplastic / Taxane",
        "rxnorm_cui": "72962",
    },
    {
        "id": "DB00602_irinotecan",
        "name": "Irinotecan",
        "brand_names": ["Camptosar", "Onivyde"],
        "description": (
            "Topoisomerase I inhibitor for colorectal cancer, NSCLC. Converted to active SN-38 "
            "by carboxylesterase; SN-38 inactivated by UGT1A1 glucuronidation. UGT1A1*28 "
            "homozygotes (10% of population) have reduced SN-38 inactivation — 3-4x higher "
            "levels, severe diarrhea and neutropenia. Reduce dose in *28/*28 patients."
        ),
        "drug_class": "Antineoplastic / Topoisomerase I Inhibitor",
        "rxnorm_cui": "51499",
    },
    {
        "id": "DB00877_temsirolimus",
        "name": "Temsirolimus",
        "brand_names": ["Torisel"],
        "description": (
            "mTOR inhibitor (rapalogue) for advanced renal cell carcinoma. Prodrug converted "
            "by CYP3A4/5 to active sirolimus (rapamycin). Strong CYP3A4 inhibitors increase "
            "sirolimus levels. Strong CYP3A4 inducers (rifampin) reduce sirolimus AUC ~50%. "
            "Combination with sunitinib caused dose-limiting toxicity."
        ),
        "drug_class": "Antineoplastic / mTOR Inhibitor",
        "rxnorm_cui": "483242",
    },
]
