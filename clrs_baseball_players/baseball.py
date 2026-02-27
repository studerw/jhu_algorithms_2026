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


def parse_stdin() -> list[Player]:
    raw = sys.stdin.read()
    data = json.loads(raw)
    players = [Player.from_dict(entry) for entry in data]
    return players


def solve(players: list[Player], budget: int):
    # TODO: implement dynamic programming solution
    pass


def main():
    players = parse_stdin()

    print(f"Read {len(players)} players:")
    for p in players:
        print(f"  {p}")


if __name__ == "__main__":
    main()