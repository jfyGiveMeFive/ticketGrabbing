#!/bin/bash
# 一键部署脚本 - 快速设置和运行 12306 抢票工具

set -e  # 遇到错误立即退出

echo "============================================================"
echo "12306 抢票工具 - 一键部署脚本"
echo "============================================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Python 版本
echo "步骤 1/5: 检查 Python 版本..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} 找到 Python $PYTHON_VERSION"

    # 检查版本是否 >= 3.7
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 7 ]); then
        echo -e "${RED}✗${NC} Python 版本过低，需要 Python 3.7+"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} 未找到 Python 3，请先安装 Python 3.7+"
    exit 1
fi

# 检查 Chrome 浏览器
echo ""
echo "步骤 2/5: 检查 Chrome 浏览器..."
if [ -d "/Applications/Google Chrome.app" ] || command -v google-chrome &> /dev/null || command -v chromium &> /dev/null; then
    echo -e "${GREEN}✓${NC} Chrome 浏览器已安装"
else
    echo -e "${YELLOW}⚠${NC} 未检测到 Chrome 浏览器"
    echo "请从以下地址下载安装: https://www.google.com/chrome/"
    read -p "已安装 Chrome？按回车继续，或 Ctrl+C 退出..."
fi

# 安装依赖
echo ""
echo "步骤 3/5: 安装 Python 依赖包..."
if [ -f "requirements.txt" ]; then
    echo "正在安装依赖..."
    pip3 install -r requirements.txt --user
    echo -e "${GREEN}✓${NC} 依赖安装完成"
else
    echo -e "${RED}✗${NC} 未找到 requirements.txt 文件"
    exit 1
fi

# 创建配置文件
echo ""
echo "步骤 4/5: 创建配置文件..."
if [ ! -f "conf/conf.ini" ]; then
    if [ -f "conf/conf.ini.template" ]; then
        cp conf/conf.ini.template conf/conf.ini
        echo -e "${GREEN}✓${NC} 配置文件已创建: conf/conf.ini"
        echo -e "${YELLOW}⚠${NC} 请编辑 conf/conf.ini 填入你的账号信息"
    else
        echo -e "${RED}✗${NC} 未找到配置模板文件"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} 配置文件已存在: conf/conf.ini"
fi

# 运行验证脚本
echo ""
echo "步骤 5/5: 验证环境..."
if [ -f "verify_modernization.py" ]; then
    python3 verify_modernization.py
else
    echo -e "${YELLOW}⚠${NC} 验证脚本不存在，跳过验证"
fi

# 完成提示
echo ""
echo "============================================================"
echo -e "${GREEN}部署完成！${NC}"
echo "============================================================"
echo ""
echo "下一步操作："
echo "1. 编辑配置文件:"
echo "   nano conf/conf.ini"
echo "   或"
echo "   open -a TextEdit conf/conf.ini"
echo ""
echo "2. 填写以下必填信息:"
echo "   - 用户名和密码"
echo "   - 出发日期"
echo "   - 起始站和到达站"
echo "   - 车次（可选）"
echo "   - 乘车人"
echo "   - 车站 Cookie（重要！）"
echo ""
echo "3. 获取车站 Cookie 的方法:"
echo "   - 打开 https://kyfw.12306.cn/otn/leftTicket/init"
echo "   - 输入起始站、到达站，点击查询"
echo "   - 按 F12 打开开发者工具"
echo "   - Application > Cookies > https://kyfw.12306.cn"
echo "   - 复制 _jc_save_fromStation 和 _jc_save_toStation 的值"
echo ""
echo "4. 运行程序:"
echo "   python3 crawler.py conf/conf.ini"
echo ""
echo "5. 查看详细文档:"
echo "   - 快速开始: cat QUICK_START.md"
echo "   - 使用帮助: python3 crawler.py --help"
echo ""
echo "祝你抢票成功！🎫"
echo ""
