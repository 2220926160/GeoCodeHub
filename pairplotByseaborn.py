import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

"""///////////// 1 生成基础数据
"""

np.random.seed(42)
data = {
    "Eco_S": np.random.rand(100),  # 生成100个0到1之间的随机数
    "Soc_S": np.random.rand(100),
    "Env_S": np.random.rand(100),
    "HQ": np.random.rand(100),
    "WY": np.random.rand(100),
    "CS": np.random.rand(100),
    "SC": np.random.rand(100),
}
df = pd.DataFrame(data)


"""///////////// 2 绘制图标

    2.1 绘制空表，有数据，但设置为透明，sns.pairplot的使用参考 https://seaborn.org.cn/generated/seaborn.pairplot.html
    2.2 在上三角绘制相关系数
    2.3 在下三角绘制散点图
"""

g = sns.pairplot(
    df,
    kind="scatter",
    diag_kind="kde",
    corner=False,  # 上三角不展示图，但展示文字，同样需要绘制
    height=2,
    aspect=1,
    plot_kws={"alpha": 0},  # 设置为透明
)


def corrfunc(x, y, **kws):
    """在上三角区域添加相关系数

    Parameters
    ----------
    x : _type_
        _description_
    y : _type_
        _description_
    """
    r = np.corrcoef(x, y)[0, 1]  # 相关系数 r = np.float64(-0.03403250097882254)
    ax = plt.gca()  # Get Current Axes
    ax.annotate(
        f"Corr:\n{r:.3f}",
        xy=(0.5, 0.5),
        xycoords="axes fraction",
        ha="center",
        va="center",
        fontsize=12,
        color=(0.5, 0, 0),
        alpha=0.8,
    )


g.map_upper(corrfunc)  # 2.2
g.map_lower(sns.scatterplot, marker="o", alpha=0.6, color=(0.6, 0.8, 0.2), s=70)  # 2.3


"""///////////// 3 调整坐标轴

    3.1 下三角及对角线启用浅灰色线条网格，清空底部、左侧标签，绘制顶部、右侧标签
    3.2 所有子图均绘制外轮廓
    3.3 除左侧与底部，其余子图除去刻度线
    3.4 调整布局，避免标签被遮挡
"""

col_num = len(df.columns)
for i, ax in enumerate(g.axes.flat):
    if ax is not None:
        # 3.1
        ax.set_xlabel("")
        ax.set_ylabel("")

        if i % col_num <= i // col_num:  # 下三角及对角线
            ax.grid(True, color=(0.8, 0.8, 0.8), linestyle="-", linewidth=0.5)
        if i < col_num:  # 顶部
            ax.annotate(
                df.columns[i],
                xy=(0.5, 1.05),
                xycoords="axes fraction",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                rotation=0,
            )
        if i % col_num == col_num - 1:  # 右侧
            ax.annotate(
                df.columns[i // col_num],
                xy=(1.05, 0.5),
                xycoords="axes fraction",
                ha="left",
                va="center",
                fontsize=10,
                fontweight="bold",
                rotation=270,
            )
        if i % col_num != 0 and i // col_num != col_num - 1:  # 非左侧非底部 删所有
            ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        elif i % col_num == 0 and i // col_num != col_num - 1:  # 左侧非底部 删底刻度
            ax.tick_params(left=True, bottom=False, labelleft=True, labelbottom=False)
        elif i % col_num != 0 and i // col_num == col_num - 1:  # 非左侧但底部 删左刻度
            ax.tick_params(left=False, bottom=True, labelleft=False, labelbottom=True)

        if i // col_num == col_num - 1:  # 底部 设置刻度倾斜 避免重叠
            for label in ax.get_xticklabels():
                label.set_rotation(45)

        #  3.2
        rect = Rectangle(
            (0, 0), 1, 1, transform=ax.transAxes, color="black", fill=False, lw=1
        )
        ax.add_patch(rect)

        # 3.3
        ax.set_xticks(np.linspace(0, 1, 5))
        ax.set_yticks(np.linspace(0, 1, 5))

plt.subplots_adjust(top=0.95, right=0.95)  # 3.4

plt.show()
