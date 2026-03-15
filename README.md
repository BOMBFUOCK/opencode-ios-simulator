# iOS Simulator Skill

iOS Simulator automation CLI tool.

## Installation

```bash
# Install via pip
pip install --upgrade ios-simulator-skill

# Or install in development mode
cd ios-simulator-opencode-skill
pip install -e .
```

## Usage

```bash
# Check environment
sim check

# List simulators
sim list

# Boot simulator
sim boot "iPhone 17 Pro"

# Launch app
sim launch com.apple.Preferences

# Map screen elements
sim map

# Tap element
sim tap --text "General"

# Enter text
sim text "hello"

# Swipe
sim swipe up
```

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list` | List simulators | `list --state booted` |
| `boot` | Boot simulator | `boot "iPhone 17 Pro"` |
| `shutdown` | Shutdown simulator | `shutdown --udid XXX` |
| `create` | Create simulator | `create "iPhone 17 Pro" --ios 26.3` |
| `delete` | Delete simulator | `delete --udid XXX --force` |
| `erase` | Erase simulator | `erase` |
| `launch` | Launch app | `launch com.example.app` |
| `terminate` | Terminate app | `terminate com.example.app` |
| `install` | Install app | `install app.ipa` |
| `uninstall` | Uninstall app | `uninstall com.app` |
| `map` | Map screen | `map` |
| `tree` | Accessibility tree | `tree --json` |
| `tap` | Tap element | `tap --text "Button"` |
| `text` | Enter text | `text "hello"` |
| `swipe` | Swipe gesture | `swipe up` |
| `key` | Press key | `key return` |
| `button` | Hardware button | `button home` |
| `audit` | Accessibility audit | `audit` |
| `diff` | Visual diff | `diff base.png curr.png` |
| `log` | Monitor logs | `log --app com.app` |
| `state` | Capture state | `state` |
| `privacy` | Manage permissions | `privacy --bundle-id com.app --grant camera` |
| `push` | Push notification | `push --title "Hi" --body "Hello"` |
| `clipboard` | Set clipboard | `clipboard "text"` |
| `statusbar` | Status bar | `statusbar --get` |
| `build` | Build project | `build --project App.xcodeproj` |
| `test` | Run tests | `test --project App.xcodeproj` |
| `check` | Check environment | `check` |
| `booted` | Get booted device | `booted` |

## JSON Output

All commands support `--json`:

```bash
sim list --json
# {"simulators": [...], "count": 10}

sim check --json
# {"ready": true, "checks": {...}}
```

## Dependencies

- macOS + Xcode
- idb-companion (`brew install idb-companion`)
- Python 3
- Pillow (for visual_diff)
