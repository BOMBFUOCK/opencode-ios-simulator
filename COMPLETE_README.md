# iOS Simulator Skill

Unified CLI tool for iOS Simulator automation.

## Installation

```bash
# Install via pip
pip install --upgrade ios-simulator-skill

# Or install in development mode
pip install -e .
```

## Quick Start

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

### Device Lifecycle (6)
| Command | Description | Example |
|---------|-------------|---------|
| `sim list` | List simulators | `sim list --state booted` |
| `sim boot` | Boot simulator | `sim boot "iPhone 17 Pro"` |
| `sim shutdown` | Shutdown simulator | `sim shutdown` |
| `sim create` | Create simulator | `sim create "iPhone 17 Pro" --ios 26.3` |
| `sim delete` | Delete simulator | `sim delete --udid XXX --force` |
| `sim erase` | Erase simulator | `sim erase` |

### App Management (4)
| Command | Description | Example |
|---------|-------------|---------|
| `sim launch` | Launch app | `sim launch com.apple.Preferences` |
| `sim terminate` | Terminate app | `sim terminate com.apple.Preferences` |
| `sim install` | Install app | `sim install app.ipa` |
| `sim uninstall` | Uninstall app | `sim uninstall com.app` |

### Navigation & Interaction (5)
| Command | Description | Example |
|---------|-------------|---------|
| `sim map` | Map screen elements | `sim map` |
| `sim tree` | Accessibility tree | `sim tree` |
| `sim tap` | Tap element | `sim tap --text "General"` |
| `sim text` | Enter text | `sim text "hello"` |
| `sim swipe` | Swipe | `sim swipe up` |

### Advanced Interaction (2)
| Command | Description | Example |
|---------|-------------|---------|
| `sim key` | Press key | `sim key return` |
| `sim button` | Hardware button | `sim button home` |

### Testing & Analysis (4)
| Command | Description | Example |
|---------|-------------|---------|
| `sim audit` | Accessibility audit | `sim audit` |
| `sim diff` | Visual diff | `sim diff base.png curr.png` |
| `sim log` | Monitor logs | `sim log --app com.app` |
| `sim state` | Capture state | `sim state` |

### Permissions & Settings (4)
| Command | Description | Example |
|---------|-------------|---------|
| `sim privacy` | Manage permissions | `sim privacy --grant camera --bundle-id com.app` |
| `sim push` | Push notification | `sim push --title "Hi" --body "Hello"` |
| `sim clipboard` | Clipboard | `sim clipboard "text"` |
| `sim statusbar` | Status bar | `sim statusbar --get` |

### Build (2)
| Command | Description | Example |
|---------|-------------|---------|
| `sim build` | Build project | `sim build --project App.xcodeproj` |
| `sim test` | Run tests | `sim test --project App.xcodeproj` |

### Info (2)
| Command | Description | Example |
|---------|-------------|---------|
| `sim check` | Environment check | `sim check` |
| `sim booted` | Booted device | `sim booted` |

## JSON Output

All commands support `--json`:

```bash
sim list --json
# {"simulators": [...], "count": 11}

sim check --json
# {"ready": true, "checks": {...}}
```

## Dependencies

- macOS + Xcode
- idb-companion (`brew install idb-companion`)
- Python 3
- Pillow (for visual_diff)
