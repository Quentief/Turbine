########################### Import

import pandas as pd

########################### Calculs des propriétés de l'air

proprietes_air_xl = 'Model\Propriétés air.xlsx'
proprietes_air = pd.read_excel(proprietes_air_xl, sheet_name="Feuil1")
nbre_lignes_proprietes_air = len(proprietes_air)
gamma_table = {proprietes_air["Temperature (K)"].tolist()[i] : proprietes_air["Ratio of specific heats gamma, (cp/cv)"].tolist()[i] for i in range(nbre_lignes_proprietes_air)}
cp_table = {proprietes_air["Temperature (K)"].tolist()[i] : proprietes_air["Specific heat cp (kJ/kg/K)"].tolist()[i] for i in range(nbre_lignes_proprietes_air)}

far_xl = "Model\Fuel Air ratio.xlsx"      # far = Fuel Air ratio
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

class Cycle :
    def __init__(self, user, python):
        self.titre = user.keys()[1]
        self.sequence = self.sequence_fonction(user[self.titre].tolist(), user["Nom composants"].tolist())
        self.air_exterieur_table = self.raccourcir_liste(user["Air exterieur"].tolist())
        self.parametrage = self.parametrage_fonction(self.sequence, python)
    def sequence_fonction(self,code_sequence, noms_composants):
        code_sequence = code_sequence[0:len(code_sequence) - 9]  # On retire la légende de l'XL de la liste
        sequence = {}
        for i in range(len(code_sequence)):
            if not pd.isnull(code_sequence[i]):
                sequence[noms_composants[i]] = code_sequence[i]
        return sequence
    def parametrage_fonction(self, sequence, python):
        liste_r = python["Ratio compression"].tolist()
        liste_NM = python["Rendement mécanique (%)"].tolist()
        liste_NT = python["Rendement thermique (%)"].tolist()
        liste_NI = python["Rendement isentropique (%)"].tolist()
        liste_NP = python["Rendement polytropique (%)"].tolist()
        liste_T = python["Température combustion (K)"].tolist()
        liste_dPp = python["Pertes de charges (%)"].tolist()
        liste_dPb = python["Pertes de charges à la sortie (bar)"].tolist()
        parametrage = {}
        for i in range(len(sequence.keys())) :
            nom = list(sequence.keys())[i]
            parametrage[nom] = [ liste_r[i], liste_NM[i], liste_NT[i], liste_NI[i], liste_NP[i],
                                             liste_T[i], liste_dPp[i], liste_dPb[i] ]
        return parametrage
    def raccourcir_liste(self,liste):
        return [x for x in liste if pd.isnull(x) == False]



interface_xl = 'Interface2.xlsx'
user1 = pd.read_excel(interface_xl, sheet_name="Cycle 1")
user2 = pd.read_excel(interface_xl, sheet_name="Cycle 2")
python1 = pd.read_excel(interface_xl, sheet_name="Python 1")
python2 = pd.read_excel(interface_xl, sheet_name="Python 2")

cycle1 = Cycle(user1,python1)
cycle2 = Cycle(user1,python2)