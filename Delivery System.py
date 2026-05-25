import json
import math
import sys
import csv

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


# bonus feature 1 - show a simple ascii map of all locations
def show_ascii_map(warehouses, agents, packages):
    print("\nASCII Route Map:")
    print("-" * 40)

    # collect all x and y values to figure out the map size
    all_x = []
    all_y = []

    for wid in warehouses:
        all_x.append(warehouses[wid][0])
        all_y.append(warehouses[wid][1])

    for aid in agents:
        all_x.append(agents[aid][0])
        all_y.append(agents[aid][1])

    for pkg in packages:
        all_x.append(pkg["destination"][0])
        all_y.append(pkg["destination"][1])

    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)

    # grid size 20x20
    grid_size = 20

    # make empty grid
    grid = []
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            row.append(".")
        grid.append(row)

    # helper to convert real coords to grid coords
    def to_grid(x, y):
        if max_x == min_x:
            gx = 0
        else:
            gx = int((x - min_x) / (max_x - min_x) * (grid_size - 1))

        if max_y == min_y:
            gy = 0
        else:
            gy = int((y - min_y) / (max_y - min_y) * (grid_size - 1))

        return gx, gy

    # place warehouses on grid
    for wid in warehouses:
        gx, gy = to_grid(warehouses[wid][0], warehouses[wid][1])
        grid[gy][gx] = "W"

    # place agents on grid
    for aid in agents:
        gx, gy = to_grid(agents[aid][0], agents[aid][1])
        grid[gy][gx] = "A"

    # place destinations on grid
    for pkg in packages:
        gx, gy = to_grid(pkg["destination"][0], pkg["destination"][1])
        if grid[gy][gx] == ".":
            grid[gy][gx] = "*"

    # print the grid
    for row in grid:
        print(" ".join(row))

    print("\nLegend:  A = Agent   W = Warehouse   * = Destination")
    print("-" * 40)


# bonus feature 2 - export top performer to csv
def export_top_to_csv(result, best):
    with open("top_performer.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["agent_id", "packages_delivered", "total_distance", "efficiency"])

        # write best agent first
        r = result[best]
        writer.writerow([best, r["packages_delivered"], r["total_distance"], r["efficiency"]])

    print("top performer saved to top_performer.csv")


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

    # bonus features
    show_ascii_map(warehouses, agents, packages)
    export_top_to_csv(result, best)


main()
