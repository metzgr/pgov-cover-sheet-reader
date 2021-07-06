import utility

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

    # UTILITY METHODS

    def get_goals(self):
        """
        Returns a list of the APGs that the agency has set.

        :return: A list of strings, each representing a unique APG of the agency.
        """
        return list(self.agency_df["Goal Name"].unique())

    def get_goal_status_df(self, goal_names=None, year=None, quarter=None):
        """
        Returns a DataFrame mapping each agency APG name to its status for the specified year and quarter.

        param goal_names: A list of the goal names to be represented in the returned DataFrame. Defaults to returning all goals within the represented agency.
        :param year: The year from which to retrieve goal status. Defaults to the year that the object represents, "all" returns the data from all years and quarters.
        :param quarter: The quarter from which to retrieve goal status. Defaults to the quarter that the object represents. "all" returns the data from all years and quarters. "previous" returns the data only from the previous quarter.
        :return: A DataFrame mapping each APG to its goal status across the specified year and quarters.
        """
        if not year:
            year = self.current_year

        if not quarter:
            quarter = self.current_quarter
        elif quarter == "previous":
            quarter, year = utility.get_previous_quarter_and_year(self.get_quarter(), self.get_year())

        conditional = pd.Series(data=[True for i in range(len(self.agency_df))], index=self.agency_df.index)     # defaults to all rows
        
        if not "all" in [year, quarter]:
            conditional = conditional & (self.agency_df["Fiscal Year"] == year) & (self.agency_df["Quarter"] == quarter)
        
        if goal_names:
            conditional = conditional & (self.agency_df["Goal Name"].isin(goal_names))

        return self.agency_df.loc[conditional, ["Goal Name", "Quarter", "Fiscal Year", "Status"]].reset_index(drop=True)

    def get_goal_status(self, goal_name, year=None, quarter=None):
        """
        Returns the goal status of the passed APG.

        :param goal_name: The name of the APG from which a status will be returned.
        :param year: The year from which to retrieve goal status. Defaults to the year that the object represents, "all" returns the data from all years and quarters.
        :param quarter: The quarter from which to retrieve goal status. Defaults to the quarter that the object represents, "all" returns the data from all years and quarters.
        """
        if not year:
            year = self.current_year
        if not quarter:
            quarter = self.current_quarter

        try:
            return self.agency_df.loc[(self.df["Goal Name"] == goal_name) & (self.agency_df["Fiscal Year"] == year) & (self.agency_df["Quarter"] == quarter), "Status"].iloc[0]
        except IndexError:  # if the passed goal name is not held within the agency
            return None
