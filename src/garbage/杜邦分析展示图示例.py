# 在金融领域，人们从公司的财务报表，如年度损益表、资产负债表和现金流量表，发觉有用的信息。
# 比率分析是常用的工具之一，常常用来比较不同企业之间以及同一公司历年来的表现。
# 杜邦等式是比率分析中的一种，是把股本回报率分为毛利率、资产周转率和权益乘数三个比率。

import pandas as pd
import matplotlib.pyplot as plt

ticker = 'Ticker'
name1 = 'profitMargin'
name2 = 'assetTurnover'
name3 = 'equitMultiplier'
scale = 7

raw_data = {ticker: ['IBM', 'DELL', 'WMT'],
            name1: [0.1589*scale, 0.0417*scale, 0.036*scale],
            name2: [0.8766, 1.1977, 2.31],
            name3: [6.32, 4.45, 2.6604]}
df = pd.DataFrame(raw_data, columns=[ticker, name1, name2, name3])
f, ax1 = plt.subplots(1, figsize=(10, 5))
w = 0.75
x = [i+1 for i in range(len(df[name1]))]

tick_pos = [i+(w/2.) for i in x]
ax1.bar(x, df[name1], width=w, label=name1, alpha=0.5, color='blue')
ax1.bar(x, df[name2], width=w, bottom=df[name1], label=name2, alpha=0.5, color='red')
ax1.bar(x, df[name3], width=w, bottom=[i+j for i, j in zip(df[name1], df[name2])],
        label=name3, alpha=0.5, color='green')
plt.xticks(tick_pos, df[ticker])
plt.ylabel("Dupoint Identity")
plt.xlabel("Different tickers")
plt.legend(loc='upper right')
plt.title("Dupoint Identity for 3 firms")
plt.xlim([min(tick_pos)-w, max(tick_pos)+w])
plt.show()

# matplotlib呈现杜邦分析图例成功，之后要在另外一个库里面编写matplotlob使用手册
