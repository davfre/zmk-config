# Current Cradio Layout

Source: `../../config/cradio.keymap`

This is the human-readable reference for the currently active keymap. It should be updated when `cradio.keymap` changes, especially after edits made through ZMK Studio.

## Layer Summary

- `DEFAULT`: typing, Colemak-style base, home-row mods.
- `RGT`: numbers, navigation, Scandinavian characters.
- `LFT`: symbols and ZMK Studio unlock.
- `TRI`: system, bootloader/reset, Bluetooth profile selection.
- `extra1`: reserved.
- `extra2`: reserved.

## Access

- Hold left thumb `TAB` for `LFT`.
- Hold right thumb `BSPC` for `RGT`.
- Hold both `LFT` and `RGT` for `TRI`.
- `extra1` and `extra2` are not reachable yet.

## DEFAULT

```text
Left hand                         Right hand
Q      W      F      P      B      J      L      U      Y      ;
A/SFT  R/ALT  S/CTL  T/GUI  G      M      N/GUI  E/CTL  I/ALT  O/SFT
Z      X      C      D      V      K      H      ,      .      /

Thumbs:
TAB/LFT    ENTER                  SPACE     BSPC/RGT
```

Home-row mod notes:

- Left home row holds: Shift, Alt, Ctrl, GUI.
- Right home row holds: GUI, Ctrl, Alt, Shift.

## RGT

```text
Left hand                         Right hand
INS    1      2      3      .      HOME   PGDN   PGUP   END    .
DEL    4      5      6      .      LEFT   DOWN   UP     RIGHT  :
CAPS   7      8      9      0      AE     OE     AA     A-UML  O-UML

Thumbs:
.      ESC                        .      .
```

Dots represent transparent keys.

## LFT

```text
Left hand                         Right hand
~      .      {      }      Studio ^      (      )      [      ]
@      !      #      $      %      *      -      =      \      |
Studio .      .      .      .      &      _      +      `      .

Thumbs:
.      .                          .      .
```

Dots represent transparent keys.

## TRI

```text
Left hand                         Right hand
Reset  .      Studio .      BT0    .      .      .      .      Reset
Boot   .      .      .      BT1    .      .      .      .      Boot
.      .      .      BTClear BT2   .      .      .      .      .

Thumbs:
.      .                          .      .
```

Dots represent transparent keys.

## Notes

- `&studio_unlock` is present on `LFT` and `TRI`.
- `cradio.conf` is currently empty.
- `HOST_OS` is set to `2` in `cradio.keymap` for Unicode helper behavior.
