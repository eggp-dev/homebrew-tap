# Homebrew tap for Conn

[Conn](https://github.com/eggplantiny/conn) is a terminal you share with the AI agent you already use: it works in your shell, you approve what matters, and typing takes the keyboard back.

```sh
brew install --cask eggplantiny/tap/conn
```

Apple Silicon, macOS 12 or newer. The cask installs the signed and notarized DMG from Conn's GitHub releases and checks it against the SHA-256 published with that release. Conn updates itself from inside the app afterwards.

```sh
brew uninstall --cask conn          # your profiles, policy and activity record in ~/.conn stay
```

## How this tap stays current

`Casks/conn.rb` follows Conn's newest published release. A scheduled workflow runs `scripts/update_cask.py`, which reads the release list and that release's `SHA256SUMS` and commits the new version and checksum. Every change is then installed for real on a macOS runner: audit, install, signature and notarization check, version check, uninstall.

If Conn's repository moves, set `CONN_REPO` for the script and update the two addresses in the cask.
