# Full Adder &mdash; CMOS Layout in Glade

A one-bit **full adder** designed at the **transistor and layout level** in [Glade](http://www.peardrop.co.uk/glade/) using the **C5N 0.5 µm CMOS PDK**. The cell is built from a hand-laid library of CMOS gates (INV, NAND, NOR, AND, OR, XOR) that were each independently verified with **DRC** (design-rule check) and **LVS** (layout vs schematic) before being composed into the adder.

[![Tool](https://img.shields.io/badge/Layout-Glade-1E6FBA)](http://www.peardrop.co.uk/glade/)
[![PDK](https://img.shields.io/badge/PDK-C5N%200.5%CE%BCm-525252)](#)
[![Verification](https://img.shields.io/badge/LVS-Clean-2E8B57)](#verification-results)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Repository layout

The repo is organised in **three views** so different audiences can find what they need:

```
.
├── final report.docx       # written report (design choices, results, figures)
│
├── design/                 # CURATED, human-readable — read this if you don't have Glade
│   ├── inverter_{schematic,extracted}.cdl   inverter.lvs
│   ├── nand_{schematic,extracted}.cdl       nand.lvs
│   ├── nor_{schematic,extracted,layout}.cdl nor.lvs
│   ├── and_{schematic,extracted,layout}.cdl and.lvs
│   ├── or_{schematic,extracted,layout}.cdl  or.lvs
│   ├── xor_{schematic,extracted,layout}.cdl xor.lvs
│   └── full_adder_{schematic,extracted,layout}.cdl  full_adder.lvs
│
├── cellviews/              # FEATURED cells in raw Glade format (inverter + latch)
│   ├── inverter/{schematic,symbol,layout,extracted}
│   └── latch/{schematic,symbol,layout,extracted}
│
└── glade-project/          # FULL Glade working tree — open this if you have Glade
    ├── basic/              # base library (pins, vdd, vss, gnd, vcc)
    ├── tech/               # PDK iterations
    │   ├── ENGR3426/       #   - original course PDK + early gate work
    │   ├── ENGR3426_mod/   #   - modified PDK + main gate library and full adder
    │   ├── ENGR3426_mod1/  #   - alternative PDK variant
    │   └── FreePDK15/      #   - FreePDK 15nm files (additional exploration)
    ├── temp/               # Glade cell views (inv, latch)
    └── verifications/      # DRC and LVS report directories
```

### Which folder should I look at?

| If you are…                          | Open…                                  |
|---------------------------------------|----------------------------------------|
| A recruiter / curious reader          | `final report.docx` + `design/`        |
| A circuit designer who wants the netlists | `design/*.cdl` (open in any text editor) |
| Someone who has Glade installed        | `glade-project/` (point Glade at it)    |

> **Not included:** the Glade application binaries (`glade.exe`, `gemini.exe`, `fastcap.exe`), the embedded Python 2.7 runtime, the Qt DLLs, and the session log files. Glade is a proprietary EDA tool by Peardrop &mdash; download it for free for academic use at [peardrop.co.uk/glade](http://www.peardrop.co.uk/glade/) and drop the contents of `glade-project/` into a fresh Glade project root.

## Approach

1. **Build a standard-cell library bottom-up.** Each gate (INV → NAND → NOR → AND → OR → XOR) is drawn as a stick-diagram schematic, then promoted to a real layout view with proper well, contact, and metal layers matching the C5N PDK rules.
2. **Verify each cell independently** with DRC (design-rule check) and LVS against its schematic before reusing it.
3. **Compose the full adder** from the verified cells using the standard 2-XOR / 2-AND / 1-OR realisation:
   - `sum  = a XOR b XOR c_in`
   - `cout = (a AND b) OR (c_in AND (a XOR b))`
4. **Run LVS on the assembled adder** &mdash; the layout extracts to a netlist topologically equivalent to the schematic.

## File-type reference

| Extension | Meaning |
|-----------|---------|
| `*.cdl`   | SPICE-like circuit netlist (Calibre/Glade Description Language). Plain text. Open with any editor. |
| `*_schematic.cdl` | Netlist exported from the schematic view |
| `*_layout.cdl`    | Netlist written from the layout view |
| `*_extracted.cdl` | Netlist back-extracted from the layout (includes transistor sizes, S/D area & perimeter) |
| `*.lvs`   | LVS comparison report (Gemini engine, shipped with Glade) |
| `*.tch`   | Glade technology file (PDK definition) |
| `*.sub`   | SPICE subcircuit include file |
| `*.py`    | PDK device descriptions and DRC/LVS rule scripts |
| `cellviews/<cell>/{schematic,symbol,layout,extracted}` | Glade binary cell-view files |

## Verification results

The extracted full-adder layout reduces to **35 devices and 18 nets** that match the schematic netlist transistor-for-transistor (see [`design/full_adder.lvs`](design/full_adder.lvs)). Each constituent gate has its own clean LVS report.

| Cell        | Layout LVS report                       |
|-------------|-----------------------------------------|
| Inverter    | [`inverter.lvs`](design/inverter.lvs)   |
| NAND        | [`nand.lvs`](design/nand.lvs)           |
| NOR         | [`nor.lvs`](design/nor.lvs)             |
| AND         | [`and.lvs`](design/and.lvs)             |
| OR          | [`or.lvs`](design/or.lvs)               |
| XOR         | [`xor.lvs`](design/xor.lvs)             |
| **Full adder** | [`full_adder.lvs`](design/full_adder.lvs) |

## Reproducing in Glade

1. Install [Glade](http://www.peardrop.co.uk/glade/) (free for academic use).
2. Copy the contents of `glade-project/` into a fresh Glade workspace directory.
3. Launch Glade from that workspace &mdash; it will pick up the technology files in `tech/` and the cells in `basic/` and `temp/`.
4. Open any cell's `schematic` to inspect wiring or `layout` to inspect geometry.

## Course context

Built for ENGR3426 (Digital Electronics / VLSI Design) at PSUT. Demonstrates the full custom-layout flow on a textbook PDK: cell-library construction, hierarchical schematic/layout, DRC, LVS, and post-layout netlist extraction.

## Author

**Leen Almousa** &mdash; [github.com/leenalmousa](https://github.com/leenalmousa)

## License

Released under the [MIT License](LICENSE).
