from itertools import cycle
from threading import Thread

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

cycol = cycle(['b', 'g', 'r', 'c', 'm', 'k', 'y', 'olive', 'burlywood', 'chartreuse', 'brown'])


class GraphManager:

    def __init__(self):
        super().__init__()
        self.current_plots = []

    def start(self) -> None:
        plt.show()

    def new_plot(self, y_data, legend=None):
        fig = plt.figure()
        ax = plt.axes()

        if isinstance(y_data, (dict, list)):
            for index, item in enumerate(y_data):
                date, data = self.split_dict(y_data[item])
                plt.plot_date(date, data, "-o", color=next(cycol), label=item)

        font_p = FontProperties()
        font_p.set_size('small')
        fig.legend(legend, prop=font_p)
        self.current_plots.append(fig)

        return fig

    def split_dict(self, y_data):
        x_axis = []
        y_axis = []
        for element in y_data:
            x_axis.append(element["date"])
            y_axis.append(element["data"])

        return x_axis, y_axis
