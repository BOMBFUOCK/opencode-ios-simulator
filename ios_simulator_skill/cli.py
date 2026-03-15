#!/usr/bin/env python3
"""
iOS Simulator Skill - CLI

Unified CLI for iOS Simulator automation.
Usage: sim <command> [options]
"""

import argparse
import json
import os
import subprocess
import sys
import time


def run_cmd(cmd, check=True, capture=True, input_str=None):
    """Execute command."""
    result = subprocess.run(
        cmd,
        shell=isinstance(cmd, str),
        capture_output=capture,
        text=True,
        input=input_str,
    )
    if check and result.returncode != 0:
        return None
    return result.stdout.strip() if capture else ""


# ============== Device Lifecycle ==============

def cmd_list(args, checks):
    """List simulators."""
    sims = run_cmd("xcrun simctl list devices available -j", check=False)
    if not sims:
        sims = run_cmd("xcrun simctl list devices available")
        print(sims or "No simulators")
        return
    
    try:
        data = json.loads(sims)
        devices = data.get("devices", {})
        sims_list = []
        for runtime, devs in devices.items():
            for dev in devs:
                sims_list.append({
                    "name": dev.get("name"),
                    "udid": dev.get("udid"),
                    "state": dev.get("state", "Shutdown"),
                })
    except:
        # Fallback to text parsing
        sims_list = []
        for line in sims.split("\n"):
            if "(" in line and ")" in line:
                name = line.split("(")[0].strip()
                udid = line.split("(")[1].split(")")[0].strip()
                state = "Booted" if "Booted" in line else "Shutdown"
                sims_list.append({"name": name, "udid": udid, "state": state})
    
    if args.state == "booted":
        sims_list = [s for s in sims_list if s["state"] == "Booted"]
    elif args.state == "available":
        sims_list = [s for s in sims_list if s["state"] == "Shutdown"]
    
    if args.json:
        print(json.dumps({"simulators": sims_list, "count": len(sims_list)}))
    else:
        print(f"Simulators ({len(sims_list)}):")
        for s in sims_list:
            print(f"  {s['name']} - {s['state']} - {s['udid']}")


def cmd_boot(args, checks):
    """Boot simulator."""
    target = args.device or "booted"
    result = run_cmd(f'xcrun simctl boot "{target}"', check=False)
    if result is None:
        print(f"Error: Failed to boot {target}", file=sys.stderr)
        sys.exit(1)
    print(f"Booted: {target}")


def cmd_shutdown(args, checks):
    """Shutdown simulator."""
    target = args.udid or "booted"
    run_cmd(f"xcrun simctl shutdown {target}")
    print(f"Shutdown: {target}")


def cmd_create(args, checks):
    """Create simulator."""
    device_type = args.device_type
    ios = args.ios or ""
    name = args.name or device_type
    
    cmd = f'xcrun simctl create "{name}" "{device_type}" {ios}'
    result = run_cmd(cmd, check=False)
    if result is None:
        print(f"Error: Failed to create simulator", file=sys.stderr)
        sys.exit(1)
    print(f"Created: {name}")


def cmd_delete(args, checks):
    """Delete simulator."""
    udid = args.udid
    if not udid:
        print("Error: --udid required", file=sys.stderr)
        sys.exit(1)
    
    if not args.force:
        print(f"Delete {udid}? Use --force to confirm.")
        sys.exit(1)
    
    run_cmd(f"xcrun simctl delete {udid}")
    print(f"Deleted: {udid}")


def cmd_erase(args, checks):
    """Erase simulator."""
    udid = args.udid or "booted"
    run_cmd(f"xcrun simctl erase {udid}")
    print(f"Erased: {udid}")


# ============== App Management ==============

def cmd_launch(args, checks):
    """Launch app."""
    bundle_id = args.bundle_id
    result = run_cmd(f"xcrun simctl launch booted {bundle_id}", check=False)
    if result is None:
        print(f"Error: Failed to launch {bundle_id}", file=sys.stderr)
        sys.exit(1)
    print(f"Launched: {bundle_id}")


def cmd_terminate(args, checks):
    """Terminate app."""
    bundle_id = args.bundle_id
    run_cmd(f"xcrun simctl terminate booted {bundle_id}")
    print(f"Terminated: {bundle_id}")


def cmd_install(args, checks):
    """Install app."""
    path = args.path
    result = run_cmd(f"xcrun simctl install booted '{path}'", check=False)
    if result is None:
        print(f"Error: Failed to install {path}", file=sys.stderr)
        sys.exit(1)
    print(f"Installed: {path}")


def cmd_uninstall(args, checks):
    """Uninstall app."""
    bundle_id = args.bundle_id
    run_cmd(f"xcrun simctl uninstall booted {bundle_id}")
    print(f"Uninstalled: {bundle_id}")


# ============== Navigation & Interaction ==============

def _get_accessibility_tree():
    """Get accessibility tree via idb."""
    result = run_cmd("idb ui describe-all --json", check=False)
    if not result:
        return None
    try:
        data = json.loads(result)
        return data[0] if isinstance(data, list) else data
    except:
        return None


def _flatten_tree(node, depth=0):
    """Flatten accessibility tree."""
    elements = [node]
    for child in node.get("children", []):
        elements.extend(_flatten_tree(child, depth + 1))
    return elements


def cmd_map(args, checks):
    """Map screen elements."""
    if not checks["idb"]:
        print("Error: IDB not available. Install: brew install idb-companion")
        sys.exit(1)
    
    tree = _get_accessibility_tree()
    if not tree:
        print("Error: Failed to get accessibility tree")
        sys.exit(1)
    
    flat = _flatten_tree(tree)
    interactive = [e for e in flat if e.get("type") in ["Button", "TextField", "Link", "Cell"]]
    
    if args.json:
        print(json.dumps({"total": len(flat), "interactive": interactive[:10]}))
    else:
        print(f"Interactive elements ({len(interactive)}):")
        for e in interactive[:10]:
            t = e.get("type", "?")
            l = e.get("AXLabel", "") or e.get("AXValue", "")
            print(f"  {t}: {l}")


def cmd_tree(args, checks):
    """Get accessibility tree."""
    if not checks["idb"]:
        print("Error: IDB not available")
        sys.exit(1)
    
    tree = _get_accessibility_tree()
    if not tree:
        print("Error: Failed to get tree")
        sys.exit(1)
    
    flat = _flatten_tree(tree)
    
    if args.json:
        print(json.dumps({"tree": tree, "elements": flat[:20]}))
    else:
        print(f"Screen elements ({len(flat)}):")
        for e in flat[:15]:
            t = e.get("type", "?")
            l = e.get("AXLabel", "")
            print(f"  {t}: {l}")


def cmd_tap(args, checks):
    """Tap element."""
    if not checks["idb"]:
        print("Error: IDB not available")
        sys.exit(1)
    
    tree = _get_accessibility_tree()
    flat = _flatten_tree(tree)
    
    matches = []
    for elem in flat:
        if not elem.get("enabled", True):
            continue
        if args.type and elem.get("type") != args.type:
            continue
        if args.id and elem.get("AXUniqueId") != args.id:
            continue
        if args.text:
            text = (elem.get("AXLabel") or "") + " " + (elem.get("AXValue") or "")
            if args.text.lower() not in text.lower():
                continue
        matches.append(elem)
    
    if not matches or args.index >= len(matches):
        print("Element not found")
        sys.exit(1)
    
    target = matches[args.index]
    frame = target.get("frame", {})
    x = int(frame.get("x", 0) + frame.get("width", 0) / 2)
    y = int(frame.get("y", 0) + frame.get("height", 0) / 2)
    
    run_cmd(f"idb ui tap {x} {y}", check=False)
    print(f"Tapped: {target.get('type')} at ({x}, {y})")


def cmd_text(args, checks):
    """Enter text."""
    if not checks["idb"]:
        print("Error: IDB not available")
        sys.exit(1)
    
    text = args.text
    run_cmd(f"idb ui text '{text}'", check=False)
    print(f"Entered: {text}")


def cmd_swipe(args, checks):
    """Swipe gesture."""
    if not checks["idb"]:
        print("Error: IDB not available")
        sys.exit(1)
    
    direction = args.direction
    tree = _get_accessibility_tree()
    frame = tree.get("frame", {}) if tree else {}
    w = int(frame.get("width", 390))
    h = int(frame.get("height", 844))
    
    dirs = {
        "up": ((w / 2, h * 0.8), (w / 2, h * 0.2)),
        "down": ((w / 2, h * 0.2), (w / 2, h * 0.8)),
        "left": ((w * 0.8, h / 2), (w * 0.2, h / 2)),
        "right": ((w * 0.2, h / 2), (w * 0.8, h / 2)),
    }
    
    start, end = dirs.get(direction, dirs["up"])
    run_cmd(
        f"idb ui swipe {int(start[0])} {int(start[1])} {int(end[0])} {int(end[1])}",
        check=False,
    )
    print(f"Swiped {direction}")


# ============== Advanced Interaction ==============

def cmd_key(args, checks):
    """Press key."""
    key = args.key
    key_codes = {
        "return": "40",
        "enter": "40",
        "delete": "42",
        "backspace": "42",
        "tab": "43",
        "space": "44",
        "escape": "41",
        "esc": "41",
        "up": "126",
        "down": "125",
        "left": "123",
        "right": "124",
    }
    
    code = key_codes.get(key.lower(), key)
    run_cmd(f"idb ui key {code}", check=False)
    print(f"Pressed: {key}")


def cmd_button(args, checks):
    """Press hardware button."""
    button = args.button
    
    if button == "home":
        run_cmd("idb ui key 3", check=False)
    elif button == "lock":
        run_cmd("idb ui key 16", check=False)
    elif button == "volumeup":
        run_cmd("idb ui key 0", check=False)
    elif button == "volumedown":
        run_cmd("idb ui key 1", check=False)
    elif button == "screenshot":
        name = f"/tmp/screenshot_{int(time.time())}.png"
        run_cmd(f"xcrun simctl io booted screenshot {name}", check=False)
        print(f"Screenshot: {name}")
        return
    
    print(f"Pressed: {button}")


# ============== Testing & Analysis ==============

def cmd_audit(args, checks):
    """Accessibility audit."""
    if not checks["idb"]:
        print("Error: IDB not available")
        sys.exit(1)
    
    tree = _get_accessibility_tree()
    flat = _flatten_tree(tree)
    
    issues = []
    for elem in flat:
        if elem.get("type") in ["Button", "Link"] and not elem.get("AXLabel"):
            issues.append(f"Missing label: {elem.get('type')}")
        if elem.get("type") == "Button" and not (
            elem.get("AXLabel") or elem.get("AXValue")
        ):
            issues.append("Empty button")
        frame = elem.get("frame", {})
        if frame.get("width", 0) < 44 or frame.get("height", 0) < 44:
            issues.append(f"Small target: {elem.get('type')}")
    
    if args.json:
        print(json.dumps({"issues": issues, "count": len(issues)}))
    else:
        print(f"Accessibility issues: {len(issues)}")
        for issue in issues[:10]:
            print(f"  - {issue}")


def cmd_diff(args, checks):
    """Visual diff."""
    baseline = args.baseline
    current = args.current
    
    try:
        from PIL import Image, ImageChops
    except ImportError:
        print("Error: Pillow not installed. Run: pip install pillow")
        sys.exit(1)
    
    try:
        b = Image.open(baseline)
        c = Image.open(current)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    if b.size != c.size:
        print(f"Size mismatch: {b.size} vs {c.size}")
        sys.exit(1)
    
    diff = ImageChops.difference(b, c)
    diff_ratio = sum(diff.getdata()) / (b.size[0] * b.size[1] * 255)
    
    if args.json:
        print(json.dumps({"diff_ratio": diff_ratio, "match": diff_ratio < 0.01}))
    else:
        print(f"Diff: {diff_ratio*100:.2f}%")
        print("Match: ✓" if diff_ratio < 0.01 else "Match: ✗")


def cmd_log(args, checks):
    """Monitor logs."""
    app = args.app or "*"
    duration = args.duration or "1"
    
    cmd = f"xcrun simctl spawn booted log show --predicate 'process == \"{app}\"' --last {duration}m"
    
    if args.errors_only:
        cmd += " --type error"
    
    result = run_cmd(cmd, check=False)
    
    if args.json:
        lines = result.split("\n") if result else []
        print(json.dumps({"logs": lines[-50:], "count": len(lines)}))
    else:
        print(result[-2000:] if result else "No logs")


def cmd_state(args, checks):
    """Capture app state."""
    udid = args.udid or "booted"
    
    screenshot = f"/tmp/state_{int(time.time())}_screen.png"
    run_cmd(f"xcrun simctl io {udid} screenshot {screenshot}")
    
    tree = ""
    if checks["idb"]:
        t = _get_accessibility_tree()
        if t:
            tree = json.dumps(t)[:500]
    
    print(f"State captured:")
    print(f"  Screenshot: {screenshot}")
    if tree:
        print(f"  Elements: {tree[:100]}...")


# ============== Permissions & Settings ==============

def cmd_privacy(args, checks):
    """Manage permissions."""
    bundle_id = args.bundle_id
    service = args.service
    action = "grant" if args.grant else "revoke"
    
    if not bundle_id or not service:
        print("Usage: sim privacy --bundle-id <id> --grant/--revoke <service>")
        print("Services: camera, microphone, location, contacts, photos, calendar,")
        print("          health, reminders, motion, keyboard, mediaLibrary, calls, siri")
        sys.exit(1)
    
    cmd = f"xcrun simctl privacy {action} {service} booted {bundle_id}"
    run_cmd(cmd, check=False)
    print(f"Permission {action}ed: {service} for {bundle_id}")


def cmd_push(args, checks):
    """Send push notification."""
    bundle_id = args.bundle_id or "booted"
    title = args.title or "Test"
    body = args.body or "Notification"
    
    payload = json.dumps({"aps": {"alert": {"title": title, "body": body}}})
    
    cmd = f"xcrun simctl push {bundle_id} -"
    result = run_cmd(cmd, check=False, input_str=payload)
    
    if result is not None:
        print(f"Push sent: {title}")
    else:
        print("Error: Failed to send push")


def cmd_clipboard(args, checks):
    """Set clipboard."""
    text = args.text
    run_cmd(f"xcrun simctl pbcopy booted '{text}'", check=False)
    print(f"Clipboard: {text[:30]}...")


def cmd_statusbar(args, checks):
    """Status bar."""
    if args.get:
        result = run_cmd("xcrun simctl status_bar booted get", check=False)
        print(result or "No data")
    else:
        print("Use: sim statusbar --get")


# ============== Build ==============

def cmd_build(args, checks):
    """Build Xcode project."""
    project = args.project
    workspace = args.workspace
    scheme = args.scheme
    config = args.config or "Debug"
    
    if not project and not workspace:
        print("Error: --project or --workspace required")
        sys.exit(1)
    
    target = workspace if workspace else project
    
    if workspace:
        cmd = f'xcodebuild -workspace "{workspace}"'
    else:
        cmd = f'xcodebuild -project "{project}"'
    
    if scheme:
        cmd += f" -scheme {scheme}"
    cmd += f" -configuration {config} -destination 'platform=iOS Simulator' build"
    
    print(f"Building: {target}...")
    result = run_cmd(cmd, check=False)
    
    if "BUILD SUCCEEDED" in (result or ""):
        print("Build: SUCCESS")
    else:
        print("Build: FAILED")


def cmd_test(args, checks):
    """Run tests."""
    project = args.project
    workspace = args.workspace
    scheme = args.scheme
    
    if not project and not workspace:
        print("Error: --project or --workspace required")
        sys.exit(1)
    
    if workspace:
        cmd = f'xcodebuild -workspace "{workspace}"'
    else:
        cmd = f'xcodebuild -project "{project}"'
    
    if scheme:
        cmd += f" -scheme {scheme}"
    cmd += " -destination 'platform=iOS Simulator' test"
    
    print("Running tests...")
    result = run_cmd(cmd, check=False)
    
    if "TEST SUCCEEDED" in (result or ""):
        print("Tests: PASSED")
    else:
        print("Tests: FAILED")


# ============== Info ==============

def cmd_check(args, checks):
    """Check environment."""
    if args.json:
        print(json.dumps({"ready": all(checks.values()), "checks": checks}))
    else:
        print("Environment:")
        for k, v in checks.items():
            print(f"  {'✓' if v else '✗'} {k}")


def cmd_booted(args, checks):
    """Get booted device."""
    result = run_cmd("xcrun simctl list devices booted -j", check=False)
    if not result:
        if args.json:
            print(json.dumps({"booted": False, "udid": None}))
        else:
            print("No device booted")
        return
    
    try:
        data = json.loads(result)
        devices = data.get("devices", {})
        for runtime, devs in devices.items():
            for dev in devs:
                if args.json:
                    print(json.dumps({"booted": True, "udid": dev.get("udid")}))
                else:
                    print(f"Booted: {dev.get('udid')}")
                return
    except:
        pass
    
    if args.json:
        print(json.dumps({"booted": False, "udid": None}))
    else:
        print("No device booted")


# ============== Main ==============

def main():
    # Check environment
    checks = {}
    checks["xcrun"] = run_cmd("xcrun --version", check=False) is not None
    checks["idb"] = run_cmd("idb list-targets", check=False) is not None
    
    result = run_cmd("xcrun simctl list devices booted -j", check=False)
    checks["booted"] = result is not None and "udid" in (result or "")
    
    parser = argparse.ArgumentParser(description="iOS Simulator Skill CLI", add_help=False)
    parser.add_argument("--json", action="store_true", help="JSON output")
    
    subparsers = parser.add_subparsers(dest="command", title="commands")
    
    # Device Lifecycle
    p = subparsers.add_parser("list", help="List simulators")
    p.add_argument("--state", choices=["booted", "available", "all"], default="all")
    
    p = subparsers.add_parser("boot", help="Boot simulator")
    p.add_argument("device", nargs="?", help="Device name or UDID")
    
    p = subparsers.add_parser("shutdown", help="Shutdown simulator")
    p.add_argument("--udid", help="Device UDID")
    
    p = subparsers.add_parser("create", help="Create simulator")
    p.add_argument("device_type", help="Device type (e.g., iPhone 17 Pro)")
    p.add_argument("--ios", help="iOS version")
    p.add_argument("--name", help="Custom name")
    
    p = subparsers.add_parser("delete", help="Delete simulator")
    p.add_argument("--udid", required=True, help="Device UDID")
    p.add_argument("--force", action="store_true", help="Skip confirmation")
    
    p = subparsers.add_parser("erase", help="Reset simulator")
    p.add_argument("--udid", help="Device UDID")
    
    # App Management
    p = subparsers.add_parser("launch", help="Launch app")
    p.add_argument("bundle_id", help="Bundle ID")
    
    p = subparsers.add_parser("terminate", help="Terminate app")
    p.add_argument("bundle_id", help="Bundle ID")
    
    p = subparsers.add_parser("install", help="Install app")
    p.add_argument("path", help="IPA file path")
    
    p = subparsers.add_parser("uninstall", help="Uninstall app")
    p.add_argument("bundle_id", help="Bundle ID")
    
    # Navigation
    p = subparsers.add_parser("map", help="Map screen elements")
    p = subparsers.add_parser("tree", help="Get accessibility tree")
    
    p = subparsers.add_parser("tap", help="Tap element")
    p.add_argument("--text", help="Text to find")
    p.add_argument("--type", help="Element type")
    p.add_argument("--id", help="Accessibility ID")
    p.add_argument("--index", type=int, default=0)
    
    p = subparsers.add_parser("text", help="Enter text")
    p.add_argument("text", help="Text")
    
    p = subparsers.add_parser("swipe", help="Swipe")
    p.add_argument("direction", choices=["up", "down", "left", "right"])
    
    # Advanced
    p = subparsers.add_parser("key", help="Press key")
    p.add_argument("key", help="Key name")
    
    p = subparsers.add_parser("button", help="Hardware button")
    p.add_argument("button", choices=["home", "lock", "volumeup", "volumedown", "screenshot"])
    
    # Testing
    p = subparsers.add_parser("audit", help="Accessibility audit")
    p = subparsers.add_parser("diff", help="Visual diff")
    p.add_argument("baseline", help="Baseline image")
    p.add_argument("current", help="Current image")
    
    p = subparsers.add_parser("log", help="Monitor logs")
    p.add_argument("--app", help="App bundle ID")
    p.add_argument("--duration", help="Duration (e.g., 1m)")
    p.add_argument("--errors_only", action="store_true", help="Errors only")
    
    p = subparsers.add_parser("state", help="Capture state")
    p.add_argument("--udid", help="Device UDID")
    
    # Permissions
    p = subparsers.add_parser("privacy", help="Manage permissions")
    p.add_argument("--bundle-id", help="Bundle ID")
    p.add_argument("--service", help="Service name")
    p.add_argument("--grant", action="store_true", help="Grant")
    p.add_argument("--revoke", action="store_true", help="Revoke")
    
    p = subparsers.add_parser("push", help="Send push")
    p.add_argument("--bundle-id", help="Bundle ID")
    p.add_argument("--title", help="Title")
    p.add_argument("--body", help="Body")
    
    p = subparsers.add_parser("clipboard", help="Set clipboard")
    p.add_argument("text", help="Text")
    
    p = subparsers.add_parser("statusbar", help="Status bar")
    p.add_argument("--get", action="store_true", help="Get status")
    
    # Build
    p = subparsers.add_parser("build", help="Build project")
    p.add_argument("--project", help="xcodeproj")
    p.add_argument("--workspace", help="xcworkspace")
    p.add_argument("--scheme", help="Scheme")
    p.add_argument("--config", help="Configuration")
    
    p = subparsers.add_parser("test", help="Run tests")
    p.add_argument("--project", help="xcodeproj")
    p.add_argument("--workspace", help="xcworkspace")
    p.add_argument("--scheme", help="Scheme")
    
    # Info
    p = subparsers.add_parser("check", help="Check environment")
    p = subparsers.add_parser("booted", help="Get booted device")
    
    args = parser.parse_args()
    
    if not args.command:
        print(__doc__)
        sys.exit(1)
    
    commands = {
        "list": cmd_list,
        "boot": cmd_boot,
        "shutdown": cmd_shutdown,
        "create": cmd_create,
        "delete": cmd_delete,
        "erase": cmd_erase,
        "launch": cmd_launch,
        "terminate": cmd_terminate,
        "install": cmd_install,
        "uninstall": cmd_uninstall,
        "map": cmd_map,
        "tree": cmd_tree,
        "tap": cmd_tap,
        "text": cmd_text,
        "swipe": cmd_swipe,
        "key": cmd_key,
        "button": cmd_button,
        "audit": cmd_audit,
        "diff": cmd_diff,
        "log": cmd_log,
        "state": cmd_state,
        "privacy": cmd_privacy,
        "push": cmd_push,
        "clipboard": cmd_clipboard,
        "statusbar": cmd_statusbar,
        "build": cmd_build,
        "test": cmd_test,
        "check": cmd_check,
        "booted": cmd_booted,
    }
    
    commands.get(args.command, lambda a, c: print(f"Unknown: {args.command}"))(args, checks)


if __name__ == "__main__":
    main()
