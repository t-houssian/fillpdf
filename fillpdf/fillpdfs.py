import fitz
import math
import pdfrw
from pdf2image import convert_from_path # Needs conda install -c conda-forge poppler
from PIL import Image
from collections import OrderedDict

ANNOT_KEY = '/Annots'               # key for all annotations within a page
ANNOT_FIELD_KEY = '/T'              # Name of field. i.e. given ID of field
ANNOT_FORM_type = '/FT'             # Form type (e.g. text/button)
ANNOT_FORM_button = '/Btn'          # ID for buttons, i.e. a checkbox
ANNOT_FORM_text = '/Tx'             # ID for textbox
ANNOT_FORM_options = '/Opt'
ANNOT_FORM_combo = '/Ch'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'
ANNOT_FIELD_PARENT_KEY = '/Parent'  # Parent key for older pdf versions
ANNOT_FIELD_KIDS_KEY = '/Kids'      # Kids key for older pdf versions
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'

def get_form_fields(input_pdf_path, sort=False, page_number=None):
    """
    Retrieves the form fields from a pdf to then be stored as a dictionary and
    passed to the write_fillable_pdf() function. Uses pdfrw.
    Parameters
    ---------
    input_pdf_path: str
        Path to the pdf you want the fields from.
    Returns
    ---------
    A dictionary of form fields and their filled values.
    """
    data_dict = {}

    pdf = pdfrw.PdfReader(input_pdf_path)
    count = 1
    if page_number is not None:
        if type(page_number) == int:
            if page_number > 0:
                if page_number <= len(pdf.pages):
                    pass
                else:
                    raise ValueError(f"page_number must be inbetween 1 & {len(pdf.pages)}")
            else:
                raise ValueError(f"page_number must be inbetween 1 & {len(pdf.pages)}")
        else:
            raise ValueError(f"page_number must be an int")
    for page in pdf.pages:
        if page_number is not None:
            if count != page_number:
                count += 1
                continue
            else:
                print(f"Values From Page {page_number}")
        annotations = page[ANNOT_KEY]
        if annotations:
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        key = annotation[ANNOT_FIELD_KEY][1:-1]
                        data_dict[key] = ''
                        if annotation[ANNOT_VAL_KEY]:
                            value = annotation[ANNOT_VAL_KEY]
                            data_dict[key] = annotation[ANNOT_VAL_KEY]
                            try:
                                if type(annotation[ANNOT_VAL_KEY]) == pdfrw.objects.pdfstring.PdfString:
                                    data_dict[key] = pdfrw.objects.PdfString.decode(annotation[ANNOT_VAL_KEY])
                                elif type(annotation[ANNOT_VAL_KEY]) == pdfrw.objects.pdfname.BasePdfName:
                                    if '/' in annotation[ANNOT_VAL_KEY]:
                                        data_dict[key] = annotation[ANNOT_VAL_KEY][1:]
                            except:
                                pass
                    elif annotation['/AP']:
                        if not annotation['/T']:
                            annotation = annotation['/Parent']
                        key = annotation['/T'].to_unicode()
                        data_dict[key] = annotation[ANNOT_VAL_KEY]
                        try:
                            if type(annotation[ANNOT_VAL_KEY]) == pdfrw.objects.pdfstring.PdfString:
                                data_dict[key] = pdfrw.objects.PdfString.decode(annotation[ANNOT_VAL_KEY])
                            elif type(annotation[ANNOT_VAL_KEY]) == pdfrw.objects.pdfname.BasePdfName:
                                if '/' in annotation[ANNOT_VAL_KEY]:
                                    data_dict[key] = annotation[ANNOT_VAL_KEY][1:]
                        except:
                            pass
        if count == page_number:
            break
    if sort == True:
        return dict(sorted(data_dict.items()))
    else:
        return data_dict


def print_form_fields(input_pdf_path, sort=False, page_number=None):
    """
    Retrieves the form fields from get_form_fields(), then pretty prints
    the data_dict. Uses pdfrw.
    Parameters
    ---------
    input_pdf_path: str
        Path to the pdf you want the fields from.
    Returns
    ---------
    """
    data_dict = get_form_fields(input_pdf_path, sort, page_number)
    print("{" + ",\n".join("{!r}: {!r}".format(k, v) for k, v in data_dict.items()) + "}")


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
        if template_pdf.Root.AcroForm is not None:
            template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        else:
            print("Warning: Form Not Found")
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
            res[sub] = dictionary[sub]
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

    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for Page in template_pdf.pages:
        if Page[ANNOT_KEY]:
            for annotation in Page[ANNOT_KEY]:
                target = annotation if annotation[ANNOT_FIELD_KEY] else annotation[ANNOT_FIELD_PARENT_KEY]
                if annotation[ANNOT_FORM_type] == None:
                    pass
                if target and annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    key = target[ANNOT_FIELD_KEY][1:-1] # Remove parentheses
                    target_aux = target
                    while target_aux['/Parent']:
                        key = target['/Parent'][ANNOT_FIELD_KEY][1:-1] + '.' + key
                        target_aux = target_aux['/Parent']
                    if key in data_dict.keys():
                        if target[ANNOT_FORM_type] == ANNOT_FORM_button:
                            # button field i.e. a radiobuttons
                            if not annotation['/T']:
                                if annotation['/AP']:
                                    keys = annotation['/AP']['/N'].keys()
                                    if keys[0]:
                                        if keys[0][0] == '/':
                                            keys[0] = str(keys[0][1:])
                                    list_delim, tuple_delim = '-', '^'
                                    res = dict()
                                    for sub in data_dict:
                                        if isinstance(data_dict[sub], list):
                                            res[sub] = list_delim.join([str(ele) for ele in data_dict[sub]]) 
                                        else:
                                            res[sub] = str(data_dict[sub])
                                    temp_dict = res
                                    annotation = annotation['/Parent']
                                    options = []
                                    for each in annotation['/Kids']:
                                        keys2 = each['/AP']['/N'].keys()
                                        if '/Off' in keys2:
                                            keys2.remove('/Off')
                                        if ['/Off'] in keys:
                                            keys2.remove('/Off')
                                        export = keys2[0]
                                        if '/' in export:
                                            options.append(export[1:])
                                        else:
                                            options.append(export)
                                        if f'/{data_dict[key]}' == export:
                                            val_str = pdfrw.objects.pdfname.BasePdfName(f'/{data_dict[key]}')
                                        else:
                                            val_str = pdfrw.objects.pdfname.BasePdfName(f'/Off')
                                        if set(keys).intersection(set(temp_dict.values())):
                                            each.update(pdfrw.PdfDict(AS=val_str))
                                    if data_dict[key] not in options:
                                        if data_dict[key] != "None"  and data_dict[key] != "":
                                            raise KeyError(f"{data_dict[key]} Not An Option, Options are {options}")
                                    else:
                                        if set(keys).intersection(set(temp_dict.values())):
                                            annotation.update(pdfrw.PdfDict(V=pdfrw.objects.pdfname.BasePdfName(f'/{data_dict[key]}')))
                            else:
                                # button field i.e. a checkbox
                                target.update( pdfrw.PdfDict( V=pdfrw.PdfName(data_dict[key]) , AS=pdfrw.PdfName(data_dict[key]) ))
                                if target[ANNOT_FIELD_KIDS_KEY]:
                                    target[ANNOT_FIELD_KIDS_KEY][0].update( pdfrw.PdfDict( V=pdfrw.PdfName(data_dict[key]) , AS=pdfrw.PdfName(data_dict[key]) ))
                        elif target[ANNOT_FORM_type] == ANNOT_FORM_combo:
                            # Drop Down Combo Box
                            export = None
                            options = annotation[ANNOT_FORM_options]
                            if len(options) > 0:
                                if type(options[0]) == pdfrw.objects.pdfarray.PdfArray:
                                    options = list(options)
                                    options = [pdfrw.objects.pdfstring.PdfString.decode(x[0]) for x in options]
                                if type(options[0]) == pdfrw.objects.pdfstring.PdfString:
                                    options = [pdfrw.objects.pdfstring.PdfString.decode(x) for x in options]
                            if type(data_dict[key]) == list:
                                export = []
                                for each in options:
                                    if each in data_dict[key]:
                                        export.append(pdfrw.objects.pdfstring.PdfString.encode(each))
                                if export is None:
                                    if data_dict[key] != "None"  and data_dict[key] != "":
                                        raise KeyError(f"{data_dict[key]} Not An Option For {annotation[ANNOT_FIELD_KEY]}, Options are {options}")
                                pdfstr = pdfrw.objects.pdfarray.PdfArray(export)
                            else:
                                for each in options:
                                    if each == data_dict[key]:
                                        export = each
                                if export is None:
                                    if data_dict[key] != "None" and data_dict[key] != "":
                                        raise KeyError(f"{data_dict[key]} Not An Option For {annotation[ANNOT_FIELD_KEY]}, Options are {options}")
                                pdfstr = pdfrw.objects.pdfstring.PdfString.encode(data_dict[key])
                            annotation.update(pdfrw.PdfDict(V=pdfstr, AS=pdfstr))
                        elif target[ANNOT_FORM_type] == ANNOT_FORM_text:
                            # regular text field
                            target.update( pdfrw.PdfDict( V=data_dict[key], AP=data_dict[key]) )
                            if target[ANNOT_FIELD_KIDS_KEY]:
                                target[ANNOT_FIELD_KIDS_KEY][0].update( pdfrw.PdfDict( V=data_dict[key], AP=data_dict[key]) )
                if flatten == True:
                    annotation.update(pdfrw.PdfDict(Ff=1))
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


def rotate_page(deg, input_pdf_path, output_map_path, page_number):
    """
    Rotate a page within the pdf document.
    Parameters
    ---------
    deg: float
        The x coordinate of the top left corner of the text.
    input_pdf_path: str
        Path to the pdf you want the fields from.
    output_map_path: str
        Path of the new pdf that is generated.
    page_number: float
        Number of the page to get the map of.
    Returns
    ---------
    """
    doc = fitz.open(input_pdf_path)
    page = doc[page_number-1]
    
    page.set_rotation(deg)
        
    doc.save(output_map_path)


def place_radiobutton(field_name, x, y, input_pdf_path, output_map_path, page_number, width=10, height=10, font_size=12, font_name=None, fill_color=(0.8,0.8,0.8), font_color=(0,0,0)):
    """
    Place a radio box in the pdf document. Use the get_coordinate_map
    function to help with placement.
    Parameters
    ---------
    field_name: str
        The name you want attatched to the field
    x: float
        The x coordinate of the top left corner of the text.
    y: float
        The y coordinate of the top right corner of the text.
    input_pdf_path: str
        Path to the pdf you want the fields from.
    output_map_path: str
        Path of the new pdf that is generated.
    page_number: float
        Number of the page to get the map of.
    width: float
        The width of the image
    height: float
        The height of the image
    font_size: float
        Size of the text being inserted.
    font_name: str
        The name of the font type you are using.
        https://github.com/t-houssian/fillpdf/blob/main/README.md#fonts
    fill_color: tuple
        The color to use (0,0,0) = white, (1,1,1) = black
    font_color: tuple
        The color to use (0,0,0) = white, (1,1,1) = black
    Returns
    ---------
    """
    doc = fitz.open(input_pdf_path)
    page = doc[page_number-1]
    
    widget = fitz.Widget()
    widget.rect = fitz.Rect(x, y, x+width, y+height)
    widget.field_type = fitz.PDF_WIDGET_TYPE_RADIOBUTTON
    widget.text_fontsize = 12
    widget.text_color = font_color
    widget.text_font = font_name
    widget.fill_color = fill_color
    widget.field_name = field_name
    
    page.add_widget(widget)
        
    doc.save(output_map_path)


def place_dropdown(field_name, values, x, y, input_pdf_path, output_map_path, page_number, width=10, height=10, font_size=12, font_name=None, fill_color=(0.8,0.8,0.8), font_color=(0,0,0)):
    """
    Place a dropdown box widget in the pdf document. Use the get_coordinate_map
    function to help with placement.
    Parameters
    ---------
    field_name: str
        The name you want attatched to the field
    values: tuple
        The values for the dropdown menu. The first value becomes the default.
    x: float
        The x coordinate of the top left corner of the text.
    y: float
        The y coordinate of the top right corner of the text.
    input_pdf_path: str
        Path to the pdf you want the fields from.
    output_map_path: str
        Path of the new pdf that is generated.
    page_number: float
        Number of the page to get the map of.
    width: float
        The width of the image
    height: float
        The height of the image
    font_size: float
        Size of the text being inserted.
    font_name: str
        The name of the font type you are using.
        https://github.com/t-houssian/fillpdf/blob/main/README.md#fonts
    fill_color: tuple
        The color to use (0,0,0) = white, (1,1,1) = black
    font_color: tuple
        The color to use (0,0,0) = white, (1,1,1) = black
    Returns
    ---------
    """
    doc = fitz.open(input_pdf_path)
    page = doc[page_number-1]
    widget = fitz.Widget()
    widget.field_name = field_name
    widget.field_label = "Drop Down"
    widget.fill_color = fill_color
    widget.text_color = font_color
    widget.field_type = fitz.PDF_WIDGET_TYPE_LISTBOX
    widget.field_flags = fitz.PDF_CH_FIELD_IS_COMMIT_ON_SEL_CHANGE
    widget.choice_values = values
    widget.rect = fitz.Rect(x, y, x+width, y+height)
    widget.text_fontsize = font_size
    widget.field_value = widget.choice_values[-1]
    page.add_widget(widget)
    
    doc.save(output_map_path)


def place_text_box(field_name, prefilled_text, x, y, input_pdf_path, output_map_path, page_number, width=10, height=10, font_size=12, font_name=None, fill_color=(0.8,0.8,0.8), font_color=(0,0,0)):
    """
    Place a fillable text box widget in the pdf document. Use the get_coordinate_map
    function to help with placement.
    Parameters
    ---------
    field_name: str
        The name you want attatched to the field
    prefilled_text: str
        The text you want prefilled in this widget
    x: float
        The x coordinate of the top left corner of the text.
    y: float
        The y coordinate of the top right corner of the text.
    input_pdf_path: str
        Path to the pdf you want the fields from.
    output_map_path: str
        Path of the new pdf that is generated.
    page_number: float
        Number of the page to get the map of.
    width: float
        The width of the image
    height: float
        The height of the image
    font_size: float
        Size of the text being inserted.
    font_name: str
        The name of the font type you are using.
        https://github.com/t-houssian/fillpdf/blob/main/README.md#fonts
    fill_color: tuple
        The color to use (0,0,0) = white, (1,1,1) = black
    font_color: tuple
        The color to use (0,0,0) = white, (1,1,1) = black
    Returns
    ---------
    """
    doc = fitz.open(input_pdf_path)
    page = doc[page_number-1]
    
    widget = fitz.Widget()
    widget.rect = fitz.Rect(x, y, x+width, y+height)
    widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    widget.text_fontsize = 12
    widget.text_font = font_name
    widget.fill_color = fill_color
    widget.text_color = font_color
    widget.field_name = field_name
    widget.field_value = prefilled_text
    widget.field_label = "arbitrary text - e.g. to help filling the field"
    
    page.add_widget(widget)
    field = page.first_widget
    assert field.field_type_string == "Text"
    
    doc.save(output_map_path)


def place_image(file_name, x, y, input_pdf_path, output_map_path, page_number, width=10, height=10):
    """
    Place image on the pdf document. Use the get_coordinate_map
    function to help with placement.
    Parameters
    ---------
    file_name: str
        The path of the file to be placed in the image
    x: float
        The x coordinate of the top left corner of the text.
    y: float
        The y coordinate of the top right corner of the text.
    input_pdf_path: str
        Path to the pdf you want the fields from.
    output_map_path: str
        Path of the new pdf that is generated.
    page_number: float
        Number of the page to get the map of.
    width: float
        The width of the image
    height: float
        The height of the image
    Returns
    ---------
    """
    doc = fitz.open(input_pdf_path)
    page = doc[page_number-1]
    
    page.insert_image(fitz.Rect(x, y, x+width, y+height), filename=file_name)
    doc.save(output_map_path)


def place_text(text, x, y, input_pdf_path, output_map_path, page_number, font_size=12, font_name="helv", color=None):
    """
    Place Text on the pdf document. Use the get_coordinate_map
    function to help with placement.
    Parameters
    ---------
    text: str
        The string you want to be place in the document
    x: float
        The x coordinate of the bottom left corner of the text.
    y: float
        The y coordinate of the bootom right corner of the text.
    input_pdf_path: str
        Path to the pdf you want the fields from.
    output_map_path: str
        Path of the new pdf that is generated.
    page_number: float
        Number of the page to get the map of.
    font_size: float
        Size of the text being inserted.
    font_name: str
        The name of the font type you are using.
        https://github.com/t-houssian/fillpdf/blob/main/README.md#fonts
    color: tuple
        The color to use (0,0,0) = white, (1,1,1) = black
    Returns
    ---------
    """
    doc = fitz.open(input_pdf_path)
    page = doc[page_number-1]
    page.insert_text(fitz.Point(x, y), str(text), fontname=font_name, color=color, fontsize=font_size)
    doc.save(output_map_path)


def get_coordinate_map(input_pdf_path, output_map_path, page_number=1):
    """
    Creates a map on the pdf page to help in the placement of text, photos,
    and widgets.
    Parameters
    ---------
    input_pdf_path: str
        Path to the pdf you want the fields from.
    output_map_path: str
        Path of the new pdf that is generated.
    page_number: float
        Number of the page to get the map of.
    Returns
    ---------
    A dictionary of form fields and their filled values.
    """
    doc = fitz.open(input_pdf_path)
    page = doc[page_number-1]
    max_x = page.rect[2]
    max_y = page.rect[3]
        
    for y in range(0, int(math.ceil(max_y / 50.0)) * 50, 50): # Drop a dot every 20 px x and y
        page.insert_text(fitz.Point(0 , y), str(y), fontsize=12, fontname="times-bold", color=(1, 0, 0))
        page.draw_line(fitz.Point(0 , y), fitz.Point(max_x , y), color=(1, 0, 0))
        
    for x in range(0, int(math.ceil(max_x / 50.0)) * 50, 50):
        page.insert_text(fitz.Point(x , 12), str(x), fontsize=12, fontname="times-bold", color=(1, 0, 0))
        page.draw_line(fitz.Point(x , 12), fitz.Point(x , max_y), color=(1, 0, 0))
    
    doc.save(output_map_path)