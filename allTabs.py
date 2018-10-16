from bokeh.models.widgets import Panel, Tabs
from pivotTableHTML import PivotTable
from scatterplotHTML import Scatterplot
from regressionsHTML import Regression
from functools import partial
from dataProcessor import DataProcessor


class AllTabs:
    """Serves as a communicator between the flask part of the application (__init__.py), the backend (DataProcessor),
    and each of the bokeh tabs (PivotTable, Scatterplot, Regression).
    """

    def __init__(self):
        """Initialize allTabs object."""
        self.dp = DataProcessor()

    def update_df(self, filename):
        """Update the backend when a file is uploaded. Called in __init__.py

        Keyword arguments:
        filename -- the filename of the csv file containing the data
        """
        self.dp.setUp(filename)

    def clear_df(self):
        """Removes data from the data processor. Called in __init__.py upon logout."""
        self.dp.clearDf()

    def runServer(self, doc):
        """Starts the bokeh server.

        Keyword arguments:
        doc -- passed automatically when called in __init__.py
        """
        original = self.dp

        # Each tab is now it's own object so information can go between one another from this file
        pt = PivotTable(original)
        sp = Scatterplot(original)
        reg = Regression(original)

        def pivotCallback():
            """Callback for pivot table."""
            try:
                # attempt to update pivot table data
                pt.update_data()

                # only update backend if the categorical list was changed
                if self.dp.cat_indices != pt.checkPanel.active:
                    self.dp.cat_indices = pt.checkPanel.active
                    sp.catIndices = self.dp.cat_indices

            except Exception as e:
                # display exception in pivot table tab
                pt.toReturn.children[0].children[7].text = "<p style=\"color:red\">" + \
                    str(e) + "</p>"

        # on_change and on_click handlers need to go outside or else passing data between tabs can't happen
        for w in [pt.updateButton]:
            w.on_click(partial(pivotCallback))

        def checkboxCallback(placeholder):
            """Callback for checkboxes in pivot tab. Updates the backend on change."""
            # only update backend if the categorical list was changed
            if self.dp.cat_indices != pt.checkPanel.active:

                try:
                    self.dp.cat_indices = pt.checkPanel.active
                    sp.catIndices = self.dp.cat_indices

                    # Update options for values in pivot table based on checkboxes
                    pt.updateValueOptions()
                    pt.toReturn.children[0].children[0].options = pt.valueOptions

                    # Redraw scatterplot as soon as the checkboxes are changed
                    sp.toReturn.children[1] = sp.plot(sp.x_select.value, sp.y_select.value)

                except Exception as e:
                    pass

        # Pivot table listener
        for w in [pt.checkPanel]:
            w.on_click(partial(checkboxCallback))

        # Scatter plot listener for x and y values
        for w in [sp.x_select, sp.y_select]:
            w.on_change('value', sp.update_data)

        # Scatter plot listener for title change
        sp.text.on_change('value', sp.update_title)

        # Regression listener
        reg.updateButton.on_click(reg.updateRegression)


        # toReturn corresponds to a bokeh row attribute in each object
        tab1 = Panel(child=pt.toReturn, title="Pivot Table")
        tab2 = Panel(child=sp.toReturn, title="Scatterplot")
        tab3 = Panel(child=reg.toReturn, title="Regression")

        allTabs = Tabs(tabs=[tab1, tab2, tab3])
        doc.add_root(allTabs)
