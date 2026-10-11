# Forever Tracking

<p align="center"><img src="media/logo.png" width="160" alt="Forever Tracking radar logo"></p>

**Track herbs or minerals - not the toggle.**

Forever Tracking remembers your active **Find Herbs** or **Find Minerals**
choice and brings it back after a login, UI reload, zone change, or resurrection.
Turn tracking off whenever you like; it stays off until you select either one
again.

## Features

- **Remembers your pick:** Saves the last active tracking spell per character.
- **Handles the interruptions:** Restores it after login, reloads, zoning,
  death, and resurrection.
- **Respects your choice:** Turning tracking off pauses automatic restores;
  selecting Find Herbs or Find Minerals again resumes them.
- **Works in any language:** Identifies spells by ID, not translated names.
- **Stays lightweight:** No settings, slash commands, or dependencies. Does
  nothing if neither tracking ability is available.

## How to use it

Enable the addon and play as usual. On first use, it selects Find Herbs when
available, otherwise Find Minerals. After that, it remembers whichever
supported tracking spell you use.

## Installation

Download a release from
[GitHub Releases](https://github.com/psykzz/wow-forever-tracking/releases) and
extract the `ForeverTracking` folder into
`World of Warcraft\_classic_beta_\Interface\AddOns`. Enable **Forever
Tracking** in the AddOns list.

For development, copy the `ForeverTracking` folder from this repository into
the AddOns directory.

## Development

The addon targets the WoW Forever beta client, interface `16001`. Validate
Lua 5.1 syntax and lint with:

```powershell
luac5.1 -p ForeverTracking.lua
luacheck ForeverTracking.lua
```

GitHub Actions runs these checks on pushes to `main` and pull requests. To
publish a release to CurseForge project `1738956`, configure the
`CURSEFORGE_API_TOKEN` repository secret with an authorized CurseForge API
token, then push a `v*` semantic-version tag. BigWigs Packager creates the
GitHub release and uploads the addon to CurseForge. The workflow maps that
secret to the `CF_API_TOKEN` variable expected by the packager. GitHub
publishing uses the workflow's `GITHUB_TOKEN`.

In game, test both professions: switch between Find Herbs and Find Minerals,
turn either off, then test zoning, reload, death, and resurrection. Turning off
tracking should remain off through those transitions.

The 512 × 512 `media/logo.png` is project artwork for CurseForge and is excluded
from the in-game addon package.

## License

MIT. See [LICENSE](LICENSE).
