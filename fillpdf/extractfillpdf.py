# -*- coding: utf-8 -*-
"""
This command extract the fields and data from a fillable PDF.

It is, basically, a wrapper around the fillpdf library.

Note:

References:
"""

import argparse
import json
import logging
import sys
from typing import List

from fillpdf import fillpdfs,  __version__

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter

def extractfillpdf(input_file: str, output_file: str) -> int:
    """ "Extract data an store it in json format

    Args:
        input_file (str): Input PDF file
        output_file (str): Output JSON file

    Returns:
        int: number of records
    """

    # read PDF file with fillpdf.get_form_fields
    dict_data = fillpdfs.get_form_fields(input_file)

    # check if dict_data is not empty
    if dict_data:
        _logger.debug("Read data: {}".format(dict_data))
        # write json file
        with open(output_file, "w") as outfile:
            json.dump(dict_data, outfile)
    else:
        _logger.error("No data found")
        print("No data found")

    return len(dict_data)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args: List[str]) -> argparse.Namespace:
    """Parse command line parameters

    Args:
        args (List[str]): command line parameters as list of strings
                          (for example  ``["--help"]``).

    Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """

    parser = argparse.ArgumentParser(description="Extract fill data from PDF")
    parser.add_argument(
        dest="inputfile",
        help="Input pdf file",
        type=str,
        metavar="test.pdf",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="outputfile",
        help="Output file to write result, if none given, \
            it will be the input file with the JSON extension",
        type=str,
        metavar="test.json",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="extractfillpdf {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel: int):
    """Setup basic logging

    Args:
        loglevel (int): minimum loglevel for emitting messages
    """

    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args_m: List[str]):
    """Wrapper allowing :func:`extractfillpdf` to be called with string arguments
    in a CLI fashion

    Instead of returning the value from :func:`extractfillpdf`, it prints the result
    to the ``stdout`` in a nicely formatted message.

    Args:
        args_m (List[str]): command line parameters as list of strings
                            (for example  ``["--verbose", "42"]``).
    """

    args = parse_args(args_m)
    setup_logging(args.loglevel)

    # check if outputfile is given, if not, use inputfile with JSON extension
    if args.outputfile:
        pass
    else:
        # remove pdf extension and add json extension
        args.outputfile = args.inputfile.replace(".pdf", ".json")
        _logger.debug("Output file name created: {}".format(args.outputfile))

    # trim spaces
    args.outputfile = args.outputfile.strip()

    print(">{}<".format(args.outputfile))
    num_records = extractfillpdf(args.inputfile, args.outputfile)
    print(
        "{} records have been proccesed from {} to {}".format(
            num_records, args.inputfile, args.outputfile
        )
    )
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m fillpdf.extractfillpdf test.pdf
    #
    run()
