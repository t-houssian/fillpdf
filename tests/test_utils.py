from typing import Optional

from fillpdf.utils.field_format import make_read_only

# Given no test framework is currently defined, I just used some standard python

def test_make_read_only_with_valid_field_format(fixture: str = "34325"):
  read_only_field_format = make_read_only(fixture)
  binary_field_format = "{0:b}".format(int(read_only_field_format))
  assert binary_field_format.endswith("1")

def test_make_read_only_with_empty_field_format(fixture: Optional[str] = None):
  read_only_field_format = make_read_only(fixture)
  binary_field_format = "{0:b}".format(int(read_only_field_format))
  assert binary_field_format.endswith("1")
