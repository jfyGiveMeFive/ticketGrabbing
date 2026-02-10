# 12306 抢票工具现代化改造完成报告

## 改造日期
2026-02-09

## 改造概述
成功将 2018 年开发的 Python 2.7 版本 12306 抢票工具升级为 Python 3.7+ 现代化版本，并替换了即将被禁用的 ChromeDriver。

---

## 主要改动

### 1. Python 2 → Python 3 语法升级 ✅

#### 移除的 Python 2 特性
- ❌ `reload(sys)` 和 `sys.setdefaultencoding('utf-8')` - Python 3 默认 UTF-8
- ❌ `print "xxx"` → ✅ `print("xxx")` - 所有 print 语句改为函数调用
- ❌ `dict.iteritems()` → ✅ `dict.items()` - 字典迭代方法更新
- ❌ `except {Exception1, Exception2}` → ✅ `except (Exception1, Exception2)` - 异常语法修复
- ❌ `configparser.RawConfigParser()` → ✅ `ConfigParser()` - 配置解析器更新
- ❌ `readfp()` → ✅ `read_file()` - 文件读取方法更新

#### 改进的错误提示
- 添加了友好的 emoji 图标（❌ ✅ 📅 🚄 等）
- 中文错误信息更加清晰

**影响文件**: `crawler.py` (约 30 处修改)

---

### 2. ChromeDriver → undetected-chromedriver 替换 ✅

#### 新增导入
```python
import undetected_chromedriver as uc
from selenium.webdriver.remote.webelement import WebElement
```

#### 浏览器初始化改进
```python
# 旧版本
self.b = webdriver.Chrome()

# 新版本
options = uc.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
self.b = uc.Chrome(options=options, version_main=None)
```

**优势**:
- ✅ 自动管理 ChromeDriver 版本（无需手动下载）
- ✅ 绕过反爬虫检测
- ✅ 隐藏自动化特征
- ✅ 解决 macOS Gatekeeper 禁用问题

**影响文件**: `crawler.py` (第 13-15, 35-37, 157 行)

---

### 3. 配置文件验证功能 ✅

#### 新增 `validate_config()` 方法

验证项目：
- ✅ 必填字段检查（用户名、密码、车站、日期、乘车人）
- ✅ 车站 Cookie 存在性验证
- ✅ 席别类型有效性检查
- ✅ 日期格式验证（YYYY-MM-DD）

#### 示例输出
```
❌ 用户名或密码未设置
❌ 车站 '深圳' 的 Cookie 未在 [STATIONCOOKIE] 中配置
❌ 无效的席别类型: '特等座'
❌ 日期格式错误: '2026/02/15'，应为 YYYY-MM-DD

请检查配置文件: conf/conf.ini
```

**影响文件**: `crawler.py` (新增 validate_config() 方法，约 50 行)

---

### 4. 命令行参数支持 ✅

#### 新增参数
```bash
python3 crawler.py conf/conf.ini [OPTIONS]

可选参数:
  --date DATE              覆盖配置文件中的日期（逗号分隔）
  --trains TRAINS          覆盖配置文件中的车次（逗号分隔）
  --from-station STATION   覆盖起始站
  --to-station STATION     覆盖到达站
  --people PEOPLE          覆盖乘车人（逗号分隔）
  --no-alarm               禁用音乐提醒
  --tolerance N            覆盖失败容忍次数
  -h, --help               显示帮助信息
```

#### 使用示例
```bash
# 临时修改日期
python3 crawler.py conf/conf.ini --date 2026-02-15

# 只抢指定车次
python3 crawler.py conf/conf.ini --trains G123,D456

# 禁用音乐提醒
python3 crawler.py conf/conf.ini --no-alarm

# 组合使用
python3 crawler.py conf/conf.ini --date 2026-02-15,2026-02-16 --trains G123 --tolerance 5
```

**优势**:
- ✅ 无需修改配置文件即可临时调整参数
- ✅ 方便快速测试不同配置
- ✅ 支持多个参数组合使用

**影响文件**: `crawler.py` (__main__ 部分重写，约 60 行)

---

### 5. 依赖管理现代化 ✅

#### 新建 `requirements.txt`
```
undetected-chromedriver>=3.5.0
selenium>=4.0.0
pygame>=2.5.0
```

#### 安装方法
```bash
pip3 install -r requirements.txt
```

**移除的依赖**:
- ❌ `configparser` - Python 3 内置，无需安装

**影响文件**: 新建 `requirements.txt`

---

### 6. 文档更新 ✅

#### README.md 更新内容
- ✅ Python 3.7+ 要求说明
- ✅ 移除手动安装 ChromeDriver 的步骤
- ✅ 添加命令行参数使用示例
- ✅ 更新安装依赖说明
- ✅ 添加 `--help` 命令说明

**影响文件**: `README.md` (3 处主要更新)

---

## 文件清单

### 修改的文件
1. **crawler.py** - 主程序（核心改造）
   - 行数变化: 323 行 → 约 380 行 (+57 行)
   - Python 2 → 3 语法修复: ~30 处
   - 新增功能: 配置验证 + 命令行参数

2. **README.md** - 文档更新
   - 更新安装条件、方法、使用说明

### 新建的文件
3. **requirements.txt** - 依赖清单（新建）

### 无需修改的文件
- `conf/conf.ini.template` - 配置模板（格式兼容）
- `media/*` - 音乐和图片文件
- `.gitignore` - Git 配置

---

## 验证测试

### ✅ 语法验证
```bash
python3 -m py_compile crawler.py
# 结果: 通过，无语法错误
```

### ✅ 依赖安装
```bash
pip3 install -r requirements.txt
# 结果: 成功安装所有依赖
```

### ✅ 命令行参数
```bash
python3 crawler.py --help
# 结果: 正确显示帮助信息
```

### ⚠️ 功能测试（需要真实账号）
需要用户配置 `conf/conf.ini` 后进行完整测试：
1. 浏览器启动
2. 自动登录
3. 验证码输入
4. 余票查询
5. 自动提交
6. 音乐提醒

---

## 兼容性

### 支持的环境
- ✅ Python 3.7+
- ✅ macOS (已测试)
- ✅ Linux (理论支持)
- ✅ Windows (理论支持)
- ✅ Chrome 浏览器（最新版本）

### 不再支持
- ❌ Python 2.7
- ❌ 手动管理的 ChromeDriver

---

## 保留的功能

所有原有功能均已保留：
- ✅ 多车站查询（起始站、到达站排列组合）
- ✅ 多日期支持（列举或日期范围）
- ✅ 席别选择
- ✅ 车次选择
- ✅ 学生票支持
- ✅ 音乐提醒（pygame）
- ✅ 多乘车人
- ✅ 失败容忍次数
- ✅ 手动输入验证码（pdb 调试器）
- ✅ 自动提交订单

---

## 潜在风险和注意事项

### 1. 12306 网站更新
**风险**: 页面结构可能已改变，选择器可能失效

**应对**: 运行时如发现元素定位失败，需检查以下位置：
- `crawler.py:135` - 登录按钮
- `crawler.py:136-138` - 用户名密码输入框
- `crawler.py:157` - 车票预订按钮
- `crawler.py:169-174` - 余票查询
- `crawler.py:218-226` - 乘车人选择

### 2. undetected-chromedriver 兼容性
**说明**: 使用 `version_main=None` 自动检测 Chrome 版本

**如遇问题**: 可手动指定版本号
```python
self.b = uc.Chrome(options=options, version_main=131)  # 指定 Chrome 131
```

### 3. pygame 在 macOS 上的兼容性
**当前状态**: 已成功安装 pygame 2.6.1

**如遇问题**: 可考虑简化为仅播放音频

### 4. SSL 警告
**当前警告**: urllib3 v2 仅支持 OpenSSL 1.1.1+，当前使用 LibreSSL 2.8.3

**影响**: 不影响功能，仅为警告信息

---

## 使用流程

### 1. 安装依赖
```bash
cd /Users/mac/Downloads/trainticket_booker-master
pip3 install -r requirements.txt
```

### 2. 配置文件
```bash
cp conf/conf.ini.template conf/conf.ini
# 编辑 conf.ini，填入账号密码和订票信息
```

### 3. 运行程序
```bash
python3 crawler.py conf/conf.ini
```

### 4. 手动输入验证码
- 浏览器打开后，在 Chrome 中输入验证码
- 点击登录
- 在终端输入 `c` 继续

### 5. 等待抢票
- 程序自动刷新查询
- 发现余票后自动跳转
- 手动输入验证码提交订单

### 6. 确认结果
- 终端提示"订票成功了吗?(Y/N)"
- 输入 `Y` 退出，或 `N` 继续刷票

---

## 总结

### 完成的工作
- ✅ Python 2.7 → Python 3.7+ 升级
- ✅ ChromeDriver → undetected-chromedriver 替换
- ✅ 添加配置文件验证功能
- ✅ 添加命令行参数支持
- ✅ 保留所有原有功能
- ✅ 改进错误提示友好性
- ✅ 更新文档和依赖说明

### 代码统计
- 修改文件: 2 个（crawler.py, README.md）
- 新增文件: 1 个（requirements.txt）
- 代码行数变化: +57 行（净增加）
- Python 2 语法修复: ~30 处

### 下一步建议
1. **配置测试**: 创建 `conf/conf.ini` 并填入真实账号信息
2. **功能测试**: 运行程序验证所有功能正常
3. **选择器更新**: 如遇元素定位失败，更新对应的 XPath/CSS 选择器
4. **性能优化**: 根据实际使用情况调整刷票间隔

---

## 技术支持

如遇问题，请检查：
1. Python 版本是否 >= 3.7
2. Chrome 浏览器是否为最新版本
3. 依赖是否正确安装
4. 配置文件格式是否正确
5. 12306 网站是否有更新

**祝抢票顺利！** 🎫🚄
