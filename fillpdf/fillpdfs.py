import pdfrw
from pdf2image import convert_from_path # Needs conda install -c conda-forge poppler
from PIL import Image
from collections import OrderedDict
from PyPDF2 import PdfFileWriter, PdfFileReader

def _getFields(obj, tree=None, retval=None, fileobj=None):
    """
    Extracts field data if this PDF contains interactive form fields.
    The *tree* and *retval* parameters are for recursive use.
    Parameters
    ---------
    fileobj: PdfFileReader.Object
        A file object (usually a text file) to write
        a report to on all interactive form fields found.
    Returns
    ---------
    retval- dict, or ``None`` if form data could not be located.
        A dictionary where each key is a field name, and each
        value is a :class:`Field<PyPDF2.generic.Field>` object. By
        default, the mapping name is used for keys.
    """
    fieldAttributes = {'/FT': 'Field Type', '/Parent': 'Parent', '/T': 'Field Name', '/TU': 'Alternate Field Name',
                       '/TM': 'Mapping Name', '/Ff': 'Field Flags', '/V': 'Value', '/DV': 'Default Value'}
    if retval is None:
        retval = OrderedDict()
        catalog = obj.trailer["/Root"]
        # get the AcroForm tree
        if "/AcroForm" in catalog:
            tree = catalog["/AcroForm"]
        else:
            return None
    if tree is None:
        return retval

    obj._checkKids(tree, retval, fileobj)
    for attr in fieldAttributes:
        if attr in tree:
            # Tree is a field
            obj._buildField(tree, retval, fileobj, fieldAttributes)
            break

    if "/Fields" in tree:
        fields = tree["/Fields"]
        for f in fields:
            field = f.getObject()
            obj._buildField(field, retval, fileobj, fieldAttributes)

    return retval


def get_form_fields(input_pdf_path):
    """
    Retrieves the form fields from a pdf to then be stored as a dictionary and
    passed to the write_fillable_pdf() function. Uses PyPDF2.
    Parameters
    ---------
    input_pdf_path: str
        Path to the pdf you want the fields from.
    Returns
    ---------
    """
    input_pdf_path = PdfFileReader(open(input_pdf_path, 'rb'))
    fields = _getFields(input_pdf_path)
    return dict(OrderedDict((k, v.get('/V', '')) for k, v in fields.items()))


def flatten_pdf(input_pdf_path, output_pdf_path, as_images=False):
    """
    Flattens the pdf so each annotation becomes uneditable. This function provides
    two ways to do so, either with the pdfrw function annotation.update(pdfrw.PdfDict(Ff=1))
    or converting the pages to images then reinserting.
    Parameters
    ---------
    input_pdf_path: str
        Path to the pdf you want to flatten.
    output_pdf_path: str
        Path of the new pdf that is generated.
    as_images: bool
        Default is False meaning it will update each individual annotation and set
        it to False. True means it will convert to images and then reinsert into the
        pdf
    Returns
    ---------
    """
    if as_images == True:
        images = convert_from_path(input_pdf_path) 
        im1 = images[0]
        images.pop(0)

        pdf1_filename = output_pdf_path

        im1.save(pdf1_filename, "PDF" ,resolution=100.0, save_all=True, append_images=images)
    else:
        ANNOT_KEY = '/Annots'               # key for all annotations within a page

        template_pdf = pdfrw.PdfReader(input_pdf_path)
        for Page in template_pdf.pages:
            if Page[ANNOT_KEY]:
                for annotation in Page[ANNOT_KEY]:
                    annotation.update(pdfrw.PdfDict(Ff=1))
        template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
        

def convert_dict_values_to_string(dictionary):
    """
    Converts dictionary values to string including arrays and tuples.
    Parameters
    ---------
    dictionary: dict
        Any single level dictionary. Specifically made for the data_dict returned from
        the function get_form_fields() from the fillpdf library
    Returns
    ---------
    res: dict
        The resulting dictionary with only string values.
    """
    list_delim, tuple_delim = '-', '^'
  
    res = dict()
    for sub in dictionary:

        # checking data types
        if isinstance(dictionary[sub], list):
            res[sub] = list_delim.join([str(ele) for ele in dictionary[sub]])
        elif isinstance(dictionary[sub], tuple):
            res[sub] = tuple_delim.join(list([str(ele) for ele in dictionary[sub]]))
        else:
            res[sub] = str(dictionary[sub])
            
    return res    
    
    
def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict, flatten=False):
    """
    Writes the dictionary values to the pdf. Currently supports text and buttons.
    Does so by updating each individual annotation with the contents of the dat_dict.
    Parameters
    ---------
    input_pdf_path: str
        Path to the pdf you want to flatten.
    output_pdf_path: str
        Path of the new pdf that is generated.
    data_dict: dict
        The data_dict returned from the function get_form_fields()
    flatten: bool
        Default is False meaning it will stay editable. True means the annotations
        will be uneditable.
    Returns
    ---------
    """
    data_dict = convert_dict_values_to_string(data_dict)
    
    ANNOT_KEY = '/Annots'               # key for all annotations within a page
    ANNOT_FIELD_KEY = '/T'              # Name of field. i.e. given ID of field
    ANNOT_FORM_type = '/FT'             # Form type (e.g. text/button)
    ANNOT_FORM_button = '/Btn'          # ID for buttons, i.e. a checkbox
    ANNOT_FORM_text = '/Tx'             # ID for textbox
    SUBTYPE_KEY = '/Subtype'
    WIDGET_SUBTYPE_KEY = '/Widget'
    ANNOT_FIELD_PARENT_KEY = '/Parent'  # Parent key for older pdf versions
    ANNOT_FIELD_KIDS_KEY = '/Kids'      # Kids key for older pdf versions

    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for Page in template_pdf.pages:
        if Page[ANNOT_KEY]:
            for annotation in Page[ANNOT_KEY]:
                target = annotation if annotation[ANNOT_FIELD_KEY] else annotation[ANNOT_FIELD_PARENT_KEY]
                if target and annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    key = target[ANNOT_FIELD_KEY][1:-1] # Remove parentheses
                    if key in data_dict.keys():
                        print(target[ANNOT_FORM_type])
                        if target[ANNOT_FORM_type] == ANNOT_FORM_button:
                            # button field i.e. a checkbox
                            target.update( pdfrw.PdfDict( V=pdfrw.PdfName(data_dict[key]) , AS=pdfrw.PdfName(data_dict[key]) ))
                            if target[ANNOT_FIELD_KIDS_KEY]:
                                target[ANNOT_FIELD_KIDS_KEY][0].update( pdfrw.PdfDict( V=pdfrw.PdfName(data_dict[key]) , AS=pdfrw.PdfName(data_dict[key]) ))
                        elif target[ANNOT_FORM_type] == ANNOT_FORM_text:
                            # regular text field
                            target.update( pdfrw.PdfDict( V=data_dict[key], AP=data_dict[key]) )
                            if target[ANNOT_FIELD_KIDS_KEY]:
                                target[ANNOT_FIELD_KIDS_KEY][0].update( pdfrw.PdfDict( V=data_dict[key], AP=data_dict[key]) )
                if flatten == True:
                    annotation.update(pdfrw.PdfDict(Ff=1))
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)