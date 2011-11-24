def parse_conferences(conference_file, year):
    conferences = []
    current_conference = {}

    for line in conference_file:
        if line.startswith("  "):
            if current_conference:
                team = line.strip().replace('"', "")
                current_conference["teams"].append(team)
        elif line.startswith(" "):
            current_conference = {
                "name": line.strip(),
                "teams": [],
            }
            conferences.append(current_conference)

    return {
        "year": year,
        "conferences": conferences,
    }


def parse_scores(score_file):
    scores = []

    for line in score_file:
        try:
            game, location = line.strip().split("@")
            city, state = [loc.strip() for loc in location.split(",")]
        except ValueError:
            game = line.strip()
            city = None
            state = None

        if not len(game):
            continue

        date       = game[:11].strip()
        home_team  = game[11:38].strip()
        home_score = int(game[39:42].strip())
        away_team  = game[43:71].strip()
        away_score = int(game[71:].strip())

        scores.append([date, home_team, home_score, away_team,
                      away_score, city, state])

    return scores




