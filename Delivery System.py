import json
import math
import sys

# load the json file
def load_data(file):
    f = open(file, "r")
    data = json.load(f)
    f.close()

    # warehouses can be dict or list so handling both
    if isinstance(data["warehouses"], dict):
        warehouses = data["warehouses"]
    else:
        warehouses = {}
        for w in data["warehouses"]:
            warehouses[w["id"]] = w["location"]

    # same for agents
    if isinstance(data["agents"], dict):
        agents = data["agents"]
    else:
        agents = {}
        for a in data["agents"]:
            agents[a["id"]] = a["location"]

    packages = data["packages"]

    return warehouses, agents, packages


# euclidean distance between two points
def get_distance(p1, p2):
    dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    return dist


# find which agent is closest to each package's warehouse and assign
def assign_packages(packages, warehouses, agents):
    assigned = {}
    for a in agents:
        assigned[a] = []

    for pkg in packages:
        # get warehouse key - sometimes its "warehouse" sometimes "warehouse_id"
        if "warehouse" in pkg:
            wid = pkg["warehouse"]
        else:
            wid = pkg["warehouse_id"]

        w_loc = warehouses[wid]

        # check distance from every agent to this warehouse
        closest = None
        min_dist = 99999

        for agent_id in agents:
            d = get_distance(agents[agent_id], w_loc)
            if d < min_dist:
                min_dist = d
                closest = agent_id

        assigned[closest].append(pkg)

    return assigned


# simulate each agent picking up and delivering packages
def simulate(assigned, warehouses, agents):
    result = {}

    for agent_id in assigned:
        pkgs = assigned[agent_id]
        total_dist = 0
        current_pos = agents[agent_id]  # agent starts from their location

        for pkg in pkgs:
            if "warehouse" in pkg:
                wid = pkg["warehouse"]
            else:
                wid = pkg["warehouse_id"]

            w_loc = warehouses[wid]
            dest = pkg["destination"]

            # agent goes to warehouse first then to destination
            total_dist += get_distance(current_pos, w_loc)
            total_dist += get_distance(w_loc, dest)

            current_pos = dest  # agent is now at destination

        count = len(pkgs)
        if count > 0:
            efficiency = round(total_dist / count, 2)
        else:
            efficiency = 0

        result[agent_id] = {
            "packages_delivered": count,
            "total_distance": round(total_dist, 2),
            "efficiency": efficiency
        }

    return result


# find agent with lowest efficiency (best performance)
def get_best_agent(result):
    best = None
    best_eff = 99999

    for agent_id in result:
        if result[agent_id]["packages_delivered"] == 0:
            continue
        if result[agent_id]["efficiency"] < best_eff:
            best_eff = result[agent_id]["efficiency"]
            best = agent_id

    return best


# save report to json file
def save_report(result, best):
    report = {}
    for agent_id in result:
        report[agent_id] = result[agent_id]
    report["best_agent"] = best

    with open("report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("report saved to report.json")


# main function
def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "base_case.json"

    print("loading file:", filename)

    warehouses, agents, packages = load_data(filename)

    print("warehouses:", len(warehouses))
    print("agents:", len(agents))
    print("packages:", len(packages))

    # assign packages to agents
    assigned = assign_packages(packages, warehouses, agents)

    print("\npackage assignments:")
    for a in assigned:
        ids = [p["id"] for p in assigned[a]]
        print(" ", a, "->", ids)

    # simulate deliveries
    result = simulate(assigned, warehouses, agents)

    # find best agent
    best = get_best_agent(result)

    # print report
    print("\nDelivery Report:")
    print("-" * 40)
    for agent_id in result:
        r = result[agent_id]
        print(f"  {agent_id}: packages={r['packages_delivered']}  distance={r['total_distance']}  efficiency={r['efficiency']}")
    print(f"\n  best agent: {best}")
    print("-" * 40)

    save_report(result, best)


main()