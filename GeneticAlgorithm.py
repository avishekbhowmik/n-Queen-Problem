#!/usr/bin/env python3
import sys
import time
import random
import tracemalloc

def conflicts(board):
    n = len(board)
    c = 0
    for i in range(n):
        for j in range(i+1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                c += 1
    return c

def fitness(board):
    maxc = len(board) * (len(board) - 1) // 2
    return maxc - conflicts(board)

def ordered_crossover(p1, p2):
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    child = [-1] * n
    child[a:b+1] = p1[a:b+1]
    pos = b + 1
    for val in p2:
        if val not in child:
            if pos >= n:
                pos = 0
            child[pos] = val
            pos += 1
    return child

def mutate_swap(ind, rate):
    if random.random() < rate:
        i, j = random.sample(range(len(ind)), 2)
        ind[i], ind[j] = ind[j], ind[i]
    return ind

def roulette(pop, fits):
    total = sum(fits)
    pick = random.uniform(0, total)
    acc = 0
    for i, f in enumerate(fits):
        acc += f
        if acc >= pick:
            return pop[i][:]
    return pop[-1][:]

def genetic_algorithm(n, pop_size, gens, mut_rate=0.1, elite=2):
    pop = [random.sample(range(n), n) for _ in range(pop_size)]
    best_sol = None
    best_fit = -1
    max_fit = n * (n - 1) // 2
    for gen in range(gens):
        fits = [fitness(ind) for ind in pop]
        gen_best = max(fits)
        if gen_best > best_fit:
            best_fit = gen_best
            best_sol = pop[fits.index(gen_best)][:]
            if best_fit == max_fit:
                return best_sol, gen+1
        elite_idx = sorted(range(pop_size), key=lambda i: fits[i], reverse=True)[:elite]
        new_pop = [pop[i][:] for i in elite_idx]
        while len(new_pop) < pop_size:
            p1 = roulette(pop, fits)
            p2 = roulette(pop, fits)
            child = ordered_crossover(p1, p2)
            child = mutate_swap(child, mut_rate)
            new_pop.append(child)
        pop = new_pop
    return best_sol, gens

def solve_ga(n):
    if n <= 30:
        pop, gens = 100, 1000
    elif n <= 100:
        pop, gens = 150, 2000
    elif n <= 200:
        pop, gens = 200, 4000
    else:
        pop, gens = 300, 8000
    mut_rate = 0.1
    elite = max(2, int(0.1 * pop))
    tracemalloc.start()
    start = time.perf_counter()
    sol, used = genetic_algorithm(n, pop, gens, mut_rate, elite)
    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    final_conf = conflicts(sol) if sol else None
    return {
        'success': final_conf == 0,
        'time_sec': end - start,
        'memory_mb': peak / (1024 * 1024),
        'generations': used,
        'final_conflicts': final_conf
    }

if __name__ == "__main__":
    n = None
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            pass
    if n is None:
        n = int(input("Enter N: "))
    res = solve_ga(n)
    print(f"Success: {res['success']}")
    print(f"Time: {res['time_sec']:.4f}s")
    print(f"Memory: {res['memory_mb']:.2f} MB")
    print(f"Generations: {res['generations']}")
    print(f"Conflicts: {res['final_conflicts']}")