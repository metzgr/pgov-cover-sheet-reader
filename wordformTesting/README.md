# Word Form Data Extractor

## About

This program is used to extract data from Microsoft Word Forms and posts the data to an AirTable. This program converts .docx files into structured .xml files to identify and extract all of the form inputs. The resulting output is a JSON friendly 'key - value pair' structure, where the data related to a particular file is tagged with the file's name. Take a look at 'output.json' for a sneak peek at the output format. Within a particular files data, the keys are the word object's title property, and the value is the user input into the form. This data is then passed into post request to add the data to the specified AirTable.

This program has been tested with the following types of word form input types:

- Rich Text
- Plain text
- Check boxes
- Combo Boxes
- Drop down boxes
- Date pickers

\*Note: This program was left in development status. It is not production ready. The main outstanding items that need to developed:
1. Finalization of the word form
2. Development of schema to map word form fields to database fields and data validation
3. Development of logic to post to a database to following the structure defined in the schema
4. Should the source database change from AirTable, changes will be required
5. Decide and implement how to handle forms with errors

Developed by: Brian Sullivan || <bcsullivan@guidehouse.com>

## Usage:

### Project Set-Up (One Time)

#### Create a Virtual Environment (Optional, but encouraged)

To create and activate a new virtual environment, run the following commands in the root directory

- `$ python -m venv 'PATH'`
- `$ .\PATH\Scripts\Activate`

To confirm the new environment has been activated, you should see (PATH) at the beginning of your terminal window

#### Install dependencies

Install project dependenicies using:  
`$ pip install -r requirements.txt`

#### Define Environment Variables

To protect confidential API keys and Airtable environment variables, the '.env' file is not included in the git commit. Create a file in the root directory called '.env' and copy and paste the below, replacing the quoted text with the appropriate strings. You'll need to get this information from Airtable.

`AIRTABLE_TOKEN = 'AUTH_TOKEN'`  
`AIRTABLE_BASE_ID = 'BASE_ID'`  
`AIRTABLE_TABLE_MAPPING = 'TABLE'`  
`AIRTABLE_TABLE_DATADICT = 'TABLE'`

### Continued Use

1. Inspect the globals.py file. The 'DIRECTORY' variable should be the file path (folder) that contains the .docx files that you would like to extract data from.
2. After updating the 'DIRECTORY' variable, run `$ python main.py` in the main project directory.
3. Inspect the output in 'output.json'
4. If you would like to actually post the results to the AirTable, run `$ python main.py -p`

## Debugging

For debugging purposes, the function 'printXML' is available in 'functions.py'. This function takes a single word document as input and outputs an XML version of the document as 'output.xml'. To use, run:

- `$ python debug.py`

This program targets the 'std' tags in the XML tree and uses the 'alias' and 't' tags within to set the key-value pairs.

## Assumptions

The following assumptions were made throughtout the development of the logic included in this program:

1. All form inputs have a unique id
2. To nest fields in the resulting data structure, use "&' in the input ID to define the structure. For Example:
   - This list of ID's:
     `['Goal title', 'projects&1&title', 'projects&1&status', 'projects&2&title', 'projects&2&status']`
   - Would lead to this nested data structure
   ```
   {'Goal title': '',
   'projects':{
       '1': {
           'title':'',
           'status':''
       },
       '2':{
           'title':'',
           'status':''
       }
   }}
   ```
3. Each form has an input with the ID of 'Version', which is used to indentify the correct schema from the database.
4. The schema should contain all of the input IDs from the form.

## Document Tree

- **.env**: Store Environment variables, see above.
- **.gitignore**: Disable certain files from inclusion in git repos.
- **debug.py**: Output the xml version of a docx file.
- **main.py**: Run the main script
- **README.md**: This file
- **requirements.txt**: A list of all python packages needed to use this program
- **src/**: Folder with most of the code, inputs and outputs
  - **globals.py**: Definition of some global variables
  - **schema.py**: Example Schema document
  - **functions/**: Folder with functions
    - **create_prepopulated_form.py**: Testing function to add data to an empty form
    - **create_schema.py**: Function to create the schema from the databse
    - **data_extraction.py**: Functions to extract data from a word form
    - **data_validation.py**: Functions to validate extracted data
    - **write_data.py**: Simple functions to write data to airtable
  - **objects/**: Folder containing code for classes
    - **docWriter.py**: Doc writer class used to populate an empty word form
    - **testing/**: Testing input and output documents for pre populating a form
  - **input/**: Folder containing various input files
    - **apgCoverSheet_v1.0_template_WORKING.docx**: Current template for the word form.
    - **dir/**: Folder containing example docx files, filled with dummy data using the template
    - **archive/**: Folder containing old versions of the word form for documention purposes. Not in use.
  - **output/**: 
    - **output.json**: Where main.py outputs data
    - **output.xml**: Where debug.py outputs data

## Future Development Considerations

At the time of this documentation, the form was to be Microsoft Word-based, however there have been discussions to change to a PDF-based or even Excel-based form. Although not exhaustive, some initial thoughts related to how this may be done (Subject to any changing requirements):

### Steps to convert to PDF based form

1. Develop PDF form following ID naming convention above for nesting, as necessary
2. Modify function 'extract_data' in src/functions/data_extraction.py'

   - Based on previous experience, I would recommend using the 'PyPDF2' package `pip install PyPDF2`: [PyPDF2 PyPi](https://pypi.org/project/PyPDF2/)
   - Sample code to get started

     ```
     import pypdf2

     def extract_data(full_file_path):
         dict = {}
         object= open(full_file_path,'rb')
         # Read the file
         reader = PyPDF2.PdfFileReader(object)
         # Get all contents in the file as a dictionary using the pdf form feilds
         form = reader.getFields()
         # Pull out the values for each of the fields if there is one
         for key in form:
             try:
                 dict[key] = form[key]['/V']
             except:
                 dict[key] = ''
         # Close the pdf and return dict
         object.close()
         return dict

     data = {}
     path = 'file_path_to_input_pdfs'

     # Loop through the files
     for file in os.listdir(path):
         # if its a pdf, pass it to the function
         if file.lower.endswith('.pdf'):
            data[file] = extract_data(path + file)
     ```

3. the function 'checkbox_convert' in src/functions/data_extraction.py may also need to be modified to correctly capture checkbox inputs.

### Considerations for Excel-based forms:

- There are a lot of potential benefits surrounding the development of a form in Microsoft Excel, such as:
  - More robust data validation controls
  - Dynamic dropdown menus
  - Ability to provide the user with a dashboard report that immediately summarizes their data
- Given the nature of Excel, I would recommend careful consideration on what types of actions will be allowable to the end user to ensure the format of the form and thus ability to extract the neccessary data elements.
- The most 'stable' way to develop the form would be to use 'UserForms' and macros (VBA code) to collect the data and lock the entire spreadsheet for changes
  - The user could only interact with the 'UserForm(s)' for data entry
  - You could programitically display user data in a user-friendly format, AND populate a traditional table with the collected data.
  - Significanly less likelihood of data errors (assuming robust requirements)
  - Can define the data model in the backend of the excel workbook and easily collect that data with python
  - The development of a form in this manner, will require a higher LOE and a skillset familiar with VBA
