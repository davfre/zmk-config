set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

default:
    @just --list

status:
    jj status

diff-stat:
    jj diff --stat

diff:
    jj diff --git

hunk:
    hunk diff

init:
    west init -l config
    west update

west-update:
    west update

zephyr-export:
    west zephyr-export

_build-left:
    west build -s zmk/app -d build/cradio_left_studio -b nice_nano_v2 \
      -S studio-rpc-usb-uart -- -DSHIELD=cradio_left -DCONFIG_ZMK_STUDIO=y

_build-right:
    west build -s zmk/app -d build/cradio_right -b nice_nano_v2 \
      -- -DSHIELD=cradio_right

build: _build-left _build-right _collect-firmware

_collect-firmware:
    mkdir -p firmware
    cp build/cradio_left_studio/zephyr/zmk.uf2 firmware/left.uf2
    cp build/cradio_right/zephyr/zmk.uf2 firmware/right.uf2
    ls -lh firmware/left.uf2 firmware/right.uf2

flash-left mount="/Volumes/NICENANO":
    test -d "{{mount}}" || (echo "Mount not found: {{mount}}" >&2; exit 1)
    printf "Put LEFT half into bootloader mode mounted at %s, then press Enter." "{{mount}}"
    read _
    cp firmware/left.uf2 "{{mount}}/"

flash-right mount="/Volumes/NICENANO1":
    test -d "{{mount}}" || (echo "Mount not found: {{mount}}" >&2; exit 1)
    printf "Put RIGHT half into bootloader mode mounted at %s, then press Enter." "{{mount}}"
    read _
    cp firmware/right.uf2 "{{mount}}/"
