import json
from numpy import random, array, subtract

team_names = ['alpha', 'bravo']

def new_teams(team_names: list = team_names):
    teams = {}
    for name in team_names:
        teams[name] = {}
        teams[name]["members"] = []
    return teams


def toss_coin() -> float:
    return random.uniform()


def assign_team(coin_toss: float) -> str:
    if coin_toss < 0.5:
        return team_names[0]
    else:
        return team_names[1]


def number_of_teammates(team: list) -> int:
    return len(team)


def get_team_other_than(name: str, team_names: list) -> str:
    other_teams = team_names.copy()
    other_teams.remove(name)
    return other_teams[0]


def assign_teams(personnel: list, teams: dict, maximum_team_size: int = 5) -> dict:
    for person in personnel:
        coin_toss = toss_coin()
        suggested_team = assign_team(coin_toss)
        if number_of_teammates(teams[suggested_team]["members"]) >= maximum_team_size:
            suggested_team = get_team_other_than(suggested_team, team_names)
        teams[suggested_team]["members"].append(person)
    return teams


def get_total_years_of_experience(team: list) -> int:
    years_experience = 0
    for person in team:
        years_experience += person["years_experience"]
    return years_experience


def annotate_total_years_of_experience(teams: dict) -> None:
    for team_name, team in teams.items():
        teams[team_name]["total_years_of_experience"] = get_total_years_of_experience(team["members"])


def compare_total_years_of_experience(teams: dict) -> None:
    team_experience = array([team["total_years_of_experience"] for team_name, team in teams.items()])
    difference_matrix = subtract.outer(team_experience, team_experience)
    return difference_matrix.max()


def annotate_rosters(teams: dict) -> None:
    for team_name, team in teams.items():
        teams[team_name]["roster"] = [person["name"] for person in team["members"]]


if __name__ == "__main__":
    with open('personnel.json') as file:
        personnel = json.load(file)
        difference_in_total_years_experience = 999
        while difference_in_total_years_experience > 0.5:
            teams = new_teams()
            assign_teams(personnel, teams)
            annotate_total_years_of_experience(teams)
            difference_in_total_years_experience = compare_total_years_of_experience(teams)
        annotate_rosters(teams)
        for team_name, team in teams.items():
            team_assignment = {"name": team_name, "roster": team["roster"]}
            with open(f"{team_name}.json", "w") as outfile:
                json.dump(team_assignment, outfile)        
