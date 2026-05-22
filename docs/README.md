# Keyboard Layout Docs

This directory keeps layout documentation separate from the buildable ZMK config.

## Structure

- `layouts/current-layout.md`: readable map of the currently active firmware.
- `layouts/window-editor-v1.md`: proposed Windows tiling and editor-navigation layer design.

## Repo Workflow

Keep `config/` as the only active ZMK config folder. Use JJ bookmarks for firmware alternatives instead of duplicating active-looking config directories.

Suggested bookmark names:

- `layout/main`: known-good current layout, equivalent to the main bookmark.
- `layout/window-v1`: adds a Windows/PowerToys layer only.
- `layout/window-editor-v1`: adds Windows/PowerToys and editor-navigation layers.

Before implementing an alternative, create a new JJ change/bookmark from the known-good layout, then edit `config/cradio.keymap` there.
