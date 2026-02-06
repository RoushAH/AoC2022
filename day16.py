import re
from collections import defaultdict
from itertools import combinations

import numpy as np
from numba import njit
import networkx as nx

from utils import file_name


def split_line(line):
    pattern = re.compile(
        r"^Valve\s+([A-Z]+)\s+has\s+flow\s+rate=(\d+);\s+"
        r"tunnels?\s+lead[s]?\s+to\s+valves?\s+(.+)$"
    )
    m = pattern.match(line)
    if not m:
        print(line)
        raise ValueError("No match")
    valve = m.group(1)
    flow = int(m.group(2))
    targets = [v.strip() for v in m.group(3).split(",")]
    return valve, flow, targets


def get_data(file):
    edges = set()
    flows = {}
    for row in file.split('\n'):
        name, rate, targets = split_line(row)
        edges.update((name, t) for t in targets)
        if rate:
            flows[name] = rate
    G = nx.Graph()
    G.add_edges_from(edges)
    return G, flows


@njit
def dfs(cur, time_left, opened_mask, cost, flow, memo):
    # memo dims: [2^n, n+1, minutes+1]
    cached = memo[opened_mask, cur, time_left]
    if cached != -1:
        return cached

    n = flow.shape[0]
    best = 0

    for v in range(n):
        bit = 1 << v
        if opened_mask & bit:
            continue

        t2 = time_left - cost[cur, v] - 1  # move + open
        if t2 <= 0:
            continue

        gain = flow[v] * t2
        val = gain + dfs(v, t2, opened_mask | bit, cost, flow, memo)
        if val > best:
            best = val

    memo[opened_mask, cur, time_left] = best
    return best


def best_pressure_numba(costs, flows, minutes=30, start="AA"):
    """
    costs: dict[str][str] -> int  (shortest path steps between named nodes)
    flows: dict[str] -> int       (ONLY nonzero-flow valves, per your note)
    """
    valves = list(flows.keys())
    n = len(valves)

    # Map valve names -> indices 0..n-1
    vid = {name: i for i, name in enumerate(valves)}

    # We'll represent the start node as index n (not in flows)
    START = n

    # cost[cur, v] where cur in 0..n plus START=n, and v in 0..n-1
    cost = np.empty((n + 1, n), dtype=np.int16)

    # Fill cost rows for each "current" node: each valve + AA(start)
    # Row for each valve as current:
    for cur_name, cur_idx in vid.items():
        row = costs[cur_name]
        for v_name, v_idx in vid.items():
            if v_name != cur_name:
                cost[cur_idx, v_idx] = row[v_name]
            else:
                cost[cur_idx, v_idx] = 0

    # Row for start:
    row = costs[start]
    for v_name, v_idx in vid.items():
        cost[START, v_idx] = row[v_name]

    flow = np.array([flows[name] for name in valves], dtype=np.int32)

    # memo[mask, cur, t] initialized to -1
    memo = np.full((1 << n, n + 1, minutes + 1), -1, dtype=np.int32)

    return int(dfs(START, minutes, 0, cost, flow, memo))


def get_limited_graph(G, flows):
    nodes = ["AA"] + [f for f in flows if flows[f] > 0]
    costs = defaultdict(dict)
    for a, b in combinations(nodes, 2):
        costs[a][b] = nx.shortest_path_length(G, a, b)
        costs[b][a] = costs[a][b]
    return costs


@njit
def dfs_fill_best_by_mask(cur, time_left, opened_mask, total, cost, flow, best_by_mask):
    # Record best total for this opened set
    if total > best_by_mask[opened_mask]:
        best_by_mask[opened_mask] = total

    n = flow.shape[0]
    for v in range(n):
        bit = 1 << v
        if opened_mask & bit:
            continue

        t2 = time_left - cost[cur, v] - 1  # move + open
        if t2 <= 0:
            continue

        gain = flow[v] * t2
        dfs_fill_best_by_mask(v, t2, opened_mask | bit, total + gain, cost, flow, best_by_mask)


@njit
def maximize_over_submasks(best_by_mask):
    """
    After this, best_by_mask[mask] becomes:
      max(best_by_mask[submask]) for all submask ⊆ mask
    This is crucial so pairing with the complement works correctly.
    """
    n_masks = best_by_mask.size
    # infer n such that 2^n == n_masks
    n = 0
    while (1 << n) < n_masks:
        n += 1

    for i in range(n):
        bit = 1 << i
        for mask in range(n_masks):
            if mask & bit:
                other = mask ^ bit
                if best_by_mask[other] > best_by_mask[mask]:
                    best_by_mask[mask] = best_by_mask[other]


@njit
def best_two_agents(best_by_mask):
    all_mask = best_by_mask.size - 1
    best = 0
    for mask in range(best_by_mask.size):
        other = all_mask ^ mask
        val = best_by_mask[mask] + best_by_mask[other]
        if val > best:
            best = val
    return best


def best_pressure_numba_elephant(costs, flows, minutes=26, start="AA"):
    """
    Part 2: you + elephant, both start at AA, both have `minutes` (26), valves are disjoint.
    costs: dict[str][str] -> int  (shortest path steps between named nodes)
    flows: dict[str] -> int       (ONLY nonzero-flow valves)
    """
    valves = list(flows.keys())
    n = len(valves)

    vid = {name: i for i, name in enumerate(valves)}
    START = n

    # Build cost matrix (same as your part 1)
    cost = np.empty((n + 1, n), dtype=np.int16)

    for cur_name, cur_idx in vid.items():
        row = costs[cur_name]
        for v_name, v_idx in vid.items():
            if v_name != cur_name:
                cost[cur_idx, v_idx] = row[v_name]
            else:
                cost[cur_idx, v_idx] = 0

    row = costs[start]
    for v_name, v_idx in vid.items():
        cost[START, v_idx] = row[v_name]

    flow = np.array([flows[name] for name in valves], dtype=np.int32)

    # best_by_mask[mask] = best pressure you can get opening exactly that set (as discovered by DFS)
    best_by_mask = np.full((1 << n,), -1, dtype=np.int32)

    # Explore all feasible opening sequences, recording best score per mask
    dfs_fill_best_by_mask(START, minutes, 0, 0, cost, flow, best_by_mask)

    # Turn "exactly mask" into "any submask of mask" so complements pair correctly
    maximize_over_submasks(best_by_mask)

    # Pair disjoint subsets (mask for you, complement for elephant)
    return int(best_two_agents(best_by_mask))


def part_one(file, tgt=None, minutes=None):
    print("\n\n", "Part one!", "\n")
    connections, flows = get_data(file)
    # Next step, get a limited graph that only contains nodes with value
    costs = get_limited_graph(connections, flows)
    score = best_pressure_numba(costs, flows, minutes)
    print(score)
    # score = explore(costs, minutes, flows)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None, minutes=None):
    print("\n\n", "Part two!", "\n")

    connections, flows = get_data(file)
    costs = get_limited_graph(connections, flows)
    score = p2 = best_pressure_numba_elephant(costs, flows, minutes=26, start="AA")
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def main():
    filename = file_name()
    with open(f"data/{filename}.txt", 'r') as f:
        data_file = f.read()
    with open(f"test/{filename}.txt", 'r') as f:
        test_file = f.read()

    part_one(test_file, 1651, 30)
    part_one(data_file, minutes=30)
    part_two(test_file, 1707, 26)
    part_two(data_file)


if __name__ == '__main__':
    main()
