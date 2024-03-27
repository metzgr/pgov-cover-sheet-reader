
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ---------------------- Data Extraction Functions -----------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Functions included here convert word files into xml and extract data.

# Developed by Brian Sullivan || bcsullivan@guidehouse.com

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# ------------------------- Set-up / Package Imports ---------------------------
# ------------------------------------------------------------------------------


# Standard Library Imports
import os
import zipfile
import xml.etree.ElementTree as ET

# Local Imports
from src.globals import NS
from src.functions.data_validation import *
from src.functions.create_schema import create_schema


# ------------------------------------------------------------------------------
# -------------------------- Function Definition -------------------------------
# ------------------------------------------------------------------------------


# main caller function to loop through the files and extract data
def get_data(dir):
    data = {}
    for file in os.listdir(dir):
        # If it is a docx file
        if file.endswith("docx"):
            # Open as XML and Extract the data add it to the dictionary
            data[file] = extract_data(dir + file)

    # Create a set of all of the versions that are in data
    versions = set([data[form]['Version'] for form in data])

    # create the schema
    schema = create_schema(versions)

    # Currently, the schema in Airtable doesn't align with the latest template
    # As such this line is commented out
    # Validate the data that was entered into the forms
    # data = process_data(data, schema)
        
    return data


# extract the desired data from an XML Tree
def extract_data(wordDoc):
    # Get structured XML tree
    tree = get_xml(wordDoc)
    # Initiate a dict
    data = {}
    # Loop through the elements in the tree
    for elem in tree.iter():
        # If the element is an input
        if elem.tag == NS + "sdt":
            # Reset key and value
            key = ''
            value = ''
            # Loop through the sub elements
            for x in elem.iter():
                # Get the 'alias' and set it to key
                if x.tag == NS + "alias":
                    key = x.attrib[NS + "val"]
                # If 'alias' doesn't exist get the id
                elif x.tag == NS + 'id' and key == "":
                    key = x.attrib[NS + 'val']
                # Get the text from the 't' element
                if x.tag == NS + "t":
                    # There could be multiple 't' elements per input
                    value = value + checkbox_convert(x.text)
                # Update data with the new key value pair
                data[key] = value                    
    # process the output dict so it is nested properly
    data = create_nested_dict(data)

    return data


# Convert the word doc into a structured XML Tree
def get_xml(wordDoc):
    return ET.fromstring(zipfile.ZipFile(wordDoc).read("word/document.xml"))


# Convert word doc into xml string
def get_string_xml(wordDoc):
    return zipfile.ZipFile(wordDoc).read("word/document.xml")


# Helper function to convert encoded values in a checkbox
def checkbox_convert(value):
    vals = {"\u2610": "", "\u2612": "X"}
    if value in vals:
        value = vals[value]
    return value


# Processes data for validation and prep for post
def process_data(data, schema):
    for form in data:
        # Init an errors dict within data
        data[form]['Errors'] = {}

        # Look for a schema with the version that is on the form
        try:
            schema = {feild['wordFormColumn']: feild for feild in schema[data[form]['Version']]}
        except IndexError:
            return f'Error: Version {form["Version"]} does not exist in schema.'

        # For each feild, validate the data according to the rules in schema
        for feild in data[form]:
            if feild != 'Errors':
                data[form] = data_type(feild, schema[feild], data[form])
                data[form] = data_values(feild, schema[feild], data[form])
                data[form] = data_required(feild, schema[feild], data[form])

        # Rename the feilds based on schema
        data[form] = {schema[k].get('airTableColumnName', k) if k !=
                      'Errors' else k: v for k, v in data.items()}

    return data


# Create a nested dictionary
def create_nested_dict(flat_dict):
    nested_dict = {}
    # Loop through input dict
    for key, value in flat_dict.items():
        # Look for '&' in the key
        if '&' in key:
            # If exist, split the key on '&'
            keys = key.split('&')
            current_dict = nested_dict
            # Loop through the new list of keys
            for k in keys[:-1]:
                # Create a key with an empty dict
                if k not in current_dict:
                    current_dict[k] = {}
                current_dict = current_dict[k]
            # set the value
            current_dict[keys[-1]] = value
        else:
            # Set the value
            nested_dict[key] = value
    return nested_dict


# Write the xml of a docx to a file for inspection
def print_xml(wordDoc):
    ET.ElementTree(get_xml(wordDoc)).write("./src/output/output.xml")
    return


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------- End Script -----------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
