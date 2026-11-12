@echo off
REM vnpy_akshare 快速安装和测试脚本

echo ========================================
echo vnpy_akshare 安装脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python,请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/4] 检查Python环境...
python -c "import sys; print(f'Python版本: {sys.version}')"
echo.

REM 安装依赖包
echo [2/4] 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖包安装失败
    pause
    exit /b 1
)
echo.

REM 安装vnpy_akshare
echo [3/4] 安装vnpy_akshare...
pip install .
if errorlevel 1 (
    echo [错误] vnpy_akshare安装失败
    pause
    exit /b 1
)
echo.

REM 验证安装
echo [4/4] 验证安装...
python -c "import vnpy_akshare; print(f'vnpy_akshare版本: {vnpy_akshare.__version__}')"
if errorlevel 1 (
    echo [错误] 导入vnpy_akshare失败
    pause
    exit /b 1
)
echo.

echo ========================================
echo 安装完成!
echo ========================================
echo.
echo 接下来可以运行测试脚本:
echo   python example_usage.py
echo.
echo 或在VeighNa Trader中配置使用
echo.
pause
