import sys

reconnexion = 15
freq_commerce = 30
troops_cities = [] # nom des villes où on veut recruter des troupes, à indiquer aussi dans non_farm_cities pour éviter les conflits
non_farm_cities = ["exemple"] # nom des villes où on ne veut PAS récupérer des ressources
building_queue = {"44 01 Feurst" : ["académie", "entrepôt"], "44 02 Song" : ["sénat","ferme","académie"]} # "ville" : "data_building_id"

# Les temps sont à donner en minutes

# Généralement, il est plus efficace d'abaisser la valeur de freq_commerce si on a peu de villes, car cela permet de lancer
# les constructions à une fréquence plus élevée. En revanche au delà d'un certain seuil, si cette valeur est trop faible, certaines
# ressources des paysans ne sont pas récupérées. C'est à l'utilisateur d'adapter les valeurs à ses besoins.

# Id des batiments : académie, port, sénat, ferme, remparts, entrepôt
