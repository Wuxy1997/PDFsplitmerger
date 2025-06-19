import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import PyPDF2
from pathlib import Path
import threading
import re

# 语言字典
LANGUAGES = {
    'zh': {
        'title': 'PDF分割工具',
        'file_selection': '文件选择',
        'pdf_file': 'PDF文件:',
        'output_dir': '输出目录:',
        'browse': '浏览',
        'pdf_info': 'PDF信息',
        'split_method': '分割方式',
        'range_split': '按页面范围分割',
        'pages_split': '按页数分割',
        'bookmark_split': '按书签分割',
        'custom_split': '自定义分割',
        'page_range': '页面范围 (例如: 1-5, 8-12, 15):',
        'range_help': '(用逗号分隔多个范围)',
        'pages_per_split': '每份页数:',
        'bookmark_level': '书签级别:',
        'custom_points': '分割点 (例如: 5,10,15):',
        'custom_help': '(在指定页面前分割)',
        'output_options': '输出选项',
        'filename_prefix': '文件名前缀:',
        'overwrite_files': '覆盖已存在的文件',
        'ready': '就绪',
        'start_split': '开始分割',
        'merge_pdf': '合并PDF',
        'exit': '退出',
        'processing': '正在处理...',
        'split_complete': 'PDF分割完成！',
        'merge_complete': '合并完成！输出文件：',
        'error': '错误',
        'no_pdf_selected': '请选择PDF文件',
        'no_output_dir': '请选择输出目录',
        'invalid_range': '页面范围格式错误',
        'invalid_pages': '页数必须是正整数',
        'invalid_custom': '自定义分割点格式错误',
        'no_bookmarks': 'PDF文件不包含书签',
        'split_failed': '分割失败',
        'merge_failed': '合并失败',
        'select_pdf_files': '选择要合并的PDF文件',
        'add_files': '添加文件',
        'remove_selected': '移除选中',
        'move_up': '上移',
        'move_down': '下移',
        'output_directory': '输出目录:',
        'output_filename': '输出文件名:',
        'start_merge': '开始合并',
        'add_merge_files': '请添加要合并的PDF文件！',
        'select_output_dir': '请选择输出目录！',
        'invalid_filename': '请输入有效的输出文件名（以.pdf结尾）！',
        'merge_window_title': '合并PDF文件',
        'language': '语言',
        'chinese': '中文',
        'english': 'English',
        'file_size': '文件大小',
        'total_pages': '总页数',
        'bookmark_count': '书签数量',
        'bookmark_structure': '书签结构',
        'no_bookmarks_found': '无书签',
        'filename': '文件名',
        'mb': 'MB',
        'pages': '页',
        'level': '级别',
        'unknown_page': '未知',
    },
    'en': {
        'title': 'PDF Splitter Tool',
        'file_selection': 'File Selection',
        'pdf_file': 'PDF File:',
        'output_dir': 'Output Directory:',
        'browse': 'Browse',
        'pdf_info': 'PDF Information',
        'split_method': 'Split Method',
        'range_split': 'Split by Page Range',
        'pages_split': 'Split by Page Count',
        'bookmark_split': 'Split by Bookmarks',
        'custom_split': 'Custom Split',
        'page_range': 'Page Range (e.g., 1-5, 8-12, 15):',
        'range_help': '(separate multiple ranges with commas)',
        'pages_per_split': 'Pages per Split:',
        'bookmark_level': 'Bookmark Level:',
        'custom_points': 'Split Points (e.g., 5,10,15):',
        'custom_help': '(split before specified pages)',
        'output_options': 'Output Options',
        'filename_prefix': 'Filename Prefix:',
        'overwrite_files': 'Overwrite Existing Files',
        'ready': 'Ready',
        'start_split': 'Start Split',
        'merge_pdf': 'Merge PDF',
        'exit': 'Exit',
        'processing': 'Processing...',
        'split_complete': 'PDF Split Complete!',
        'merge_complete': 'Merge Complete! Output File:',
        'error': 'Error',
        'no_pdf_selected': 'Please select a PDF file',
        'no_output_dir': 'Please select output directory',
        'invalid_range': 'Invalid page range format',
        'invalid_pages': 'Page count must be a positive integer',
        'invalid_custom': 'Invalid custom split points format',
        'no_bookmarks': 'PDF file contains no bookmarks',
        'split_failed': 'Split Failed',
        'merge_failed': 'Merge Failed',
        'select_pdf_files': 'Select PDF Files to Merge',
        'add_files': 'Add Files',
        'remove_selected': 'Remove Selected',
        'move_up': 'Move Up',
        'move_down': 'Move Down',
        'output_directory': 'Output Directory:',
        'output_filename': 'Output Filename:',
        'start_merge': 'Start Merge',
        'add_merge_files': 'Please add PDF files to merge!',
        'select_output_dir': 'Please select output directory!',
        'invalid_filename': 'Please enter a valid output filename (ending with .pdf)!',
        'merge_window_title': 'Merge PDF Files',
        'language': 'Language',
        'chinese': '中文',
        'english': 'English',
        'file_size': 'File Size',
        'total_pages': 'Total Pages',
        'bookmark_count': 'Bookmark Count',
        'bookmark_structure': 'Bookmark Structure',
        'no_bookmarks_found': 'No Bookmarks',
        'filename': 'Filename',
        'mb': 'MB',
        'pages': 'pages',
        'level': 'Level',
        'unknown_page': 'Unknown',
    }
}

class MergeWindow:
    def __init__(self, parent, get_text_func, language_callback):
        self.parent = parent
        self.get_text = get_text_func
        self.language_callback = language_callback
        self.window = tk.Toplevel(parent)
        self.window.title(self.get_text('merge_window_title'))
        self.window.geometry("600x400")
        self.window.grab_set()
        self.widgets = {}  # 保存控件引用
        self.file_list = []
        self.create_widgets()

    def create_widgets(self):
        # 文件列表框
        self.widgets['listbox'] = tk.Listbox(self.window, selectmode=tk.EXTENDED, width=60, height=10)
        self.widgets['listbox'].grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky=tk.W+tk.E)

        self.widgets['add_files'] = ttk.Button(self.window, text=self.get_text('add_files'), command=self.add_files)
        self.widgets['add_files'].grid(row=1, column=0, padx=5, pady=5)
        self.widgets['remove_selected'] = ttk.Button(self.window, text=self.get_text('remove_selected'), command=self.remove_file)
        self.widgets['remove_selected'].grid(row=1, column=1, padx=5, pady=5)
        self.widgets['move_up'] = ttk.Button(self.window, text=self.get_text('move_up'), command=self.move_up)
        self.widgets['move_up'].grid(row=1, column=2, padx=5, pady=5)
        self.widgets['move_down'] = ttk.Button(self.window, text=self.get_text('move_down'), command=self.move_down)
        self.widgets['move_down'].grid(row=1, column=3, padx=5, pady=5)

        self.out_dir_var = tk.StringVar()
        self.out_name_var = tk.StringVar(value="merged.pdf")

        self.widgets['output_directory_label'] = ttk.Label(self.window, text=self.get_text('output_directory'))
        self.widgets['output_directory_label'].grid(row=2, column=0, sticky=tk.W, padx=10, pady=(20, 5))
        self.widgets['out_dir_entry'] = ttk.Entry(self.window, textvariable=self.out_dir_var, width=40)
        self.widgets['out_dir_entry'].grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=(20, 5))
        self.widgets['browse'] = ttk.Button(self.window, text=self.get_text('browse'), command=self.select_out_dir)
        self.widgets['browse'].grid(row=2, column=3, pady=(20, 5))

        self.widgets['output_filename_label'] = ttk.Label(self.window, text=self.get_text('output_filename'))
        self.widgets['output_filename_label'].grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.widgets['out_name_entry'] = ttk.Entry(self.window, textvariable=self.out_name_var, width=40)
        self.widgets['out_name_entry'].grid(row=3, column=1, columnspan=2, sticky=tk.W, pady=5)
        self.widgets['pdf_label'] = ttk.Label(self.window, text=".pdf")
        self.widgets['pdf_label'].grid(row=3, column=3, sticky=tk.W, pady=5)

        self.widgets['start_merge'] = ttk.Button(self.window, text=self.get_text('start_merge'), command=self.do_merge)
        self.widgets['start_merge'].grid(row=4, column=0, columnspan=4, pady=20)

    def refresh_listbox(self):
        self.widgets['listbox'].delete(0, tk.END)
        for f in self.file_list:
            self.widgets['listbox'].insert(tk.END, f)

    def add_files(self):
        files = filedialog.askopenfilenames(
            title=self.get_text('select_pdf_files'),
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        for f in files:
            if f not in self.file_list:
                self.file_list.append(f)
        self.refresh_listbox()

    def remove_file(self):
        sel = self.widgets['listbox'].curselection()
        for idx in reversed(sel):
            del self.file_list[idx]
        self.refresh_listbox()

    def move_up(self):
        sel = self.widgets['listbox'].curselection()
        if not sel or sel[0] == 0:
            return
        idx = sel[0]
        self.file_list[idx-1], self.file_list[idx] = self.file_list[idx], self.file_list[idx-1]
        self.refresh_listbox()
        self.widgets['listbox'].selection_set(idx-1)

    def move_down(self):
        sel = self.widgets['listbox'].curselection()
        if not sel or sel[0] == len(self.file_list)-1:
            return
        idx = sel[0]
        self.file_list[idx+1], self.file_list[idx] = self.file_list[idx], self.file_list[idx+1]
        self.refresh_listbox()
        self.widgets['listbox'].selection_set(idx+1)

    def select_out_dir(self):
        d = filedialog.askdirectory(title=self.get_text('select_output_dir'))
        if d:
            self.out_dir_var.set(d)

    def do_merge(self):
        if not self.file_list:
            messagebox.showerror(self.get_text('error'), self.get_text('add_merge_files'), parent=self.window)
            return
        if not self.out_dir_var.get():
            messagebox.showerror(self.get_text('error'), self.get_text('select_output_dir'), parent=self.window)
            return
        out_name = self.out_name_var.get().strip()
        if not out_name or not out_name.lower().endswith('.pdf'):
            messagebox.showerror(self.get_text('error'), self.get_text('invalid_filename'), parent=self.window)
            return
        out_path = os.path.join(self.out_dir_var.get(), out_name)
        try:
            merger = PyPDF2.PdfMerger()
            for f in self.file_list:
                merger.append(f)
            merger.write(out_path)
            merger.close()
            messagebox.showinfo(self.get_text('merge_window_title'), f"{self.get_text('merge_complete')}\n{out_path}", parent=self.window)
        except Exception as e:
            messagebox.showerror(self.get_text('error'), f"{self.get_text('merge_failed')}: {e}", parent=self.window)

    def update_ui_text(self):
        self.window.title(self.get_text('merge_window_title'))
        self.widgets['add_files'].config(text=self.get_text('add_files'))
        self.widgets['remove_selected'].config(text=self.get_text('remove_selected'))
        self.widgets['move_up'].config(text=self.get_text('move_up'))
        self.widgets['move_down'].config(text=self.get_text('move_down'))
        self.widgets['output_directory_label'].config(text=self.get_text('output_directory'))
        self.widgets['browse'].config(text=self.get_text('browse'))
        self.widgets['output_filename_label'].config(text=self.get_text('output_filename'))
        self.widgets['start_merge'].config(text=self.get_text('start_merge'))
        # .pdf标签无需切换

class PDFSplitter:
    def __init__(self, root):
        self.root = root
        self.current_language = 'zh'  # 默认中文
        self.root.title(LANGUAGES[self.current_language]['title'])
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
        self.merge_windows = []  # 新增：保存所有合并窗口实例
        
        self.create_widgets()
        
    def get_text(self, key):
        """获取当前语言的文本"""
        return LANGUAGES[self.current_language].get(key, key)
        
    def switch_language(self):
        """切换语言"""
        self.current_language = 'en' if self.current_language == 'zh' else 'zh'
        self.update_ui_text()
        # 新增：同步所有合并窗口语言
        for win in self.merge_windows:
            win.update_ui_text()
        
    def update_ui_text(self):
        """更新界面文本"""
        self.root.title(self.get_text('title'))
        
        # 更新语言切换按钮
        self.lang_button.config(text=self.get_text('english') if self.current_language == 'zh' else self.get_text('chinese'))
        
        # 更新主要标签框架
        self.file_selection_label.configure(text=self.get_text('file_selection'))
        self.pdf_info_label.configure(text=self.get_text('pdf_info'))
        self.split_method_label.configure(text=self.get_text('split_method'))
        self.output_options_label.configure(text=self.get_text('output_options'))
        
        # 更新按钮文本
        self.split_button.config(text=self.get_text('start_split'))
        self.merge_button.config(text=self.get_text('merge_pdf'))
        self.exit_button.config(text=self.get_text('exit'))
        
        # 更新状态
        self.status_var.set(self.get_text('ready'))
        
        # 新增：分割参数区控件文本更新
        self.range_radio.config(text=self.get_text('range_split'))
        self.range_label.config(text=self.get_text('page_range'))
        self.range_help_label.config(text=self.get_text('range_help'))
        self.pages_radio.config(text=self.get_text('pages_split'))
        self.pages_label.config(text=self.get_text('pages_per_split'))
        self.bookmark_radio.config(text=self.get_text('bookmark_split'))
        self.bookmark_label.config(text=self.get_text('bookmark_level'))
        self.custom_radio.config(text=self.get_text('custom_split'))
        self.custom_label.config(text=self.get_text('custom_points'))
        self.custom_help_label.config(text=self.get_text('custom_help'))
        
        # 新增：文件选择和输出选项区label文本更新
        self.pdf_file_label.config(text=self.get_text('pdf_file'))
        self.output_dir_label.config(text=self.get_text('output_dir'))
        self.browse_pdf_button.config(text=self.get_text('browse'))
        self.browse_output_button.config(text=self.get_text('browse'))
        self.filename_prefix_label.config(text=self.get_text('filename_prefix'))
        self.overwrite_check.config(text=self.get_text('overwrite_files'))
        
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 语言切换按钮
        lang_frame = ttk.Frame(main_frame)
        lang_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(lang_frame, text=self.get_text('language') + ":").pack(side=tk.LEFT, padx=(0, 5))
        self.lang_button = ttk.Button(lang_frame, text=self.get_text('english') if self.current_language == 'zh' else self.get_text('chinese'), 
                                     command=self.switch_language)
        self.lang_button.pack(side=tk.LEFT)
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text=self.get_text('file_selection'), padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        self.pdf_file_label = ttk.Label(file_frame, text=self.get_text('pdf_file'))
        self.pdf_file_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.pdf_path_var = tk.StringVar()
        self.pdf_entry = ttk.Entry(file_frame, textvariable=self.pdf_path_var, state="readonly")
        self.pdf_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.browse_pdf_button = ttk.Button(file_frame, text=self.get_text('browse'), command=self.select_pdf)
        self.browse_pdf_button.grid(row=0, column=2)
        
        self.output_dir_label = ttk.Label(file_frame, text=self.get_text('output_dir'))
        self.output_dir_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        self.output_path_var = tk.StringVar()
        self.output_entry = ttk.Entry(file_frame, textvariable=self.output_path_var, state="readonly")
        self.output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(10, 0))
        self.browse_output_button = ttk.Button(file_frame, text=self.get_text('browse'), command=self.select_output_dir)
        self.browse_output_button.grid(row=1, column=2, pady=(10, 0))
        
        # PDF信息显示
        info_frame = ttk.LabelFrame(main_frame, text=self.get_text('pdf_info'), padding="10")
        info_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=6, width=80)
        self.info_text.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # 分割方式选择
        split_frame = ttk.LabelFrame(main_frame, text=self.get_text('split_method'), padding="10")
        split_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.split_method = tk.StringVar(value="range")
        
        # 按页面范围分割
        range_frame = ttk.Frame(split_frame)
        range_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        range_frame.columnconfigure(1, weight=1)
        self.range_radio = ttk.Radiobutton(range_frame, text=self.get_text('range_split'), variable=self.split_method, 
                       value="range", command=self.on_method_change)
        self.range_radio.grid(row=0, column=0, sticky=tk.W)
        self.range_frame = ttk.Frame(range_frame)
        self.range_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        self.range_frame.columnconfigure(1, weight=1)
        self.range_label = ttk.Label(self.range_frame, text=self.get_text('page_range'))
        self.range_label.grid(row=0, column=0, sticky=tk.W, padx=(20, 5))
        self.range_var = tk.StringVar()
        self.range_entry = ttk.Entry(self.range_frame, textvariable=self.range_var)
        self.range_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.range_help_label = ttk.Label(self.range_frame, text=self.get_text('range_help'))
        self.range_help_label.grid(row=0, column=2, sticky=tk.W)
        
        # 按页数分割
        pages_frame = ttk.Frame(split_frame)
        pages_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        pages_frame.columnconfigure(1, weight=1)
        self.pages_radio = ttk.Radiobutton(pages_frame, text=self.get_text('pages_split'), variable=self.split_method, 
                       value="pages", command=self.on_method_change)
        self.pages_radio.grid(row=0, column=0, sticky=tk.W)
        self.pages_frame = ttk.Frame(pages_frame)
        self.pages_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        self.pages_frame.columnconfigure(1, weight=1)
        self.pages_label = ttk.Label(self.pages_frame, text=self.get_text('pages_per_split'))
        self.pages_label.grid(row=0, column=0, sticky=tk.W, padx=(20, 5))
        self.pages_per_split_var = tk.StringVar()
        self.pages_per_split_entry = ttk.Entry(self.pages_frame, textvariable=self.pages_per_split_var)
        self.pages_per_split_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # 按书签分割
        bookmark_frame = ttk.Frame(split_frame)
        bookmark_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        bookmark_frame.columnconfigure(1, weight=1)
        self.bookmark_radio = ttk.Radiobutton(bookmark_frame, text=self.get_text('bookmark_split'), variable=self.split_method, 
                       value="bookmark", command=self.on_method_change)
        self.bookmark_radio.grid(row=0, column=0, sticky=tk.W)
        self.bookmark_frame = ttk.Frame(bookmark_frame)
        self.bookmark_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        self.bookmark_frame.columnconfigure(1, weight=1)
        self.bookmark_label = ttk.Label(self.bookmark_frame, text=self.get_text('bookmark_level'))
        self.bookmark_label.grid(row=0, column=0, sticky=tk.W, padx=(20, 5))
        self.bookmark_level_var = tk.StringVar(value="1")
        self.bookmark_level_combo = ttk.Combobox(self.bookmark_frame, textvariable=self.bookmark_level_var, 
                                                values=["1", "2", "3", "4", "5"], state="readonly", width=10)
        self.bookmark_level_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 5))
        
        # 自定义分割
        custom_frame = ttk.Frame(split_frame)
        custom_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        custom_frame.columnconfigure(1, weight=1)
        self.custom_radio = ttk.Radiobutton(custom_frame, text=self.get_text('custom_split'), variable=self.split_method, 
                       value="custom", command=self.on_method_change)
        self.custom_radio.grid(row=0, column=0, sticky=tk.W)
        self.custom_frame = ttk.Frame(custom_frame)
        self.custom_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        self.custom_frame.columnconfigure(1, weight=1)
        self.custom_label = ttk.Label(self.custom_frame, text=self.get_text('custom_points'))
        self.custom_label.grid(row=0, column=0, sticky=tk.W, padx=(20, 5))
        self.custom_var = tk.StringVar()
        self.custom_entry = ttk.Entry(self.custom_frame, textvariable=self.custom_var)
        self.custom_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.custom_help_label = ttk.Label(self.custom_frame, text=self.get_text('custom_help'))
        self.custom_help_label.grid(row=0, column=2, sticky=tk.W)
        
        # 输出选项
        output_frame = ttk.LabelFrame(main_frame, text=self.get_text('output_options'), padding="10")
        output_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.filename_prefix_label = ttk.Label(output_frame, text=self.get_text('filename_prefix'))
        self.filename_prefix_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.prefix_var = tk.StringVar(value="split_")
        self.prefix_entry = ttk.Entry(output_frame, textvariable=self.prefix_var, width=20)
        self.prefix_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        self.overwrite_var = tk.BooleanVar(value=False)
        self.overwrite_check = ttk.Checkbutton(output_frame, text=self.get_text('overwrite_files'), 
                                              variable=self.overwrite_var)
        self.overwrite_check.grid(row=0, column=2, sticky=tk.W)
        
        # 进度条和状态
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.status_var = tk.StringVar(value=self.get_text('ready'))
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
        self.split_button = ttk.Button(button_frame, text=self.get_text('start_split'), command=self.start_split)
        self.split_button.grid(row=0, column=0, padx=(0, 10))
        
        # 新增：合并PDF按钮
        self.merge_button = ttk.Button(button_frame, text=self.get_text('merge_pdf'), command=self.open_merge_window)
        self.merge_button.grid(row=0, column=1, padx=(0, 10))
        
        self.exit_button = ttk.Button(button_frame, text=self.get_text('exit'), command=self.root.quit)
        self.exit_button.grid(row=0, column=2)
        
        # 保存标签引用用于语言切换
        self.file_selection_label = file_frame
        self.pdf_info_label = info_frame
        self.split_method_label = split_frame
        self.output_options_label = output_frame
        
        # 初始化界面状态
        self.on_method_change()
        
    def select_pdf(self):
        file_path = filedialog.askopenfilename(
            title=self.get_text('select_pdf_files'),
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if file_path:
            self.pdf_path = file_path
            self.pdf_path_var.set(file_path)
            self.load_pdf_info()
            
    def select_output_dir(self):
        dir_path = filedialog.askdirectory(title=self.get_text('select_output_dir'))
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
            
            info = f"{self.get_text('filename')}: {os.path.basename(self.pdf_path)}\n"
            info += f"{self.get_text('total_pages')}: {self.total_pages}\n"
            info += f"{self.get_text('file_size')}: {os.path.getsize(self.pdf_path) / 1024 / 1024:.2f} {self.get_text('mb')}\n"
            
            # 显示书签信息
            if self.pdf_reader.outline:
                info += f"{self.get_text('bookmark_count')}: {len(self.pdf_reader.outline)}\n"
                info += f"{self.get_text('bookmark_structure')}:\n"
                self.display_bookmarks(self.pdf_reader.outline, info, 0)
            else:
                info += f"{self.get_text('no_bookmarks_found')}\n"
                
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info)
            
        except Exception as e:
            messagebox.showerror(self.get_text('error'), f"{self.get_text('no_pdf_selected')}: {str(e)}")
            
    def display_bookmarks(self, bookmarks, info, level):
        for i, bookmark in enumerate(bookmarks):
            indent = "  " * level
            if isinstance(bookmark, list):
                self.display_bookmarks(bookmark, info, level + 1)
            else:
                page_num = bookmark.page + 1 if hasattr(bookmark, 'page') else self.get_text('unknown_page')
                info += f"{indent}- {bookmark.title} ({self.get_text('level')}{page_num})\n"
                
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
            messagebox.showerror(self.get_text('error'), self.get_text('no_pdf_selected'))
            return False
            
        if not self.output_dir:
            messagebox.showerror(self.get_text('error'), self.get_text('no_output_dir'))
            return False
            
        if not self.pdf_reader:
            messagebox.showerror(self.get_text('error'), self.get_text('no_pdf_selected'))
            return False
            
        method = self.split_method.get()
        
        if method == "range":
            if not self.range_var.get().strip():
                messagebox.showerror(self.get_text('error'), self.get_text('no_pdf_selected'))
                return False
                
        elif method == "pages":
            try:
                pages = int(self.pages_per_split_var.get())
                if pages <= 0 or pages > self.total_pages:
                    messagebox.showerror(self.get_text('error'), f"{self.get_text('invalid_pages')} (1-{self.total_pages})")
                    return False
            except ValueError:
                messagebox.showerror(self.get_text('error'), self.get_text('invalid_pages'))
                return False
                
        elif method == "custom":
            if not self.custom_var.get().strip():
                messagebox.showerror(self.get_text('error'), self.get_text('invalid_custom'))
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
                        raise ValueError(f"{self.get_text('invalid_range')}: {part}")
                except ValueError:
                    raise ValueError(f"{self.get_text('invalid_range')}: {part}")
            else:
                try:
                    page = int(part)
                    if page > 0 and page <= self.total_pages:
                        ranges.append((page-1, page-1))  # 转换为0索引
                    else:
                        raise ValueError(f"{self.get_text('invalid_range')}: {part}")
                except ValueError:
                    raise ValueError(f"{self.get_text('invalid_range')}: {part}")
                    
        return ranges
        
    def parse_custom_points(self, custom_str):
        """解析自定义分割点"""
        try:
            points = [int(x.strip()) for x in custom_str.split(',')]
            points = [p for p in points if p > 0 and p < self.total_pages]
            points.sort()
            return points
        except ValueError:
            raise ValueError(self.get_text('invalid_custom'))
            
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
                
            self.root.after(0, lambda: messagebox.showinfo("完成", self.get_text('split_complete')))
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: messagebox.showerror(self.get_text('error'), f"{self.get_text('split_failed')}: {error_msg}"))
        finally:
            # 分割完成后关闭PDF文件对象
            if self.pdf_file_obj:
                self.pdf_file_obj.close()
                self.pdf_file_obj = None
            self.root.after(0, lambda: self.split_button.config(state="normal"))
            
    def split_by_range(self, prefix):
        ranges = self.parse_range(self.range_var.get())
        
        for i, (start, end) in enumerate(ranges):
            self.status_var.set(f"{self.get_text('processing')} {i+1}/{len(ranges)}...")
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
            self.status_var.set(f"{self.get_text('processing')} {i+1}/{total_splits}...")
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
            raise ValueError(self.get_text('no_bookmarks'))
            
        # 添加开始和结束页
        all_pages = [0] + bookmark_pages + [self.total_pages]
        all_pages = sorted(list(set(all_pages)))
        
        for i in range(len(all_pages) - 1):
            self.status_var.set(f"{self.get_text('processing')} {i+1}/{len(all_pages)-1}...")
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
            raise ValueError(self.get_text('invalid_custom'))
            
        # 添加开始和结束页
        all_points = [0] + split_points + [self.total_pages]
        
        for i in range(len(all_points) - 1):
            self.status_var.set(f"{self.get_text('processing')} {i+1}/{len(all_points)-1}...")
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
        win = MergeWindow(self.root, self.get_text, self.switch_language)
        self.merge_windows.append(win)
        def on_close():
            self.merge_windows.remove(win)
            win.window.destroy()
        win.window.protocol("WM_DELETE_WINDOW", on_close)

def main():
    root = tk.Tk()
    app = PDFSplitter(root)
    root.mainloop()

if __name__ == "__main__":
    main() 