# vnpy_akshare 使用指南

## 快速开始

### 1. 安装

```bash
# 方式1: 从PyPI安装(发布后)
pip install vnpy_akshare

# 方式2: 从源码安装
cd vnpy_akshare
pip install .
```

### 2. 配置

在VeighNa Trader的配置文件(`setting.json`)中添加以下配置:

```json
{
    "datafeed.name": "akshare",
    "datafeed.username": "",
    "datafeed.password": ""
}
```

或者在代码中直接设置:

```python
from vnpy.trader.setting import SETTINGS
SETTINGS["datafeed.name"] = "akshare"
```

### 3. 基本使用

#### 获取数据服务实例

```python
from vnpy.trader.datafeed import get_datafeed

# 获取数据服务实例
datafeed = get_datafeed()
```

#### 查询股票日线数据

```python
from datetime import datetime
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import HistoryRequest

# 创建历史数据请求
req = HistoryRequest(
    symbol="600519",              # 股票代码
    exchange=Exchange.SSE,        # 交易所(上交所)
    start=datetime(2023, 1, 1),   # 开始日期
    end=datetime(2023, 12, 31),   # 结束日期
    interval=Interval.DAILY       # 周期(日线)
)

# 查询数据
bars = datafeed.query_bar_history(req)

# 处理数据
if bars:
    print(f"获取到 {len(bars)} 条K线数据")
    for bar in bars[:5]:
        print(f"{bar.datetime.date()} O:{bar.open_price} H:{bar.high_price} "
              f"L:{bar.low_price} C:{bar.close_price} V:{bar.volume}")
```

#### 查询期货分钟线数据

```python
# 创建分钟线数据请求
req = HistoryRequest(
    symbol="rb2405",              # 期货合约代码
    exchange=Exchange.SHFE,       # 上期所
    start=datetime(2024, 1, 1),   # 开始日期
    end=datetime(2024, 1, 31),    # 结束日期
    interval=Interval.MINUTE      # 周期(1分钟)
)

# 查询数据
bars = datafeed.query_bar_history(req)
```

## 支持的合约类型

### 股票

| 交易所 | 代码后缀 | 示例 |
|--------|---------|------|
| 上海证券交易所 | .SH / SSE | 600519.SH (贵州茅台) |
| 深圳证券交易所 | .SZ / SZSE | 300750.SZ (宁德时代) |
| 北京证券交易所 | .BJ / BSE | 835368.BJ |

### 期货

| 交易所 | 代码 | 示例 |
|--------|-----|------|
| 上海期货交易所 | SHFE | rb2405 (螺纹钢) |
| 大连商品交易所 | DCE | i2405 (铁矿石) |
| 郑州商品交易所 | CZCE | SR401 (白糖) |
| 中国金融期货交易所 | CFFEX | IF2401 (沪深300股指期货) |
| 上海国际能源交易中心 | INE | sc2401 (原油) |

## 支持的数据周期

- **日线**: `Interval.DAILY`
- **小时线**: `Interval.HOUR` (60分钟)
- **分钟线**: `Interval.MINUTE` (1分钟)

## 高级用法

### 在策略中使用

```python
from vnpy_ctastrategy import CtaTemplate
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import BarData
from datetime import datetime


class MyStrategy(CtaTemplate):
    """示例策略"""
    
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        
    def on_init(self):
        """初始化时加载历史数据"""
        self.write_log("策略初始化")
        
        # 加载100天历史数据
        days = 100
        self.load_bar(days)
        
    def on_bars(self, bars):
        """收到K线推送"""
        for vt_symbol, bar in bars.items():
            # 处理K线数据
            pass
    
    def on_bar(self, bar: BarData):
        """收到单根K线推送"""
        # 实现策略逻辑
        pass
```

### 数据缓存控制

AkShareDatafeed内置了数据缓存机制,可以通过以下方式控制:

```python
from vnpy_akshare.akshare_datafeed import AkShareDatafeed

# 创建数据服务实例
datafeed = AkShareDatafeed()

# 修改缓存超时时间(秒)
datafeed.cache_timeout = 600  # 10分钟

# 清空缓存
datafeed.cache.clear()
datafeed.cache_timestamp.clear()
```

### 自定义复权方式

目前支持三种复权方式:

```python
# 在 akshare_datafeed.py 的 _fetch_stock_data 方法中修改 adjust 参数:

# 不复权(默认)
adjust=""

# 前复权
adjust="qfq"

# 后复权
adjust="hfq"
```

## 常见问题

### Q1: 为什么获取不到数据?

**A:** 可能的原因:
1. 检查股票代码和交易所是否正确
2. 检查日期范围是否合理
3. AkShare数据源可能暂时不可用
4. 查看控制台输出的错误信息

### Q2: 如何调试数据获取问题?

**A:** 启用详细日志输出:

```python
def custom_output(msg):
    print(f"[AKSHARE] {msg}")

bars = datafeed.query_bar_history(req, output=custom_output)
```

### Q3: 分钟线数据为什么很少?

**A:** 
- AkShare的股票分钟线数据接口可能有限制
- 建议优先使用日线数据进行回测
- 期货分钟线数据相对完整

### Q4: 数据更新延迟怎么办?

**A:**
- AkShare数据来源于网络爬虫,可能存在延迟
- 实盘交易建议使用专业的付费数据源(如RQData、Tushare Pro等)
- 可以结合多个数据源使用

### Q5: 如何处理期货夜盘数据?

**A:**
- 期货第一条夜盘K线为集合竞价数据
- 可以根据需求过滤或合并该数据
- 在 `_convert_to_bardata` 方法中添加过滤逻辑

## 性能优化建议

1. **合理使用缓存**: 避免重复请求相同数据
2. **批量获取数据**: 一次性获取较长时间范围的数据
3. **控制请求频率**: 避免频繁调用导致被限流
4. **选择合适的数据源**: 根据实际需求选择日线或分钟线

## 贡献代码

欢迎提交Issue和Pull Request!

提交PR前请确保:
1. 代码符合PEP8规范
2. 添加了必要的注释和文档
3. 测试用例通过

## 许可证

MIT License

## 联系方式

- VeighNa社区: https://www.vnpy.com
- AkShare文档: https://akshare.akfamily.xyz
- GitHub Issues: https://github.com/vnpy/vnpy_akshare/issues
