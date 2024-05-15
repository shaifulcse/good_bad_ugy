import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)

styles = ["-", "--", "-.", ":", "-", "--", "-.", ":"]
marks = ["^", "d", "o", "v", "p", "s", "<", ">"]
width = [3, 3, 3, 3, 3, 3, 3, 3]
marks_size = [20, 20, 20, 20, 20, 10, 12, 15]
marker_color = ['#0F52BA', '#ff7518', '#6CA939', '#e34234', '#756bb1', 'brown', '#c994c7', '#636363']
gaps = [4, 4, 4, 4, 4, 4, 4, 4]


def draw_line_graph(lists, config):
    index = 0
    for list in lists:
        ln = (plt.plot(range(1, len(list) + 1), list))
        plt.setp(ln, linewidth=width[index], ls=styles[index], color=marker_color[index])
        index += 1
    if "x_label" in config:
        plt.xlabel(config["x_label"], fontsize=24)
    if "y_label" in config:
        plt.ylabel(config["y_label"], fontsize=24)
    if "legends" in config:
        plt.legend(config["legends"], loc=0, fontsize=20)
    if "xscale" in config:
        if config["xscale"]:
            plt.xscale("log")
    if "yscale" in config:
        if config["yscale"]:
            plt.yscale("log")

    plt.grid(True)
    if "x_ticks" in config:
        plt.xticks(config["x_ticks"])

    for label in ax.get_xticklabels():
        label.set_fontsize(20)
    for label in ax.get_yticklabels():
        label.set_fontsize(20)

    if "xlim" in config:
        plt.xlim(config["xlim"])

    plt.tight_layout()
    plt.show()
