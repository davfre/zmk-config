# ZMK Config for Cradio Split Keyboard (nice!nano v2)

This repo contains the ZMK configuration for a split Cradio keyboard powered by two nice!nano v2 controllers. It supports [ZMK Studio](https://zmk.studio) for live keymap editing over USB, so you can make changes without rebuilding firmware — as long as the left side is flashed with Studio support.

*Last updated: 2025-06-09*

---

## 🧠 Setup Summary

### Physical Setup

* Split keyboard with two **nice!nano v2** microcontrollers.
* **Reset buttons not soldered**; bootloader entry is done via keybindings or shorting pins manually.

---

## 🔑 Keymap Features

* Home row mods (`&ht`)
* Tri-layer logic (`RGT + LFT ⇒ TRI`)
* Unicode support for Swedish and Danish characters
* `&bootloader` and `&sys_reset` mapped on the **tri\_layer**
* `&studio_unlock` temporarily mapped for ZMK Studio setup
* Keymap file used in build: `zmk/app/boards/shields/cradio/cradio.keymap`

---

## 💻 ZMK Studio Integration

ZMK Studio allows live keymap editing via USB (Chrome or native app). To support this:

* The **left half (central controller)** must be built with:

  * `studio-rpc-usb-uart` snippet
  * `CONFIG_ZMK_STUDIO=y`
  * `&studio_unlock` added to the keymap

Once enabled, open [https://zmk.studio](https://zmk.studio), press the `&studio_unlock` key, and edit your layout in real time.

---

## 📁 Folder Structure

```
zmk-config/
├── config/             ← your local overlay (optional)
├── zmk/                ← ZMK firmware source (contains `app/`)
├── zmk/app/boards/shields/cradio/cradio.keymap  ← active keymap file
├── zephyr/, modules/   ← auto-fetched by `west update`
├── build/              ← build outputs
├── firmware/           ← collected `.uf2` files for flashing
```

---

## 💠 Build Instructions

### 1. Initialize Workspace (only once)

```bash
west init -l config
west update
```

### 2. Export Zephyr SDK

Ensure the SDK is installed (see below), then run:

```bash
west zephyr-export
```

---

### 3. Ensure your keymap is in the correct path

ZMK will only use the keymap located at:

```
zmk/app/boards/shields/cradio/cradio.keymap
```

If you’ve been editing your keymap elsewhere (e.g., `config/cradio.keymap`), make sure to copy it before building:

```bash
cp config/cradio.keymap zmk/app/boards/shields/cradio/cradio.keymap
```

---

### 4. Build left half (Studio-enabled)

```bash
west build -s zmk/app -d build/cradio_left_studio -b nice_nano_v2 \
  -S studio-rpc-usb-uart -- -DSHIELD=cradio_left -DCONFIG_ZMK_STUDIO=y
```

### 5. Build right half (normal)

```bash
west build -s zmk/app -d build/cradio_right -b nice_nano_v2 \
  -- -DSHIELD=cradio_right
```

---

## 📦 Copy Firmware Files

```bash
mkdir -p firmware
cp build/cradio_left_studio/zephyr/zmk.uf2 firmware/left.uf2
cp build/cradio_right/zephyr/zmk.uf2       firmware/right.uf2
```

---

## 💾 Flashing Firmware

1. Put each half into **bootloader mode**:

   * Either double-tap the reset button (if installed)
   * Or press the key bound to `&bootloader` in the `tri_layer` layer
   * Or short the RST pads with tweezers/screwdriver (double-tap)

2. Then:

```bash
cp firmware/left.uf2 /Volumes/NICENANO       # left half
cp firmware/right.uf2 /Volumes/NICENANO1     # right half
```

> On macOS, use Finder or `ls /Volumes` to confirm mount names.
> If copying fails, try `cp -X` or use `rsync` to avoid metadata conflicts.

---

## 🚀 Using ZMK Studio

1. Go to [https://zmk.studio](https://zmk.studio) in Chrome or use the native app
2. Connect the **left half** via USB
3. Click “Connect” and press the `&studio_unlock` key
4. Edit layers and keybindings in real time
5. Use “Write to Device” to save changes
6. Avoid editing `.keymap` manually unless you use “Restore Stock Settings”

---

## 🪠 Toolchain Setup

### Dependencies

```bash
brew install dtc ninja
pip install west protobuf grpcio-tools
```

### Install Zephyr SDK

Download and install from:
👉 [https://github.com/zephyrproject-rtos/sdk-ng/releases](https://github.com/zephyrproject-rtos/sdk-ng/releases)

Common path: `/opt/zephyr-sdk`

Then run:

```bash
west zephyr-export
```

---

## 🛠️ Optional Build Script

Create a file called `build-all.sh`:

```bash
#!/bin/bash
set -e

echo "Building LEFT (Studio)..."
west build -s zmk/app -d build/cradio_left_studio -b nice_nano_v2 \
  -S studio-rpc-usb-uart -- -DSHIELD=cradio_left -DCONFIG_ZMK_STUDIO=y

echo "Building RIGHT..."
west build -s zmk/app -d
```
