########################### Import

from Model.model2 import proprietes_air, gamma_table, cp_table, far_bornes1A_temperature, far_bornes1B_temperature, \
    far_bornes1A_far, far_bornes1B_far, far_bornes2A_temperature, far_bornes2B_temperature, far_bornes2A_far, \
    far_bornes2B_far, cycle1, cycle2

from ViewController.view2 import affichage_console, affichage_comparaison

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
    def __init__(self, air_entree, r, NM, NI, NP, cp, gamma):
        self.air_entree = air_entree
        self.air_sortie = Air(r * self.air_entree.pression,
                              self.calcul_temperature_sortie(air_entree, gamma, r, NI, NP))
        self.travail = self.calcul_travail(cp, air_entree.temperature, self.air_sortie.temperature, NM)
    def calcul_temperature_sortie(self, air_entree, gamma, r, NI, NP):
        Ta = air_entree.temperature
        if NP == 0 :
            return Ta + Ta/NI * ( r**( (gamma - 1)/gamma) - 1)
        else :
            return Ta*r**( (gamma-1)/(gamma*NP) )
    def calcul_travail(self, cp, Ta, T2, NM):
        return cp*(T2 - Ta)/NM


class Combustion:
    def __init__(self, air_entree, NB, TB, dP):
        self.air_entree = air_entree
        self.air_sortie = Air(air_entree.pression - dP, TB)
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
    def __init__(self, air_entree, pression_sortie, NM, NI, NP, dP, cp, gamma):
        self.air_entree = air_entree
        self.air_sortie = self.calcul_air_sortie(air_entree, pression_sortie, gamma, NI, NP, dP)
        self.travail = self.calcul_travail(air_entree, self.air_sortie.temperature, NM, cp)
        self.dP = dP
    def calcul_air_sortie(self, air_entree, P4, gamma, NI, NP, dP):
        T3 = air_entree.temperature
        P3 = air_entree.pression
        if NP == 0 :
            T4 = T3 * (1 - NI * (1 - ((P4 + dP) / P3) ** ((gamma - 1) / gamma)))
            return Air(P4,T4)
        else :
            return T3*(P4/P3)**( NP*(gamma-1)/gamma )
    def calcul_travail(self, air_entree, T4, NM, cp):
        T3 = air_entree.temperature
        return cp*(T3 - T4)*NM


class Gas_generator_turbine :
    def __init__(self, air_entree, travail, NI, NP, cp, gamma) :
        self.air_entree = air_entree
        self.travail = travail
        self.air_sortie = self.calcul_air_sortie(air_entree, travail, NI, NP, cp, gamma)
    def calcul_air_sortie(self, air_entree, travail, NI, NP, cp, gamma):
        T3 = air_entree.temperature
        T4 = T3 - travail/cp
        if NP == 0 :
            P4 = air_entree.pression*( 1 - (T3-T4)/(NI*T3) )**( gamma / (gamma -1) )
        return Air(P4,T4)


class Echangeur_chaleur :
    def __init__(self, air_entree, NE, dP, temperature_gaz_entree, pression_gaz_sortie):
        self.air_entree = air_entree
        self.air_sortie = self.calcul_air_sortie(self.air_entree.temperature, temperature_gaz_entree, dP, NE, self.air_entree)
        self.gaz_entree = self.calcul_gaz_entree(pression_gaz_sortie, dP, temperature_gaz_entree)
    def calcul_air_sortie(self, T2, T4, dP, NE, air_entree):
        T5 = NE * (T4 - T2) + T2
        P5 = air_entree.pression - dP
        return Air(P5, T5)
    def calcul_gaz_entree(self, pression_gaz_sortie, dP, temperature_gaz_entree):
        P4 = pression_gaz_sortie + dP
        T4 = temperature_gaz_entree
        return Air(P4,T4)


########################### Auto-programmation de la séquence


class Simulation :
    def __init__(self, cycle):
        self.cycle = cycle
        self.elements_table = self.auto_sequence(cycle)
        SWO,SFC,rendement = self.calcul_performance(self.elements_table,cycle)
        self.SWO = SWO
        self.SFC = SFC
        self.rendement = rendement
    def __str__(self):
        return "Specific Power Output : {:.2f} kJ/kg | Specific Fuel Consumption {:.2f} kg/kWh " \
               "| Efficiency : {:.2f} % ".format(self.SWO,self.SFC,self.rendement*100)
    def auto_sequence(self, cycle) :
        elements_table = {i: [ Air(cycle.air_exterieur_table[0], cycle.air_exterieur_table[1]),
                               Air(cycle.air_exterieur_table[0], cycle.air_exterieur_table[1]) ] for i in cycle.sequence.keys()}
        liens_table = {}
        for j in range(100) :
            transfert_selon_lien = {}
            for nom in cycle.sequence.keys() :
                #print(j,nom)
                parametrage = cycle.parametrage[nom]
                air_entree, air_sortie = elements_table[nom][0], elements_table[nom][1]
                try :
                    code,lien = cycle.sequence[nom].split(",")
                except :
                    code = cycle.sequence[nom]
                if j == 0 :
                    cp = air_entree.cp
                    gamma = air_entree.gamma
                else :
                    cp = (air_entree.cp + air_sortie.cp) / 2
                    gamma = (air_entree.gamma + air_sortie.gamma) / 2
                if nom != list(cycle.sequence.keys())[-1] :  # Pertes de charges
                    dP = air_entree.pression*parametrage[6]
                else :
                    dP = parametrage[7]
                if code == "C" or code == "GGC":
                    element = Compresseur(air_entree, parametrage[0], parametrage[1], parametrage[3], parametrage[4], cp, gamma)
                    elements_table[nom] = [air_entree, element.air_sortie, -element.travail]
                    caracteristique = -element.travail
                elif code == "B" :
                    element = Combustion(air_entree, parametrage[2], parametrage[5], dP)
                    elements_table[nom] = [air_entree, element.air_sortie, element.far]
                    caracteristique = element.far
                    lien = code
                elif code == "T" :
                    element = Power_turbine(air_entree, air_sortie.pression, parametrage[1], parametrage[3],
                                                  parametrage[4], dP, cp, gamma)
                    elements_table[nom] = [air_entree, element.air_sortie, element.travail]
                    caracteristique = element.travail
                elif "EC" in code :
                    if j == 0 :
                        air_sortie = air_entree
                        caracteristique = 0
                    else :
                        element = Echangeur_chaleur(air_entree, parametrage[2], dP, air_entree.temperature, air_sortie.pression)
                        if code == "ECA" :
                            air_sortie = element.air_sortie
                            caracteristique = element.air_entree
                        elif code == "ECG":
                            air_sortie = transfert_selon_lien[lien]
                            caracteristique = 0
                    elements_table[nom] = [air_entree, air_sortie]
                elif code == "GGT" :
                    element = Gas_generator_turbine(air_entree, -transfert_selon_lien[lien], parametrage[3],
                                                                  parametrage[4], cp, gamma)
                    elements_table[nom] = [air_entree, element.air_sortie, element.travail]
                    caracteristique = 0
                try :
                    transfert_selon_lien[lien] += caracteristique
                except :
                    transfert_selon_lien[lien] = caracteristique
                #print(transfert_selon_lien)
                #print(elements_table)
                index = list(cycle.sequence.keys()).index(nom)
                if index < len(cycle.sequence) - 1 :
                    elements_table[list(cycle.sequence.keys())[index + 1]][0] = elements_table[list(cycle.sequence.keys())[index]][1]
        return elements_table
    def calcul_performance(selfself, elements_table, cycle) :
        SWO = 0
        FAR = 0
        for nom in elements_table :
            try :
                code,lien = cycle.sequence[nom].split(",")
            except :
                code = cycle.sequence[nom]
            if "C" == code or "T" == code or "GG" in code :
                SWO += elements_table[nom][2]
            elif "B" == cycle.sequence[nom] :
                FAR += elements_table[nom][2]
        SFC = 3600*FAR/SWO
        rendement = 3600 / (SFC * 43100)
        return SWO,SFC,rendement

def start():
    comparaison_on = 1
    try :
        simulation1 = Simulation(sequence1,parametrage1,sequence_nom[0])
        affichage_console(simulation1)
    except :
        simulation1 = "Pas de Séquence 1"
        print(simulation1)
        comparaison_on = 0
    if comparaison_on == 1 :
        pause = input("Appuyer pour passer à l'affichage suivant")
    try :
        simulation2 = Simulation(sequence2,parametrage2,sequence_nom[1])
        affichage_console(simulation2)
    except :
        simulation2 = "Pas de Séquence 2"
        print(simulation2)
        comparaison_on = 0
    if comparaison_on == 1:
        pause = input("Appuyer pour passer à l'affichage suivant")
    if comparaison_on == 1 :
        affichage_comparaison(simulation1,sequence_nom[0],simulation2,sequence_nom[1])
    return simulation1,simulation2