from util import utility, graphs

fr = open(utility.BASE_PATH + "/leave_one_results.csv", "r")
line = fr.readline()
lines = fr.readlines()
fr.close()
precisions = []
recalls = []
fscores = []
for line in lines:
    data = line.strip().split("\t")
    precisions.append(float(data[2]))
    recalls.append(float(data[3]))
    fscores.append(float(data[4]))

X = []
Y = []
x, y = utility.ecdf(precisions)
X.append(x*100)
Y.append(y)

x, y = utility.ecdf(recalls)
X.append(x*100)
Y.append(y)

x, y = utility.ecdf(fscores)
X.append(x*100)
Y.append(y)

configs = {}
configs["x_label"] = "Score"
configs["y_label"] = "CDF"
configs["legends"] = ["Precision", "Recall", "F1"]
configs['marker'] = True
graphs.draw_line_graph_multiple_with_x(X, Y, configs)