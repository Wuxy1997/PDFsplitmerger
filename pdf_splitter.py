import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import PyPDF2
from pathlib import Path
import threading
import re

class PDFSplitter:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF分割工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        self.pdf_path = ""
        self.output_dir = ""
        self.pdf_reader = None
        self.total_pages = 0
        self.pdf_file_obj = None  # 新增：用于保存打开的PDF文件对象
        
        self.create_widgets()
        
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="PDF文件:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.pdf_path_var = tk.StringVar()
        self.pdf_entry = ttk.Entry(file_frame, textvariable=self.pdf_path_var, state="readonly")
        self.pdf_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(file_frame, text="浏览", command=self.select_pdf).grid(row=0, column=2)
        
        ttk.Label(file_frame, text="输出目录:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        self.output_path_var = tk.StringVar()
        self.output_entry = ttk.Entry(file_frame, textvariable=self.output_path_var, state="readonly")
        self.output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(10, 0))
        ttk.Button(file_frame, text="浏览", command=self.select_output_dir).grid(row=1, column=2, pady=(10, 0))
        
        # PDF信息显示
        info_frame = ttk.LabelFrame(main_frame, text="PDF信息", padding="10")
        info_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=6, width=80)
        self.info_text.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # 分割方式选择
        split_frame = ttk.LabelFrame(main_frame, text="分割方式", padding="10")
        split_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.split_method = tk.StringVar(value="range")
        
        # 按页面范围分割
        range_frame = ttk.Frame(split_frame)
        range_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        range_frame.columnconfigure(1, weight=1)
        
        ttk.Radiobutton(range_frame, text="按页面范围分割", variable=self.split_method, 
                       value="range", command=self.on_method_change).grid(row=0, column=0, sticky=tk.W)
        
        self.range_frame = ttk.Frame(range_frame)
        self.range_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        self.range_frame.columnconfigure(1, weight=1)
        
        ttk.Label(self.range_frame, text="页面范围 (例如: 1-5, 8-12, 15):").grid(row=0, column=0, sticky=tk.W, padx=(20, 5))
        self.range_var = tk.StringVar()
        self.range_entry = ttk.Entry(self.range_frame, textvariable=self.range_var)
        self.range_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Label(self.range_frame, text="(用逗号分隔多个范围)").grid(row=0, column=2, sticky=tk.W)
        
        # 按页数分割
        pages_frame = ttk.Frame(split_frame)
        pages_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        pages_frame.columnconfigure(1, weight=1)
        
        ttk.Radiobutton(pages_frame, text="按页数分割", variable=self.split_method, 
                       value="pages", command=self.on_method_change).grid(row=0, column=0, sticky=tk.W)
        
        self.pages_frame = ttk.Frame(pages_frame)
        self.pages_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        self.pages_frame.columnconfigure(1, weight=1)
        
        ttk.Label(self.pages_frame, text="每份页数:").grid(row=0, column=0, sticky=tk.W, padx=(20, 5))
        self.pages_per_split_var = tk.StringVar()
        self.pages_per_split_entry = ttk.Entry(self.pages_frame, textvariable=self.pages_per_split_var)
        self.pages_per_split_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # 按书签分割
        bookmark_frame = ttk.Frame(split_frame)
        bookmark_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        bookmark_frame.columnconfigure(1, weight=1)
        
        ttk.Radiobutton(bookmark_frame, text="按书签分割", variable=self.split_method, 
                       value="bookmark", command=self.on_method_change).grid(row=0, column=0, sticky=tk.W)
        
        self.bookmark_frame = ttk.Frame(bookmark_frame)
        self.bookmark_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        self.bookmark_frame.columnconfigure(1, weight=1)
        
        ttk.Label(self.bookmark_frame, text="书签级别:").grid(row=0, column=0, sticky=tk.W, padx=(20, 5))
        self.bookmark_level_var = tk.StringVar(value="1")
        self.bookmark_level_combo = ttk.Combobox(self.bookmark_frame, textvariable=self.bookmark_level_var, 
                                                values=["1", "2", "3", "4", "5"], state="readonly", width=10)
        self.bookmark_level_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 5))
        
        # 自定义分割
        custom_frame = ttk.Frame(split_frame)
        custom_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        custom_frame.columnconfigure(1, weight=1)
        
        ttk.Radiobutton(custom_frame, text="自定义分割", variable=self.split_method, 
                       value="custom", command=self.on_method_change).grid(row=0, column=0, sticky=tk.W)
        
        self.custom_frame = ttk.Frame(custom_frame)
        self.custom_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        self.custom_frame.columnconfigure(1, weight=1)
        
        ttk.Label(self.custom_frame, text="分割点 (例如: 5,10,15):").grid(row=0, column=0, sticky=tk.W, padx=(20, 5))
        self.custom_var = tk.StringVar()
        self.custom_entry = ttk.Entry(self.custom_frame, textvariable=self.custom_var)
        self.custom_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Label(self.custom_frame, text="(在指定页面前分割)").grid(row=0, column=2, sticky=tk.W)
        
        # 输出选项
        output_frame = ttk.LabelFrame(main_frame, text="输出选项", padding="10")
        output_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.prefix_var = tk.StringVar(value="split_")
        ttk.Label(output_frame, text="文件名前缀:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.prefix_entry = ttk.Entry(output_frame, textvariable=self.prefix_var, width=20)
        self.prefix_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        self.overwrite_var = tk.BooleanVar(value=False)
        self.overwrite_check = ttk.Checkbutton(output_frame, text="覆盖已存在的文件", 
                                              variable=self.overwrite_var)
        self.overwrite_check.grid(row=0, column=2, sticky=tk.W)
        
        # 进度条和状态
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        self.split_button = ttk.Button(button_frame, text="开始分割", command=self.start_split)
        self.split_button.grid(row=0, column=0, padx=(0, 10))
        
        # 新增：合并PDF按钮
        self.merge_button = ttk.Button(button_frame, text="合并PDF", command=self.open_merge_window)
        self.merge_button.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(button_frame, text="退出", command=self.root.quit).grid(row=0, column=2)
        
        # 初始化界面状态
        self.on_method_change()
        
    def select_pdf(self):
        file_path = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if file_path:
            self.pdf_path = file_path
            self.pdf_path_var.set(file_path)
            self.load_pdf_info()
            
    def select_output_dir(self):
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_dir = dir_path
            self.output_path_var.set(dir_path)
            
    def load_pdf_info(self):
        try:
            # 关闭之前的文件对象
            if self.pdf_file_obj:
                self.pdf_file_obj.close()
            self.pdf_file_obj = open(self.pdf_path, 'rb')
            self.pdf_reader = PyPDF2.PdfReader(self.pdf_file_obj)
            self.total_pages = len(self.pdf_reader.pages)
            
            info = f"文件名: {os.path.basename(self.pdf_path)}\n"
            info += f"总页数: {self.total_pages}\n"
            info += f"文件大小: {os.path.getsize(self.pdf_path) / 1024 / 1024:.2f} MB\n"
            
            # 显示书签信息
            if self.pdf_reader.outline:
                info += f"书签数量: {len(self.pdf_reader.outline)}\n"
                info += "书签结构:\n"
                self.display_bookmarks(self.pdf_reader.outline, info, 0)
            else:
                info += "无书签\n"
                
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info)
            
        except Exception as e:
            messagebox.showerror("错误", f"无法读取PDF文件: {str(e)}")
            
    def display_bookmarks(self, bookmarks, info, level):
        for i, bookmark in enumerate(bookmarks):
            indent = "  " * level
            if isinstance(bookmark, list):
                self.display_bookmarks(bookmark, info, level + 1)
            else:
                page_num = bookmark.page + 1 if hasattr(bookmark, 'page') else "未知"
                info += f"{indent}- {bookmark.title} (第{page_num}页)\n"
                
    def on_method_change(self):
        # 隐藏所有框架
        for frame in [self.range_frame, self.pages_frame, self.bookmark_frame, self.custom_frame]:
            frame.grid_remove()
            
        # 显示选中的框架
        method = self.split_method.get()
        if method == "range":
            self.range_frame.grid()
        elif method == "pages":
            self.pages_frame.grid()
        elif method == "bookmark":
            self.bookmark_frame.grid()
        elif method == "custom":
            self.custom_frame.grid()
            
    def validate_inputs(self):
        if not self.pdf_path:
            messagebox.showerror("错误", "请选择PDF文件")
            return False
            
        if not self.output_dir:
            messagebox.showerror("错误", "请选择输出目录")
            return False
            
        if not self.pdf_reader:
            messagebox.showerror("错误", "PDF文件未正确加载")
            return False
            
        method = self.split_method.get()
        
        if method == "range":
            if not self.range_var.get().strip():
                messagebox.showerror("错误", "请输入页面范围")
                return False
                
        elif method == "pages":
            try:
                pages = int(self.pages_per_split_var.get())
                if pages <= 0 or pages > self.total_pages:
                    messagebox.showerror("错误", f"每份页数必须在1到{self.total_pages}之间")
                    return False
            except ValueError:
                messagebox.showerror("错误", "请输入有效的页数")
                return False
                
        elif method == "custom":
            if not self.custom_var.get().strip():
                messagebox.showerror("错误", "请输入分割点")
                return False
                
        return True
        
    def parse_range(self, range_str):
        """解析页面范围字符串"""
        ranges = []
        parts = range_str.split(',')
        
        for part in parts:
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                try:
                    start = int(start.strip())
                    end = int(end.strip())
                    if start > 0 and end <= self.total_pages and start <= end:
                        ranges.append((start-1, end-1))  # 转换为0索引
                    else:
                        raise ValueError(f"无效范围: {part}")
                except ValueError:
                    raise ValueError(f"无效范围格式: {part}")
            else:
                try:
                    page = int(part)
                    if page > 0 and page <= self.total_pages:
                        ranges.append((page-1, page-1))  # 转换为0索引
                    else:
                        raise ValueError(f"无效页码: {part}")
                except ValueError:
                    raise ValueError(f"无效页码格式: {part}")
                    
        return ranges
        
    def parse_custom_points(self, custom_str):
        """解析自定义分割点"""
        try:
            points = [int(x.strip()) for x in custom_str.split(',')]
            points = [p for p in points if p > 0 and p < self.total_pages]
            points.sort()
            return points
        except ValueError:
            raise ValueError("自定义分割点格式错误")
            
    def get_bookmark_pages(self, level=1):
        """获取指定级别的书签页面"""
        if not self.pdf_reader.outline:
            return []
            
        pages = []
        self.extract_bookmark_pages(self.pdf_reader.outline, pages, level, 1)
        return sorted(list(set(pages)))
        
    def extract_bookmark_pages(self, bookmarks, pages, target_level, current_level):
        """递归提取书签页面"""
        for bookmark in bookmarks:
            if isinstance(bookmark, list):
                self.extract_bookmark_pages(bookmark, pages, target_level, current_level + 1)
            else:
                if current_level == target_level and hasattr(bookmark, 'page'):
                    pages.append(bookmark.page)
                    
    def start_split(self):
        if not self.validate_inputs():
            return
            
        # 禁用按钮
        self.split_button.config(state="disabled")
        
        # 在新线程中执行分割
        thread = threading.Thread(target=self.perform_split)
        thread.daemon = True
        thread.start()
        
    def perform_split(self):
        try:
            method = self.split_method.get()
            prefix = self.prefix_var.get()
            
            if method == "range":
                self.split_by_range(prefix)
            elif method == "pages":
                self.split_by_pages(prefix)
            elif method == "bookmark":
                self.split_by_bookmarks(prefix)
            elif method == "custom":
                self.split_by_custom(prefix)
                
            self.root.after(0, lambda: messagebox.showinfo("完成", "PDF分割完成！"))
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: messagebox.showerror("错误", f"分割失败: {error_msg}"))
        finally:
            # 分割完成后关闭PDF文件对象
            if self.pdf_file_obj:
                self.pdf_file_obj.close()
                self.pdf_file_obj = None
            self.root.after(0, lambda: self.split_button.config(state="normal"))
            
    def split_by_range(self, prefix):
        ranges = self.parse_range(self.range_var.get())
        
        for i, (start, end) in enumerate(ranges):
            self.status_var.set(f"正在分割第{i+1}个范围...")
            self.progress['value'] = (i + 1) / len(ranges) * 100
            self.root.update_idletasks()
            
            output_path = os.path.join(self.output_dir, f"{prefix}range_{i+1}.pdf")
            
            if os.path.exists(output_path) and not self.overwrite_var.get():
                continue
                
            writer = PyPDF2.PdfWriter()
            for page_num in range(start, end + 1):
                writer.add_page(self.pdf_reader.pages[page_num])
                
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
                
    def split_by_pages(self, prefix):
        pages_per_split = int(self.pages_per_split_var.get())
        total_splits = (self.total_pages + pages_per_split - 1) // pages_per_split
        
        for i in range(total_splits):
            self.status_var.set(f"正在分割第{i+1}/{total_splits}份...")
            self.progress['value'] = (i + 1) / total_splits * 100
            self.root.update_idletasks()
            
            start_page = i * pages_per_split
            end_page = min((i + 1) * pages_per_split, self.total_pages)
            
            output_path = os.path.join(self.output_dir, f"{prefix}part_{i+1}.pdf")
            
            if os.path.exists(output_path) and not self.overwrite_var.get():
                continue
                
            writer = PyPDF2.PdfWriter()
            for page_num in range(start_page, end_page):
                writer.add_page(self.pdf_reader.pages[page_num])
                
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
                
    def split_by_bookmarks(self, prefix):
        level = int(self.bookmark_level_var.get())
        bookmark_pages = self.get_bookmark_pages(level)
        
        if not bookmark_pages:
            raise ValueError("未找到指定级别的书签")
            
        # 添加开始和结束页
        all_pages = [0] + bookmark_pages + [self.total_pages]
        all_pages = sorted(list(set(all_pages)))
        
        for i in range(len(all_pages) - 1):
            self.status_var.set(f"正在分割第{i+1}个书签部分...")
            self.progress['value'] = (i + 1) / (len(all_pages) - 1) * 100
            self.root.update_idletasks()
            
            start_page = all_pages[i]
            end_page = all_pages[i + 1] - 1
            
            output_path = os.path.join(self.output_dir, f"{prefix}bookmark_{i+1}.pdf")
            
            if os.path.exists(output_path) and not self.overwrite_var.get():
                continue
                
            writer = PyPDF2.PdfWriter()
            for page_num in range(start_page, end_page + 1):
                writer.add_page(self.pdf_reader.pages[page_num])
                
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
                
    def split_by_custom(self, prefix):
        split_points = self.parse_custom_points(self.custom_var.get())
        
        if not split_points:
            raise ValueError("未找到有效的分割点")
            
        # 添加开始和结束页
        all_points = [0] + split_points + [self.total_pages]
        
        for i in range(len(all_points) - 1):
            self.status_var.set(f"正在分割第{i+1}个自定义部分...")
            self.progress['value'] = (i + 1) / (len(all_points) - 1) * 100
            self.root.update_idletasks()
            
            start_page = all_points[i]
            end_page = all_points[i + 1] - 1
            
            output_path = os.path.join(self.output_dir, f"{prefix}custom_{i+1}.pdf")
            
            if os.path.exists(output_path) and not self.overwrite_var.get():
                continue
                
            writer = PyPDF2.PdfWriter()
            for page_num in range(start_page, end_page + 1):
                writer.add_page(self.pdf_reader.pages[page_num])
                
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

    def open_merge_window(self):
        merge_win = tk.Toplevel(self.root)
        merge_win.title("合并PDF文件")
        merge_win.geometry("600x400")
        merge_win.grab_set()
        
        # 文件列表
        file_list = []
        
        def refresh_listbox():
            listbox.delete(0, tk.END)
            for f in file_list:
                listbox.insert(tk.END, f)
        
        def add_files():
            files = filedialog.askopenfilenames(
                title="选择要合并的PDF文件",
                filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
            )
            for f in files:
                if f not in file_list:
                    file_list.append(f)
            refresh_listbox()
        
        def remove_file():
            sel = listbox.curselection()
            for idx in reversed(sel):
                del file_list[idx]
            refresh_listbox()
        
        def move_up():
            sel = listbox.curselection()
            if not sel or sel[0] == 0:
                return
            idx = sel[0]
            file_list[idx-1], file_list[idx] = file_list[idx], file_list[idx-1]
            refresh_listbox()
            listbox.selection_set(idx-1)
        
        def move_down():
            sel = listbox.curselection()
            if not sel or sel[0] == len(file_list)-1:
                return
            idx = sel[0]
            file_list[idx+1], file_list[idx] = file_list[idx], file_list[idx+1]
            refresh_listbox()
            listbox.selection_set(idx+1)
        
        # 文件列表框
        listbox = tk.Listbox(merge_win, selectmode=tk.EXTENDED, width=60, height=10)
        listbox.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky=tk.W+tk.E)
        
        ttk.Button(merge_win, text="添加文件", command=add_files).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(merge_win, text="移除选中", command=remove_file).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(merge_win, text="上移", command=move_up).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(merge_win, text="下移", command=move_down).grid(row=1, column=3, padx=5, pady=5)
        
        # 输出目录和文件名
        out_dir_var = tk.StringVar()
        out_name_var = tk.StringVar(value="merged.pdf")
        
        def select_out_dir():
            d = filedialog.askdirectory(title="选择输出目录")
            if d:
                out_dir_var.set(d)
        
        ttk.Label(merge_win, text="输出目录:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=(20, 5))
        out_dir_entry = ttk.Entry(merge_win, textvariable=out_dir_var, width=40)
        out_dir_entry.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=(20, 5))
        ttk.Button(merge_win, text="浏览", command=select_out_dir).grid(row=2, column=3, pady=(20, 5))
        
        ttk.Label(merge_win, text="输出文件名:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        out_name_entry = ttk.Entry(merge_win, textvariable=out_name_var, width=40)
        out_name_entry.grid(row=3, column=1, columnspan=2, sticky=tk.W, pady=5)
        ttk.Label(merge_win, text=".pdf").grid(row=3, column=3, sticky=tk.W, pady=5)
        
        # 合并操作
        def do_merge():
            if not file_list:
                messagebox.showerror("错误", "请添加要合并的PDF文件！", parent=merge_win)
                return
            if not out_dir_var.get():
                messagebox.showerror("错误", "请选择输出目录！", parent=merge_win)
                return
            out_name = out_name_var.get().strip()
            if not out_name or not out_name.lower().endswith('.pdf'):
                messagebox.showerror("错误", "请输入有效的输出文件名（以.pdf结尾）！", parent=merge_win)
                return
            out_path = os.path.join(out_dir_var.get(), out_name)
            try:
                merger = PyPDF2.PdfMerger()
                for f in file_list:
                    merger.append(f)
                merger.write(out_path)
                merger.close()
                messagebox.showinfo("完成", f"合并完成！输出文件：\n{out_path}", parent=merge_win)
            except Exception as e:
                messagebox.showerror("错误", f"合并失败: {e}", parent=merge_win)
        
        ttk.Button(merge_win, text="开始合并", command=do_merge).grid(row=4, column=0, columnspan=4, pady=20)

def main():
    root = tk.Tk()
    app = PDFSplitter(root)
    root.mainloop()

if __name__ == "__main__":
    main() 