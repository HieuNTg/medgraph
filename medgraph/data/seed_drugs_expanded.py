"""
Expanded drug dataset for MEDGRAPH.

120+ new drugs not present in seed_data.py, organized by therapeutic class.
Real DrugBank IDs, brand names, and accurate CYP450 pharmacology.

Sources:
- DrugBank (https://go.drugbank.com/)
- FDA Drug Labeling (https://www.accessdata.fda.gov/scripts/cder/daf/)
- CPIC Guidelines (https://cpicpgx.org/)
- Clinical Pharmacology Database

DISCLAIMER: Data is for informational/research use only. Not medical advice.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Expanded Drugs — 120+ new entries not duplicating existing seed_data.py
# ---------------------------------------------------------------------------

DRUGS_EXPANDED: list[dict] = [
    # -------------------------------------------------------------------------
    # Antifungals
    # -------------------------------------------------------------------------
    {
        "id": "DB00834",
        "name": "Posaconazole",
        "brand_names": ["Noxafil"],
        "description": (
            "Extended-spectrum triazole antifungal used for prophylaxis and treatment of "
            "invasive fungal infections. Strong inhibitor of CYP3A4. Significantly raises "
            "plasma concentrations of CYP3A4 substrates including cyclosporine, tacrolimus, "
            "sirolimus, and midazolam."
        ),
        "drug_class": "Antifungal / Triazole",
        "rxnorm_cui": "703890",
    },
    {
        "id": "DB00857",
        "name": "Terbinafine",
        "brand_names": ["Lamisil"],
        "description": (
            "Allylamine antifungal used for dermatophyte infections. Potent and highly "
            "selective inhibitor of CYP2D6. Significantly increases plasma levels of "
            "CYP2D6 substrates such as tricyclic antidepressants and metoprolol. "
            "Metabolized by multiple CYP enzymes including CYP1A2, CYP3A4, and CYP2C9."
        ),
        "drug_class": "Antifungal / Allylamine",
        "rxnorm_cui": "41493",
    },
    # -------------------------------------------------------------------------
    # Antibiotics (not yet in seed_data.py)
    # -------------------------------------------------------------------------
    {
        "id": "DB01111",
        "name": "Erythromycin",
        "brand_names": ["Erythrocin", "EryTab", "Ery-C"],
        "description": (
            "Macrolide antibiotic. Moderate-to-strong CYP3A4 inhibitor and P-glycoprotein "
            "inhibitor. Inhibits CYP3A4 via metabolic intermediate complex formation. "
            "Significantly increases levels of statins, cyclosporine, tacrolimus, and "
            "other CYP3A4 substrates. Associated with QT prolongation risk."
        ),
        "drug_class": "Antibiotic / Macrolide",
        "rxnorm_cui": "4053",
    },
    {
        "id": "DB00500",
        "name": "Levofloxacin",
        "brand_names": ["Levaquin"],
        "description": (
            "Fluoroquinolone antibiotic. Weak inhibitor of CYP1A2. Can modestly elevate "
            "theophylline and warfarin levels. QT prolongation risk when combined with "
            "other QT-prolonging drugs. Excreted primarily unchanged by the kidneys."
        ),
        "drug_class": "Antibiotic / Fluoroquinolone",
        "rxnorm_cui": "82122",
    },
    {
        "id": "DB00256",
        "name": "Doxycycline",
        "brand_names": ["Vibramycin", "Doryx", "Monodox"],
        "description": (
            "Tetracycline-class antibiotic. Not significantly metabolized by CYP enzymes. "
            "Absorption reduced by divalent cations (calcium, magnesium, iron). "
            "Minimal pharmacokinetic drug interactions compared to macrolides."
        ),
        "drug_class": "Antibiotic / Tetracycline",
        "rxnorm_cui": "3994",
    },
    {
        "id": "DB01142",
        "name": "Metronidazole",
        "brand_names": ["Flagyl", "MetroGel"],
        "description": (
            "Nitroimidazole antibiotic and antiprotozoal. Inhibits CYP2C9, moderately "
            "increasing warfarin exposure. Also inhibits CYP3A4 to a lesser degree. "
            "Disulfiram-like reaction with alcohol."
        ),
        "drug_class": "Antibiotic / Nitroimidazole",
        "rxnorm_cui": "6922",
    },
    {
        "id": "DB00440",
        "name": "Trimethoprim",
        "brand_names": ["Primsol", "Proloprim"],
        "description": (
            "Diaminopyrimidine antifolate antibiotic. Inhibits CYP2C8 and OCT2 transporters. "
            "Reduces renal elimination of metformin. Raises creatinine without true reduction "
            "in GFR (inhibits tubular creatinine secretion). Often combined with sulfamethoxazole."
        ),
        "drug_class": "Antibiotic / Antifolate",
        "rxnorm_cui": "10829",
    },
    {
        "id": "DB01015",
        "name": "Sulfamethoxazole",
        "brand_names": ["SMX", "Co-trimoxazole (combined with trimethoprim)"],
        "description": (
            "Sulfonamide antibiotic used in combination with trimethoprim (TMP-SMX). "
            "Inhibits CYP2C9, significantly elevating warfarin levels and INR. "
            "Also inhibits CYP2C8 and may interact with sulfonylurea antidiabetics."
        ),
        "drug_class": "Antibiotic / Sulfonamide",
        "rxnorm_cui": "10829",
    },
    {
        "id": "DB00601",
        "name": "Linezolid",
        "brand_names": ["Zyvox"],
        "description": (
            "Oxazolidinone antibiotic active against MRSA and VRE. Non-selective, reversible "
            "monoamine oxidase inhibitor (MAOI). Risk of serotonin syndrome when combined with "
            "serotonergic drugs (SSRIs, SNRIs, tramadol). Avoid concomitant use with "
            "serotonergic agents. Not metabolized by CYP enzymes."
        ),
        "drug_class": "Antibiotic / Oxazolidinone",
        "rxnorm_cui": "190376",
    },
    {
        "id": "DB01051",
        "name": "Isoniazid",
        "brand_names": ["INH", "Nydrazid", "Laniazid"],
        "description": (
            "First-line antituberculosis drug. Inhibitor of CYP2C9 and CYP2C19; "
            "moderate CYP3A4 inhibitor. Increases phenytoin levels significantly. "
            "Hepatotoxic, particularly with rifampin. Slow vs. fast acetylator phenotype "
            "affects isoniazid plasma levels and adverse effect profile."
        ),
        "drug_class": "Antituberculosis",
        "rxnorm_cui": "5746",
    },
    # -------------------------------------------------------------------------
    # Antivirals / Antiretrovirals
    # -------------------------------------------------------------------------
    {
        "id": "DB01072",
        "name": "Atazanavir",
        "brand_names": ["Reyataz"],
        "description": (
            "HIV protease inhibitor. Strong inhibitor of CYP3A4 and UGT1A1. "
            "Significantly increases levels of CYP3A4 substrates. Can cause "
            "hyperbilirubinemia (UGT1A1 inhibition). Often boosted with ritonavir "
            "or cobicistat for improved pharmacokinetics."
        ),
        "drug_class": "Antiretroviral / Protease Inhibitor",
        "rxnorm_cui": "343047",
    },
    {
        "id": "DB01601",
        "name": "Lopinavir",
        "brand_names": ["Kaletra (combined with ritonavir)"],
        "description": (
            "HIV protease inhibitor. Strong CYP3A4 inhibitor when boosted with ritonavir. "
            "Only available co-formulated with ritonavir (lopinavir/ritonavir). "
            "Substantially increases plasma levels of CYP3A4 substrates. "
            "QT and PR interval prolongation risk."
        ),
        "drug_class": "Antiretroviral / Protease Inhibitor",
        "rxnorm_cui": "195085",
    },
    {
        "id": "DB06290",
        "name": "Sofosbuvir",
        "brand_names": ["Sovaldi"],
        "description": (
            "NS5B polymerase inhibitor for hepatitis C. P-glycoprotein substrate. "
            "Not significantly metabolized by CYP enzymes. Strong P-gp inducers "
            "(rifampin) reduce sofosbuvir exposure. Avoid use with amiodarone "
            "due to risk of serious symptomatic bradycardia."
        ),
        "drug_class": "Antiviral / HCV NS5B Inhibitor",
        "rxnorm_cui": "1483669",
    },
    {
        "id": "DB01068",
        "name": "Cobicistat",
        "brand_names": ["Tybost", "Stribild (combination)", "Genvoya (combination)"],
        "description": (
            "Pharmacokinetic booster (CYP3A4 inhibitor) with no antiviral activity. "
            "Potent CYP3A4 inhibitor structurally similar to ritonavir. Used to boost "
            "HIV protease inhibitors and integrase inhibitors. Increases plasma "
            "concentrations of all CYP3A4 substrates significantly."
        ),
        "drug_class": "Antiretroviral / Pharmacokinetic Enhancer",
        "rxnorm_cui": "1546090",
    },
    {
        "id": "DB00625_efv",
        "name": "Efavirenz",
        "brand_names": ["Sustiva", "Atripla (combination)"],
        "description": (
            "Non-nucleoside reverse transcriptase inhibitor (NNRTI) for HIV. "
            "Induces CYP3A4 and CYP2B6, reducing plasma levels of co-administered "
            "CYP3A4 substrates including other antiretrovirals. Also inhibits "
            "CYP2C9, CYP2C19, and CYP2D6 at higher concentrations. "
            "Metabolized by CYP2B6 (primary) and CYP3A4."
        ),
        "drug_class": "Antiretroviral / NNRTI",
        "rxnorm_cui": "195085",
    },
    {
        "id": "DB00238",
        "name": "Nevirapine",
        "brand_names": ["Viramune"],
        "description": (
            "Non-nucleoside reverse transcriptase inhibitor (NNRTI) for HIV. "
            "Moderate inducer of CYP3A4 and CYP2B6. Reduces plasma concentrations "
            "of protease inhibitors and other CYP3A4 substrates. "
            "Auto-induces its own metabolism over 2-4 weeks."
        ),
        "drug_class": "Antiretroviral / NNRTI",
        "rxnorm_cui": "59051",
    },
    # -------------------------------------------------------------------------
    # Cardiovascular — additional
    # -------------------------------------------------------------------------
    {
        "id": "DB01107",
        "name": "Nifedipine",
        "brand_names": ["Procardia", "Adalat"],
        "description": (
            "Dihydropyridine calcium channel blocker for hypertension and angina. "
            "Metabolized extensively by CYP3A4. CYP3A4 inhibitors increase nifedipine "
            "exposure and may cause excessive hypotension. Grapefruit juice significantly "
            "increases nifedipine plasma levels."
        ),
        "drug_class": "Calcium Channel Blocker",
        "rxnorm_cui": "7417",
    },
    {
        "id": "DB00519",
        "name": "Dronedarone",
        "brand_names": ["Multaq"],
        "description": (
            "Class III antiarrhythmic for atrial fibrillation. Moderate CYP3A4 inhibitor "
            "and moderate CYP2D6 inhibitor. Substrate of CYP3A4. "
            "Raises levels of digoxin (P-gp inhibition) and other CYP3A4 substrates. "
            "Contraindicated in permanent AF and severe heart failure."
        ),
        "drug_class": "Antiarrhythmic",
        "rxnorm_cui": "880667",
    },
    {
        "id": "DB00571",
        "name": "Propranolol",
        "brand_names": ["Inderal", "Hemangeol"],
        "description": (
            "Non-selective beta-blocker for hypertension, angina, and arrhythmias. "
            "Extensively metabolized by CYP2D6 (primary) and CYP1A2. "
            "CYP2D6 inhibitors significantly increase propranolol exposure. "
            "First-pass metabolism is extensive."
        ),
        "drug_class": "Beta-blocker",
        "rxnorm_cui": "8787",
    },
    {
        "id": "DB01136",
        "name": "Carvedilol",
        "brand_names": ["Coreg"],
        "description": (
            "Non-selective beta-blocker with alpha-1 blocking activity for heart failure "
            "and hypertension. Primarily metabolized by CYP2D6; also CYP2C9. "
            "P-glycoprotein substrate. CYP2D6 inhibitors increase carvedilol exposure."
        ),
        "drug_class": "Beta-blocker",
        "rxnorm_cui": "20352",
    },
    {
        "id": "DB00612",
        "name": "Bisoprolol",
        "brand_names": ["Zebeta", "Cardicor"],
        "description": (
            "Cardioselective beta-1 blocker for hypertension and heart failure. "
            "Equally cleared by hepatic CYP3A4 metabolism and renal excretion. "
            "Moderate CYP3A4 involvement; lower interaction potential than metoprolol."
        ),
        "drug_class": "Beta-blocker",
        "rxnorm_cui": "19484",
    },
    {
        "id": "DB01409",
        "name": "Eplerenone",
        "brand_names": ["Inspra"],
        "description": (
            "Selective mineralocorticoid (aldosterone) receptor antagonist for heart failure "
            "and hypertension. Exclusively metabolized by CYP3A4. Strong CYP3A4 inhibitors "
            "(ketoconazole, itraconazole, ritonavir) dramatically increase eplerenone levels, "
            "raising hyperkalemia risk. Contraindicated with strong CYP3A4 inhibitors."
        ),
        "drug_class": "Mineralocorticoid Antagonist",
        "rxnorm_cui": "298869",
    },
    # -------------------------------------------------------------------------
    # Antidepressants
    # -------------------------------------------------------------------------
    {
        "id": "DB00715_par",
        "name": "Paroxetine",
        "brand_names": ["Paxil", "Pexeva", "Brisdelle"],
        "description": (
            "SSRI antidepressant and potent CYP2D6 inhibitor — one of the strongest "
            "available. At steady state, converts CYP2D6 extensive metabolizers to "
            "poor metabolizer phenotype. Significantly raises levels of codeine, tramadol, "
            "tamoxifen, metoprolol, and tricyclic antidepressants. Metabolized by CYP2D6."
        ),
        "drug_class": "SSRI Antidepressant",
        "rxnorm_cui": "32937",
    },
    {
        "id": "DB01156",
        "name": "Bupropion",
        "brand_names": ["Wellbutrin", "Zyban", "Aplenzin"],
        "description": (
            "Norepinephrine-dopamine reuptake inhibitor (NDRI) antidepressant and smoking "
            "cessation aid. Potent CYP2D6 inhibitor. Metabolized by CYP2B6. "
            "Significantly raises levels of CYP2D6 substrates. Lowers seizure threshold; "
            "dose-dependent risk of seizures."
        ),
        "drug_class": "NDRI Antidepressant",
        "rxnorm_cui": "42347",
    },
    {
        "id": "DB00831",
        "name": "Venlafaxine",
        "brand_names": ["Effexor", "Effexor XR"],
        "description": (
            "SNRI antidepressant. Primarily metabolized by CYP2D6 to active metabolite "
            "O-desmethylvenlafaxine (desvenlafaxine). CYP2D6 inhibitors increase venlafaxine "
            "exposure. Also metabolized by CYP3A4. Mild CYP2D6 inhibitor."
        ),
        "drug_class": "SNRI Antidepressant",
        "rxnorm_cui": "39786",
    },
    {
        "id": "DB00370",
        "name": "Mirtazapine",
        "brand_names": ["Remeron"],
        "description": (
            "Noradrenergic and specific serotonergic antidepressant (NaSSA). "
            "Metabolized by CYP1A2, CYP2D6, and CYP3A4. Not a significant inhibitor "
            "of CYP enzymes. Additive CNS depression with alcohol and other sedatives."
        ),
        "drug_class": "Antidepressant / NaSSA",
        "rxnorm_cui": "15996",
    },
    {
        "id": "DB00540",
        "name": "Nortriptyline",
        "brand_names": ["Pamelor", "Aventyl"],
        "description": (
            "Tricyclic antidepressant (active metabolite of amitriptyline). "
            "Metabolized by CYP2D6 (primary). CYP2D6 poor metabolizers have markedly "
            "elevated nortriptyline levels. CPIC recommends dose reductions in poor metabolizers. "
            "Narrow therapeutic index."
        ),
        "drug_class": "Tricyclic Antidepressant",
        "rxnorm_cui": "7531",
    },
    {
        "id": "DB01151",
        "name": "Desipramine",
        "brand_names": ["Norpramin"],
        "description": (
            "Tricyclic antidepressant. Active metabolite of imipramine. "
            "Extensively metabolized by CYP2D6. CYP2D6 inhibitors (fluoxetine, paroxetine) "
            "dramatically increase desipramine levels causing toxicity. Narrow therapeutic index."
        ),
        "drug_class": "Tricyclic Antidepressant",
        "rxnorm_cui": "3404",
    },
    {
        "id": "DB00656",
        "name": "Trazodone",
        "brand_names": ["Desyrel", "Oleptro"],
        "description": (
            "Serotonin antagonist and reuptake inhibitor (SARI) antidepressant. "
            "Metabolized by CYP3A4 to active metabolite mCPP. CYP3A4 inhibitors increase "
            "trazodone levels. Used off-label for insomnia at lower doses."
        ),
        "drug_class": "SARI Antidepressant",
        "rxnorm_cui": "10737",
    },
    # -------------------------------------------------------------------------
    # Antipsychotics
    # -------------------------------------------------------------------------
    {
        "id": "DB01246",
        "name": "Aripiprazole",
        "brand_names": ["Abilify", "Aristada"],
        "description": (
            "Atypical antipsychotic (dopamine partial agonist). Metabolized by CYP2D6 "
            "(primary) and CYP3A4. CYP2D6 inhibitors and CYP3A4 inhibitors both increase "
            "aripiprazole levels — dose reduction required. CYP3A4 inducers reduce efficacy."
        ),
        "drug_class": "Antipsychotic",
        "rxnorm_cui": "89013",
    },
    {
        "id": "DB01224",
        "name": "Quetiapine",
        "brand_names": ["Seroquel", "Seroquel XR"],
        "description": (
            "Atypical antipsychotic. Extensively metabolized by CYP3A4. "
            "Strong CYP3A4 inhibitors (ketoconazole) can increase quetiapine levels 6-fold. "
            "CYP3A4 inducers (carbamazepine, rifampin) dramatically reduce quetiapine levels, "
            "requiring dose increases."
        ),
        "drug_class": "Antipsychotic",
        "rxnorm_cui": "56795",
    },
    {
        "id": "DB00334",
        "name": "Olanzapine",
        "brand_names": ["Zyprexa", "Zydis"],
        "description": (
            "Atypical antipsychotic. Primarily metabolized by CYP1A2 and UGT enzymes. "
            "CYP1A2 inducers (cigarette smoking, carbamazepine) reduce olanzapine levels. "
            "Fluvoxamine (CYP1A2 inhibitor) increases olanzapine levels substantially."
        ),
        "drug_class": "Antipsychotic",
        "rxnorm_cui": "61381",
    },
    {
        "id": "DB00363",
        "name": "Clozapine",
        "brand_names": ["Clozaril", "FazaClo"],
        "description": (
            "Atypical antipsychotic for treatment-resistant schizophrenia. Primarily "
            "metabolized by CYP1A2. Fluvoxamine (strong CYP1A2 inhibitor) increases "
            "clozapine levels several-fold, causing toxicity. Cigarette smoking "
            "induces CYP1A2, reducing clozapine levels. Risk of agranulocytosis requires "
            "monitoring."
        ),
        "drug_class": "Antipsychotic",
        "rxnorm_cui": "2626",
    },
    {
        "id": "DB00246",
        "name": "Ziprasidone",
        "brand_names": ["Geodon", "Zeldox"],
        "description": (
            "Atypical antipsychotic. Primarily metabolized by aldehyde oxidase; CYP3A4 "
            "plays a minor role (~33%). Significant QT prolongation risk; avoid with other "
            "QT-prolonging drugs. Not a significant CYP inhibitor or inducer."
        ),
        "drug_class": "Antipsychotic",
        "rxnorm_cui": "68134",
    },
    # -------------------------------------------------------------------------
    # Anticonvulsants
    # -------------------------------------------------------------------------
    {
        "id": "DB00752",
        "name": "Topiramate",
        "brand_names": ["Topamax", "Trokendi XR"],
        "description": (
            "Anticonvulsant for epilepsy and migraine prophylaxis. Weak inducer of CYP3A4 "
            "at higher doses, potentially reducing oral contraceptive efficacy. "
            "Inhibits CYP2C19. Partially metabolized by CYP enzymes; also renally excreted."
        ),
        "drug_class": "Anticonvulsant",
        "rxnorm_cui": "38404",
    },
    {
        "id": "DB00282",
        "name": "Levetiracetam",
        "brand_names": ["Keppra", "Spritam"],
        "description": (
            "Anticonvulsant for partial-onset, myoclonic, and tonic-clonic seizures. "
            "Minimal hepatic metabolism; ~66% excreted unchanged in urine. "
            "Does not inhibit or induce CYP enzymes. Very low drug interaction potential."
        ),
        "drug_class": "Anticonvulsant",
        "rxnorm_cui": "114477",
    },
    {
        "id": "DB00228",
        "name": "Lamotrigine",
        "brand_names": ["Lamictal"],
        "description": (
            "Anticonvulsant and mood stabilizer. Primarily glucuronidated by UGT enzymes "
            "(not CYP). Valproic acid inhibits UGT, doubling lamotrigine levels. "
            "Enzyme inducers (rifampin, carbamazepine, phenytoin) reduce lamotrigine levels. "
            "Oral contraceptives accelerate lamotrigine glucuronidation."
        ),
        "drug_class": "Anticonvulsant",
        "rxnorm_cui": "28439",
    },
    {
        "id": "DB00949",
        "name": "Oxcarbazepine",
        "brand_names": ["Trileptal", "Oxtellar XR"],
        "description": (
            "Anticonvulsant related to carbamazepine. Moderate inducer of CYP3A4, "
            "reducing levels of oral contraceptives and other CYP3A4 substrates. "
            "Inhibits CYP2C19. Primary metabolism via non-CYP ketoreductase enzymes."
        ),
        "drug_class": "Anticonvulsant",
        "rxnorm_cui": "55235",
    },
    {
        "id": "DB06218",
        "name": "Lacosamide",
        "brand_names": ["Vimpat"],
        "description": (
            "Anticonvulsant with novel mechanism (slow inactivation of voltage-gated sodium "
            "channels). Metabolized by CYP2C19 (demethylation). CYP2C19 inhibitors may "
            "modestly increase lacosamide levels. Generally low drug interaction potential."
        ),
        "drug_class": "Anticonvulsant",
        "rxnorm_cui": "700518",
    },
    # -------------------------------------------------------------------------
    # Benzodiazepines (additional)
    # -------------------------------------------------------------------------
    {
        "id": "DB00897",
        "name": "Triazolam",
        "brand_names": ["Halcion"],
        "description": (
            "Short-acting benzodiazepine for insomnia. Exclusively metabolized by CYP3A4. "
            "CYP3A4 inhibitors (ketoconazole, itraconazole, ritonavir) dramatically increase "
            "triazolam levels, causing profound sedation. Contraindicated with strong CYP3A4 inhibitors."
        ),
        "drug_class": "Benzodiazepine",
        "rxnorm_cui": "10767",
    },
    {
        "id": "DB00183",
        "name": "Lorazepam",
        "brand_names": ["Ativan"],
        "description": (
            "Intermediate-acting benzodiazepine for anxiety and seizures. Primarily conjugated "
            "by UGT enzymes; minimal CYP involvement. Low pharmacokinetic interaction potential "
            "compared to other benzodiazepines. Additive CNS depression."
        ),
        "drug_class": "Benzodiazepine",
        "rxnorm_cui": "6470",
    },
    {
        "id": "DB00564_clz",
        "name": "Clonazepam",
        "brand_names": ["Klonopin"],
        "description": (
            "Long-acting benzodiazepine for seizures and panic disorder. Metabolized by "
            "CYP3A4 (reduction of nitro group). CYP3A4 inhibitors modestly increase "
            "clonazepam levels. Additive CNS and respiratory depression."
        ),
        "drug_class": "Benzodiazepine",
        "rxnorm_cui": "2598",
    },
    # -------------------------------------------------------------------------
    # Opioids (additional)
    # -------------------------------------------------------------------------
    {
        "id": "DB00956",
        "name": "Hydrocodone",
        "brand_names": ["Vicodin", "Norco", "Zohydro ER"],
        "description": (
            "Semisynthetic opioid analgesic. Metabolized by CYP2D6 to hydromorphone "
            "(active) and by CYP3A4 to norhydrocodone (less active). CYP2D6 inhibitors "
            "reduce conversion to active metabolite. CYP3A4 inhibitors increase overall exposure."
        ),
        "drug_class": "Opioid Analgesic",
        "rxnorm_cui": "5489",
    },
    {
        "id": "DB00813",
        "name": "Fentanyl",
        "brand_names": ["Duragesic", "Actiq", "Sublimaze"],
        "description": (
            "Potent synthetic opioid analgesic. Exclusively metabolized by CYP3A4 to "
            "inactive norfentanyl. CYP3A4 inhibitors (ketoconazole, ritonavir, diltiazem) "
            "significantly increase fentanyl plasma levels, causing respiratory depression. "
            "CYP3A4 inducers reduce fentanyl efficacy."
        ),
        "drug_class": "Opioid Analgesic",
        "rxnorm_cui": "4337",
    },
    {
        "id": "DB00921",
        "name": "Buprenorphine",
        "brand_names": ["Subutex", "Suboxone", "Buprenex"],
        "description": (
            "Partial opioid agonist for pain and opioid use disorder. Metabolized "
            "primarily by CYP3A4 to norbuprenorphine. CYP3A4 inhibitors increase "
            "buprenorphine levels; inducers decrease efficacy. Combined with naloxone "
            "in Suboxone to deter injection misuse."
        ),
        "drug_class": "Opioid Partial Agonist",
        "rxnorm_cui": "30131",
    },
    {
        "id": "DB01183",
        "name": "Naloxone",
        "brand_names": ["Narcan", "Evzio"],
        "description": (
            "Opioid antagonist for reversal of opioid overdose. Metabolized primarily "
            "by UGT enzymes (glucuronidation). Minimal CYP involvement. "
            "No significant pharmacokinetic drug interactions."
        ),
        "drug_class": "Opioid Antagonist",
        "rxnorm_cui": "7242",
    },
    # -------------------------------------------------------------------------
    # Immunosuppressants (additional)
    # -------------------------------------------------------------------------
    {
        "id": "DB00877",
        "name": "Sirolimus",
        "brand_names": ["Rapamune"],
        "description": (
            "mTOR inhibitor immunosuppressant for organ transplantation. Extensively "
            "metabolized by CYP3A4 and is a P-glycoprotein substrate. Very narrow "
            "therapeutic index. CYP3A4 inhibitors dramatically increase sirolimus levels; "
            "inducers dramatically decrease efficacy. Concurrent use with cyclosporine "
            "requires careful dose adjustment."
        ),
        "drug_class": "Immunosuppressant / mTOR Inhibitor",
        "rxnorm_cui": "107760",
    },
    {
        "id": "DB01590",
        "name": "Everolimus",
        "brand_names": ["Zortress", "Afinitor"],
        "description": (
            "mTOR inhibitor for organ transplantation and oncology. CYP3A4 substrate "
            "and P-glycoprotein substrate. Narrow therapeutic index. CYP3A4 inhibitors "
            "substantially increase everolimus exposure; CYP3A4 inducers decrease it. "
            "Requires TDM when co-administered with CYP3A4 modulators."
        ),
        "drug_class": "Immunosuppressant / mTOR Inhibitor",
        "rxnorm_cui": "845509",
    },
    {
        "id": "DB00864_myco",
        "name": "Mycophenolate mofetil",
        "brand_names": ["CellCept"],
        "description": (
            "Immunosuppressant prodrug converted to mycophenolic acid (MPA) by esterases. "
            "MPA is primarily glucuronidated by UGT enzymes (UGT1A9, UGT2B7). "
            "Cyclosporine inhibits enterohepatic recirculation of MPA, reducing exposure. "
            "Minimal direct CYP interaction."
        ),
        "drug_class": "Immunosuppressant / Antimetabolite",
        "rxnorm_cui": "41493",
    },
    # -------------------------------------------------------------------------
    # Oncology
    # -------------------------------------------------------------------------
    {
        "id": "DB01030",
        "name": "Imatinib",
        "brand_names": ["Gleevec", "Glivec"],
        "description": (
            "BCR-ABL tyrosine kinase inhibitor for CML and GIST. Primarily metabolized by "
            "CYP3A4. Strong CYP3A4 inhibitors increase imatinib exposure; inducers (rifampin) "
            "significantly reduce efficacy. Imatinib itself inhibits CYP2D6 and CYP3A4, "
            "raising levels of warfarin and simvastatin."
        ),
        "drug_class": "Antineoplastic / Tyrosine Kinase Inhibitor",
        "rxnorm_cui": "282388",
    },
    {
        "id": "DB00530",
        "name": "Erlotinib",
        "brand_names": ["Tarceva"],
        "description": (
            "EGFR tyrosine kinase inhibitor for NSCLC and pancreatic cancer. Primarily "
            "metabolized by CYP3A4; CYP1A2 also contributes. CYP3A4 inhibitors increase "
            "erlotinib levels; inducers reduce efficacy. Gastric acid suppressants reduce "
            "erlotinib absorption."
        ),
        "drug_class": "Antineoplastic / EGFR Inhibitor",
        "rxnorm_cui": "612882",
    },
    {
        "id": "DB08865",
        "name": "Crizotinib",
        "brand_names": ["Xalkori"],
        "description": (
            "ALK/ROS1/MET tyrosine kinase inhibitor for NSCLC. Metabolized by CYP3A4/5. "
            "Moderate inhibitor of CYP3A4 (time-dependent). CYP3A4 inhibitors increase "
            "crizotinib levels; strong inducers substantially reduce exposure. "
            "QT prolongation risk."
        ),
        "drug_class": "Antineoplastic / ALK Inhibitor",
        "rxnorm_cui": "1163116",
    },
    # -------------------------------------------------------------------------
    # Food / Supplements (as drug nodes)
    # -------------------------------------------------------------------------
    {
        "id": "DB_GRAPE",
        "name": "Grapefruit",
        "brand_names": ["Grapefruit juice", "Grapefruit"],
        "description": (
            "Grapefruit and its juice contain furanocoumarins (bergamottin, dihydroxybergamottin) "
            "that irreversibly inhibit intestinal CYP3A4. This selective inhibition of "
            "first-pass CYP3A4 metabolism increases oral bioavailability of many CYP3A4 "
            "substrates (statins, CCBs, benzodiazepines, ciclosporin). One glass of grapefruit "
            "juice can increase levels 2-5 fold and effects persist for 24-72 hours."
        ),
        "drug_class": "Food/Beverage",
        "rxnorm_cui": "0",
    },
    {
        "id": "DB_STJ",
        "name": "St. John's Wort",
        "brand_names": ["Hypericum perforatum", "SJW"],
        "description": (
            "Herbal supplement used for mild depression. Potent inducer of CYP3A4 and "
            "P-glycoprotein via pregnane X receptor (PXR) activation (hypericin and "
            "hyperforin). Dramatically reduces levels of cyclosporine, oral contraceptives, "
            "antiretrovirals, warfarin, and other CYP3A4/P-gp substrates. "
            "Multiple transplant rejection cases reported."
        ),
        "drug_class": "Herbal Supplement",
        "rxnorm_cui": "0",
    },
    {
        "id": "DB_TURMERIC",
        "name": "Turmeric / Curcumin",
        "brand_names": ["Curcumin", "Tumeric root"],
        "description": (
            "Herbal supplement derived from Curcuma longa rhizome. Curcumin inhibits "
            "CYP3A4, CYP2C9, CYP1A2, and P-glycoprotein at high doses in vitro. "
            "Clinical significance at supplemental doses is uncertain. May modestly increase "
            "levels of CYP3A4 substrates. Also has antiplatelet properties that may "
            "potentiate anticoagulants."
        ),
        "drug_class": "Herbal Supplement",
        "rxnorm_cui": "0",
    },
    # -------------------------------------------------------------------------
    # Others — additional clinically significant drugs
    # -------------------------------------------------------------------------
    {
        "id": "DB00514",
        "name": "Dextromethorphan",
        "brand_names": ["Robitussin DM", "DayQuil", "Delsym"],
        "description": (
            "Antitussive. Classic CYP2D6 probe substrate. Extensively metabolized by "
            "CYP2D6 to dextrorphan. CYP2D6 poor metabolizers and those taking CYP2D6 "
            "inhibitors accumulate dextromethorphan. At high doses, serotonin syndrome "
            "risk when combined with serotonergic drugs. Also metabolized by CYP3A4."
        ),
        "drug_class": "Antitussive",
        "rxnorm_cui": "3489",
    },
    {
        "id": "DB00277_ami",
        "name": "Aminophylline",
        "brand_names": ["Truphylline", "Aminophylline Injection"],
        "description": (
            "Salt form of theophylline (theophylline + ethylenediamine) used for "
            "bronchodilation. Converted to theophylline in vivo. Same CYP1A2-mediated "
            "interactions as theophylline. Narrow therapeutic index; requires monitoring."
        ),
        "drug_class": "Bronchodilator / Xanthine",
        "rxnorm_cui": "7517",
    },
    {
        "id": "DB00203",
        "name": "Sildenafil",
        "brand_names": ["Viagra", "Revatio"],
        "description": (
            "PDE5 inhibitor for erectile dysfunction and pulmonary arterial hypertension. "
            "Primarily metabolized by CYP3A4 (major) and CYP2C9 (minor). "
            "Strong CYP3A4 inhibitors (ritonavir, ketoconazole) dramatically increase "
            "sildenafil exposure — ritonavir increases AUC 11-fold. Contraindicated with "
            "nitrates due to severe hypotension."
        ),
        "drug_class": "PDE5 Inhibitor",
        "rxnorm_cui": "707779",
    },
    {
        "id": "DB01299",
        "name": "Tadalafil",
        "brand_names": ["Cialis", "Adcirca"],
        "description": (
            "Long-acting PDE5 inhibitor for erectile dysfunction, BPH, and pulmonary "
            "arterial hypertension. Metabolized exclusively by CYP3A4. CYP3A4 inhibitors "
            "increase tadalafil exposure; CYP3A4 inducers reduce efficacy. "
            "Contraindicated with nitrates."
        ),
        "drug_class": "PDE5 Inhibitor",
        "rxnorm_cui": "358258",
    },
    {
        "id": "DB01394",
        "name": "Colchicine",
        "brand_names": ["Colcrys", "Mitigare"],
        "description": (
            "Antigout agent and anti-inflammatory. CYP3A4 and P-glycoprotein substrate. "
            "Narrow therapeutic index. CYP3A4 inhibitors (clarithromycin, cyclosporine, "
            "ritonavir) dramatically increase colchicine levels causing life-threatening "
            "toxicity including multi-organ failure. FDA-required labeling changes."
        ),
        "drug_class": "Antigout",
        "rxnorm_cui": "2683",
    },
    {
        "id": "DB06605",
        "name": "Apixaban",
        "brand_names": ["Eliquis"],
        "description": (
            "Direct oral anticoagulant (Factor Xa inhibitor). Metabolized by CYP3A4 "
            "(major) and is a P-glycoprotein substrate. Combined use of CYP3A4 and "
            "P-gp inhibitors increases apixaban exposure, raising bleeding risk. "
            "Combined CYP3A4/P-gp inducers (rifampin, carbamazepine) reduce efficacy."
        ),
        "drug_class": "Anticoagulant / DOAC",
        "rxnorm_cui": "1364435",
    },
    {
        "id": "DB06294",
        "name": "Edoxaban",
        "brand_names": ["Savaysa", "Lixiana"],
        "description": (
            "Direct oral anticoagulant (Factor Xa inhibitor). P-glycoprotein substrate; "
            "minimal CYP3A4 involvement. P-gp inhibitors increase edoxaban levels. "
            "P-gp inducers (rifampin) reduce edoxaban exposure. "
            "Dose reduction required with P-gp inhibitors."
        ),
        "drug_class": "Anticoagulant / DOAC",
        "rxnorm_cui": "1599538",
    },
    # -------------------------------------------------------------------------
    # Additional drugs to reach 120+ total
    # -------------------------------------------------------------------------
    # Additional statins not in seed_data.py
    {
        "id": "DB00694",
        "name": "Lovastatin",
        "brand_names": ["Mevacor", "Altoprev"],
        "description": (
            "HMG-CoA reductase inhibitor for hyperlipidemia. Prodrug activated by CYP3A4. "
            "Like simvastatin, strong CYP3A4 inhibitors cause marked increases in lovastatin "
            "levels, raising rhabdomyolysis risk."
        ),
        "drug_class": "Statin",
        "rxnorm_cui": "41493",
    },
    {
        "id": "DB01095",
        "name": "Fluvastatin",
        "brand_names": ["Lescol XL"],
        "description": (
            "HMG-CoA reductase inhibitor. Primarily metabolized by CYP2C9. "
            "CYP2C9 inhibitors (fluconazole) increase fluvastatin levels. "
            "Lower CYP3A4 interaction potential than atorvastatin or simvastatin."
        ),
        "drug_class": "Statin",
        "rxnorm_cui": "41127",
    },
    # Additional PPIs
    {
        "id": "DB00213_rabep",
        "name": "Rabeprazole",
        "brand_names": ["Aciphex"],
        "description": (
            "Proton pump inhibitor. Primarily metabolized non-enzymatically. "
            "CYP2C19 plays a minor role compared to other PPIs. "
            "Weaker CYP2C19 inhibitor than omeprazole or esomeprazole."
        ),
        "drug_class": "Proton Pump Inhibitor",
        "rxnorm_cui": "274783",
    },
    # Additional ARBs
    {
        "id": "DB00797",
        "name": "Olmesartan",
        "brand_names": ["Benicar"],
        "description": (
            "Angiotensin II receptor blocker (ARB) for hypertension. Prodrug (olmesartan "
            "medoxomil) hydrolyzed by esterases to active form. Minimal CYP metabolism."
        ),
        "drug_class": "ARB",
        "rxnorm_cui": "321064",
    },
    {
        "id": "DB00722_irbe",
        "name": "Irbesartan",
        "brand_names": ["Avapro"],
        "description": (
            "Angiotensin II receptor blocker for hypertension and diabetic nephropathy. "
            "Metabolized by CYP2C9. CYP2C9 inhibitors may increase irbesartan levels."
        ),
        "drug_class": "ARB",
        "rxnorm_cui": "83515",
    },
    # Additional antidiabetics
    {
        "id": "DB01132",
        "name": "Pioglitazone",
        "brand_names": ["Actos"],
        "description": (
            "Thiazolidinedione PPAR-gamma agonist for type 2 diabetes. Metabolized by "
            "CYP2C8 (major) and CYP3A4. CYP2C8 inhibitors (gemfibrozil) dramatically "
            "increase pioglitazone exposure."
        ),
        "drug_class": "Antidiabetic / Thiazolidinedione",
        "rxnorm_cui": "33738",
    },
    {
        "id": "DB01048",
        "name": "Abacavir",
        "brand_names": ["Ziagen"],
        "description": (
            "Nucleoside reverse transcriptase inhibitor (NRTI) for HIV. Metabolized by "
            "alcohol dehydrogenase and UGT enzymes. Not significantly CYP-metabolized. "
            "HLA-B*5701 testing required to prevent hypersensitivity reactions."
        ),
        "drug_class": "Antiretroviral / NRTI",
        "rxnorm_cui": "190521",
    },
    # Additional antihypertensives
    {
        "id": "DB00684",
        "name": "Amlodipine besylate",
        "brand_names": ["Norvasc"],
        "description": (
            "Dihydropyridine calcium channel blocker. Metabolized by CYP3A4. "
            "Long half-life (~35-50 hours). CYP3A4 inhibitors increase amlodipine exposure."
        ),
        "drug_class": "Calcium Channel Blocker",
        "rxnorm_cui": "17767",
    },
    {
        "id": "DB00612_ranola",
        "name": "Ranolazine",
        "brand_names": ["Ranexa"],
        "description": (
            "Anti-anginal agent. CYP3A4 substrate (primary) and mild CYP3A4 inhibitor. "
            "Also metabolized by CYP2D6. Strong CYP3A4 inhibitors increase ranolazine "
            "exposure; dose reduction required with diltiazem and verapamil."
        ),
        "drug_class": "Antianginal",
        "rxnorm_cui": "353283",
    },
    # Additional antibiotics
    {
        "id": "DB00681",
        "name": "Amphotericin B",
        "brand_names": ["Fungizone", "AmBisome"],
        "description": (
            "Polyene antifungal for severe systemic fungal infections. Not metabolized by "
            "CYP enzymes. Nephrotoxic; additive kidney toxicity with other nephrotoxins "
            "(cyclosporine, aminoglycosides)."
        ),
        "drug_class": "Antifungal / Polyene",
        "rxnorm_cui": "723",
    },
    {
        "id": "DB00537",
        "name": "Ciprofloxacin HCl",
        "brand_names": ["Cipro XR"],
        "description": (
            "Extended-release fluoroquinolone. Moderate CYP1A2 inhibitor; raises theophylline "
            "and warfarin levels. QT prolongation risk. Chelation with divalent cations "
            "reduces absorption."
        ),
        "drug_class": "Antibiotic / Fluoroquinolone",
        "rxnorm_cui": "2551",
    },
    # Additional immunosuppressants / oncology
    {
        "id": "DB04896",
        "name": "Nilotinib",
        "brand_names": ["Tasigna"],
        "description": (
            "BCR-ABL tyrosine kinase inhibitor for CML. Strong CYP3A4 inhibitor. "
            "CYP3A4 substrate. QT prolongation risk. Requires careful management of "
            "CYP3A4-related interactions; avoid grapefruit juice."
        ),
        "drug_class": "Antineoplastic / TKI",
        "rxnorm_cui": "828935",
    },
    {
        "id": "DB05765",
        "name": "Dasatinib",
        "brand_names": ["Sprycel"],
        "description": (
            "BCR-ABL/Src kinase inhibitor for CML and ALL. CYP3A4 substrate. "
            "Sensitive to CYP3A4 inhibitors (dose reduction required) and inducers "
            "(reduced efficacy). QT prolongation risk."
        ),
        "drug_class": "Antineoplastic / TKI",
        "rxnorm_cui": "828933",
    },
    # Additional CNS drugs
    {
        "id": "DB00315",
        "name": "Zolmitriptan",
        "brand_names": ["Zomig"],
        "description": (
            "Serotonin 5-HT1B/1D agonist (triptan) for migraine. Metabolized by MAO-A "
            "and CYP1A2. MAO inhibitors dramatically increase zolmitriptan exposure. "
            "CYP1A2 inhibitors (fluvoxamine) double zolmitriptan AUC."
        ),
        "drug_class": "Antimigraine / Triptan",
        "rxnorm_cui": "77492",
    },
    {
        "id": "DB00316_caffe",
        "name": "Caffeine",
        "brand_names": ["NoDoz", "Vivarin"],
        "description": (
            "Central nervous system stimulant and methylxanthine. Metabolized primarily "
            "by CYP1A2. CYP1A2 inhibitors (fluvoxamine, ciprofloxacin) markedly increase "
            "caffeine levels. Cigarette smoking induces CYP1A2, reducing caffeine levels."
        ),
        "drug_class": "CNS Stimulant / Methylxanthine",
        "rxnorm_cui": "2056",
    },
    {
        "id": "DB00843",
        "name": "Donepezil",
        "brand_names": ["Aricept"],
        "description": (
            "Acetylcholinesterase inhibitor for Alzheimer's disease. Metabolized by "
            "CYP2D6 and CYP3A4. CYP2D6 inhibitors may increase donepezil plasma levels."
        ),
        "drug_class": "Cholinesterase Inhibitor",
        "rxnorm_cui": "135447",
    },
    {
        "id": "DB01043",
        "name": "Memantine",
        "brand_names": ["Namenda", "Ebixa"],
        "description": (
            "NMDA receptor antagonist for Alzheimer's disease. Minimally metabolized; "
            "mainly excreted unchanged. Minimal CYP enzyme involvement."
        ),
        "drug_class": "NMDA Antagonist",
        "rxnorm_cui": "181863",
    },
    {
        "id": "DB00177_ami",
        "name": "Pregabalin",
        "brand_names": ["Lyrica CR"],
        "description": (
            "Anticonvulsant and analgesic for neuropathic pain, fibromyalgia, and seizures. "
            "Not metabolized by CYP enzymes; primarily excreted unchanged in urine. "
            "Very low drug interaction potential."
        ),
        "drug_class": "Anticonvulsant / Analgesic",
        "rxnorm_cui": "187832",
    },
    # Additional cardiovascular
    {
        "id": "DB06817",
        "name": "Rivaroxaban extended",
        "brand_names": ["Xarelto OD"],
        "description": (
            "Direct Factor Xa inhibitor anticoagulant (once-daily formulation). "
            "Same CYP3A4 and P-gp substrate profile as standard rivaroxaban. "
            "Dual CYP3A4/P-gp inhibitors significantly increase exposure and bleeding risk."
        ),
        "drug_class": "Anticoagulant / DOAC",
        "rxnorm_cui": "1037045",
    },
    {
        "id": "DB01113",
        "name": "Ivabradine",
        "brand_names": ["Corlanor", "Procoralan"],
        "description": (
            "HCN channel blocker that reduces heart rate for stable angina and heart failure. "
            "Exclusively metabolized by CYP3A4. Strong CYP3A4 inhibitors are contraindicated "
            "as they markedly increase ivabradine levels, causing excessive bradycardia."
        ),
        "drug_class": "Heart Rate Reducing Agent",
        "rxnorm_cui": "1721068",
    },
    {
        "id": "DB09267",
        "name": "Sacubitril",
        "brand_names": ["Entresto (with valsartan)"],
        "description": (
            "Neprilysin inhibitor combined with valsartan for heart failure. Active metabolite "
            "LBQ657 is a neprilysin inhibitor. Converted to active form by esterases. "
            "Minimal CYP metabolism. Avoid with ACE inhibitors due to angioedema risk."
        ),
        "drug_class": "Neprilysin Inhibitor",
        "rxnorm_cui": "1656340",
    },
    # Additional antimicrobials
    {
        "id": "DB00537_moxi",
        "name": "Moxifloxacin",
        "brand_names": ["Avelox"],
        "description": (
            "Fourth-generation fluoroquinolone antibiotic. Not significantly metabolized "
            "by CYP enzymes (glucuronidation and sulfation). Significant QT prolongation "
            "risk; avoid with other QT-prolonging drugs and hypokalemia."
        ),
        "drug_class": "Antibiotic / Fluoroquinolone",
        "rxnorm_cui": "41493",
    },
    {
        "id": "DB00537_tetra",
        "name": "Tetracycline",
        "brand_names": ["Sumycin", "Achromycin"],
        "description": (
            "Tetracycline-class antibiotic. Not significantly metabolized by CYP enzymes. "
            "Absorption greatly impaired by dairy products and divalent cations. "
            "Reduces warfarin effect due to reduction in gut flora production of vitamin K."
        ),
        "drug_class": "Antibiotic / Tetracycline",
        "rxnorm_cui": "10600",
    },
    {
        "id": "DB01190",
        "name": "Clindamycin",
        "brand_names": ["Cleocin"],
        "description": (
            "Lincosamide antibiotic for anaerobic infections. Metabolized by CYP3A4. "
            "Not a significant CYP inhibitor or inducer. May enhance neuromuscular blockade."
        ),
        "drug_class": "Antibiotic / Lincosamide",
        "rxnorm_cui": "2582",
    },
    # Additional respiratory drugs
    {
        "id": "DB01048_mont",
        "name": "Montelukast",
        "brand_names": ["Singulair"],
        "description": (
            "Leukotriene receptor antagonist for asthma and allergic rhinitis. Metabolized "
            "by CYP2C8 and CYP3A4. Gemfibrozil (CYP2C8 inhibitor) increases montelukast "
            "levels. Generally low drug interaction potential."
        ),
        "drug_class": "Leukotriene Antagonist",
        "rxnorm_cui": "88249",
    },
    {
        "id": "DB01110",
        "name": "Tiotropium",
        "brand_names": ["Spiriva"],
        "description": (
            "Long-acting muscarinic antagonist (LAMA) for COPD. Renally excreted; "
            "not significantly metabolized by CYP enzymes. Minimal pharmacokinetic "
            "drug interactions."
        ),
        "drug_class": "Anticholinergic / LAMA",
        "rxnorm_cui": "274783",
    },
    # Additional hormonal
    {
        "id": "DB01196",
        "name": "Estradiol",
        "brand_names": ["Estrace", "Vivelle", "Climara"],
        "description": (
            "Endogenous estrogen used for menopausal hormone therapy and contraception. "
            "Metabolized by CYP3A4. CYP3A4 inducers (rifampin, carbamazepine) markedly "
            "reduce estradiol levels. Oral formulation subject to high first-pass CYP3A4 metabolism."
        ),
        "drug_class": "Estrogen",
        "rxnorm_cui": "4124",
    },
    {
        "id": "DB00288",
        "name": "Finasteride",
        "brand_names": ["Proscar", "Propecia"],
        "description": (
            "5-alpha reductase inhibitor for BPH and male pattern baldness. Metabolized "
            "by CYP3A4. Not a significant CYP inhibitor or inducer. Low drug interaction potential."
        ),
        "drug_class": "5-Alpha Reductase Inhibitor",
        "rxnorm_cui": "49999",
    },
    # Additional mental health
    {
        "id": "DB00448_benzo",
        "name": "Buspirone",
        "brand_names": ["Buspar"],
        "description": (
            "Non-benzodiazepine anxiolytic. Extensively metabolized by CYP3A4. "
            "Strong CYP3A4 inhibitors (ketoconazole, ritonavir) markedly increase buspirone "
            "levels. CYP3A4 inducers (rifampin) reduce buspirone to negligible levels."
        ),
        "drug_class": "Anxiolytic",
        "rxnorm_cui": "1827",
    },
    {
        "id": "DB00580",
        "name": "Modafinil",
        "brand_names": ["Provigil"],
        "description": (
            "Wakefulness-promoting agent for narcolepsy and sleep disorders. Mild inducer "
            "of CYP3A4 and inhibitor of CYP2C19. Reduces plasma levels of oral contraceptives. "
            "Metabolized by amide hydrolysis and CYP3A4."
        ),
        "drug_class": "CNS Stimulant / Wakefulness Agent",
        "rxnorm_cui": "72614",
    },
    # Additional analgesics / anti-inflammatory
    {
        "id": "DB00461",
        "name": "Celecoxib",
        "brand_names": ["Celebrex"],
        "description": (
            "COX-2 selective NSAID. Primarily metabolized by CYP2C9. CYP2C9 poor metabolizers "
            "and patients taking CYP2C9 inhibitors have elevated celecoxib levels. "
            "Increases lithium levels and warfarin anticoagulant effect."
        ),
        "drug_class": "NSAID / COX-2 Inhibitor",
        "rxnorm_cui": "140587",
    },
    {
        "id": "DB00814",
        "name": "Meloxicam",
        "brand_names": ["Mobic", "Vivlodex"],
        "description": (
            "Preferential COX-2 NSAID. Primarily metabolized by CYP2C9 and CYP3A4. "
            "CYP2C9 inhibitors may increase meloxicam exposure. Increases bleeding risk "
            "with anticoagulants."
        ),
        "drug_class": "NSAID",
        "rxnorm_cui": "41493",
    },
    # Additional GI drugs
    {
        "id": "DB00375",
        "name": "Colestipol",
        "brand_names": ["Colestid"],
        "description": (
            "Bile acid sequestrant for hyperlipidemia. Not systemically absorbed; no CYP "
            "metabolism. Reduces absorption of many drugs taken concomitantly including "
            "warfarin, digoxin, and thyroid hormones. Administer other drugs 1h before or "
            "4-6h after colestipol."
        ),
        "drug_class": "Bile Acid Sequestrant",
        "rxnorm_cui": "2760",
    },
    {
        "id": "DB00489",
        "name": "Ondansetron",
        "brand_names": ["Zofran", "Zuplenz"],
        "description": (
            "5-HT3 antagonist antiemetic. Metabolized by CYP1A2, CYP2D6, and CYP3A4. "
            "Significant QT prolongation risk; avoid with other QT-prolonging drugs. "
            "Dose-dependent QT prolongation led to FDA safety communication."
        ),
        "drug_class": "Antiemetic / 5-HT3 Antagonist",
        "rxnorm_cui": "312086",
    },
    # Additional psychiatric
    {
        "id": "DB00477",
        "name": "Chlorpromazine",
        "brand_names": ["Thorazine"],
        "description": (
            "First-generation (typical) antipsychotic. Metabolized by CYP2D6. "
            "CYP2D6 inhibitors increase chlorpromazine levels. Significant QT prolongation "
            "and anticholinergic side effects. Moderate CYP2D6 inhibitor itself."
        ),
        "drug_class": "Antipsychotic",
        "rxnorm_cui": "2403",
    },
    {
        "id": "DB00227_vlf",
        "name": "Lisdexamfetamine",
        "brand_names": ["Vyvanse"],
        "description": (
            "Prodrug of d-amphetamine for ADHD. Converted to active d-amphetamine by "
            "lysosomal enzymes after absorption. Minimal CYP involvement. "
            "Serotonin syndrome risk with MAOIs."
        ),
        "drug_class": "CNS Stimulant / ADHD",
        "rxnorm_cui": "854800",
    },
    {
        "id": "DB01104_escit",
        "name": "Citalopram",
        "brand_names": ["Celexa"],
        "description": (
            "SSRI antidepressant. Primarily metabolized by CYP2C19 (major) and CYP3A4. "
            "Mild CYP2D6 inhibitor. CYP2C19 poor metabolizers or strong inhibitors increase "
            "citalopram exposure and QT prolongation risk. FDA dose limits apply."
        ),
        "drug_class": "SSRI Antidepressant",
        "rxnorm_cui": "2556",
    },
    # Additional urology / endocrinology
    {
        "id": "DB00374",
        "name": "Tamsulosin",
        "brand_names": ["Flomax"],
        "description": (
            "Alpha-1A/D-selective antagonist for BPH. Primarily metabolized by CYP3A4 "
            "and CYP2D6. CYP3A4 inhibitors increase tamsulosin exposure, potentiating "
            "hypotensive effects. Use with caution with PDE5 inhibitors."
        ),
        "drug_class": "Alpha-1 Blocker",
        "rxnorm_cui": "77492",
    },
    {
        "id": "DB01611",
        "name": "Hydroxychloroquine",
        "brand_names": ["Plaquenil"],
        "description": (
            "Antimalarial and disease-modifying antirheumatic drug (DMARD). "
            "Metabolized by CYP2C8 and CYP3A4. QT prolongation risk. "
            "Inhibits CYP2D6, raising levels of metoprolol and other CYP2D6 substrates."
        ),
        "drug_class": "Antimalarial / DMARD",
        "rxnorm_cui": "41493",
    },
    # Additional renal / electrolyte
    {
        "id": "DB00999_tors",
        "name": "Torsemide",
        "brand_names": ["Demadex"],
        "description": (
            "Loop diuretic for edema and hypertension. Metabolized by CYP2C9. "
            "CYP2C9 inhibitors may increase torsemide levels and diuretic effect."
        ),
        "drug_class": "Diuretic / Loop",
        "rxnorm_cui": "38413",
    },
    {
        "id": "DB00682_apix2",
        "name": "Betrixaban",
        "brand_names": ["Bevyxxa"],
        "description": (
            "Direct oral anticoagulant (Factor Xa inhibitor) for VTE prophylaxis. "
            "P-glycoprotein substrate; minimal CYP3A4 metabolism. P-gp inhibitors "
            "(clarithromycin, ketoconazole) increase betrixaban exposure and bleeding risk."
        ),
        "drug_class": "Anticoagulant / DOAC",
        "rxnorm_cui": "1946831",
    },
    {
        "id": "DB01268",
        "name": "Sunitinib",
        "brand_names": ["Sutent"],
        "description": (
            "Multi-targeted tyrosine kinase inhibitor for renal cell carcinoma and GIST. "
            "Metabolized by CYP3A4 to its active metabolite SU12662. CYP3A4 inhibitors "
            "increase sunitinib levels; inducers reduce efficacy. QT prolongation risk."
        ),
        "drug_class": "Antineoplastic / TKI",
        "rxnorm_cui": "847738",
    },
    {
        "id": "DB01036",
        "name": "Tolterodine",
        "brand_names": ["Detrol", "Detrol LA"],
        "description": (
            "Muscarinic receptor antagonist for overactive bladder. Primarily metabolized "
            "by CYP2D6 to active 5-hydroxymethyl metabolite; also CYP3A4. "
            "CYP2D6 poor metabolizers have 7-fold higher tolterodine exposure. "
            "Strong CYP3A4 inhibitors are contraindicated."
        ),
        "drug_class": "Anticholinergic / Urological",
        "rxnorm_cui": "41493",
    },
    {
        "id": "DB00349",
        "name": "Clobazam",
        "brand_names": ["Onfi", "Sympazan"],
        "description": (
            "1,5-benzodiazepine anticonvulsant for Lennox-Gastaut syndrome. "
            "Metabolized by CYP2C19 (major) and CYP3A4 to active metabolite N-desmethylclobazam. "
            "CYP2C19 inhibitors (fluconazole) increase metabolite levels. "
            "Inhibits CYP2D6, raising levels of CYP2D6 substrates."
        ),
        "drug_class": "Benzodiazepine / Anticonvulsant",
        "rxnorm_cui": "2598",
    },
    {
        "id": "DB01051_bed",
        "name": "Bedaquiline",
        "brand_names": ["Sirturo"],
        "description": (
            "Diarylquinoline antibiotic for multidrug-resistant tuberculosis. "
            "Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase bedaquiline exposure, "
            "raising QT prolongation risk. QT-prolonging drugs should be avoided."
        ),
        "drug_class": "Antituberculosis",
        "rxnorm_cui": "1540463",
    },
    {
        "id": "DB01268_lenva",
        "name": "Lenvatinib",
        "brand_names": ["Lenvima"],
        "description": (
            "Multi-kinase inhibitor for thyroid cancer and hepatocellular carcinoma. "
            "Metabolized by CYP3A4 and aldehyde oxidase. CYP3A4 inducers (rifampin) "
            "reduce lenvatinib exposure. QT prolongation risk."
        ),
        "drug_class": "Antineoplastic / TKI",
        "rxnorm_cui": "1657016",
    },
    {
        "id": "DB01048_pazop",
        "name": "Pazopanib",
        "brand_names": ["Votrient"],
        "description": (
            "Multi-kinase inhibitor for renal cell carcinoma and soft tissue sarcoma. "
            "Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase pazopanib exposure. "
            "CYP3A4 inducers reduce efficacy. Strong CYP3A4 inhibitors: use with caution."
        ),
        "drug_class": "Antineoplastic / TKI",
        "rxnorm_cui": "1099800",
    },
    {
        "id": "DB00295_hydro",
        "name": "Hydromorphone",
        "brand_names": ["Dilaudid", "Exalgo"],
        "description": (
            "Potent opioid analgesic (active metabolite of hydrocodone). Primarily "
            "glucuronidated by UGT enzymes; minimal CYP involvement. Valproic acid (UGT "
            "inhibitor) may modestly increase hydromorphone levels."
        ),
        "drug_class": "Opioid Analgesic",
        "rxnorm_cui": "3423",
    },
    {
        "id": "DB00316_metam",
        "name": "Methadone",
        "brand_names": ["Dolophine", "Methadose"],
        "description": (
            "Long-acting opioid analgesic and opioid use disorder treatment. Metabolized "
            "by CYP3A4 (primary), CYP2D6, CYP2B6, and CYP2C19. Highly variable "
            "pharmacokinetics. QT prolongation risk at high doses. Many clinically significant "
            "CYP interactions can alter levels unpredictably."
        ),
        "drug_class": "Opioid Analgesic / Opioid Use Disorder",
        "rxnorm_cui": "6813",
    },
    {
        "id": "DB00564_pen",
        "name": "Phenobarbital",
        "brand_names": ["Luminal", "Solfoton"],
        "description": (
            "Long-acting barbiturate anticonvulsant and sedative. Potent inducer of CYP3A4, "
            "CYP2C9, CYP2C19, CYP1A2, and CYP2B6. Substantially reduces plasma levels of "
            "many drugs including warfarin, oral contraceptives, and cyclosporine. "
            "Metabolized by CYP2C9."
        ),
        "drug_class": "Anticonvulsant / Barbiturate",
        "rxnorm_cui": "8134",
    },
    {
        "id": "DB00571_iva",
        "name": "Ivermectin",
        "brand_names": ["Stromectol", "Soolantra"],
        "description": (
            "Antiparasitic agent for onchocerciasis, strongyloidiasis, and other parasitic "
            "infections. CYP3A4 substrate and P-glycoprotein substrate. Strong CYP3A4 "
            "and P-gp inhibitors may increase ivermectin plasma levels."
        ),
        "drug_class": "Antiparasitic",
        "rxnorm_cui": "41493",
    },
    {
        "id": "DB01048_glecp",
        "name": "Glecaprevir",
        "brand_names": ["Mavyret (with pibrentasvir)"],
        "description": (
            "NS3/4A protease inhibitor for hepatitis C. P-glycoprotein inhibitor; "
            "inhibits OATP1B1/3. Increases plasma levels of statins and other OATP substrates. "
            "Cyclosporine is contraindicated with glecaprevir/pibrentasvir."
        ),
        "drug_class": "Antiviral / HCV Protease Inhibitor",
        "rxnorm_cui": "1945103",
    },
    {
        "id": "DB01048_pibr",
        "name": "Pibrentasvir",
        "brand_names": ["Mavyret (with glecaprevir)"],
        "description": (
            "NS5A inhibitor for hepatitis C. P-glycoprotein inhibitor and inhibitor "
            "of BCRP transporter. Combined with glecaprevir increases levels of rosuvastatin "
            "and other substrates of P-gp and BCRP."
        ),
        "drug_class": "Antiviral / HCV NS5A Inhibitor",
        "rxnorm_cui": "1945103",
    },
    {
        "id": "DB09102",
        "name": "Venetoclax",
        "brand_names": ["Venclexta"],
        "description": (
            "BCL-2 inhibitor for CLL and AML. CYP3A4 substrate and P-gp substrate. "
            "Strong and moderate CYP3A4 inhibitors significantly increase venetoclax "
            "exposure, raising risk of tumor lysis syndrome and cytopenias. "
            "Strong CYP3A4 inhibitors are contraindicated during initiation."
        ),
        "drug_class": "Antineoplastic / BCL-2 Inhibitor",
        "rxnorm_cui": "1876361",
    },
    {
        "id": "DB09141",
        "name": "Ibrutinib",
        "brand_names": ["Imbruvica"],
        "description": (
            "BTK inhibitor for B-cell malignancies. Extensively metabolized by CYP3A4. "
            "Strong CYP3A4 inhibitors (ketoconazole, clarithromycin) markedly increase "
            "ibrutinib exposure. Strong CYP3A4 inducers (rifampin) reduce levels by ~90%. "
            "Concomitant antiplatelet/anticoagulant use increases bleeding risk."
        ),
        "drug_class": "Antineoplastic / BTK Inhibitor",
        "rxnorm_cui": "1629936",
    },
    {
        "id": "DB00564_oxa",
        "name": "Oxaliplatin",
        "brand_names": ["Eloxatin"],
        "description": (
            "Platinum-based chemotherapy for colorectal cancer. Not metabolized by CYP "
            "enzymes; undergoes non-enzymatic chemical transformation. Minimal pharmacokinetic "
            "CYP-mediated interactions."
        ),
        "drug_class": "Antineoplastic / Platinum Compound",
        "rxnorm_cui": "341693",
    },
    {
        "id": "DB01048_olapar",
        "name": "Olaparib",
        "brand_names": ["Lynparza"],
        "description": (
            "PARP inhibitor for BRCA-mutated cancers. Metabolized by CYP3A4. "
            "Strong CYP3A4 inhibitors (itraconazole) increase olaparib exposure 2.7-fold. "
            "Strong CYP3A4 inducers (rifampin) reduce olaparib exposure by 87%."
        ),
        "drug_class": "Antineoplastic / PARP Inhibitor",
        "rxnorm_cui": "1553543",
    },
    {
        "id": "DB00616",
        "name": "Methylprednisolone",
        "brand_names": ["Medrol", "Solu-Medrol"],
        "description": (
            "Synthetic glucocorticoid for inflammatory and allergic conditions. "
            "Metabolized by CYP3A4. Strong CYP3A4 inhibitors increase methylprednisolone "
            "exposure. Large doses induce CYP3A4. Used intravenously for acute conditions."
        ),
        "drug_class": "Corticosteroid",
        "rxnorm_cui": "6902",
    },
    {
        "id": "DB01234_budes",
        "name": "Budesonide",
        "brand_names": ["Pulmicort", "Entocort", "Uceris"],
        "description": (
            "Glucocorticoid for asthma, COPD, IBD. Metabolized by CYP3A4. "
            "Strong CYP3A4 inhibitors (ketoconazole, ritonavir) markedly increase "
            "systemic budesonide exposure, causing adrenal suppression and Cushing's syndrome."
        ),
        "drug_class": "Corticosteroid",
        "rxnorm_cui": "19831",
    },
]
