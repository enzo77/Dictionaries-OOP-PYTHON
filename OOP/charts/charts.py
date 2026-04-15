"""
Project: Simple chart system using matplotlib.

This class provides a clean interface to generate charts.
All matplotlib details are hidden inside the class.

https://matplotlib.org
https://matplotlib.org/stable/tutorials/index.html
"""

import matplotlib.pyplot as plt


class Chart:

    def __init__(self, title="Chart"):
        self.title = title
        self.x = []
        self.y = []

    def set_data(self, x, y):
        self.x = x
        self.y = y

    def line_chart(self):
        plt.figure()
        plt.plot(self.x, self.y)
        plt.title(self.title)

    def bar_chart(self):
        plt.figure()
        plt.bar(self.x, self.y)
        plt.title(self.title)

    def scatter_chart(self):
        plt.figure()
        plt.scatter(self.x, self.y)
        plt.title(self.title)

    def save(self, filename):
        plt.savefig(filename)

    def show(self):
        plt.show()


if __name__ == "__main__":

    chart = Chart("Monthly Sales")

    months = ["Jan", "Feb", "Mar", "Apr"]
    sales = [100, 150, 130, 170]

    chart.set_data(months, sales)

    # Line chart
    chart.line_chart()
    chart.save("line_chart.png")
    chart.show()

    # Bar chart
    chart.bar_chart()
    chart.save("bar_chart.png")
    chart.show()

    # Scatter chart
    chart.scatter_chart()
    chart.save("scatter_chart.png")
    chart.show()