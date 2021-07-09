"""
Guides the creation of visualizations for the summary report from the source data.
"""

import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pandas.api.types import CategoricalDtype

import utility
import df_creator

DEFAULT_DIRECTORY = "viz/"

# FIRST PAGE

sns.set_theme()

def create_goal_summary_small_multiples(agency, dir=DEFAULT_DIRECTORY, names=["small_multiples_previous", "small_multiples_current"]):
    """
    Creates small multiple graphics to summarize quarter-over-quarter summary goal status progress, saves them to the specified directory.

    :param agency: The agency from which goal summary small multiples will be created.
    :param dir: The directory to which the figures will be saved to. Default value is the directory stored in the DEFAULT_DIRECTORY constant.
    :param names: The file names that the figures will be saved to. The first item in the list is the name of the previous quarter's graph, and the second is for the current quarter's graph.
    """
    # Error handling
    if not isinstance(names, list) or len(names) != 2:
        raise Exception("A list of length two is required to be passed in the 'names' argument.")

    if not all([isinstance(name, str) for name in names]):
        raise Exception("All items in the 'names' argument must be stings")

    goal_stauts_count_df = df_creator.get_status_count_groupby_agency_year_quarter(agency.get_agency_df())

    # Create ordered hierarchy of statuses
    status_ordered = CategoricalDtype(
        ['Blocked', 'On Track', 'Ahead'], 
        ordered=True
    )

    # Seting plot's font
    font = {
        'family' : 'sans-serif',
        'size'   : 40
    }
    plt.rc('font', **font)

    previous_quarter, previous_year = utility.get_previous_quarter_and_year(agency.get_quarter(), agency.get_year())

    quarters = [previous_quarter, agency.get_quarter()]
    years = [previous_year, agency.get_year()]

    # Loops through each list in parallel
    for quarter, year, filename in zip(quarters, years, names):
        # Initializes DataFrame as slice of main DataFrame that relates to the agency, fiscal year and quarter being analyzed in this loop
        quarter_statuses_df = goal_stauts_count_df.loc[
            (goal_stauts_count_df["Agency Name"] == agency.get_name()) & 
            (goal_stauts_count_df["Fiscal Year"] == year) & 
            (goal_stauts_count_df["Quarter"] == quarter)
        ].reset_index(drop=True)
        
        for status in ['Ahead', 'Blocked', 'On track']:     # TODO: Replace this hard-coded list with a constant
            if not status in quarter_statuses_df["Status"].unique(): 
                new_row = pd.Series(quarter_statuses_df.iloc[0])
                new_row["Status"] = status
                new_row["Count"] = 0
                quarter_statuses_df = quarter_statuses_df.append(new_row).reset_index(drop=True)    # adds row indicating that a status had no occurrences in this window
                
        quarter_statuses_df["Status"] = quarter_statuses_df["Status"].astype(status_ordered)    # applies order to statuses column, used to display x-axis in correct order

        # Creates barplot
        sns.barplot(x=quarter_statuses_df["Status"], y=quarter_statuses_df["Count"])

        fig = plt.gcf()
        ax = plt.gca()

        # Editing the display of the plot
        plt.suptitle(f"{quarter} {year}")   # sets title of plot
        plt.xlabel("")  # removes x label
        ax.margins(y=0)
        plt.xticks(fontsize=24)
        plt.yticks(ticks=[i for i in range(len(agency.get_goals()) + 1)], fontsize=24)
        ax.set_ylabel(ax.yaxis.get_label().get_text(), fontdict=font)   # sets the size of the category label on the y axis
        
        # Exporting figure
        fig.set_size_inches(12, 8)
        fig.savefig(f"{dir}{filename}", bbox_inches='tight')
        plt.clf()  # clears plot
