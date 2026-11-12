# VeighNa框架的AkShare数据服务接口

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
  <img src ="https://img.shields.io/badge/version-1.0.0-blueviolet.svg"/>
  <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
  <img src ="https://img.shields.io/badge/python-3.8|3.9|3.10|3.11-blue.svg"/>
  <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## 说明

基于akshare模块开发的VeighNa数据服务接口,支持以下中国金融市场的K线数据:

* **股票**:
  * SSE:上海证券交易所
  * SZSE:深圳证券交易所
  * BSE:北京证券交易所

* **期货**:
  * CFFEX:中国金融期货交易所
  * SHFE:上海期货交易所
  * DCE:大连商品交易所
  * CZCE:郑州商品交易所
  * INE:上海国际能源交易中心

注意:需要使用相应的数据服务权限,AkShare是免费开源的金融数据接口包。

## 安装

安装环境推荐基于3.0.0版本以上的【[**VeighNa Studio**](https://www.vnpy.com)】。

直接使用pip命令:

```
pip install vnpy_akshare
```

或者下载源代码后,解压后在cmd中运行:

```
pip install .
```

## 使用

在VeighNa Trader的全局配置中填写以下字段信息:

|名称|含义|必填|举例|
|---------|----|---|---|
|datafeed.name|名称|是|akshare|
|datafeed.username|用户名|否|-|
|datafeed.password|密码|否|-|

## 脚本使用

### 加载脚本

在脚本中加载所需的包和数据结构

```python
from datetime import datetime
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.datafeed import get_datafeed
from vnpy.trader.object import HistoryRequest

# 获取数据服务实例
datafeed = get_datafeed()
```

### 获取K线历史数据

```python
# 创建历史数据请求
req = HistoryRequest(
    symbol="600519",
    exchange=Exchange.SSE,
    start=datetime(2023, 1, 1),
    end=datetime(2023, 12, 31),
    interval=Interval.DAILY
)

# 查询数据
bars = datafeed.query_bar_history(req)
```

## 许可证

本插件遵循MIT协议开源

## 贡献

欢迎提交Issue和Pull Request!

## 相关链接

* [VeighNa官网](https://www.vnpy.com)
* [AkShare文档](https://akshare.akfamily.xyz)
* [VeighNa GitHub](https://github.com/vnpy/vnpy)
