#!/usr/bin/env python3
"""
Builds the Bar Inventory & Pour Cost Calculator (.xlsx).
    python3 tools/lead-magnets/build_bar_calculator.py <output.xlsx>
"""
import sys
from xlsxlite import S, Sheet, r2, save

OUT = sys.argv[1]

# ---------- How to use ----------
h = Sheet("How to use", [4, 100])
h.set("B2", "EPAY POS  |  Bar Inventory & Pour Cost Calculator", S["title"])
h.set("B3", "Know what every pour costs you, and catch liquor that's leaving without being rung in.", S["note"])
lines = [
    ("How it works", S["sub"]),
    ("1.  Pour Cost tab: one row per product. Enter the bottle size, what you pay for the bottle, your pour size and what you charge. It works out pours per bottle, cost per pour, pour cost % and profit per drink.", S["body"]),
    ("2.  Inventory Count tab: count once a week, same day and time. Enter the opening count, what came in, the closing count and that product's sales from your POS. It shows what you used and your real pour cost %.", S["body"]),
    ("3.  Compare the two. When real pour cost runs higher than the recipe says it should, liquor is going out as over-pours, spills, comps or drinks that were never rung in.", S["body"]),
    ("", S["body"]),
    ("Which cells to edit", S["sub"]),
    ("Yellow cells with blue numbers are yours to fill in. White cells are formulas: leave them alone. The first row on each tab is an example. Type over it or clear it.", S["body"]),
    ("Count partial bottles as decimals: a bottle about half full is 0.5.", S["body"]),
    ("", S["body"]),
    ("The formulas", S["sub"]),
    ("Pours per bottle  =  bottle size (oz)  ÷  pour size (oz)", S["body"]),
    ("Cost per pour  =  bottle cost  ÷  bottle size  ×  pour size", S["body"]),
    ("Pour cost %  =  cost per pour  ÷  drink price", S["body"]),
    ("Used  =  opening count  +  received  −  closing count", S["body"]),
    ("Real pour cost %  =  cost of what you used  ÷  sales of that product", S["body"]),
    ("", S["body"]),
    ("Bottle sizes in ounces:  375 ml = 12.7 oz  ·  750 ml = 25.4 oz  ·  1 liter = 33.8 oz  ·  1.75 liter = 59.2 oz", S["note"]),
    ("Your target pour cost % is your call. Set it from your own prices and costs.", S["note"]),
    ("", S["body"]),
    ("From EPAY POS", S["sub"]),
    ("EPAY POS integrates with AndroBar, a liquor pouring system (androbar.com). If your counts keep showing more liquor used than you sold, ask us how AndroBar works with EPAY POS at your bar.", S["body"]),
    ("Tabs, pre-auth and a bar-ready POS: epaypos.net/bar-lounge  ·  Free statement review: epaypos.net/offers/statement-review  ·  947-228-7226 ext. 3", S["body"]),
]
row = 5
for text, st in lines:
    h.set(f"B{row}", text, st)
    if st == S["body"] and len(text) > 115: h.heights[row] = 30
    row += 1

# ---------- Pour Cost ----------
p = Sheet("Pour Cost", [30, 14, 14, 15, 13, 15, 13, 14, 13, 15], freeze=7)
p.set("A1", "Pour Cost", S["title"])
p.set("A2", "One row per bottle you pour from. Bottle size and pour size in ounces.", S["note"])
p.set("A4", "Your target pour cost %", S["label"]); p.set("C4", None, S["in_pct"])
p.set("D4", "Optional. Rows above it get flagged.", S["note"]); p.merges.append("D4:J4")
heads = ["Product", "Category", "Bottle size (oz)", "Bottle cost ($)", "Pour size (oz)", "Drink price ($)",
         "Pours per bottle", "Cost per pour ($)", "Pour cost %", "Profit per drink ($)"]
for i, t in enumerate(heads):
    p.set(f"{chr(65 + i)}6", t, S["header"])
p.heights[6] = 30
p.set("K6", "Over target?", S["header"])
p.widths.append(13)
first, last = 7, 46
for r in range(first, last + 1):
    if r == first:
        name, cat, size, cost, pour, price = "House vodka (example)", "Vodka", 33.8, 18.00, 1.5, 7.00
        p.set(f"A{r}", name, S["in_text"]); p.set(f"B{r}", cat, S["in_text"]); p.set(f"C{r}", size, S["in_num"])
        p.set(f"D{r}", cost, S["in_money"]); p.set(f"E{r}", pour, S["in_num"]); p.set(f"F{r}", price, S["in_money"])
        pours = size / pour; cpp = cost / size * pour; pc = cpp / price; prof = price - cpp
    else:
        for c, st in zip("ABCDEF", ["in_text", "in_text", "in_num", "in_money", "in_num", "in_money"]):
            p.set(f"{c}{r}", None, S[st])
        pours = cpp = pc = prof = 0
    p.set(f"G{r}", r2(pours), S["f_num"], f"IF(AND(ISNUMBER(E{r}),E{r}>0),C{r}/E{r},0)")
    p.set(f"H{r}", r2(cpp), S["f_money"], f"IF(AND(ISNUMBER(C{r}),C{r}>0),D{r}/C{r}*E{r},0)")
    p.set(f"I{r}", r2(pc), S["f_pct"], f"IF(AND(ISNUMBER(F{r}),F{r}>0),H{r}/F{r},0)")
    p.set(f"J{r}", r2(prof), S["f_money"], f"IF(AND(ISNUMBER(F{r}),F{r}>0),F{r}-H{r},0)")
    p.set(f"K{r}", "", S["f_money"], f'IF(AND(ISNUMBER($C$4),$C$4>0,I{r}>$C$4),"Over","")')
p.set(f"A{last + 2}", "Row 7 is an example with sample prices, not a recommendation. Replace it with your own.", S["note"])
p.merges.append(f"A{last + 2}:K{last + 2}")

# ---------- Inventory Count ----------
c = Sheet("Inventory Count", [30, 11, 13, 13, 13, 13, 15, 16, 17, 15], freeze=7)
c.set("A1", "Weekly Inventory Count", S["title"])
c.set("A2", "Count the same day and time every week. Sales per product come from your POS product sales report.", S["note"])
c.set("A4", "Week of", S["label"]); c.set("B4", None, S["in_text"]); c.merges.append("B4:C4"); c.set("C4", None, S["in_text"])
heads = ["Product", "Unit", "Opening count", "Received", "Closing count", "Used", "Cost per unit ($)",
         "Cost of what you used ($)", "Sales of this product ($)", "Real pour cost %"]
for i, t in enumerate(heads):
    c.set(f"{chr(65 + i)}6", t, S["header"])
c.heights[6] = 30
cf, cl = 7, 56
tot_cost = tot_sales = 0.0
for r in range(cf, cl + 1):
    if r == cf:
        c.set(f"A{r}", "House vodka (example)", S["in_text"]); c.set(f"B{r}", "1 L bottle", S["in_text"])
        c.set(f"C{r}", 6, S["in_num"]); c.set(f"D{r}", 6, S["in_num"]); c.set(f"E{r}", 7.5, S["in_num"])
        c.set(f"G{r}", 18.00, S["in_money"]); c.set(f"I{r}", 340.00, S["in_money"])
        used = 6 + 6 - 7.5; cost = used * 18.0; sales = 340.0; pct = cost / sales
    else:
        for col_, st in zip("ABCDEGI", ["in_text", "in_text", "in_num", "in_num", "in_num", "in_money", "in_money"]):
            c.set(f"{col_}{r}", None, S[st])
        used = cost = sales = pct = 0
    tot_cost += cost; tot_sales += sales
    c.set(f"F{r}", r2(used), S["f_num"], f"IF(COUNT(C{r}:E{r})=0,0,N(C{r})+N(D{r})-N(E{r}))")
    c.set(f"H{r}", r2(cost), S["f_money"], f"F{r}*N(G{r})")
    c.set(f"J{r}", r2(pct), S["f_pct"], f"IF(AND(ISNUMBER(I{r}),I{r}>0),H{r}/I{r},0)")
tr = cl + 2
c.set(f"G{tr}", "Totals", S["label"])
c.set(f"H{tr}", r2(tot_cost), S["total"], f"SUM(H{cf}:H{cl})")
c.set(f"I{tr}", r2(tot_sales), S["total"], f"SUM(I{cf}:I{cl})")
c.set(f"J{tr}", r2(tot_cost / tot_sales if tot_sales else 0), S["f_pct"], f"IF(I{tr}>0,H{tr}/I{tr},0)")
c.set(f"A{tr + 2}", "Row 7 is an example: 6 bottles on the shelf + 6 received − 7.5 left = 4.5 bottles used. Replace it with your own counts.", S["note"])
c.merges.append(f"A{tr + 2}:J{tr + 2}")

save(OUT, [h, p, c], "Bar Inventory & Pour Cost Calculator")
print(f"wrote {OUT}: example cost/pour ${18/33.8*1.5:.3f}, pour cost {18/33.8*1.5/7:.1%}; count used 4.5, real pour cost {4.5*18/340:.1%}")
