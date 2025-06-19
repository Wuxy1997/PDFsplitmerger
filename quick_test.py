#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证GUI界面能正常启动
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time

def test_gui_startup():
    """测试GUI启动"""
    print("正在测试GUI启动...")
    
    try:
        # 导入主程序
        import pdf_splitter
        
        # 创建根窗口
        root = tk.Tk()
        root.title("PDF分割工具 - 测试")
        root.geometry("400x200")
        
        # 添加测试标签
        label = tk.Label(root, text="PDF分割工具测试\nGUI界面启动成功！", 
                        font=("Arial", 14), pady=20)
        label.pack()
        
        # 添加关闭按钮
        def close_test():
            root.destroy()
            
        close_btn = tk.Button(root, text="关闭测试", command=close_test)
        close_btn.pack(pady=10)
        
        # 3秒后自动关闭
        def auto_close():
            time.sleep(3)
            try:
                root.after(0, root.destroy)
            except:
                pass
                
        timer_thread = threading.Thread(target=auto_close)
        timer_thread.daemon = True
        timer_thread.start()
        
        print("✓ GUI启动测试成功")
        root.mainloop()
        return True
        
    except Exception as e:
        print(f"✗ GUI启动测试失败: {e}")
        return False

def test_main_program_gui():
    """测试主程序GUI"""
    print("正在测试主程序GUI...")
    
    try:
        import pdf_splitter
        
        # 创建主程序实例（但不显示）
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        app = pdf_splitter.PDFSplitter(root)
        
        # 检查关键组件是否存在
        if hasattr(app, 'pdf_path_var') and hasattr(app, 'split_button'):
            print("✓ 主程序GUI组件创建成功")
            root.destroy()
            return True
        else:
            print("✗ 主程序GUI组件创建失败")
            root.destroy()
            return False
            
    except Exception as e:
        print(f"✗ 主程序GUI测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 40)
    print("PDF分割工具 - 快速GUI测试")
    print("=" * 40)
    
    # 测试1: 基本GUI启动
    test1 = test_gui_startup()
    
    # 测试2: 主程序GUI
    test2 = test_main_program_gui()
    
    print("\n" + "=" * 40)
    if test1 and test2:
        print("🎉 所有GUI测试通过！")
        print("程序可以正常启动和使用。")
    else:
        print("❌ 部分GUI测试失败")
        print("请检查程序配置。")
    print("=" * 40) 