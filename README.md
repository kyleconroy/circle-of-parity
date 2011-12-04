# Circle of Parity

A circle of parity happens when every team in a conference has beaten another team and lost to another in such a way that a cycle exists. This implies that every team is better than another team and worse than another, which seems contradictory

I posit that this happens more than you would think and is not a rare event. To the data!

## Installation

    pip install -r requirements.txt

## Process

A huge thanks to James Howell and his awesome [College Football Scores](http://homepages.cae.wisc.edu/~dwilson/rfsc/history/howell/) page. This wouldn't have been possible without it.

### Scrape the Data (You don't need to do this)

    fab scrape

This will scrape and download the score data, the conference data, and the logos

### Transform the Data

    fab transform

This will transform the raw txt data into CSV and JSON.

### Analyze the Data

    fab analyze

This takes in the CSV and JSON files and spits out a circle.json file with all the parity circles in the data 

### Make it Pretty 

    fab report

Print out a nice report of all circles

    Total circles        : 134 in 142 years
    Average per year     : 0.943661971831
    First circle         : 1869
    Most in a season     : 6 in 2006 with Big 12, Big East, CUSA, MAC, Pac 10, SEC
    Largest circle       : 16 teams, WAC in 1997
    Most in a conference : 16 in the Big Ten in 1959, 1962, 1963, 1964, 1972, 1976, 1982, 1985, 1986, 1996, 2000, 2001, 2004, 2008, 2009, 2010
        
### Interactive Parity Circles
   
   fab circles_to_html

Create an HTML page for each circle of parity. You can access via any browser by opening data/circles_html/circles*num*.html where *num* ranges from 0-134 (number of circles of parity we found so far). Thanks to Addy Osmani for his great jQuery plugin roundrr (http://addyosmani.com/blog/jquery-roundrr/). Also uses Jinja2 for templating in the HTML page creation. 