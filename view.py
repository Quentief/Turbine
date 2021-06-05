########################### Import


########################### Affichage des résultats via la console


def affichage_console(simulation,sequence_table,titre_sequence):
    indice = 0
    dash = "-" * 99
    print(dash)
    print("{:^50}".format(titre_sequence.upper()))
    print("")
    print('{:<31s}{:>13s}{:>23s}'.format("Composant", "Pression", "Température"))
    print(dash)
    for j in range(len(sequence_table)):
        code_element = sequence_table[j]
        if code_element == 1:
            element = "Compresseur"
        elif code_element == 2:
            element = "Chambre combustion"
        elif code_element == 3:
            element = "Power turbine"
        elif code_element == 4.1 :
            element = "EC - coté air frais"
        elif code_element == 4.2 :
            element = "EC - coté gaz chauds"
        elif code_element == 5.1 :
            element = "GG - compresseur"
        elif code_element == 5.2 :
            element = "GG - turbine"
        print("{:<30s}{:>10.2f} bar {:>20.2f} K".format(element, simulation.air_table[code_element][1].pression,
                                    simulation.air_table[code_element][1].temperature))
        # elif indice == 1:
        #     print("{:<30s}{:>10.2f} bar {:>20.2f} K".format(element, simulation.air_table_avec_EC[code_element][1].pression,
        #                             simulation.air_table_avec_EC[code_element][1].temperature))
    print("")
    print(simulation.performance)