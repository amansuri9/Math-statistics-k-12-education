import pandas as pd
import numpy as np
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import MultiSelect, Button, Select, Div, CheckboxGroup


class PivotTable:
    """Class to create scatter plot object. Instantiated in allTabs.py."""

    def __init__(self, original):
        """Initialize scatter plot object.

        Keyword arguments:
        original -- the data processor object containing data and list of categorical indices
        """

        # Read in data table, tell Bokeh it's the data we're using
        self.original = original.df
        self.source = ColumnDataSource(original.df)

        # Take in the column names and the indices of those names that are categorical
        self.columnNames = list(self.original.columns.values)
        self.valueOptions = list(self.original.columns.values)

        self.colIndices = original.cat_indices

        # Checkboxes for categorical variables
        self.checkPanel = CheckboxGroup(labels=self.columnNames, active=self.colIndices)

        # Remove categoricals from value box on start
        self.updateValueOptions()

        # Create input tools that live on left side of pivot table
        self.valuesSelect = MultiSelect(title="Values:", options=self.valueOptions)
        self.indexSelect = MultiSelect(title="Indices:", options=self.columnNames)
        self.columnsSelect = MultiSelect(title="Columns:", options=self.columnNames)

        # Bokeh currently does not have label attribute for checkbox panels
        self.catLabel = Div(text="<label>Categorical Variables:</label>")

        # Allow user to select aggregate function (currently sum or average)
        self.aggSelect = Select(title="Aggregate Function:", value="Sum", options=["Sum", "Average"])

        # Set up update button to make changes take effect
        self.updateButton = Button(label="Update", button_type="success")

        # Placeholder for where error messages show up
        self.errorDiv = Div(text="", width=200, height=100)

        # Generate table to show user the actual data set before any pivot table stuff happens
        self.table = Div(text=self.toBootstrapTable(self.original.to_html()), width=900, height=400)

        # Bind all of input tools to one widgetbox
        self.inputs = widgetbox(self.valuesSelect, self.indexSelect, self.columnsSelect, self.aggSelect, self.catLabel,
                                self.checkPanel, self.updateButton, self.errorDiv)

        # Tell Bokeh to put input tools on left and table on right
        self.toReturn = row(self.inputs, self.table, width=800)

    def updateValueOptions(self):
        """Update values for categorical checkboxes."""
        self.valueOptions = list(self.original.columns.values)
        temp = list(self.original.columns.values)
        for i in range(0, len(temp)):
            if i in self.checkPanel.active:
                self.valueOptions.remove(temp[i])

    def toBootstrapTable(self, html):
        """Make things Bootstrap-friendly"""
        return html.replace("dataframe", "table table-fixed table-striped").replace("<th>", "<th class=\"col-xs\">")

    def update_data(self):
        """Runs whenever the update button is clicked, generates/updates pivot table"""
        # Generate pandas pivot table
        self.pivotTable = pd.pivot_table(self.original, values=self.valuesSelect.value,
                                         index=self.indexSelect.value, columns=self.columnsSelect.value)

        # Change the aggregate function to sum if selected
        if self.aggSelect.value == "Sum":
            self.pivotTable.aggfunc = np.sum

        # Generate the actual pivot table
        self.table = Div(text=self.toBootstrapTable(self.pivotTable.to_html()), width=900, height=400)

        self.errorDiv.text = ""
        self.toReturn.children[1] = self.table

