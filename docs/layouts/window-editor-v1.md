# Window And Editor Layer Plan

This is a proposed layout direction. It is not implemented in firmware yet.

## Goals

- Keep the base typing layout unchanged.
- Reduce mouse use on Windows 11 and WSL.
- Make PowerToys/FancyZones window movement easy enough to use reflexively.
- Add text cleanup commands for dictation and editing without overloading the existing arrow layer.
- Keep `TRI` focused on system/Bluetooth/firmware actions.

## Proposed Layers

- `WIN`: Windows 11, PowerToys/FancyZones, virtual desktops, monitor movement, app/window focus.
- `EDIT`: word movement, selection, deletion, undo/redo, clipboard actions.

## Why New Layers Instead Of More Modifiers

The current `RGT` layer already has arrows, so many commands are technically possible by combining `RGT` with modifiers:

```text
RGT + arrow
Ctrl + RGT + arrow
Shift + Ctrl + RGT + arrow
Win + RGT + arrow
Win + Ctrl + RGT + arrow
```

That is powerful, but it creates heavy chords and makes the same physical arrows mean cursor movement, word movement, selection, window snapping, monitor movement, and virtual desktop switching.

Dedicated layers make the intent explicit:

- `WIN`: steer windows and desktops.
- `EDIT`: clean up and restructure text.
- `RGT`: ordinary numbers and navigation.

## WIN Candidate

```text
Left hand                         Right hand
DeskL  Task   DeskR  NewDsk CloseD .      MonL   Max    MonR   .
PrevW  AltTab NextW  Close  SnapZ  .      ZoneL  Rest   ZoneR  .
.      .      .      .      .      .      .      Min    .      .

Thumbs:
.      .                          .      .
```

Possible bindings:

- `DeskL`: `Win+Ctrl+Left`
- `DeskR`: `Win+Ctrl+Right`
- `NewDsk`: `Win+Ctrl+D`
- `CloseD`: `Win+Ctrl+F4`
- `Task`: `Win+Tab`
- `PrevW`: `Alt+Shift+Tab`
- `AltTab` / `NextW`: `Alt+Tab`
- `Close`: `Alt+F4`
- `SnapZ`: `Win+Z`
- `ZoneL`: `Win+Left`
- `ZoneR`: `Win+Right`
- `Max`: `Win+Up`
- `Rest` / `Min`: `Win+Down`
- `MonL`: `Win+Shift+Left`
- `MonR`: `Win+Shift+Right`

## EDIT Candidate

```text
Left hand                         Right hand
Undo   Redo   Cut    Copy   Paste  .      Home   PgDn   PgUp   End
SelL   WordL  DelL   DelR   WordR  .      Left   Down   Up     Right
.      .      .      .      .      .      CHome  .      .      CEnd

Thumbs:
.      Esc                        .      .
```

Possible bindings:

- `WordL`: `Ctrl+Left`
- `WordR`: `Ctrl+Right`
- `SelL`: `Shift+Ctrl+Left`
- add `SelR` if a comfortable key is available.
- `DelL`: `Ctrl+Backspace`
- `DelR`: `Ctrl+Delete`
- `CHome`: `Ctrl+Home`
- `CEnd`: `Ctrl+End`
- `Undo`: `Ctrl+Z`
- `Redo`: `Ctrl+Y` or `Ctrl+Shift+Z`, depending on Windows/app preference.
- `Cut`: `Ctrl+X`
- `Copy`: `Ctrl+C`
- `Paste`: `Ctrl+V`

## Access Options To Decide

- Add one combo for `WIN`.
- Add one combo for `EDIT`.
- Reuse a noncritical transparent key on an existing layer.
- Use ZMK Studio first for a short trial if the needed bindings are supported there.

The first implementation should probably add only `WIN`. Add `EDIT` after the window workflow proves useful.
