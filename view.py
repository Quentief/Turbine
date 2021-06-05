########################### Import

from colorama import Style, Fore

########################### Affichage des résultats via la console


def affichage_console(simulation,sequence_table,titre_sequence):
    dash = "-" * 99
    print(dash)
    print("{:^50}".format(titre_sequence.upper()))
    print("")
    print('{:<31s}{:>13s}{:>27s}{:>27s}'.format("Composant", "Pression", "Température", "Travail"))
    print(dash)
    for j in range(len(sequence_table)):
        code_element = sequence_table[j]
        travail = ""
        if code_element == 1:
            element = "Compresseur"
            travail = -simulation.performance.travail_compresseur
        elif code_element == 2:
            element = "Chambre combustion"
        elif code_element == 3:
            element = "Power turbine"
            travail = simulation.performance.travail_turbine
        elif code_element == 4.1 :
            element = "EC - coté air frais"
        elif code_element == 4.2 :
            element = "EC - coté gaz chauds"
        elif code_element == 5.1 :
            element = "GG - compresseur"
            travail = -simulation.performance.travail_compresseur
        elif code_element == 5.2 :
            element = "GG - turbine"
            travail = simulation.performance.travail_compresseur
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



def affichage_comparaison(simulation1,simulation2):
    dash = "-" * 99
    print(dash)
    print("{:^50}".format("Bilan".upper()))
    print(dash)
    SPO_compare = couleur( (simulation2.performance.puissance_specifique_sortie
            - simulation1.performance.puissance_specifique_sortie) / simulation1.performance.puissance_specifique_sortie )
    SFC_compare = couleur2( (simulation2.performance.sfc - simulation1.performance.sfc) / simulation1.performance.sfc )
    rendement_compare = couleur( (simulation2.performance.rendement
                         - simulation1.performance.rendement) / simulation1.performance.rendement )
    print("{:<31s}{:>10s}".format("Specific Power Output", SPO_compare))
    print("{:<31s}{:>10s}".format("Specific Fuel Consumption", SFC_compare))
    print("{:<31s}{:>10s}".format("Rendement", rendement_compare))