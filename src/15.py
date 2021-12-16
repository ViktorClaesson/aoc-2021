NODE_INDEX = tuple[int, int]
COST_MATRIX = dict[NODE_INDEX, int]


def get_side_length(cost_matrix: COST_MATRIX) -> int:
    side_length = len(cost_matrix) ** 0.5
    if side_length % 1 != 0:
        raise "Not square"
    return int(side_length)


def get_neighbours(cost_matrix: COST_MATRIX, node: NODE_INDEX) -> list[NODE_INDEX]:
    x, y = node
    return [neighbour for neighbour in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)] if neighbour in cost_matrix]


def main(cost_matrix: COST_MATRIX) -> int:
    lowest_cost_matrix: COST_MATRIX = {(0, 0): 0}
    queue: set[NODE_INDEX] = {(0, 0)}

    while queue:
        current = min(queue, key=lambda node: lowest_cost_matrix[node])
        queue.remove(current)
        for neighbour in get_neighbours(cost_matrix, current):
            if neighbour not in lowest_cost_matrix or lowest_cost_matrix[current] + cost_matrix[neighbour] < lowest_cost_matrix[neighbour]:
                lowest_cost_matrix[neighbour] = cost_matrix[neighbour] + lowest_cost_matrix[current]
                queue.add(neighbour)

    lower_right_index = get_side_length(cost_matrix) - 1
    return lowest_cost_matrix[(lower_right_index, lower_right_index)]


def extend_matrix(matrix: COST_MATRIX, times: int) -> COST_MATRIX:
    side_length = get_side_length(matrix)
    return {
        (x + dx * side_length, y + dy * side_length): 1 + (cost + dx + dy - 1) % 9
        for (x, y), cost in matrix.items()
        for dy in range(times)
        for dx in range(times)
    }


if __name__ == "__main__":
    with open("src/15.txt") as file:
        ls = file.read().splitlines()

    global_matrix: COST_MATRIX = {(x, y): int(ch) for y, ch_row in enumerate(ls) for x, ch in enumerate(ch_row)}

    print("Part 1:")
    print(main(global_matrix))
    print("Part 2:")
    print(main(extend_matrix(global_matrix, 5)))
