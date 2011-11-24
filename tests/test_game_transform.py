import parity
from nose.tools import assert_equals
from StringIO import StringIO

SCORE_FILE = StringIO("""
09/12/1959 North Dakota                27  Montana                     19 
09/13/1959 St. Ambrose                  7  Xavier                      27 
09/18/1959 Florida                     30  Tulane                       0 
09/18/1959 San Jose State              14  Denver                      13 
09/19/1959 California                  20  Washington State             6 @ Spokane, WA
09/19/1959 Clemson                     20  North Carolina              18 
""")

OUTPUT_FILE = [
    ["09/12/1959", "North Dakota", 27, "Montana", 19],
    ["09/13/1959", "St. Ambrose", 7, "Xavier", 27],
    ["09/18/1959", "Florida", 30, "Tulane", 0],
    ["09/18/1959", "San Jose State", 14, "Denver", 13],
    ["09/19/1959", "California", 20, "Washington State", 6],
    ["09/19/1959", "Clemson", 20, "North Carolina", 18],
    ]

SINGLE_SCORE = StringIO("""
09/12/1959 North Dakota                27  Montana                     19 
""")

SINGLE_OUTPUT = [
    ["09/12/1959", "North Dakota", 27, "Montana", 19],
]

LOC_SCORE = StringIO("""
09/19/1959 California                  20  Washington State             6 @ Spokane, WA
""")

LOC_OUTPUT = [
    ["09/19/1959", "California", 20, "Washington State", 6],
]


def test_single_score_with_loc():
    assert_equals(parity.parse_scores(SINGLE_SCORE), SINGLE_OUTPUT)

def test_scores():
    assert_equals(parity.parse_scores(SCORE_FILE), OUTPUT_FILE)

def test_single_score():
    assert_equals(parity.parse_scores(SINGLE_SCORE), SINGLE_OUTPUT)

def test_single_score_with_loc():
    assert_equals(parity.parse_scores(LOC_SCORE), LOC_OUTPUT)

def test_long_college_name():
    score = "10/13/1883 Brooklyn Polytechnic Institute                               0  Stevens                               59"
    row = [["10/13/1883", "Brooklyn Polytechnic Institute", 0, "Stevens", 59]]
    assert_equals(row, parity.parse_scores(StringIO(score)))
