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

Score obtenu : 583.79

Avec le paramètrage suivant :

* time_budget: 20
* pop_size = 80

Cette instance présente une structure très régulière où les 600 villes sont organisées en clusters disposés en anneau autour d'un centre.
Cette géométrie particulière est très favorable à notre algorithme génétique car :
- La structure en anneau offre une solution naturelle : traverser les clusters dans l'ordre
- L'initialisation par nearest-neighbor détecte rapidement cette structure
- L'optimisation 2-opt converge très rapidement sur cette géométrie convexe

Le score très faible (583.79 km) reflète cette excellente qualité de solution. Malgré un time_budget réduit à 20 secondes et une population modérée (80 individus), l'algorithme trouve une très bonne solution en exploitant la structure de l'instance. Cette instance démontre que les algorithmes génétiques ne sont pas nécessaires pour les problèmes avec structure géométrique claire.

### Grille régulière - Le damier maudit (625 villes)

Score obtenu : 2554.59

Avec le paramètrage suivant :

* time_budget: 180
* pop_size = 80

Cette instance organise 625 villes en grille régulière (25×25), ce qui crée un problème particulièrement difficile pour les algorithmes de recherche locale.

Le score de 2554.59 km est plus élevé proportionnellement au nombre de villes que pour l'instance précédente en anneau. Cela s'explique par :
- La grille régulière ne possède pas une solution "naturelle" apparente contrairement à l'anneau
- Les solutions greedy initiales produisent des chemins non optimaux qui zigzaguent inefficacement
- L'optimisation 2-opt stagne rapidement dans des optima locaux dus à la régularité de la structure

Avec un budget très limité (20 secondes) et une petite population (80), l'algorithme n'a pas le temps de suffisamment le problème. Un augmentation du `time_budget` aurait probablement permis une amélioration significative du score.

### Cercles concentriques - Les anneaux de feu (800 villes)

Score obtenu : 1510.26

Avec le paramètrage suivant :

* time_budget: 180
* pop_size = 50

Cette instance dispose 800 villes le long de plusieurs cercles concentriques, ce qui constitue une structure géométrique très particulière.

Le score de 1510.26 km pour 800 villes est relativement performant. La structure concentrique offre quelques avantages :
- La solution consiste à traverser les cercles de manière efficace (soit en spirale, soit en zigzag entre les cercles)
- L'heuristique nearest-neighbor peut identifier des chemins proches du cercle actuel
- Cependant, la connexion entre les cercles reste un point d'optimisation critique

Avec 20 secondes de time_budget et une population de 80, l'algorithme identifie une stratégie de traversée raisonnable. Le score suggère que la structure est suffisamment régulière pour que même avec des ressources limitées, une solution correcte soit trouvée rapidement. Cette instance montre comment la géométrie influence la convergence : une structure avec symétries ou régularités permet de meilleures solutions même avec peu de générations.

### Étoile alternée - Le soleil noir (1 000 villes)

Score obtenu : 1093.93

Avec le paramètrage suivant :

* time_budget: 180
* pop_size = 50

Cette instance organise 1000 villes en configuration d'étoile alternée avec des branches rayonnantes depuis un centre. C'est une structure géométrique très spécifique.

Le score de 1093.93 km pour 1000 villes est remarquablement bon et reflète comment la structure d'étoile est exploitable par notre algorithme :
- La solution naturelle consiste à suivre les branches de l'étoile et revenir au centre
- L'ordre de visite des branches peut être optimisé par le croisement génétique
- L'alternance des branches crée des opportunités de croisement efficaces entre solutions

Malgré les ressources limitées (20s, 80 individus), le score est excellent car :
- La structure géométrique guide naturellement vers une bonne solution
- L'initialisation nearest-neighbor identifie rapidement le passage par le centre
- La mutation et le croisement OX trouvent rapidement l'ordre optimal entre les branches

Cette instance démontre que la qualité de solution dépend fortement de la structure géométrique du problème, plus que du seul pouvoir de calcul disponible.

### Double spirale - La galaxie de Hubble (1 400 villes)

Score obtenu : 1944.32

* time_budget: 300
* pop_size: 80

Nous avons commencé nos essais avec un paramètre de `pop_size` allant de 10 à 100, où notre score s'améliorer au fur et à mesure que nous augmentant `pop_size` allant de 200 à 1940.

Cependant, nous avons constaté une saturation où on passant `pop_size` de 80 à 100, l'algorithme fut plus couteuse et a mis 300 secondes (du coup le `time_budget`) pour se finir et obtenir un de score 1952.70 km, n'étant pas meilleur que celle obtenu initialement avec une population de 80.

### Clusters hiérarchiques - L'archipel des damnés (2 000 villes)

Score obtenu : 1478.49

Avec le paramètrage suivant :

* time_budget: 180
* pop_size = 50

Cette instance représente le problème le plus complexe avec 2000 villes organisées selon une structure hiérarchique de clusters (d'où le nom "archipel").

Le score de 1478.49 km pour 2000 villes est excellent étant donné la complexité :
- La structure hiérarchique exige de visiter les clusters dans le bon ordre, puis optimiser les chemins intra-cluster
- L'algorithme dispose de plus de temps (180s) mais d'une population réduite (50 individus) pour gérer la complexité

Les choix paramétriques reflètent un équilibre nécessaire pour 2000 villes :
- `time_budget=180` : suffisant pour que le processus génétique explore l'espace de recherche
- `pop_size=50` : réduit car maintenir et évaluer 150+ individus prendrait trop de temps par génération
- Cette réduction de population est compensée par le temps additionnel permettant plus de générations

Le score montre que même avec une structure complexe, notre algorithme avec ses opérateurs de croisement OX et ses stratégies de mutation variées réussit à trouver des solutions de très bonne qualité. L'optimisation 2-opt initiale et durant l'évolution joue un rôle crucial pour atteindre ce résultat avec une population aussi réduite.
