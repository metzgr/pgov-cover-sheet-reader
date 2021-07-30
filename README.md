# Performance.gov Cover Sheet Project

## Introduction 

This project is an exploration into the potential of automating the collection and analysis of performance reporting information for [Agency Priority Goals (APGs)](https://trumpadministration.archives.performance.gov/about/APG_about.html#:~:text=Agency%20Priority%20Goals%20(APGs)%20are,drive%20significant%20progress%20and%20change.). The dataset is derived from a "cover sheet", which is a new initiative being explored for collecting performance reporting data from CFO Act agencies that enables more candidness about goal progress and, therefore, has potential for better business intelligence. This project includes both the code needed to collect data from an input of cover sheet files and the implementation of generating a piece of business intelligence based on the collected information. 

The team tasked with developing [Performance.gov](https://www.performance.gov/) within the [GSA's Office of Shared Solutions and Performance Improvement (OSSPI)](https://www.gsa.gov/governmentwide-initiatives/shared-solutions-and-performance-improvement) heads this project and its development.

## Installation

To install this project for local development, follow the steps below:

1. Install [Python](https://www.python.org/downloads/).
2. Install Git ([GitHub desktop](https://desktop.github.com/) recommended, but Git can also be [used via the command line](https://docs.github.com/en/get-started/quickstart/set-up-git))
3. [Clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository#cloning-a-repository).
4. Open a terminal and change your current working directory to where you cloned the project.
5. Run the following command to install the project's required Python packages:
```
pip install -r requirements.txt
```

## Contributing 

All are welcome to contribute to this project. If you wish to propose a change, please [open a pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) for the developers to consider. Please note that at this time, the dataset used to drive this project is for internal use only and is not available to the public.

## No-code editing

This project is designed such that the output file can be modified without touching the code. After changing any of the no-code files associated with this project (e.g., the Word template documents), follow the steps below to create a test output document:

1. Open the terminal.
2. Change directories to the location of the project folder.
3. Enter and run the following prompt:
```
python testing.py
```
4. In your file explorer, navigate to the folder `src/resources/templates` and find the file `SBA_output.docx`, which is the sample output file that was created by the test run.

The project output can be changed without touching the code in the following ways:

#### Changing the layout of the output .docx files

To edit the layout of the output .docx files (e.g., to change formatting or text alignment), access the template files under the directory [src/resources/templates](https://github.com/jasondamico/pgov-cover-sheet-reader/tree/jasondamico/update-readme/src/resources/templates). These files may be edited just as any other docx file would be. Once you are satisfied with your edits, please [open a pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) with your updated files for them to be merged into the repository. **NOTE: Please do not remove or change the dimensions of any of the placeholder images.** It is acceptable to scale the images to rearrange text, but changing the width-to-height ratio compromises the display. If you have a proposal for a new graphic to be used or spot an issue with one of the existing images pulled into the document, please [create an issue in this repository](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue) to notify the developers.

#### Editing the text blocks that populate the summary report

Throughout the summary report template documents, there are placeholders that are replaced by text blocks that are dynamically populated with information specific to the report. The templates for these text blocks are all pulled from a spreadsheet, `text_block_templates.xlsx`, which can be found in the directory [src/resources/templates](https://github.com/jasondamico/pgov-cover-sheet-reader/tree/jasondamico/update-readme/src/resources/templates). Each column of the spreadsheet has a specific purpose:

- `Template Document`: the name of the template document where this text template will be generated
- `Variable Name`: The variable in the template report which will be filled with the text block. **Please do not change this field**, but instead use it as a reference.
- `Context`: A brief explanation about what the text block is and what purpose it serves.
- `Sentence Template Neutral`: The default sentence that will populate the template document (required).
- `Sentence Template Plural`: The sentence that will populate the template document in the case when there is a plural form of whatever the sentence is describing (if applicable). 
- `Sentence Template Progressing`: The sentence that will be rendered when the phenomenon being described is improving/trending positively (if applicable). 	
- `Sentence Template Regressing`: The sentence that will be rendered when the phenomenon being described is regressing/trending negatively (if applicable). 	
- `Currently in template`: A field representing whether or not the text field is currently included in one of the template documents.

Please edit the text fields in the spreadsheet as you see fit to reword the generated text blocks. Please note that bolding and italicizing in the text fields can be done by Markdown conventions:

- To **bold** a string of characters, place **\*\*double asterisks\*\*** around them.
- To *italicize* a string of characters, place *\*single asterisks\** around them.
