import csv
import requests
import os
import json
import urllib
import parity
from collections import namedtuple
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


def find_all_paths(graph, start, end, path=[]):
        #http://www.python.org/doc/essays/graphs/
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths


def find_cycle(graph):
    cycles=[]
    for startnode in graph:
        for endnode in graph:
            newpaths = find_all_paths(graph, startnode, endnode)
            for path in newpaths:
                if (len(path)==len(graph)):
                    if path[0] in graph[path[len(graph)-1]]:
                        #print path[0], graph[path[len(graph)-1]]
                        path.append(path[0])
                        cycles.append(path)
    return cycles


@task
def analyze():
    Game = namedtuple('Game', 'day home_team home_score away_team away_score')
    local("mkdir -p data/circles")

    for year in range(1869, 2011):
        results = {}
        score_file = "data/scores/scores_{}.csv".format(year)
        conference_file = "data/teams/teams_{}.json".format(year)

        try:
            reader = csv.reader(open(score_file))
        except IOError:
            continue

        for row in reader:
            game = Game(*row)
            if game.home_team not in results:
                results[game.home_team] = set()

            if game.away_team not in results:
                results[game.away_team] = set()

            if int(game.home_score) > int(game.away_score):
                results[game.home_team].add(game.away_team)
            else:
                results[game.away_team].add(game.home_team)

        data = json.load(open(conference_file)) 

        for conference in data["conferences"]:
            print conference["name"]
            team = len(conference["teams"])
            print "Plays {} games".format((team * (team - 1)) / 2)

        continue

        
        for conference in data["conferences"]:
            graph = {}
            queue = []
            seen = set()

            for team in conference["teams"]:
                if team in results:
                    graph[team] = results[team]

            a = find_cycle(graph)

            queue.append(graph.keys().pop())

            while len(queue):
                first = queue.pop() 

                if first not in graph:
                    continue

                if first not in seen:
                    seen.add(first)
                    queue.extend(list(graph[first]))
                else:
                    pass
                    #print "Parity in {} {}?".format(year, conference["name"])

@task
def report():
    pass
