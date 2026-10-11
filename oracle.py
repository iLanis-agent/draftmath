#!/usr/bin/env python3
"""Python mirror of engine.js - regenerates expected.json. Exact float-for-float mirror."""
import json, math, os

def r0(x): return math.floor(x + 0.5)
def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100
def jsnum(x):
    if isinstance(x, float) and x == int(x): return int(x)
    return x
def fmt(x): return repr(jsnum(x))
def pos(nums, msg):
    for n in nums:
        if not (n > 0) or n != n or n == float('inf'): return {"error": msg}
    return None

def gapPlan(gapMm, perimeterM):
    bad = pos([gapMm, perimeterM], "gap and perimeter must be positive")
    if bad: return bad
    area = gapMm * perimeterM * 10
    hole = 2 * math.sqrt(area / math.pi)
    return {"areaCm2": r0(area), "holeCm": jsnum(r1(hole))}

def stripPlan(doors, windows, doorM, windowM, rollM):
    bad = pos([doors, windows, doorM, windowM, rollM], "doors, windows, perimeters and roll must be positive")
    if bad: return bad
    total = doors * doorM + windows * windowM
    rolls = math.ceil(total / rollM)
    return {"totalM": jsnum(r1(total)), "rolls": rolls, "leftM": jsnum(r1(rolls * rollM - total))}

def costPlan(rolls, priceRoll, doors, windows, minEach):
    bad = pos([rolls, priceRoll, doors, windows, minEach], "rolls, price, frames and minutes must be positive")
    if bad: return bad
    minutes = r0((doors + windows) * minEach)
    return {"cost": jsnum(r2(rolls * priceRoll)), "minutes": minutes}

def plural(n, w): return fmt(n) + " " + w + ("" if n == 1 else "s")

def renderGap(r, gapMm, perimeterM):
    return "A " + fmt(gapMm) + " mm gap along " + fmt(perimeterM) + " m is " + str(r["areaCm2"]) + " cm²" + " of open air - a hole about " + fmt(r["holeCm"]) + " cm across, the size of a labeled brick."

def renderStrip(r, doors, windows, rollM):
    return plural(doors, "door") + " and " + plural(windows, "window") + " need " + fmt(r["totalM"]) + " m of strip - " + plural(r["rolls"], "roll") + " of " + fmt(rollM) + " m, " + fmt(r["leftM"]) + " m left over."

def renderCost(r, rolls, priceRoll, minEach):
    return plural(rolls, "roll") + " at " + fmt(priceRoll) + " each is " + fmt(r["cost"]) + " - plus about " + plural(r["minutes"], "minute") + " of your Saturday at a labeled " + fmt(minEach) + " minutes a frame."

cases = []
gap_args = [(3,5),(2,4),(5,6),(1,5),(4,4.5),(3,8),(2.5,5),(6,3),(3.5,6.5),(2,10),(4,7),(1.5,4),(0,5),(3,0)]
for a in gap_args:
    r = gapPlan(*a)
    case = {"fn": "gapPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderGap(r, a[0], a[1])
    cases.append(case)
strip_args = [(2,3,5,4,5),(1,2,5,4,5),(3,4,5,3.5,10),(2,0,5,4,5),(4,6,5,4,5),
              (1,1,5,4,5),(2,3,5,4,10),(3,2,6,4.5,5),(1,4,5,3,5),(2,5,5,4,6),
              (5,3,5,4,5),(2,2,4.5,3.5,5),(0,3,5,4,5),(2,3,0,4,5),(2,3,5,4,0)]
for a in strip_args:
    r = stripPlan(*a)
    case = {"fn": "stripPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderStrip(r, a[0], a[1], a[4])
    cases.append(case)
cost_args = [(5,4,2,3,15),(3,5,1,2,15),(6,3.5,3,4,20),(2,6,1,1,15),(8,4,4,6,15),
             (1,5,1,1,15),(4,4.5,2,2,18),(7,3,3,3,15),(5,5,2,3,12),(3,4,1,2,25),
             (6,4,2,4,15),(9,3.2,4,5,16),(0,4,2,3,15),(5,0,2,3,15),(5,4,0,3,15),(5,4,2,3,0)]
for a in cost_args:
    r = costPlan(*a)
    case = {"fn": "costPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderCost(r, a[0], a[1], a[4])
    cases.append(case)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expected.json")
with open(out, "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print("wrote", len(cases), "cases")
