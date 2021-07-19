# Performance.gov Cover Sheet Project

## Introduction 

This project is an exploration into the potential of automating the collection and analysis of performance reporting information for [Agency Priority Goals (APGs)](https://trumpadministration.archives.performance.gov/about/APG_about.html#:~:text=Agency%20Priority%20Goals%20(APGs)%20are,drive%20significant%20progress%20and%20change.). The dataset is derived from a "cover sheet", which is a new initiative being explored for collecting performance reporting data from CFO Act agencies that enables more candidness about goal progress and, therefore, has potential for better business intelligence. This project includes both the code needed to collect data from an input of cover sheet files and the implementation of generating a piece of business intelligence based on the collected information. 

The team tasked with developing [Performance.gov](https://www.performance.gov/) within the [GSA's Office of Shared Solutions and Performance Improvement (OSSPI)](https://www.gsa.gov/governmentwide-initiatives/shared-solutions-and-performance-improvement) heads this project and its development.

## Installation

To install this project for local development, follow the steps below:

1. Install [Python](https://www.python.org/downloads/).
2. [Clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository#cloning-a-repository).
3. Open a terminal and change your current working directory to where you cloned the project.
4. Run the following command to install the project's required Python packages:
```
pip install -r requirements.txt
```

## Contributing 

All are welcome to contribute to this project. If you wish to propose a change, please [open a pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) for the developers to consider. Please note that at this time, the dataset used to drive this project is for internal use only and is not available to the public.

## No-code editing

This project is designed such that the output file can be modified without touching the code.

### Changing the layout of the output .docx files

To edit the layout of the output .docx files (e.g., to change formatting or text alignment), access the template files under the directory [src/resources/templates](https://github.com/jasondamico/pgov-cover-sheet-reader/tree/jasondamico/update-readme/src/resources/templates). These files may be edited just as any other docx file would be. Once you are satisfied with your edits, please [open a pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) with your updated files for them to be merged into the repository.

**NOTE: Please do not remove or change the dimensions of any of the placeholder images.** It is acceptable to scale the images to rearrange text, but changing the width-to-height ratio compromises the display. If you have a proposal for a new graphic to be used or spot an issue with one of the existing images pulled into the document, please [create an issue in this repository](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue) to notify the developers.
