########################### Import


import pandas as pd


########################### Calculs des propriétés de l'air

proprietes_air_xl = 'Propriétés air.xlsx'
proprietes_air = pd.read_excel(proprietes_air_xl, sheet_name="Feuil1")
nbre_lignes_proprietes_air = len(proprietes_air)
gamma_table = {proprietes_air["Temperature (K)"].tolist()[i] : proprietes_air["Ratio of specific heats gamma, (cp/cv)"].tolist()[i] for i in range(nbre_lignes_proprietes_air)}
cp_table = {proprietes_air["Temperature (K)"].tolist()[i] : proprietes_air["Specific heat cp (kJ/kg/K)"].tolist()[i] for i in range(nbre_lignes_proprietes_air)}

far_xl = "Fuel Air ratio.xlsx"      # far = Fuel Air ratio
far = pd.read_excel(far_xl, sheet_name="Feuil1")
nbre_lignes_far = len(far)
far_bornes1A_temperature = {far["inlet air temperature (K)"].tolist()[i] : far["temperature rise bornes 1A (K)"][i] for i in range(nbre_lignes_far)}
far_bornes1A_far = {far["inlet air temperature (K)"].tolist()[i] : far["fuel/air ratio borne 1A"][i] for i in range(nbre_lignes_far)}
far_bornes1B_temperature = {far["inlet air temperature (K)"].tolist()[i] : far["temperature rise bornes 1B (K)"][i] for i in range(nbre_lignes_far)}
far_bornes1B_far = {far["inlet air temperature (K)"].tolist()[i] : far["fuel/air ratio borne 1B"][i] for i in range(nbre_lignes_far)}
far_bornes2A_temperature = {far["inlet air temperature (K)"].tolist()[i] : far["temperature rise bornes 2A (K)"][i] for i in range(nbre_lignes_far)}
far_bornes2A_far = {far["inlet air temperature (K)"].tolist()[i] : far["fuel/air ratio borne 2A"][i] for i in range(nbre_lignes_far)}
far_bornes2B_temperature = {far["inlet air temperature (K)"].tolist()[i] : far["temperature rise bornes 2B (K)"][i] for i in range(nbre_lignes_far)}
far_bornes2B_far = {far["inlet air temperature (K)"].tolist()[i] : far["fuel/air ratio borne 2B"][i] for i in range(nbre_lignes_far)}


########################### Extraction du paramétrage du système depuis l'Excel Interface


interface_xl = 'Interface.xlsx'
user = pd.read_excel(interface_xl, sheet_name="user")

sequence_table = user["Séquence"].tolist()
sequence_table = [x for x in sequence_table if pd.isnull(x) == False]      # Supprimer les nan de la liste

python = pd.read_excel(interface_xl, sheet_name="python")

air_exterieur_table = python["Air exterieur"].tolist()
air_exterieur_table = [x for x in air_exterieur_table if pd.isnull(x) == False]

compresseur_table = python["Compresseur"].tolist()
compresseur_table = [x for x in compresseur_table if pd.isnull(x) == False]

combustion_table = python["Chambre de combustion"].tolist()
combustion_table = [x for x in combustion_table if pd.isnull(x) == False]

turbine_table = python["Turbine"].tolist()
turbine_table = [x for x in turbine_table if pd.isnull(x) == False]

echangeur_table = python["Échangeur de chaleur"].tolist()
echangeur_table = [x for x in echangeur_table if pd.isnull(x) == False]