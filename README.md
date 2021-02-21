# fillpdf

# Overview
This is a simple package to make filling pdfs much easier. I have delt with a lot projects that involve manipulating pdfs in python. I found no easy solution for writting, or flattening pdfs, so I decided to make a library to make this task much easier. As a young software engineer I kept this library really simple but practicle and am open to any input for the future!

- Fills pdfs
- Lists fields in pdf
- Flattens pdfs (Turns to an image)

# Function Documentation
#####
    write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict)
- input_pdf_path- path to your pdf you want to alter (including the pdf name could just leave as 'blank.pdf' if the pdf is in your current directory)
- output_pdf_path- path of where you want your pdf to write to (including the pdf name could just leave as 'new.pdf' to write to current directory)
- data_dict- dictionary that contains the fields to write to as your key and what to write to it as your value
###### For Example:
    data_dict = {'Address 1 Text Box': '500 West Main Street',
    'Driving License Check Box': 'Yes',
    'Language 1 Check Box': 'Off',}
    
    fillpdfs.write_fillable_pdf('blank.pdf', 'new.pdf', data_dict)
- For radio boxes ('Off' = not filled, 'Yes' = filled) 

##### flatten_pdf
    flatten_pdf(input_pdf_path, output_pdf_path)
- input_pdf_path- path to your pdf you want to alter (including the pdf name could just leave as 'blank.pdf' if the pdf is in your current directory)
- output_pdf_path- path of where you want your pdf to write to (including the pdf name could just leave as 'new.pdf' to write to current directory)
###### For Example:
    fillpdfs.flatten_pdf('new.pdf', 'newflat.pdf')

##### get_form_fields
    get_form_fields(input_pdf_path)
- input_pdf_path- path to your pdf you want to alter (including the pdf name could just leave as 'blank.pdf' if the pdf is in your current directory)
###### For Example:
    fillpdfs.get_form_fields('blank.pdf')


[Software Demo Video](http://youtube.link.goes.here)

# Installation
    pip install fillpdf 
    conda install -c conda-forge poppler

# Development Environment
##### Builds upon
- 'pdfrw'
- 'pdf2image'
- 'Pillow'
- 'PyPDF2'

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [List PDF Fields](https://stackoverflow.com/questions/3984003/how-to-extract-pdf-fields-from-a-filled-out-form-in-python)
* [Fill PDF Fields](https://stackoverflow.com/questions/60082481/how-to-edit-checkboxes-and-save-changes-in-an-editable-pdf-using-the-python-pdfr)
* [Flatten PDFs](https://stackoverflow.com/questions/27023043/generate-flattened-pdf-with-python)

# Credit
- [dvska](https://stackoverflow.com/users/1303068/dvska)
- [tomatoeshift](https://stackoverflow.com/users/11998874/tomatoeshift)
- [Tyler Houssian](https://stackoverflow.com/users/13537359/tyler-houssian)

# Future Work
* Add perfect fill (sometimes does not fill random things ie. drop down lists)
* give option to place text by coordinate
* easier way to fill the data dictionary in write_fillable_pdf function
