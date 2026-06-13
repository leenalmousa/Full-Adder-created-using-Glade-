# Full Adder &mdash; CMOS Layout in Glade

A one-bit **full adder** designed at the **transistor and layout level** in [Glade](http://www.peardrop.co.uk/glade/) using the **C5N 0.5 µm CMOS PDK**. Built bottom-up from a hand-laid library of CMOS gates (INV → AND → OR → XOR → adder), each verified with **DRC** and **LVS** before being composed into the next.

[![Tool](https://img.shields.io/badge/Layout-Glade-1E6FBA)](http://www.peardrop.co.uk/glade/)
[![PDK](https://img.shields.io/badge/PDK-C5N%200.5%CE%BCm-525252)](#)
[![Verification](https://img.shields.io/badge/LVS-Clean-2E8B57)](#verification-results)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## What's in here

One folder per circuit. Each folder contains the same set of files at three levels of abstraction, plus the LVS verification report.

```
.
├── final report.docx        # written report (design choices, results)
│
├── inverter/                # the basic CMOS inverter
│   ├── schematic.cdl
│   ├── extracted.cdl
│   └── lvs.txt
│
├── and/                     # 2-input AND gate
│   ├── schematic.cdl
│   ├── layout.cdl
│   ├── extracted.cdl
│   └── lvs.txt
│
├── or/                      # 2-input OR gate
│   ├── schematic.cdl
│   ├── layout.cdl
│   ├── extracted.cdl
│   └── lvs.txt
│
├── xor/                     # 2-input XOR gate
│   ├── schematic.cdl
│   ├── layout.cdl
│   ├── extracted.cdl
│   └── lvs.txt
│
└── full_adder/              # 1-bit full adder built from the gates above
    ├── schematic.cdl
    ├── layout.cdl
    ├── extracted.cdl
    └── lvs.txt
```

### What each file is

| File              | Description |
|-------------------|-------------|
| `schematic.cdl`   | SPICE-like netlist of the schematic view &mdash; the intent. |
| `layout.cdl`      | Netlist generated from the layout view &mdash; the geometry. |
| `extracted.cdl`   | Netlist back-extracted from the layout, including real transistor sizes and source/drain area & perimeter. |
| `lvs.txt`         | LVS (Layout vs. Schematic) report from the Gemini engine &mdash; should show a clean match. |

All `.cdl` and `.txt` files are plain text. Open them in any editor or directly on GitHub.

## Approach

1. **Build a standard-cell library bottom-up.** Start with the inverter, then compose larger gates from verified primitives.
2. **Verify each cell independently** with DRC and LVS against its schematic before reusing it.
3. **Compose the full adder** from the verified gates using the standard 2-XOR / 2-AND / 1-OR realisation:
   - `sum  = a XOR b XOR c_in`
   - `cout = (a AND b) OR (c_in AND (a XOR b))`
4. **Run LVS on the assembled adder** &mdash; the layout extracts to a netlist topologically equivalent to the schematic.

## Verification results

Every cell passes LVS &mdash; the layout extraction matches the schematic netlist transistor-for-transistor.

| Cell           | Devices (after reduction) | Report                                  |
|----------------|---------------------------|-----------------------------------------|
| Inverter       | 2                         | [`inverter/lvs.txt`](inverter/lvs.txt)  |
| AND            | 6                         | [`and/lvs.txt`](and/lvs.txt)            |
| OR             | 6                         | [`or/lvs.txt`](or/lvs.txt)              |
| XOR            | 12                        | [`xor/lvs.txt`](xor/lvs.txt)            |
| **Full adder** | **35**                    | [`full_adder/lvs.txt`](full_adder/lvs.txt) |

The full adder's extracted netlist contains **42 raw transistors** that reduce to **35** after series/parallel collapse, with **18 internal nets** matching the schematic.

## Course context

Built for ENGR3426 (Digital Electronics / VLSI Design) at PSUT. Demonstrates the full custom-layout flow on a textbook PDK: cell-library construction, hierarchical schematic/layout, DRC, LVS, and post-layout netlist extraction.

## Author

**Leen Almousa** &mdash; [github.com/leenalmousa](https://github.com/leenalmousa)

## License

Released under the [MIT License](LICENSE).
