import unittest

from vnpy_akshare.akshare_datafeed import to_ak_symbol
from vnpy.trader.constant import Exchange


class TestToAkSymbol(unittest.TestCase):
    """测试合约代码转换功能"""
    
    # 股票
    def test_stock(self) -> None:
        """测试股票代码转换"""
        self.assertEqual(to_ak_symbol('600519', Exchange.SSE), "600519.SH")  # 沪市
        self.assertEqual(to_ak_symbol('300750', Exchange.SZSE), "300750.SZ")  # 深市
        self.assertEqual(to_ak_symbol('835368', Exchange.BSE), "835368.BJ")  # 北交所
    
    # 期货 - 上期所
    def test_future_shfe(self) -> None:
        """测试上期所期货代码转换"""
        self.assertEqual(to_ak_symbol('rb2405', Exchange.SHFE), "RB2405")  # 螺纹钢
        self.assertEqual(to_ak_symbol('au2406', Exchange.SHFE), "AU2406")  # 黄金
    
    # 期货 - 大商所
    def test_future_dce(self) -> None:
        """测试大商所期货代码转换"""
        self.assertEqual(to_ak_symbol('i2405', Exchange.DCE), "I2405")  # 铁矿石
        self.assertEqual(to_ak_symbol('m2405', Exchange.DCE), "M2405")  # 豆粕
    
    # 期货 - 郑商所(特殊格式)
    def test_future_czce(self) -> None:
        """测试郑商所期货代码转换"""
        self.assertEqual(to_ak_symbol('SR2401', Exchange.CZCE), "SR401")  # 白糖
        self.assertEqual(to_ak_symbol('CF2401', Exchange.CZCE), "CF401")  # 棉花
    
    # 期货 - 中金所
    def test_future_cffex(self) -> None:
        """测试中金所期货代码转换"""
        self.assertEqual(to_ak_symbol('IF2401', Exchange.CFFEX), "IF2401")  # 股指期货
        self.assertEqual(to_ak_symbol('IC2401', Exchange.CFFEX), "IC2401")  # 中证500
    
    # 期货 - 能源中心
    def test_future_ine(self) -> None:
        """测试能源中心期货代码转换"""
        self.assertEqual(to_ak_symbol('sc2401', Exchange.INE), "SC2401")  # 原油


if __name__ == '__main__':
    unittest.main()
