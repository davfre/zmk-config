# Current Cradio Layout

Source: `../../config/cradio.keymap`

This is the generated human-readable reference for the currently active keymap. Regenerate it after keymap edits, especially after edits made through ZMK Studio.

Generated printable reference:

- `current-layout.html`
- `current-layout.svg`

Open `current-layout.html` in a browser for the printable view. Use browser print / save as PDF for a one-page PDF copy.

Regenerate all layout references with:

```bash
just layout-ref
```

## Compact Reference

```text
Access
  hold left thumb TAB  -> LFT symbols
  hold right thumb BSP -> RGT numbers/nav
  hold both LFT + RGT  -> TRI system

DEFAULT
  Q       W       F       P       B       | J       L       U       Y       ;
  A/SFT   R/ALT   S/CTL   T/GUI   G       | M       N/GUI   E/CTL   I/ALT   O/SFT
  Z       X       C       D       V       | K       H       ,       .       /
                          TAB/LFT ENTER   | SPACE   BSP/RGT

LFT symbols
  ~       .       {       }       Studio  | ^       (       )       [       ]
  @       !       #       $       %       | *       -       =       \       |
  Studio  .       .       .       .       | &       _       +       `       .
                          .       .       | .       .

RGT numbers/nav
  INS     1       2       3       .       | HOME    PGDN    PGUP    END     .
  DEL     4       5       6       .       | LEFT    DOWN    UP      RIGHT   :
  CAPS    7       8       9       0       | AE      OE      AA      A-um    O-um
                          .       ESC     | .       .

TRI system
  Reset   .       Studio  .       BT0     | .       .       .       .       Reset
  Boot    .       .       .       BT1     | .       .       .       .       Boot
  .       .       .       BTClr   BT2     | .       .       .       .       .
                          .       .       | .       .
```

Dots represent transparent keys.

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
  Q       W       F       P       B       | J       L       U       Y       ;
  A/SFT   R/ALT   S/CTL   T/GUI   G       | M       N/GUI   E/CTL   I/ALT   O/SFT
  Z       X       C       D       V       | K       H       ,       .       /
                          TAB/LFT ENTER   | SPACE   BSP/RGT
```

## RGT

```text
  INS     1       2       3       .       | HOME    PGDN    PGUP    END     .
  DEL     4       5       6       .       | LEFT    DOWN    UP      RIGHT   :
  CAPS    7       8       9       0       | AE      OE      AA      A-um    O-um
                          .       ESC     | .       .
```

## LFT

```text
  ~       .       {       }       Studio  | ^       (       )       [       ]
  @       !       #       $       %       | *       -       =       \       |
  Studio  .       .       .       .       | &       _       +       `       .
                          .       .       | .       .
```

## TRI

```text
  Reset   .       Studio  .       BT0     | .       .       .       .       Reset
  Boot    .       .       .       BT1     | .       .       .       .       Boot
  .       .       .       BTClr   BT2     | .       .       .       .       .
                          .       .       | .       .
```

Dots represent transparent keys.

## Notes

- Center labels come from `DEFAULT`.
- Top-left labels in the SVG are `LFT`.
- Top-right labels in the SVG are `RGT`.
- Top-center red labels in the SVG are `TRI`.
- Bottom-center labels in the SVG are held modifiers or held layers from `DEFAULT`.
