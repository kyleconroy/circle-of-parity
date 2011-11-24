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
        line = line.replace("Institute1", "Institute ")
        parts = line.split()

        if not len(parts):
            continue

        city = None
        state = None
        
        row = [parts.pop(0)]
        team = []
        score_count = 0

        for part in parts:
            if score_count > 2:
                break
            try:
                score = int(part)
                row.append(" ".join(team))
                row.append(score)
                score_count += 1
                team = []
            except ValueError:
                team.append(part)
    
        scores.append(row)

    return scores




