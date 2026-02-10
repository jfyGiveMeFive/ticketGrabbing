# 快速开始指南

## 一、环境准备（5分钟）

### 1. 检查 Python 版本
```bash
python3 --version
# 需要 Python 3.7 或更高版本
```

### 2. 安装依赖
```bash
cd /Users/mac/Downloads/trainticket_booker-master
pip3 install -r requirements.txt
```

### 3. 安装 Chrome 浏览器
确保已安装最新版本的 Chrome 浏览器（无需手动安装 ChromeDriver）

---

## 二、配置文件设置（10分钟）

### 1. 复制配置模板
```bash
cp conf/conf.ini.template conf/conf.ini
```

### 2. 编辑配置文件
```bash
# 使用你喜欢的编辑器打开
nano conf/conf.ini
# 或
vim conf/conf.ini
# 或
open -a TextEdit conf/conf.ini
```

### 3. 必填配置项

#### [GLOBAL] 区域
```ini
[GLOBAL]
username = 你的12306用户名
password = 你的12306密码
browser = chrome
```

#### [TICKET] 区域
```ini
[TICKET]
# 出发日期（逗号分隔，或使用日期范围）
date = 2026-02-15

# 起始站（逗号分隔，支持多个）
from_station = 广州

# 到达站（逗号分隔，支持多个）
to_station = 北京

# 车次（逗号分隔，留空表示所有车次）
trains = G123,D456

# 席别类型（逗号分隔）
# 可选: 商务座,一等座,二等座,高级软卧,软卧,动卧,硬卧,软座,硬座,无座
ticket_type = 二等座,一等座

# 乘车人（逗号分隔，必须是12306账号中已添加的联系人）
people = 张三,李四

# 是否学生票（Y/N）
student = N

# 失败容忍次数（-1表示无限制）
tolerance = 5

# 是否开启音乐提醒（Y/N）
alarm = Y

# 是否使用日期范围查询（Y/N）
range_query = N
```

#### [STATIONCOOKIE] 区域
**重要**: 需要获取车站的 Cookie 值

##### 获取方法：
1. 打开 Chrome 浏览器，访问 https://kyfw.12306.cn/otn/leftTicket/init
2. 输入起始站、到达站和日期，点击"查询"
3. 按 `F12` 打开开发者工具
4. 选择 `Application` 标签（或 `存储` 标签）
5. 左侧选择 `Cookies` > `https://kyfw.12306.cn`
6. 找到以下两个 Cookie：
   - `_jc_save_fromStation` - 起始站 Cookie
   - `_jc_save_toStation` - 到达站 Cookie
7. 复制 Cookie 的 `Value` 值

##### 配置示例：
```ini
[STATIONCOOKIE]
广州 = %u5E7F%u5DDE%2CGZQ
北京 = %u5317%u4EAC%2CBJP
上海 = %u4E0A%u6D77%2CSHH
深圳 = %u6DF1%u5733%2CSZQ
```

**注意**: 每个你要查询的车站都需要添加对应的 Cookie 值！

---

## 三、运行程序

### 基本运行
```bash
python3 crawler.py conf/conf.ini
```

### 使用命令行参数（推荐）
```bash
# 临时修改日期
python3 crawler.py conf/conf.ini --date 2026-02-15

# 只抢指定车次
python3 crawler.py conf/conf.ini --trains G123,D456

# 禁用音乐提醒（适合办公室使用）
python3 crawler.py conf/conf.ini --no-alarm

# 组合使用
python3 crawler.py conf/conf.ini \
  --date 2026-02-15,2026-02-16 \
  --trains G123 \
  --tolerance 5 \
  --no-alarm
```

### 查看帮助
```bash
python3 crawler.py --help
```

---

## 四、操作流程

### 1. 程序启动
```bash
python3 crawler.py conf/conf.ini
```

输出示例：
```
✅ 配置文件验证通过
pygame 2.6.1 (SDL 2.28.4, Python 3.9.6)
Hello from the pygame community. https://www.pygame.org/contribute.html
```

### 2. 浏览器自动打开
- Chrome 浏览器自动打开
- 自动跳转到 12306 登录页面
- 用户名和密码已自动填充

### 3. 输入验证码
- **在浏览器中**点击验证码图片
- 点击"登录"按钮

### 4. 继续执行
终端会显示：
```bash
(Pdb)
```

在终端输入 `c` 并按回车：
```bash
(Pdb) c
```

### 5. 自动刷票
程序开始自动刷新查询：
```
Try 1 times
date: 2026-02-15, from 广州, to 北京
Try 2 times
date: 2026-02-15, from 广州, to 北京
...
```

### 6. 发现余票
当发现余票时：
```
G123 的 二等座 有余票 5 张!
```

- 浏览器自动跳转到订单提交页面
- 乘车人已自动选择
- **手动输入验证码**
- 点击"提交订单"

### 7. 确认结果
终端提示：
```
订票成功了吗?(Y/N)
```

- 输入 `Y` - 程序退出
- 输入 `N` - 继续刷票（该车次失败次数 +1）

### 8. 退出程序
按 `Ctrl+C` 强制退出

---

## 五、常见问题

### Q1: 提示"❌ 车站 'XXX' 的 Cookie 未在 [STATIONCOOKIE] 中配置"
**解决**: 按照上面的方法获取该车站的 Cookie 值并添加到配置文件

### Q2: 浏览器启动失败
**解决**:
- 确保 Chrome 浏览器已安装
- 检查 Chrome 版本是否为最新
- 尝试重新安装依赖：`pip3 install --upgrade undetected-chromedriver`

### Q3: 找不到元素（Element not found）
**解决**: 12306 网站可能已更新，需要更新代码中的选择器

### Q4: 验证码输入后无反应
**解决**:
- 确保在终端输入了 `c` 并按回车
- 检查是否在 `(Pdb)` 提示符下

### Q5: 音乐提醒不工作
**解决**:
- 检查 `media/sound.ogg` 和 `media/img.jpg` 文件是否存在
- 或使用 `--no-alarm` 禁用音乐提醒

### Q6: SSL 警告信息
**说明**: 这是正常的警告信息，不影响功能使用

---

## 六、高级技巧

### 1. 日期范围查询
在配置文件中设置：
```ini
range_query = Y
date = 2026-02-15,2026-02-20
```
程序会自动查询 2月15日 到 2月20日 之间的所有日期

### 2. 多车站组合
```ini
from_station = 广州,深圳
to_station = 北京,上海
```
程序会查询所有组合：
- 广州 → 北京
- 广州 → 上海
- 深圳 → 北京
- 深圳 → 上海

### 3. 失败容忍机制
```ini
tolerance = 3
```
如果某个车次连续失败 3 次，程序会自动跳过该车次

### 4. 命令行快速测试
```bash
# 测试明天的票
python3 crawler.py conf/conf.ini --date 2026-02-10

# 测试特定车次
python3 crawler.py conf/conf.ini --trains G123

# 静音模式（办公室友好）
python3 crawler.py conf/conf.ini --no-alarm
```

---

## 七、配置文件完整示例

```ini
[GLOBAL]
username = zhangsan@example.com
password = MyPassword123
browser = chrome

[TICKET]
date = 2026-02-15
from_station = 广州
to_station = 北京
trains = G123,D456,G789
ticket_type = 二等座,一等座
people = 张三,李四
student = N
tolerance = 5
alarm = Y
range_query = N

[STATIONCOOKIE]
广州 = %u5E7F%u5DDE%2CGZQ
北京 = %u5317%u4EAC%2CBJP
上海 = %u4E0A%u6D77%2CSHH
深圳 = %u6DF1%u5733%2CSZQ
杭州 = %u676D%u5DDE%2CHZH
南京 = %u5357%u4EAC%2CNJH
```

---

## 八、检查清单

在运行程序前，请确认：

- [ ] Python 3.7+ 已安装
- [ ] Chrome 浏览器已安装
- [ ] 依赖包已安装（`pip3 install -r requirements.txt`）
- [ ] 配置文件已创建（`conf/conf.ini`）
- [ ] 用户名和密码已填写
- [ ] 日期、车站、车次已配置
- [ ] 乘车人已配置（必须是12306账号中的联系人）
- [ ] 所有车站的 Cookie 已获取并配置
- [ ] 配置验证通过（运行时显示 ✅）

---

## 九、性能优化建议

### 1. 减少查询组合
- 尽量减少车站和日期的组合数量
- 明确指定车次而不是查询所有车次

### 2. 合理设置容忍次数
- 热门车次可以设置较高的容忍次数（如 10）
- 冷门车次可以设置较低的容忍次数（如 3）

### 3. 网络环境
- 使用稳定的网络连接
- 避免使用 VPN（可能被12306检测）

---

## 十、安全提示

⚠️ **重要安全提示**：

1. **配置文件安全**
   - `conf/conf.ini` 包含你的账号密码
   - 不要将此文件上传到公共代码仓库
   - 不要分享给他人

2. **合法使用**
   - 本工具仅供个人学习和合法购票使用
   - 不要用于商业倒票
   - 遵守12306服务条款

3. **账号安全**
   - 使用后建议修改密码
   - 定期检查账号登录记录

---

## 需要帮助？

如遇到问题：
1. 检查本文档的"常见问题"部分
2. 查看 `MODERNIZATION_SUMMARY.md` 了解技术细节
3. 查看 `README.md` 了解项目背景

**祝你抢票成功！** 🎫✨
