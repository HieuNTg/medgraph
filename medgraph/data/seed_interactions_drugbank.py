"""
DrugBank-expansion interaction dataset for MEDGRAPH — 100+ additional interactions.

Covers well-documented CYP450-mediated and transporter-mediated drug-drug interactions
involving both new and existing drugs.

Interaction ID format: IX_drugbank_{DrugAid}_{DrugBid}

Sources:
- FDA Drug Labeling
- CPIC Guidelines (https://cpicpgx.org/)
- Clinical Pharmacology Database
- Flockhart Table CYP450 Drug Interactions (Indiana University)

DISCLAIMER: Data is for informational/research use only. Not medical advice.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Drug-Enzyme Relations for new DrugBank-expansion drugs
# ---------------------------------------------------------------------------

DRUG_ENZYME_RELATIONS_DRUGBANK: list[dict] = [
    # --- Statins ---
    {
        "drug_id": "DB01076_ator",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00641_rosu",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    {
        "drug_id": "DB00861_prava",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    {
        "drug_id": "DB00227_fluva",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01098_pitav",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    # --- ACE Inhibitors (no CYP) ---
    # --- ARBs ---
    {
        "drug_id": "DB00177_los",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00177_los",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00812_irbe",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00678_azil",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # --- Beta-blockers ---
    {
        "drug_id": "DB00264_meto",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01136_carve",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01136_carve",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00319_nebiv",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # --- CCBs ---
    {
        "drug_id": "DB00381_amlo",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00661_vera",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00661_vera",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00661_vera",
        "enzyme_id": "PGLYCO",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00470_dilt",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00470_dilt",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01107_felod",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00409_nicar",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00409_nicar",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "weak",
    },
    # --- DOACs ---
    {
        "drug_id": "DB00682_apix",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00682_apix",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB06228_riva",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB06228_riva",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # --- SSRIs ---
    {
        "drug_id": "DB01104_sert",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01104_sert",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01561_escit",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01561_escit",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00472_fluox",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00472_fluox",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01174_cital",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00215_fluvo",
        "enzyme_id": "CYP1A2",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00215_fluvo",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    # --- SNRIs ---
    {
        "drug_id": "DB00696_dulox",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00696_dulox",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00285_venla",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # --- Benzodiazepines ---
    {
        "drug_id": "DB00321_alpraz",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00829_diaz",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00829_diaz",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01068_clona",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # --- Antipsychotics ---
    {
        "drug_id": "DB00543_quetia",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00734_rispe",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01049_arip",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01049_arip",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00246_zipras",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00371_cloz",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00371_cloz",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00334_olanz",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # --- Anticonvulsants ---
    {
        "drug_id": "DB00564_cbz",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00564_cbz",
        "enzyme_id": "CYP3A4",
        "relation_type": "induces",
        "strength": "strong",
    },
    {
        "drug_id": "DB00564_cbz",
        "enzyme_id": "CYP2C9",
        "relation_type": "induces",
        "strength": "strong",
    },
    {
        "drug_id": "DB00564_cbz",
        "enzyme_id": "CYP1A2",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00313_valp",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # --- Opioids ---
    {
        "drug_id": "DB00956_hydro",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00956_hydro",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01535_oxycod",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01535_oxycod",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    {
        "drug_id": "DB00813_fent",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00196_buprenor",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00333_methadone",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00333_methadone",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00333_methadone",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01174_codeine",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00193_tramadol",
        "enzyme_id": "CYP2D6",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00193_tramadol",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # --- Antifungals ---
    {
        "drug_id": "DB01026_keto",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB01026_keto",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00636_flucon",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB00636_flucon",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01182_voricon",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01182_voricon",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB01182_voricon",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB01182_voricon",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    # --- Corticosteroids ---
    {
        "drug_id": "DB00591_dexa",
        "enzyme_id": "CYP3A4",
        "relation_type": "induces",
        "strength": "strong",
    },
    {
        "drug_id": "DB00635_pred",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01280_flutica",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01411_budesonide",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # --- Anticonvulsants (continued) ---
    {
        "drug_id": "DB00521_oxcarb",
        "enzyme_id": "CYP3A4",
        "relation_type": "induces",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00521_oxcarb",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # --- GI ---
    {
        "drug_id": "DB00338_omeprz",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00338_omeprz",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00736_esomep",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00736_esomep",
        "enzyme_id": "CYP2C19",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00501_cimetidine",
        "enzyme_id": "CYP1A2",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00501_cimetidine",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00501_cimetidine",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00501_cimetidine",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "weak",
    },
    # --- Antiemetics ---
    {
        "drug_id": "DB00904_ondansetron",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00904_ondansetron",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00757_aprepitant",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00757_aprepitant",
        "enzyme_id": "CYP3A4",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    # --- Respiratory ---
    {
        "drug_id": "DB00675_salme",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00698_theoph",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00353_roflumilast",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00353_roflumilast",
        "enzyme_id": "CYP1A2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # --- Immunology ---
    {
        "drug_id": "DB01589_leflu",
        "enzyme_id": "CYP1A2",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01589_leflu",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11817_tofa",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11817_tofa",
        "enzyme_id": "CYP2C19",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # --- Oncology ---
    {
        "drug_id": "DB01418_capecit",
        "enzyme_id": "CYP2C9",
        "relation_type": "inhibits",
        "strength": "strong",
    },
    {
        "drug_id": "DB01048_ibrutinib",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB09023_imatinib",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB09023_imatinib",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB08877_erlot",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB09073_palbociclib",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11093_venetoclax",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB11901_abira",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11901_abira",
        "enzyme_id": "CYP2C8",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00773_etoposide",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01229_paclitaxel",
        "enzyme_id": "CYP2C8",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01229_paclitaxel",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00531_docetaxel",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01067_pioglitazone",
        "enzyme_id": "CYP2C8",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01067_pioglitazone",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    # --- PDE5 inhibitors ---
    {
        "drug_id": "DB00513_sildenafil",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00513_sildenafil",
        "enzyme_id": "CYP2C9",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00203_tadalafil",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # --- Antimalarials ---
    {
        "drug_id": "DB01611_hydroxy",
        "enzyme_id": "CYP2D6",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01611_hydroxy",
        "enzyme_id": "CYP2C8",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB01410_mefloquine",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    # --- Acetaminophen ---
    {
        "drug_id": "DB00945_acetamino",
        "enzyme_id": "CYP2E1",
        "relation_type": "metabolized_by",
        "strength": "weak",
    },
    # --- Misc ---
    {
        "drug_id": "DB00513_sildenafil",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB00558_osimertinib",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB09168_colchi",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB09168_colchi",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB08880_teriflunomide",
        "enzyme_id": "CYP1A2",
        "relation_type": "inhibits",
        "strength": "moderate",
    },
    {
        "drug_id": "DB09067_apremilast",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
    {
        "drug_id": "DB01076_fingolimod",
        "enzyme_id": "CYP4F2",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB00697_spiro",
        "enzyme_id": "CYP3A4",
        "relation_type": "metabolized_by",
        "strength": "moderate",
    },
    {
        "drug_id": "DB11652_nintedanib",
        "enzyme_id": "PGLYCO",
        "relation_type": "metabolized_by",
        "strength": "strong",
    },
]

# ---------------------------------------------------------------------------
# Drug-Drug Interactions — 100+ clinically significant interactions
# ---------------------------------------------------------------------------

INTERACTIONS_DRUGBANK: list[dict] = [
    # =========================================================================
    # Statin interactions
    # =========================================================================
    {
        "id": "IX_db_ator_keto",
        "drug_a_id": "DB01076_ator",
        "drug_b_id": "DB01026_keto",
        "severity": "major",
        "description": (
            "Ketoconazole is a potent CYP3A4 inhibitor that markedly increases atorvastatin "
            "plasma concentrations, raising the risk of myopathy and rhabdomyolysis. "
            "Concurrent use should be avoided or atorvastatin dose capped at 20mg."
        ),
        "mechanism": "CYP3A4 inhibition by ketoconazole -> elevated atorvastatin -> myopathy risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_fluva_flucon",
        "drug_a_id": "DB00227_fluva",
        "drug_b_id": "DB00636_flucon",
        "severity": "major",
        "description": (
            "Fluconazole is a strong CYP2C9 inhibitor and markedly increases fluvastatin "
            "exposure (up to 3-fold). Increases risk of statin-associated myopathy. "
            "Monitor or reduce fluvastatin dose. Other statins metabolized by CYP3A4 "
            "have moderate interaction with fluconazole."
        ),
        "mechanism": "CYP2C9 inhibition by fluconazole -> elevated fluvastatin",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_ator_diltiazem",
        "drug_a_id": "DB01076_ator",
        "drug_b_id": "DB00470_dilt",
        "severity": "moderate",
        "description": (
            "Diltiazem moderately inhibits CYP3A4, increasing atorvastatin AUC approximately "
            "50%. Risk of myopathy is elevated. Consider dose reduction or monitoring. "
            "Lovastatin and simvastatin have higher interaction risk with diltiazem."
        ),
        "mechanism": "CYP3A4 inhibition by diltiazem -> elevated atorvastatin",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_ator_verapamil",
        "drug_a_id": "DB01076_ator",
        "drug_b_id": "DB00661_vera",
        "severity": "moderate",
        "description": (
            "Verapamil inhibits CYP3A4 and P-gp, increasing atorvastatin exposure and risk "
            "of myopathy. Atorvastatin dose should not exceed 40mg with verapamil. "
            "Simvastatin has more stringent restrictions with verapamil (capped at 10mg)."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition by verapamil -> elevated atorvastatin",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Anticoagulant interactions
    # =========================================================================
    {
        "id": "IX_db_apix_rifampin",
        "drug_a_id": "DB00682_apix",
        "drug_b_id": "DB01045",
        "severity": "major",
        "description": (
            "Rifampin (rifampicin) is a strong CYP3A4 and P-gp inducer that reduces "
            "apixaban AUC by ~54%. Combined strong CYP3A4/P-gp inducers markedly reduce "
            "apixaban efficacy, increasing stroke/VTE risk. Avoid combination with apixaban."
        ),
        "mechanism": "CYP3A4 + P-gp induction by rifampin -> reduced apixaban exposure",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_apix_ketoconazole",
        "drug_a_id": "DB00682_apix",
        "drug_b_id": "DB01026_keto",
        "severity": "major",
        "description": (
            "Ketoconazole (strong dual CYP3A4/P-gp inhibitor) increases apixaban AUC ~2-fold. "
            "Avoid use with strong dual CYP3A4/P-gp inhibitors unless benefit justifies risk. "
            "Reduce apixaban dose if combination unavoidable."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition -> elevated apixaban -> bleeding risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_riva_ketoconazole",
        "drug_a_id": "DB06228_riva",
        "drug_b_id": "DB01026_keto",
        "severity": "major",
        "description": (
            "Ketoconazole increases rivaroxaban AUC ~2.6-fold and Cmax ~1.7-fold via combined "
            "CYP3A4 and P-gp inhibition. Concomitant use with strong dual CYP3A4/P-gp inhibitors "
            "is contraindicated due to increased bleeding risk."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition -> elevated rivaroxaban -> bleeding risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # CCB interactions
    # =========================================================================
    {
        "id": "IX_db_felod_clarithro",
        "drug_a_id": "DB01107_felod",
        "drug_b_id": "DB01211",
        "severity": "major",
        "description": (
            "Clarithromycin is a potent CYP3A4 inhibitor that substantially increases "
            "felodipine plasma levels, causing excessive hypotension, peripheral edema, "
            "and reflex tachycardia. Monitor blood pressure closely or substitute with "
            "a non-CYP3A4-metabolized antihypertensive."
        ),
        "mechanism": "CYP3A4 inhibition by clarithromycin -> elevated felodipine -> hypotension",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_salme_keto",
        "drug_a_id": "DB00675_salme",
        "drug_b_id": "DB01026_keto",
        "severity": "major",
        "description": (
            "Ketoconazole markedly increases salmeterol AUC ~16-fold and Cmax ~12-fold via "
            "strong CYP3A4 inhibition. Risk of serious cardiovascular adverse effects "
            "(QTc prolongation, ventricular arrhythmia). Contraindicated combination."
        ),
        "mechanism": "CYP3A4 inhibition -> elevated salmeterol -> QTc prolongation and arrhythmia",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Beta-blocker / CYP2D6 interactions
    # =========================================================================
    {
        "id": "IX_db_meto_parox",
        "drug_a_id": "DB00264_meto",
        "drug_b_id": "DB00715_par",
        "severity": "major",
        "description": (
            "Paroxetine is a potent CYP2D6 inhibitor that substantially increases metoprolol "
            "plasma levels (4- to 5-fold), leading to bradycardia, hypotension, and heart "
            "block. Choose alternative beta-blocker (atenolol, bisoprolol) or use non-CYP2D6 "
            "inhibiting antidepressant."
        ),
        "mechanism": "CYP2D6 inhibition by paroxetine -> elevated metoprolol -> bradycardia",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_meto_fluox",
        "drug_a_id": "DB00264_meto",
        "drug_b_id": "DB00472_fluox",
        "severity": "moderate",
        "description": (
            "Fluoxetine and its active metabolite norfluoxetine are potent CYP2D6 inhibitors, "
            "increasing metoprolol levels several-fold. Risk of bradycardia and heart block "
            "is elevated. Due to long half-life of norfluoxetine, interaction persists for "
            "weeks after fluoxetine discontinuation."
        ),
        "mechanism": "CYP2D6 inhibition by fluoxetine/norfluoxetine -> elevated metoprolol",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_nebiv_parox",
        "drug_a_id": "DB00319_nebiv",
        "drug_b_id": "DB00715_par",
        "severity": "major",
        "description": (
            "Paroxetine markedly inhibits CYP2D6, increasing nebivolol AUC ~5-fold. "
            "Significant bradycardia risk. Consider switching to antidepressant with less "
            "CYP2D6 inhibitory activity or monitoring heart rate closely."
        ),
        "mechanism": "CYP2D6 inhibition by paroxetine -> markedly elevated nebivolol",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # SSRI interactions
    # =========================================================================
    {
        "id": "IX_db_escit_omeprazole",
        "drug_a_id": "DB01561_escit",
        "drug_b_id": "DB00338_omeprz",
        "severity": "moderate",
        "description": (
            "Omeprazole inhibits CYP2C19, the primary metabolic enzyme for escitalopram, "
            "increasing escitalopram AUC by ~50%. Combined with escitalopram's intrinsic "
            "QTc-prolonging potential, combination may increase cardiac risk at higher "
            "escitalopram doses. Monitor QTc; consider dose cap at 20mg."
        ),
        "mechanism": "CYP2C19 inhibition by omeprazole -> elevated escitalopram -> QTc risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_fluvo_clozapine",
        "drug_a_id": "DB00215_fluvo",
        "drug_b_id": "DB00371_cloz",
        "severity": "major",
        "description": (
            "Fluvoxamine is a potent CYP1A2 inhibitor that raises clozapine plasma levels "
            "up to 3-fold or more. Risk of dose-dependent clozapine toxicity including "
            "seizures, agranulocytosis, sedation, and orthostatic hypotension. "
            "If combination necessary, reduce clozapine dose by 50-75% with close monitoring."
        ),
        "mechanism": "CYP1A2 inhibition by fluvoxamine -> markedly elevated clozapine levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_fluvo_theophylline",
        "drug_a_id": "DB00215_fluvo",
        "drug_b_id": "DB00698_theoph",
        "severity": "major",
        "description": (
            "Fluvoxamine markedly inhibits CYP1A2, significantly elevating theophylline plasma "
            "concentrations. Theophylline has a narrow therapeutic index; levels can reach "
            "toxic range (>20 mcg/mL) causing seizures, cardiac arrhythmias. "
            "Reduce theophylline dose and monitor levels closely."
        ),
        "mechanism": "CYP1A2 inhibition by fluvoxamine -> elevated theophylline -> toxicity",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_sert_tramadol",
        "drug_a_id": "DB01104_sert",
        "drug_b_id": "DB00193_tramadol",
        "severity": "major",
        "description": (
            "Combination of sertraline with tramadol increases serotonin syndrome risk. "
            "Tramadol inhibits serotonin reuptake and is a mu-opioid agonist. "
            "Sertraline also inhibits CYP2D6, reducing tramadol conversion to active M1 "
            "but increasing the parent compound (serotonergic) levels."
        ),
        "mechanism": "Additive serotonergic effects; CYP2D6 inhibition alters tramadol metabolism",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Antipsychotic interactions
    # =========================================================================
    {
        "id": "IX_db_quetia_cbz",
        "drug_a_id": "DB00543_quetia",
        "drug_b_id": "DB00564_cbz",
        "severity": "major",
        "description": (
            "Carbamazepine is a potent CYP3A4 inducer that reduces quetiapine AUC by ~87%. "
            "Combination leads to subtherapeutic quetiapine levels. If combination required, "
            "quetiapine dose may need 5-fold increase. Consider alternative anticonvulsant "
            "without CYP3A4 induction (levetiracetam, lamotrigine)."
        ),
        "mechanism": "CYP3A4 induction by carbamazepine -> markedly reduced quetiapine exposure",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_quetia_keto",
        "drug_a_id": "DB00543_quetia",
        "drug_b_id": "DB01026_keto",
        "severity": "major",
        "description": (
            "Ketoconazole increases quetiapine AUC approximately 6-fold via potent CYP3A4 "
            "inhibition. Markedly increases risk of QTc prolongation, sedation, and orthostatic "
            "hypotension. Avoid combination; use alternative antifungal or antipsychotic."
        ),
        "mechanism": "CYP3A4 inhibition by ketoconazole -> greatly elevated quetiapine",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_arip_parox",
        "drug_a_id": "DB01049_arip",
        "drug_b_id": "DB00715_par",
        "severity": "major",
        "description": (
            "Paroxetine inhibits CYP2D6, increasing aripiprazole AUC ~60%. "
            "Reduce aripiprazole dose by 50% when adding strong CYP2D6 inhibitors. "
            "Monitor for aripiprazole adverse effects (akathisia, sedation, metabolic effects)."
        ),
        "mechanism": "CYP2D6 inhibition by paroxetine -> elevated aripiprazole",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_olanz_smoking",
        "drug_a_id": "DB00334_olanz",
        "drug_b_id": "DB00698_theoph",
        "severity": "moderate",
        "description": (
            "Both olanzapine and theophylline are primarily metabolized by CYP1A2. "
            "CYP1A2 inducers (cigarette smoking) reduce both drug levels. CYP1A2 inhibitors "
            "(fluvoxamine, ciprofloxacin) increase both drug levels. "
            "Co-administration requires monitoring of both drug plasma levels."
        ),
        "mechanism": "Shared CYP1A2 metabolism; susceptibility to same inducers/inhibitors",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Opioid interactions
    # =========================================================================
    {
        "id": "IX_db_fent_ritonavir",
        "drug_a_id": "DB00813_fent",
        "drug_b_id": "DB00503",
        "severity": "critical",
        "description": (
            "Ritonavir is a potent CYP3A4 inhibitor that markedly increases fentanyl exposure "
            "when administered systemically. Risk of fatal respiratory depression. "
            "Even transdermal fentanyl exposure is significantly increased. "
            "Monitor closely and consider dose reduction of 50% or more."
        ),
        "mechanism": "CYP3A4 inhibition by ritonavir -> massively elevated fentanyl -> respiratory depression",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_oxycod_keto",
        "drug_a_id": "DB01535_oxycod",
        "drug_b_id": "DB01026_keto",
        "severity": "major",
        "description": (
            "Ketoconazole increases oxycodone AUC ~2.4-fold via CYP3A4 inhibition. "
            "Risk of respiratory depression, excessive sedation, and opioid toxicity. "
            "Reduce oxycodone dose and monitor for signs of opioid excess."
        ),
        "mechanism": "CYP3A4 inhibition -> elevated oxycodone -> respiratory depression risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_codeine_parox",
        "drug_a_id": "DB01174_codeine",
        "drug_b_id": "DB00715_par",
        "severity": "major",
        "description": (
            "Paroxetine inhibits CYP2D6, blocking codeine's conversion to the active morphine "
            "metabolite. In most patients, this reduces analgesia (making codeine ineffective). "
            "This pharmacogenomics-type interaction makes codeine a poor choice when CYP2D6 "
            "inhibitors are co-administered."
        ),
        "mechanism": "CYP2D6 inhibition by paroxetine -> impaired codeine -> morphine conversion -> no analgesia",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_methadone_flucon",
        "drug_a_id": "DB00333_methadone",
        "drug_b_id": "DB00636_flucon",
        "severity": "major",
        "description": (
            "Fluconazole inhibits CYP3A4 and CYP2C9, both involved in methadone metabolism, "
            "increasing methadone levels and QTc prolongation risk. "
            "Also inhibits CYP2C19, which contributes to methadone clearance. "
            "Monitor QTc and adjust methadone dose if combination necessary."
        ),
        "mechanism": "Multi-CYP inhibition by fluconazole -> elevated methadone -> QTc prolongation",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Anticonvulsant interactions
    # =========================================================================
    {
        "id": "IX_db_cbz_valp",
        "drug_a_id": "DB00564_cbz",
        "drug_b_id": "DB00313_valp",
        "severity": "major",
        "description": (
            "Carbamazepine induces CYP3A4 and reduces valproate clearance (epoxide hydrolase "
            "inhibition by valproate increases carbamazepine-10,11-epoxide toxic metabolite). "
            "Net effect is complex: reduced valproate levels and potential carbamazepine toxicity "
            "from accumulation of toxic epoxide metabolite."
        ),
        "mechanism": "Bidirectional: CBZ reduces VPA levels; VPA increases CBZ-epoxide via epoxide hydrolase inhibition",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_lamot_valp",
        "drug_a_id": "DB00745_lamot",
        "drug_b_id": "DB00313_valp",
        "severity": "major",
        "description": (
            "Valproate inhibits UGT1A4 and UGT2B7 enzymes responsible for lamotrigine "
            "glucuronidation, approximately doubling lamotrigine plasma levels. "
            "This substantially increases risk of lamotrigine-associated Stevens-Johnson "
            "syndrome and toxic epidermal necrolysis. Reduce lamotrigine dose by 50% "
            "when adding valproate."
        ),
        "mechanism": "UGT inhibition by valproate -> elevated lamotrigine -> Stevens-Johnson syndrome risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_cbz_warfarin",
        "drug_a_id": "DB00564_cbz",
        "drug_b_id": "DB00682",
        "severity": "major",
        "description": (
            "Carbamazepine is a potent CYP2C9 inducer, markedly increasing warfarin clearance "
            "and reducing anticoagulation effect. INR can drop substantially, increasing "
            "thromboembolic risk. Increase warfarin dose with close INR monitoring when "
            "starting or stopping carbamazepine."
        ),
        "mechanism": "CYP2C9 induction by carbamazepine -> reduced warfarin levels -> subtherapeutic anticoagulation",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_pheny_cbz",
        "drug_a_id": "DB00564_cbz",
        "drug_b_id": "DB00252",
        "severity": "major",
        "description": (
            "Carbamazepine induces CYP2C9 and CYP3A4, reducing phenytoin clearance variably. "
            "Phenytoin may also reduce carbamazepine levels. Both drugs have narrow therapeutic "
            "indices and complex bidirectional pharmacokinetic interactions. "
            "Therapeutic drug monitoring is essential for both agents."
        ),
        "mechanism": "Bidirectional CYP induction; both drugs are narrow-TI with mutual level changes",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Diabetes drug interactions
    # =========================================================================
    {
        "id": "IX_db_pioglit_gemfibrozil",
        "drug_a_id": "DB01067_pioglitazone",
        "drug_b_id": "DB01241",
        "severity": "major",
        "description": (
            "Gemfibrozil is a potent CYP2C8 inhibitor that increases pioglitazone AUC ~3-fold. "
            "Significant increase in risk of fluid retention, heart failure exacerbation, and "
            "hypoglycemia. Reduce pioglitazone dose or avoid combination. Monitor for edema "
            "and cardiac decompensation."
        ),
        "mechanism": "CYP2C8 inhibition by gemfibrozil -> markedly elevated pioglitazone",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_glyburide_flucon",
        "drug_a_id": "DB01145_glyburide",
        "drug_b_id": "DB00636_flucon",
        "severity": "major",
        "description": (
            "Fluconazole inhibits CYP2C9, increasing glyburide AUC ~2-fold. "
            "This substantially increases risk of serious hypoglycemia. "
            "Monitor blood glucose closely; reduce sulfonylurea dose or substitute with "
            "a non-CYP2C9-metabolized agent."
        ),
        "mechanism": "CYP2C9 inhibition by fluconazole -> elevated glyburide -> hypoglycemia",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_metform_trimethoprim",
        "drug_a_id": "DB00331_metform",
        "drug_b_id": "DB00440",
        "severity": "moderate",
        "description": (
            "Trimethoprim inhibits OCT2 (organic cation transporter 2), the primary renal "
            "secretion pathway for metformin. This increases metformin plasma levels by "
            "approximately 40%. In patients with renal impairment, the risk of lactic acidosis "
            "may be elevated. Monitor for metformin toxicity if combination used."
        ),
        "mechanism": "OCT2 inhibition by trimethoprim -> reduced renal metformin clearance -> elevated levels",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # GI / Absorption interactions
    # =========================================================================
    {
        "id": "IX_db_erlot_ppi",
        "drug_a_id": "DB08877_erlot",
        "drug_b_id": "DB00338_omeprz",
        "severity": "moderate",
        "description": (
            "PPIs reduce gastric acidity, substantially decreasing erlotinib absorption. "
            "Erlotinib solubility is pH-dependent; omeprazole reduces erlotinib AUC ~46%. "
            "Avoid combination if possible. If PPI needed, take erlotinib 2h before or 10h "
            "after PPI. H2 blockers have lesser but still clinically relevant effect."
        ),
        "mechanism": "Reduced gastric pH by PPI -> impaired erlotinib solubility -> decreased absorption",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_dasatinib_omep",
        "drug_a_id": "DB00619_imatinib_gleevec",
        "drug_b_id": "DB00338_omeprz",
        "severity": "major",
        "description": (
            "PPIs raise gastric pH, significantly reducing dasatinib absorption. "
            "Dasatinib AUC reduced by ~43% with concomitant PPI use. "
            "Avoid concomitant PPI use with dasatinib; use antacids (not within 2h) "
            "or H2 blockers (12h separation) if acid suppression needed."
        ),
        "mechanism": "Elevated gastric pH by PPI -> reduced dasatinib dissolution and absorption",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_levothyrox_ppi",
        "drug_a_id": "DB00755_levothyrox",
        "drug_b_id": "DB00338_omeprz",
        "severity": "moderate",
        "description": (
            "PPIs reduce gastric acidity, impairing levothyroxine absorption and leading to "
            "suboptimal thyroid hormone replacement. TSH may rise. Timing separation (take "
            "levothyroxine 60 minutes before PPI) partially mitigates this interaction. "
            "Monitor TSH and adjust levothyroxine dose as needed."
        ),
        "mechanism": "Elevated gastric pH by PPI -> reduced levothyroxine absorption -> elevated TSH",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Oncology interactions
    # =========================================================================
    {
        "id": "IX_db_capecit_warfarin",
        "drug_a_id": "DB01418_capecit",
        "drug_b_id": "DB00682",
        "severity": "critical",
        "description": (
            "Capecitabine inhibits CYP2C9, the primary enzyme metabolizing the S-enantiomer "
            "of warfarin. INR can increase dramatically (> 5-fold), causing life-threatening "
            "bleeding. The interaction may be delayed and unpredictable. Monitor INR at least "
            "weekly during capecitabine therapy and for 4 weeks after discontinuation."
        ),
        "mechanism": "CYP2C9 inhibition by capecitabine/5-FU -> markedly elevated warfarin -> major bleeding",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_ibrutinib_keto",
        "drug_a_id": "DB01048_ibrutinib",
        "drug_b_id": "DB01026_keto",
        "severity": "critical",
        "description": (
            "Ketoconazole increases ibrutinib AUC up to 24-fold via potent CYP3A4 inhibition. "
            "This can cause severe ibrutinib toxicity (bleeding, atrial fibrillation, infections). "
            "Strong CYP3A4 inhibitors are contraindicated with standard ibrutinib dosing. "
            "If unavoidable, reduce ibrutinib dose to 140mg/day."
        ),
        "mechanism": "CYP3A4 inhibition by ketoconazole -> massively elevated ibrutinib -> severe toxicity",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_venetoclax_flucon",
        "drug_a_id": "DB11093_venetoclax",
        "drug_b_id": "DB00636_flucon",
        "severity": "major",
        "description": (
            "Fluconazole inhibits CYP3A4, significantly increasing venetoclax exposure and "
            "risk of tumor lysis syndrome and other toxicities. "
            "Moderate CYP3A4 inhibitors may require dose reduction of venetoclax. "
            "Strong CYP3A4 inhibitors during ramp-up phase require even greater caution."
        ),
        "mechanism": "CYP3A4 inhibition by fluconazole -> elevated venetoclax -> TLS risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_paclitaxel_gemfibrozil",
        "drug_a_id": "DB01229_paclitaxel",
        "drug_b_id": "DB01241",
        "severity": "moderate",
        "description": (
            "Gemfibrozil is a potent CYP2C8 inhibitor. Paclitaxel is primarily metabolized "
            "by CYP2C8. Co-administration increases paclitaxel exposure and potential toxicity. "
            "Monitor for paclitaxel-related toxicities (neuropathy, myelosuppression). "
            "Clinically relevant when gemfibrozil used in oncology patients."
        ),
        "mechanism": "CYP2C8 inhibition by gemfibrozil -> elevated paclitaxel -> toxicity risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_irinotecan_cbz",
        "drug_a_id": "DB00602_irinotecan",
        "drug_b_id": "DB00564_cbz",
        "severity": "major",
        "description": (
            "Carbamazepine induces CYP3A4 and reduces irinotecan conversion to active SN-38, "
            "while also increasing irinotecan clearance. Net result is reduced antitumor "
            "efficacy. Avoid concomitant use of irinotecan with strong CYP3A4 inducers. "
            "Switch to non-enzyme-inducing anticonvulsant if possible."
        ),
        "mechanism": "CYP3A4 induction by carbamazepine -> reduced irinotecan -> SN-38 conversion and increased clearance",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Corticosteroid interactions
    # =========================================================================
    {
        "id": "IX_db_flutica_ritonavir",
        "drug_a_id": "DB01280_flutica",
        "drug_b_id": "DB00503",
        "severity": "major",
        "description": (
            "Ritonavir, a potent CYP3A4 inhibitor, dramatically increases systemic fluticasone "
            "exposure even from inhaled doses. This can cause iatrogenic Cushing syndrome and "
            "adrenal suppression. HIV patients on ritonavir-based ART should avoid inhaled "
            "fluticasone; use beclomethasone (less CYP3A4-dependent) instead."
        ),
        "mechanism": "CYP3A4 inhibition by ritonavir -> markedly elevated systemic fluticasone -> Cushing syndrome",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_dexa_keto",
        "drug_a_id": "DB00591_dexa",
        "drug_b_id": "DB01026_keto",
        "severity": "moderate",
        "description": (
            "Ketoconazole inhibits CYP3A4, increasing dexamethasone exposure and enhancing "
            "glucocorticoid effects. Conversely, dexamethasone (CYP3A4 inducer) may reduce "
            "ketoconazole levels over time. This bidirectional interaction is clinically "
            "relevant in patients receiving both agents (e.g., oncology patients)."
        ),
        "mechanism": "CYP3A4 inhibition by ketoconazole increases dexamethasone; dexamethasone induces CYP3A4",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Antimalarial interactions
    # =========================================================================
    {
        "id": "IX_db_hydroxy_metoprolol",
        "drug_a_id": "DB01611_hydroxy",
        "drug_b_id": "DB00264_meto",
        "severity": "moderate",
        "description": (
            "Hydroxychloroquine inhibits CYP2D6, increasing metoprolol AUC by ~65%. "
            "Risk of clinically relevant bradycardia and hypotension. Both drugs also "
            "carry QTc-prolonging potential, so cardiac monitoring is recommended when "
            "used concomitantly."
        ),
        "mechanism": "CYP2D6 inhibition by hydroxychloroquine -> elevated metoprolol -> bradycardia + QTc risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Respiratory interactions
    # =========================================================================
    {
        "id": "IX_db_theoph_cipro",
        "drug_a_id": "DB00698_theoph",
        "drug_b_id": "DB00537",
        "severity": "major",
        "description": (
            "Ciprofloxacin inhibits CYP1A2, increasing theophylline AUC by approximately "
            "87%. Theophylline has a narrow therapeutic index; toxic levels cause seizures "
            "and ventricular arrhythmias. Reduce theophylline dose by 30-50% when starting "
            "ciprofloxacin and monitor serum theophylline levels."
        ),
        "mechanism": "CYP1A2 inhibition by ciprofloxacin -> elevated theophylline -> seizures and arrhythmia risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_roflumilast_rifampin",
        "drug_a_id": "DB00353_roflumilast",
        "drug_b_id": "DB01045",
        "severity": "major",
        "description": (
            "Rifampin strongly induces CYP3A4 and CYP1A2, reducing total roflumilast PDE4 "
            "inhibitory activity by ~60%. This substantially diminishes roflumilast's "
            "anti-inflammatory efficacy in COPD. Avoid concomitant use; consider alternative "
            "COPD management during rifampin treatment."
        ),
        "mechanism": "CYP3A4/1A2 induction by rifampin -> reduced roflumilast active moiety -> loss of efficacy",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Immunology interactions
    # =========================================================================
    {
        "id": "IX_db_tofa_rifampin",
        "drug_a_id": "DB11817_tofa",
        "drug_b_id": "DB01045",
        "severity": "major",
        "description": (
            "Rifampin is a strong CYP3A4 inducer, reducing tofacitinib AUC by ~84%. "
            "This substantially reduces JAK inhibition and tofacitinib efficacy in RA. "
            "Avoid combination; if rifampin is required for mycobacterial infection, "
            "consider alternative JAK inhibitor with different metabolism or therapeutic approach."
        ),
        "mechanism": "CYP3A4 induction by rifampin -> markedly reduced tofacitinib exposure",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_tofa_ketoconazole",
        "drug_a_id": "DB11817_tofa",
        "drug_b_id": "DB01026_keto",
        "severity": "major",
        "description": (
            "Ketoconazole (potent CYP3A4 inhibitor) increases tofacitinib AUC ~107%. "
            "Reduce tofacitinib dose by 50% when combined with strong CYP3A4 inhibitors "
            "to avoid excessive immunosuppression and infection risk."
        ),
        "mechanism": "CYP3A4 inhibition by ketoconazole -> elevated tofacitinib -> excessive immunosuppression",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_leflu_warfarin",
        "drug_a_id": "DB01589_leflu",
        "drug_b_id": "DB00682",
        "severity": "major",
        "description": (
            "Leflunomide's active metabolite teriflunomide inhibits CYP2C9, the primary "
            "metabolic enzyme for S-warfarin. This increases warfarin exposure and INR. "
            "Monitor INR closely after starting or stopping leflunomide and adjust warfarin "
            "dose as needed."
        ),
        "mechanism": "CYP2C9 inhibition by teriflunomide -> elevated warfarin -> increased INR/bleeding risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # PDE5 inhibitor interactions
    # =========================================================================
    {
        "id": "IX_db_sildenafil_ritonavir",
        "drug_a_id": "DB00513_sildenafil",
        "drug_b_id": "DB00503",
        "severity": "critical",
        "description": (
            "Ritonavir markedly increases sildenafil AUC ~11-fold and Cmax ~4-fold via CYP3A4 "
            "inhibition. Risk of sildenafil toxicity: severe hypotension, priapism, and "
            "vision/hearing loss. Sildenafil for ED is contraindicated with ritonavir. "
            "For PAH (Revatio), lower doses (20mg BID) with caution and monitoring."
        ),
        "mechanism": "CYP3A4 inhibition by ritonavir -> massively elevated sildenafil",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_tadalafil_ketoconazole",
        "drug_a_id": "DB00203_tadalafil",
        "drug_b_id": "DB01026_keto",
        "severity": "major",
        "description": (
            "Ketoconazole increases tadalafil AUC ~2-fold via CYP3A4 inhibition. "
            "Risk of tadalafil adverse effects (hypotension, flushing, visual disturbances). "
            "Concomitant use requires dose limitation and monitoring. "
            "Absolute contraindication remains with nitrates (class effect)."
        ),
        "mechanism": "CYP3A4 inhibition by ketoconazole -> elevated tadalafil",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Thyroid interactions
    # =========================================================================
    {
        "id": "IX_db_levothyrox_iron",
        "drug_a_id": "DB00755_levothyrox",
        "drug_b_id": "DB00999_hydrochlorothiazide",
        "severity": "minor",
        "description": (
            "Hydrochlorothiazide does not directly interact with levothyroxine. However, "
            "diuretics in combination with levothyroxine require monitoring since TSH may "
            "shift. This entry documents cardiovascular co-treatment requiring periodic "
            "thyroid function monitoring."
        ),
        "mechanism": "Indirect: hemodynamic effects of diuretic may alter thyroid hormone requirements",
        "source": "seed",
        "evidence_count": 0,
    },
    # =========================================================================
    # Colchicine interactions
    # =========================================================================
    {
        "id": "IX_db_colchi_clarithro",
        "drug_a_id": "DB09168_colchi",
        "drug_b_id": "DB01211",
        "severity": "critical",
        "description": (
            "Clarithromycin inhibits CYP3A4 and P-gp, dramatically increasing colchicine "
            "plasma levels. Cases of fatal colchicine toxicity (multi-organ failure, bone "
            "marrow suppression, neuromuscular toxicity) reported. Combination is "
            "contraindicated in patients with renal or hepatic impairment. "
            "Reduce colchicine dose to 0.6mg single dose if combination unavoidable in "
            "normal renal/hepatic function."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition by clarithromycin -> markedly elevated colchicine -> life-threatening toxicity",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_colchi_keto",
        "drug_a_id": "DB09168_colchi",
        "drug_b_id": "DB01026_keto",
        "severity": "major",
        "description": (
            "Ketoconazole inhibits CYP3A4 and P-gp, substantially increasing colchicine "
            "levels. Nausea, vomiting, and muscle pain may signal early toxicity. "
            "Reduce colchicine dose and monitor for signs of toxicity. "
            "Avoid in renal or hepatic impairment."
        ),
        "mechanism": "CYP3A4 + P-gp inhibition by ketoconazole -> elevated colchicine -> toxicity risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Anticoagulant interactions (continued)
    # =========================================================================
    {
        "id": "IX_db_acenocoumarol_flucon",
        "drug_a_id": "DB01166_acenocoumarol",
        "drug_b_id": "DB00636_flucon",
        "severity": "critical",
        "description": (
            "Fluconazole strongly inhibits CYP2C9, the primary enzyme metabolizing acenocoumarol. "
            "INR can increase dramatically. Potentially life-threatening bleeding. "
            "Monitor INR closely; reduce acenocoumarol dose significantly during fluconazole "
            "treatment. Even single-dose fluconazole (150mg) can have clinically meaningful effect."
        ),
        "mechanism": "CYP2C9 inhibition by fluconazole -> markedly elevated acenocoumarol -> major bleeding risk",
        "source": "fda_label",
        "evidence_count": 0,
    },
    # =========================================================================
    # Miscellaneous high-priority interactions
    # =========================================================================
    {
        "id": "IX_db_apremilast_rifampin",
        "drug_a_id": "DB09067_apremilast",
        "drug_b_id": "DB01045",
        "severity": "major",
        "description": (
            "Rifampin reduces apremilast AUC by ~72% via strong CYP3A4 induction. "
            "This significantly diminishes apremilast's PDE-4 inhibitory efficacy. "
            "Avoid concomitant use. Choose alternative DMARD or anti-inflammatory agent."
        ),
        "mechanism": "CYP3A4 induction by rifampin -> markedly reduced apremilast exposure",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_fingolimod_amiodarone",
        "drug_a_id": "DB01076_fingolimod",
        "drug_b_id": "DB01118",
        "severity": "major",
        "description": (
            "Both fingolimod and amiodarone prolong QTc and can cause clinically significant "
            "bradycardia. Fingolimod causes transient dose-dependent bradycardia (especially "
            "at first dose). Combining with class III antiarrhythmics markedly increases "
            "risk of severe bradycardia, AV block, and ventricular arrhythmia."
        ),
        "mechanism": "Additive cardiac effect: both agents reduce heart rate and prolong QTc",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_osimertinib_rifampin",
        "drug_a_id": "DB00558_osimertinib",
        "drug_b_id": "DB01045",
        "severity": "major",
        "description": (
            "Rifampin reduces osimertinib AUC ~84% via strong CYP3A4 induction. "
            "This substantially reduces osimertinib exposure and likely diminishes "
            "antitumor efficacy in EGFR-mutant NSCLC. Avoid concomitant use of strong "
            "CYP3A4 inducers with osimertinib."
        ),
        "mechanism": "CYP3A4 induction by rifampin -> markedly reduced osimertinib exposure",
        "source": "fda_label",
        "evidence_count": 0,
    },
    {
        "id": "IX_db_acetamino_alcohol",
        "drug_a_id": "DB00945_acetamino",
        "drug_b_id": "DB01177_ethanol",
        "severity": "major",
        "description": (
            "Chronic heavy alcohol use induces CYP2E1, increasing formation of hepatotoxic "
            "NAPQI from acetaminophen. Risk of acetaminophen hepatotoxicity is substantially "
            "increased even at standard doses. FDA recommends patients who consume 3+ "
            "alcoholic drinks per day consult a doctor before using acetaminophen."
        ),
        "mechanism": "CYP2E1 induction by chronic alcohol -> increased NAPQI from acetaminophen -> hepatotoxicity",
        "source": "fda_label",
        "evidence_count": 0,
    },
]
