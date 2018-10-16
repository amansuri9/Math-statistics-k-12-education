from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.models.widgets import Select, TextInput, Div
from bokeh.layouts import widgetbox, row
from bokeh.transform import jitter
from operator import xor


class Scatterplot:
    """Class to create scatter plot object. Instantiated in allTabs.py."""

    def __init__(self, original):
        """Initialize scatter plot object.

        Keyword arguments:
        original -- the data processor object containing data and list of categorical indices
        """

        self.original = original.df
        self.source = ColumnDataSource(original.df)
        self.errorDiv = Div(text="", width=200, height=100)

        # The list of the columns for any upload doc
        self.colnames = list(self.original.columns.values)
        self.catIndices = original.cat_indices

        # Set up widgets, where x and y plot the first two columns
        self.text = TextInput(title="Plot Title", value='Scatter Plot')
        self.x_select = Select(title="x value:", value=list(self.original.columns.values)[0], options=self.colnames)
        self.y_select = Select(title="y value:", value=list(self.original.columns.values)[1], options=self.colnames)
        self.p = figure(plot_width=600, plot_height=400, title="Scatter Plot")
        self.p = self.plot(self.x_select.value, self.y_select.value)

        # Set up layouts and add to document
        self.inputs = widgetbox(self.text, self.x_select, self.y_select, self.errorDiv)
        self.toReturn = row(self.inputs, self.p, width=800)

    def plot(self, x, y):
        """Returns a scatterplot with given x and y values.

        Keyword arguments:
        x -- column name of column to be plotted on x-axis
        y -- column name of column to be plotted on y-axis
        """
        # Hovering Tool
        self.hover = HoverTool(tooltips=[
            (self.x_select.value, "@" + self.x_select.value),
            (self.y_select.value, "@" + self.y_select.value)
        ])

        x_cat = self.colnames.index(x) in self.catIndices
        y_cat = self.colnames.index(y) in self.catIndices

        p = figure(plot_width=600, plot_height=400, title=self.text.value, tools=[self.hover])
        p.x_range.range_padding = 0
        p.ygrid.grid_line_color = None

        # Handling of plotting numerical and categorical variables
        # When one variable is categorical
        if xor(x_cat, y_cat):

            # When x is categorical and y is numerical
            if x_cat:
                p = figure(plot_width=600, plot_height=400, x_range=self.original[x].unique(), title=self.text.value,
                           tools=[self.hover], x_axis_label=x, y_axis_label=y)

                # Add spacing if categorical variables are numbers
                try:
                    p.x_range.start = min(self.original[x].unique())-1
                    p.x_range.end = max(self.original[x].unique())+1
                except:
                    pass

                p.circle(x=x, y=jitter(y, width=0.6, range=self.p.x_range), source=self.source, alpha=0.3)
                self.errorDiv.text = " "
                return p

            # When y is categorical and x numerical
            else:
                p = figure(plot_width=600, plot_height=400, y_range=self.original[y].unique(), title=self.text.value,
                           tools=[self.hover], x_axis_label=x, y_axis_label=y)

                # Add spacing if categorical variables are numbers
                try:
                    p.y_range.start = min(self.original[y].unique())-1
                    p.y_range.end = max(self.original[y].unique())+1
                except:
                    pass

                p.circle(x=jitter(x, width=0.6, range=self.p.x_range), y=y, source=self.source, alpha=0.3)
                self.errorDiv.text = " "
                return p

        # When both variables are categorical
        elif x_cat and y_cat:
                self.errorDiv.text = "<p style=\"color:red\">You cannot plot two categorical options</p>"
                return p  # Returns a blank graph/figure

        # When plotting two numerical variables
        else:
                p = figure(plot_width=600, plot_height=400, title=self.text.value,
                           tools=[self.hover], x_axis_label=x, y_axis_label=y)
                p.circle(x=x, y=jitter(y, width=0.6, range=self.p.y_range), source=self.source, alpha=0.3)
                self.errorDiv.text = " "
                return p

    def update_title(self, attrname, old, new):
        """Update title of graph."""
        self.p.title.text = self.text.value
        p = self.plot(self.x_value.value, self.y_select.value)
        self.toReturn.children[1] = p

    def update_data(self, attrname, old, new):
        """Update what data is plotted."""
        x = self.x_select.value
        y = self.y_select.value
        p = self.plot(x, y)
        self.toReturn.children[1] = p
