import csv
import json
import parity
from collections import namedtuple


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
                        return path
    return cycles


def pairs(lst):
    i = iter(lst)
    first = prev = i.next()
    for item in i:
        yield prev, item
        prev = item
    yield item, first


def analyze():
    Game = namedtuple('Game', 'day home_team home_score away_team away_score')
    cops = []

    for year in range(1869, 2011):
        results = {}
        lookup = {}
        score_file = "data/scores/scores_{0}.csv".format(year)
        conference_file = "data/teams/teams_{0}.json".format(year)

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

            lookup[(game.away_team, game.home_team)] = game
            lookup[(game.home_team, game.away_team)] = game

            if int(game.home_score) > int(game.away_score):
                results[game.home_team].add(game.away_team)
            elif int(game.home_score) < int(game.away_score):
                results[game.away_team].add(game.home_team)

        data = json.load(open(conference_file)) 
        
        for conference in data["conferences"]:
            graph = {}
            queue = []
            seen = set()

            for team in conference["teams"]:
                if team in results:
                    graph[team] = results[team]

            cop = find_cycle(graph)

            if not cop:
                continue

            circle = []

            for winner, loser in pairs(cop):
                game = lookup[(winner, loser)]
                scores = [int(game.away_score), int(game.home_score)]
                circle.append({
                    "winner": winner,
                    "loser": loser,
                    "winning_score": max(scores),
                    "losing_score": min(scores),
                    })

            cops.append({
                "conference": conference["name"],
                "year": year,
                "teams": circle,
                })

    return cops

if __name__ == "__main__":
    analyze()  

