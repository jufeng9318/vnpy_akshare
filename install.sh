#!/bin/bash
# vnpy_akshare 快速安装和测试脚本 (Linux/Mac)

echo "========================================"
echo "vnpy_akshare 安装脚本"
echo "========================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3,请先安装Python 3.8+"
    exit 1
fi

echo "[1/4] 检查Python环境..."
python3 -c "import sys; print(f'Python版本: {sys.version}')"
echo ""

# 安装依赖包
echo "[2/4] 安装依赖包..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[错误] 依赖包安装失败"
    exit 1
fi
echo ""

# 安装vnpy_akshare
echo "[3/4] 安装vnpy_akshare..."
pip3 install .
if [ $? -ne 0 ]; then
    echo "[错误] vnpy_akshare安装失败"
    exit 1
fi
echo ""

# 验证安装
echo "[4/4] 验证安装..."
python3 -c "import vnpy_akshare; print(f'vnpy_akshare版本: {vnpy_akshare.__version__}')"
if [ $? -ne 0 ]; then
    echo "[错误] 导入vnpy_akshare失败"
    exit 1
fi
echo ""

echo "========================================"
echo "安装完成!"
echo "========================================"
echo ""
echo "接下来可以运行测试脚本:"
echo "  python3 example_usage.py"
echo ""
echo "或在VeighNa Trader中配置使用"
echo ""
