"""
Holds definition of Agency class and its associated methods.
"""

from src.constants import OUTCOMES_LIST, THEMATIC_MAPPING_DF, CHALLENGES_LIST, THEMES_LIST, CAP_GOALS_LIST, AGENCY_NAME_TO_ABBREVIATION, AGENCY_ABBREVIATION_TO_NAME
import src.utility as utility

import pandas as pd

class Agency():
    """
    Represents a CFO Act agency at a given quarter and fiscal year and contains data related to the performance of its APGs over quarters and fiscal years.
    """
    
    def __init__(self, df, name, current_quarter, current_year):
        """
        Constructor method; creates a Agency object initialized with the basic attributes of a agency being reported on.

        :param df: The central DataFrame that information will be pulled from - includes the data for all agencies, not just the agency that the object represents.
        :param name: The name of the agency that this object represents. Takes either an abbreviation or a full agency name.
        :param current_quarter: The quarter that this agency will be reporting on.
        :param current_year: The year that this agency will be reporting on. 
        """
        if name in AGENCY_ABBREVIATION_TO_NAME.keys():  # if name is an abbreviation:
            self.name = AGENCY_ABBREVIATION_TO_NAME[name]
            self.abbreviation = name
        elif name in AGENCY_NAME_TO_ABBREVIATION.keys():    # if name is a full agency name
            self.name = name
            self.abbreviation = AGENCY_NAME_TO_ABBREVIATION[name]
        else:
            raise ValueError(f"\"{name}\" is neither a valid agency abbreviation nor a full agency name of one of the 24 CFO act agencies.")

        self.df = df
        self.agency_df = self.get_df().loc[self.get_df()["Agency Name"] == self.get_abbreviation()]  # a DataFrame only containing data relevant to the agency that the object represents
        self.apgs = list(self.get_agency_df()["Goal Name"].unique())
        self.current_quarter = current_quarter 
        self.current_year = current_year

    # GETTER METHODS

    def get_df(self):
        """
        Returns the central DataFrame used to store the data surrounding agencies and their goal statuses. Contains data of all CFO Act agencies, not just the agency that the object represents.

        :return: A DataFrame that stores the data surrounding agencies and their goal statuses.
        """
        return self.df

    def get_agency_df(self):
        """
        Returns the DataFrame representing the agency and its APGs. Only contains data from the CFO Act agency that the object represents.

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

    def get_goals(self):
        """
        Returns a list of the APGs that the agency has set.

        :return: A list of strings, each representing a unique APG of the agency.
        """
        return self.apgs

    # UTILITY METHODS

    def get_goal_status_df(self, goal_names=None, year=None, quarter=None):
        """
        Returns a DataFrame mapping each agency APG name to its status for the specified year and quarter.

        param goal_names: A list of the goal names to be represented in the returned DataFrame. Defaults to returning all goals within the represented agency.
        :param year: The year from which to retrieve goal status. Defaults to the year that the object represents, "all" returns the data from all years and quarters.
        :param quarter: The quarter from which to retrieve goal status. Defaults to the quarter that the object represents. "all" returns the data from all years and quarters. "previous" returns the data only from the previous quarter.
        :return: A DataFrame mapping each APG to its goal status across the specified year and quarters.
        """
        year, quarter = self.__handle_year_quarter_input(year, quarter)

        conditional = pd.Series(data=[True for i in range(len(self.get_agency_df()))], index=self.get_agency_df().index)     # defaults to all rows
        
        if not "all" in [year, quarter]:
            conditional = conditional & (self.get_agency_df()["Fiscal Year"] == year) & (self.get_agency_df()["Quarter"] == quarter)
        
        if goal_names:
            conditional = conditional & (self.get_agency_df()["Goal Name"].isin(goal_names))

        return self.get_agency_df().loc[conditional, ["Goal Name", "Quarter", "Fiscal Year", "Status"]].reset_index(drop=True)

    def get_goal_status(self, goal_name, year=None, quarter=None):
        """
        Returns the goal status of the passed APG.

        :param goal_name: The name of the APG from which a status will be returned.
        :param year: The year from which to retrieve goal status. Defaults to the year that the object represents.
        :param quarter: The quarter from which to retrieve goal status. Defaults to the quarter that the object represents. "previous" returns the data only from the previous quarter.
        """
        try:
            return self.get_apg_row(goal_name, year=year, quarter=quarter)["Status"].iloc[0]
        except IndexError:  # if the passed goal name is not held within the agency
            return None

    def get_challenges(self, goal_name):
        """
        Returns a list of the challenges reported for the passed goal name.

        :param goal_name: The name of the APG from which the challenges reported will be returned.
        :return: A list of the challenges reported by the passed goal team.
        """
        return self.get_apg_row(goal_name)[CHALLENGES_LIST].columns[(self.get_apg_row(goal_name)[CHALLENGES_LIST] == 1).all()].tolist()     # list of challenge columns that are in the affirmative

    def get_themes(self, goal_name):
        """
        Returns a list of the themes connected to the passed goal name.

        :param goal_name: The name of the APG from which the related themes will be returned.
        :return: A list of the themes connected to the the passed goal.
        """
        return self.__get_affirmative_thematic_columns(goal_name, THEMES_LIST)

    def get_cap_goals(self, goal_name):
        """
        Returns a list of the CAP goals connected to the passed goal name.

        :param goal_name: The name of the APG from which the related CAP goals will be returned.
        :return: A list of the CAP goals connected to the the passed goal.
        """
        return self.__get_affirmative_thematic_columns(goal_name, CAP_GOALS_LIST)

    def get_outcomes(self, goal_name):
        """
        Returns a list of the outcomes connected to the passed goal name.

        :param goal_name: The name of the APG from which the related outcomes will be returned.
        :return: A list of the outcomes connected to the the passed goal.
        """
        return self.__get_affirmative_thematic_columns(goal_name, OUTCOMES_LIST)

    def get_apg_row(self, goal_name, year=None, quarter=None):
        """
        Returns a single row of a DataFrame containing the data retrieved for the passed goal for the current quarter.

        :param goal_name: The name of the APG from which the challenges reported will be returned.
        :param year: The year from which to retrieve goal status. Defaults to the year that the object represents.
        :param quarter: The quarter from which to retrieve goal status. Defaults to the quarter that the object represents.
        :return: A single row of a DataFrame containing the data retrieved for the passed goal for the current quarter.
        """
        year, quarter = self.__handle_year_quarter_input(year, quarter)

        return self.get_agency_df().loc[(self.get_agency_df()["Quarter"] == quarter) & (self.get_agency_df()["Fiscal Year"] == year) & (self.get_agency_df()["Goal Name"] == goal_name)]

    def get_common_apgs_theme_challenge(self, theme, challenge):
        """
        Given a passed theme and challenge, returns a DataFrame with each row being a unique instance of an APG team with the same theme and challenge.

        :param theme: The theme for which common APG teams will be retrieved.
        :param challenge: The challenge for which common APG teams will be revealed.
        :return: A DataFrame where each row is a unique instance of an APG team within the passed theme that is addressing the passed challenge in the current quarter.
        """
        common_theme_apgs = THEMATIC_MAPPING_DF.loc[(THEMATIC_MAPPING_DF[theme] == 1) & (THEMATIC_MAPPING_DF["Agency Name"] != self.get_name()), "Goal Name"].tolist()

        common_agencies_df = self.get_df().loc[(self.get_df()["Quarter"] == self.get_quarter()) & (self.get_df()["Fiscal Year"] == self.get_year())]    # retrieves slice of DataFrame for current year and quarter
        common_agencies_df = common_agencies_df.loc[(common_agencies_df["Goal Name"].isin(common_theme_apgs)) & (common_agencies_df[challenge] == 1)]  # filters DataFrame for only agencies with common themes, challenges

        return common_agencies_df

    def __get_affirmative_thematic_columns(self, goal_name, column_list):
        """
        For the passed goal, returns a list of the names of the columns in the affirmative from the list of columns passed that are included in the thematic mapping DataFrame.

        :param goal_name: The name of the APG for which a list of columns in the affirmative will be returned.
        :param column_list: A list of column names that are included in the thematic mapping DataFrame. Most commonly used as a group of related columns such as CAP goals, outcomes or themes.
        :return: A list of the names of the columns in the affirmative among the passed list.
        """
        thematic_mapping_row = THEMATIC_MAPPING_DF.loc[THEMATIC_MAPPING_DF["Goal Name"] == goal_name]

        return thematic_mapping_row[column_list].columns[(thematic_mapping_row[column_list] == 1).all()].tolist()

    def __handle_year_quarter_input(self, year, quarter):
        """
        Handles input values of year and quarter and returns either the raw values or machine-readable interpretations of input.

        :param year: The year from which to retrieve goal status. Defaults to the year that the object represents.
        :param quarter: The quarter from which to retrieve goal status. Defaults to the quarter that the object represents. "previous" returns the data only from the previous quarter.
        :return: A formatted year followed by a formatted quarter.
        """
        if not year:    # assigns current year if no year is specified
            year = self.get_year()
        if not quarter:     # assigns current quarter if no quarter is specified
            quarter = self.get_quarter()
        elif quarter == "previous":     # if quarter is "previous", then the previous year and quarter combination is assigned
            quarter, year = utility.get_previous_quarter_and_year(self.get_quarter(), self.get_year())

        return year, quarter
