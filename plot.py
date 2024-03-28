from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT,
    )
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, xlabel="x", ylabel="y", title="Title"):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)
        fig.set_facecolor('#f8f9f9')
        super(MplCanvas, self).__init__(fig)
        self.toolbar = NavigationToolbar2QT(self, parent)

        self.x_data = []
        self.y_data = []

        self.graph, = self.axes.plot(self.x_data, self.y_data)
    
    def append_data(self, x_data, y_data):
        self.x_data.extend(x_data)
        self.y_data.extend(y_data)
        if x_data:
            #print(self.x_data)
            self.axes.set_xlim(self.x_data[0], self.x_data[-1])
        else:
            self.axes.set_xlim(0, 0)
        if y_data:    
            self.axes.set_ylim(min(self.y_data), max(self.y_data))
        else:
            self.axes.set_ylim(0, 0)

        self.graph.set_xdata(self.x_data)
        self.graph.set_ydata(self.y_data)
        self.toolbar.update()

        self.draw()

    def data(self):
        return self.x_data, self.y_data
    
    def clear(self):
        self.x_data = []
        self.y_data = []
        self.axes.set_xlim(0, 0)
        self.axes.set_ylim(0, 0)
        self.graph.set_xdata([])
        self.graph.set_ydata([])
        self.toolbar.update()
        self.draw()


class MplImage(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, xlabel="x", ylabel="y", title="Title"):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self._meta_setter()
        fig.set_facecolor('#f8f9f9')
        super(MplImage, self).__init__(fig)
        self.toolbar = NavigationToolbar2QT(self, parent)
    
    def update_data(self, data, extent_x: tuple[float, float]=(0, 1), extent_y: tuple[float, float]=(0, 1)):
        self.axes.cla()
        self.axes.imshow(data, cmap='inferno', aspect='auto', extent=[extent_x[0], extent_x[1], extent_y[0], extent_y[1]])
        self._meta_setter()
        self.draw()
    
    def _meta_setter(self):
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        self.axes.set_title(self.title)

    def clear(self):
        self.axes.cla()
        self._meta_setter()
        self.toolbar.update()
        self.draw()