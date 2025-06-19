#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语言切换功能测试脚本
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time

def test_language_switching():
    """测试语言切换功能"""
    print("正在测试语言切换功能...")
    
    try:
        import pdf_splitter
        
        # 创建根窗口
        root = tk.Tk()
        root.title("语言切换测试")
        root.geometry("400x300")
        
        # 创建应用实例
        app = pdf_splitter.PDFSplitter(root)
        
        # 测试语言切换
        print("✓ 应用创建成功")
        
        # 测试初始语言
        initial_lang = app.current_language
        print(f"✓ 初始语言: {initial_lang}")
        
        # 测试语言切换
        app.switch_language()
        new_lang = app.current_language
        print(f"✓ 切换后语言: {new_lang}")
        
        # 验证语言确实切换了
        if initial_lang != new_lang:
            print("✓ 语言切换成功")
        else:
            print("✗ 语言切换失败")
            return False
            
        # 测试文本获取
        test_text = app.get_text('title')
        print(f"✓ 获取文本: {test_text}")
        
        # 测试界面更新
        try:
            app.update_ui_text()
            print("✓ 界面文本更新成功")
        except Exception as e:
            print(f"✗ 界面文本更新失败: {e}")
            return False
            
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ 语言切换测试失败: {e}")
        return False

def test_language_dictionary():
    """测试语言字典"""
    print("正在测试语言字典...")
    
    try:
        import pdf_splitter
        
        # 检查语言字典是否存在
        if hasattr(pdf_splitter, 'LANGUAGES'):
            print("✓ 语言字典存在")
            
            # 检查中英文是否都有
            if 'zh' in pdf_splitter.LANGUAGES and 'en' in pdf_splitter.LANGUAGES:
                print("✓ 中英文语言包都存在")
                
                # 检查关键文本
                zh_texts = pdf_splitter.LANGUAGES['zh']
                en_texts = pdf_splitter.LANGUAGES['en']
                
                key_texts = ['title', 'start_split', 'merge_pdf', 'exit']
                for key in key_texts:
                    if key in zh_texts and key in en_texts:
                        print(f"✓ {key}: {zh_texts[key]} / {en_texts[key]}")
                    else:
                        print(f"✗ 缺少文本: {key}")
                        return False
                        
                return True
            else:
                print("✗ 语言包不完整")
                return False
        else:
            print("✗ 语言字典不存在")
            return False
            
    except Exception as e:
        print(f"✗ 语言字典测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("语言切换功能测试")
    print("=" * 50)
    
    tests = [
        ("语言字典", test_language_dictionary),
        ("语言切换", test_language_switching),
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
        print("🎉 语言切换功能测试通过！")
        print("现在可以正常使用中英文切换功能。")
        return True
    else:
        print("❌ 部分语言切换测试失败。")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1) 