@echo off
echo 正在安装PDF分割工具依赖包...
echo.

echo 检查Python是否已安装...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.7或更高版本
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python已安装，正在安装依赖包...
pip install -r requirements.txt

if errorlevel 1 (
    echo 安装失败，请检查网络连接或手动安装依赖包
    pause
    exit /b 1
)

echo.
echo 安装完成！现在可以运行 run.bat 启动程序
pause 