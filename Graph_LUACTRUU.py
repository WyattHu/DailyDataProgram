import pandas as pd
from matplotlib import pyplot as plt


def run():
    df1 = pd.read_excel('DailyData/LUACTRUU.xlsx')
    # print(df1)
    plt.cla()
    plt.figure(figsize=(2, 0.35))
    plt.plot(df1['PX_LAST'], color='r')
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.yticks([])
    plt.xticks([])
    plt.savefig('DailyData/LUACTRUU.jpg')


if __name__ == '__main__':
    run()
