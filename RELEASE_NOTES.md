# v0.1.1

Fix archive containment validation when the temporary/source path is reached through a system symlink (such as macOS /var). CI regression caught the discrepancy between macOS and Linux path resolution.

Initial offline persistent-undo inventory. Explicit Vim and Neovim directory paths, privacy-preserving counts/bytes and shared-directory warning, optional copy-only archive to a new destination. No editor execution or source modification. See README for limitations and archive verification guidance.
