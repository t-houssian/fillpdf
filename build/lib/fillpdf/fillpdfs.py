import pdfrw
from pdf2image import convert_from_path # Needs conda install -c conda-forge poppler
from PIL import Image
from collections import OrderedDict
from PyPDF2 import PdfFileWriter, PdfFileReader

def _getFields(obj, tree=None, retval=None, fileobj=None):
    """
    Extracts field data if this PDF contains interactive form fields.
    The *tree* and *retval* parameters are for recursive use.

    :param fileobj: A file object (usually a text file) to write
        a report to on all interactive form fields found.
    :return: A dictionary where each key is a field name, and each
        value is a :class:`Field<PyPDF2.generic.Field>` object. By
        default, the mapping name is used for keys.
    :rtype: dict, or ``None`` if form data could not be located.
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
    input_pdf_path = PdfFileReader(open(input_pdf_path, 'rb'))
    fields = _getFields(input_pdf_path)
    return dict(OrderedDict((k, v.get('/V', '')) for k, v in fields.items()))


def flatten_pdf(input_pdf_path, output_pdf_path):
    images = convert_from_path(input_pdf_path) 
    im1 = images[0]
    images.pop(0)
    
    pdf1_filename = output_pdf_path

    im1.save(pdf1_filename, "PDF" ,resolution=100.0, save_all=True, append_images=images)
    
    
def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):

    ANNOT_KEY = '/Annots'           # key for all annotations within a page
    ANNOT_FIELD_KEY = '/T'          # Name of field. i.e. given ID of field
    ANNOT_FORM_type = '/FT'         # Form type (e.g. text/button)
    ANNOT_FORM_button = '/Btn'      # ID for buttons, i.e. a checkbox
    ANNOT_FORM_text = '/Tx'         # ID for textbox
    SUBTYPE_KEY = '/Subtype'
    WIDGET_SUBTYPE_KEY = '/Widget'

    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for Page in template_pdf.pages:
        if Page[ANNOT_KEY]:
            for annotation in Page[ANNOT_KEY]:
                if annotation[ANNOT_FIELD_KEY] and annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY :
                    key = annotation[ANNOT_FIELD_KEY][1:-1] # Remove parentheses
                    if key in data_dict.keys():
                        if annotation[ANNOT_FORM_type] == ANNOT_FORM_button:
                            # button field i.e. a checkbox
                            annotation.update( pdfrw.PdfDict( V=pdfrw.PdfName(data_dict[key]) , AS=pdfrw.PdfName(data_dict[key]) ))
                        elif annotation[ANNOT_FORM_type] == ANNOT_FORM_text:
                            # regular text field
                            annotation.update( pdfrw.PdfDict( V=data_dict[key], AP=data_dict[key]) )
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)