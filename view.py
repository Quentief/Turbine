########################### Import

import pandas as pd

########################### Paramètres à renseigner (méthode input) :

# ## Conditions ambiantes
# Ta = float(input("Température ambiante (Kelvin) "))
# Pa = float(input("Pression ambiante (bar) "))
# ## Chambre combustion et compresseur
# r = float(input("Ratio compression "))
# TB = float(input("Température chambre combustion (Kelvin) "))
# ## Rendements composants
# NC = float(input("Rendement isentropique interne compresseur "))
# NT = float(input("Rendement isentropique interne turibne "))
# NM = float(input("Rendement mécanique "))
# NB = float(input("Rendement combustion "))
# NE = float(input("Rendement échangeur chaleur "))
# ## Pertes de pression
# dPB = float(input("Pertes de charges chambre combustion "))
# dPEa = float(input("Pertes de charges échangeur chaleur, côté air frais "))
# dPEg = float(input("Pertes de charges échangeur chaleur, côté air gaz chauds "))

interface_xl = 'Interface.xlsx'
user = pd.read_excel(interface_xl, sheet_name="user")

sequence_table = user["Séquence"].tolist()
sequence_table = [x for x in sequence_table if pd.isnull(x) == False]      # Supprimer les nan de la liste

python = pd.read_excel(interface_xl, sheet_name="python")

air_exterieur_table = python["Air exterieur"].tolist()
air_exterieur_table = [x for x in air_exterieur_table if pd.isnull(x) == False]

compresseur_table = python["Compresseur"].tolist()
compresseur_table = [x for x in compresseur_table if pd.isnull(x) == False]

combustion_table = python["Chambre de combustion"].tolist()
combustion_table = [x for x in combustion_table if pd.isnull(x) == False]

turbine_table = python["Turbine"].tolist()
turbine_table = [x for x in turbine_table if pd.isnull(x) == False]

echangeur_table = python["Échangeur de chaleur"].tolist()
echangeur_table = [x for x in echangeur_table if pd.isnull(x) == False]

########################### Paramètres extraits de l'interface XL :
# ## Conditions ambiantes
# Pa = float(air_exterieur_table[0])
# Ta = float(air_exterieur_table[1])
# ## Chambre combustion et compresseur
# r = float(compresseur_table[0])
# TB = float(combustion_table[0])
# ## Rendements composants
# NC = float(compresseur_table[2])
# NT = float(turbine_table[0])
# NM = float(compresseur_table[1])
# NB = float(combustion_table[1])
# NE = float(echangeur_table[0])
# ## Pertes de pression
# dPB = float(combustion_table[2])
# dPEa = float(echangeur_table[1])
# dPEg = float(echangeur_table[2])