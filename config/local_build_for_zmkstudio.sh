#!/bin/bash
set -e

echo "Building LEFT (with Studio)..."
west build -s zmk/app -d build/cradio_left_studio -b 'nice_nano//zmk' \
  -S studio-rpc-usb-uart -- -DSHIELD=cradio_left -DCONFIG_ZMK_STUDIO=y

echo "Building RIGHT..."
west build -s zmk/app -d build/cradio_right -b 'nice_nano//zmk' \
  -- -DSHIELD=cradio_right

echo "Copying .uf2 files to firmware/..."
mkdir -p firmware
cp build/cradio_left_studio/zephyr/zmk.uf2 firmware/left.uf2
cp build/cradio_right/zephyr/zmk.uf2       firmware/right.uf2

echo "Done. Flash via:"
echo "  cp firmware/left.uf2 /Volumes/NICENANO"
echo "  cp firmware/right.uf2 /Volumes/NICENANO1"
