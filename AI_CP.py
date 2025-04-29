import heapq
import math
import itertools


class State:
    def __init__(self, m_left, c_left, boat, total_m, total_c):
        self.m_left = m_left
        self.c_left = c_left
        self.m_right = total_m - m_left
        self.c_right = total_c - c_left
        self.boat = boat
        self.total_m = total_m
        self.total_c = total_c

    def is_valid(self):
        if (0 <= self.m_left <= self.total_m and 0 <= self.c_left <= self.total_c and
                0 <= self.m_right <= self.total_m and 0 <= self.c_right <= self.total_c):
            if (self.m_left == 0 or self.m_left >= self.c_left) and \
                    (self.m_right == 0 or self.m_right >= self.c_right):
                return True
        return False

    def is_goal(self):
        return self.m_left == 0 and self.c_left == 0 and self.boat == 'right'

    def heuristic(self):
        return math.ceil((self.m_left + self.c_left) / 2)

    def visualize(self):
        left_bank = "M" * self.m_left + "C" * self.c_left
        right_bank = "M" * self.m_right + "C" * self.c_right
        boat = "B"
        if self.boat == 'left':
            print(f"| {left_bank} {boat:<2} ~~~RIVER~~~ {right_bank:>10} |")
        else:
            print(f"| {left_bank:<10} ~~~RIVER~~~ {boat} {right_bank} |")

    def get_successors(self):
        successors = []
        moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

        for m, c in moves:
            if self.boat == 'left':
                new_state = State(self.m_left - m, self.c_left - c, 'right', self.total_m, self.total_c)
            else:
                new_state = State(self.m_left + m, self.c_left + c, 'left', self.total_m, self.total_c)

            if new_state.is_valid():
                successors.append((new_state, (m, c)))

        return successors

    def __hash__(self):
        return hash((self.m_left, self.c_left, self.boat))

    def __eq__(self, other):
        return (self.m_left, self.c_left, self.boat) == (other.m_left, other.c_left, other.boat)


def a_star_search(total_m, total_c):
    start = State(total_m, total_c, 'left', total_m, total_c)
    frontier = []
    counter = itertools.count()  # Unique counter for tie-breaking
    heapq.heappush(frontier, (start.heuristic(), 0, next(counter), start, []))
    visited = set()

    while frontier:
        f, g, _, current, path = heapq.heappop(frontier)

        if current.is_goal():
            return path

        if current in visited:
            continue
        visited.add(current)

        for next_state, move in current.get_successors():
            if next_state not in visited:
                new_g = g + 1
                h = next_state.heuristic()
                new_f = new_g + h
                new_path = path + [(move, current, next_state, new_f, new_g, h)]
                heapq.heappush(frontier, (new_f, new_g, next(counter), next_state, new_path))

    return None


def main():
    total_m = int(input("Enter number of missionaries: "))
    total_c = int(input("Enter number of cannibals: "))

    if total_c > total_m:
        print("Invalid input: Cannibals cannot outnumber missionaries at the start.")
        return

    solution = a_star_search(total_m, total_c)

    if solution:
        print("\nSteps to solve the problem:\n")
        start_state = State(total_m, total_c, 'left', total_m, total_c)
        start_state.visualize()
        print("Initial State\n")

        for i, (move, from_state, to_state, f_val, g_val, h_val) in enumerate(solution, 1):
            print(f"Step {i}: Move {move[0]} M and {move[1]} C from {from_state.boat} to {to_state.boat}")
            to_state.visualize()
            print(f"Left Bank -> M: {to_state.m_left}, C: {to_state.c_left}")
            print(f"Right Bank -> M: {to_state.m_right}, C: {to_state.c_right}")
            print(f"Step Validity: {'VALID ✅' if to_state.is_valid() else 'INVALID ❌'}")
            print(f"A* value (f(n)): {f_val} | Cost so far (g(n)): {g_val} | Heuristic value (h(n)): {h_val}\n")
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()
