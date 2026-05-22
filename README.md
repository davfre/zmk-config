# ZMK Config for Cradio Split Keyboard

This repo contains the ZMK user config for a split Cradio/Ferris Sweep style keyboard powered by two `nice_nano_v2` controllers. The left half is built with [ZMK Studio](https://zmk.studio) support.

## Hardware

- Split Cradio keyboard.
- Two `nice_nano_v2` microcontrollers.
- Reset buttons are not soldered; bootloader entry is done with keybindings or by shorting reset pads.

## Active Config

- `config/cradio.keymap`: active keymap source; defines layers and what each key does.
- `config/cradio.conf`: active config overrides; changes firmware settings from their defaults.
- `config/west.yml`: ZMK workspace manifest; tells West which source repos and modules to fetch.
- `build.yaml`: GitHub Actions build matrix.
- `config/README.md`: notes about the active config folder.
- `docs/layouts/current-layout.md`: human-readable current layout reference.
- `docs/layouts/window-editor-v1.md`: proposed Windows/editor layer plan.

Keep `config/` as the only active ZMK config folder. Use JJ bookmarks for alternative firmware variants instead of duplicating buildable config directories.

## Keymap Features

- Home-row mods using `&ht`.
- Tri-layer logic: `RGT + LFT => TRI`.
- Unicode support for Swedish and Danish characters.
- `&bootloader` and `&sys_reset` on the `TRI` layer.
- `&studio_unlock` mapped for ZMK Studio setup.

## ZMK Studio

The left half is the central controller and must be built with:

- `studio-rpc-usb-uart` snippet.
- `CONFIG_ZMK_STUDIO=y`.
- `&studio_unlock` in the keymap.

Once enabled, open [ZMK Studio](https://zmk.studio), connect the left half over USB, press the `&studio_unlock` key, and edit the layout.

## Repo Layout

```text
zmk-config/
├── build.yaml
├── config/             # active ZMK config
├── docs/               # layout plans and references
├── zmk/                # fetched by west update
├── zephyr/, modules/   # fetched by west update
├── build/              # local build outputs
└── firmware/           # collected .uf2 files
```

## Build

```bash
just                 # list recipes
just init            # first checkout only: west init -l config; west update
just zephyr-export   # after installing the Zephyr SDK
just build           # build both halves and collect firmware
```

`just build` builds both halves. The left/central half is built with ZMK Studio enabled. Use `just west-update` to update fetched dependencies after the workspace has been initialized.

## Firmware

`just build` writes the flashable firmware files to `firmware/left.uf2` and `firmware/right.uf2`.

To flash, put the target half into bootloader mode:

- Press the key bound to `&bootloader` on the `TRI` layer.
- Or short the reset pads manually.
- Or double-tap reset if reset buttons are later installed.

Then run:

```bash
just flash-left
just flash-right
```

Each flash recipe prompts before copying firmware. The default mount paths are `/Volumes/NICENANO` and `/Volumes/NICENANO1`.

Pass a mount path if your host uses a different one:

```bash
just flash-left /mnt/d
just flash-right /mnt/e
```

> On macOS, use Finder or `ls /Volumes` to confirm mount names.
> If copying fails, try `cp -X` or use `rsync` to avoid metadata conflicts.

## Using ZMK Studio

1. Go to [https://zmk.studio](https://zmk.studio) in Chrome or use the native app
2. Connect the **left half** via USB
3. Click “Connect” and press the `&studio_unlock` key
4. Edit layers and keybindings in real time
5. Use “Write to Device” to save changes
6. Avoid editing `.keymap` manually unless you use “Restore Stock Settings”

ZMK Studio is the preferred path for quick layout experiments. Rebuild and flash firmware when changing firmware structure, such as adding new layers, combos, conditionals, or behaviors.

## JJ Workflow

This repo is managed with Jujutsu (`jj`) on top of Git.

Useful review commands:

```bash
just status
just diff-stat
just diff
just hunk
jj show @
```

Use bookmarks for alternative layout variants, for example:

```text
main
layout/window-v1
layout/window-editor-v1
```

Do not move to a new JJ change until the current diff has been reviewed.

## Toolchain Setup

### Dependencies

```bash
brew install dtc ninja just
pip install west protobuf grpcio-tools
```

### Install Zephyr SDK

Download and install from:
👉 [https://github.com/zephyrproject-rtos/sdk-ng/releases](https://github.com/zephyrproject-rtos/sdk-ng/releases)

Common path: `/opt/zephyr-sdk`

Then run:

```bash
just zephyr-export
```

## Just Recipes

The root `justfile` contains:

```text
status            # jj status
diff-stat         # jj diff --stat
diff              # jj diff --git
hunk              # hunk diff
init              # west init -l config; west update
west-update       # west update
zephyr-export     # west zephyr-export
build             # build both halves and collect firmware
flash-left        # prompt, then copy left.uf2 to mount
flash-right       # prompt, then copy right.uf2 to mount
```
