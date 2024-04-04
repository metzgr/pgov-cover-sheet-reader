
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------ Word Form Data Extraction ---------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# This script defines the schema based on data pulled from AirTable.
# Both the Mapping and Data dictionary AirTable's are used.

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

# Third-Party Imports
from pyairtable import Api


# ------------------------------------------------------------------------------
# -------------------------- Function Definition -------------------------------
# ------------------------------------------------------------------------------

# Function to get schema from Airtable
# This may need to be modified if the data model changes
def create_schema(versions):
    
    # Define the Airtable API
    api = Api(os.getenv("AIRTABLE_TOKEN"))

    # Define the mapping table
    mapping = api.table(base_id = os.getenv("AIRTABLE_BASE_ID"),
                        table_name = os.getenv("AIRTABLE_TABLE_MAPPING")).all()

    # Get additional information from the data dictionary
    datadict = api.table(base_id = os.getenv("AIRTABLE_BASE_ID"),
                        table_name = os.getenv("AIRTABLE_TABLE_DATADICT")).all()
    
    # Restructure the data dictionary
    datadict = {x['id']: x for x in datadict}
    
    # Initiate the SCHEMA dict
    schema = {}

    for version in versions:
        # Configure the schema based on the mapping table
        schema[version] = [x['fields'] for x in mapping if x['fields']['form_version'] == version]

        # Loop through the feilds in the schema 
        for field in schema[version]:
            
            # Add relevent feilds from data dict
            field.update(get_fields(field['associated_field'][0]), datadict)
            
            # Remove unwanted fields
            field.pop('form_name', None)
            field.pop('form_version', None)
            field.pop('associated_feild', None)
            # Convert allowable values from string to list
            if 'values' in field:
                field['values'] = field['values'].split(", ")
    
    return schema


# Function to add feilds from the data dict to the schema
def get_fields(id, datadict):
    # List of needed feilds
    keyList = ['is_optional', 'data_type', 'associated_table', 'field_name']

    # Get the associated data from the data dictionary
    vals = datadict.get(id)['fields']

    # Return just the fields in the key list
    vals = {k: v for k, v in vals.items() if k in keyList}
    return vals


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------ End Script ------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
