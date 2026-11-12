# 快速开始指南

## 5分钟上手vnpy_akshare

### 步骤1: 安装 (1分钟)

#### Windows用户
双击运行 `install.bat` 或在命令行执行:
```bash
install.bat
```

#### Linux/Mac用户
```bash
chmod +x install.sh
./install.sh
```

#### 手动安装
```bash
pip install -r requirements.txt
pip install .
```

### 步骤2: 验证安装 (30秒)

```python
python -c "import vnpy_akshare; print(f'版本: {vnpy_akshare.__version__}')"
```

应该输出: `版本: 1.0.0`

### 步骤3: 运行示例 (2分钟)

```bash
python example_usage.py
```

这将测试:
- ✅ 股票日线数据(贵州茅台)
- ✅ 股票分钟线数据(宁德时代)
- ✅ 期货日线数据(螺纹钢)
- ✅ 期货分钟线数据(股指期货)

### 步骤4: 在代码中使用 (1分钟)

```python
from datetime import datetime
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.datafeed import get_datafeed
from vnpy.trader.object import HistoryRequest

# 获取数据服务
datafeed = get_datafeed()

# 创建请求
req = HistoryRequest(
    symbol="600519",              # 股票代码
    exchange=Exchange.SSE,        # 上交所
    start=datetime(2023, 1, 1),   # 开始日期
    end=datetime(2023, 12, 31),   # 结束日期
    interval=Interval.DAILY       # 日线
)

# 获取数据
bars = datafeed.query_bar_history(req)

# 使用数据
if bars:
    print(f"获取到 {len(bars)} 条K线")
    for bar in bars[:5]:
        print(f"{bar.datetime.date()} 收盘价: {bar.close_price}")
```

## 在VeighNa Trader中配置

### 方法1: 修改配置文件

编辑 `setting.json`:
```json
{
    "datafeed.name": "akshare"
}
```

### 方法2: 代码中设置

```python
from vnpy.trader.setting import SETTINGS
SETTINGS["datafeed.name"] = "akshare"
```

## 常用场景

### 场景1: 策略回测

```python
from vnpy_ctastrategy import CtaTemplate

class MyStrategy(CtaTemplate):
    def on_init(self):
        # 加载100天历史数据
        self.load_bar(100)
    
    def on_bar(self, bar):
        # 策略逻辑
        pass
```

### 场景2: 批量下载数据

```python
symbols = ["600519", "000858", "300750"]

for symbol in symbols:
    req = HistoryRequest(
        symbol=symbol,
        exchange=Exchange.SSE if symbol.startswith("6") else Exchange.SZSE,
        start=datetime(2023, 1, 1),
        end=datetime(2023, 12, 31),
        interval=Interval.DAILY
    )
    bars = datafeed.query_bar_history(req)
    print(f"{symbol}: {len(bars)} 条数据")
```

### 场景3: 获取分钟线

```python
req = HistoryRequest(
    symbol="rb2405",
    exchange=Exchange.SHFE,
    start=datetime(2024, 1, 1),
    end=datetime(2024, 1, 31),
    interval=Interval.MINUTE  # 1分钟线
)
bars = datafeed.query_bar_history(req)
```

## 下一步

- 📖 查看 [详细使用指南](USAGE.md)
- 🔧 查看 [开发指南](DEVELOPMENT.md)
- 📝 查看 [项目总结](PROJECT_SUMMARY.md)

## 遇到问题?

### Q: 导入失败?
```bash
# 确保在项目根目录执行
cd d:\Code\Python\vnpy_akshare
python -m pip install -e .
```

### Q: 获取不到数据?
1. 检查网络连接
2. 检查股票代码和交易所是否正确
3. 查看控制台错误信息
4. 尝试运行 `example_usage.py` 测试

### Q: 需要帮助?
- 查看 [USAGE.md](USAGE.md) 的常见问题部分
- 提交 Issue: https://github.com/vnpy/vnpy_akshare/issues

## 支持的合约

### 股票
- 上交所: 600519.SH (贵州茅台)
- 深交所: 300750.SZ (宁德时代)
- 北交所: 835368.BJ

### 期货
- 上期所: rb2405 (螺纹钢)
- 大商所: i2405 (铁矿石)
- 郑商所: SR401 (白糖)
- 中金所: IF2401 (股指期货)

## 支持的数据周期

- 📅 日线: `Interval.DAILY`
- ⏰ 小时线: `Interval.HOUR`
- ⏱️ 分钟线: `Interval.MINUTE`

---

**开始你的量化交易之旅吧!** 🚀
