class Agency():
    
    def __init__(self, df, name, current_quarter, current_year):
        """
        Constructor method; creates a Agency object initialized with the basic attributes of a agency being reported on.

        :param df: The central DataFrame that information will be pulled from - includes the data for all agencies, not just the agency that the object represents.
        :param name: The name of the agency that this object represents.
        :param current_quarter: The quarter that this agency will be reporting on.
        :param current_year: The year that this agency will be reporting on. 
        """
        self.df = df
        self.name = name
        self.agency_df = df.loc[df["Agency Name"] == name]  # a DataFrame only containing data relevant to the agency that the object represents
        self.abbreviation = ""  # the abbreviation of the passed agency
        self.current_quarter = current_quarter 
        self.current_year = current_year
