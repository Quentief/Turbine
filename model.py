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

