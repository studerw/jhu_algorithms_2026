import json
import sys


class Player:
    def __init__(self, name: str, position: str, cost: int, war: float):
        self.name = name
        self.position = position
        self.cost = cost  # in dollars, multiple of $100,000
        self.war = war

    def __repr__(self):
        return f"Player(name={self.name!r}, position={self.position!r}, cost=${self.cost:,}, war={self.war})"

    @classmethod
    def from_dict(cls, d: dict) -> "Player":
        return cls(
            name=d["name"],
            position=d["position"],
            cost=d["cost"],
            war=d["war"],
        )


class ProblemInput:
    def __init__(self, maximum_cost: int, players: list[Player]):
        self.maximum_cost = maximum_cost
        self.players = players

    def __repr__(self):
        return f"ProblemInput(maximum_cost=${self.maximum_cost:,}, players=[{len(self.players)} players])"


def parse_stdin() -> ProblemInput:
    raw = sys.stdin.read()
    data = json.loads(raw)
    maximum_cost = data["maximum_cost"]
    players = [Player.from_dict(entry) for entry in data["players"]]
    return ProblemInput(maximum_cost, players)


def solve(input_obj: ProblemInput):
    # TODO: implement dynamic programming solution
    pass


def main():
    input_obj = parse_stdin()

    print(f"Budget: ${input_obj.maximum_cost:,}")
    print(f"Read {len(input_obj.players)} players:")
    for p in input_obj.players:
        print(f"  {p}")


if __name__ == "__main__":
    main()
