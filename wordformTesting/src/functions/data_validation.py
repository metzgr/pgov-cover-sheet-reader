
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ---------------------- Data Validation Functions -----------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Functions included here validate data that was extracted.

# For the data validation process to work correctly, the database schema must 
# be updated in parallel to changes with the word form.

# Developed by Brian Sullivan || bcsullivan@guidehouse.com

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# -------------------------- Function Definition -------------------------------
# ------------------------------------------------------------------------------


# Function to ensure the data type matches what schema dictates
def data_type(feild, schema, data):
    # Get the required datatype from schema
    data_type = schema['dataType']
    # Is datatype int?
    if data_type == 'integer':
        # Try to convert the form input to an int
        try:
            data[feild] = int(data[feild])
        # If error, add to the error dict in data
        except ValueError:
            error_msg = error_handle(feild, data, data_type)
            data = add_error(data, feild, error_msg)
            return data
    if data_type == 'date':  # this needs to be built out
        data[feild] = data[feild]
    return data


# Check if form data is in the list of accepted values for each feild
def data_values(feild, schema, data):
    if type(schema['values']) == list:
        if not data[feild] in schema['values']:
            error_msg = f"ValueError: '{data[feild]}' is not an accepted option in schema for feild {feild}"
            data = add_error(data, feild, error_msg)
    return data


# Check if the feild is required and filled out?
def data_required(feild, schema, data):

    if schema['required'] and data[feild] == "":
        error_msg = f'RequiredError: Required feild missing: {feild}'
        data = add_error(data, feild, error_msg)
    return data


# Helper function to create invalid data type error messages
def error_handle(feild, data, dataType):
    return f'TypeError: Feild {feild}({data[feild]}) not of type {dataType}'


# Append error to list of errors for field
def add_error(data, feild, error):
    if feild in data['Errors']:
        data['Errors'][feild].append(error)
    else:
        data['Errors'][feild] = [error]
    return data

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------ End Script ------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
