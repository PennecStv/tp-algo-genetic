"""
TP Noté — Algorithmes Génétiques — TSP
CPE Lyon 4IRC — Mars 2026
"""

import math
import random
import time
import requests

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_URL = "https://tsp-sra0.onrender.com"
STUDENT_ID = "steve_hanan"

MAX_NO_IMPROVE =3000  # générations sans amélioration avant d'arrêter la boucle génétique

# =============================================================================
# API CLIENT
# =============================================================================

def list_instances():
    """GET /instances — liste toutes les instances disponibles."""
    r = requests.get(f"{BASE_URL}/instances")
    r.raise_for_status()
    return r.json()


def get_instance(instance_id):
    """GET /instances/{instance_id} — récupère les villes d'une instance."""
    r = requests.get(f"{BASE_URL}/instances/{instance_id}")
    r.raise_for_status()
    return r.json()  # {"instance_id", "name", "cities": [[lon, lat], ...]}


def submit_solution(instance_id, tour):
    """POST /submit — soumet une solution et retourne la réponse du serveur."""
    payload = {
        "student_id": STUDENT_ID,
        "instance_id": instance_id,
        "tour": tour,
    }
    r = requests.post(f"{BASE_URL}/submit", json=payload)
    if r.status_code == 200:
        return r.json()
    else:
        print(f"  [ERREUR] {r.status_code}: {r.json()}")
        return None

# =============================================================================
# DISTANCE
# =============================================================================

def haversine(city_a, city_b):
    """Distance en km entre deux villes [lon, lat] via la formule de Haversine."""
    R = 6371.0
    lon_a, lat_a = math.radians(city_a[0]), math.radians(city_a[1])
    lon_b, lat_b = math.radians(city_b[0]), math.radians(city_b[1])
    dlat = lat_b - lat_a
    dlon = lon_b - lon_a
    a = math.sin(dlat / 2) ** 2 + math.cos(lat_a) * math.cos(lat_b) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def build_distance_matrix(cities):
    """Pré-calcule toutes les distances entre villes."""
    n = len(cities)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = haversine(cities[i], cities[j])
            dist[i][j] = d
            dist[j][i] = d
    return dist


def tour_distance(tour, dist):
    """Distance totale d'un tour (cycle complet)."""
    total = 0.0
    n = len(tour)
    for i in range(n):
        total += dist[tour[i]][tour[(i + 1) % n]]
    return total

# =============================================================================
# INITIALISATION DE LA POPULATION
# =============================================================================

def nearest_neighbor_tour(start, dist, n):
    """Construit un tour greedy nearest-neighbor depuis 'start'."""
    visited = [False] * n
    tour = [start]
    visited[start] = True
    for _ in range(n - 1):
        current = tour[-1]
        best_next = -1
        best_d = float("inf")
        for j in range(n):
            if not visited[j] and dist[current][j] < best_d:
                best_d = dist[current][j]
                best_next = j
        tour.append(best_next)
        visited[best_next] = True
    return tour


def init_population(pop_size, n, dist):
    """
    Initialise la population avec :
    - quelques tours greedy (nearest-neighbor depuis des départs aléatoires)
    - le reste aléatoire
    """
    population = []
    # Tours greedy (25% de la population)
    n_greedy = max(1, pop_size // 4)
    starts = random.sample(range(n), min(n_greedy, n))
    for s in starts:
        population.append(nearest_neighbor_tour(s, dist, n))

    # Tours aléatoires pour le reste
    base = list(range(n))
    while len(population) < pop_size:
        t = base[:]
        random.shuffle(t)
        population.append(t)

    return population

# =============================================================================
# SÉLECTION
# =============================================================================

def tournament_selection(population, fitnesses, k=5):
    """
    Sélection par tournoi de taille k.
    Retourne l'indice du gagnant (meilleure fitness = distance minimale).
    """
    contestants = random.sample(range(len(population)), k)
    winner = min(contestants, key=lambda i: fitnesses[i])
    return population[winner]

# =============================================================================
# CROISEMENT (Order Crossover — OX)
# =============================================================================

def order_crossover(parent1, parent2):
    """
    OX (Order Crossover) : préserve l'ordre relatif des villes de parent2
    pour les positions non couvertes par le segment de parent1.
    Garantit une permutation valide.
    """
    n = len(parent1)
    a, b = sorted(random.sample(range(n), 2))

    child = [-1] * n
    # Copie le segment de parent1
    child[a:b + 1] = parent1[a:b + 1]
    segment_set = set(child[a:b + 1])

    # Remplit les positions restantes dans l'ordre de parent2
    pos = (b + 1) % n
    for city in parent2[b + 1:] + parent2[:b + 1]:
        if city not in segment_set:
            child[pos] = city
            pos = (pos + 1) % n

    return child

# =============================================================================
# MUTATION
# =============================================================================

def mutate_swap(tour):
    """Échange deux villes aléatoires."""
    n = len(tour)
    i, j = random.sample(range(n), 2)
    tour[i], tour[j] = tour[j], tour[i]
    return tour


def mutate_inversion(tour):
    """Inverse un segment aléatoire du tour (équivalent à un mouvement 2-opt)."""
    n = len(tour)
    i, j = sorted(random.sample(range(n), 2))
    tour[i:j + 1] = tour[i:j + 1][::-1]
    return tour


def mutate_or_opt(tour):
    """
    Or-opt : déplace un segment de 1, 2 ou 3 villes consécutives
    vers une autre position du tour.
    """
    n = len(tour)
    seg_len = random.randint(1, min(3, n - 2))
    i = random.randint(0, n - seg_len - 1)
    segment = tour[i:i + seg_len]
    rest = tour[:i] + tour[i + seg_len:]
    j = random.randint(0, len(rest))
    new_tour = rest[:j] + segment + rest[j:]
    return new_tour


def mutate(tour, mutation_rate):
    """Applique une mutation aléatoire avec probabilité mutation_rate."""
    if random.random() < mutation_rate:
        choice = random.random()
        if choice < 0.4:
            return mutate_inversion(tour[:])
        elif choice < 0.7:
            return mutate_or_opt(tour[:])
        else:
            return mutate_swap(tour[:])
    return tour

# =============================================================================
# OPTIMISATION LOCALE — 2-OPT
# =============================================================================

def two_opt(tour, dist, max_iter=None, time_limit=None):
    """
    Amélioration locale 2-opt : inverse des segments jusqu'à convergence.
    Paramètres optionnels pour limiter le temps ou les itérations.
    """
    n = len(tour)
    improved = True
    iterations = 0
    t0 = time.time()

    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                if j == n - 1 and i == 0:
                    continue  # évite le cas trivial de retournement complet

                # Gain du 2-opt : remplacer (i, i+1) et (j, j+1) par (i, j) et (i+1, j+1)
                a, b = tour[i], tour[i + 1]
                c, d = tour[j], tour[(j + 1) % n]
                delta = (dist[a][c] + dist[b][d]) - (dist[a][b] + dist[c][d])
                if delta < -1e-10:
                    tour[i + 1:j + 1] = tour[i + 1:j + 1][::-1]
                    improved = True

        iterations += 1
        if max_iter and iterations >= max_iter:
            break
        if time_limit and time.time() - t0 > time_limit:
            break

    return tour


def or_opt_improve(tour, dist, seg_len=1):
    """
    Amélioration locale or-opt : teste le déplacement de segments de longueur seg_len.
    """
    n = len(tour)
    improved = True
    while improved:
        improved = False
        for i in range(n):
            # Segment à déplacer
            seg = [tour[(i + k) % n] for k in range(seg_len)]
            seg_set = set(seg)
            prev_i = tour[(i - 1) % n]
            next_seg = tour[(i + seg_len) % n]

            # Coût actuel de connexion du segment à sa position
            cost_remove = (dist[prev_i][seg[0]] + dist[seg[-1]][next_seg]
                           - dist[prev_i][next_seg])

            for j in range(n):
                if j in range(i - 1, i + seg_len + 1):
                    continue
                before = tour[j]
                after = tour[(j + 1) % n]
                if before in seg_set or after in seg_set:
                    continue
                gain = (cost_remove + dist[before][after]
                        - dist[before][seg[0]] - dist[seg[-1]][after])
                if gain > 1e-10:
                    # Reconstruction du tour
                    flat = []
                    k = (i + seg_len) % n
                    while k != i:
                        flat.append(tour[k])
                        k = (k + 1) % n
                    # Insertion après j dans flat
                    pos = flat.index(after)
                    new_tour = flat[:pos] + seg + flat[pos:]
                    tour = new_tour
                    improved = True
                    break
            if improved:
                break
    return tour

# =============================================================================
# ALGORITHME GÉNÉTIQUE PRINCIPAL
# =============================================================================

def genetic_algorithm(cities, time_budget=60, pop_size=150, mutation_rate=0.02,
                      elite_ratio=0.1, tournament_k=5):
    """
    Résout le TSP par algorithme génétique.

    Paramètres :
        cities        : liste de [lon, lat]
        time_budget   : temps maximum en secondes
        pop_size      : taille de la population
        mutation_rate : probabilité de mutation par individu
        elite_ratio   : fraction des meilleurs individus conservés directement (élitisme)
        tournament_k  : taille du tournoi de sélection

    Retourne le meilleur tour trouvé et sa distance.
    """
    n = len(cities)
    dist = build_distance_matrix(cities)

    print(f"  Matrice de distances calculée ({n}x{n})")

    # --- Initialisation ---
    population = init_population(pop_size, n, dist)

    # Amélioration initiale 2-opt rapide sur chaque individu
    print("  Amélioration 2-opt initiale...")
    time_per_indiv = min(2.0, time_budget * 0.1 / pop_size)
    for i in range(len(population)):
        population[i] = two_opt(population[i], dist, time_limit=time_per_indiv)

    fitnesses = [tour_distance(t, dist) for t in population]

    best_idx = min(range(pop_size), key=lambda i: fitnesses[i])
    best_tour = population[best_idx][:]
    best_dist = fitnesses[best_idx]

    print(f"  Distance initiale : {best_dist:.2f} km")

    n_elite = max(1, int(pop_size * elite_ratio))
    t_start = time.time()
    generation = 0
    
    no_improve_count = 0

    # --- Boucle génétique ---
    while time.time() - t_start < time_budget:
        generation += 1
        new_population = []

        # Élitisme : copie les meilleurs individus directement
        elite_indices = sorted(range(pop_size), key=lambda i: fitnesses[i])[:n_elite]
        for idx in elite_indices:
            new_population.append(population[idx][:])

        # Génération des enfants
        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, fitnesses, tournament_k)
            parent2 = tournament_selection(population, fitnesses, tournament_k)

            child = order_crossover(parent1, parent2)
            child = mutate(child, mutation_rate)

            # 2-opt léger sur l'enfant (1 passe rapide)
            if n <= 200:
                child = two_opt(child, dist, max_iter=1)

            new_population.append(child)

        population = new_population
        fitnesses = [tour_distance(t, dist) for t in population]

        # Mise à jour du meilleur
        gen_best_idx = min(range(pop_size), key=lambda i: fitnesses[i])
        if fitnesses[gen_best_idx] < best_dist:
            best_dist = fitnesses[gen_best_idx]
            best_tour = population[gen_best_idx][:]
            no_improve_count = 0
        else:
            no_improve_count += 1
            
        if no_improve_count >= MAX_NO_IMPROVE:
            break
        
        if generation % 20 == 0:
            elapsed = time.time() - t_start
            print(f"  Gen {generation:4d} | Meilleure dist : {best_dist:.2f} km | "
                  f"Temps écoulé : {elapsed:.1f}s")

    # --- Optimisation locale finale sur le meilleur tour ---
    print("  Optimisation 2-opt finale...")
    remaining = max(5, time_budget - (time.time() - t_start))
    best_tour = two_opt(best_tour, dist, time_limit=remaining)
    best_dist = tour_distance(best_tour, dist)
    print(f"  Distance finale : {best_dist:.2f} km après {generation} générations")

    return best_tour, best_dist

# =============================================================================
# PIPELINE PRINCIPAL
# =============================================================================

def run_instance(instance_id, time_budget=60, **ga_kwargs):
    """
    Exécute le pipeline complet sur une instance :
    1. Récupère les données
    2. Lance l'algorithme génétique
    3. Soumet la meilleure solution
    """
    print(f"\n{'='*60}")
    print(f"Instance : {instance_id}")
    print(f"{'='*60}")

    data = get_instance(instance_id)
    cities = data["cities"]
    print(f"  {len(cities)} villes chargées")

    best_tour, best_dist = genetic_algorithm(cities, time_budget=time_budget, **ga_kwargs)

    print(f"  Soumission de la solution (distance locale : {best_dist:.2f} km)...")
    print(f"  Tour soumis : {best_tour[:10]}... (total {len(best_tour)} villes)")
    result = submit_solution(instance_id, best_tour)
    if result:
        print(f"  Statut      : {result.get('status')}")
        print(f"  Distance    : {result.get('distance'):.2f} km")
        print(f"  Amélioré    : {result.get('improved')}")
        print(f"  Dans top 5  : {result.get('in_top5')}")
        if result.get("in_top5"):
            print(f"  Rang        : #{result.get('rank')}")

    return best_tour, best_dist


if __name__ == "__main__":
    # Paramètres par instance (ajustés selon la taille et le temps disponible)
    instances_config = {
        "regions":     {"time_budget": 30,  "pop_size": 200},
        # "random_50":   {"time_budget": 60,  "pop_size": 150},
        # "prefectures": {"time_budget": 20, "pop_size": 200},
        # "random_100":  {"time_budget": 120, "pop_size": 100},
        # "random_200":  {"time_budget": 20, "pop_size": 80},
        # "random_500":  {"time_budget": 300, "pop_size": 50},
        # "hard_clusters":  {"time_budget": 300, "pop_size": 50},
        # "hard_grid":  {"time_budget": 300, "pop_size": 50},
        # "hard_circles":  {"time_budget": 300, "pop_size": 50},
        # "hard_star":  {"time_budget": 300, "pop_size": 50},
        # "hard_spiral":  {"time_budget": 300, "pop_size": 70},
        # "hard_hierarchical":  {"time_budget": 180, "pop_size": 50},
    }

    # Lancement sur toutes les instances (commenter celles à ignorer)
    for instance_id, cfg in instances_config.items():
        run_instance(instance_id, **cfg)
