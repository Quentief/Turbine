########################### Import


import matplotlib.pyplot as plt
import numpy as np


########################### Affichage des résultats via la console


def affichage_console(simulation,sequence_table):
    indice = 0
    dash = "-" * 99
    for i in range(2) :
        print(dash)
        if indice == 0 :
            print("{:^50}".format("Performances sans EC : ".upper()))
        else :
            print("{:^50}".format("Performances avec EC : ".upper()))
        print('{:<30s}{:>10s}{:>20s}'.format("Composant", "Pression", "Température"))
        print(dash)
        for j in range(len(sequence_table)):
            code_element = sequence_table[j]
            if code_element == 1:
                element = "Compresseur"
            elif code_element == 2:
                element = "Chambre combustion"
            elif code_element == 3:
                element = "Turbine"
            elif code_element == 4.1 and indice == 1 :
                element = "EC - coté air frais"
            elif code_element == 4.2 and indice == 1 :
                element = "EC - coté gaz chauds"
            if indice == 0 and code_element not in [4.1,4.2]:
                print("{:<30s}{:>10.2f}{:>20.2f}".format(element, simulation.air_table_sans_EC[code_element][1].pression,
                                        simulation.air_table_sans_EC[code_element][1].temperature))
            elif indice == 1:
                print("{:<30s}{:>10.2f}{:>20.2f}".format(element, simulation.air_table_avec_EC[code_element][1].pression,
                                        simulation.air_table_avec_EC[code_element][1].temperature))
        print("")
        if indice == 0 :
            print(simulation.performance_sans_EC)
            indice = 1
        else :
            print(simulation.performance_avec_EC)


# def affichage_graphique(simulation):
#     labels = ["Sans EC","Avec EC"]
#     SWO = [simulation.performance_sans_EC.puissance_specifique_sortie,simulation.performance_avec_EC.puissance_specifique_sortie]
#     SFC = [simulation.performance_sans_EC.sfc*100,simulation.performance_avec_EC.sfc*100]
#     rendement = [simulation.performance_sans_EC.rendement*100,simulation.performance_avec_EC.rendement*100]
#
#     plt.figure(4)
#     plt.subplot(311)
#     data = [23, 45, 56, 78, 213]
#     plt.bar([1, 2, 3, 4, 5], data)
#     plt.subplot(212)
#     data = [23, 45, 56, 78, 213]
#     plt.bar([1, 2, 3, 4, 5], data)
#     plt.subplot(213)
#     data = [23, 45, 56, 78, 213]
#     plt.bar([1, 2, 3, 4, 5], data)
#     plt.show()