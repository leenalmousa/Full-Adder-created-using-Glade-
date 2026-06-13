# Full Adder &mdash; CMOS Layout in Glade

A one-bit **CMOS full adder** designed at the **transistor and layout level** in [Glade](http://www.peardrop.co.uk/glade/), built bottom-up from a hand-laid library of CMOS gates (INV → NAND/NOR → AND/OR/XOR → adder) on the **C5N 0.5 µm PDK**. Each cell was verified with **DRC** and **LVS** before being reused.

[![Tool](https://img.shields.io/badge/Layout-Glade-1E6FBA)](http://www.peardrop.co.uk/glade/)
[![PDK](https://img.shields.io/badge/PDK-C5N%200.5%CE%BCm-525252)](#)
[![Verification](https://img.shields.io/badge/LVS-Clean-2E8B57)](#verification-results)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## How to use this repo

The repo is laid out as a **Glade workspace** — clone it, point Glade at the root, and everything just works. The directory structure matches what Glade expects, with the application itself excluded (download it separately).

```
.
├── final report.docx          # written report (methodology, figures, results)
│
├── basic/                     # Glade base library (pins, supplies)
│   ├── glade.lib              # library index
│   ├── ipin/   opin/   iopin/ # input / output / bidirectional pins
│   └── vdd/    vss/   gnd/  vcc/  # supply / ground symbols
│
├── tech/                      # technology kits (PDKs)
│   ├── ENGR3426/              #   - course-original C5N PDK + early inverter work
│   ├── ENGR3426_mod/          #   - **main PDK** — gates + full adder netlists & LVS
│   ├── ENGR3426_mod1/         #   - alternative PDK variant
│   └── FreePDK15/             #   - FreePDK 15 nm files (exploration)
│
├── temp/                      # cell views (Glade binary format)
│   ├── inv/{schematic, symbol, layout, extracted}    # the inverter cell
│   └── latch/{schematic, symbol, layout, extracted}  # latch cell
│
└── verifications/             # DRC and LVS report directories
    ├── drc/
    └── lvs/
```

### Plugging this into Glade

1. Install Glade for your OS from [peardrop.co.uk/glade](http://www.peardrop.co.uk/glade/) (free for academic use).
2. Clone this repo and launch `glade.exe` from inside the repo root (or set the **working directory** to the repo root from Glade's launcher).
3. Glade will pick up:
   - `basic/glade.lib` as the base library,
   - `tech/ENGR3426_mod/C5N.tch` as the active technology,
   - the cells in `temp/` so you can open them under **File → Open Cellview**.
4. To re-run LVS on the full adder, point Gemini (Glade's LVS engine) at the `.cdl` netlists in `tech/ENGR3426_mod/` &mdash; the reports are next to them as `.lvs` files.

### Why the Glade application itself is excluded

`glade.exe`, `gemini.exe`, `fastcap.exe`, the bundled Python 2.7 runtime, the Qt DLLs, and the session log files are **not** in this repo &mdash; they are Peardrop's proprietary software and cannot legally be redistributed on GitHub. Get a free academic copy from peardrop.co.uk.

## Where each gate lives

Most of the design work for the adder is in **`tech/ENGR3426_mod/`**. File-name suffix conventions:

| Suffix             | Meaning                                                                  |
|--------------------|--------------------------------------------------------------------------|
| `*.cdl`            | SPICE-like netlist (Glade Description Language). Plain text.             |
| `* CDL.cdl` / `*_schematic.cdl` / `* final.cdl` | Netlist exported from the schematic view |
| `*_layout.cdl`     | Netlist generated from the layout view                                   |
| `*_extracted.cdl`  | Netlist back-extracted from the layout (real W/L, S/D area & perimeter)  |
| `*.lvs`            | LVS report from the Gemini engine (clean = layout matches schematic)     |
| `*.tch`            | Glade technology file (layer stack, design rules, extraction rules)      |
| `*.py`             | PDK device descriptions and DRC/LVS rule scripts                          |
| `*.sub`            | SPICE subcircuit include file                                            |

The inverter and latch additionally have **Glade cell-view binaries** (the unextensioned `schematic` / `symbol` / `layout` / `extracted` files in `temp/`).

## Verification results

Every cell passes LVS &mdash; the layout matches the schematic netlist transistor-for-transistor.

| Cell           | Devices (after reduction) | LVS report                                             |
|----------------|---------------------------|--------------------------------------------------------|
| Inverter       | 2                         | [`tech/ENGR3426_mod/inverter layout .lvs`](tech/ENGR3426_mod/) |
| NAND           | 4                         | [`tech/ENGR3426_mod/NAND LAYOUT.lvs`](tech/ENGR3426_mod/)       |
| NOR            | 4                         | [`tech/ENGR3426_mod/NOR LAYOUT NEW.lvs`](tech/ENGR3426_mod/)    |
| AND            | 6                         | [`tech/ENGR3426_mod/AND layout.lvs`](tech/ENGR3426_mod/)        |
| OR             | 6                         | [`tech/ENGR3426_mod/OR LAYOUT.lvs`](tech/ENGR3426_mod/)         |
| XOR            | 12                        | [`tech/ENGR3426_mod/XOR LAYOUT.lvs`](tech/ENGR3426_mod/)        |
| **Full adder** | **35** (42 before reduction) | [`tech/ENGR3426_mod/full adder.lvs`](tech/ENGR3426_mod/)    |

The full adder is composed from the verified gates using the standard realisation:

```
sum  = a XOR b XOR c_in
cout = (a AND b) OR (c_in AND (a XOR b))
```

## Course context

Built for **ENGR3426 (Digital Electronics / VLSI Design)** at PSUT. Demonstrates the full custom-layout flow on a textbook PDK: cell-library construction, hierarchical schematic/layout, DRC, LVS, and post-layout netlist extraction.

## Author

**Leen Almousa** &mdash; [github.com/leenalmousa](https://github.com/leenalmousa)

## License

Released under the [MIT License](LICENSE).
