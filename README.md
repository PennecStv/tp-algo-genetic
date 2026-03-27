# TP Noté - Algorithmes génétiques

## Groupe

- Steve PENNEC, 4IRC
- Hanan M'HAMED, CLBD

---

## Compte-Rendu

### Paramètrage globale par défaut

* time_budget=60
* pop_size=150
* mutation_rate=0.15
* elite_ratio=0.1
* tournament_k=5

### Tiny - Tour de France des régions

Score obtenu : 3235.49

Avec le paramètrage suivant :

* time_budget: 30
* pop_size = 100

En essayant de varier le taux d'exploitation et d'exploration en augmentant les valeurs de `time_budget` et `pop_size`, on retombe toujours sur le même score. On suppose que c'est la solution la plus optimale trouvable pour cette instance.

Cette instance possédant un nombre très peu de ville. Il est facile de pour notre algorithme génétique pour trouver sa solution la plus optimale.

### Small - Livraison Express
Score obtenu : 4117.70

Avec le paramétrage suivant :
time_budget = 60
pop_size = 150
mutation_rate = 0.15
elite_ratio = 0.1
tournament_k = 5

Nous avons effectué plusieurs exécutions de l’algorithme en faisant varier le nombre de générations ainsi que le temps d’exécution.
Dans tous les cas l’algorithme converge vers une solution de distance 4117.70 km sans amélioration supplémentaire, même en augmentant fortement le nombre de générations (jusqu’à 500).

Ce comportement indique que l’algorithme atteint rapidement un optimum local stable, voire l’optimum global pour cette instance.

L’algorithme génétique utilisé est très efficace pour cette instance de taille moyenne.
Le fait d’obtenir systématiquement le même résultat montre une bonne stabilité de l’algorithme et suggère que la solution trouvée est proche de l’optimum.



### Medium - Tournée des préfectures



### Hard - Road Trip improvisé
Score obtenu : 5904.89

Avec le paramétrage suivant :
time_budget = 120
pop_size = 100
mutation_rate = 0.15
elite_ratio = 0.1
tournament_k = 5

En faisant varier les paramètres (time_budget, pop_size, mutation_rate), on observe que l’algorithme produit des solutions légèrement différentes à chaque exécution, avec des distances comprises entre 5928 km et 5904 km.

Cependant, malgré ces variations l’algorithme converge très souvent vers une valeur proche de 5900 km, ce qui suggère la présence d’un optimum local de bonne qualité.

L’augmentation du temps d’exécution permet parfois d’obtenir de meilleures solutions (jusqu’à 5928 km à 5904 km), mais les améliorations deviennent rapidement limitées.

Cette instance étant plus complexe (100 villes) l’algorithme nécessite plus de générations pour converger, mais reste efficace grâce à l’optimisation locale qui améliore significativement les solutions.



### Extreme - Le facteur est fou



### Nightmare - Cauchemar du livreur
Score obtenu : 12950.63
Avec le paramétrage suivant :
* time_budget = 300
* pop_size = 50
* mutation_rate = 0.15
* elite_ratio = 0.1
* tournament_k = 5

Cette instance contient 500 villes et représente un problème beaucoup plus complexe que les instances précédentes.  
La taille importante de l’espace de recherche rend impossible l’exploration exhaustive des solutions, ce qui nécessite l’utilisation d’heuristiques efficaces.

Lors de plusieurs exécutions de l’algorithme, les distances obtenues varient généralement entre 12950 km et 13400 km.  
La meilleure solution trouvée au cours de nos tests est 12950.63 km, ce qui nous a permis d’atteindre la première place du classement pour cette instance.

On observe également que l’algorithme génétique améliore peu la solution après l’initialisation de la population. En effet, la phase d’initialisation utilisant l’heuristique Nearest Neighbor, combinée à une optimisation locale 2-opt, produit déjà des solutions de bonne qualité.

Le processus génétique (croisement, mutation et sélection) permet néanmoins d’explorer différentes régions de l’espace de recherche et d’obtenir parfois des solutions légèrement meilleures selon l’initialisation aléatoire.





### Clusters en anneau - La ronde infernale (600 villes)



### Grille régulière - Le damier maudit (625 villes)



### Cercles concentriques - Les anneaxu de feu (800 villes)



### Étoile alternée - Le soleil noir (1 000 villes)



### Double spirale - La galaxie de Hubble (1 400 villes)



### Clusters hiérarchiques - L'archipel des damnés (2 000 villes)


