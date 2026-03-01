import json
import sys

# Global debug variable
DEBUG = False

class Player:
    def __init__(self, name: str, position: str, cost: int, war: float) -> None:
        self.name = name
        self.position = position
        self.cost = cost  # in dollars, multiple of $100,000
        self.war = war

    def __repr__(self) -> str:
        return f"Player(name={self.name!r}, position={self.position!r}, cost=${self.cost:,}, war={self.war})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.name == other.name and self.position == other.position

    def __hash__(self) -> int:
        return hash((self.name, self.position))

    @classmethod
    def from_dict(cls, d: dict[str, object]) -> "Player":
        return cls(
            name=str(d["name"]),
            position=str(d["position"]),
            cost=int(d["cost"]),  # type: ignore[arg-type]
            war=float(d["war"]),  # type: ignore[arg-type]
        )


class PlayersAndMaxCost:
    def __init__(self, maximum_cost: int, players: set[Player]) -> None:
        self.maximum_cost = maximum_cost
        self.players = players

    def __repr__(self) -> str:
        return f"PlayersAndMaxCost(maximum_cost=${self.maximum_cost:,}, players=[{len(self.players)} players])"


def parse_stdin() -> PlayersAndMaxCost:
    if "-f" in sys.argv or "--file" in sys.argv:
        try:
            idx = sys.argv.index("-f") if "-f" in sys.argv else sys.argv.index("--file")
            filename = sys.argv[idx + 1]
            f = open(filename, 'r')
            raw_json = f.read()
            f.close()
        except (IndexError, IOError) as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        raw_json = sys.stdin.read()

    data: dict[str, object] = json.loads(raw_json)
    maximum_cost = int(data["maximum_cost"])  # type: ignore[arg-type]
    players: set[Player] = {
        Player.from_dict(entry)  # type: ignore[arg-type]
        for entry in data["players"]  # type: ignore[union-attr]
    }
    return PlayersAndMaxCost(maximum_cost, players)


def solve(p_a_m_c: PlayersAndMaxCost, use_memo: bool) -> set[Player]:
    if use_memo:
        memo: dict[tuple[frozenset[Player], int], set[Player]] = {}
        return memoized_solve(p_a_m_c.players, p_a_m_c.maximum_cost, memo)
    else:
        return brute_force_solve(p_a_m_c.players, p_a_m_c.maximum_cost)


def brute_force_solve(players: set[Player], maximum_cost: int) -> set[Player]:
    current_player = next(iter(players), None)
    if current_player is None or maximum_cost <= 0:
        return set()

    remaining_players = {p for p in players if p != current_player}

    # Branch A: Without
    result_without_current = brute_force_solve(remaining_players, maximum_cost)

    # Branch B: With
    result_with_current = set()
    if current_player.cost <= maximum_cost:
        others_at_diff_pos = {p for p in remaining_players if p.position != current_player.position}
        sub_result = brute_force_solve(others_at_diff_pos, maximum_cost - current_player.cost)
        result_with_current = {current_player} | sub_result

    war_with = sum(p.war for p in result_with_current)
    war_without = sum(p.war for p in result_without_current)

    if DEBUG:
        print(f"DEBUG: Evaluating {current_player.name if current_player else 'None'}")

    return result_with_current if war_with > war_without else result_without_current


def memoized_solve(
    players: set[Player],
    maximum_cost: int,
    memo: dict[tuple[frozenset[Player], int], set[Player]],
) -> set[Player]:
    key: tuple[frozenset[Player], int] = (frozenset(players), maximum_cost)
    if key in memo:
        if DEBUG:
            print(f"DEBUG: Cache hit — {len(players)} players, budget ${maximum_cost:,}")
        return memo[key]

    current_player = next(iter(players), None)
    if current_player is None or maximum_cost <= 0:
        memo[key] = set()
        return set()

    remaining_players = {p for p in players if p != current_player}

    # Branch A: Without
    result_without_current = memoized_solve(remaining_players, maximum_cost, memo)

    # Branch B: With
    result_with_current: set[Player] = set()
    if current_player.cost <= maximum_cost:
        others_at_diff_pos = {p for p in remaining_players if p.position != current_player.position}
        sub_result = memoized_solve(others_at_diff_pos, maximum_cost - current_player.cost, memo)
        result_with_current = {current_player} | sub_result

    war_with = sum(p.war for p in result_with_current)
    war_without = sum(p.war for p in result_without_current)

    if DEBUG:
        print(f"DEBUG: Evaluating {current_player.name}")

    result = result_with_current if war_with > war_without else result_without_current
    memo[key] = result
    return result


def main() -> None:
    global DEBUG
    if "-d" in sys.argv or "--debug" in sys.argv:
        DEBUG = True

    use_memo: bool = "-m" in sys.argv or "--memo" in sys.argv

    input_obj: PlayersAndMaxCost = parse_stdin()

    if DEBUG:
        print("DEBUG MODE ENABLED")
        print(f"Using: {'memoized' if use_memo else 'brute force'} solver")

    print(f"Budget: ${input_obj.maximum_cost:,}")
    print(f"Read {len(input_obj.players)} players:")
    if DEBUG:
        for p in input_obj.players:
            print(f"  {p}")

    result: set[Player] = solve(input_obj, use_memo)

    if DEBUG:
        print(f"----------------\n\n")
        for p in result:
            print(f"  {p}")
        print(f"----------------\n\n")

    total_war = sum(p.war for p in result)
    total_cost = sum(p.cost for p in result)
    extra_money = input_obj.maximum_cost - total_cost
    print(f"Total WAR: {total_war:.1f}")
    print(f"Total Cost: ${total_cost:,}, Money Left Over (should be positive): ${extra_money:,}")


if __name__ == "__main__":
    main()
