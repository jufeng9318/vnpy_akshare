"""
vnpy_akshare使用示例
演示如何使用AkShare数据服务获取股票和期货数据
"""

from datetime import datetime
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.datafeed import get_datafeed
from vnpy.trader.object import HistoryRequest


def test_stock_daily():
    """测试获取股票日线数据"""
    print("=" * 60)
    print("测试1: 获取贵州茅台(600519.SH)日线数据")
    print("=" * 60)
    
    # 获取数据服务实例
    datafeed = get_datafeed()
    
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
    
    if bars:
        print(f"成功获取 {len(bars)} 条数据")
        print("\n前5条数据:")
        for bar in bars[:5]:
            print(f"日期: {bar.datetime.date()}, "
                  f"开: {bar.open_price:.2f}, "
                  f"高: {bar.high_price:.2f}, "
                  f"低: {bar.low_price:.2f}, "
                  f"收: {bar.close_price:.2f}, "
                  f"量: {bar.volume}")
    else:
        print("未获取到数据")
    
    print()


def test_stock_minute():
    """测试获取股票分钟线数据"""
    print("=" * 60)
    print("测试2: 获取宁德时代(300750.SZ) 60分钟线数据")
    print("=" * 60)
    
    # 获取数据服务实例
    datafeed = get_datafeed()
    
    # 创建历史数据请求
    req = HistoryRequest(
        symbol="300750",
        exchange=Exchange.SZSE,
        start=datetime(2024, 1, 1),
        end=datetime(2024, 1, 31),
        interval=Interval.HOUR
    )
    
    # 查询数据
    bars = datafeed.query_bar_history(req)
    
    if bars:
        print(f"成功获取 {len(bars)} 条数据")
        print("\n前5条数据:")
        for bar in bars[:5]:
            print(f"时间: {bar.datetime}, "
                  f"开: {bar.open_price:.2f}, "
                  f"高: {bar.high_price:.2f}, "
                  f"低: {bar.low_price:.2f}, "
                  f"收: {bar.close_price:.2f}, "
                  f"量: {bar.volume}")
    else:
        print("未获取到数据")
    
    print()


def test_future_daily():
    """测试获取期货日线数据"""
    print("=" * 60)
    print("测试3: 获取螺纹钢(rb2405.SHFE)日线数据")
    print("=" * 60)
    
    # 获取数据服务实例
    datafeed = get_datafeed()
    
    # 创建历史数据请求
    req = HistoryRequest(
        symbol="rb2405",
        exchange=Exchange.SHFE,
        start=datetime(2024, 1, 1),
        end=datetime(2024, 3, 31),
        interval=Interval.DAILY
    )
    
    # 查询数据
    bars = datafeed.query_bar_history(req)
    
    if bars:
        print(f"成功获取 {len(bars)} 条数据")
        print("\n前5条数据:")
        for bar in bars[:5]:
            print(f"日期: {bar.datetime.date()}, "
                  f"开: {bar.open_price:.2f}, "
                  f"高: {bar.high_price:.2f}, "
                  f"低: {bar.low_price:.2f}, "
                  f"收: {bar.close_price:.2f}, "
                  f"量: {bar.volume}, "
                  f"持仓: {bar.open_interest}")
    else:
        print("未获取到数据")
    
    print()


def test_future_minute():
    """测试获取期货分钟线数据"""
    print("=" * 60)
    print("测试4: 获取股指期货(IF2401.CFFEX) 1分钟线数据")
    print("=" * 60)
    
    # 获取数据服务实例
    datafeed = get_datafeed()
    
    # 创建历史数据请求
    req = HistoryRequest(
        symbol="IF2401",
        exchange=Exchange.CFFEX,
        start=datetime(2024, 1, 2),
        end=datetime(2024, 1, 5),
        interval=Interval.MINUTE
    )
    
    # 查询数据
    bars = datafeed.query_bar_history(req)
    
    if bars:
        print(f"成功获取 {len(bars)} 条数据")
        print("\n前5条数据:")
        for bar in bars[:5]:
            print(f"时间: {bar.datetime}, "
                  f"开: {bar.open_price:.2f}, "
                  f"高: {bar.high_price:.2f}, "
                  f"低: {bar.low_price:.2f}, "
                  f"收: {bar.close_price:.2f}, "
                  f"量: {bar.volume}")
    else:
        print("未获取到数据")
    
    print()


if __name__ == "__main__":
    """运行所有测试"""
    print("\n开始测试vnpy_akshare数据服务...\n")
    
    try:
        # 测试股票日线
        test_stock_daily()
        
        # 测试股票分钟线
        test_stock_minute()
        
        # 测试期货日线
        test_future_daily()
        
        # 测试期货分钟线
        test_future_minute()
        
        print("=" * 60)
        print("所有测试完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
