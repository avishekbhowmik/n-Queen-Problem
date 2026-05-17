import sys
import time
import random
import math
import tracemalloc

def conflicts(board):
    n = len(board)
    c = 0
    for i in range(n):
        for j in range(i+1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                c += 1
    return c

def simulated_annealing(n, temp0=1000, cooling=0.995, max_iter=50000):
    current = list(range(n))
    random.shuffle(current)
    cur_conf = conflicts(current)
    temp = temp0
    for it in range(max_iter):
        if cur_conf == 0:
            return current, it+1
        i, j = random.sample(range(n), 2)
        current[i], current[j] = current[j], current[i]
        new_conf = conflicts(current)
        delta = new_conf - cur_conf
        if delta < 0 or random.random() < math.exp(-delta / temp):
            cur_conf = new_conf
        else:
            current[i], current[j] = current[j], current[i]
        temp *= cooling
    return current, max_iter

def solve_sa(n):
    tracemalloc.start()
    start = time.perf_counter()
    sol, iters = simulated_annealing(n)
    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    final_conf = conflicts(sol) if sol else None
    return {
        'success': final_conf == 0,
        'time_sec': end - start,
        'memory_mb': peak / (1024 * 1024),
        'iterations': iters,
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
    res = solve_sa(n)
    print(f"Success: {res['success']}")
    print(f"Time: {res['time_sec']:.4f}s")
    print(f"Memory: {res['memory_mb']:.2f} MB")
    print(f"Iterations: {res['iterations']}")
    print(f"Conflicts: {res['final_conflicts']}")