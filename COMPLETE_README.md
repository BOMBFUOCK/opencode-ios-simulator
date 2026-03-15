# Opencode iOS Simulator

iOS 模拟器自动化 CLI 工具，专为 AI Agent 和自动化工作流设计。

## 安装

```bash
# 通过 pip 安装
pip install --upgrade opencode-ios-simulator

# 或开发模式安装
pip install -e .
```

## 快速开始

```bash
# 检查环境
sim check

# 列出模拟器
sim list

# 启动模拟器
sim boot "iPhone 17 Pro"

# 启动应用
sim launch com.apple.Preferences

# 映射屏幕元素
sim map

# 点击元素
sim tap --text "通用"

# 输入文本
sim text "hello"

# 滑动
sim swipe up
```

## 命令列表

### 设备生命周期 (6)
| 命令 | 说明 | 示例 |
|------|------|------|
| `sim list` | 列出模拟器 | `sim list --state booted` |
| `sim boot` | 启动模拟器 | `sim boot "iPhone 17 Pro"` |
| `sim shutdown` | 关闭模拟器 | `sim shutdown` |
| `sim create` | 创建模拟器 | `sim create "iPhone 17 Pro" --ios 26.3` |
| `sim delete` | 删除模拟器 | `sim delete --udid XXX --force` |
| `sim erase` | 重置模拟器 | `sim erase` |

### 应用管理 (4)
| 命令 | 说明 | 示例 |
|------|------|------|
| `sim launch` | 启动应用 | `sim launch com.apple.Preferences` |
| `sim terminate` | 终止应用 | `sim terminate com.apple.Preferences` |
| `sim install` | 安装应用 | `sim install app.ipa` |
| `sim uninstall` | 卸载应用 | `sim uninstall com.app` |

### 导航与交互 (5)
| 命令 | 说明 | 示例 |
|------|------|------|
| `sim map` | 映射屏幕元素 | `sim map` |
| `sim tree` | 无障碍树 | `sim tree` |
| `sim tap` | 点击元素 | `sim tap --text "通用"` |
| `sim text` | 输入文本 | `sim text "hello"` |
| `sim swipe` | 滑动 | `sim swipe up` |

### 高级交互 (2)
| 命令 | 说明 | 示例 |
|------|------|------|
| `sim key` | 按键 | `sim key return` |
| `sim button` | 硬件按钮 | `sim button home` |

### 测试与分析 (4)
| 命令 | 说明 | 示例 |
|------|------|------|
| `sim audit` | 无障碍审计 | `sim audit` |
| `sim diff` | 视觉对比 | `sim diff base.png curr.png` |
| `sim log` | 日志监控 | `sim log --app com.app` |
| `sim state` | 状态捕获 | `sim state` |

### 权限与设置 (4)
| 命令 | 说明 | 示例 |
|------|------|------|
| `sim privacy` | 权限管理 | `sim privacy --grant camera --bundle-id com.app` |
| `sim push` | 推送通知 | `sim push --title "Hi" --body "Hello"` |
| `sim clipboard` | 剪贴板 | `sim clipboard "text"` |
| `sim statusbar` | 状态栏 | `sim statusbar --get` |

### 构建 (2)
| 命令 | 说明 | 示例 |
|------|------|------|
| `sim build` | 构建项目 | `sim build --project App.xcodeproj` |
| `sim test` | 运行测试 | `sim test --project App.xcodeproj` |

### 信息 (2)
| 命令 | 说明 | 示例 |
|------|------|------|
| `sim check` | 环境检查 | `sim check` |
| `sim booted` | 已启动设备 | `sim booted` |

## JSON 输出

所有命令支持 `--json`：

```bash
sim list --json
# {"simulators": [...], "count": 11}

sim check --json
# {"ready": true, "checks": {...}}
```

## 依赖

- macOS + Xcode
- idb-companion (`brew install idb-companion`)
- Python 3.10+
- Pillow（用于视觉对比）
