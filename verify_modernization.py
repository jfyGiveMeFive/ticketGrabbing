#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证脚本 - 检查现代化改造是否成功
"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """检查 Python 版本"""
    print("=" * 60)
    print("1. 检查 Python 版本")
    print("=" * 60)
    version = sys.version_info
    print(f"当前 Python 版本: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 版本过低，需要 Python 3.7+")
        return False
    else:
        print("✅ Python 版本符合要求")
        return True

def check_dependencies():
    """检查依赖包"""
    print("\n" + "=" * 60)
    print("2. 检查依赖包")
    print("=" * 60)

    dependencies = {
        'undetected_chromedriver': 'undetected-chromedriver',
        'selenium': 'selenium',
        'pygame': 'pygame'
    }

    all_installed = True
    for module, package in dependencies.items():
        spec = importlib.util.find_spec(module)
        if spec is None:
            print(f"❌ {package} 未安装")
            all_installed = False
        else:
            try:
                mod = importlib.import_module(module)
                version = getattr(mod, '__version__', '未知版本')
                print(f"✅ {package} 已安装 (版本: {version})")
            except:
                print(f"✅ {package} 已安装")

    return all_installed

def check_syntax():
    """检查 Python 语法"""
    print("\n" + "=" * 60)
    print("3. 检查 Python 语法")
    print("=" * 60)

    try:
        result = subprocess.run(
            ['python3', '-m', 'py_compile', 'crawler.py'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print("✅ crawler.py 语法检查通过")
            return True
        else:
            print("❌ crawler.py 语法错误:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 语法检查失败: {e}")
        return False

def check_imports():
    """检查关键导入"""
    print("\n" + "=" * 60)
    print("4. 检查关键导入")
    print("=" * 60)

    try:
        # 检查是否能导入关键模块
        import undetected_chromedriver as uc
        print("✅ undetected_chromedriver 导入成功")

        from selenium import webdriver
        print("✅ selenium.webdriver 导入成功")

        from selenium.webdriver.remote.webelement import WebElement
        print("✅ WebElement 导入成功")

        from configparser import ConfigParser
        print("✅ ConfigParser 导入成功")

        import argparse
        print("✅ argparse 导入成功")

        import pygame
        print("✅ pygame 导入成功")

        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def check_command_line():
    """检查命令行参数"""
    print("\n" + "=" * 60)
    print("5. 检查命令行参数功能")
    print("=" * 60)

    try:
        result = subprocess.run(
            ['python3', 'crawler.py', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0 and '12306 火车票自动抢票工具' in result.stdout:
            print("✅ 命令行参数功能正常")
            print("\n可用参数:")
            for line in result.stdout.split('\n'):
                if line.strip().startswith('--'):
                    print(f"  {line.strip()}")
            return True
        else:
            print("❌ 命令行参数功能异常")
            return False
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False

def check_files():
    """检查文件完整性"""
    print("\n" + "=" * 60)
    print("6. 检查文件完整性")
    print("=" * 60)

    import os

    required_files = {
        'crawler.py': '主程序文件',
        'requirements.txt': '依赖清单',
        'README.md': '项目文档',
        'conf/conf.ini.template': '配置模板',
        'media/sound.ogg': '提醒音乐',
        'media/img.jpg': '提醒图片'
    }

    all_exist = True
    for file, desc in required_files.items():
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({desc}) - {size} 字节")
        else:
            print(f"❌ {file} ({desc}) - 文件不存在")
            all_exist = False

    return all_exist

def check_python2_syntax():
    """检查是否还有 Python 2 语法"""
    print("\n" + "=" * 60)
    print("7. 检查 Python 2 语法残留")
    print("=" * 60)

    with open('crawler.py', 'r', encoding='utf-8') as f:
        content = f.read()

    python2_patterns = [
        ('reload(sys)', 'reload() 函数'),
        ('sys.setdefaultencoding', 'setdefaultencoding()'),
        ('.iteritems()', 'dict.iteritems()'),
        ('print "', 'print 语句'),
        ('configparser.RawConfigParser', 'RawConfigParser'),
        ('.readfp(', 'readfp() 方法')
    ]

    found_issues = False
    for pattern, desc in python2_patterns:
        if pattern in content:
            print(f"❌ 发现 Python 2 语法: {desc}")
            found_issues = True

    if not found_issues:
        print("✅ 未发现 Python 2 语法残留")
        return True
    else:
        return False

def check_new_features():
    """检查新功能是否存在"""
    print("\n" + "=" * 60)
    print("8. 检查新功能")
    print("=" * 60)

    with open('crawler.py', 'r', encoding='utf-8') as f:
        content = f.read()

    features = [
        ('def validate_config(self):', '配置验证功能'),
        ('import undetected_chromedriver as uc', 'undetected-chromedriver'),
        ('parser = argparse.ArgumentParser', '命令行参数解析'),
        ('uc.Chrome(options=options', 'undetected Chrome 初始化'),
        ("'--date'", '日期参数'),
        ("'--trains'", '车次参数'),
        ("'--no-alarm'", '禁用提醒参数')
    ]

    all_exist = True
    for pattern, desc in features:
        if pattern in content:
            print(f"✅ {desc} 已实现")
        else:
            print(f"❌ {desc} 未找到")
            all_exist = False

    return all_exist

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("12306 抢票工具现代化改造验证脚本")
    print("=" * 60)

    results = []

    # 执行所有检查
    results.append(("Python 版本", check_python_version()))
    results.append(("依赖包", check_dependencies()))
    results.append(("Python 语法", check_syntax()))
    results.append(("关键导入", check_imports()))
    results.append(("命令行参数", check_command_line()))
    results.append(("文件完整性", check_files()))
    results.append(("Python 2 语法清理", check_python2_syntax()))
    results.append(("新功能实现", check_new_features()))

    # 汇总结果
    print("\n" + "=" * 60)
    print("验证结果汇总")
    print("=" * 60)

    passed = 0
    failed = 0

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:20s} {status}")
        if result:
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print(f"总计: {passed} 项通过, {failed} 项失败")
    print("=" * 60)

    if failed == 0:
        print("\n🎉 所有检查通过！现代化改造成功完成！")
        print("\n下一步:")
        print("1. 配置 conf/conf.ini 文件")
        print("2. 运行: python3 crawler.py conf/conf.ini")
        print("3. 查看 QUICK_START.md 了解详细使用方法")
        return 0
    else:
        print(f"\n⚠️  有 {failed} 项检查失败，请检查上述错误信息")
        if not results[1][1]:  # 依赖包检查失败
            print("\n建议运行: pip3 install -r requirements.txt")
        return 1

if __name__ == '__main__':
    sys.exit(main())
