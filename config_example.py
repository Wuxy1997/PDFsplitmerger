# PDF分割工具配置示例
# 可以修改这些设置来自定义程序行为

# 默认设置
DEFAULT_SETTINGS = {
    # 默认输出目录
    'default_output_dir': '',
    
    # 默认文件名前缀
    'default_prefix': 'split_',
    
    # 默认书签级别
    'default_bookmark_level': 1,
    
    # 默认每份页数
    'default_pages_per_split': 10,
    
    # 是否默认覆盖文件
    'default_overwrite': False,
    
    # 界面主题 (可选: 'clam', 'alt', 'default', 'classic')
    'theme': 'clam',
    
    # 窗口大小
    'window_width': 800,
    'window_height': 600,
    
    # 是否记住上次使用的目录
    'remember_last_directory': True,
    
    # 最大文件大小警告 (MB)
    'max_file_size_warning': 100,
    
    # 进度条更新频率 (毫秒)
    'progress_update_interval': 100,
}

# 文件类型过滤器
FILE_FILTERS = [
    ("PDF文件", "*.pdf"),
    ("所有文件", "*.*")
]

# 支持的分割方式
SPLIT_METHODS = {
    'range': '按页面范围分割',
    'pages': '按页数分割', 
    'bookmark': '按书签分割',
    'custom': '自定义分割'
}

# 书签级别选项
BOOKMARK_LEVELS = [1, 2, 3, 4, 5]

# 错误消息
ERROR_MESSAGES = {
    'no_pdf_selected': '请选择PDF文件',
    'no_output_dir': '请选择输出目录',
    'invalid_range': '页面范围格式错误',
    'invalid_pages': '页数必须是正整数',
    'invalid_custom': '自定义分割点格式错误',
    'no_bookmarks': 'PDF文件不包含书签',
    'file_too_large': '文件过大，处理可能需要较长时间',
    'insufficient_space': '磁盘空间不足',
    'permission_denied': '没有写入权限',
}

# 成功消息
SUCCESS_MESSAGES = {
    'split_complete': 'PDF分割完成！',
    'files_created': '已创建 {count} 个文件',
    'processing_complete': '处理完成',
}

# 界面文本
UI_TEXTS = {
    'title': 'PDF分割工具',
    'file_selection': '文件选择',
    'pdf_file': 'PDF文件:',
    'output_dir': '输出目录:',
    'browse': '浏览',
    'pdf_info': 'PDF信息',
    'split_method': '分割方式',
    'output_options': '输出选项',
    'filename_prefix': '文件名前缀:',
    'overwrite_files': '覆盖已存在的文件',
    'start_split': '开始分割',
    'exit': '退出',
    'ready': '就绪',
    'processing': '正在处理...',
}

# 使用示例
USAGE_EXAMPLES = {
    'range': {
        'description': '按页面范围分割',
        'examples': [
            '1-5 (第1到第5页)',
            '1-5, 8-12, 15 (多个范围)',
            '1, 3, 5 (单个页面)',
            '1-10, 15-20, 25 (混合格式)'
        ]
    },
    'pages': {
        'description': '按页数分割',
        'examples': [
            '5 (每份5页)',
            '10 (每份10页)',
            '1 (每页单独分割)'
        ]
    },
    'bookmark': {
        'description': '按书签分割',
        'examples': [
            '级别1 (顶级书签)',
            '级别2 (二级书签)',
            '级别3 (三级书签)'
        ]
    },
    'custom': {
        'description': '自定义分割',
        'examples': [
            '5,10,15 (在第5、10、15页前分割)',
            '10,20,30,40 (在指定页面前分割)',
            '1,5,10 (混合分割点)'
        ]
    }
} 