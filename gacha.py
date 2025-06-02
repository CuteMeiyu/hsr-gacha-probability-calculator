import argparse
import re
from functools import cache

import data


def calc(pulls: int, route: str, character_pity=0, lightcone_pity=0, character_guaranteed=False, lightcone_guaranteed=False):
    return _calc(pulls, route, character_pity, lightcone_pity, character_guaranteed, lightcone_guaranteed)


@cache
def _calc(pulls: int, route: str, cp=0, lp=0, cg=False, lg=False):
    if len(route) == 0:
        return 1.0
    current = route[0]
    dist = data.dist[current]
    if current == "C":
        dist = dist[cp:]
        max_n = min(len(dist), pulls)
        rev = 1.0 / data.rev_dist[current][cp]
        if cg:
            return sum(dist[n] * rev * _calc(pulls - n - 1, route[1:], 0, lp, False, lg) for n in range(max_n))
        return sum(dist[n] * rev * 0.5625 * _calc(pulls - n - 1, route[1:], 0, lp, False, lg) for n in range(max_n)) + sum(
            dist[n] * rev * 0.4375 * _calc(pulls - n - 1, route, 0, lp, True, lg) for n in range(max_n)
        )
    else:
        dist = dist[lp:]
        max_n = min(len(dist), pulls)
        rev = 1.0 / data.rev_dist[current][lp]
        if lg:
            return sum(dist[n] * rev * _calc(pulls - n - 1, route[1:], cp, 0, cg, False) for n in range(max_n))
        return sum(dist[n] * rev * 0.78125 * _calc(pulls - n - 1, route[1:], cp, 0, cg, False) for n in range(max_n)) + sum(
            dist[n] * rev * 0.21875 * _calc(pulls - n - 1, route, cp, 0, cg, True) for n in range(max_n)
        )


def convert_target(route: str):
    return f"E{route.count("C")-1}S{route.count("L")}"


def flat_route(route: str):
    parts: list[str] = re.findall(r"(\d+|\D+)", route)
    if len(parts) == 0:
        return ""
    parts = [parts[0]] + [parts[i - 1][-1] * (int(part) - 1) if part.isdigit() else part for i, part in enumerate(parts) if i > 0]
    return "".join(parts)


def main():
    parser = argparse.ArgumentParser(description="HSR Gacha Probability Calculator")
    parser.add_argument(dest="pulls", type=int)
    parser.add_argument(dest="route", type=str, help='Order (C: Character, L: Lightcone). For example if you want E0 -> S1 -> E2: "CLCC" or "CLC2"')
    parser.add_argument("-cp", "--character_pity", type=int, default=0)
    parser.add_argument("-lp", "--lightcone_pity", type=int, default=0)
    parser.add_argument("-cg", "--character_guaranteed", action="store_true")
    parser.add_argument("-lg", "--lightcone_guaranteed", action="store_true")
    parser.add_argument("-d", "--digit", type=int, default=4)
    args = parser.parse_args()
    args.route = flat_route(args.route.upper())
    if not all(char in "CL" for char in args.route):
        parser.error("Invalid route")
    if args.character_pity < 0 or args.character_pity >= 90:
        parser.error("Invalid character pity")
    if args.lightcone_pity < 0 or args.lightcone_pity >= 80:
        parser.error("Invalid lightcone pity")
    kwargs = {key: value for key, value in args._get_kwargs() if key not in ("route", "digit")}
    print(f"Target: {convert_target(args.route)}", ("Probability: {:." + str(args.digit) + "%}").format(calc(**kwargs, route=args.route)), sep=", ")
    sub_routes = [args.route[:i] for i in range(1, len(args.route) + 1)]
    targets = [convert_target(sub_route) for sub_route in sub_routes]
    rev_cumu = [calc(**kwargs, route=sub_route) for sub_route in sub_routes]
    dist = [rev_cumu[i] - rev_cumu[i + 1] for i in range(len(rev_cumu) - 1)]
    dist.append(rev_cumu[-1])
    table = [targets[i] + ": " + ("{:." + str(args.digit) + "%}").format(dist[i]) for i in range(len(dist)) if round(dist[i], args.digit + 2) > 0]
    print("Distribution:")
    print(*table, sep="\n")


if __name__ == "__main__":
    main()
