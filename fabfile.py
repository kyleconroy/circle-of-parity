import csv
import requests
import os
import json
import urllib
import parity
from fabric.api import task, local
from lxml.etree import HTML


@task
def download():
    pass


@task 
def scrape_games():

    def scrape_game_info(url, folder):
        local("mkdir -p data/{}".format(folder))
        urls = [url.format(year) for year in xrange(1869, 2011)]
        results = [requests.get(u) for u in urls]
        for year, resp in enumerate(results, start=1869):
            if resp.ok:
                with open("data/{0}/{0}_{1}.txt".format(folder, year), "w") as f:
                    f.write(resp.content)
            else:
                print "Error retrieving {}".format(resp.url)

    base_uri = "http://homepages.cae.wisc.edu/~dwilson/rfsc/history/howell/"
    scrape_game_info(base_uri + "cf{}tms.txt", "teams")
    scrape_game_info(base_uri + "cf{}gms.txt", "scores")


@task
def scrape_logos():
    local("mkdir -p data/logos")

    base_uri = "http://www.sportslogos.net/league.php?id={}"
    for url in [base_uri.format(page_id) for page_id in xrange(30, 36)]:
        resp = requests.get(url)

        if not resp.ok:
            print "Error retrieving {}".format(url)
            continue

        tree = HTML(resp.content)

        for thumb in tree.findall(".//div[@class='thumbHolder']"):
            link = thumb.find("a")
            logo = link.find("img")

            title = link.attrib["title"].lower().replace("Logos", "")
            title = title.replace(" ", "_").strip()
            filename = "data/logos/{}.gif".format(title)

            urllib.urlretrieve(logo.attrib["src"], filename)


@task
def scrape():
    scarpe_games()
    scrape_logos()


@task
def transform_teams():
    files = [path for path in os.listdir("data/teams") if path.endswith("txt")]
    for conference_file in files:
        year = int(conference_file.replace("teams_", "").replace(".txt", ""))
        filename = "teams_{}.json".format(year)

        with open(os.path.join("data/teams", conference_file)) as f:
            data = parity.parse_conferences(f, year)

        with open(os.path.join("data/teams", filename), "w") as f:
            json.dump(data, f)

@task
def transform_scores():
    files = [p for p in os.listdir("data/scores") if p.endswith("txt")]
    for score_file in files:
        year = int(score_file.replace("scores_", "").replace(".txt", ""))
        filename = "scores_{}.csv".format(year)

        with open(os.path.join("data/scores", score_file)) as f:
            data = parity.parse_scores(f)

        writer = csv.writer(open(os.path.join("data/scores", filename), "w"))

        for row in data:
            writer.writerow(row)

@task
def transform():
    transform_teams()
    transform_scores()


@task
def analyze():
    pass


@task
def report():
    pass
