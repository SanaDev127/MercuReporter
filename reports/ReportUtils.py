import matplotlib.pyplot as plt
import base64
from io import BytesIO
import plotly.express as px


def get_matplot_graph():
    buffer = BytesIO
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    return graph


def plotly_plot_pie(data_df, plot_title, plot_values, plot_names, height=1000, width=1000):
    fig = px.pie(data_df, title=plot_title, values=plot_values, names=plot_names, height=height, width=width)
    chart = fig.to_html()
    return chart


# x_axis, y_axis
# x=x_axis, y=y_axis
def plotly_plot_line(data_df, plot_title, height=1000, width=1000):
    fig = px.line(data_df, title=plot_title, height=height, width=width)
    chart = fig.to_html()
    return chart


def plotly_line_plot_test(data_df, plot_title, height=1000, width=1000):
    fig = px.line(data_df, title=plot_title, height=height, width=width)
    chart = fig.to_image()
    return chart


def plot_pie(data_df, data_column, fig_length, fig_height, title=None, colors=None):
    plt.switch_backend('AGG')
    fig = plt.figure()
    plot = data_df.astype(float).plot.pie(y=data_column,
                                          shadow=False,
                                          startangle=90,
                                          autopct='%1.1f%%',
                                          figsize=(fig_length, fig_height),
                                          )

    plt.axis('equal')
    plt.tight_layout()
    if title:
        plt.title(title)
    graph = get_matplot_graph()
    return graph


def plot_bar():
    pass


def plot_barh(yLabels, yvalues, xvalues, fig_length, fig_height, title=None):
    fig = plt.figure()
    plt.barh(yvalues, xvalues, figure=fig, figsize=(fig_length, fig_height))
    plt.yticks(yvalues, yLabels, figure=fig)


# https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.line.html
def plot_line(data_df, fig_length, fig_height):
    fig = plt.figure()
    plot = data_df.plot.line(figsize=(fig_length, fig_height))
    plt.tight_layout()
    plt.savefig("test_line_plot")
    return fig
