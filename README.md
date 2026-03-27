# TP Noté - Algorithmes génétiques

## Groupe

- Steve PENNEC, 4IRC
- Hanan M'HAMED, CLBD

---

## Compte-Rendu

## Algorithme génétique et méthodes utilisées

Nous utilisons un algorithme génétique pour résoudre le problème du voyageur de commerce (TSP).  
Le principe est de générer plusieurs solutions  et de les améliorer progressivement au fil des générations.

Chaque solution représente un ordre de visite des villes. L’algorithme sélectionne les meilleures solutions et les combine pour créer de nouvelles solutions.

Plusieurs méthodes sont utilisées :

- **Nearest Neighbor**: utilisée pour créer des solutions initiales assez bonnes rapidement en allant toujours vers la ville la plus proche.
- **Sélection par tournoi** : permet de choisir les meilleures solutions pour la reproduction tout en gardant un peu d’aléatoire.
- **Order Crossover** : utilisé pour combiner deux solutions et créer un nouvel individu tout en gardant un ordre valide des villes.
- **Mutation** : modifie légèrement une solution afin d’explorer de nouvelles possibilités.
- **2-opt** : méthode d’amélioration locale qui réduit la distance du tour en inversant certaines parties du chemin.

Ces méthodes permettent d’explorer différentes solutions et d’améliorer progressivement la distance totale du tour.


### Paramètrage globale par défaut

* `time_budget=60`:
Temps maximal (en secondes) alloué à l'algorithme pour trouver la solution. L'algorithme s'arrête après 60 secondes, même s'il pourrait continuer.

* `pop_size=150`:
Nombre d'individus (tours) maintenus dans la population à chaque génération. Plus grand = plus d'exploration mais plus lent par génération.

* `mutation_rate=0.15`:
Probabilité (15%) qu'un enfant subisse une mutation. Plus élevé = plus d'exploration mais moins de stabilité des bonnes solutions.

* `elite_ratio=0.1`:
Fraction (10%) des meilleurs individus conservés directement sans modification dans la génération suivante. Garantit que les bonnes solutions ne disparaissent pas.

* `tournament_k=5`:
Nombre d'individus sélectionnés aléatoirement dans le tournoi de sélection. Plus grand = sélection plus stricte (favorise les meilleurs), plus petit = plus de diversité.

* `MAX_NO_IMPROVE=3000`:
Nombre maximum de générations sans amélioration avant d'arrêter l'algorithme. Évite de perdre du time_budget si on stagne (convergence prématurée).

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

Score obtenu : 6491.49

Avec le paramètrage suivant :

* time_budget: 120
* pop_size = 100

Pour celui-là, il fallait trouver un bon équilibre entre le ratio exploitation et exploration.

Gen   20 | Meilleure dist : 6537.00 km | Temps écoulé : 1.3s
Gen   40 | Meilleure dist : 6517.63 km | Temps écoulé : 2.6s
Gen   60 | Meilleure dist : 6517.63 km | Temps écoulé : 3.9s
Gen   80 | Meilleure dist : 6509.54 km | Temps écoulé : 5.1s
...
Gen  320 | Meilleure dist : 6509.54 km | Temps écoulé : 19.7s
Gen  340 | Meilleure dist : 6491.61 km | Temps écoulé : 20.9s

On observe alors que la solution optimale a été trouvé après 20 secondes pour un génération d'une population de 340 individus.

En essayant d'augmenter l'exploitation avec un `pop_size=200`, j'ai réussi à avoir l'optimum plus rapidement :
Gen   20 | Meilleure dist : 6539.59 km | Temps �coul� : 2.4s
Gen   40 | Meilleure dist : 6491.61 km | Temps �coul� : 4.8s

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

Score obtenu : 6491.49

Avec le paramètrage suivant :

* time_budget: 20
* pop_size = 80

En phase d'essai, avec le paramètrage suivant pour un ratio d'exploitation et d'exploration pas assez élevé :
- "time_budget": 10
- "pop_size": 30

Nous avons obtenu :

  Gen  100 | Meilleure dist : 8260.61 km | Temps �coul� : 8.5s

Cela montre une exploitation très rapide avec pas assez d'exploration. On augmente alors le `pop_size` à 80 pour avoir une meilleure qualité, sans être trop coûteux sachant que cette instance possède 200 villes.

Gen   20 | Meilleure dist : 8204.85 km | Temps �coul� : 4.7s
Gen   40 | Meilleure dist : 8202.83 km | Temps �coul� : 9.3s
Gen   60 | Meilleure dist : 8202.83 km | Temps �coul� : 13.8s
Gen   80 | Meilleure dist : 8169.03 km | Temps �coul� : 18.4s

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

Score obtenu : 1944.32

* time_budget: 300
* pop_size: 80

Nous avons commencé nos essais avec un paramètre de `pop_size` allant de 10 à 100, où notre score s'améliorer au fur et à mesure que nous augmentant `pop_size` allant de 200 à 1940.

Cependant, nous avons constaté une saturation où on passant `pop_size` de 80 à 100, l'algorithme fut plus couteuse et a mis 300 secondes (du coup le `time_budget`) pour se finir et obtenir un de score 1952.70 km, n'étant pas meilleur que celle obtenu initialement avec une population de 80.

### Clusters hiérarchiques - L'archipel des damnés (2 000 villes)


