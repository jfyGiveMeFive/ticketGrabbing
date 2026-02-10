# 浏览器与依赖版本要求

## 浏览器要求

### Google Chrome（必需）

#### 推荐版本
- **Chrome 120+**（2024年及以后版本）
- 建议使用最新稳定版本

#### 最低版本
- **Chrome 90+**（2021年4月及以后）

#### 下载地址
- 官方网站：https://www.google.com/chrome/
- macOS：通过官网下载 .dmg 安装包
- Linux：通过包管理器或官网下载
- Windows：通过官网下载 .exe 安装程序

#### 版本检查
```bash
# macOS/Linux
google-chrome --version
# 或
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version

# Windows
chrome.exe --version
```

#### 重要说明
- ✅ **无需手动安装 ChromeDriver**
- ✅ `undetected-chromedriver` 会自动下载并管理 ChromeDriver
- ✅ 自动匹配 Chrome 浏览器版本
- ✅ 解决 macOS Gatekeeper 禁用问题

---

## Python 依赖版本要求

### Python 版本

#### 推荐版本
- **Python 3.9+** 或 **Python 3.10+**

#### 最低版本
- **Python 3.7+**（必需）

#### 版本检查
```bash
python3 --version
```

#### 安装 Python
- macOS：使用 Homebrew
  ```bash
  brew install python@3.10
  ```
- Linux：使用包管理器
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3.10

  # CentOS/RHEL
  sudo yum install python3.10
  ```
- Windows：从 https://www.python.org/downloads/ 下载安装

---

## Python 包依赖

### 核心依赖包

#### 1. undetected-chromedriver

**版本要求**：`>= 3.5.0`

**推荐版本**：`3.5.5` 或更高

**功能**：
- 自动管理 ChromeDriver 版本
- 绕过反爬虫检测
- 隐藏自动化特征
- 解决 macOS Gatekeeper 问题

**安装**：
```bash
pip3 install undetected-chromedriver>=3.5.0
```

**兼容性**：
- ✅ Chrome 90+
- ✅ Python 3.7+
- ✅ macOS, Linux, Windows

---

#### 2. selenium

**版本要求**：`>= 4.0.0`

**推荐版本**：`4.15.0` 或更高

**功能**：
- Web 自动化框架
- 浏览器控制
- 元素定位和操作

**安装**：
```bash
pip3 install selenium>=4.0.0
```

**重要变化**（从 Selenium 3.x 升级）：
- ✅ 新的 Service 对象
- ✅ 改进的等待机制
- ✅ 更好的错误提示
- ✅ 支持 Chrome DevTools Protocol

**兼容性**：
- ✅ Python 3.7+
- ✅ 所有主流浏览器

---

#### 3. pygame

**版本要求**：`>= 2.5.0`

**推荐版本**：`2.5.2` 或更高

**功能**：
- 音频播放（抢票成功提醒）
- 图片显示

**安装**：
```bash
pip3 install pygame>=2.5.0
```

**macOS 注意事项**：
- 可能需要安装 SDL2 库
- 如遇问题，可使用 Homebrew 安装：
  ```bash
  brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
  ```

**可选性**：
- 如果不需要音乐提醒，可使用 `--no-alarm` 参数
- 安装失败不影响核心功能

**兼容性**：
- ✅ Python 3.7+
- ✅ macOS, Linux, Windows

---

## 完整安装命令

### 一键安装所有依赖
```bash
pip3 install -r requirements.txt
```

### requirements.txt 内容
```
undetected-chromedriver>=3.5.0
selenium>=4.0.0
pygame>=2.5.0
```

### 验证安装
```bash
# 运行验证脚本
python3 verify_modernization.py

# 或手动检查
python3 -c "import undetected_chromedriver; print('undetected-chromedriver:', undetected_chromedriver.__version__)"
python3 -c "import selenium; print('selenium:', selenium.__version__)"
python3 -c "import pygame; print('pygame:', pygame.version.ver)"
```

---

## 操作系统兼容性

### macOS

#### 支持版本
- ✅ macOS 11 (Big Sur) 及以上
- ✅ macOS 10.15 (Catalina) 及以上（可能需要额外配置）

#### 已测试版本
- ✅ macOS 14.6 (Sonoma)

#### 特殊注意事项
- Gatekeeper 可能阻止 ChromeDriver 运行
- `undetected-chromedriver` 已解决此问题
- 如遇权限问题，可能需要在"系统偏好设置 > 安全性与隐私"中允许

---

### Linux

#### 支持发行版
- ✅ Ubuntu 20.04+
- ✅ Debian 10+
- ✅ CentOS 8+
- ✅ Fedora 35+
- ✅ Arch Linux

#### 依赖要求
```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip chromium-browser

# CentOS/RHEL
sudo yum install python3 python3-pip chromium

# Arch Linux
sudo pacman -S python python-pip chromium
```

---

### Windows

#### 支持版本
- ✅ Windows 10 (1809+)
- ✅ Windows 11

#### 依赖要求
- Python 3.7+ (从 python.org 下载)
- Google Chrome 浏览器
- Visual C++ Redistributable（通常已安装）

#### 特殊注意事项
- 使用 PowerShell 或 CMD 运行
- 路径中避免使用中文字符
- 可能需要管理员权限安装依赖

---

## 网络要求

### 必需的网络访问

#### 12306 官方网站
- `https://kyfw.12306.cn` - 主站
- `https://www.12306.cn` - 备用

#### ChromeDriver 下载（首次运行）
- `https://chromedriver.storage.googleapis.com` - ChromeDriver 仓库
- `https://googlechromelabs.github.io` - 备用下载源

#### Python 包下载（安装依赖时）
- `https://pypi.org` - Python 包索引
- `https://files.pythonhosted.org` - 包文件存储

### 网络建议
- ✅ 使用稳定的网络连接
- ✅ 避免使用 VPN（可能被 12306 检测）
- ✅ 确保防火墙允许 Python 和 Chrome 访问网络
- ⚠️ 首次运行需要下载 ChromeDriver（约 5-10 MB）

---

## 常见问题

### Q1: Chrome 版本过旧怎么办？
**A**: 更新到最新版本
```bash
# macOS
# 打开 Chrome，菜单 > 关于 Google Chrome > 自动更新

# Linux
sudo apt-get update && sudo apt-get upgrade google-chrome-stable

# Windows
# 打开 Chrome，设置 > 关于 Chrome > 自动更新
```

---

### Q2: undetected-chromedriver 下载失败？
**A**: 手动指定 ChromeDriver 版本或使用镜像源
```bash
# 使用国内镜像
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple undetected-chromedriver
```

---

### Q3: pygame 安装失败（macOS）？
**A**: 安装 SDL2 依赖
```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
pip3 install pygame
```

或者禁用音乐提醒：
```bash
python3 crawler.py conf/conf.ini --no-alarm
```

---

### Q4: Selenium 4.x 与旧代码不兼容？
**A**: 本项目已完全适配 Selenium 4.x，无需担心兼容性问题

---

### Q5: 如何检查所有依赖是否正确安装？
**A**: 运行验证脚本
```bash
python3 verify_modernization.py
```

应该看到：
```
✅ Python 版本检查 - 通过
✅ 依赖包安装 - 通过
✅ Python 语法检查 - 通过
✅ 关键导入测试 - 通过
...
🎉 所有检查通过！
```

---

## 版本兼容性矩阵

| 组件 | 最低版本 | 推荐版本 | 最高测试版本 |
|------|---------|---------|-------------|
| Python | 3.7 | 3.10+ | 3.12 |
| Chrome | 90 | 120+ | 131 |
| undetected-chromedriver | 3.5.0 | 3.5.5+ | 3.5.5 |
| selenium | 4.0.0 | 4.15.0+ | 4.26.1 |
| pygame | 2.5.0 | 2.5.2+ | 2.6.1 |
| macOS | 10.15 | 11+ | 14.6 |
| Ubuntu | 20.04 | 22.04+ | 24.04 |
| Windows | 10 (1809) | 11 | 11 |

---

## 更新建议

### 定期更新
```bash
# 更新所有依赖到最新版本
pip3 install --upgrade -r requirements.txt

# 更新 Chrome 浏览器
# macOS/Windows: 通过浏览器自动更新
# Linux: 通过包管理器更新
```

### 更新频率建议
- **Chrome 浏览器**: 每月检查更新
- **Python 包**: 每季度更新一次
- **Python 版本**: 每年考虑升级

---

## 技术支持

如遇依赖问题：
1. 运行 `python3 verify_modernization.py` 检查环境
2. 查看 `QUICK_START.md` 的常见问题部分
3. 确认 Chrome 和 Python 版本符合要求
4. 检查网络连接是否正常

---

**最后更新**: 2026-02-10
**文档版本**: 1.0
**项目版本**: 2.0.0
