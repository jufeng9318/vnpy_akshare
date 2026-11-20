# 在VeighNa中配置vnpy_akshare

## 问题说明

从测试结果可以看到,当前VeighNa使用的是**TushareDatafeed**,而不是AkShareDatafeed。这是因为VeighNa的全局配置中设置了`datafeed.name = "tushare"`。

## 解决方案

### 方法1: 修改VeighNa配置文件(推荐)

找到VeighNa的配置文件 `vt_setting.json`,通常位于:
- Windows: `C:\Users\你的用户名\.vntrader\vt_setting.json`
- Linux/Mac: `~/.vntrader/vt_setting.json`

修改以下配置:

```json
{
    "datafeed.name": "akshare",
    "datafeed.username": "",
    "datafeed.password": ""
}
```

**注意**: AkShare无需认证,username和password留空即可。

### 方法2: 在代码中动态设置

在你的Python脚本开头添加:

```python
from vnpy.trader.setting import SETTINGS

# 设置使用akshare数据源
SETTINGS["datafeed.name"] = "akshare"
SETTINGS["datafeed.username"] = ""
SETTINGS["datafeed.password"] = ""
```

### 方法3: 使用VeighNa Trader界面配置

1. 启动VeighNa Trader
2. 点击菜单栏 **配置** -> **全局配置**
3. 找到 **数据服务** 部分
4. 修改以下字段:
   - `datafeed.name`: 改为 `akshare`
   - `datafeed.username`: 留空
   - `datafeed.password`: 留空
5. 点击 **保存**
6. 重启VeighNa Trader

## 验证配置

运行测试脚本验证配置是否成功:

```bash
python test_integration.py
```

预期输出:
```
============================================================
测试vnpy_akshare数据服务
============================================================
✓ 数据服务实例创建成功: AkShareDatafeed

[测试1] 获取贵州茅台(600519.SH)日线数据
✓ 成功获取 XX 条K线数据
  ...

[测试2] 获取螺纹钢(rb2405.SHFE)日线数据
✓ 成功获取 XX 条K线数据
  ...
```

## 常见问题

### Q1: 修改配置后仍然显示TushareDatafeed?

**A**: 需要重启VeighNa Trader或Python进程,使新配置生效。

### Q2: 如何确认当前使用的是哪个数据源?

**A**: 运行以下代码查看:

```python
from vnpy.trader.datafeed import get_datafeed
from vnpy.trader.setting import SETTINGS

print(f"当前数据源: {SETTINGS.get('datafeed.name', '未设置')}")
datafeed = get_datafeed()
print(f"数据服务类: {type(datafeed).__name__}")
```

### Q3: 想同时使用多个数据源怎么办?

**A**: VeighNa每次只能使用一个数据源。如果需要切换,修改配置后重启即可。

也可以在代码中临时切换:

```python
from vnpy.trader.setting import SETTINGS

# 切换到akshare
SETTINGS["datafeed.name"] = "akshare"

# 或者切换到tushare
SETTINGS["datafeed.name"] = "tushare"
```

## 在CTA策略中使用

配置好数据源后,在CTA策略中加载历史数据会自动使用akshare:

```python
from vnpy_ctastrategy import CtaTemplate


class MyStrategy(CtaTemplate):
    """示例策略"""
    
    def on_init(self):
        """策略初始化"""
        self.write_log("策略初始化")
        
        # 自动通过配置的datafeed加载历史数据
        # 如果datafeed.name="akshare",则使用akshare获取数据
        self.load_bar(100)  # 加载100根K线
        
    def on_bars(self, bars):
        """收到K线推送"""
        pass
    
    def on_bar(self, bar):
        """收到单根K线推送"""
        # 实现你的策略逻辑
        pass
```

## 数据支持情况

### 股票
- ✅ 日线数据 (稳定)
- ⚠️ 分钟线数据 (可能不稳定)
- 支持交易所: SSE(上交所), SZSE(深交所), BSE(北交所)

### 期货
- ✅ 日线数据 (稳定)
- ⚠️ 分钟线数据 (依赖AkShare版本)
- 支持交易所: SHFE, DCE, CZCE, CFFEX, INE

## 优势对比

| 特性 | AkShare | Tushare |
|------|---------|---------|
| 费用 | 完全免费 | 需要积分/付费 |
| 注册 | 无需注册 | 需要注册获取token |
| 稳定性 | 良好 | 优秀 |
| 数据范围 | 股票+期货 | 更全面 |
| 适用场景 | 学习/回测 | 实盘/专业使用 |

---

**配置完成后,你就可以在VeighNa中使用akshare获取免费的金融数据了!** 🎉
