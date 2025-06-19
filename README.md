# PDF分割工具 / PDF Splitter Tool

一个功能强大的PDF文档分割和合并软件，支持多种分割方式，并提供中英文双语界面。

A powerful PDF document splitting and merging tool with multiple splitting methods and bilingual Chinese-English interface.

## 功能特点 / Features

- **多种分割方式 / Multiple Split Methods**: 
  - 按页面范围分割 / Split by Page Range
  - 按页数分割 / Split by Page Count
  - 按书签分割 / Split by Bookmarks
  - 自定义分割 / Custom Split
- **PDF合并功能 / PDF Merge Function**: 支持多个PDF文件合并为一个文件 / Support merging multiple PDF files into one
- **中英文双语界面 / Bilingual Interface**: 用户可随时切换中英文界面 / Users can switch between Chinese and English interfaces anytime
- **批量处理 / Batch Processing**: 支持大文件处理，带进度显示 / Support large file processing with progress display
- **文件覆盖控制 / File Overwrite Control**: 可选择是否覆盖已存在的文件 / Option to overwrite existing files
- **友好的图形界面 / User-Friendly GUI**: 直观易用的用户界面 / Intuitive and easy-to-use interface
- **文件排序 / File Sorting**: 合并时可调整PDF文件顺序 / Adjust PDF file order during merging

## 界面语言切换 / Interface Language Switching

程序支持中英文双语界面：
- 点击界面顶部的语言切换按钮即可在中英文之间切换
- 所有界面文本、按钮、提示信息都会实时更新
- 支持中文和English两种语言

The program supports bilingual Chinese-English interface:
- Click the language switch button at the top of the interface to switch between Chinese and English
- All interface text, buttons, and prompt messages are updated in real-time
- Supports both Chinese and English languages

## 安装要求 / Requirements

- Python 3.7+
- PyPDF2 (用于PDF处理 / for PDF processing)
- tkinter (通常随Python安装，用于图形界面 / usually comes with Python, for GUI)

## 安装步骤 / Installation

### 方法一：使用安装脚本（推荐）/ Method 1: Use Installation Script (Recommended)
1. 双击 `install.bat` 文件 / Double-click the `install.bat` file
2. 脚本会自动检查Python并安装依赖包 / The script will automatically check Python and install dependencies

### 方法二：手动安装 / Method 2: Manual Installation
1. 确保已安装Python 3.7或更高版本 / Ensure Python 3.7 or higher is installed
2. 安装依赖包 / Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法 / Usage

### 方法一：使用启动脚本（推荐）/ Method 1: Use Launch Script (Recommended)
1. 双击 `run.bat` 文件启动程序 / Double-click `run.bat` to start the program

### 方法二：命令行启动 / Method 2: Command Line Launch
```bash
python pdf_splitter.py
```

### 使用步骤 / Usage Steps

#### PDF分割 / PDF Splitting
1. 选择要分割的PDF文件 / Select the PDF file to split
2. 选择输出目录 / Select output directory
3. 选择分割方式并设置相应参数 / Choose split method and set parameters
4. 点击"开始分割"按钮 / Click "Start Split" button

#### PDF合并 / PDF Merging
1. 点击"合并PDF"按钮 / Click "Merge PDF" button
2. 在弹出的窗口中选择要合并的PDF文件 / Select PDF files to merge in the popup window
3. 调整文件顺序（可选）/ Adjust file order (optional)
4. 选择输出目录和文件名 / Select output directory and filename
5. 点击"开始合并"按钮 / Click "Start Merge" button

## 分割方式说明 / Split Method Description

### 按页面范围分割 / Split by Page Range
- 格式 / Format: `1-5, 8-12, 15`
- 支持单个页面和页面范围 / Support single pages and page ranges
- 多个范围用逗号分隔 / Multiple ranges separated by commas

### 按页数分割 / Split by Page Count
- 指定每份PDF包含的页数 / Specify the number of pages per PDF
- 程序会自动计算分割份数 / The program automatically calculates the number of splits

### 按书签分割 / Split by Bookmarks
- 根据PDF的书签结构进行分割 / Split based on PDF bookmark structure
- 可选择书签级别（1-5级）/ Choose bookmark level (1-5)
- 每个书签对应一个分割点 / Each bookmark corresponds to a split point

### 自定义分割 / Custom Split
- 在指定页面前进行分割 / Split before specified pages
- 格式 / Format: `5,10,15`
- 程序会在第5、10、15页前分割 / The program will split before pages 5, 10, 15

## 合并功能说明 / Merge Function Description

### 文件选择 / File Selection
- 支持多选PDF文件 / Support multiple PDF file selection
- 可随时添加或移除文件 / Can add or remove files anytime
- 支持文件顺序调整（上移/下移）/ Support file order adjustment (move up/down)

### 输出设置 / Output Settings
- 自定义输出目录 / Custom output directory
- 自定义输出文件名 / Custom output filename
- 自动添加.pdf扩展名 / Automatically add .pdf extension

## 输出文件命名 / Output File Naming

### 分割文件 / Split Files
- 文件名格式 / Filename format: `{前缀}{类型}_{序号}.pdf` / `{prefix}{type}_{number}.pdf`
- 默认前缀 / Default prefix: `split_`
- 可在界面中自定义前缀 / Can customize prefix in the interface

### 合并文件 / Merge Files
- 用户自定义文件名 / User-defined filename
- 自动保存到指定目录 / Automatically saved to specified directory

## 注意事项 / Notes

- 确保有足够的磁盘空间存储分割后的文件 / Ensure sufficient disk space for split files
- 大文件处理可能需要较长时间 / Large file processing may take a long time
- 建议在处理前备份原始文件 / Recommend backing up original files before processing
- 程序支持Windows、macOS和Linux系统 / Program supports Windows, macOS and Linux systems
- 界面语言设置会实时生效 / Interface language settings take effect immediately

## 故障排除 / Troubleshooting

1. **无法读取PDF文件 / Cannot Read PDF File**
   - 检查文件是否损坏 / Check if the file is corrupted
   - 确认文件是有效的PDF格式 / Confirm the file is in valid PDF format

2. **分割失败 / Split Failed**
   - 检查输出目录权限 / Check output directory permissions
   - 确认磁盘空间充足 / Confirm sufficient disk space
   - 验证输入参数格式 / Verify input parameter format

3. **书签分割无效果 / Bookmark Split No Effect**
   - 确认PDF包含书签 / Confirm PDF contains bookmarks
   - 尝试不同的书签级别 / Try different bookmark levels

4. **安装依赖包失败 / Failed to Install Dependencies**
   - 确保Python版本为3.7或更高 / Ensure Python version is 3.7 or higher
   - 尝试使用管理员权限运行安装命令 / Try running installation command with administrator privileges
   - 检查网络连接 / Check network connection

5. **界面显示问题 / Interface Display Issues**
   - 尝试切换语言 / Try switching languages
   - 重启程序 / Restart the program

## 系统要求 / System Requirements

- **操作系统 / Operating System**: Windows 7+, macOS 10.12+, Linux
- **Python**: 3.7或更高版本 / 3.7 or higher
- **内存 / Memory**: 建议2GB以上 / Recommended 2GB or more
- **磁盘空间 / Disk Space**: 根据PDF文件大小而定 / Depends on PDF file size

## 更新日志 / Changelog

### v2.0
- 新增PDF合并功能 / Added PDF merge function
- 新增中英文双语界面 / Added bilingual Chinese-English interface
- 优化用户界面布局 / Optimized user interface layout
- 修复文件句柄问题 / Fixed file handle issues

### v1.0
- 基础PDF分割功能 / Basic PDF split function
- 四种分割方式 / Four split methods
- 图形用户界面 / Graphical user interface

## 许可证 / License

本项目采用MIT许可证。

This project is licensed under the MIT License.

## 贡献 / Contributing

欢迎提交问题报告和功能建议！

Welcome to submit issue reports and feature suggestions!

---

## 项目文件说明 / Project File Description

- `pdf_splitter.py` - 主程序文件 / Main program file
- `requirements.txt` - Python依赖包列表 / Python dependency list
- `README.md` - 使用说明文档 / Usage documentation
- `install.bat` - Windows安装脚本 / Windows installation script
- `run.bat` - Windows启动脚本 / Windows launch script
- `config_example.py` - 配置示例文件 / Configuration example file
- `test_program.py` - 功能测试脚本 / Function test script
- `quick_test.py` - 快速测试脚本 / Quick test script 