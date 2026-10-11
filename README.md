# ForeverTracking

<p align="center"><img src="media/logo.png" width="160" alt="ForeverTracking radar logo"></p>

Keeps Find Herbs or Find Minerals tracking active across zoning, UI reloads,
death, and resurrection on the WoW Forever beta client.

## Behavior

- Remembers the last active tracking spell per character in `ForeverTrackingDB`.
- Restores that spell after entering the world, changing zones, dying, or
  resurrecting.
- On first use, selects Find Herbs when available, otherwise Find Minerals.
- Turning off herb/mineral tracking disables automatic restoration. Selecting
  either tracking spell again re-enables it.
- Does nothing when neither tracking spell is available.

The addon uses the locale-independent spell IDs 2383 (Find Herbs) and 2580
(Find Minerals), with the client's `C_Minimap` tracking API.

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
`CF_API_TOKEN` repository secret with an authorized CurseForge API token, then
push a `v*` semantic-version tag. BigWigs Packager creates the GitHub release
and uploads the addon to CurseForge. GitHub publishing uses the workflow's
`GITHUB_TOKEN`.

In game, test both professions: switch between Find Herbs and Find Minerals,
turn either off, then test zoning, reload, death, and resurrection. Turning off
tracking should remain off through those transitions.

The 512 × 512 `media/logo.png` is project artwork for CurseForge and is excluded
from the in-game addon package.

## License

MIT. See [LICENSE](LICENSE).
