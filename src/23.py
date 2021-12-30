from __future__ import annotations

from pathlib import Path

import utils


class State:
    cost = 0
    hallway: list[str]
    room_a: list[str]
    room_b: list[str]
    room_c: list[str]
    room_d: list[str]

    def __str__(self):
        string = ""
        string += f"#############\n"
        string += f"#{''.join(self.hallway)}#\n"
        string += f"###{self.room_a[0]}#{self.room_b[0]}#{self.room_c[0]}#{self.room_d[0]}###\n"
        for i in range(1, len(self.room_a)):
            string += f"  #{self.room_a[i]}#{self.room_b[i]}#{self.room_c[i]}#{self.room_d[i]}#  \n"
        string += f"  #########  "

        return string

    def cleared_rooms(self) -> int:
        return sum(
            (
                all(ch == "A" or ch == " " for ch in self.room_a),
                all(ch == "B" or ch == " " for ch in self.room_b),
                all(ch == "C" or ch == " " for ch in self.room_c),
                all(ch == "D" or ch == " " for ch in self.room_d),
            )
        )

    def complete(self) -> bool:
        return (
            all(ch == " " for ch in self.hallway)
            and all(amphipod == "A" for amphipod in self.room_a)
            and all(amphipod == "B" for amphipod in self.room_b)
            and all(amphipod == "C" for amphipod in self.room_c)
            and all(amphipod == "D" for amphipod in self.room_d)
        )

    def copy(self) -> State:
        new_state = State()
        new_state.cost = self.cost
        new_state.hallway = self.hallway.copy()
        new_state.room_a = self.room_a.copy()
        new_state.room_b = self.room_b.copy()
        new_state.room_d = self.room_d.copy()
        new_state.room_c = self.room_c.copy()
        return new_state

    def hallway_free(self, room_index, hallway_index):
        return all(ch == " " for ch in (self.hallway[hallway_index + 1 : room_index + 1] or self.hallway[room_index:hallway_index]))

    def amphipod_movement_cost(self, amphipod: str):
        if amphipod == "A":
            return 1
        elif amphipod == "B":
            return 10
        elif amphipod == "C":
            return 100
        elif amphipod == "D":
            return 1000
        raise Exception(f"unknown amphipod: {amphipod}")

    def valid_moves(self) -> list[State]:
        amphipod_room_dict = {
            "A": (self.room_a, 2),
            "B": (self.room_b, 4),
            "C": (self.room_c, 6),
            "D": (self.room_d, 8),
        }
        room_door_indexes = [door_index for _, door_index in amphipod_room_dict.values()]

        # An amphipod can move out of a room
        clearing_moves: list[State] = []
        for room_key, (room, door_index) in amphipod_room_dict.items():
            if not all(ch == room_key or ch == " " for ch in room):
                for room_index, room_space in enumerate(room):
                    if room_space != " ":
                        for hallway_index, hallway_space in enumerate(self.hallway):
                            if hallway_space == " " and hallway_index not in room_door_indexes and self.hallway_free(door_index, hallway_index):
                                spaces_to_move = room_index + 1 + abs(door_index - hallway_index)
                                movement_cost = self.amphipod_movement_cost(room_space) * spaces_to_move
                                new_state = self.copy()
                                new_state.cost += movement_cost
                                if room is self.room_a:
                                    new_state.hallway[hallway_index] = new_state.room_a[room_index]
                                    new_state.room_a[room_index] = " "
                                elif room is self.room_b:
                                    new_state.hallway[hallway_index] = new_state.room_b[room_index]
                                    new_state.room_b[room_index] = " "
                                elif room is self.room_c:
                                    new_state.hallway[hallway_index] = new_state.room_c[room_index]
                                    new_state.room_c[room_index] = " "
                                elif room is self.room_d:
                                    new_state.hallway[hallway_index] = new_state.room_d[room_index]
                                    new_state.room_d[room_index] = " "
                                clearing_moves.append(new_state)
                        break

        # An amphipod in the hallway can move into their room
        solving_moves = []
        for hallway_index, hallway_space in enumerate(self.hallway):
            if hallway_space == " ":
                continue

            target_room, target_door_index = amphipod_room_dict[hallway_space]
            if self.hallway_free(target_door_index, hallway_index):
                for room_index, room_space in reversed(list(enumerate(target_room))):
                    if room_space == " ":
                        spaces_to_move = room_index + 1 + abs(target_door_index - hallway_index)
                        movement_cost = self.amphipod_movement_cost(hallway_space) * spaces_to_move
                        new_state = self.copy()
                        new_state.cost += movement_cost
                        if target_room is self.room_a:
                            new_state.room_a[room_index] = hallway_space
                        elif target_room is self.room_b:
                            new_state.room_b[room_index] = hallway_space
                        elif target_room is self.room_c:
                            new_state.room_c[room_index] = hallway_space
                        elif target_room is self.room_d:
                            new_state.room_d[room_index] = hallway_space
                        new_state.hallway[hallway_index] = " "
                        solving_moves.append(new_state)
                        break
                    elif room_space != hallway_space:
                        break

        return sorted(solving_moves, key=lambda state: state.cost) + sorted(clearing_moves, key=lambda state: (-state.cleared_rooms(), state.cost))


def load_initial_state(path: Path) -> State:
    state = State()
    state.hallway = [" "] * 11
    state.room_a = []
    state.room_b = []
    state.room_c = []
    state.room_d = []
    lines = utils.read_lines(path)
    for line in lines:
        a, b, c, d = line
        state.room_a.append(a)
        state.room_b.append(b)
        state.room_c.append(c)
        state.room_d.append(d)
    return state


def recursion(state: State, min_so_far: int | None = None) -> int | None:
    if min_so_far is not None and state.cost >= min_so_far:
        # print(f"found worse solution, returning: {min_so_far}")
        return min_so_far

    if state.complete():
        print(f"found solution: {state.cost}")
        return state.cost

    for new_state in state.valid_moves():
        min_so_far = recursion(new_state, min_so_far) or min_so_far

    return min_so_far


def main(path: Path) -> int:
    return recursion(load_initial_state(path))


if __name__ == "__main__":
    input_path_part_1 = Path(__file__).parents[1] / "inputs" / "23.1.txt"
    print("Part 1:")
    print(main(input_path_part_1))

    input_path_part_2 = Path(__file__).parents[1] / "inputs" / "23.2.txt"
    print("Part 2:")
    print(main(input_path_part_2))
