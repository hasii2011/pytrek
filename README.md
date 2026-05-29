![](https://github.com/hasii2011/code-ally-basic/blob/master/developer/agpl-license-web-badge-version-2-256x48.png "AGPL")

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/hasii2011/pytrek/tree/master.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/hasii2011/pytrek/tree/master)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Introduction
Written in Python 3 using the arcade library by [Humberto A. Sanchez II](https://www.linkedin.com/in/hasii/)

# PyTrek Project Description

`PyTrek` (specifically `PyTrekV2`) is a modern, graphical Python 3 reimagining of the classic **1975 text-based Star Trek game**, 
built using the **Arcade** 2D game library. It combines retro terminal-style gameplay mechanics with active graphical 
UI rendering, audio feedback, and structured system architecture.

---

## 🎮 Game Architecture & Design

The project uses a structured architecture to cleanly separate game logic, state, and user interface rendering:

### 1. **Model-View-Mediator Pattern**
To keep UI components decoupled from backend engines, the game leverages mediators under `src/pytrek/mediators/`:
* **`EnterpriseMediator`**: Coordinates states, shield levels, warp parameters, and sounds for the USS Enterprise.
* **`GalaxyMediator` & `GalaxyViewMediator`**: Manage scanned quadrants and render the 10x10 Galaxy Map overlay.
* **`LongRangeSensorScanMediator`**: Handles coordinates, calculations, and performance-optimized rendering of the adjacent 8-directional sensor scans.
* **`QuadrantMediator`**: Renders dynamic game pieces (Enterprise, Klingons, Star-bases, Stars, Planets) inside the local sector grid.

### 2. **Arcade UI Sections (Layout)**
The main interface (`src/pytrek/PyTrekV2.py`) is divided into distinct, modular visual zones using Arcade's `SectionManager`:
* **`QuadrantSection`**: Graphical view of the active quadrant grid (10x10 sectors).
* **`StatusConsoleSection`**: Right-hand panel displaying critical ship parameters (Stardate, Condition, Warp Factor, Energy, Shields, Torpedoes).
* **`MessageConsoleSection`**: Bottom output zone that displays warnings, combat results, and computer logs.
* **`CommandInputSection`**: Text input box that accepts keyboard commands, styled to override default OS themes with custom monospaced fonts and isolated focus outline parameters.

### 3. **Modal & Performance-Optimized Overlays**
Specialized views are drawn as toggleable sections or modal overlays:
* **`WarpEffectSection`**: Modal overlay that plays a custom sprite sheet particle warp animation with stereo audio effects when shifting quadrants.
* **`DeviceStatusSection`**: Table displaying damaged/functional device states, repair times, and repair progression.
* **`GalaxySection` & `LongRangeSensorScanSection`**: Visual overlays displaying galactic scan info.
  * *Optimization Note*: Renders use cached `arcade.Text` objects inside their mediators (such as the 2D grid in `GalaxyViewMediator`) to minimize dynamic texture rebuilds on every draw frame.

---

## 🛠️ Key Engine Components

* **`CommandHandler.py`**: Dispatches parsed commands to respective game engines (e.g. firing phasers, raising shields, warping, or shutting down/quitting the game).
* **`CommandParser.py`**: Parses complex text commands, handling short abbreviations (e.g., `M M .1` for manual sector moves or `M A 2 9` for autopilot jumps) and custom wayback coordinate formats (e.g., letter-number references).
* **`GameState.py`**: Manages runtime stats (current stardate, remaining time, Klingon count, score trackers, and game loop settings).
* **`GameSettings.py`**: Validates, deserializes, and loads game options (including visual configurations like the custom `viewDimRGBA` color representation).
* **`SoundMachine.py`**: Handles play state, channels, and volume controls for high-fidelity `.wav` game sound effects (warp sounds, shield hits, explosions).

---

## 🧪 Testing Suite
The project contains a comprehensive suite of **240 unit tests** (under `tests/`) covering:
* Game state serialization and parsing.
* Vector movement computations under warp/impulse drive.
* Sound and volume parameters.
* Target acquisition and phaser/torpedo hit mathematics.
