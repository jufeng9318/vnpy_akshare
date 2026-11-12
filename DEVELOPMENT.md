# vnpy_akshare 开发指南

## 目录结构说明

```
vnpy_akshare/
├── vnpy_akshare/                 # 主包
│   ├── __init__.py              # 包初始化,导出Datafeed类
│   └── akshare_datafeed.py      # 核心数据接口实现
├── example_usage.py             # 使用示例
├── setup.py                     # 打包配置
├── requirements.txt             # 依赖列表
├── README.md                    # 项目简介
├── USAGE.md                     # 使用指南
├── PROJECT_SUMMARY.md           # 项目总结
├── DEVELOPMENT.md               # 开发指南(本文件)
├── LICENSE                      # 许可证
├── .gitignore                   # Git忽略配置
├── install.bat                  # Windows安装脚本
└── install.sh                   # Linux/Mac安装脚本
```

## 核心架构

### 1. BaseDatafeed接口

VeighNa定义了标准的数据服务接口`BaseDatafeed`,位于`vnpy.trader.datafeed`模块。

**必须实现的方法**:

```python
class BaseDatafeed(ABC):
    @abstractmethod
    def init(self, output: Callable = print) -> bool:
        """初始化数据服务连接"""
        pass
    
    @abstractmethod
    def query_bar_history(
        self, 
        req: HistoryRequest, 
        output: Callable = print
    ) -> Optional[List[BarData]]:
        """查询K线历史数据"""
        pass
    
    @abstractmethod
    def query_tick_history(
        self,
        req: HistoryRequest,
        output: Callable = print
    ) -> Optional[List[TickData]]:
        """查询Tick历史数据"""
        pass
```

### 2. AkShareDatafeed实现

我们的实现位于`vnpy_akshare/akshare_datafeed.py`:

#### 关键组件

**2.1 代码转换函数**

```python
def to_ak_symbol(symbol: str, exchange: Exchange) -> Optional[str]:
    """
    VeighNa格式 -> AkShare格式
    
    示例:
    - "600519" + SSE -> "600519.SH"
    - "rb2405" + SHFE -> "RB2405"
    - "SR2401" + CZCE -> "SR401" (郑商所特殊处理)
    """
```

**2.2 数据获取方法**

```python
def _fetch_stock_data(...) -> DataFrame:
    """获取股票数据"""
    # 日线: ak.stock_zh_a_hist()
    # 分钟线: ak.stock_zh_a_minute()

def _fetch_future_data(...) -> DataFrame:
    """获取期货数据"""
    # 日线: ak.futures_zh_daily_sina()
    # 分钟线: ak.futures_zh_minute_sina()
```

**2.3 数据转换方法**

```python
def _convert_to_bardata(...) -> List[BarData]:
    """
    DataFrame -> BarData列表
    
    映射关系:
    - datetime -> datetime (带时区)
    - open -> open_price
    - high -> high_price
    - low -> low_price
    - close -> close_price
    - volume -> volume
    - turnover -> turnover
    - open_interest -> open_interest
    """
```

## 扩展开发

### 添加新的数据源

如果需要支持更多AkShare接口,按以下步骤操作:

#### 步骤1: 在常量中添加映射

```python
# 在文件顶部添加新的交易所映射
EXCHANGE_VT2AK[Exchange.NEW_EXCHANGE] = "NEW_CODE"

# 添加到支持列表
STOCK_LIST.append(Exchange.NEW_EXCHANGE)
```

#### 步骤2: 更新代码转换函数

```python
def to_ak_symbol(symbol: str, exchange: Exchange) -> Optional[str]:
    # 添加新交易所的处理逻辑
    if exchange == Exchange.NEW_EXCHANGE:
        return f"{symbol}.NEW_SUFFIX"
    # ... 其他逻辑
```

#### 步骤3: 添加数据获取方法

```python
def _fetch_new_type_data(...) -> DataFrame:
    """获取新类型数据"""
    try:
        df = ak.new_api_function(...)
        # 数据处理和列重命名
        return df
    except Exception as ex:
        output(f"获取数据失败: {ex}")
        return None
```

#### 步骤4: 在主方法中调用

```python
def query_bar_history(...):
    # 在适当位置添加新类型的判断
    elif exchange in NEW_TYPE_LIST:
        df = self._fetch_new_type_data(...)
```

### 添加新的周期支持

目前支持: DAILY, HOUR, MINUTE

要添加WEEKLY或MONTHLY:

```python
# 1. 在INTERVAL_VT2AK中添加映射
INTERVAL_VT2AK[Interval.WEEKLY] = "weekly"
INTERVAL_VT2AK[Interval.MONTHLY] = "monthly"

# 2. 在_fetch_stock_data中处理
if interval == Interval.WEEKLY:
    df = ak.stock_zh_a_hist(period="weekly", ...)
elif interval == Interval.MONTHLY:
    df = ak.stock_zh_a_hist(period="monthly", ...)
```

### 自定义缓存策略

当前缓存实现:

```python
self.cache: Dict[str, DataFrame] = {}
self.cache_timeout: int = 300  # 5分钟
```

可以改进为:

```python
from functools import lru_cache
from datetime import timedelta

class AkShareDatafeed(BaseDatafeed):
    def __init__(self):
        # LRU缓存,最多100个
        self._cached_fetch = lru_cache(maxsize=100)(self._fetch_data)
        
        # 或使用 TTLCache
        from cachetools import TTLCache
        self.cache = TTLCache(maxsize=100, ttl=300)
```

## 调试技巧

### 1. 启用详细日志

```python
import logging
logging.basicConfig(level=logging.DEBUG)

def debug_output(msg):
    logging.debug(f"[AKSHARE] {msg}")

bars = datafeed.query_bar_history(req, output=debug_output)
```

### 2. 检查原始数据

```python
# 在 _convert_to_bardata 之前打印DataFrame
print("原始数据:")
print(df.head())
print("\n列名:", df.columns.tolist())
print("\n数据类型:")
print(df.dtypes)
```

### 3. 测试单个API

```python
import akshare as ak

# 直接测试AkShare API
df = ak.stock_zh_a_hist(symbol="600519", period="daily")
print(df)
```

### 4. 验证BarData对象

```python
for bar in bars[:3]:
    print(f"Symbol: {bar.symbol}")
    print(f"Exchange: {bar.exchange}")
    print(f"Datetime: {bar.datetime}")
    print(f"Open: {bar.open_price}")
    print(f"Close: {bar.close_price}")
    print("---")
```

## 常见问题排查

### 问题1: 导入错误

**现象**: `ModuleNotFoundError: No module named 'vnpy_akshare'`

**解决**:
```bash
# 确保正确安装
pip install -e .  # 开发模式安装

# 或检查Python路径
python -c "import sys; print(sys.path)"
```

### 问题2: 数据返回为空

**可能原因**:
1. 股票代码错误
2. 日期范围无数据
3. AkShare API变更

**排查**:
```python
# 检查请求参数
print(f"Symbol: {req.symbol}")
print(f"Exchange: {req.exchange}")
print(f"Start: {req.start}")
print(f"End: {req.end}")

# 直接调用AkShare测试
import akshare as ak
df = ak.stock_zh_a_hist(symbol="600519")
print(df.empty)
```

### 问题3: 时区错误

**现象**: `TypeError: can't compare offset-naive and offset-aware datetimes`

**解决**:
```python
# 确保所有datetime都有时区
from vnpy.trader.utility import ZoneInfo
CHINA_TZ = ZoneInfo("Asia/Shanghai")

if dt.tzinfo is None:
    dt = dt.replace(tzinfo=CHINA_TZ)
```

## 性能优化

### 1. 批量请求

```python
# 一次性获取较长时间范围,而非多次小范围请求
req = HistoryRequest(
    start=datetime(2020, 1, 1),
    end=datetime(2024, 12, 31),  # 5年数据一次获取
    ...
)
```

### 2. 合理使用缓存

```python
# 根据使用场景调整缓存时间
datafeed.cache_timeout = 3600  # 1小时(回测场景)
datafeed.cache_timeout = 60    # 1分钟(实时监控)
```

### 3. 异步IO(高级)

```python
import asyncio
import aiohttp

async def fetch_data_async(symbol):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# 并发获取多个合约数据
tasks = [fetch_data_async(s) for s in symbols]
results = await asyncio.gather(*tasks)
```

## 代码规范

### PEP8遵循

- 每行不超过79字符
- 使用4空格缩进
- 函数和类之间空2行
- 运算符周围加空格

### 类型注解

```python
# 好的做法
def get_data(
    self,
    symbol: str,
    start: datetime,
    end: datetime
) -> Optional[DataFrame]:
    pass

# 避免
def get_data(self, symbol, start, end):
    pass
```

### 文档字符串

```python
def method_name(self, param1: str, param2: int) -> bool:
    """
    方法的简要描述
    
    Args:
        param1: 参数1的说明
        param2: 参数2的说明
        
    Returns:
        返回值的说明
        
    Raises:
        ExceptionType: 异常情况说明
    """
    pass
```

## 测试

### 单元测试示例

```python
import unittest
from datetime import datetime
from vnpy.trader.constant import Exchange, Interval

class TestAkShareDatafeed(unittest.TestCase):
    
    def setUp(self):
        self.datafeed = AkShareDatafeed()
        self.datafeed.init()
    
    def test_init(self):
        """测试初始化"""
        self.assertTrue(self.datafeed.inited)
    
    def test_stock_daily(self):
        """测试股票日线"""
        req = HistoryRequest(
            symbol="600519",
            exchange=Exchange.SSE,
            start=datetime(2023, 1, 1),
            end=datetime(2023, 1, 31),
            interval=Interval.DAILY
        )
        bars = self.datafeed.query_bar_history(req)
        self.assertIsNotNone(bars)
        self.assertGreater(len(bars), 0)
    
    def test_code_conversion(self):
        """测试代码转换"""
        result = to_ak_symbol("600519", Exchange.SSE)
        self.assertEqual(result, "600519.SH")

if __name__ == '__main__':
    unittest.main()
```

## 发布流程

### 1. 更新版本号

修改`setup.py`和`__init__.py`中的版本号

### 2. 构建分发包

```bash
python setup.py sdist bdist_wheel
```

### 3. 上传到PyPI

```bash
# 安装twine
pip install twine

# 上传
twine upload dist/*
```

### 4. 创建Git标签

```bash
git tag v1.0.0
git push origin v1.0.0
```

## 贡献指南

### 提交Issue

包含:
- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息(Python版本、vnpy版本等)

### 提交PR

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 代码审查要点

- 代码是否符合PEP8
- 是否有完整的类型注解
- 是否添加了文档字符串
- 是否有适当的错误处理
- 是否进行了充分测试

## 资源链接

- [VeighNa文档](https://www.vnpy.com/docs)
- [AkShare文档](https://akshare.akfamily.xyz)
- [Python类型注解](https://docs.python.org/3/library/typing.html)
- [PEP8规范](https://peps.python.org/pep-0008/)

---

**祝开发愉快!** 🚀
