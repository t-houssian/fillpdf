# fillpdf
https://pypi.org/project/fillpdf/

# Overview
This is a simple package to make filling pdfs much easier. I have delt with a lot projects that involve manipulating pdfs in python. I found no easy solution for writting, or flattening pdfs, so I decided to make a library to make this task much easier. As a young software engineer I kept this library really simple but practicle and am open to any input for the future!

This project primarily builds upon a forked version of pdfrw called [pdfrw2](https://pypi.org/project/pdfrw2/).

- Fills pdfs
- Lists fields in pdf
- Flattens pdfs (Turns to a non-editable pdf)

# Function Documentation
    import fillpdf
    from fillpdf import fillpdfs
##### get_form_fields (returns the data_dict)
    get_form_fields(input_pdf_path, sort=False, page_number=None)
- input_pdf_path- path to your pdf you want to alter (including the pdf name could just leave as 'blank.pdf' if the pdf is in your current directory)
- sort- sorts the dictionary alphabetically if True, retains the normal pdf order if false
- page_number- (int) pass the page number you want the values from if you are just needing a single pages values or if you want to find which page a key belongs to
###### For Example:
    fillpdfs.get_form_fields('blank.pdf')

##### print_form_fields (prints the data_dict)
    print_form_fields(input_pdf_path, sort=False, page_number=None)
- input_pdf_path- path to your pdf you want to alter (including the pdf name could just leave as 'blank.pdf' if the pdf is in your current directory)
- sort (default = False) - sorts the dictionary alphabetically if True, retains the normal pdf order if false
- page_number- (int) pass the page number you want the values from if you are just needing a single pages values or if you want to find which page a key belongs to. The number passed must be within the page range.
###### For Example:
    fillpdfs.print_form_fields('blank.pdf')
    
##### write_fillable_pdf
    write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict, flatten=False)
- input_pdf_path- path to your pdf you want to alter (including the pdf name could just leave as 'blank.pdf' if the pdf is in your current directory)
- output_pdf_path- path of where you want your pdf to write to (including the pdf name could just leave as 'new.pdf' to write to current directory)
- data_dict- dictionary that contains the fields to write to as your key and what to write to it as your value (get this from the get_form_fields function)
- flatten (default=False)- If True, then the fields will become uneditable when you write to the pdf.
###### For Example:
    data_dict = {'Address 1 Text Box': '500 West Main Street',
    'Driving License Check Box': 'Yes',
    'Language 1 Check Box': 'Off',}
    
    fillpdfs.write_fillable_pdf('blank.pdf', 'new.pdf', data_dict)
- For radio boxes ('Off' = not filled, 'Yes' = filled)
- For check boxes ('Off' or '' = not filled, 'Yes' = filled)
- For drop downs (Enter the name of the desired drop down option)
- For radio groups ('0' = The first option, '1' = The second option, '2' = the third option, etc.)

##### flatten_pdf
    flatten_pdf(input_pdf_path, output_pdf_path, as_images=False)
- input_pdf_path- path to your pdf you want to alter (including the pdf name could just leave as 'blank.pdf' if the pdf is in your current directory)
- output_pdf_path- path of where you want your pdf to write to (including the pdf name could just leave as 'new.pdf' to write to current directory)
- as_images=False- Default is False meaning it will update each individual annotation and set
        it to False. True means it will convert to images and then reinsert into the
        pdf. Try this if the first is not working. (this image technique requires poppler.)
###### For Example:
    fillpdfs.flatten_pdf('new.pdf', 'newflat.pdf')

###### Fonts
    {'courier': 'Courier',
    'courier-oblique': 'Courier-Oblique',
    'courier-bold': 'Courier-Bold',
    'courier-boldoblique': 'Courier-BoldOblique',
    'helvetica': 'Helvetica',
    'helvetica-oblique': 'Helvetica-Oblique',
    'helvetica-bold': 'Helvetica-Bold',
    'helvetica-boldoblique': 'Helvetica-BoldOblique',
    'times-roman': 'Times-Roman',
    'times-italic': 'Times-Italic',
    'times-bold': 'Times-Bold',
    'times-bolditalic': 'Times-BoldItalic',
    'symbol': 'Symbol',
    'zapfdingbats': 'ZapfDingbats',
    'helv': 'Helvetica',
    'heit': 'Helvetica-Oblique',
    'hebo': 'Helvetica-Bold',
    'hebi': 'Helvetica-BoldOblique',
    'cour': 'Courier',
    'coit': 'Courier-Oblique',
    'cobo': 'Courier-Bold',
    'cobi': 'Courier-BoldOblique',
    'tiro': 'Times-Roman',
    'tibo': 'Times-Bold',
    'tiit': 'Times-Italic',
    'tibi': 'Times-BoldItalic',
    'symb': 'Symbol',
    'zadb': 'ZapfDingbats'}

# Command Line Use
A command line wrapper is available for this tool. Here are the two commands:
##### extractfillpdf
    extractfillpdf input_pdf_path
    or
    extractfillpdf input_pdf_path -o output_json_path
- input_pdf_path- path to your pdf you want to alter (including the pdf name could just leave as 'blank.pdf' if the pdf is in your current directory)
- output_json_path- path of where you want your json file containing the fields and contents of the pdf to write to (If not included then the default will be the same name/path as the input_pdf_path but .json instead of .pdf)
###### For Example:
    extractfillpdf blank.pdf
    or
    extractfillpdf blank.pdf -o data.json
##### insertfillpdf
    insertfillpdf -j input_json_path -o output_pdf_path input_pdf_path
- input_pdf_path- path to your pdf you want to alter (including the pdf name could just leave as 'blank.pdf' if the pdf is in your current directory)
- input_json_path- path to the json file that you generated and modified with the extractfillpdf command. 
- output_pdf_path- path of where you want your pdf to write to (including the pdf name could just leave as 'new.pdf' to write to current directory)
###### For Example:
    insertfillpdf -j blank.json -o new.pdf blank.pdf
###### Help Command
    extractfillpdf --help or extractfillpdf -h
Will bring up this menu

    positional arguments:
      test.pdf              Input pdf file

    optional arguments:
      -h, --help            show this help message and exit
      -o test.json, --output test.json
                            Output file to write result, if none given, it will be the input file
                            with the JSON extension
      --version             show program's version number and exit
      -v, --verbose         set loglevel to INFO
      -vv, --very-verbose   set loglevel to DEBUG
      
###### Or:
    insertfillpdf --help or insertfillpdf -h
Will bring up this menu

    positional arguments:
      test.pdf              Input PDF file

    optional arguments:
      -h, --help            show this help message and exit
      -j test.json, --JSON test.json
                            Input JSON file, if none given, it will be the input file with the JSON
                            extension
      -o test_out.pdf, --output test_out.pdf
                            Output file to write result, if none given, it will be the input file
                            with '_out.pdf' extension'
      --version             show program's version number and exit
      -v, --verbose         set loglevel to INFO
      -vv, --very-verbose   set loglevel to DEBUG


[Software Demo Video](https://youtu.be/oM9XGmpbGyg)

# Installation
    pip install fillpdf 
    conda install -c conda-forge poppler
poppler is only needed if you are using the as_images=True mode of the `flattenpdf` function

# Development Environment
##### Builds upon
- 'pdfrw'
- 'pdf2image'
- 'Pillow'
- 'poppler'

# Useful Websites

* [List PDF Fields pdfrw](https://github.com/pmaupin/pdfrw/issues/165)
* [List PDF Fields](https://stackoverflow.com/questions/3984003/how-to-extract-pdf-fields-from-a-filled-out-form-in-python)
* [Fill PDF Fields](https://stackoverflow.com/questions/60082481/how-to-edit-checkboxes-and-save-changes-in-an-editable-pdf-using-the-python-pdfr)
* [Flatten PDFs](https://stackoverflow.com/questions/27023043/generate-flattened-pdf-with-python)
* [pdfrw2](https://pypi.org/project/pdfrw2/)

# Credit
- [dvska](https://stackoverflow.com/users/1303068/dvska)
- [gbroiles](https://github.com/pmaupin/pdfrw/issues/165)
- [tomatoeshift](https://stackoverflow.com/users/11998874/tomatoeshift)
- [Tyler Houssian](https://stackoverflow.com/users/13537359/tyler-houssian)
- [jtplaarj](https://github.com/jtplaarj)
- [WestHealth](https://github.com/WestHealth/pdf-form-filler)
- [sarnold](https://github.com/sarnold)
- [Patrick Maupin](https://github.com/pmaupin)

# Future Work
* give option to place text by coordinate
* alter or view pdf versions
