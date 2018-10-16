import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
# Above imports taken from Github. Reasons for why this import structure was recommended are unknown.
import pandas as pd
from bokeh.layouts import widgetbox, row
from bokeh.models.widgets import Button, Select, MultiSelect, Div
from patsy import dmatrices, dmatrix
import statsmodels.api as sm


class Regression:
    """Class to create regression object. Instantiated in allTabs.py."""

    def __init__(self, original):
        """Initialize regression object.

        Keyword arguments:
        original -- the data processor object containing data and list of categorical indices
        """

        self.original = original.df

        # Sets up widgets to take user input
        self.y_select = Select(title="Value to Predict:", options=list(self.original.columns.values))
        self.x_select = MultiSelect(title="Values used to Predict:", options=list(self.original.columns.values))
        self.updateButton = Button(label="Calculate Regression", button_type="success")
        self.inputs = widgetbox(self.y_select, self.x_select, self.updateButton)

        # Defines an object variable that is later used to display regression info
        self.p = Div(text=" ")

        # Defines an object variable that holds the entire layout for this tab
        self.toReturn = row(self.inputs, self.p)

    def toBootstrapTable(self, html):
        """ This function makes the regression information prettier.

        Keyword arguments:
        html -- variable containing html code
        """
        return html.replace("dataframe", "table table-fixed table-striped")

    def updateRegression(self):
        """Used to update the regression information"""
        # String manipulation to create a formula for the dmatrices function
        formula = (self.y_select.value + " ~ " + ' + '.join(self.x_select.value))

        # Make sure we don't pass a bad formula on initialization
        if formula != " ~ ":
            y, X = dmatrices(formula, self.original, return_type='dataframe')
            model = sm.OLS(y, X)
            regression = model.fit()
            dataTable = pd.read_csv(StringIO(regression.summary().tables[1].as_csv()))
            self.p = Div(text=self.toBootstrapTable(dataTable.to_html()), width=900, height=400)
            self.toReturn.children[1] = self.p
