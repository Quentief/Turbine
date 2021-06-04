########################### Import


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
        print('{:<31s}{:>13s}{:>23s}'.format("Composant", "Pression", "Température"))
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
                print("{:<30s}{:>10.2f} bar {:>20.2f} K".format(element, simulation.air_table_sans_EC[code_element][1].pression,
                                        simulation.air_table_sans_EC[code_element][1].temperature))
            elif indice == 1:
                print("{:<30s}{:>10.2f} bar {:>20.2f} K".format(element, simulation.air_table_avec_EC[code_element][1].pression,
                                        simulation.air_table_avec_EC[code_element][1].temperature))
        print("")
        if indice == 0 :
            print(simulation.performance_sans_EC)
            indice = 1
        else :
            print(simulation.performance_avec_EC)