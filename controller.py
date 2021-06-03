########################### Import

from model import proprietes_air, gamma_table, cp_table, far_bornes1A_temperature, far_bornes1B_temperature, \
    far_bornes1A_far, far_bornes1B_far, far_bornes2A_temperature, far_bornes2B_temperature, far_bornes2A_far, \
    far_bornes2B_far

from view import air_exterieur_table, compresseur_table, combustion_table, turbine_table, echangeur_table, \
    sequence_table

import bisect as bis

########################### Calculs des propriétés de l'air

class Air:
    def __init__(self,pression,temperature):
        self.pression = pression
        self.temperature = temperature
        self.gamma = self.gamma_function(temperature)
        self.cp = self.cp_function(temperature)
    def __str__(self):
        return "Pression : {:.2f} bars | Temperature {:.2f} K".format(self.pression,self.temperature)
    def gamma_function(self,temperature):
        temperature_table = proprietes_air["Temperature (K)"].tolist()
        if temperature in temperature_table:
            return gamma_table[temperature]
        else:
            bis.insort(temperature_table, temperature)
            index = temperature_table.index(temperature)
            # Regression linéaire :
            temperatureA = temperature_table[index - 1]
            temperatureB = temperature_table[index + 1]
            return gamma_table[temperatureA] + (gamma_table[temperatureB] - gamma_table[temperatureA]) / (temperatureB - temperatureA) * (temperature - temperatureA)
    def cp_function(self,temperature):
        temperature_table = proprietes_air["Temperature (K)"].tolist()
        if temperature in temperature_table:
            return cp_table[temperature]
        else:
            bis.insort(temperature_table, temperature)
            index = temperature_table.index(temperature)
            # Regression linéaire :
            temperatureA = temperature_table[index - 1]
            temperatureB = temperature_table[index + 1]
            return cp_table[temperatureA] + (cp_table[temperatureB] - cp_table[temperatureA]) / (temperatureB - temperatureA) * (temperature - temperatureA)

########################### Modélisation des composants

class Compresseur:
    def __init__(self,air_entree, r, NC, NM):
        self.air_entree = air_entree
        self.r = r
        self.NC = NC
        self.NM = NM
        self.air_sortie = Air(r*self.air_entree.pression,self.calcul_temperature_sortie(self.air_entree.gamma,self.air_entree.temperature,self.NC,self.r))
        self.travail = self.calcul_travail(self.air_entree.cp, self.air_entree.temperature, self.air_sortie.temperature, self.NM)
    def calcul_temperature_sortie(self,gamma,Ta,NC,r):
        return Ta + Ta/NC * ( r**( (gamma - 1)/gamma) - 1)
    def calcul_travail(self, cp, Ta, T2, NM):
        return cp*(T2 - Ta)/NM


class Combustion:
    def __init__(self, air_entree, dPB, TB, NB):
        self.air_entree = air_entree
        self.air_sortie = Air(air_entree.pression*(1-dPB), TB)
        self.TB = TB
        self.far = self.calcul_FA_ratio(TB - air_entree.temperature)/NB
    def calcul_FA_ratio(self,temperature_rise):
        gamme_temerature = list(far_bornes1A_temperature.keys())
        inlet_air_temperature = min(gamme_temerature, key=lambda x:abs(x-air_entree.temperature))        # trouve la temperature la plus proche dans la gamme
        if temperature_rise <= far_bornes1A_temperature[inlet_air_temperature] :
            temperature_A = far_bornes1A_temperature[inlet_air_temperature]
            temperature_B = far_bornes1B_temperature[inlet_air_temperature]
            far_A = far_bornes1A_far[inlet_air_temperature]
            far_B = far_bornes1B_far[inlet_air_temperature]
        else :
            temperature_A = far_bornes2A_temperature[inlet_air_temperature]
            temperature_B = far_bornes2B_temperature[inlet_air_temperature]
            far_A = far_bornes2A_far[inlet_air_temperature]
            far_B = far_bornes2B_far[inlet_air_temperature]
        return far_A + (far_B - far_A)/(temperature_B - temperature_A)*(temperature_rise - temperature_A)


class Turbine:
    def __init__(self,air_entree,pression_sortie,NT):
        self.air_entree = air_entree
        self.pression_sortie = pression_sortie
        self.NT = NT
        self.gaz_sortie = self.calcul_air_sortie(self.pression_sortie, self.air_entree.temperature, self.air_entree.pression, self.pression_sortie, self.air_entree.gamma, self.NT)
        self.travail = self.calcul_travail(self.air_entree.cp, self.air_entree.temperature, self.gaz_sortie.temperature)
    def calcul_air_sortie(self,pression_sortie,T3,P3,P4,gamma,NT):
        T4 = T3 - NT*T3*(1 - (P4/P3)**((gamma-1)/gamma))
        return Air(pression_sortie,T4)
    def calcul_travail(self, cp, T3, T4):
        return cp*(T3 - T4)


class Echangeur_chaleur :
    def __init__(self,air_entree,NE,dPEa,dPEg,temperature_gaz_entree,pression_gaz_sortie):
        self.air_entree = air_entree
        self.pression_gaz_sortie = pression_gaz_sortie
        self.temperature_gaz_entree = temperature_gaz_entree
        self.NE = NE
        self.dPEa = dPEa
        self.dPEg = dPEg
        self.air_sortie = self.calcul_air_sortie(self.air_entree.temperature,self.temperature_gaz_entree,self.dPEa,self.NE,self.air_entree)
        self.gaz_entree = self.calcul_gaz_entree(self.pression_gaz_sortie,self.dPEg,self.temperature_gaz_entree)
    def calcul_air_sortie(self, T2, T4,dPEa,NE,air_entree):
        T5 = NE * (T4 - T2) + T2
        P5 = air_entree.pression * (1 - dPEa)
        return Air(P5, T5)
    def calcul_gaz_entree(self,pression_gaz_sortie,dPEg,temperature_gaz_entree):
        P4 = pression_gaz_sortie + dPEg
        T4 = temperature_gaz_entree
        return Air(P4,T4)


class Performance :
    def __init__(self,compresseur,turbine,combustion):
        self.puissance_specifique_sortie = turbine.travail - compresseur.travail
        self.sfc = 3600*combustion.far / (self.puissance_specifique_sortie)       # SFC = spécific fuel consumption
        self.rendement = 3600 / (self.sfc*43100)      # 43 100 kJ/kg = PCI du kérosène
    def __str__(self):
        return "Specific power output : {:.2f} kJ/kg | SFC {:.2f} kg/kWh " \
               "| Rendement global : {:.2f} % ".format(self.puissance_specifique_sortie, self.sfc,self.rendement*100)


########################### Auto-programmation de la séquence

def sequence(sequence_table, sequence_table_sans_EC, air_entree_table, air_sortie_table, indice) :
    if indice == 0 :        # Indice = 0 -> pas d'échangeur, Indice = 1 -> échangeur considéré
        sequence_indice = sequence_table_sans_EC
    else :
        sequence_indice = sequence_table
    ### Paramétrage de l'air exterieur puor les 1er et derniers composants
    air_entree_table[sequence_indice[0]] = Air(float(air_exterieur_table[0]), float(air_exterieur_table[1]))
    air_sortie_table[sequence_indice[-1]] = Air(float(air_exterieur_table[0]), float(air_exterieur_table[1]))
    for i in range(len(sequence_indice)):
        code_element = sequence_indice[i]
        if code_element == 1:  # Compresseur
            air_entree = air_entree_table[1]
            compresseur = Compresseur(air_entree, float(compresseur_table[0]), float(compresseur_table[2]),
                                      float(compresseur_table[1]))
            air_sortie_table[1] = compresseur.air_sortie
            air_entree_table[sequence_indice[i] + 1] = compresseur.air_sortie
        elif code_element == 2:  # Chambre combustion
            air_entree = air_entree_table[2]
            combustion = Combustion(air_entree, float(combustion_table[2]), float(combustion_table[0]),
                                    float(combustion_table[1]))
            air_sortie_table[2] = combustion.air_sortie
            air_entree_table[sequence_indice[i] + 1] = combustion.air_sortie
        elif code_element == 3:  # Turbine
            air_entree = air_entree_table[3]
            pression_sortie = air_sortie_table[3].pression
            turbine = Turbine(air_entree, pression_sortie, float(turbine_table[0]))
            air_sortie_table[3] = turbine.gaz_sortie
            air_entree_table[sequence_indice[i] + 1] = turbine.gaz_sortie
        elif code_element == 4.1 or code_element == 4.2 :      # Échangeur de chaleur, côté air frais
            air_entree = air_entree_table[4.1]
            temperature_gaz_entree = air_entree.temperature
            pression_gaz_sortie = air_sortie_table[4.2].pression
            echangeur = Echangeur_chaleur(air_entree,float(echangeur_table[0]),float(echangeur_table[1]),
                                          float(echangeur_table[2]),temperature_gaz_entree,pression_gaz_sortie)
        if indice == 0 :
            j = sequence_table.index(code_element)
            air_entree_table[sequence_table[j+1]] = air_entree_table[sequence_indice[i] + 1]
    air_entree_table.popitem()
    performance = Performance(compresseur,turbine,combustion)
    return air_entree_table,air_sortie_table,performance


def start():
    air_entree_table = {i : 0 for i in sequence_table }
    air_sortie_table = {i: 0 for i in sequence_table}
    if 4.1 in sequence_table and 4.2 in sequence_table :        # Séquence sans échangeur de chaleur
        indice = 0
        sequence_table_sans_EC = sequence_table.copy()
        sequence_table_sans_EC.remove(4.1)
        sequence_table_sans_EC.remove(4.2)
        air_entree_table, air_sortie_table, performance = sequence(sequence_table, sequence_table_sans_EC,
                                                                   air_entree_table, air_sortie_table, indice)
    indice = 1
    air_entree_table, air_sortie_table, performance = sequence(sequence_table, sequence_table_sans_EC, air_entree_table,
                                                  air_sortie_table, indice)











