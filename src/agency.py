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

    # GETTER METHODS

    def get_agency_df(self):
        """
        Returns the DataFrame representing the agency and its APGs.

        :return: A slice of the central DataFrame used to initialize the object that only containts rows relevant to the represented agency.
        """
        return self.agency_df

    def get_name(self):
        """
        Returns the name of the agency represented by the object.

        :return: The name of the agency that the object represents.
        """
        return self.name
    
    def get_abbreviation(self):
        """
        Returns the most common abbreviation of the agency represented by the object.

        :return: The most common abbreviation of the agency represented by the object.
        """
        return self.abbreviation

    def get_quarter(self):
        """
        Returns the quarter that the object represents.

        :return: The quarter that the Agency object represents.
        """
        return self.current_quarter

    def get_year(self):
        """
        Returns the year that the object represents.

        :return: The year that the Agency object represents.
        """
        return self.current_year
