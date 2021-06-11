########################### Import

from colorama import Style, Fore

########################### Affichage des résultats via la console


def affichage_console(simulation):
    sequence_table = simulation.sequence
    dash = "-" * 99
    print(dash)
    print("{:^25}{:^5}".format("PERFORMANCES :",simulation.titre.upper()))
    print("")
    print('{:<31s}{:>13s}{:>27s}{:>27s}'.format("Composant", "Pression", "Température", "Travail"))
    print(dash)
    for j in range(len(sequence_table)):
        code_element = sequence_table[j]
        travail = ""
        if code_element == 1:
            element = "Compresseur"
            travail = simulation.travail[1]
        elif code_element == 2:
            element = "Chambre combustion"
        elif code_element == 3:
            element = "Power turbine"
            travail = simulation.travail[3]
        elif code_element == 4.1 :
            element = "Echangeur chaleur - air frais"
        elif code_element == 4.2 :
            element = "Echangeur chaleur - gaz chauds"
        elif code_element == 5.1 :
            element = "Gas generator - compresseur"
            travail = simulation.travail[5.1]
        elif code_element == 5.2 :
            element = "Gas generator - turbine"
            travail = simulation.travail[5.2]
        if travail == "" :
            print("{:<30s}{:>10.2f} bar {:>24.2f} K {:>20}".format( element, simulation.air_table[code_element][1].pression,
                                    simulation.air_table[code_element][1].temperature, travail ) )
        else :
            print("{:<30s}{:>10.2f} bar {:>24.2f} K {:>20.2f} kJ/kg".format( element, simulation.air_table[code_element][1].pression,
                                    simulation.air_table[code_element][1].temperature, travail ) )
    print("")
    print(simulation.performance)


def couleur(x):
    x = round(x,2)
    if x < 0:
        return Fore.RED + "Perte : " + str(x*100) + " %" + Style.RESET_ALL
    else:
        return Fore.GREEN + "Gain : " + str(x*100) + " %" + Style.RESET_ALL

def couleur2(x):
    x = round(x,2)
    if x > 0:
        return Fore.RED + "Perte : " + str(x*100) + " %" + Style.RESET_ALL
    else:
        return Fore.GREEN + "Gain : " + str(x*100) + " %" + Style.RESET_ALL



def affichage_comparaison(simulation1,titre1,simulation2,titre2):
    dash = "-" * 99
    print(dash)
    print("{}  {}  {}  {}".format("BILAN :",titre1.upper(),"PAR RAPPORT À",titre2.upper()))
    print(dash)
    SPO_compare = couleur( (simulation2.performance.puissance_specifique_sortie
            - simulation1.performance.puissance_specifique_sortie) / simulation1.performance.puissance_specifique_sortie )
    SFC_compare = couleur2( (simulation2.performance.sfc - simulation1.performance.sfc) / simulation1.performance.sfc )
    rendement_compare = couleur( (simulation2.performance.rendement
                         - simulation1.performance.rendement) / simulation1.performance.rendement )
    print("{:<31s}{:>10s}".format("Specific Power Output", SPO_compare))
    print("{:<31s}{:>10s}".format("Specific Fuel Consumption", SFC_compare))
    print("{:<31s}{:>10s}".format("Rendement", rendement_compare))