# Active ZMK Config

This folder is the active build input for the Cradio split keyboard.

## Files

- `cradio.keymap`: active keymap source.
- `cradio.conf`: active board/shield config overrides.
- `west.yml`: ZMK workspace manifest.
- `local_build_for_zmkstudio.sh`: local left/right firmware build helper.
- `sketching layout.md`: older scratchpad; useful history, but not canonical.
- `oakley-map.md`: external layout reference notes.

## Source Of Truth

Use `cradio.keymap` as the firmware source of truth.

Use `../docs/layouts/current-layout.md` as the human-readable reference generated from the current keymap.

Alternative layouts should be planned under `../docs/layouts/` and implemented on separate JJ bookmarks when they become real firmware variants.
