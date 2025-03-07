import matplotlib.pyplot as plt

def create_pie_chart(data, labels=None, title="资产分配图", notes=None):
    # 设置中文字体（解决标题显示问题）
    plt.rcParams['font.sans-serif'] = ['Heiti TC']  # 微软雅黑也可以用'Arial Unicode MS'
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    if not labels:
        labels = [f'资产类别 {i+1}' for i in range(len(data))]
    
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
    
    fig, ax = plt.subplots(figsize=(5, 4))
    wedges, texts, autotexts = ax.pie(
        data,
        labels=labels,
        colors=colors,
        autopct='%1.2f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 0.5},
        pctdistance=0.6  # 调整百分比位置
    )

    # 添加标题（调整标题位置和大小）
    plt.title(title, fontsize=16, pad=20)
    
    # 添加图例说明（带数值）
    legend_labels = [f'{l} ({v})' for l, v in zip(labels, data)]
    plt.legend(
        wedges,
        legend_labels, 
        title="资产详情",
        loc="center left",
        bbox_to_anchor=(1.05, 0, 0.5, 1)
    )

    # 添加备注文本框
    if notes:
        note_text = "\n".join([f"● {n}" for n in notes])
        plt.text(1.15, -1.1, note_text, fontsize=5, 
                bbox=dict(facecolor='#f0f0f0', alpha=0.5))

    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# 示例用法
if __name__ == "__main__":
    input_data = [303, 220, 350,50]
    sum = str(sum(input_data))
    asset_notes = [
        "股票投资（高风险）",
        "债券投资（稳定收益）",
        "现金储备（流动性资产）",
        "新兴资产（人称小彩票）",
        "总计"+sum
    ]
    create_pie_chart(
        input_data,
        labels=["股票", "债券", "现金","新兴资产"],
        notes=asset_notes
    )