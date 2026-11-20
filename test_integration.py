"""
测试vnpy_akshare在VeighNa中的集成
"""

from datetime import datetime
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.datafeed import get_datafeed
from vnpy.trader.object import HistoryRequest


def test_datafeed():
    """测试数据服务"""
    print("=" * 60)
    print("测试vnpy_akshare数据服务")
    print("=" * 60)
    
    # 获取数据服务实例
    try:
        datafeed = get_datafeed()
        print(f"✓ 数据服务实例创建成功: {type(datafeed).__name__}")
    except Exception as e:
        print(f"✗ 数据服务实例创建失败: {e}")
        return
    
    # 测试1: 获取股票日线数据
    print("\n[测试1] 获取贵州茅台(600519.SH)日线数据")
    try:
        req = HistoryRequest(
            symbol="600519",
            exchange=Exchange.SSE,
            start=datetime(2024, 1, 1),
            end=datetime(2024, 1, 31),
            interval=Interval.DAILY
        )
        
        bars = datafeed.query_bar_history(req)
        
        if bars:
            print(f"✓ 成功获取 {len(bars)} 条K线数据")
            print(f"  第一条: {bars[0].datetime.date()} O:{bars[0].open_price} C:{bars[0].close_price}")
            print(f"  最后一条: {bars[-1].datetime.date()} O:{bars[-1].open_price} C:{bars[-1].close_price}")
        else:
            print("✗ 未获取到数据")
    except Exception as e:
        print(f"✗ 获取数据失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试2: 获取期货日线数据
    print("\n[测试2] 获取螺纹钢(rb2405.SHFE)日线数据")
    try:
        req = HistoryRequest(
            symbol="rb2405",
            exchange=Exchange.SHFE,
            start=datetime(2024, 1, 1),
            end=datetime(2024, 1, 31),
            interval=Interval.DAILY
        )
        
        bars = datafeed.query_bar_history(req)
        
        if bars:
            print(f"✓ 成功获取 {len(bars)} 条K线数据")
            print(f"  第一条: {bars[0].datetime.date()} O:{bars[0].open_price} C:{bars[0].close_price}")
            print(f"  最后一条: {bars[-1].datetime.date()} O:{bars[-1].open_price} C:{bars[-1].close_price}")
        else:
            print("✗ 未获取到数据")
    except Exception as e:
        print(f"✗ 获取数据失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    test_datafeed()
