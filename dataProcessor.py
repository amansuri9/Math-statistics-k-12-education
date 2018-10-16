import pandas as pd


class DataProcessor:
    """Data Processor class to manage data. Has a dataframe containing the data (df) and a list of indices of the
    columns in the dataframe that are categorical (cat_indices).
    """

    def __init__(self):
        """Initialize DataProcessor with an empty dataframe and an empty list."""
        self.df = pd.DataFrame()  # dataframe to hold data
        self.cat_indices = []     # holds indices of columns that are categorical

    def setUp(self, filename):
        """Populate the df and set up cat_indices when a file is uploaded. Called in allTabs.py

        Keyword arguments:
        filename -- the filename of the csv file containing the data
        """
        self.df = pd.read_csv(filename)
        self.guessCategorical()

    def clearDf(self):
        """Set df and cat_indices to null when user logs out."""
        self.df = pd.DataFrame()
        self.cat_indices = []

    def guessCategorical(self):
        """Basic function to pre-determine which columns are categorical"""
        for i in range(0, self.df.shape[1]):
            if not str(self.df.iloc[0, i]).replace('.', '').isdigit():
                self.cat_indices.append(i)

    def setCatIndices(self, new_indices):
        """Set cat_indices with new values"""
        self.cat_indices = new_indices
