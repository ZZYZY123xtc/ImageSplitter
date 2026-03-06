# 🎨 Image Splitter - 图片元素分割工具

[中文](#中文) | [English](#english)

---

## 中文

一个强大的图片处理工具，能自动去除 PNG 的透明边并分割成独立元素。完美适配游戏开发工作流！

### ✨ 核心功能

- 🎯 **自动去透明边** - 智能检测和裁剪四周透明区域
- 🔪 **元素分割** - 使用连通区域标记算法自动识别独立对象
- 🎨 **保留透明度** - 输出原生 RGBA PNG，保持所有透明信息
- ⚡ **快速处理** - 单张 < 1秒，批量处理 < 2分钟
- 📁 **自动打开** - 处理完自动打开输出文件夹
- 🎮 **游戏引擎友好** - 支持 Godot、Unity、Unreal Engine 等

### 🚀 快速开始

#### 方式1️⃣：使用 EXE 应用（推荐）

```bash
# Windows 用户直接双击运行
./bin/图片分割工具.exe
```

**三种功能模式：**
1. 📋 **快速粘贴分割** - Win+Shift+S → Ctrl+C → 点按钮
2. 🖼️ **选择单个文件** - 浏览选择 PNG → 自动处理
3. 📁 **批量处理文件夹** - 选文件夹 → 一键全部

#### 方式2️⃣：使用 Python 脚本

```bash
# 安装依赖
pip install -r requirements.txt

# 运行主应用（GUI）
python src/图片分割工具.py

# 或运行其他版本
python src/gui_splitter.py       # GUI 版本
python src/paste_and_split.py    # 粘贴版本
python src/quick_split.py        # 批量处理
```

#### 方式3️⃣：快速启动脚本

```bash
# Windows 双击运行
scripts/启动.bat
```

### 📂 项目结构

```
ImageSplitter/
├── bin/
│   └── 图片分割工具.exe          # 独立应用（Windows）
├── src/
│   ├── 图片分割工具.py           # 主应用（推荐修改这个）
│   ├── gui_splitter.py           # GUI 版本源码
│   ├── paste_and_split.py        # 粘贴版本
│   ├── quick_split.py            # 批量处理版本
│   ├── crop_transparent.py       # 仅去透明边版本
│   └── split_elements.py         # 基础分割库
├── docs/
│   ├── 快速开始.md               # 详细使用指南
│   ├── 使用说明.md               # 功能说明
│   ├── 参考卡.txt                # 快速参考
│   └── README.txt                # 文件清单
├── scripts/
│   └── 启动.bat                  # 快速启动脚本
├── requirements.txt              # Python 依赖
└── README.md                     # 本文件
```

### 💾 输出示例

处理后的文件结构：

```
参考图片/
└── 原始图片_elements/
    ├── 00_full.png               # 完整裁剪后的图片
    ├── element_001.png           # 第1个元素
    ├── element_002.png           # 第2个元素
    └── element_003.png           # 第3个元素
```

### 🔧 技术细节

**去透明边算法：**
- 使用 PIL/Pillow 获取 Alpha 通道
- 通过 Alpha > 128 阈值检测非透明区域
- 自动计算边界框并智能裁剪

**元素分割算法：**
- 基于 SciPy 的连通区域标记（Connected Component Labeling）
- 自动识别相邻的非透明像素
- 为每个连通区域生成独立文件
- 自动添加 2px 边距确保完整性

### ⚡ 性能指标

| 操作 | 耗时 | 内存 |
|------|------|------|
| 单张 1000x1000 处理 | < 1 秒 | ~ 200 MB |
| 包含 10 个元素的分割 | < 3 秒 | ~ 300 MB |
| 批量处理 100 张 | < 2 分钟 | ~ 500 MB |

### 🎮 游戏引擎支持

| 引擎 | 支持 | 说明 |
|------|------|------|
| Godot | ✅ | 原生支持 PNG RGBA |
| Unity | ✅ | 直接导入 Sprite |
| Unreal Engine | ✅ | 支持 PNG 纹理 |
| Custom Engine | ✅ | 标准 PNG RGBA 格式 |

### 📋 系统要求

- **OS**: Windows 7 及以上
- **Python**: 3.8+ (仅限运行脚本版本)
- **内存**: > 200 MB
- **磁盘**: EXE 版本 ~55 MB
- **网络**: 不需要

### 🔄 工作流示例

#### 截图 → 处理 → 导入游戏

```
1. Win + Shift + S 截图
   ↓
2. Ctrl + C 复制
   ↓
3. 点"快速粘贴分割"按钮
   ↓
4. 结果文件夹自动打开
   ↓
5. 拖拽 PNG 到游戏引擎
```

### 🛠️ 开发和自定义

#### 修改源代码重新打包

```bash
# 1. 修改源代码
edit src/图片分割工具.py

# 2. 安装 PyInstaller
pip install pyinstaller

# 3. 重新打包
pyinstaller --onefile --windowed --name "图片分割工具" src/图片分割工具.py

# 4. 输出在 dist/ 文件夹
```

#### 调整分割敏感度

在源代码中找到这一行：

```python
binary = alpha > 128  # 修改 128 这个值
```

- 数值越小，越容易检测到透明区域（可能过度分割）
- 数值越大，越严格（可能遗漏细节）
- 建议范围：100-150

### 📚 更多文档

- [快速开始指南](docs/快速开始.md) - 详细的使用教程
- [功能说明](docs/使用说明.md) - 各个功能特性详解
- [参考卡](docs/参考卡.txt) - 打印版快速参考

### 🐛 常见问题

**Q: EXE 这么大（55MB）为什么？**
A: 包含了完整的 Python 运行环境和所有依赖库。

**Q: 可以在 Mac/Linux 上用吗？**
A: EXE 是 Windows 专用。但可以运行 Python 版本。

**Q: 分割结果太多/太少？**
A: 调整源代码中的 Alpha 阈值（默认 128）。

**Q: 能处理其他图片格式吗？**
A: 目前专为 PNG 优化，其他格式会自动转换为 RGBA。

### 📦 依赖库

```
Pillow >= 9.0.0     # 图片处理
numpy >= 1.21.0     # 数组操作
scipy >= 1.7.0      # 连通区域标记
```

完整列表见 [requirements.txt](requirements.txt)

### 📝 许可证

MIT License - 详见 LICENSE 文件

### 🤝 贡献

欢迎 Pull Request！

如何贡献：
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

### 📞 联系方式

- 📧 Email: your.email@example.com
- 💬 Issues: [GitHub Issues](../../issues)
- 💭 Discussions: [GitHub Discussions](../../discussions)

### 🙏 致谢

- 基于 PIL/Pillow、NumPy、SciPy 等优秀开源库
- 感谢所有的贡献者和用户的支持

### 📊 更新日志

#### v1.0.0 (2026-03-06)
- ✅ 初始版本发布
- ✅ EXE 应用打包
- ✅ 三种使用模式
- ✅ 完整文档

---

## English

A powerful image processing tool that automatically removes transparent edges from PNG files and segments them into independent elements. Perfect for game development workflows!

### ✨ Features

- 🎯 **Auto Crop Transparency** - Intelligently detect and remove transparent borders
- 🔪 **Element Segmentation** - Automatically identify and separate independent objects
- 🎨 **Preserve Transparency** - Output native RGBA PNG with all transparency info
- ⚡ **Fast Processing** - Single image < 1sec, batch < 2min
- 📁 **Auto Open** - Automatically open output folder
- 🎮 **Game Engine Ready** - Support Godot, Unity, Unreal Engine, etc.

### 🚀 Quick Start

#### Method 1️⃣: Use EXE Application (Recommended)

```bash
# Windows users: Double-click to run
./bin/图片分割工具.exe
```

#### Method 2️⃣: Use Python Script

```bash
# Install dependencies
pip install -r requirements.txt

# Run main app
python src/图片分割工具.py
```

### 📂 Project Structure

```
ImageSplitter/
├── bin/                          # Compiled applications
├── src/                          # Source code
├── docs/                         # Documentation
├── scripts/                      # Utility scripts
├── requirements.txt
└── README.md
```

### 🎮 Supported Game Engines

- ✅ Godot
- ✅ Unity
- ✅ Unreal Engine
- ✅ Any engine supporting PNG RGBA

### 📋 System Requirements

- **OS**: Windows 7+
- **Memory**: > 200 MB
- **Disk**: EXE ~55 MB

### 📞 Contact

- 📧 Issues: [GitHub Issues](../../issues)
- 💬 Discussions: [GitHub Discussions](../../discussions)

### 📝 License

MIT License

---

**Ready to use? Start now!** 🎨
