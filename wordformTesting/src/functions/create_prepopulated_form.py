
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ----------------------- Create a Prepopulated Form ---------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# This testing script serves as a POC for populating an empty form template
# with data 

# Developed by Brian Sullivan || bcsullivan@guidehouse.com

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# ------------------------- Set-up / Package Imports ---------------------------
# ------------------------------------------------------------------------------

# Local Imports
from objects.docWriter import DocWriter


# ------------------------------------------------------------------------------
# -------------------------- Function Definition -------------------------------
# ------------------------------------------------------------------------------


# Ability to create prepopulated forms
# This needs to be completed to loop through files and use data instead of replacements
def create_pre_populated_forms(output_file, replacements, template_file):
    
    # Empty form to be populated
    template_file = r'src\objects\testing\input\formB_quarterlySubmission_coverSheet_BCS.docx'
    
    # Where you want to output the populated form
    output_file = r'./src/objects/testing/output/testing.docx'

    # Key value pair of replacements. Keys are word form ID's
    # In practice this would a function input and contain collected data
    replacements = {
        'FY': '24',
        'Quarter': '1',
        'Agency': 'DOC',
        'Goal': 'Testing Goal',
        'Type': 'Annual',
        'Key Result 1': 'Testing Key Result'
    }

    # Initiate the template
    template = DocWriter(template_file)

    # Create the outout file
    template.create_output_file(output_file, replacements)
        
    return


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------ End Script ------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
