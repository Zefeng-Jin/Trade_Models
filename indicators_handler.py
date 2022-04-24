def sma(df, fast, slow):
    """
    计算算术移动平均线
    :param df:
    :param fast:
    :param slow:
    :return:
    """
    df['ema_fast'] = df['Close'].ewm(span=fast, adjust=False, min_periods=fast).mean()
    df['ema_slow'] = df['Close'].ewm(span=slow, adjust=False, min_periods=slow).mean()
    df.dropna(inplace=True)
    return df


def atr(df, n):
    """
    计算真实波幅均值
    :param df:
    :param n:
    :return:
    """
    df = df.copy()
    df['H-L'] = abs(df['High'] - df['Low'])
    df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    df['ATR'] = df['TR'].ewm(span=n, adjust=False, min_periods=n).mean()
    df2 = df.drop(['H-L', 'H-PC', 'L-PC'], axis=1)
    return df2


