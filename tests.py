# ###########################  Tests avec exemple 2.1 page 74
#
# air_entree = Air(1,288)
# compresseur = Compresseur(air_entree,4,0.85,0.99)
# print(compresseur.air_sortie.pression)      # OK
# print(compresseur.air_sortie.temperature)   # OK
#
# air_entree = Air(4*(1-0.03),758.7)
# combustion = Combustion(air_entree, 0.02, 1100, 0.98)
# print(combustion.air_sortie.pression)       # OK
# print(combustion.air_sortie.temperature)    # OK
#
# air_entree = Air(3.8,1100)
# turbine = Turbine(air_entree,1.04,0.87)
# print(turbine.air_sortie.temperature)       # OK
# print(turbine.travail)                      # OK
#
# air_entree = Air(4,452.7)
# gaz_entree = Air(1.04,835.2)
# echangeur = Echangeur_chaleur(air_entree,0.80,0.03,0.04,835.2,1)
# print(echangeur.air_sortie.temperature)     # OK
# print(echangeur.air_sortie.pression)        # OK (car pertes de charges chambre combustion prise en compte dans Combustion)
# print(echangeur.gaz_entree.temperature)     # OK
# print(echangeur.gaz_entree.pression)        # OK
#
# performance = Performance(compresseur,turbine,combustion)
# print(performance.sfc)                      # OK
# print(performance.rendement)                # OK
#
########################### 1ere boucle sans Échamgeur de chaleur
air_entree = Air(1,288)
compresseur = Compresseur(air_entree,4,0.85,0.99)
air_entree = compresseur.air_sortie     # Pression : 4.00 bars | Temperature 452.84 K
combustion = Combustion(air_entree, 0.02, 1100, 0.98)
air_entree = combustion.air_sortie       # Pression : 3.92 bars | Temperature 1100.00 K
turbine = Turbine(air_entree,1,0.87)     # Pression : 1.00 bars | Temperature 825.40 K
performance1 = Performance(compresseur,turbine,combustion)      # Specific power output : 151.00 kJ/kg | SFC 0.43 kg/kWh | Rendement global : 19.63 %
print(performance1)

########################### 2eme boucle avec Échangeur de chaleur
air_entree = compresseur.air_sortie
gaz_entree = turbine.gaz_sortie
echangeur = Echangeur_chaleur(air_entree, 0.80, 0.03, 0.04, turbine.gaz_sortie.temperature, 1)
air_entree = echangeur.air_sortie
combustion = Combustion(air_entree, 0.02, 1100, 0.98)
air_entree = combustion.air_sortie
turbine = Turbine(air_entree,echangeur.gaz_entree.pression,0.87)
performance = Performance(compresseur,turbine,combustion)
print(performance)


for i in range(len(sequence_table_sans_EC)):
    code_element = sequence_table_sans_EC[i]
    print(air_entree_table[code_element])

for i in range(len(sequence_table_sans_EC)):
    code_element = sequence_table_sans_EC[i]
    print(air_sortie_table[code_element])