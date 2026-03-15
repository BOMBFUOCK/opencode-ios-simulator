# Opencode iOS Simulator

iOS 模拟器自动化 CLI 工具，专为 AI Agent 和自动化工作流设计。

## 项目简介

Opencode iOS Simulator 是一个功能强大的命令行工具，用于自动化控制 iOS 模拟器。它提供了丰富的命令集，支持设备生命周期管理、应用安装与启动、屏幕交互、无障碍测试等功能。

该工具特别设计用于：
- **AI Agent 自动化**：为 AI 代理提供可靠的 iOS 模拟器控制能力
- **自动化测试**：简化 iOS 应用的测试流程
- **CI/CD 集成**：支持在持续集成环境中运行
- **开发调试**：帮助开发者快速调试 iOS 应用

## 功能特性

### 设备管理
- 列出、创建、删除模拟器
- 启动、关闭、重置模拟器
- 多设备状态管理

### 应用管理
- 安装 IPA 应用
- 启动、终止应用
- 卸载应用

### 屏幕交互
- 映射屏幕元素（Accessibility Tree）
- 点击指定元素
- 输入文本
- 滑动操作（上、下、左、右）
- 硬件按钮模拟（Home、Power 等）
- 按键模拟

### 测试与分析
- 无障碍审计
- 视觉差异对比
- 应用日志监控
- 状态捕获

### 权限与设置
- 权限管理（相机、麦克风、位置等）
- 推送通知模拟
- 剪贴板操作
- 状态栏控制

### 构建与测试
- Xcode 项目构建
- 单元测试运行

## 安装

### 环境要求

- macOS 操作系统
- Xcode（已安装命令行工具）
- Python 3.10+
- idb-companion

### 安装步骤

1. **安装 idb-companion**（必需）：

```bash
brew install idb-companion
```

2. **安装 opencode-ios-simulator**：

```bash
# 通过 pip 安装
pip install --upgrade opencode-ios-simulator

# 或开发模式安装
pip install -e .
```

### 验证安装

```bash
# 检查环境配置
sim check
```

## 使用示例

### 快速开始

```bash
# 检查环境
sim check

# 列出所有模拟器
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

# 滑动操作
sim swipe up

# 关闭模拟器
sim shutdown
```

### 设备管理示例

```bash
# 列出已启动的模拟器
sim list --state booted

# 创建新模拟器
sim create "iPhone 17 Pro" --ios 26.3

# 删除模拟器
sim delete --udid <UDID> --force

# 重置模拟器
sim erase
```

### 应用管理示例

```bash
# 安装应用
sim install app.ipa

# 启动应用
sim launch com.apple.Preferences

# 终止应用
sim terminate com.apple.Preferences

# 卸载应用
sim uninstall com.app
```

### 交互操作示例

```bash
# 获取无障碍树
sim tree

# 点击按钮
sim tap --text "确认"

# 输入文本
sim text "用户名"

# 滑动屏幕
sim swipe down

# 按下按键
sim key return

# 硬件按钮
sim button home
```

### 测试与分析示例

```bash
# 无障碍审计
sim audit

# 视觉差异对比
sim diff base.png curr.png

# 监控应用日志
sim log --app com.app

# 捕获当前状态
sim state
```

### 权限与设置示例

```bash
# 授予权限
sim privacy --grant camera --bundle-id com.app

# 发送推送通知
sim push --title "提醒" --body "您有新消息"

# 复制文本到剪贴板
sim clipboard "文本内容"

# 获取状态栏信息
sim statusbar --get
```

### 构建示例

```bash
# 构建项目
sim build --project App.xcodeproj

# 运行测试
sim test --project App.xcodeproj
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

所有命令支持 `--json` 格式输出，方便程序解析：

```bash
# 列出模拟器（JSON 格式）
sim list --json
# 输出: {"simulators": [...], "count": 11}

# 检查环境（JSON 格式）
sim check --json
# 输出: {"ready": true, "checks": {...}}
```

## 依赖

- **操作系统**：macOS
- **开发工具**：Xcode + Xcode Command Line Tools
- **Python**：3.10+
- **idb-companion**：`brew install idb-companion`
- **Pillow**：用于视觉对比功能

## 许可证

MIT License

## 问题反馈

如果您遇到问题或有功能建议，请提交 [Issue](https://github.com/opencode-ai/opencode-ios-simulator/issues)。
