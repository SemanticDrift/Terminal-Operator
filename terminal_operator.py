def is_admissible(k):
    """
    Check if k is in the admissible lock set L = {4n | n ∈ ℕ₀}.
    """
    return k % 4 == 0


def terminal_operator(s):
    """
    The Terminal Operator T
    Series: Mathematical Foundations for Universal Systems
    Author: Carolina Johnson (CJ), December 31, 2025

    Projects any state s onto the nearest admissible lock point
    using exactly one binary choice. No backtracking. No search.

    Lock set L = {0, 4, 8, 12, 16, 20, ...}

    T(s) = k_s      if k_s ∈ L
    T(s) = k_s + 1  if k_s ∉ L and k_s + 1 ∈ L
    T(s) = None     otherwise (terminal state ⊥)

    Parameters:
    - s: state value in ℕ≥4

    Returns:
    - projected lock point, or None if terminal
    """
    k = s // 10
    if is_admissible(k):
        return k
    elif is_admissible(k + 1):
        return k + 1
    else:
        return None


def is_recoverable(s):
    """
    Admissibility predictor: determine without computation
    whether state s will find a lock point.

    For any s, let a = ⌊s/10⌋.
    Recoverable if (a mod 4 == 0) or ((a+1) mod 4 == 0).
    """
    a = s // 10
    return (a % 4 == 0) or ((a + 1) % 4 == 0)


def descend(s):
    """
    Follow the full T-chain from s to its terminal state.

    Parameters:
    - s: starting state >= 4

    Returns:
    - chain: list of states in the descent sequence
    - terminal: final lock point or None
    """
    chain = [s]
    current = s
    while True:
        nxt = terminal_operator(current)
        if nxt is None or nxt == current:
            break
        chain.append(nxt)
        current = nxt
    return chain, current


def admissibility_map(limit=200):
    """
    Classify all states up to limit as admissible or terminal.
    Reproduces the structural pattern: 10 admissible, 10 terminal,
    repeating every 20 units.
    """
    results = []
    for s in range(4, limit + 1):
        target = terminal_operator(s)
        status = "Admissible" if target is not None else "Terminal Block"
        results.append((s, s // 10, target, status))
    return results


if __name__ == "__main__":
    print("--- THE TERMINAL OPERATOR ---")
    print("Prevents cascading drift without backtracking.")
    print()

    # Demonstrate descent chains
    test_states = [1523, 7890, 4321, 99999, 123456]
    print("Descent chains:")
    for s in test_states:
        chain, terminal = descend(s)
        chain_str = " -> ".join(str(x) for x in chain)
        status = f"lock: {terminal}" if terminal is not None else "terminal: ⊥"
        print(f"  {s} -> {chain_str} [{status}]")

    print()

    # Show the 20-unit cycle
    print("Admissibility structure (first 60 states):")
    print(f"{'s':>6}  {'floor':>6}  {'T(s)':>6}  {'status'}")
    print("-" * 40)
    for s, k, target, status in admissibility_map(60):
        t_str = str(target) if target is not None else "⊥"
        print(f"  {s:>4}    {k:>4}    {t_str:>4}  {status}")

    print()
    print("Pattern repeats every 20 units.")
    print("10 admissible. 10 terminal. Predictable without computation.")
    print()
    print("One degree of freedom is the minimum amount required for stability.")
