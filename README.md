# Full Adder &mdash; CMOS Layout in Glade

A one-bit **CMOS full adder** designed at the **transistor and layout level** in [Glade](http://www.peardrop.co.uk/glade/) using the **C5N 0.5 µm PDK**. Built bottom-up: hand-laid CMOS gates (INV → NAND/NOR → AND/OR/XOR → adder), each verified with **DRC** and **LVS** before being composed into the next.

[![Tool](https://img.shields.io/badge/Layout-Glade-1E6FBA)](http://www.peardrop.co.uk/glade/)
[![PDK](https://img.shields.io/badge/PDK-C5N%200.5%CE%BCm-525252)](#)
[![Verification](https://img.shields.io/badge/LVS-Clean-2E8B57)](#verification-results)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## What's in here

One folder per gate I built, each containing the same set of files:

```
.
├── final report.docx          # written report
│
├── inverter/                  # the CMOS inverter (foundational cell)
│   ├── schematic.cdl
│   ├── extracted.cdl
│   └── lvs.txt
│
├── nand/                      # 2-input NAND
├── nor/                       # 2-input NOR
├── and/                       # 2-input AND   (= NAND + INV)
├── or/                        # 2-input OR    (= NOR  + INV)
├── xor/                       # 2-input XOR
├── full_adder/                # 1-bit full adder built from the above
├── tap/                       # standalone well/substrate tap cell
└── latch/                     # SR latch (Glade cell views only — no netlist)
```

Inside every gate folder you also get a **`glade_cellview/`** subfolder &mdash; the actual Glade binary cell-view files (`schematic`, `layout`, `extracted`) carrying the layout polygons. Open them in Glade to see / edit the geometry. They are not viewable on GitHub.

Each gate folder contains:

| File              | What it is |
|-------------------|------------|
| `schematic.cdl`   | SPICE-like netlist of the schematic view &mdash; the intent. |
| `layout.cdl`      | Netlist generated from the layout view &mdash; the geometry. |
| `extracted.cdl`   | Netlist back-extracted from the layout (real transistor sizes, source/drain area & perimeter). |
| `lvs.txt`         | LVS (Layout vs. Schematic) report &mdash; clean means the layout matches the schematic. |

All files in the gate folders are plain text. Open in any editor or directly on GitHub.

The **`latch/`** folder is different &mdash; it contains four **Glade binary cell-view files** (`schematic`, `symbol`, `layout`, `extracted`) with no extensions. These can only be opened in Glade, not viewed on GitHub.

## Approach

1. **Start with the inverter.** Hand-lay the polygons (well, diffusion, poly, metal, contacts), verify DRC, then verify LVS against the schematic.
2. **Build NAND / NOR** as the next layer of primitives.
3. **Compose AND / OR / XOR** from those primitives, verifying each.
4. **Compose the full adder** from the verified gates using the standard realisation:
   - `sum  = a XOR b XOR c_in`
   - `cout = (a AND b) OR (c_in AND (a XOR b))`
5. **Run LVS on the assembled adder** &mdash; the extracted layout reduces to a netlist matching the schematic transistor-for-transistor.

## Verification results

Every cell passes LVS clean &mdash; the layout extraction matches the schematic netlist transistor-for-transistor.

| Cell           | Devices (after reduction) | LVS report                                |
|----------------|---------------------------|-------------------------------------------|
| Inverter       | 2                         | [`inverter/lvs.txt`](inverter/lvs.txt)    |
| NAND           | 4                         | [`nand/lvs.txt`](nand/lvs.txt)            |
| NOR            | 4                         | [`nor/lvs.txt`](nor/lvs.txt)              |
| AND            | 6                         | [`and/lvs.txt`](and/lvs.txt)              |
| OR             | 6                         | [`or/lvs.txt`](or/lvs.txt)                |
| XOR            | 12                        | [`xor/lvs.txt`](xor/lvs.txt)              |
| **Full adder** | **35** (42 before reduction) | [`full_adder/lvs.txt`](full_adder/lvs.txt) |

The full adder's extracted netlist reduces to **35 devices** with **18 internal nets** matching the schematic.

## Course context

Built for **ENGR3426 (Digital Electronics / VLSI Design)** at PSUT. Demonstrates the full custom-layout flow on a textbook PDK: cell-library construction, hierarchical schematic/layout, DRC, LVS, and post-layout netlist extraction.

## Author

**Leen Almousa** &mdash; [github.com/leenalmousa](https://github.com/leenalmousa)

## License

Released under the [MIT License](LICENSE).
