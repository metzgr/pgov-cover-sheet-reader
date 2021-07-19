"""
Guides the creation of visualizations for the summary report from the source data.
"""

import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pandas.api.types import CategoricalDtype
import numpy as np
import os

from src.constants import CHALLENGES_LIST, STATUS_RANK_MAP
import src.utility as utility
import src.output.data.df_creator as df_creator

from src.constants import VIZ_DIRECTORY as DEFAULT_DIRECTORY

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
        ['Blocked', 'On track', 'Ahead'], 
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
            (goal_stauts_count_df["Agency Name"] == agency.get_abbreviation()) & 
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
        fig.set_size_inches(12, 8)   # saved image is larger, of higher quality
        __save_figure(fig, dir, filename)

def create_challenges_reported_in_quarter(agency, dir=DEFAULT_DIRECTORY, name="challenges_reported_bar_chart"):
    """
    Creates a graph representing the challenges reported in a quarter and saves it to a specified name and directory.

    :param agency: The Agency object from which a quarterly challenges reported plot will be created.
    :param dir: The directory to which the figure will be saved to.
    :param name: The file name that the figure will be saved to.
    """
    # Retrieve DataFrame, filter for only this quarter
    challenge_count_df = df_creator.get_challenge_count_by_quarter(agency.get_agency_df())
    challenge_count_df = challenge_count_df.loc[(challenge_count_df["Quarter"] == agency.get_quarter()) & (challenge_count_df["Fiscal Year"] == agency.get_year())].sort_values(by="Count", ascending=False)

    font = {
        'family' : 'sans-serif',
        'size'   : 24
    }

    plt.rc('font', **font)

    # Creates barplot
    sns.barplot(x="Challenge", y="Count", data=challenge_count_df, ci=None, palette=["grey" for i in range(len(challenge_count_df))])
    
    fig = plt.gcf()
    ax = plt.gca()

    # Editing the display of the plot
    plt.suptitle(f"Challenges Reported across SBA APGs in Q4 2020")
    plt.xlabel("")  # removes x label
    plt.xticks(rotation=45, ha="right", fontsize=24)
    ax.margins(y=0)
    plt.yticks(ticks=[i for i in range(len(agency.get_goals()) + 1)], fontsize=24)
    ax.set_ylabel(ax.yaxis.get_label().get_text(), fontdict=font)   # sets the size of the category label on the y axis

    # Exporting figure
    fig.set_size_inches(12, 8)   # saved image is larger, of higher quality
    __save_figure(fig, dir, name)

def create_challenges_area_chart(agency, dir=DEFAULT_DIRECTORY, name="challenges_area_chart"):
    """
    Creates an area chart showing the cumulative amount of challenges reported in each category.

    :param agency: The Agency object from which a challenges area chart will be created.
    :param dir: The directory to which the figure will be saved to.
    :param name: The file name that the figure will be saved to.
    """
    # Retrieve DataFrame, sort values in chronological order
    challenge_count_df = df_creator.get_challenge_count_by_quarter(agency.get_agency_df())
    challenge_count_df.sort_values(by=["Fiscal Year", "Quarter"])

    data = {}

    # Create data entry of cumulative sum for each challenge. Cumulative sum is in chronological order, dating from the furthest back quarter reported to the most recent
    for challenge in CHALLENGES_LIST:
        challenge_df_slice = challenge_count_df.loc[challenge_count_df["Challenge"] == challenge]   # a slice of the challenge df with only the current challenge
        if challenge_df_slice["Count"].sum() != 0:  # only include challenges that were identified by the challenge team
            cumsum = list(challenge_df_slice["Count"].cumsum())
            data[challenge] = cumsum
        
    # Create area plot from cumulative sum data
    pd.DataFrame(data).plot.area(stacked=False)

    fig = plt.gcf()
    ax = plt.gca()

    # Editing the display of the plot
    quarter_list = [f"{quarter}" for year in challenge_count_df["Fiscal Year"].unique() for quarter in challenge_count_df["Quarter"].unique()]  # a list of all quarters stored in DataFrame
    plt.xticks([i for i in range(len(quarter_list))], quarter_list, fontsize=24)
    plt.yticks(fontsize=24)
    ax.grid(False)
    plt.legend(prop={'size': 20})

    # Exporting figure
    fig.set_size_inches(12, 8)
    __save_figure(plt.gcf(), dir, name)

def create_goal_status_over_time(agency, apg_name, dir=DEFAULT_DIRECTORY, name="goal_status_over_time"):
    """
    Creates a plot displaying the goal status over time of the passed APG.

    :param agency: The Agency object from which the plot will be created.
    :param apg_name: The name of the APG that will be represented in the created plot.
    :param dir: The directory to which the figure will be saved to.
    :param name: The file name that the figure will be saved to.
    """
    apg_status_df = agency.get_agency_df()
    apg_status_df = apg_status_df.loc[apg_status_df["Goal Name"] == apg_name].sort_values(by=["Fiscal Year","Quarter"])     # sort in chronological order
    apg_status_df["Quarter/Year"] = apg_status_df["Quarter"] + " " + apg_status_df["Fiscal Year"].astype(str)

    font = {
        'family' : 'sans-serif',
        'size'   : 40
    }
    plt.rc('font', **font)

    fig, ax = plt.subplots()

    # Lines dividing goal statuses
    ax.axhline(0.5, color="white")
    ax.axhline(1.5, color="white")

    # Lines dividing fiscal years
    ax.axvline(3.5, color="white", linestyle="--", dashes=[6,9])
    ax.axvline(7.5, color="white", linestyle="--", dashes=[6,9])
    ax.axvline(11.5, color="white", linestyle="--", dashes=[6,9])

    status_ranked = pd.Series([STATUS_RANK_MAP[status] for status in list(apg_status_df["Status"])])    # List of numerical ranking of APG statuses in chronological order, needed to correctly order statuses on y-axis

    # Create plot
    plt.plot(apg_status_df["Quarter/Year"], status_ranked, marker="o", markersize=16)
    plt.suptitle("Goal Status Over Time")
    plt.xticks(rotation=90, fontsize=24)
    y_ticks  = [item[0] for item in sorted(STATUS_RANK_MAP.items(), key=lambda item: item[1])]  # orders keys based on their values in ascending order
    plt.yticks(np.arange(len(y_ticks)), y_ticks, fontsize=24)     # restore string status names, overwrite numerical ranks

    ax.margins(y=0.25)
    ax.grid(False)  # turns off the seaborn plot

    # Exporting figure
    fig.set_size_inches(12, 8)
    __save_figure(plt.gcf(), dir, name)

def __save_figure(fig, dir, name):
    """
    Saves the passed figure to the passed directory path and name.

    :param fig: The figure to be saved.
    :param dir: The directory to which the figure will be saved to.
    :param name: The file name that the figure will be saved to.
    """
    if not os.path.isdir(dir):
        os.makedirs(dir)

    fig.savefig(f"{dir}{name}", bbox_inches="tight")
    plt.close(fig)
