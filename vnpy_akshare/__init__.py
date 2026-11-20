"""
VeighNa框架的AkShare数据服务接口
"""

import importlib_metadata

from .akshare_datafeed import AkShareDatafeed as Datafeed


try:
    __version__ = importlib_metadata.version("vnpy_akshare")
except importlib_metadata.PackageNotFoundError:
    __version__ = "1.0.0.dev0"
