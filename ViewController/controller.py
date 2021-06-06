########################### Import

from Model.model import proprietes_air, gamma_table, cp_table, far_bornes1A_temperature, far_bornes1B_temperature, \
    far_bornes1A_far, far_bornes1B_far, far_bornes2A_temperature, far_bornes2B_temperature, far_bornes2A_far, \
    far_bornes2B_far, parametrage1, parametrage2, sequence1, sequence2

from ViewController.view import affichage_console, affichage_comparaison

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
            return gamma_table[temperatureA] + (gamma_table[temperatureB] - gamma_table[temperatureA]) / (temperatureB
                                                                        - temperatureA) * (temperature - temperatureA)
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
            return cp_table[temperatureA] + (cp_table[temperatureB] - cp_table[temperatureA]) / (temperatureB
                                                                    - temperatureA) * (temperature - temperatureA)

########################### Modélisation des composants

class Compresseur:
    def __init__(self,air_entree, r, NC, NM, cp):
        self.air_entree = air_entree
        self.air_sortie = Air(r*self.air_entree.pression,
                              self.calcul_temperature_sortie(self.air_entree.gamma,self.air_entree.temperature,NC,r))
        self.travail = self.calcul_travail(cp, self.air_entree.temperature, self.air_sortie.temperature, NM)
    def calcul_temperature_sortie(self,gamma,Ta,NC,r):
        return Ta + Ta/NC * ( r**( (gamma - 1)/gamma) - 1)
    def calcul_travail(self, cp, Ta, T2, NM):
        return cp*(T2 - Ta)/NM


class Combustion:
    def __init__(self, air_entree, dPB, TB, NB):
        self.air_entree = air_entree
        self.air_sortie = Air(air_entree.pression*(1-dPB), TB)
        self.far = self.calcul_FA_ratio(TB - air_entree.temperature)/NB
    def calcul_FA_ratio(self,temperature_rise):
        gamme_temerature = list(far_bornes1A_temperature.keys())
        inlet_air_temperature = min(gamme_temerature, key=lambda x:abs(x-self.air_entree.temperature))        # trouve la temperature la plus proche dans la gamme
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


class Power_turbine:
    def __init__(self,air_entree,pression_sortie,NT,NM,dPt,cp):
        self.air_entree = air_entree
        self.air_sortie = self.calcul_air_sortie(air_entree, pression_sortie, NT, dPt)
        self.travail = self.calcul_travail(air_entree, self.air_sortie.temperature,NM,cp)
        self.dPt = dPt
    def calcul_air_sortie(self,air_entree,P4,NT,dPt):
        T3 = air_entree.temperature
        P3 = air_entree.pression
        gamma = air_entree.gamma
        T4 = T3 * (1 - NT*(1 - ((P4 + dPt)/P3)**((gamma-1)/gamma)) )
        return Air(P4,T4)
    def calcul_travail(self, air_entree, T4,NM,cp):
        T3 = air_entree.temperature
        return cp*(T3 - T4)*NM


class Gas_generator_turbine :
    def __init__(self, air_entree, compresseur,NT,cp) :
        self.air_entree = air_entree
        self.compresseur = compresseur
        self.air_sortie = self.calcul_air_sortie(air_entree,compresseur,NT,cp)
    def calcul_air_sortie(self,air_entree,compresseur,NT,cp):
        T3 = air_entree.temperature
        T4 = T3 - compresseur.travail/cp
        exposant = air_entree.gamma / (air_entree.gamma -1)
        P4 = air_entree.pression*( 1 - (T3-T4)/(NT*T3) )**exposant
        return Air(P4,T4)


class Echangeur_chaleur :
    def __init__(self,air_entree,NE,dPEa,dPEg,temperature_gaz_entree,pression_gaz_sortie):
        self.air_entree = air_entree
        self.air_sortie = self.calcul_air_sortie(self.air_entree.temperature,temperature_gaz_entree,dPEa,NE,self.air_entree)
        self.gaz_entree = self.calcul_gaz_entree(pression_gaz_sortie,dPEg,temperature_gaz_entree)
    def calcul_air_sortie(self, T2, T4,dPEa,NE,air_entree):
        T5 = NE * (T4 - T2) + T2
        P5 = air_entree.pression * (1 - dPEa)
        return Air(P5, T5)
    def calcul_gaz_entree(self,pression_gaz_sortie,dPEg,temperature_gaz_entree):
        P4 = pression_gaz_sortie + dPEg
        T4 = temperature_gaz_entree
        return Air(P4,T4)


class Performance :
    def __init__(self,compresseur,turbine,combustion,travail_extrait_turbine):
        self.travail_compresseur = compresseur.travail
        self.travail_turbine = turbine.travail
        self.puissance_specifique_sortie = turbine.travail - travail_extrait_turbine
        self.sfc = 3600*combustion.far / (self.puissance_specifique_sortie)       # SFC = spécific fuel consumption
        self.rendement = 3600 / (self.sfc*43100)      # 43 100 kJ/kg = PCI du kérosène
    def __str__(self):
        return "Specific Power Output : {:.2f} kJ/kg | Specific Fuel Consumption {:.2f} kg/kWh " \
               "| Efficiency : {:.2f} % ".format(self.puissance_specifique_sortie, self.sfc,self.rendement*100)


class Repeteur():
    def __init__(self,air_entree):
        self.air_entree = air_entree
        self.air_sortie = air_entree


########################### Auto-programmation de la séquence


class Simulation :
    def __init__(self, sequence_table, parametrage):
        performance, air_table = self.auto_sequence(sequence_table, parametrage.air_exterieur_table, parametrage.compresseur_table,
            parametrage.combustion_table, parametrage.power_turbine_table, parametrage.echangeur_table, parametrage.gas_generator_table)
        self.performance = performance
        self.air_table = air_table
        self.sequence = sequence_table
    def __str__(self):
        return "Specific Power Output : {:.2f} kJ/kg | Specific Fuel Consumption {:.2f} kg/kWh " \
               "| Efficiency : {:.2f} % ".format(self.performance.puissance_specifique_sortie,
                                                 self.performance.sfc,self.performance.rendement*100)
    def auto_sequence(self, sequence_table, air_exterieur_table, compresseur_table, combustion_table, power_turbine_table,
                      echangeur_table, gas_generator_table) :
        air_entree_table = {i: 0 for i in sequence_table}
        air_sortie_table = {i: 0 for i in sequence_table}
        air_entree_table[sequence_table[0]] = Air(air_exterieur_table[0], air_exterieur_table[1])
        air_sortie_table[sequence_table[-1]] = Air(air_exterieur_table[0], air_exterieur_table[1])
        if 4.1 in sequence_table and 4.2 in sequence_table :
            sequence_sans_EC = sequence_table.copy()
            sequence_sans_EC.remove(4.1)
            sequence_sans_EC.remove(4.2)
            air_entree_table[sequence_sans_EC[0]] = Air(air_exterieur_table[0], air_exterieur_table[1])
            air_sortie_table[sequence_sans_EC[-1]] = Air(air_exterieur_table[0], air_exterieur_table[1])
        for i in range(100) :
            #print(i)
            for j in range(len(sequence_table)):
                code_element = sequence_table[j]
                #print(air_entree_table[code_element])
                #print(code_element)
                if i == 0 :
                    cp = air_entree_table[code_element].cp
                else :
                    cp = (air_entree_table[code_element].cp + air_sortie_table[code_element].cp) / 2
                if code_element == 1 :
                    compresseur = Compresseur(air_entree_table[1], compresseur_table[0], compresseur_table[2],
                                          compresseur_table[1],cp)
                    air_sortie_element = compresseur.air_sortie
                elif code_element == 2:
                    combustion = Combustion(air_entree_table[2], combustion_table[2], combustion_table[0],
                                         combustion_table[1])
                    air_sortie_element = combustion.air_sortie
                elif code_element == 3 :
                    power_turbine = Power_turbine(air_entree_table[3],air_sortie_table[3].pression,power_turbine_table[1],
                                                  power_turbine_table[0],power_turbine_table[2],cp)
                    air_sortie_element = power_turbine.air_sortie
                    if i == 0 :
                        air_sortie_element.pression += power_turbine.dPt
                elif code_element == 4.1 or code_element == 4.2 :
                    if i == 0 :
                        air_sortie_element = Repeteur(air_entree_table[code_element]).air_sortie
                    else :
                        echangeur = Echangeur_chaleur(air_entree_table[4.1],echangeur_table[0],echangeur_table[1],
                                                    echangeur_table[2],
                                                      air_entree_table[4.2].temperature,air_sortie_table[4.2].pression)
                        if code_element == 4.1 :
                            air_sortie_element = echangeur.air_sortie
                        else :
                            air_sortie_element = echangeur.gaz_entree
                            air_sortie_table[sequence_table[j-1]] = air_sortie_element
                elif code_element == 5.1 :
                    compresseur = Compresseur(air_entree_table[code_element],gas_generator_table[0],
                                              gas_generator_table[2],gas_generator_table[1],cp)
                    air_sortie_element = compresseur.air_sortie
                elif code_element == 5.2 :
                    gas_generator_turbine = Gas_generator_turbine(air_entree_table[5.2],compresseur,gas_generator_table[3],cp)
                    air_sortie_element = gas_generator_turbine.air_sortie
                if j < len(sequence_table) - 1 :
                    air_sortie_table[code_element] = air_sortie_element
                    air_entree_table[sequence_table[j + 1]] = air_sortie_element
                #print(air_sortie_table[code_element])
            air_table = {}
        for k in sequence_table:           # Fusion de air_entree et air_sortie
            air_table[k] = (air_entree_table[k],air_sortie_table[k])
        if 5.2 in sequence_table :      # Permet de distinguer le cas où la power turbine n'alimente pas
                                        # le compresseur (Gas Generator : travail_extrait_turbine = 0)
            performance = Performance(compresseur, power_turbine, combustion,0)
        else :
            performance = Performance(compresseur, power_turbine, combustion, compresseur.travail)
        #print(compresseur.travail)
        #print(power_turbine.travail)
        #print(performance)
        return performance,air_table


def start():
    comparaison_on = 1
    try :
        simulation1 = Simulation(sequence1,parametrage1)
        affichage_console(simulation1, "Performances cycle Séquence 1")
    except :
        simulation1 = "Pas de Séquence 1"
        print(simulation1)
        comparaison_on = 0
    if comparaison_on == 1 :
        pause = input("Appuyer pour passer à l'affichage suivant")
    try :
        simulation2 = Simulation(sequence2,parametrage2)
        affichage_console(simulation2, "Performances cycle Séquence 2")
    except :
        simulation2 = "Pas de Séquence 2"
        print(simulation2)
        comparaison_on = 0
    if comparaison_on == 1:
        pause = input("Appuyer pour passer à l'affichage suivant")
    if comparaison_on == 1 :
        affichage_comparaison(simulation1,simulation2)
    return simulation1,simulation2