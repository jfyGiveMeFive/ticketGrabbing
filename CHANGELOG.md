# 更新日志 (CHANGELOG)

## [2.0.0] - 2026-02-09

### 🎉 重大更新：Python 3 现代化改造

这是一个重大版本更新，将整个项目从 Python 2.7 升级到 Python 3.7+，并替换了即将被禁用的 ChromeDriver。

---

## 新增功能 (Added)

### ✨ 配置文件验证
- 新增 `validate_config()` 方法，在程序启动时自动验证配置文件
- 验证项目包括：
  - 必填字段检查（用户名、密码、车站、日期、乘车人）
  - 车站 Cookie 存在性验证
  - 席别类型有效性检查
  - 日期格式验证（YYYY-MM-DD）
- 友好的错误提示，使用 emoji 图标标识问题

### 🎯 命令行参数支持
- 新增 7 个命令行参数，可覆盖配置文件设置：
  - `--date` - 指定日期（逗号分隔）
  - `--trains` - 指定车次（逗号分隔）
  - `--from-station` - 指定起始站
  - `--to-station` - 指定到达站
  - `--people` - 指定乘车人（逗号分隔）
  - `--no-alarm` - 禁用音乐提醒
  - `--tolerance` - 设置失败容忍次数
- 新增 `--help` 参数，显示详细使用说明
- 支持参数组合使用，无需修改配置文件即可快速测试

### 📚 文档完善
- 新增 `MODERNIZATION_SUMMARY.md` - 详细的改造报告
- 新增 `QUICK_START.md` - 快速开始指南
- 新增 `verify_modernization.py` - 自动验证脚本
- 新增 `requirements.txt` - 标准化依赖管理
- 更新 `README.md` - 更新安装和使用说明

---

## 改进 (Changed)

### 🔄 Python 3 语法升级
- 移除 `reload(sys)` 和 `sys.setdefaultencoding('utf-8')`（Python 3 默认 UTF-8）
- 所有 `print` 语句改为函数调用：`print("xxx")`
- 字典迭代方法：`dict.iteritems()` → `dict.items()`
- 异常捕获语法：`except {Exception}` → `except (Exception)`
- 配置解析器：`configparser.RawConfigParser()` → `ConfigParser()`
- 文件读取方法：`readfp()` → `read_file()`

### 🚀 ChromeDriver 替换
- 使用 `undetected-chromedriver` 替代原生 `selenium.webdriver.Chrome()`
- 自动管理 ChromeDriver 版本，无需手动下载
- 添加反爬虫检测绕过功能
- 隐藏自动化特征，提高成功率
- 解决 macOS Gatekeeper 禁用问题

### 💬 用户体验改进
- 错误提示添加 emoji 图标（❌ ✅ 📅 🚄 🚉 🏁 👥 🔇 ⚠️）
- 更友好的中文错误信息
- 命令行参数覆盖时显示确认信息
- 程序退出时显示友好提示

### 📦 依赖管理现代化
- 创建标准的 `requirements.txt` 文件
- 更新依赖版本：
  - `undetected-chromedriver>=3.5.0`（新增）
  - `selenium>=4.0.0`（从 2.x 升级）
  - `pygame>=2.5.0`（从 1.x 升级）
- 移除 `configparser`（Python 3 内置）

---

## 修复 (Fixed)

### 🐛 Bug 修复
- 修复 Python 2 特有的语法错误
- 修复 `configparser` 导入和使用方式
- 修复异常捕获语法错误
- 修复字典迭代方法兼容性问题
- 移除重复的 `import pdb` 语句

### 🔧 兼容性修复
- 解决 macOS Gatekeeper 对 ChromeDriver 的禁用问题
- 解决 Python 2.7 停止维护后的兼容性问题
- 更新 Selenium 4.x API 调用方式

---

## 移除 (Removed)

### ❌ 废弃功能
- 移除 Python 2.7 支持
- 移除手动 ChromeDriver 管理
- 移除 Python 2 特有的编码设置

---

## 技术细节

### 文件变更统计
```
修改的文件:
  crawler.py          323 行 → 429 行 (+106 行)
  README.md           84 行 → 104 行 (+20 行)

新增的文件:
  requirements.txt                3 行
  MODERNIZATION_SUMMARY.md      343 行
  QUICK_START.md                373 行
  verify_modernization.py       229 行

总计: +1074 行代码和文档
```

### 代码质量
- ✅ Python 3 语法检查通过
- ✅ 所有依赖包安装成功
- ✅ 命令行参数功能正常
- ✅ 文件完整性验证通过
- ✅ 无 Python 2 语法残留
- ✅ 所有新功能已实现

### 兼容性
- **支持**: Python 3.7+, macOS, Linux, Windows
- **不再支持**: Python 2.7

---

## 升级指南

### 从 1.x 升级到 2.0

#### 1. 更新 Python 版本
```bash
# 检查 Python 版本
python3 --version

# 需要 Python 3.7 或更高版本
```

#### 2. 安装新依赖
```bash
# 卸载旧依赖（可选）
pip uninstall selenium pygame

# 安装新依赖
pip3 install -r requirements.txt
```

#### 3. 移除手动安装的 ChromeDriver
```bash
# macOS
rm /usr/local/bin/chromedriver

# 或者如果使用 brew 安装
brew uninstall chromedriver
```

#### 4. 更新运行命令
```bash
# 旧版本
python crawler.py conf/conf.ini

# 新版本
python3 crawler.py conf/conf.ini
```

#### 5. 配置文件无需修改
- 配置文件格式完全兼容
- `conf/conf.ini` 无需任何修改即可使用

#### 6. 验证升级
```bash
# 运行验证脚本
python3 verify_modernization.py

# 应该看到: 🎉 所有检查通过！
```

---

## 已知问题

### ⚠️ SSL 警告
- **现象**: 启动时显示 urllib3 OpenSSL 警告
- **影响**: 不影响功能使用
- **原因**: macOS 使用 LibreSSL 而非 OpenSSL
- **解决**: 可忽略，或升级 OpenSSL

### ⚠️ 12306 网站更新
- **风险**: 12306 网站可能已更新页面结构
- **影响**: 元素定位可能失效
- **解决**: 需要手动更新选择器（参见 MODERNIZATION_SUMMARY.md）

---

## 贡献者

- **原作者**: [thushenhan@gmail.com](mailto:thushenhan@gmail.com)
- **现代化改造**: Claude Sonnet 4.5 (2026-02-09)

---

## 许可证

本项目继承原项目的许可证。

---

## 致谢

感谢原作者创建了这个实用的工具。本次现代化改造旨在让这个工具能够继续在 Python 3 时代为用户服务。

---

## 下一步计划

### 可能的未来改进
- [ ] 添加图形用户界面（GUI）
- [ ] 支持更多的通知方式（邮件、短信、微信）
- [ ] 添加自动验证码识别（需谨慎，可能违反服务条款）
- [ ] 支持多账号并发抢票
- [ ] 添加抢票成功率统计
- [ ] 支持候补购票功能

### 维护计划
- 定期更新依赖包版本
- 跟踪 12306 网站更新
- 修复用户报告的 bug
- 改进文档和使用指南

---

## 反馈和支持

如有问题或建议，请：
1. 查看 `QUICK_START.md` 的常见问题部分
2. 查看 `MODERNIZATION_SUMMARY.md` 的技术细节
3. 运行 `python3 verify_modernization.py` 检查环境
4. 联系原作者或提交 Issue

---

**最后更新**: 2026-02-09
**版本**: 2.0.0
**状态**: ✅ 稳定版本
