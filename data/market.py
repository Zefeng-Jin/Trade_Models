from enum import Enum


class market(Enum):

    # 日期
    date = "BUSI_DATE"

    # 股票代码
    code = "STOCK_CODE"

    # 发送时间
    time = "OCCUR_TIME"

    # 公开价格
    open = "OPEN_PRICE"

    # 最高价格
    high = "HIGH_PRICE"

    # 最低价格
    low = "LOW_PRICE"

    # 收盘价
    close = "CLOSE_PRICE"

    # 调整收盘价
    adj_close = "ADJUST_CLOSE_PRICE"

    # 成交量
    volume = "VOLUME"
