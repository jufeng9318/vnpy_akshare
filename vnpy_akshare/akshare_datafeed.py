"""
AkShare数据服务接口实现
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from copy import deepcopy
import pandas as pd
from pandas import DataFrame

import akshare as ak

from vnpy.trader.setting import SETTINGS
from vnpy.trader.datafeed import BaseDatafeed
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import BarData, HistoryRequest
from vnpy.trader.utility import round_to, ZoneInfo


# 数据频率映射
INTERVAL_VT2AK: Dict[Interval, str] = {
    Interval.MINUTE: "1",
    Interval.HOUR: "60",
    Interval.DAILY: "daily",
}

# 股票支持列表
STOCK_LIST: List[Exchange] = [
    Exchange.SSE,
    Exchange.SZSE,
    Exchange.BSE,
]

# 期货支持列表
FUTURE_LIST: List[Exchange] = [
    Exchange.CFFEX,
    Exchange.SHFE,
    Exchange.CZCE,
    Exchange.DCE,
    Exchange.INE,
]

# 交易所映射(股票代码后缀)
EXCHANGE_VT2AK: Dict[Exchange, str] = {
    Exchange.SSE: "SH",
    Exchange.SZSE: "SZ",
    Exchange.BSE: "BJ",
    Exchange.CFFEX: "CFFEX",
    Exchange.SHFE: "SHFE",
    Exchange.CZCE: "CZCE",
    Exchange.DCE: "DCE",
    Exchange.INE: "INE",
}

# 时间调整映射
INTERVAL_ADJUSTMENT_MAP: Dict[Interval, timedelta] = {
    Interval.MINUTE: timedelta(minutes=1),
    Interval.HOUR: timedelta(hours=1),
    Interval.DAILY: timedelta(),
}

# 中国上海时区
CHINA_TZ = ZoneInfo("Asia/Shanghai")


def to_ak_symbol(symbol: str, exchange: Exchange) -> Optional[str]:
    """
    将VeighNa的合约代码转换为AkShare支持的代码格式
    
    Args:
        symbol: 合约代码(如"600519", "rb2401")
        exchange: 交易所枚举
        
    Returns:
        AkShare格式的合约代码,失败返回None
    """
    # 股票处理
    if exchange in STOCK_LIST:
        ts_symbol: str = f"{symbol}.{EXCHANGE_VT2AK[exchange]}"
        return ts_symbol
    
    # 期货处理
    elif exchange in FUTURE_LIST:
        # 郑商所特殊处理:品种代码+月份(如SR401)
        if exchange is Exchange.CZCE:
            # CZCE的代码格式: 品种字母 + 年份后两位 + 月份(去掉前导0)
            # 例如: SR2401 -> SR401
            for count, word in enumerate(symbol):
                if word.isdigit():
                    break
            
            # 提取字母部分和数字部分
            product: str = symbol[:count]
            month: str = symbol[count:]
            
            # 郑商所格式: 产品代码 + 月份(去掉前导0)
            if len(month) >= 3:
                ts_symbol: str = f"{product}{int(month)}"
            else:
                ts_symbol: str = symbol
        else:
            # 其他期货交易所: 直接使用原代码
            ts_symbol: str = symbol.upper()
        
        return ts_symbol
    
    return None


class AkShareDatafeed(BaseDatafeed):
    """AkShare数据服务接口"""
    
    def __init__(self):
        """"""
        self.inited: bool = False
        
        # 数据缓存
        self.cache: Dict[str, DataFrame] = {}
        self.cache_timeout: int = 300  # 缓存超时时间(秒)
        self.cache_timestamp: Dict[str, datetime] = {}
    
    def init(self, output: Callable = print) -> bool:
        """
        初始化数据服务连接
        
        Args:
            output: 日志输出函数
            
        Returns:
            初始化是否成功
        """
        if self.inited:
            return True
        
        try:
            # AkShare无需认证,直接初始化
            output("AkShare数据服务初始化成功")
            self.inited = True
            return True
        except Exception as ex:
            output(f"AkShare数据服务初始化失败: {ex}")
            return False
    
    def query_bar_history(
        self, 
        req: HistoryRequest, 
        output: Callable = print
    ) -> Optional[List[BarData]]:
        """
        查询K线历史数据
        
        Args:
            req: 历史数据请求对象
            output: 日志输出函数
            
        Returns:
            K线数据列表,失败返回None
        """
        if not self.inited:
            if not self.init(output):
                return None
        
        symbol: str = req.symbol
        exchange: Exchange = req.exchange
        interval: Interval = req.interval
        start: datetime = req.start
        end: datetime = req.end
        
        # 转换为AkShare代码
        ak_symbol: str = to_ak_symbol(symbol, exchange)
        if not ak_symbol:
            output(f"不支持的合约: {symbol}.{exchange.value}")
            return None
        
        # 检查缓存
        cache_key: str = f"{ak_symbol}_{interval.value}_{start.strftime('%Y%m%d')}_{end.strftime('%Y%m%d')}"
        if cache_key in self.cache:
            cached_time: datetime = self.cache_timestamp.get(cache_key)
            if cached_time and (datetime.now() - cached_time).seconds < self.cache_timeout:
                output(f"使用缓存数据: {cache_key}")
                df: DataFrame = self.cache[cache_key]
                return self._convert_to_bardata(df, symbol, exchange, interval)
        
        try:
            # 根据类型获取数据
            if exchange in STOCK_LIST:
                df: DataFrame = self._fetch_stock_data(ak_symbol, interval, start, end, output)
            elif exchange in FUTURE_LIST:
                df: DataFrame = self._fetch_future_data(ak_symbol, exchange, interval, start, end, output)
            else:
                output(f"不支持的交易所: {exchange.value}")
                return None
            
            if df is None or df.empty:
                output(f"未获取到数据: {ak_symbol}")
                return None
            
            # 存入缓存
            self.cache[cache_key] = df
            self.cache_timestamp[cache_key] = datetime.now()
            
            # 转换为BarData
            bars: List[BarData] = self._convert_to_bardata(df, symbol, exchange, interval)
            
            output(f"成功获取 {len(bars)} 条K线数据: {ak_symbol}")
            return bars
            
        except Exception as ex:
            output(f"查询K线数据失败: {ex}")
            import traceback
            output(traceback.format_exc())
            return None
    
    def query_tick_history(
        self,
        req: HistoryRequest,
        output: Callable = print
    ) -> Optional[List]:
        """
        查询Tick历史数据(暂未实现)
        
        Args:
            req: 历史数据请求对象
            output: 日志输出函数
            
        Returns:
            Tick数据列表
        """
        output("AkShare暂不支持Tick历史数据查询")
        return []
    
    def _fetch_stock_data(
        self,
        symbol: str,
        interval: Interval,
        start: datetime,
        end: datetime,
        output: Callable
    ) -> Optional[DataFrame]:
        """
        获取股票历史数据
        
        Args:
            symbol: AkShare格式的合约代码(如"600519.SH")
            interval: K线周期
            start: 开始时间
            end: 结束时间
            output: 日志输出函数
            
        Returns:
            原始数据DataFrame
        """
        try:
            # 转换日期格式
            start_date: str = start.strftime("%Y%m%d")
            end_date: str = end.strftime("%Y%m%d")
            
            # 去除交易所后缀,AkShare只需要纯数字代码
            ak_code: str = symbol.replace(".", "")
            
            if interval == Interval.DAILY:
                # 日线数据
                df: DataFrame = ak.stock_zh_a_hist(
                    symbol=ak_code,
                    period="daily",
                    start_date=start_date,
                    end_date=end_date,
                    adjust=""  # 不复权,可选: qfq-前复权, hfq-后复权
                )
                
                # 重命名列以符合标准格式
                if not df.empty:
                    df.rename(columns={
                        "日期": "datetime",
                        "开盘": "open",
                        "最高": "high",
                        "最低": "low",
                        "收盘": "close",
                        "成交量": "volume",
                        "成交额": "turnover"
                    }, inplace=True)
                    
                    # 转换日期格式
                    df["datetime"] = pd.to_datetime(df["datetime"])
                    
                    # 按时间排序
                    df.sort_values("datetime", inplace=True)
                    df.reset_index(drop=True, inplace=True)
                
                return df
                
            else:
                # 分钟线数据(1/5/15/30/60分钟)
                period_map: Dict[Interval, str] = {
                    Interval.MINUTE: "1",
                    Interval.HOUR: "60",
                }
                
                period: str = period_map.get(interval, "1")
                
                # 注意: AkShare的股票分钟线数据接口可能有限制
                # 这里使用通用的分钟线接口
                try:
                    df: DataFrame = ak.stock_zh_a_minute(
                        symbol=ak_code,
                        period=period,
                        adjust=""
                    )
                except Exception as e:
                    output(f"股票分钟线数据获取失败: {e}")
                    output("提示: AkShare股票分钟线接口可能不稳定,建议使用日线数据")
                    return None
                
                if not df.empty:
                    df.rename(columns={
                        "day": "datetime",
                        "open": "open",
                        "high": "high",
                        "low": "low",
                        "close": "close",
                        "volume": "volume"
                    }, inplace=True)
                    
                    df["datetime"] = pd.to_datetime(df["datetime"])
                    df.sort_values("datetime", inplace=True)
                    df.reset_index(drop=True, inplace=True)
                
                return df
                
        except Exception as ex:
            output(f"获取股票数据失败: {ex}")
            return None
    
    def _fetch_future_data(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval,
        start: datetime,
        end: datetime,
        output: Callable
    ) -> Optional[DataFrame]:
        """
        获取期货历史数据
        
        Args:
            symbol: AkShare格式的合约代码(如"rb2405")
            exchange: 交易所
            interval: K线周期
            start: 开始时间
            end: 结束时间
            output: 日志输出函数
            
        Returns:
            原始数据DataFrame
        """
        try:
            if interval == Interval.DAILY:
                # 期货日线数据 - 使用新浪财经接口
                try:
                    df: DataFrame = ak.futures_zh_daily_sina(symbol=symbol)
                except Exception as e:
                    output(f"期货日线数据获取失败: {e}")
                    output("尝试使用其他数据源...")
                    return None
                
                if df is None or df.empty:
                    output(f"期货日线数据为空: {symbol}")
                    return None
                
                # 筛选日期范围
                df["date"] = pd.to_datetime(df["date"])
                mask = (df["date"] >= start) & (df["date"] <= end)
                df = df.loc[mask].copy()
                
                df.rename(columns={
                    "date": "datetime",
                    "open": "open",
                    "high": "high",
                    "low": "low",
                    "close": "close",
                    "volume": "volume",
                    "hold": "open_interest"
                }, inplace=True)
                
                df.sort_values("datetime", inplace=True)
                df.reset_index(drop=True, inplace=True)
                
                return df
                
            else:
                # 期货分钟线数据
                period_map: Dict[Interval, str] = {
                    Interval.MINUTE: "1",
                    Interval.HOUR: "60",
                }
                
                period: str = period_map.get(interval, "1")
                
                # 期货分钟线数据
                try:
                    df: DataFrame = ak.futures_zh_minute_sina(
                        symbol=symbol,
                        period=period
                    )
                except Exception as e:
                    output(f"期货分钟线数据获取失败: {e}")
                    output("提示: 期货分钟线数据可能需要较新的AkShare版本")
                    return None
                
                if df is None or df.empty:
                    output(f"期货分钟线数据为空: {symbol}")
                    return None
                
                # 筛选日期范围
                df["datetime"] = pd.to_datetime(df["datetime"])
                mask = (df["datetime"] >= start) & (df["datetime"] <= end)
                df = df.loc[mask].copy()
                
                df.rename(columns={
                    "open": "open",
                    "high": "high",
                    "low": "low",
                    "close": "close",
                    "volume": "volume"
                }, inplace=True)
                
                df.sort_values("datetime", inplace=True)
                df.reset_index(drop=True, inplace=True)
                
                return df
                
        except Exception as ex:
            output(f"获取期货数据失败: {ex}")
            return None
    
    def _convert_to_bardata(
        self,
        df: DataFrame,
        symbol: str,
        exchange: Exchange,
        interval: Interval
    ) -> List[BarData]:
        """
        将DataFrame转换为BarData列表
        
        Args:
            df: 原始数据DataFrame
            symbol: VeighNa格式的合约代码
            exchange: 交易所
            interval: K线周期
            
        Returns:
            BarData列表
        """
        bars: List[BarData] = []
        
        for ix, row in df.iterrows():
            # 确保datetime是datetime对象
            dt: datetime = row["datetime"]
            if isinstance(dt, str):
                dt = pd.to_datetime(dt)
            if hasattr(dt, 'to_pydatetime'):
                dt = dt.to_pydatetime()
            
            # 添加时区信息
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=CHINA_TZ)
            
            # 创建BarData对象
            bar: BarData = BarData(
                symbol=symbol,
                exchange=exchange,
                datetime=dt,
                interval=interval,
                volume=row.get("volume", 0),
                turnover=row.get("turnover", 0),
                open_interest=row.get("open_interest", 0),
                open_price=row.get("open", 0),
                high_price=row.get("high", 0),
                low_price=row.get("low", 0),
                close_price=row.get("close", 0),
                gateway_name="AKSHARE"
            )
            
            bars.append(bar)
        
        return bars
