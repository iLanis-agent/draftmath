// Draft math - pure arithmetic engine, runs in browser and node.
(function(root){
"use strict";
function r0(x){ return Math.round(x); }
function r1(x){ return Math.round(x*10)/10; }
function r2(x){ return Math.round(x*100)/100; }
function pos(nums, msg){
  for (var i=0;i<nums.length;i++){ if (!isFinite(nums[i]) || nums[i] <= 0) return { error: msg }; }
  return null;
}
function gapPlan(gapMm, perimeterM){
  var bad = pos([gapMm, perimeterM], "gap and perimeter must be positive");
  if (bad) return bad;
  var area = gapMm * perimeterM * 10; // mm/10 cm wide, m*100 cm long
  var hole = 2 * Math.sqrt(area / Math.PI);
  return { areaCm2: r0(area), holeCm: r1(hole) };
}
function stripPlan(doors, windows, doorM, windowM, rollM){
  var bad = pos([doors, windows, doorM, windowM, rollM], "doors, windows, perimeters and roll must be positive");
  if (bad) return bad;
  var total = doors * doorM + windows * windowM;
  var rolls = Math.ceil(total / rollM);
  return { totalM: r1(total), rolls: rolls, leftM: r1(rolls * rollM - total) };
}
function costPlan(rolls, priceRoll, doors, windows, minEach){
  var bad = pos([rolls, priceRoll, doors, windows, minEach], "rolls, price, frames and minutes must be positive");
  if (bad) return bad;
  var minutes = r0((doors + windows) * minEach);
  return { cost: r2(rolls * priceRoll), minutes: minutes };
}
function plural(n, w){ return n + " " + w + (n === 1 ? "" : "s"); }
function renderGap(r, gapMm, perimeterM){
  return "A " + gapMm + " mm gap along " + perimeterM + " m is " + r.areaCm2 + " cm²" + " of open air - a hole about " + r.holeCm + " cm across, the size of a labeled brick.";
}
function renderStrip(r, doors, windows, rollM){
  return plural(doors, "door") + " and " + plural(windows, "window") + " need " + r.totalM + " m of strip - " + plural(r.rolls, "roll") + " of " + rollM + " m, " + r.leftM + " m left over.";
}
function renderCost(r, rolls, priceRoll, minEach){
  return plural(rolls, "roll") + " at " + priceRoll + " each is " + r.cost + " - plus about " + plural(r.minutes, "minute") + " of your Saturday at a labeled " + minEach + " minutes a frame.";
}
var api = { gapPlan: gapPlan, stripPlan: stripPlan, costPlan: costPlan,
  renderGap: renderGap, renderStrip: renderStrip, renderCost: renderCost };
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.DraftMath = api;
})(typeof window !== "undefined" ? window : globalThis);
