import json
import sys


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
    raw_json: str = sys.stdin.read()
    data: dict[str, object] = json.loads(raw_json)
    maximum_cost = int(data["maximum_cost"])  # type: ignore[arg-type]
    players: set[Player] = {
        Player.from_dict(entry)  # type: ignore[arg-type]
        for entry in data["players"]  # type: ignore[union-attr]
    }
    return PlayersAndMaxCost(maximum_cost, players)


def solve(p_a_m_c: PlayersAndMaxCost) -> set[Player]:
    return brute_force_solve(p_a_m_c.players, p_a_m_c.maximum_cost)

def brute_force_solve(players: set[Player], maximum_cost: int) -> set[Player]:
    # Pop a player off the stack
    current_player = next(iter(players), None)

    # No more players or no more money
    if current_player is None or maximum_cost == 0:
        return players

    players.remove(current_player)
    result_with_current = set()

    # If this player is too expensive, try all the other players
    result_without_current = brute_force_solve(players, maximum_cost)

    # If he's not then get the optimal subsolution for play and the other players not in his position
    if current_player.cost < maximum_cost:
        result_with_current = brute_force_solve({p for p in players if p.position != current_player.position}, maximum_cost-current_player.cost)

    max_war_with = sum(p.war for p in result_with_current)
    max_war_without = sum(p.war for p in result_without_current)
    if (max_war_with > max_war_without):
        players.add(current_player)

    return players



def main() -> None:
    input_obj: PlayersAndMaxCost = parse_stdin()

    print(f"Budget: ${input_obj.maximum_cost:,}")
    print(f"Read {len(input_obj.players)} players:")
    for p in input_obj.players:
        print(f"  {p}")

    result: set[Player] = solve(input_obj)
    print(f"----------------\n\n")
    for p in result:
        print(f"  {p}")
    print(f"----------------\n\n")
    total_war = sum(p.war for p in result)
    total_cost = sum(p.cost for p in result)
    extra_money = input_obj.maximum_cost - total_cost
    print(f"Total WAR: {total_war:.1f}")
    print(f"Total Cost: ${total_cost:,}, Extra Money: ${extra_money:,}")

if __name__ == "__main__":
    main()
