
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ---------------------------- DocWriter Object --------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# The DocWriter objects allows a user to populate a word form with data.
# The process:
# 1. Zip a docx file and extract the document xml
# 2. Modify the document xml to fill in form inputs with data
# 3. Re-create the docx file by combining all of the original files and the 
# modified document xml

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
import shutil
import zipfile
import tempfile
from lxml import etree

# Local Imports
from src.globals import NS


# ------------------------------------------------------------------------------
# ---------------------------- Class Definition --------------------------------
# ------------------------------------------------------------------------------


# DocWriter class
class DocWriter:
    
    
    # Init func to create a zip file
    def __init__(self, docx_file):
        self.zipfile = zipfile.ZipFile(docx_file)


    # Get a formatted xml tree
    def get_xml(self):
        return etree.fromstring(self.zipfile.read("word/document.xml"))


    # Write the docx file
    def _write_and_close_docx(self, xml_content, output_filename):
        
        # Create a temp directory
        tmp_dir = tempfile.mkdtemp()

        # Expand the original docx zip.
        self.zipfile.extractall(tmp_dir)

        # Write the modified xml to word/document.xml
        with open(os.path.join(tmp_dir, 'word/document.xml'), 'wb') as f:
            xmlstr = etree.tostring(xml_content, pretty_print=True)
            f.write(xmlstr)

        # Zip it up as the new docx
        # Get a list of all the files in the original docx zipfile
        filenames = self.zipfile.namelist()
        # Now, create the new zip file and add all the filex into the archive
        zip_copy_filename = output_filename
        with zipfile.ZipFile(zip_copy_filename, "w") as docx:
            for filename in filenames:
                docx.write(os.path.join(tmp_dir, filename), filename)

        # Clean up the temp dir
        shutil.rmtree(tmp_dir)


    # Function to populate data
    def populate_template(self, replacements):
        # Get XML tree
        tree = self.get_xml()
        # Loop through elements in tree
        for elem in tree.iter():
            # If element is an input
            if elem.tag == NS + "sdt":
                # See if its alias is in replacements
                val = elem.find(NS + 'sdtPr').find(NS +'alias').attrib[NS + 'val']
                if val in replacements:
                    # If it is, loop through the input element
                    for x in elem.find(NS + 'sdtContent').iter():
                        # And replace the text in the 't' element
                        if x.tag == NS + "t":
                            x.text = replacements[val]
        return tree


    # Function to create an output file
    def create_output_file(self, outfilepath, replacements):
        # Populate the template with replacement data
        tree = self.populate_template(replacements)
        # Write the new file
        self._write_and_close_docx(tree, outfilepath)
        # Print Success message
        print(f'-- Success: output file created at {outfilepath}')
        return


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------- End Script -----------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
