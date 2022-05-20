import matplotlib.pyplot as plt

x = [5000, 10000, 15000]
y = [5000, 0, -5000]
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines['bottom'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.plot(x, y)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.xlabel('期货价格', fontsize=12)
plt.ylabel('空头盈亏', fontsize=12)
plt.title('期货空头盈亏图', fontsize=12)
plt.show()
