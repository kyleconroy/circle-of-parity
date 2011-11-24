from parity import parse_conferences
from nose.tools import assert_equals
from StringIO import StringIO


CONFERENCE_2010 = StringIO("""
3
Major Teams
 ACC
  Boston College"
  Clemson"
 Big 12
  Colorado"
  Iowa State"
  Texas A&M"
""")

OUTPUT_2010 = {
    "year": 2010,
    "conferences": [
        {
            "name": "ACC", 
            "teams": [
                "Boston College",
                "Clemson",
            ],
        },
        {
            "name": "Big 12",
            "teams": [
                "Colorado",
                "Iowa State",
                "Texas A&M",
            ],
        },
    ],
}

def test_conference_output():
    assert_equals(parse_conferences(CONFERENCE_2010, 2010), OUTPUT_2010) 
