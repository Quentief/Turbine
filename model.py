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

class Parametrage :
    pass

parametrage1 = Parametrage()
parametrage2 = Parametrage()


interface_xl = 'Interface.xlsx'
user = pd.read_excel(interface_xl, sheet_name="user")

sequence1 = user["Séquence 1"].tolist()
sequence1 = [x for x in sequence1 if pd.isnull(x) == False]      # Supprimer les nan de la liste
sequence2 = user["Séquence 2"].tolist()
sequence2 = [x for x in sequence2 if pd.isnull(x) == False]

python1 = pd.read_excel(interface_xl, sheet_name="python 1")
python2 = pd.read_excel(interface_xl, sheet_name="python 2")

parametrage1.air_exterieur_table = python1["Air exterieur"].tolist()
parametrage1.air_exterieur_table  = [x for x in parametrage1.air_exterieur_table if pd.isnull(x) == False]
parametrage2.air_exterieur_table = python2["Air exterieur"].tolist()
parametrage2.air_exterieur_table  = [x for x in parametrage2.air_exterieur_table if pd.isnull(x) == False]

parametrage1.compresseur_table = python1["Compresseur"].tolist()
parametrage1.compresseur_table = [x for x in parametrage1.compresseur_table if pd.isnull(x) == False]
parametrage2.compresseur_table = python2["Compresseur"].tolist()
parametrage2.compresseur_table = [x for x in parametrage2.compresseur_table if pd.isnull(x) == False]

parametrage1.combustion_table = python1["Chambre de combustion"].tolist()
parametrage1.combustion_table = [x for x in parametrage1.combustion_table if pd.isnull(x) == False]
parametrage2.combustion_table = python2["Chambre de combustion"].tolist()
parametrage2.combustion_table = [x for x in parametrage2.combustion_table if pd.isnull(x) == False]

parametrage1.power_turbine_table = python1["Power turbine"].tolist()
parametrage1.power_turbine_table = [x for x in parametrage1.power_turbine_table if pd.isnull(x) == False]
parametrage2.power_turbine_table = python2["Power turbine"].tolist()
parametrage2.power_turbine_table = [x for x in parametrage2.power_turbine_table if pd.isnull(x) == False]

parametrage1.echangeur_table = python1["Échangeur de chaleur"].tolist()
parametrage1.echangeur_table = [x for x in parametrage1.echangeur_table if pd.isnull(x) == False]
parametrage2.echangeur_table = python2["Échangeur de chaleur"].tolist()
parametrage2.echangeur_table = [x for x in parametrage2.echangeur_table if pd.isnull(x) == False]

parametrage1.gas_generator_table = python1["Gas generator"].tolist()
parametrage1.gas_generator_table = [x for x in parametrage1.gas_generator_table if pd.isnull(x) == False]
parametrage2.gas_generator_table = python2["Gas generator"].tolist()
parametrage2.gas_generator_table = [x for x in parametrage2.gas_generator_table if pd.isnull(x) == False]