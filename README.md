# FastBox Delivery System

A Python-based logistics simulator for a fictional delivery company called **FastBox**.  
This project simulates one day of delivery operations — assigning packages to agents, calculating distances, and generating a delivery report.

---

## Problem Statement

There are multiple warehouses, delivery agents, and packages on a 2D map.  
The goal is to:
- Assign each package to the nearest available agent
- Simulate the delivery (warehouse → destination)
- Calculate total distance traveled by each agent
- Find the most efficient agent and save a report

---

## How It Works

1. Reads warehouse, agent, and package data from a JSON file
2. For each package, finds the nearest agent to its warehouse using Euclidean distance
3. Simulates each agent traveling: their location → warehouse → destination
4. Calculates total distance and efficiency score per agent
5. Saves the final report to `report.json`

---

## Project Structure

```
FastBox Delivery System/
├── Delivery System.py                         # main script
├── base_case.json                             # sample input data
├── report.json                                # output report (auto-generated)
└── Python Assignment(Delivery System Test Cases)/
        ├── test_case_1.json
        ├── test_case_2.json
        └── ... (up to test_case_10.json)
```

---

## How to Run

```bash
# Run with base case
python "Delivery System.py"

# Run with a specific test case
python "Delivery System.py" "Python Assignment(Delivery System Test Cases)/test_case_1.json"
```

---

## Input Format (JSON)

```json
{
  "warehouses": {
    "W1": [0, 0],
    "W2": [50, 75]
  },
  "agents": {
    "A1": [5, 5],
    "A2": [60, 60]
  },
  "packages": [
    {"id": "P1", "warehouse": "W1", "destination": [30, 40]}
  ]
}
```

---

## Output Format (report.json)

```json
{
  "A1": {
    "packages_delivered": 2,
    "total_distance": 121.21,
    "efficiency": 60.61
  },
  "A2": {
    "packages_delivered": 2,
    "total_distance": 79.21,
    "efficiency": 39.6
  },
  "A3": {
    "packages_delivered": 1,
    "total_distance": 14.14,
    "efficiency": 14.14
  },
  "best_agent": "A3"
}
```

> **Efficiency** = total distance / packages delivered (lower is better)

---

## Requirements

- Python 3.x
- No external libraries needed (only `json`, `math`, `sys` — all built-in)

---

## Sample Output

```
loading file: base_case.json
warehouses: 3
agents: 3
packages: 5

package assignments:
  A1 -> ['P1', 'P4']
  A2 -> ['P2', 'P5']
  A3 -> ['P3']

Delivery Report:
----------------------------------------
  A1: packages=2  distance=121.21  efficiency=60.61
  A2: packages=2  distance=79.21  efficiency=39.6
  A3: packages=1  distance=14.14  efficiency=14.14

  best agent: A3
----------------------------------------
report saved to report.json
```
