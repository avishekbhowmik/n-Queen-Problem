import sys
import time
import tracemalloc

def solve_dfs(n):
    board = [-1] * n
    cols = [False] * n
    diag1 = [False] * (2 * n - 1)
    diag2 = [False] * (2 * n - 1)
    solutions = []

    def dfs(row):
        if row == n:
            solutions.append(board.copy())
            return True
        for col in range(n):
            d1 = row - col + n - 1
            d2 = row + col
            if not cols[col] and not diag1[d1] and not diag2[d2]:
                board[row] = col
                cols[col] = diag1[d1] = diag2[d2] = True
                if dfs(row + 1):
                    return True
                cols[col] = diag1[d1] = diag2[d2] = False
                board[row] = -1
        return False

    tracemalloc.start()
    start = time.perf_counter()
    dfs(0)
    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        'success': len(solutions) > 0,
        'time_sec': end - start,
        'memory_mb': peak / (1024 * 1024),
        'solutions': len(solutions)
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
    res = solve_dfs(n)
    print(f"Success: {res['success']}")
    print(f"Time: {res['time_sec']:.4f}s")
    print(f"Memory: {res['memory_mb']:.2f} MB")
    print(f"Solutions found: {res['solutions']}")