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
  * SSE: 上海证券交易所
  * SZSE: 深圳证券交易所
  * BSE: 北京证券交易所

* **期货**:
  * CFFEX: 中国金融期货交易所
  * SHFE: 上海期货交易所
  * DCE: 大连商品交易所
  * CZCE: 郑州商品交易所
  * INE: 上海国际能源交易中心

**数据周期**: 日线、分钟线(1/5/15/30/60分钟)

注意: AkShare是免费开源的金融数据接口包,无需注册即可使用。

## 安装

安装环境推荐基于3.0.0版本以上的【[**VeighNa Studio**](https://www.vnpy.com)】。

直接使用pip命令:

```bash
pip install vnpy_akshare
```

或者下载源代码后,解压后在cmd中运行:

```bash
pip install .
```

## 使用

在VeighNa中使用AkShare时,需要在全局配置中填写以下字段信息:

|名称|含义|必填|举例|
|---------|----|---|---|
|datafeed.name|名称|是|akshare|
|datafeed.username|用户名|否|-|
|datafeed.password|密码|否|-|

配置示例(`setting.json`):

```json
{
    "datafeed.name": "akshare",
    "datafeed.username": "",
    "datafeed.password": ""
}
```

## 功能特性

* ✅ 支持A股历史K线数据获取(日线和分钟线)
* ✅ 支持期货历史K线数据获取(日线和分钟线)
* ✅ 自动处理股票代码格式转换
* ✅ 支持复权数据(前复权、后复权)
* ✅ 内置数据缓存机制,减少重复请求
* ✅ 完善的异常处理和日志输出

## 依赖

* vnpy >= 3.0.0
* akshare >= 1.12.0
* pandas >= 1.5.0

## 注意事项

1. AkShare数据来源于网络爬虫,稳定性受目标网站影响
2. 建议合理控制请求频率,避免触发反爬机制
3. 期货夜盘数据处理:第一条夜盘K线为集合竞价数据,可根据需求过滤或合并
4. 数据更新可能存在延迟,请以实际返回为准

## 开发说明

### 目录结构

```
vnpy_akshare/
├── __init__.py              # 包初始化文件
├── akshare_datafeed.py      # 核心数据接口实现
└── setup.py                 # 安装配置文件
```

### 主要类说明

* `AkShareDatafeed`: 继承自`BaseDatafeed`,实现VeighNa标准数据接口
  * `init()`: 初始化数据服务连接
  * `query_bar_history()`: 查询K线历史数据
  * `query_tick_history()`: 查询Tick历史数据(暂未实现)

## 许可证

本插件遵循MIT协议开源

## 贡献

欢迎提交Issue和Pull Request!

## 相关链接

* [VeighNa官网](https://www.vnpy.com)
* [AkShare文档](https://akshare.akfamily.xyz)
* [VeighNa GitHub](https://github.com/vnpy/vnpy)
