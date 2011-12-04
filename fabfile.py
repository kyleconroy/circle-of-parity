#!/usr/local/bin/python3
import analyze as analyze_games
import csv
import requests
import os
import json
import urllib
import parity
from collections import namedtuple
from fabric.api import task, local
from lxml.etree import HTML
from jinja2 import Template, Environment, FileSystemLoader

@task
def download():
    pass


@task 
def scrape_games():

    def scrape_game_info(url, folder):
        local("mkdir -p data/{0}".format(folder))
        urls = [url.format(year) for year in xrange(1869, 2011)]
        results = [requests.get(u) for u in urls]
        for year, resp in enumerate(results, start=1869):
            if resp.ok:
                with open("data/{0}/{0}_{1}.txt".format(folder, year), "w") as f:
                    f.write(resp.content)
            else:
                print "Error retrieving {0}".format(resp.url)

    base_uri = "http://homepages.cae.wisc.edu/~dwilson/rfsc/history/howell/"
    scrape_game_info(base_uri + "cf{}tms.txt", "teams")
    scrape_game_info(base_uri + "cf{}gms.txt", "scores")


@task
def scrape_logos():
    local("mkdir -p data/logos")

    base_uri = "http://www.sportslogos.net/league.php?id={0}"
    for url in [base_uri.format(page_id) for page_id in xrange(30, 36)]:
        resp = requests.get(url)

        if not resp.ok:
            print "Error retrieving {0}".format(url)
            continue

        tree = HTML(resp.content)

        for thumb in tree.findall(".//div[@class='thumbHolder']"):
            link = thumb.find("a")
            logo = link.find("img")

            title = link.attrib["title"].lower().replace("Logos", "")
            title = title.replace(" ", "_").strip()
            filename = "data/logos/{0}.gif".format(title)

            urllib.urlretrieve(logo.attrib["src"], filename)


@task
def scrape():
    scrape_games()
    scrape_logos()


@task
def circles_to_html():
    local("mkdir -p data/circle_html")
    circles = json.load(open("data/circles.json"))
    #Environment is for working with the template. 
    env = Environment(loader=FileSystemLoader('data/circle_html/'))
    num = 0
    for circle in circles:
        imgs = []
        team_names = []
        game_info = []
        for game in circle["teams"]:
            
            logo_path = local("find data/logos -name '*{0}*'".format('_'.join(game["winner"].lower().split(' '))), capture = True)
            
            #The find might return multiple matches. This is bad. 
            #Fixed by terrible and incorrect hack. May Linus forgive me. 
            if len(logo_path.split('\n')) > 1:
                logo_path = logo_path.split('\n')[0]

            #Might actually not have logo, safety check
            elif logo_path == '':
                logo_path = 'data/circle_html/images/img_not_found.jpg'

            imgs.append(logo_path)
            team_names.append(game["winner"])
            game_info.append("Beat {0}, Score: {1} - {2}".format(game["loser"], game["winning_score"], game["losing_score"]))
        
        template = env.get_template('templates/circle_template.html')
        f = open('data/circle_html/circles{0}.html'.format(num), 'w')
        f.writelines(template.render(team_info = zip(imgs, team_names, game_info)))
        num += 1


            


@task
def transform_teams():
    files = [path for path in os.listdir("data/teams") if path.endswith("txt")]
    for conference_file in files:
        year = int(conference_file.replace("teams_", "").replace(".txt", ""))
        filename = "teams_{0}.json".format(year)

        with open(os.path.join("data/teams", conference_file)) as f:
            data = parity.parse_conferences(f, year)

        with open(os.path.join("data/teams", filename), "w") as f:
            json.dump(data, f)

@task
def transform_scores():
    files = [p for p in os.listdir("data/scores") if p.endswith("txt")]
    for score_file in files:
        year = int(score_file.replace("scores_", "").replace(".txt", ""))
        filename = "scores_{0}.csv".format(year)

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
    data = analyze_games.analyze()
    json.dump(data, open("data/circles.json", "w"))

@task
def report():
    circles = json.load(open("data/circles.json"))

    for circle in circles:
        line = "Parity in {0} in {1}".format(circle["conference"], circle["year"])

        print line
        print "".join(["="] * len(line))

        for game in circle["teams"]:
            print "{0} vs {1}: {2}-{3}".format(game["winner"], game["loser"],
                game["winning_score"], game["losing_score"])
        print

    longest = max(circles, key=lambda circle: len(circle["teams"]))
    first = min(circles, key=lambda circle: circle["year"])

    conf_total = {}
    for circle in circles:
        if not circle["conference"] in conf_total:
            conf_total[circle["conference"]] = []
        conf_total[circle["conference"]].append(str(circle["year"]))

    year_total = {}
    for circle in circles:
        if not circle["year"] in year_total:
            year_total[circle["year"]] = []
        year_total[circle["year"]].append(circle["conference"])

    most_year = max(year_total.items(), key=lambda x: len(x[1]))
    most_conf = max(conf_total.items(), key=lambda x: len(x[1]))
    avg = float(sum([len(x) for x in year_total.values()])) / len(range(1869, 2011))

    print "Total circles        : {0} in {1} years".format(
        len(circles), len(range(1869, 2011)))
    print "Average per year     : {0}".format(avg)
    print "First circle         : {0}".format(first["year"])
    print "Most in a conference : {0} in the {1} in {2}".format(
        len(most_conf[1]), most_conf[0], ", ".join(most_conf[1]))
    print "Most in a season     : {0} in {1} with {2}".format(
        len(most_year[1]), most_year[0], ", ".join(most_year[1]))
    print "Largest circle       : {0} teams, {1} in {2}".format(
        len(longest["teams"]), longest["conference"], longest["year"])


