火车票订票助手 (Python 3 现代化版本)
===================================

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-orange.svg)](CHANGELOG.md)

## 版本说明

**当前版本**: 2.0.0 (2026-02-10)
**状态**: ✅ 生产就绪

本项目已从 Python 2.7 升级到 Python 3.7+，并进行了全面的现代化改造。

### 最新更新
- 2026-02-10 添加浏览器版本要求文档，整合项目文档，添加 MIT License
- 2026-02-09 Python 3 现代化改造完成，替换为 undetected-chromedriver
- 2018-01-11 splinter 改为 selenium，修改座位种类，添加对选座的支持

---

## 关于该小工具

该脚本适用于12306刷票，无图形界面，需要安装python。原理为利用chrome测试工具自动化模拟鼠标点击买票，略慢于基于HTTP Request爬虫模式，优点是对网站升级与框架改变较鲁棒，且免去刷票软件缴费排队的优先级困扰。适合Mac与Linux用户及对python有一定了解的用户(Windows下安装python也可)。本脚本无法绕过验证码输入，需要用户手动输入验证码。

---

## 功能介绍

- 支持多车站(起始、到达)，脚本将自动查询各个起始终点站的排列组合
- 多日期(可列举各个日期或日期范围，无上限)
- 支持席别选择、车次选择
- 支持学生票
- 支持铃声提醒
- 支持多个乘车人
- 支持失败次数超过阈值放弃该车次
- 刷票间隔约1s
- 支持自动提交

---

## 安装条件

- [Chrome浏览器](https://www.google.com/chrome/browser/desktop/index.html)
- **不再需要手动安装 ChromeDriver**（自动管理）
- Python 3.7+
- undetected-chromedriver
- selenium 4.x
- pygame

详细版本要求请查看 [BROWSER_REQUIREMENTS.md](BROWSER_REQUIREMENTS.md)

---

## 安装方法

- 网上下载对应操作系统的Chrome浏览器并安装
- **无需手动安装 ChromeDriver**（undetected-chromedriver 会自动管理）
- 安装 Python 3.7 或更高版本
- 安装依赖包
``` bash
pip3 install -r requirements.txt
```

---

## 使用方法

### 基本用法

打开terminal，切换到脚本所在目录
``` bash
cd {YOUR_PATH_TO_THE_SCRIPT}/conf
```
从模板拷贝一份设置文件
``` bash
cp conf.ini.template conf.ini
cd ../
```
在conf.ini中设置你的用户名密码，根据注释设定对应参数；此处最重要的是获取你的起始到达站的cookie值,并填在[STATIONCOOKIE]区域下，模板中有广州和北京为示例。获取方法：打开12306 票查询界面，输入你的起始终点站与日期，点击查询。

在Chrome中右键, 选择Inspect，Chrome将弹出开发者工具。
选择Resources > Cookies > www.12306.cn
对应'_jc_save_fromStation'和'_jc_save_toStation'的值就是你的起始/终点站的cookie值，将其以'站名=cookie值'的形式填在[STATIONCOOKIE]区域。

安装好上述依赖之后，运行脚本
``` bash
python3 crawler.py conf/conf.ini
```

### 使用命令行参数覆盖配置

``` bash
# 指定日期
python3 crawler.py conf/conf.ini --date 2026-02-15

# 指定车次
python3 crawler.py conf/conf.ini --trains G123,D456

# 禁用音乐提醒
python3 crawler.py conf/conf.ini --no-alarm

# 组合使用
python3 crawler.py conf/conf.ini --date 2026-02-15,2026-02-16 --trains G123 --tolerance 5
```

### 查看帮助

``` bash
python3 crawler.py --help
```

浏览器将自动跳转到登陆界面（用户名密码已填好），此时脚本停在了调试暂停状态
``` bash
(pdb)
```
在Chrome中输入验证码点击登录, 脚本输入c
``` bash
(pdb)c
```
用户便可坐等脚本自动刷新了。若刷到了余票，浏览器自动跳转到提交界面，只需输入验证码点提交即可。

脚本界面此时会显示'是否抢票成功(Y/N)'，若用户此时已抢到票，输入Y，程序退出；否则输入N，浏览器自动返回查询界面继续刷票。

---

## 退出程序

按Ctrl-C 退出程序（浏览器窗口随之退出）

---

## 📚 文档索引

### 快速开始
- **[QUICK_START.md](QUICK_START.md)** - 详细的快速开始指南（推荐新手阅读）
- **[BROWSER_REQUIREMENTS.md](BROWSER_REQUIREMENTS.md)** - 浏览器与依赖版本要求

### 技术文档
- **[MODERNIZATION_SUMMARY.md](MODERNIZATION_SUMMARY.md)** - 技术改造详细报告
- **[CHANGELOG.md](CHANGELOG.md)** - 版本更新日志

### 其他
- **[LICENSE](LICENSE)** - MIT 开源协议
- **verify_modernization.py** - 环境验证脚本

---

## 🔧 验证环境

运行验证脚本检查环境是否正确配置：
```bash
python3 verify_modernization.py
```

---

## 📋 项目特性

### ✨ 新增功能（v2.0）
- ✅ Python 3.7+ 支持
- ✅ 自动管理 ChromeDriver（无需手动下载）
- ✅ 配置文件验证（启动时自动检查）
- ✅ 命令行参数支持（快速测试不同配置）
- ✅ 友好的错误提示（带 emoji）

### 🎯 核心功能
- ✅ 多车站查询（起始站、到达站排列组合）
- ✅ 多日期支持（列举或日期范围）
- ✅ 席别选择、车次选择
- ✅ 学生票支持
- ✅ 音乐提醒
- ✅ 多乘车人
- ✅ 失败容忍次数
- ✅ 自动提交订单

---

## ⚠️ 重要提示

### 配置文件安全
- `conf/conf.ini` 包含你的账号密码
- **不要上传到公共代码仓库**
- **不要分享给他人**

### 合法使用
- 仅供个人学习和合法购票使用
- 不要用于商业倒票
- 遵守 12306 服务条款

---

## 📞 支持与反馈

### 遇到问题？
1. 运行验证脚本：`python3 verify_modernization.py`
2. 查看 [QUICK_START.md](QUICK_START.md) 的常见问题部分
3. 查看 [BROWSER_REQUIREMENTS.md](BROWSER_REQUIREMENTS.md) 检查版本要求

### 联系方式
- 原作者：[thushenhan@gmail.com](mailto:thushenhan@gmail.com)
- 问题反馈：请查看文档或联系原作者

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

**祝你抢票成功！** 🎫✨🚄
