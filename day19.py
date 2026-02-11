from dataclasses import replace, asdict, fields
from functools import lru_cache

from utils import file_name, prod
import re
from dataclasses import dataclass

TYPES = "geo", "obs", "clay", "ore"

blueprint_re = re.compile(
    r"^Blueprint\s+(?P<id>\d+):\s+"
    r"Each\s+ore\s+robot\s+costs\s+(?P<ore_ore>\d+)\s+ore\.\s+"
    r"Each\s+clay\s+robot\s+costs\s+(?P<clay_ore>\d+)\s+ore\.\s+"
    r"Each\s+obsidian\s+robot\s+costs\s+(?P<obs_ore>\d+)\s+ore\s+and\s+(?P<obs_clay>\d+)\s+clay\.\s+"
    r"Each\s+geode\s+robot\s+costs\s+(?P<geo_ore>\d+)\s+ore\s+and\s+(?P<geo_obs>\d+)\s+obsidian\.$"
)

best_geo = 0


@dataclass(frozen=True)
class Blueprint:
    id: int
    ore_ore: int
    clay_ore: int
    obs_ore: int
    geo_ore: int
    geo_obs: int
    obs_clay: int


@dataclass(frozen=True)
class Stock:
    ore: int = 0
    clay: int = 0
    obs: int = 0
    geo: int = 0


@dataclass(frozen=True)
class Bots:
    ore: int = 1
    clay: int = 0
    obs: int = 0
    geo: int = 0


@dataclass(frozen=True)
class State:
    time: int
    stock: Stock
    bots: Bots
    skipped: tuple = ()  # Bot types we could have built last turn but chose not to

    def key(self):
        return (
            self.time,
            self.stock.ore, self.stock.clay, self.stock.obs, self.stock.geo,
            self.bots.ore, self.bots.clay, self.bots.obs, self.bots.geo,
        )


def add_stock(s: Stock, b: Bots) -> Stock:
    return Stock(
        s.ore + b.ore,
        s.clay + b.clay,
        s.obs + b.obs,
        s.geo + b.geo,
    )


def buy_bot(s: Stock, b: Bots, blueprint: Blueprint, kind: str) -> tuple[Stock, Bots]:
    if kind not in TYPES:
        raise ValueError(f"Unknown bot kind: {kind}")

    # Compute cost
    if kind == "ore":
        cost = Stock(ore=blueprint.ore_ore)
    elif kind == "clay":
        cost = Stock(ore=blueprint.clay_ore)
    elif kind == "obs":
        cost = Stock(
            ore=blueprint.obs_ore,
            clay=blueprint.obs_clay,
        )
    elif kind == "geo":
        cost = Stock(
            ore=blueprint.geo_ore,
            obs=blueprint.geo_obs,
        )

    # Affordability check
    if (
            s.ore < cost.ore
            or s.clay < cost.clay
            or s.obs < cost.obs
            or s.geo < cost.geo
    ):
        raise ValueError(f"Cannot afford {kind} bot")

    # Deduct stock
    new_stock = Stock(
        ore=s.ore - cost.ore,
        clay=s.clay - cost.clay,
        obs=s.obs - cost.obs,
        geo=s.geo - cost.geo,
    )

    # Increment bot count (dynamic field update)
    new_bots = replace(b, **{kind: getattr(b, kind) + 1})

    return new_stock, new_bots


def is_viable(state: State, blueprint: dict) -> bool:
    # Cap max useful spend
    max_ore = max(
        getattr(blueprint, f.name)
        for f in fields(blueprint)
        if f.name.endswith("_ore")
    )
    max_clay = max(
        getattr(blueprint, f.name)
        for f in fields(blueprint)
        if f.name.endswith("_clay")
    )
    max_obsidian = max(
        getattr(blueprint, f.name)
        for f in fields(blueprint)
        if f.name.endswith("_obs")
    )
    if state.bots.ore > max_ore:
        return False
    if state.bots.clay > max_clay:
        return False
    if state.bots.obs > max_obsidian:
        return False
    return True


def cap_stocks(time, stock, bots, blueprint, skipped=()) -> State:
    max_ore = max(
        getattr(blueprint, f.name)
        for f in fields(blueprint)
        if f.name.endswith("_ore")
    )
    max_clay = max(
        getattr(blueprint, f.name)
        for f in fields(blueprint)
        if f.name.endswith("_clay")
    )
    max_obsidian = max(
        getattr(blueprint, f.name)
        for f in fields(blueprint)
        if f.name.endswith("_obs")
    )

    ore = min(stock.ore, time * max_ore - bots.ore * (time - 1))
    clay = min(stock.clay, time * max_clay - bots.clay * (time - 1))
    obsidian = min(stock.obs, time * max_obsidian - bots.obs * (time - 1))

    stock = Stock(ore=ore, clay=clay, obs=obsidian, geo=stock.geo)

    return State(time=time, stock=stock, bots=bots, skipped=skipped)


def geo_limit(state):
    return state.stock.geo + state.bots.geo * state.time + state.time * (state.time - 1) // 2


@lru_cache(maxsize=None)
def run_minute(state, blueprint):
    """ Choose robot to build, Collect resources, Add robot to bots"""
    global best_geo
    if state.time == 0:
        # print("   ", state.stock.geo)
        if state.stock.geo > best_geo:
            best_geo = state.stock.geo
        return state.stock.geo
    # Find which bots we can afford (excluding ones we skipped last turn)
    can_afford = []
    for kind in TYPES:
        needs = {
            k.split("_")[1]: v
            for k, v in asdict(blueprint).items()
            if k.startswith(kind)
        }
        has = [getattr(state.stock, k, -1) >= v for k, v in needs.items()]
        if all(has):
            can_afford.append(kind)

    # "Don't wait" pruning: exclude bots we could have built last turn but chose not to
    new_options = [k for k in can_afford if k not in state.skipped]

    stock = add_stock(state.stock, state.bots)
    time = state.time - 1
    if "geo" in new_options:
        # Always build geo if we can (skipped=() since we're building)
        new_states = [cap_stocks(time, *buy_bot(stock, state.bots, blueprint, "geo"), blueprint, skipped=())]
    else:
        # Do nothing option: carry forward what we could have built as "skipped"
        do_nothing = cap_stocks(time, stock, state.bots, blueprint, skipped=tuple(can_afford))
        new_states = [do_nothing] if geo_limit(do_nothing) > best_geo else []

        for kind in new_options:
            # Building a bot clears skipped (skipped=())
            this_state = cap_stocks(time, *buy_bot(stock, state.bots, blueprint, kind), blueprint, skipped=())
            if is_viable(this_state, blueprint) and geo_limit(this_state) > best_geo:
                new_states.append(this_state)
    scores = [run_minute(s, blueprint) for s in new_states]
    best = max(scores) if scores else 0
    return best


def get_blueprint_info(file):
    for line in file.split("\n"):
        m = blueprint_re.match(line)
        if m:
            data = {k: int(v) for k, v in m.groupdict().items()}
            yield Blueprint(**data)


def find_the_score(blueprints, time=24, method=None):
    scorez = []
    global best_geo
    for data in blueprints:
        run_minute.cache_clear()
        best_geo = 0
        print(data)
        stock = Stock()
        bots = Bots(ore=1)
        state = State(time=time, stock=stock, bots=bots)
        if not method:
            print(s:=run_minute(state, data) * data.id)
            scorez.append(s)
        else:
            print(s := run_minute(state, data) * data.id)
            scorez.append(s)
    if not method:
        method = sum
    s =  method(scorez)
    return s


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    blueprints = get_blueprint_info(file)
    score = find_the_score(blueprints)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    blueprints = list(get_blueprint_info(file))[:3]
    score = find_the_score(blueprints, 32, method=prod)
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

    part_one(test_file, 33)
    part_one(data_file)
    part_two(test_file,62)
    part_two(data_file)


if __name__ == '__main__':
    main()
