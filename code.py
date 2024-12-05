import collections

import pandas as pd
import plotly.graph_objects as go



PlPrf = pd.read_excel('Players_Performance.xlsx')
TmPrf = pd.read_excel('Teams_Performance.xlsx')
Trsfr = pd.read_excel('Transfers.xlsx')
# Function to remove duplicates from datasets
def remove_duplicates(df):
    return df.drop_duplicates()

remove_duplicates(PlPrf)
remove_duplicates(TmPrf)
remove_duplicates(Trsfr)

# Function to remove additional leagues from datasets
def remove_additional_leagues(df):
    return df[(df['league'] != 'Eredivisie') &
              (df['league'] != 'Ligue 1') &
              (df['league'] != 'Liga NOS')]

PlPrf = remove_additional_leagues(PlPrf)
TmPrf = remove_additional_leagues(TmPrf)
Trsfr = remove_additional_leagues(Trsfr)

# Function to filter the players performance dataset
def filter_players_performance(df):
    return df[df['season'].str[2:4] >= '17']

PlPrf = filter_players_performance(PlPrf)

clubs = {} # Dictionary to store club data, structure: {club: {league: league, seasons: {season: {position: position, players: []}}}}

for team in TmPrf.itertuples():
    if team.common_name not in clubs:
        clubs[team.common_name] = {}
        clubs[team.common_name]['league'] = team.league
        clubs[team.common_name]['seasons'] = {}
    clubs[team.common_name]['seasons'][team.season] = {}
    clubs[team.common_name]['seasons'][team.season]['position'] = team.league_position
    clubs[team.common_name]['seasons'][team.season]['players'] = []
    #print(clubs['Arsenal'])

players = {} # Dictionary to store player data, structure: {name: {season: {clubs: {club: performance}}}}

for player in PlPrf.itertuples():
    perf = -1
    if player[5] == 'Defender':
        perf = player[10]
    elif player[5] == 'Midfielder':
        perf = player[9]
    elif player[5] == 'Forward':
        perf = player[8]

    if perf > 0:
        birthday = pd.Timestamp(player.birthday_GMT)
        birthday = birthday.strftime('%d/%m/%Y')
        name = (player.full_name, birthday)
        if name not in players:
            players[name] = {}
        if player.season not in players[name]:
            players[name][player.season] = {}
            players[name][player.season]['clubs'] = {}
        players[name][player.season]['clubs'][player[6]] = perf
        clubs[player[6]]['seasons'][player.season]['players'].append(name)


    #print(players[('Alexis Sanchez', '19/12/1988')])
    #print(clubs['Arsenal'])

def show_player_performance(player): # Function to show player performance by season
    seasons = []
    performance = []
    for season in players[player]:
        seasons.append(season)
        sm = sum(players[player][season]['clubs'].values())
        ln = len(players[player][season]['clubs'].values())
        performance.append(sm / ln)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=seasons, y=performance, mode='lines+markers', name='Line Graph'))

    fig.update_layout(
        title=f'{player[0]} performance',
        xaxis_title='Season',
        yaxis_title='Performance'
    )

    fig.show()

    #show_player_performance(('Alexis Sanchez', '19/12/1988'))

def show_club_performance(club): # Function to show club performance by season
    seasons = []
    position = []
    for season in clubs[club]['seasons']:
        seasons.append(season)
        position.append(clubs[club]['seasons'][season]['position'])

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=seasons, y=position, mode='lines+markers', name='Line Graph'))

    fig.update_layout(
        title=f'{club} performance',
        xaxis_title='Season',
        yaxis_title='Position'
    )

    fig.show()

    #show_club_performance('Arsenal')

def show_average_players_performance_in_club(club): # Function to show average player performance in a club
    seasons = []
    performance = []
    for season in clubs[club]['seasons']:
        seasons.append(season)
        sm = 0
        ln = 0
        for player in clubs[club]['seasons'][season]['players']:
            sm += players[player][season]['clubs'][club]
            ln += 1
        performance.append(sm / ln)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=seasons, y=performance, mode='lines+markers', name='Line Graph'))

    fig.update_layout(
        title=f'{club} average player performance',
        xaxis_title='Season',
        yaxis_title='Performance'
    )

    fig.show()

    #show_average_players_performance_in_club('Union Berlin')

def show_the_most_progressive_club(): # Function to show the most progressive club
    the_most_clubs = ['', '', '', '', '']
    the_most_coef = [0, 0, 0, 0, 0]
    for club in clubs:
        seasons = []
        performance = []
        for season in clubs[club]['seasons']:
            seasons.append(season)
            sm = 0
            ln = 0
            for player in clubs[club]['seasons'][season]['players']:
                print(players[player])
                print(season)
                sm += players[player][season]['clubs'][club]
                ln += 1
            performance.append(sm / ln)
        coef = performance[0] / performance[-1]
        ind = the_most_coef.index(min(the_most_coef))
        if coef > the_most_coef[ind]:
            the_most_coef[ind] = coef
            the_most_clubs[ind] = club
    for i in range(5):
        print(f'{the_most_clubs[i]}: {the_most_coef[i]}')
        show_club_performance(the_most_clubs[i])
        show_average_players_performance_in_club(the_most_clubs[i])

    #show_the_most_progressive_club()

def show_the_most_regressive_club(): # Function to show the most regressive club
    the_most_clubs = ['', '', '', '', '']
    the_most_coef = [5, 5, 5, 5, 5]
    for club in clubs:
        seasons = []
        performance = []
        for season in clubs[club]['seasons']:
            seasons.append(season)
            sm = 0
            ln = 0
            for player in clubs[club]['seasons'][season]['players']:
                sm += players[player][season]['clubs'][club]
                ln += 1
            performance.append(sm / ln)
        coef = performance[0] / performance[-1]
        ind = the_most_coef.index(max(the_most_coef))
        if coef < the_most_coef[ind]:
            the_most_coef[ind] = coef
            the_most_clubs[ind] = club
    for i in range(5):
        print(f'{the_most_clubs[i]}: {the_most_coef[i]}')
        show_club_performance(the_most_clubs[i])
        show_average_players_performance_in_club(the_most_clubs[i])

    #show_the_most_regressive_club()

def show_the_most_progressive_players(): # Function to show the most progressive players
    the_most_players = ['', '', '', '', '']
    the_most_coef = [0, 0, 0, 0, 0]
    for player in players:
        seasons = []
        performance = []
        for season in players[player]:
            seasons.append(season)
            sm = sum(players[player][season]['clubs'].values())
            ln = len(players[player][season]['clubs'].values())
            performance.append(sm / ln)
        coef = performance[0] / performance[-1]
        ind = the_most_coef.index(min(the_most_coef))
        if coef > the_most_coef[ind]:
            the_most_coef[ind] = coef
            the_most_players[ind] = player
    for i in range(5):
        print(f'{the_most_players[i]}: {the_most_coef[i]}')
        show_player_performance(the_most_players[i])

    #show_the_most_progressive_players()

def show_the_most_regressive_players(): # Function to show the most regressive players
    the_most_players = ['', '', '', '', '']
    the_most_coef = [5, 5, 5, 5, 5]
    for player in players:
        seasons = []
        performance = []
        for season in players[player]:
            seasons.append(season)
            sm = sum(players[player][season]['clubs'].values())
            ln = len(players[player][season]['clubs'].values())
            performance.append(sm / ln)
        coef = performance[0] / performance[-1]
        ind = the_most_coef.index(max(the_most_coef))
        if coef < the_most_coef[ind]:
            the_most_coef[ind] = coef
            the_most_players[ind] = player
    for i in range(5):
        print(f'{the_most_players[i]}: {the_most_coef[i]}')
        show_player_performance(the_most_players[i])

    #show_the_most_regressive_players()

def show_average_players_performance_after_changing_the_league(league_before, league_after): # Function to show average player performance after changing the league form league_before to league_after
    years_before = collections.defaultdict(list)
    years_after = collections.defaultdict(list)
    for player in players:
        leagues = []
        performance = []
        l1 = l2 = ''
        p1 = p2 = 0
        for season in players[player]:
            if len(players[player][season]['clubs'].keys()) == 1:
                if p1 and p2 and l1 and l2:
                    l = clubs[list(players[player][season]['clubs'].keys())[0]]['league']
                    if l == l1:
                        leagues.append(l2)
                        performance.append(p2)
                        leagues.append(l1)
                        performance.append(p1)
                    else:
                        leagues.append(l1)
                        performance.append(p1)
                        leagues.append(l2)
                        performance.append(p2)
                    l1 = l2 = ''
                    p1 = p2 = 0
                leagues.append(clubs[list(players[player][season]['clubs'].keys())[0]]['league'])
                performance.append(list(players[player][season]['clubs'].values())[0])
            else:
                if l1 and l2 and p1 and p2:
                    lst = list(players[player][season]['clubs'].keys())
                    league1 = clubs[lst[0]]['league']
                    league2 = clubs[lst[1]]['league']
                    perf1 = players[player][season]['clubs'][lst[0]]
                    perf2 = players[player][season]['clubs'][lst[1]]
                    if l1 == league1 or l1 == league2:
                        leagues.append(l2)
                        performance.append(p2)
                        leagues.append(l1)
                        performance.append(p1)
                    else:
                        leagues.append(l1)
                        performance.append(p1)
                        leagues.append(l2)
                        performance.append(p2)
                    l1 = l2 = ''
                    p1 = p2 = 0
                lst = list(players[player][season]['clubs'].keys())
                league1 = clubs[lst[0]]['league']
                league2 = clubs[lst[1]]['league']
                perf1 = players[player][season]['clubs'][lst[0]]
                perf2 = players[player][season]['clubs'][lst[1]]
                if leagues and leagues[-1] == league1:
                    leagues.append(league1)
                    performance.append(perf1)
                    leagues.append(league2)
                    performance.append(perf2)
                elif leagues and leagues[-1] == league2:
                    leagues.append(league2)
                    performance.append(perf2)
                    leagues.append(league1)
                    performance.append(perf1)
                else:
                    l1 = league1
                    l2 = league2
                    p1 = perf1
                    p2 = perf2
        if l1 and l2 and p1 and p2:
            leagues.append(l1)
            performance.append(p1)
            leagues.append(l2)
            performance.append(p2)
        i = 0
        while i < len(leagues) - 1:
            if leagues[i] == league_before and leagues[i + 1] == league_after:
                j = i
                while j >= 0 and leagues[j] == league_before:
                    years_before[j - i - 1].append(performance[j])
                    j -= 1
                j = i + 1
                while j < len(leagues) and leagues[j] == league_after:
                    years_after[j - i].append(performance[j])
                    j += 1
                i = j
            else:
                i += 1
    l1 = sorted(list(years_before.keys()))
    l2 = [sum(years_before[i])/len(years_before[i]) for i in l1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=l1, y=l2, mode='lines+markers', name='Line Graph'))

    fig.update_layout(
        title=f'Average player performance before changing the league from {league_before} to {league_after}',
        xaxis_title='Years before changing the league',
        yaxis_title='Performance'
    )

    fig.show()

    l1 = sorted(list(years_after.keys()))
    l2 = [sum(years_after[i])/len(years_after[i]) for i in l1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=l1, y=l2, mode='lines+markers', name='Line Graph'))

    fig.update_layout(
        title=f'Average player performance after changing the league from {league_before} to {league_after}',
        xaxis_title='Years after changing the league',
        yaxis_title='Performance'
    )

    fig.show()

    #show_average_players_performance_after_changing_the_league('Serie A', 'Premier League')

def show_average_players_performance_after_changing_the_club(club_before): # Function to show average player performance after changing the club from club_before
    years_before = collections.defaultdict(list)
    years_after = collections.defaultdict(list)
    for player in players:
        clubs = []
        performance = []
        c1 = c2 = ''
        p1 = p2 = 0
        for season in players[player]:
            if len(players[player][season]['clubs'].keys()) == 1:
                if p1 and p2 and c1 and c2:
                    c = list(players[player][season]['clubs'].keys())[0]
                    if c == c1:
                        clubs.append(c2)
                        performance.append(p2)
                        clubs.append(c1)
                        performance.append(p1)
                    else:
                        clubs.append(c1)
                        performance.append(p1)
                        clubs.append(c2)
                        performance.append(p2)
                    c1 = c2 = ''
                    p1 = p2 = 0
                clubs.append(list(players[player][season]['clubs'].keys())[0])
                performance.append(list(players[player][season]['clubs'].values())[0])
            else:
                if c1 and c2 and p1 and p2:
                    lst = list(players[player][season]['clubs'].keys())
                    club1 = lst[0]
                    club2 = lst[1]
                    perf1 = players[player][season]['clubs'][club1]
                    perf2 = players[player][season]['clubs'][club2]
                    if c1 == club1 or c1 == club2:
                        clubs.append(c2)
                        performance.append(p2)
                        clubs.append(c1)
                        performance.append(p1)
                    else:
                        clubs.append(c1)
                        performance.append(p1)
                        clubs.append(c2)
                        performance.append(p2)
                    c1 = c2 = ''
                    p1 = p2 = 0
                lst = list(players[player][season]['clubs'].keys())
                club1 = lst[0]
                club2 = lst[1]
                perf1 = players[player][season]['clubs'][club1]
                perf2 = players[player][season]['clubs'][club2]
                if clubs and clubs[-1] == club1:
                    clubs.append(club1)
                    performance.append(perf1)
                    clubs.append(club2)
                    performance.append(perf2)
                elif clubs and clubs[-1] == club2:
                    clubs.append(club2)
                    performance.append(perf2)
                    clubs.append(club1)
                    performance.append(perf1)
                else:
                    c1 = club1
                    c2 = club2
                    p1 = perf1
                    p2 = perf2
        if c1 and c2 and p1 and p2:
            clubs.append(c1)
            performance.append(p1)
            clubs.append(c2)
            performance.append(p2)
        i = 0
        while i < len(clubs) - 1:
            if clubs[i] == club_before:
                j = i
                while j >= 0 and clubs[j] == club_before:
                    years_before[j - i - 1].append(performance[j])
                    j -= 1
                j = i + 1
                while j < len(clubs) and clubs[j] != club_before:
                    years_after[j - i].append(performance[j])
                    j += 1
                i = j
            else:
                i += 1
    l1 = sorted(list(years_before.keys()))
    l2 = [sum(years_before[i])/len(years_before[i]) for i in l1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=l1, y=l2, mode='lines+markers', name='Line Graph'))

    fig.update_layout(
        title=f'Average player performance before changing the club from {club_before}',
        xaxis_title='Years before changing the club',
        yaxis_title='Performance'
    )

    fig.show()

    l1 = sorted(list(years_after.keys()))
    l2 = [sum(years_after[i])/len(years_after[i]) for i in l1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=l1, y=l2, mode='lines+markers', name='Line Graph'))

    fig.update_layout(
        title=f'Average player performance after changing the club from {club_before}',
        xaxis_title='Years after changing the club',
        yaxis_title='Performance'
    )

    fig.show()

    # show_average_players_performance_after_changing_the_club('RCD Espanyol')
