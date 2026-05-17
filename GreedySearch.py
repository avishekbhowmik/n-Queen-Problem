# Greedy Search Algorithm for N-Queen Problem
# Add your Greedy Search implementation here.
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

def hill_climbing(n, restarts=100, max_steps=5000):
    best_board = None
    best_conf = float('inf')
    for _ in range(restarts):
        board = list(range(n))
        random.shuffle(board)
        conf = conflicts(board)
        steps = 0
        while steps < max_steps:
            if conf == 0:
                if conf < best_conf:
                    best_board = board[:]
                    best_conf = conf
                break
            improved = False
            for i in range(n):
                for j in range(i+1, n):
                    board[i], board[j] = board[j], board[i]
                    new_conf = conflicts(board)
                    if new_conf < conf:
                        conf = new_conf
                        improved = True
                        break
                    else:
                        board[i], board[j] = board[j], board[i]
                if improved:
                    break
            if not improved:
                break
            steps += 1
        if best_conf == 0:
            break
    return best_board, best_conf

def solve_greedy(n):
    tracemalloc.start()
    start = time.perf_counter()
    sol, conf = hill_climbing(n)
    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        'success': conf == 0,
        'time_sec': end - start,
        'memory_mb': peak / (1024 * 1024),
        'final_conflicts': conf
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
    res = solve_greedy(n)
    print(f"Success: {res['success']}")
    print(f"Time: {res['time_sec']:.4f}s")
    print(f"Memory: {res['memory_mb']:.2f} MB")
    print(f"Conflicts: {res['final_conflicts']}")