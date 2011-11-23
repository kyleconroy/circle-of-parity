# Circle of Parity

A circle of parity happens when every team in a conference has beaten another team and lost to another in such a way that a cycle exists. This implies that every team is better than another team and worse than another, which seems contradictory

I posit that this happens more than you would think and is not a rare event. To the data!

## Installation

    pip install -r requirements.txt

## Process

A huge thanks to James Howell and his awesome [College Football Scores](http://homepages.cae.wisc.edu/~dwilson/rfsc/history/howell/) page. This wouldn't have been possible without it.

### Retrieve the Data

    fab scrape

### Anaylyze the Data

    fab anaylyze

### Make it Pretty 

    fab report


