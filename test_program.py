#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF分割工具测试脚本
用于验证程序的基本功能
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def test_imports():
    """测试必要的模块导入"""
    print("正在测试模块导入...")
    
    try:
        import PyPDF2
        print("✓ PyPDF2 导入成功")
    except ImportError as e:
        print(f"✗ PyPDF2 导入失败: {e}")
        return False
    
    try:
        import tkinter
        print("✓ tkinter 导入成功")
    except ImportError as e:
        print(f"✗ tkinter 导入失败: {e}")
        return False
    
    return True

def test_gui():
    """测试GUI功能"""
    print("正在测试GUI功能...")
    
    try:
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        # 测试消息框
        messagebox.showinfo("测试", "GUI功能正常")
        print("✓ GUI功能测试成功")
        
        root.destroy()
        return True
    except Exception as e:
        print(f"✗ GUI功能测试失败: {e}")
        return False

def test_pdf_operations():
    """测试PDF操作功能"""
    print("正在测试PDF操作功能...")
    
    try:
        import PyPDF2
        
        # 创建一个简单的测试PDF（如果可能的话）
        writer = PyPDF2.PdfWriter()
        print("✓ PDF写入器创建成功")
        
        # 测试PDF读取器
        reader = PyPDF2.PdfReader
        print("✓ PDF读取器可用")
        
        return True
    except Exception as e:
        print(f"✗ PDF操作测试失败: {e}")
        return False

def test_main_program():
    """测试主程序"""
    print("正在测试主程序...")
    
    try:
        # 尝试导入主程序
        import pdf_splitter
        print("✓ 主程序导入成功")
        
        # 检查主程序类是否存在
        if hasattr(pdf_splitter, 'PDFSplitter'):
            print("✓ PDFSplitter类存在")
        else:
            print("✗ PDFSplitter类不存在")
            return False
            
        return True
    except Exception as e:
        print(f"✗ 主程序测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("PDF分割工具功能测试")
    print("=" * 50)
    
    tests = [
        ("模块导入", test_imports),
        ("GUI功能", test_gui),
        ("PDF操作", test_pdf_operations),
        ("主程序", test_main_program),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！程序可以正常使用。")
        print("\n启动方法:")
        print("1. 双击 run.bat 文件")
        print("2. 或在命令行运行: python pdf_splitter.py")
        return True
    else:
        print("❌ 部分测试失败，请检查安装。")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 