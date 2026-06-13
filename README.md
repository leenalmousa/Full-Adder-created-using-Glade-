# Full Adder &mdash; CMOS Layout in Glade

A one-bit **CMOS full adder** designed at the **transistor and layout level** in [Glade](http://www.peardrop.co.uk/glade/) on the **C5N 0.5 µm PDK**. Built bottom-up from a hand-laid library of CMOS gates (INV → NAND/NOR → AND/OR/XOR → full adder), each verified with **DRC** (design-rule check) and **LVS** (layout-vs-schematic) before being composed into the next.

This repo is the **complete Glade workspace** &mdash; everything a fresh Glade installation needs to open and rerun the project. The Glade application itself is not included (you install it separately; it's free for academic use).

[![Tool](https://img.shields.io/badge/Layout-Glade-1E6FBA)](http://www.peardrop.co.uk/glade/)
[![PDK](https://img.shields.io/badge/PDK-C5N%200.5%CE%BCm-525252)](#)
[![Verification](https://img.shields.io/badge/LVS-Clean-2E8B57)](#verification)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## Table of contents

- [Repo layout](#repo-layout)
- [Quick start &mdash; running this on a fresh Glade install](#quick-start)
- [The cell library](#the-cell-library)
- [The PDK (`tech/`)](#the-pdk)
- [Design approach](#design-approach)
- [Verification](#verification)
- [License](#license)

## Repo layout

```
.
├── README.md
├── LICENSE
├── final report.docx        # written report (methodology, figures, results)
│
├── basic/                   # Glade base library (pins + supplies)
│   ├── glade.lib            # library index
│   ├── ipin/   opin/   iopin/
│   ├── vdd/    vss/    vcc/    gnd/
│
├── lib/                     # YOUR cell libraries
│   ├── default/             # an empty default workspace lib
│   ├── devices/             # generic NMOS / PMOS symbols
│   └── Training/            # ← all your work lives here
│       ├── glade.lib        # library index
│       ├── inverter schem/  inverter layout/
│       ├── NAND SCH/        NAND LAYOUT/
│       ├── NOR SCHEM/       nor/                # (nor has full views)
│       ├── AND SCHEM/       and sch/      AND layout/
│       ├── OR SCHEM/        OR LAYOUT/
│       ├── XOR SCHEM/       XOR LAYOUT/
│       ├── fulladder/       full adder/         # schematic + layout
│       ├── latch/                               # SR latch cell
│       ├── tap new in case/                     # standalone substrate-tap cell
│       ├── C5NNMOS/   C5NPMOS/                  # custom transistor cells
│       ├── grid/                                # alignment grid
│       └── ...                                  # plus Glade auto-saved revisions
│
├── tech/                    # PDKs (technology kits)
│   ├── ENGR3426/            # course-original C5N PDK
│   ├── ENGR3426_mod/        # ← main PDK (used for the full adder)
│   ├── ENGR3426_mod1/       # alternative PDK variant
│   └── FreePDK15/           # FreePDK 15 nm (additional exploration)
│
├── temp/                    # Glade scratch cells (inv, latch — earlier iterations)
│
└── verifications/           # output directories for DRC and LVS runs
    ├── drc/
    └── lvs/
```

> Each Glade cell folder (e.g. `lib/Training/inverter layout/`) contains binary view files named **`schematic`**, **`symbol`**, **`layout`**, and **`extracted`** &mdash; these are not text and only Glade can open them.

## Quick start

You will need Glade installed. This repo provides everything else.

### 1. Install Glade

Download from [peardrop.co.uk/glade](http://www.peardrop.co.uk/glade/). Free for academic use. Install for your OS (Windows, Linux, or macOS).

### 2. Clone this repo

```bash
git clone https://github.com/leenalmousa/Full-Adder-created-using-Glade-.git
cd Full-Adder-created-using-Glade-
```

The repo root is your **Glade workspace** &mdash; do not move it; Glade resolves relative paths from here.

### 3. Launch Glade with this workspace

Open a terminal in the repo root and launch Glade from there:

```bash
# Windows
"C:\Path\to\Glade\glade.exe"

# Linux / macOS
/path/to/glade
```

Glade uses the **current working directory** as the project root, so it will pick up `basic/glade.lib`, all libraries in `lib/`, and the technology kits in `tech/`.

### 4. Load the C5N technology

In Glade: **Technology → Load Technology File** → select `tech/ENGR3426_mod/C5N.tch`.

This activates the 0.5 µm C5N process with the layer table, design rules, and device extractor needed for everything else.

### 5. Open the cells

**File → Open Cellview** &mdash; pick a library and a cell:

| Library    | Cell                | What it is                                         |
|------------|---------------------|----------------------------------------------------|
| `Training` | `inverter schem`    | CMOS inverter (schematic)                          |
| `Training` | `inverter layout`   | CMOS inverter (transistor-level layout)            |
| `Training` | `NAND LAYOUT`       | 2-input NAND layout                                |
| `Training` | `NOR SCHEM` / `nor` | 2-input NOR schematic / layout                     |
| `Training` | `AND layout`        | 2-input AND layout                                 |
| `Training` | `OR LAYOUT`         | 2-input OR layout                                  |
| `Training` | `XOR LAYOUT`        | 2-input XOR layout                                 |
| `Training` | `full adder`        | **The 1-bit full adder layout**                    |
| `Training` | `fulladder`         | The full adder schematic                           |
| `Training` | `latch`             | SR latch                                           |
| `Training` | `tap new in case`   | Standalone well/substrate tap cell                 |

### 6. Re-run verification (optional)

To re-verify a cell after opening its layout:

- **DRC:** **Verify → DRC** &mdash; Glade runs `tech/ENGR3426_mod/C5N_DRC.py` and reports violations. Output lives in `verifications/drc/`.
- **LVS:** **Verify → LVS** &mdash; Glade extracts the layout via `tech/ENGR3426_mod/C5N_EXT_LVS.py`, then Gemini compares the result against the schematic. Output lives in `verifications/lvs/`.

Existing LVS reports from prior runs are in `tech/ENGR3426_mod/` as `*.lvs` files (e.g. `full adder.lvs`, `AND layout.lvs`).

## The cell library

The `lib/Training/` folder is the library that holds every cell I drew. Notable cells:

| Cell                | View(s)                           | Description |
|---------------------|-----------------------------------|-------------|
| `inverter schem`    | schematic                         | CMOS inverter at the transistor level |
| `inverter layout`   | layout, extracted                 | The hand-laid inverter — foundational cell of the library |
| `NAND SCH`          | schematic                         | 2-input NAND schematic |
| `NAND LAYOUT`       | layout, extracted                 | 2-input NAND layout |
| `NOR SCHEM`         | schematic                         | 2-input NOR schematic |
| `nor`               | schematic, layout, extracted      | 2-input NOR (full set of views) |
| `AND SCHEM` / `and sch` | schematic                     | 2-input AND schematic (= NAND + INV) |
| `AND layout`        | layout, extracted                 | 2-input AND layout |
| `OR SCHEM`          | schematic                         | 2-input OR schematic (= NOR + INV) |
| `OR LAYOUT`         | layout, extracted                 | 2-input OR layout |
| `XOR SCHEM`         | schematic                         | 2-input XOR schematic |
| `XOR LAYOUT`        | layout, extracted                 | 2-input XOR layout |
| `fulladder`         | schematic                         | 1-bit full adder schematic |
| `full adder`        | layout, extracted                 | **1-bit full adder layout** |
| `latch`             | schematic, layout, extracted      | SR latch |
| `tap new in case`   | layout                            | Standalone well/substrate tap cell |
| `C5NNMOS` / `C5NPMOS` | layout, netlist                 | Custom transistor cells |
| `grid`              | layout                            | Alignment grid (used while drawing) |

Glade also auto-saves revision copies named with `$$<number>` suffixes (e.g. `C5NPMOS$$2316608855`). These are kept for traceability.

## The PDK

Four technology kits ship with the workspace under `tech/`:

| Folder              | Use this for…                                                  |
|---------------------|----------------------------------------------------------------|
| **`ENGR3426_mod/`** | **Default. All gates and the full adder were built against this kit.** Contains the layer-stack file (`C5N.tch`), DRC rules (`C5N_DRC*.py`), extraction & LVS rules (`C5N_EXT_LVS.py`), and SPICE subcircuits (`engr3426.sub`). |
| `ENGR3426/`         | The course-original C5N PDK (earlier inverter work used this). |
| `ENGR3426_mod1/`    | An alternative PDK variant.                                    |
| `FreePDK15/`        | FreePDK 15 nm files used for additional exploration outside the main flow. |

## Design approach

1. **Build the cell library bottom-up.** Start with the inverter at the polygon level — well, diffusion, poly, metal, contacts. Verify DRC, then LVS against the schematic.
2. **Add NAND and NOR** as the next layer of primitives, reusing transistor sizes from the inverter.
3. **Compose AND / OR / XOR** from NAND/NOR + inverter, verifying each.
4. **Compose the full adder** from the verified gates using the standard 2-XOR / 2-AND / 1-OR realisation:
   ```
   sum  = a XOR b XOR c_in
   cout = (a AND b) OR (c_in AND (a XOR b))
   ```
5. **Substrate / well taps** are placed inside every cell so every transistor's body terminal is tied (NMOS body → gnd, PMOS body → VDD). A standalone tap cell (`tap new in case`) is also provided to drop extra ties wherever a larger design needs them.
6. **Run LVS on the assembled adder** &mdash; the layout extracts to a netlist topologically equivalent to the schematic.

## Verification

Every cell passes LVS clean &mdash; the layout extraction matches the schematic netlist transistor-for-transistor. Existing reports are stored alongside the netlists in `tech/ENGR3426_mod/`.

| Cell           | Devices (after reduction) | LVS report                                                       |
|----------------|---------------------------|------------------------------------------------------------------|
| Inverter       | 2                         | `tech/ENGR3426_mod/inverter layout .lvs`                         |
| NAND           | 4                         | `tech/ENGR3426_mod/NAND LAYOUT.lvs`                              |
| NOR            | 4                         | `tech/ENGR3426_mod/NOR LAYOUT NEW.lvs`                           |
| AND            | 6                         | `tech/ENGR3426_mod/AND layout.lvs`                               |
| OR             | 6                         | `tech/ENGR3426_mod/OR LAYOUT.lvs`                                |
| XOR            | 12                        | `tech/ENGR3426_mod/XOR LAYOUT.lvs`                               |
| **Full adder** | **35** (42 before reduction) | `tech/ENGR3426_mod/full adder.lvs`                            |

The full adder's extracted netlist contains 42 raw transistors that reduce to **35** after series/parallel collapse, with **18 internal nets** matching the schematic. Body terminals are tied for all 42 transistors (21 NMOS to `gnd`, 21 PMOS to `VDD`).

## What's *not* in this repo

- `glade.exe`, `gemini.exe`, `fastcap.exe`, `MetaPlacerTest0.exe` &mdash; the Glade application binaries. Install Glade yourself; it's free for academic use.
- The embedded Python 2.7 runtime and Qt DLLs that come bundled with Glade.
- Glade's HTML help docs and reference PDF.
- Session log files (`glade_*.log`) &mdash; personal noise from past editing sessions.

These exclusions are listed in `.gitignore`.

## Course context

Built for **ENGR3426 (Digital Electronics / VLSI Design)** at PSUT. Demonstrates the full custom-layout flow on a textbook PDK: cell-library construction, hierarchical schematic/layout, DRC, LVS, and post-layout netlist extraction.

## Author

**Leen Almousa** &mdash; [github.com/leenalmousa](https://github.com/leenalmousa)

## License

Released under the [MIT License](LICENSE).
