from typing import Optional


def is_text_field_multiline(field_format: int) -> bool:
  return "{0:b}".format(field_format)[-13] == 1

def make_read_only(field_format: Optional[str]) -> int:
  """
  Returns a Read-Only version of a given field format.

  According to the PDF specifications, the /Ff field is a 32-bit integer
  defining multiple characteristics. The lowest bit defines a "read-only" field.

  Parameters
  ---------
  field_format: Optional[str]
      The field format for a given field.

  Returns
  ---------
  """
  if field_format is None:
    return 1
  else:
    binary_field_format = "{0:b}".format(int(field_format))
    read_only_field_format = binary_field_format[:-1] + "1"
    return int(read_only_field_format, 2)
