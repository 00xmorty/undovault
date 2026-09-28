# UndoVault

A small offline, dependency-free Vim/Neovim persistent-undo directory inventory and opt-in copy archive. No automatic editor interrogation or configuration evaluation.

## Run

Python 3.9+ on macOS or Linux:

```sh
python3 undovault --vim-dir "$HOME/.vim/undodir" --nvim-dir "$HOME/.local/state/nvim/undo"
```

These paths are **examples**, not defaults: first inspect your editor's actual `:set undodir?` output and pass the corresponding existing directories. For multiple undodir entries, run separately for each directory. Exit 0 means inventory completed, not that undo history is valid.

To copy an archive into a **new** directory under an existing parent:

```sh
python3 undovault --vim-dir /your/vim/undo --nvim-dir /your/nvim/undo --archive-to /your/private/archive-2026-09-28
```

`--archive-to` is opt-in. It creates `vim/` and `nvim/` subfolders under the archive (including separate copies when both inputs point to the same directory). Existing destinations are refused. Verify the archive independently before changing editor settings. Source files are never deleted or changed. Tests: `python3 -m unittest discover -s tests -v`.

## Safety and limitations

- No sudo, telemetry, network calls, deletion, restore, editor execution, or configuration changes. Output includes counts/bytes and shared-directory flag only, never filenames or private paths.
- Symlinks in source trees are skipped, symlink input roots rejected; only regular files are copied. If a copy fails, a partial destination remains for manual inspection. This is **not** an atomic backup; stop editors and independently verify archive contents before migration.
- The scanner does not confirm an undo file is readable, complete, compatible, currently used, or at risk. The historical shared-undodir report does not prove a current Neovim bug or affect default installations.
- Source contents may contain private editing history. Keep archive private; do not publish it. A concurrent source change can invalidate a copy. Archive mode can use additional disk space.
