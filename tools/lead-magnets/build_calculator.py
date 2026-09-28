#!/usr/bin/env python3
"""
Builds the Food Cost & Menu Pricing Calculator (.xlsx) with the standard
library only (no openpyxl on this Mac). Every formula also carries its
computed value, so previews show numbers; spreadsheet apps recalculate on open.

    python3 tools/lead-magnets/build_calculator.py <output.xlsx>
"""
import sys

OUT = sys.argv[1]

from xlsxlite import S, Sheet, col, r2, save

# ---------- Sheet 1: How to use ----------
h = Sheet("How to use", [4, 96])
h.set("B2", "EPAY POS  |  Food Cost & Menu Pricing Calculator", S["title"])
h.set("B3", "Work out what each plate costs you to make, then price it so every sale earns what you need.", S["note"])
lines = [
    ("How it works", S["sub"]),
    ("1.  Plate Cost tab: list the ingredients in one menu item. Enter what you pay for each (price and pack size) and how much goes on one plate. The tab adds up the plate cost.", S["body"]),
    ("2.  Menu Pricing tab: enter each item's plate cost and the food cost % you are aiming for. It suggests a menu price, then shows your real food cost % and profit per plate at the price you actually charge.", S["body"]),
    ("3.  Update the numbers whenever a supplier changes a price. Every total recalculates on its own.", S["body"]),
    ("", S["body"]),
    ("Which cells to edit", S["sub"]),
    ("Yellow cells with blue numbers are yours to fill in. White cells are formulas: leave them alone.", S["body"]),
    ("The first row on each tab is a filled-in example so you can see the format. Its numbers are examples only. Type over them or clear them.", S["body"]),
    ("", S["body"]),
    ("The formulas", S["sub"]),
    ("Cost per plate  =  purchase price  ÷  purchase quantity  ×  amount used on one plate", S["body"]),
    ("Suggested price  =  plate cost  ÷  target food cost %", S["body"]),
    ("Actual food cost %  =  plate cost  ÷  your menu price", S["body"]),
    ("Profit per plate (before labor and overhead)  =  your menu price  −  plate cost", S["body"]),
    ("", S["body"]),
    ("Your target food cost % is your call. It depends on your concept, your prices and your other costs, so set it from your own numbers.", S["note"]),
    ("", S["body"]),
    ("From EPAY POS", S["sub"]),
    ("Your processing fees come out of every one of these plates too. EPAY POS offers flat-rate processing at 2.3% + 5¢, or the Consumer Choice program with 0% processing. Get a free, line-by-line review of your current statement: epaypos.net/offers/statement-review  ·  947-228-7226 ext. 3", S["body"]),
]
row = 5
for text, st in lines:
    h.set(f"B{row}", text, st)
    if st == S["body"] and len(text) > 110: h.heights[row] = 30
    row += 1

# ---------- Sheet 2: Plate Cost ----------
p = Sheet("Plate Cost", [30, 18, 18, 12, 20, 18], freeze=7)
p.set("A1", "Plate Cost Builder", S["title"])
p.set("A2", "One menu item per copy of this tab. Right-click the tab > Duplicate to cost another item.", S["note"])
p.set("A4", "Menu item", S["label"]); p.set("B4", "Chicken sandwich (example)", S["in_text"]); p.merges.append("B4:C4"); p.set("C4", None, S["in_text"])
heads = ["Ingredient", "Purchase price ($)", "Purchase quantity", "Unit", "Amount per plate (same unit)", "Cost per plate ($)"]
for i, t in enumerate(heads, 1): p.set(f"{col(i)}6", t, S["header"])
p.heights[6] = 30
example = [("Chicken breast", 24.00, 10, "lb", 0.4), ("Brioche bun", 6.00, 12, "each", 1), ("Lettuce", 3.00, 24, "leaf", 2), ("Sauce", 12.00, 64, "oz", 1)]
first, last = 7, 26
total = 0.0
for r in range(first, last + 1):
    if r - first < len(example):
        name, price, qty, unit, used = example[r - first]
        p.set(f"A{r}", name, S["in_text"]); p.set(f"B{r}", price, S["in_money"]); p.set(f"C{r}", qty, S["in_num"])
        p.set(f"D{r}", unit, S["in_text"]); p.set(f"E{r}", used, S["in_num"])
        v = price / qty * used
    else:
        for c, st in zip("ABCDE", ["in_text", "in_money", "in_num", "in_text", "in_num"]): p.set(f"{c}{r}", None, S[st])
        v = 0
    total += v
    p.set(f"F{r}", r2(v), S["f_money"], f"IF(AND(ISNUMBER(C{r}),C{r}>0),B{r}/C{r}*E{r},0)")
p.set(f"E{last + 2}", "Plate cost", S["label"])
p.set(f"F{last + 2}", r2(total), S["total"], f"SUM(F{first}:F{last})")
p.set(f"A{last + 4}", "Example rows: typed-in sample prices to show the format, not real costs. Replace them with your own invoices.", S["note"])
p.merges.append(f"A{last + 4}:F{last + 4}")

# ---------- Sheet 3: Menu Pricing ----------
m = Sheet("Menu Pricing", [32, 16, 16, 17, 17, 17, 17], freeze=5)
m.set("A1", "Menu Pricing", S["title"])
m.set("A2", "Plate cost comes from the Plate Cost tab. The target food cost % is yours to choose.", S["note"])
heads = ["Menu item", "Plate cost ($)", "Target food cost %", "Suggested price ($)", "Your menu price ($)", "Actual food cost %", "Profit per plate ($)"]
for i, t in enumerate(heads, 1): m.set(f"{col(i)}4", t, S["header"])
m.heights[4] = 30
mfirst, mlast = 5, 34
for r in range(mfirst, mlast + 1):
    if r == mfirst:
        cost = total
        m.set(f"A{r}", "Chicken sandwich (example)", S["in_text"])
        m.set(f"B{r}", r2(cost), S["f_money"], "'Plate Cost'!F28")
        m.set(f"C{r}", 0.3, S["in_pct"]); m.set(f"E{r}", 6.50, S["in_money"])
        sug, price = cost / 0.3, 6.5
        act, prof = cost / price, price - cost
    else:
        m.set(f"A{r}", None, S["in_text"]); m.set(f"B{r}", None, S["in_money"])
        m.set(f"C{r}", None, S["in_pct"]); m.set(f"E{r}", None, S["in_money"])
        sug = act = prof = 0
    m.set(f"D{r}", r2(sug), S["f_money"], f"IF(AND(ISNUMBER(C{r}),C{r}>0),B{r}/C{r},0)")
    m.set(f"F{r}", r2(act), S["f_pct"], f"IF(AND(ISNUMBER(E{r}),E{r}>0),B{r}/E{r},0)")
    m.set(f"G{r}", r2(prof), S["f_money"], f"IF(AND(ISNUMBER(E{r}),E{r}>0),E{r}-B{r},0)")
m.set(f"A{mlast + 2}", "Row 5 is an example: its plate cost links to the Plate Cost tab, and its 30% target and $6.50 price are sample inputs, not recommendations. For your own items, type the plate cost straight into column B.", S["note"])
m.merges.append(f"A{mlast + 2}:G{mlast + 2}"); m.heights[mlast + 2] = 30

sheets = [h, p, m]

save(OUT, sheets, "Food Cost & Menu Pricing Calculator")
print(f"wrote {OUT}: plate cost example = ${total:.2f}")
