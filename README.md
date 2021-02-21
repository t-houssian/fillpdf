# fillpdf

# Overview
This is a simple package to make filling pdfs much easier. I have delt with a lot projects that involve manipulating pdfs in python. I found no easy solution for writting, or flattening pdfs, so I decided to make a library to make this task much easier. As a young software engineer I kept this library really simple but practicle and am open to any input for the future!

- Fills pdfs
- Lists fields in pdf
- Flattens pdfs (Turns to an image)

[Software Demo Video](http://youtube.link.goes.here)

# Installation
    pip install  
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
