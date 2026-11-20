# VeighNa框架的AkShare数据服务接口

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-1.0.0-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg"/>
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## 说明

基于akshare模块开发，支持以下中国金融市场的K线数据：

* 期货：
  * CFFEX：中国金融期货交易所
  * SHFE：上海期货交易所
  * DCE：大连商品交易所
  * CZCE：郑州商品交易所
  * INE：上海国际能源交易中心
* 股票：
  * SSE：上海证券交易所
  * SZSE：深圳证券交易所
  * BSE：北京证券交易所

注意：AkShare是免费开源的金融数据接口包，无需注册即可使用。

## 安装

安装环境推荐基于4.0.0版本以上的【[**VeighNa Studio**](https://www.vnpy.com)】。

直接使用pip命令:

```
pip install vnpy_akshare
```

或者下载源代码后,解压后在cmd中运行:

```
pip install .
```

## 使用

在VeighNa中使用AkShare时，需要在全局配置中填写以下字段信息：

|名称|含义|必填|举例|
|---------|----|---|---|
|datafeed.name|名称|是|akshare|
|datafeed.username|用户名|否|-|
|datafeed.password|密码|否|-|

**重要提示**: 安装后需要修改VeighNa配置才能使用akshare数据源。详见 [VEIGHNA_SETUP.md](VEIGHNA_SETUP.md)

### 快速配置

找到VeighNa配置文件 `vt_setting.json` (通常位于 `~/.vntrader/`),修改:

```json
{
    "datafeed.name": "akshare",
    "datafeed.username": "",
    "datafeed.password": ""
}
```

然后重启VeighNa Trader即可。


# 单元测试

单元测试代码目录为`./tests/test_*.py`
```sh
# 指定文件执行单元测试
python -m unittest tests\test_your_file_name.py

# 全量执行
python -m unittest
```

## 许可证

本插件遵循MIT协议开源

## 贡献

欢迎提交Issue和Pull Request!

## 相关链接

* [VeighNa官网](https://www.vnpy.com)
* [AkShare文档](https://akshare.akfamily.xyz)
* [VeighNa GitHub](https://github.com/vnpy/vnpy)
