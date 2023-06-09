# First we import the endpoint
# We will be using pandas dataframes to manipulate the data
from nba_api.stats.endpoints import cumestatsteamgames, boxscoretraditionalv2, hustlestatsboxscore, boxscoreadvancedv2, boxscoresummaryv2, playerestimatedmetrics, playergamelog
from nba_api.stats.static import teams
from requests.exceptions import ReadTimeout
import json
import pandas as pd 
import json

from datetime import datetime
from csv import writer
from csv import DictWriter

nba_teams = teams.get_teams()
TEAMS = {}
for team in nba_teams: 
    TEAMS[team["id"]] = team["abbreviation"]
TEAM_STATS = {}
TEAM_RECENT = {}
def init_teams():
    for id in TEAMS.keys():
        TEAM_STATS[id] = {'OFF_RATING' : 0, 'DEF_RATING' : 0, 'NET_RATING' : 0, 'AST_PCT' : 0, "AST_TOV" : 0, 'AST_RATIO' : 0, 
                        'OREB_PCT' : 0, 'DREB_PCT' : 0, 'REB_PCT' : 0, 'TM_TOV_PCT' : 0, 'EFG_PCT' : 0, 'TS_PCT' : 0,
                        "PACE" : 0, 'POSS': 0, 'PIE' : 0, 'FGM' : 0, 'FG_PCT' : 0, 'FG3M' : 0, 'FG3_PCT' : 0,
                        'FTM' : 0, 'FT_PCT' : 0, 'BLK' : 0, 'AVG_PTS' : 0, "CONTEST_SHOT" : 0, "CHARGES" : 0, "SCREEN_AST" : 0,
                        'LOOSE_BALL' : 0, "BOX_OUT" : 0,  "DAYS" : 0, "INJ" : 0,
                        'GP' : 0, 'PTS' : 0, "H/A" : None, 'DATE' : None
                            }
        TEAM_RECENT[id] = {'OFF_RATING' : [0,0,0,0,0,0,0,0,0,0], 'DEF_RATING' : [0,0,0,0,0,0,0,0,0,0], 'NET_RATING' : [0,0,0,0,0,0,0,0,0,0], 'AST_PCT' : [0,0,0,0,0,0,0,0,0,0], "AST_TOV" : [0,0,0,0,0,0,0,0,0,0], 'AST_RATIO' : [0,0,0,0,0,0,0,0,0,0], 
                        'OREB_PCT' : [0,0,0,0,0,0,0,0,0,0], 'DREB_PCT' : [0,0,0,0,0,0,0,0,0,0], 'REB_PCT' : [0,0,0,0,0,0,0,0,0,0], 'TM_TOV_PCT' : [0,0,0,0,0,0,0,0,0,0], 'EFG_PCT' : [0,0,0,0,0,0,0,0,0,0], 'TS_PCT' : [0,0,0,0,0,0,0,0,0,0],
                        "PACE" : [0,0,0,0,0,0,0,0,0,0], 'POSS': [0,0,0,0,0,0,0,0,0,0], 'PIE' : [0,0,0,0,0,0,0,0,0,0], 'FGM' : [0,0,0,0,0,0,0,0,0,0], 'FG_PCT' : [0,0,0,0,0,0,0,0,0,0], 'FG3M' : [0,0,0,0,0,0,0,0,0,0], 'FG3_PCT' : [0,0,0,0,0,0,0,0,0,0],
                        'FTM' : [0,0,0,0,0,0,0,0,0,0], 'FT_PCT' : [0,0,0,0,0,0,0,0,0,0], 'BLK' : [0,0,0,0,0,0,0,0,0,0], 'AVG_PTS' : [0,0,0,0,0,0,0,0,0,0], "CONTEST_SHOT" : [0,0,0,0,0,0,0,0,0,0], "CHARGES" : [0,0,0,0,0,0,0,0,0,0], "SCREEN_AST" : [0,0,0,0,0,0,0,0,0,0],
                        'LOOSE_BALL' : [0,0,0,0,0,0,0,0,0,0], "BOX_OUT" : [0,0,0,0,0,0,0,0,0,0],  
                        'GP' : 0, 'PTS' : [0,0,0,0,0,0,0,0,0,0]
                            }

def b2b(team1, date2):
    date2 = date2[4]['rowSet'][0][0]
    date2 = date2[date2.find(','):]
    date2 = (date2[2:])
    date_object2 = datetime.strptime(date2, "%B %d, %Y")
    date_object1 = TEAM_STATS[team1[1]]['DATE']
    if(date_object1) == None:
        TEAM_STATS[team1[1]]['DATE'] = date_object2
        return
    days = abs((date_object2 - date_object1).days)
    TEAM_STATS[team1[1]]['DATE'] = date_object2
    TEAM_STATS[team1[1]]['DAYS'] = days

#is called after every game to update the teams stats that played 
#FOR SECOND DATABASE instead of updateing, keep asecond TEAM_STATS{} but instead of values as ints values are lists that store 10 most recent games stats, then
#use MOD to figure out which index to swap for the most recent game
def update_recent(team1, trad1, hust1):
    GP = TEAM_RECENT[team1[1]]['GP']
    '''
    {'OFF_RATING' : 0, 'DEF_RATING' : 0, 'NET_RATING' : 0, 'AST_PCT' : 0, "AST_TOV" : 0, 'AST_RATIO' : 0, 
                      'OREB_PCT' : 0, 'DREB_PCT' : 0, 'REB_PCT' : 0, 'TM_TOV_PCT' : 0, 'EFG_PCT' : 0, 'TS_PCT' : 0,
                       "PACE" : 0, 'POSS': 0, 'PIE' : 0, 'FGM' : 0, 'FG_PCT' : 0, 'FG3M' : 0, 'FG3_PCT' : 0,
                      'FTM' : 0, 'FT_PCT' : 0, 'BLK' : 0, 'AVG_PTS' : 0, "CONTEST_SHOT" : 0, "CHARGES" : 0, "SCREEN_AST" : 0,
                      'LOOSE_BALL' : 0, "BOX_OUT" : 0,  
                      'GP' : 0, 'PTS' : 0, "H/A" : None, "INJ" : 0
                        }'''
    
    
    TEAM_RECENT[team1[1]]['OFF_RATING'][GP%10] = team1[7]
    TEAM_RECENT[team1[1]]['DEF_RATING'][GP%10]  = team1[9]
    TEAM_RECENT[team1[1]]['NET_RATING'][GP%10]  = team1[11]
    TEAM_RECENT[team1[1]]['AST_PCT'][GP%10]  = team1[12]
    TEAM_RECENT[team1[1]]['AST_TOV'][GP%10]  = team1[13]
    TEAM_RECENT[team1[1]]['AST_RATIO'][GP%10]  = team1[14]
    TEAM_RECENT[team1[1]]['OREB_PCT'][GP%10]  = team1[15]
    TEAM_RECENT[team1[1]]['DREB_PCT'][GP%10]  = team1[16]
    TEAM_RECENT[team1[1]]['REB_PCT'][GP%10]  = team1[17]
    TEAM_RECENT[team1[1]]['TM_TOV_PCT'][GP%10]  = team1[19]
    TEAM_RECENT[team1[1]]['EFG_PCT'][GP%10]  = team1[20]
    TEAM_RECENT[team1[1]]['TS_PCT'][GP%10]  = team1[21]
    TEAM_RECENT[team1[1]]['PACE'][GP%10]  = team1[25]
    TEAM_RECENT[team1[1]]['POSS'][GP%10]  = team1[27]
    TEAM_RECENT[team1[1]]['PIE'][GP%10]  = team1[28]

    TEAM_RECENT[trad1[1]]['FGM'][GP%10]  = trad1[6]
    TEAM_RECENT[trad1[1]]['FG_PCT'][GP%10]  = trad1[8]
    TEAM_RECENT[trad1[1]]['FG3M'][GP%10]  = trad1[9]
    TEAM_RECENT[trad1[1]]['FG3_PCT'][GP%10]  = trad1[11]
    TEAM_RECENT[trad1[1]]['FTM'][GP%10]  = trad1[12]
    TEAM_RECENT[trad1[1]]['FT_PCT'][GP%10]  = trad1[14]
    TEAM_RECENT[trad1[1]]['BLK'][GP%10]  = trad1[20]
    TEAM_RECENT[trad1[1]]['AVG_PTS'][GP%10]  = trad1[23]

    TEAM_RECENT[hust1[1]]['CONTEST_SHOT'][GP%10] = hust1[7]
    TEAM_RECENT[hust1[1]]['CHARGES'][GP%10]  = hust1[11]
    TEAM_RECENT[hust1[1]]['SCREEN_AST'][GP%10]  = hust1[12]
    TEAM_RECENT[hust1[1]]['LOOSE_BALL'][GP%10]  = hust1[16]
    TEAM_RECENT[hust1[1]]['BOX_OUT'][GP%10]  = hust1[21]

    TEAM_RECENT[team1[1]]['GP'] += 1
    print(TEAM_RECENT[team1[1]])
def update_stats(team1, trad1, hust1):
    GP = TEAM_STATS[team1[1]]['GP']
    
    TEAM_STATS[team1[1]]['OFF_RATING'] = sum(TEAM_RECENT[team1[1]]['OFF_RATING'])/10
    TEAM_STATS[team1[1]]['DEF_RATING'] = sum(TEAM_RECENT[team1[1]]['DEF_RATING'])/10
    TEAM_STATS[team1[1]]['NET_RATING'] = sum(TEAM_RECENT[team1[1]]['NET_RATING'])/10
    TEAM_STATS[team1[1]]['AST_PCT'] = sum(TEAM_RECENT[team1[1]]['AST_PCT'])/10
    TEAM_STATS[team1[1]]['AST_TOV'] = sum(TEAM_RECENT[team1[1]]['AST_TOV'])/10
    TEAM_STATS[team1[1]]['AST_RATIO'] = sum(TEAM_RECENT[team1[1]]['AST_RATIO'])/10
    TEAM_STATS[team1[1]]['OREB_PCT'] = sum(TEAM_RECENT[team1[1]]['OREB_PCT'])/10
    TEAM_STATS[team1[1]]['DREB_PCT'] = sum(TEAM_RECENT[team1[1]]['DREB_PCT'])/10
    TEAM_STATS[team1[1]]['REB_PCT'] = sum(TEAM_RECENT[team1[1]]['REB_PCT'])/10
    TEAM_STATS[team1[1]]['TM_TOV_PCT'] = sum(TEAM_RECENT[team1[1]]['TM_TOV_PCT'])/10
    TEAM_STATS[team1[1]]['EFG_PCT'] = sum(TEAM_RECENT[team1[1]]['EFG_PCT'])/10
    TEAM_STATS[team1[1]]['TS_PCT'] = sum(TEAM_RECENT[team1[1]]['TS_PCT'])/10
    TEAM_STATS[team1[1]]['PACE'] = sum(TEAM_RECENT[team1[1]]['PACE'])/10
    TEAM_STATS[team1[1]]['POSS'] = sum(TEAM_RECENT[team1[1]]['POSS'])/10
    TEAM_STATS[team1[1]]['PIE'] = sum(TEAM_RECENT[team1[1]]['PIE'])/10

    TEAM_STATS[trad1[1]]['FGM'] = sum(TEAM_RECENT[trad1[1]]['FGM'])/10
    TEAM_STATS[trad1[1]]['FG_PCT'] = sum(TEAM_RECENT[trad1[1]]['FG_PCT'])/10
    TEAM_STATS[trad1[1]]['FG3M'] = sum(TEAM_RECENT[trad1[1]]['FG3M'])/10
    TEAM_STATS[trad1[1]]['FG3_PCT'] = sum(TEAM_RECENT[trad1[1]]['FG3_PCT'])/10
    TEAM_STATS[trad1[1]]['FTM'] = sum(TEAM_RECENT[trad1[1]]['FTM'])/10
    TEAM_STATS[trad1[1]]['FT_PCT'] = sum(TEAM_RECENT[trad1[1]]['FT_PCT'])/10
    TEAM_STATS[trad1[1]]['BLK'] = sum(TEAM_RECENT[trad1[1]]['BLK'])/10
    TEAM_STATS[trad1[1]]['AVG_PTS'] = sum(TEAM_RECENT[trad1[1]]['AVG_PTS'])/10

    TEAM_STATS[hust1[1]]['CONTEST_SHOT'] = sum(TEAM_RECENT[hust1[1]]['CONTEST_SHOT'])/10
    TEAM_STATS[hust1[1]]['CHARGES'] = sum(TEAM_RECENT[hust1[1]]['CHARGES'])/10
    TEAM_STATS[hust1[1]]['SCREEN_AST'] = sum(TEAM_RECENT[hust1[1]]['SCREEN_AST'])/10
    TEAM_STATS[hust1[1]]['LOOSE_BALL'] = sum(TEAM_RECENT[hust1[1]]['LOOSE_BALL'])/10
    TEAM_STATS[hust1[1]]['BOX_OUT'] = sum(TEAM_RECENT[hust1[1]]['BOX_OUT'])/10

    TEAM_STATS[team1[1]]['INJ'] = 0
    TEAM_STATS[team1[1]]['GP'] += 1
    print(TEAM_STATS[team1[1]])
'''
with open("data.csv", mode = "w") as csvfile:
    t1 = list(TEAM_STATS[1610612740].keys())
    del t1[-1]
    FieldNames = ['OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_PCT', 'AST_TOV', 'AST_RATIO', 'OREB_PCT', 'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT', 'PACE', 'POSS', 'PIE', 'FGM', 'FG_PCT', 'FG3M', 'FG3_PCT', 'FTM', 'FT_PCT', 'BLK', 'AVG_PTS', 'CONTEST_SHOT', 'CHARGES', 'SCREEN_AST', 'LOOSE_BALL', 'BOX_OUT', 'DAYS', 'INJ', 'GP', 'PTS', 'H/A']+['OPP_OFF_RATING', 'OPP_DEF_RATING', 'OPP_NET_RATING', 'OPP_AST_PCT', 'OPP_AST_TOV', 'OPP_AST_RATIO', 'OPP_OREB_PCT', 'OPP_DREB_PCT', 'OPP_REB_PCT', 'OPP_TM_TOV_PCT', 'OPP_EFG_PCT', 'OPP_TS_PCT', 'OPP_PACE', 'OPP_POSS', 'OPP_PIE', 'OPP_FGM', 'OPP_FG_PCT', 'OPP_FG3M', 'OPP_FG3_PCT', 'OPP_FTM', 'OPP_FT_PCT', 'OPP_BLK', 'OPP_AVG_PTS', 'OPP_CONTEST_SHOT', 'OPP_CHARGES', 'OPP_SCREEN_AST', 'OPP_LOOSE_BALL', 'OPP_BOX_OUT', 'OPP_DAYS', 'OPP_INJ', 'OPP_GP', 'OPP_PTS', 'OPP_H/A']

    dw = DictWriter(csvfile, delimiter=',', 
                        fieldnames=FieldNames)
    dw.writeheader()
    csvfile.close()
'''

SEASONS = ["2017", "2018", "2019", "2020", "2021", "2022"]
all_games = {"2017":[], "2018":[], "2019":[], "2020":[], "2021":[], "2022":[]}

#is used to populate json file with key = season and values of each season being an array of game_ids
game_file = "game2.json"
def getSeasonGames():
    for Season in SEASONS:
        for idx, id in enumerate(TEAMS.keys()):
            holder = idx
            while holder == idx:
                try:
                    print(TEAMS[id])
                    i = 0
                    temp = cumestatsteamgames.CumeStatsTeamGames(season = Season, team_id = id)
                    team = temp.get_dict()["resultSets"][0]["rowSet"]
                    for game in team:
                        i += 1
                        if game[1] not in all_games[Season]:
                            all_games[Season].append(game[1])
                    print(i, "done")
                    holder += 1
                except ReadTimeout:
                    print(all_games)
                    with open(game_file, "w") as outfile:
                        json.dump(all_games, outfile)
            print(len(all_games[Season]))
    for item in all_games.keys():
        all_games[item].sort()
    with open(game_file, "w") as outfile:
        json.dump(all_games, outfile)
    return all_games

player_seasons = ["2016-17", "2017-18", "2018-19", "2019-20", "2020-21", "2021-22"]
all_players = {"2017":{}, "2018":{}, "2019":{}, "2020":{}, "2021":{}, "2022":{}}
#write to a json where every key is a season and every value is a dict where each key is a player id and the value is [avg min played, net rating]
#creates a dict where the keys are seasons and the value is a dict where the keys are player ids and the values are {'MIN': 0, 'NET': 0, 'GP': 0}
def player_stats():
    for idx, seasons in enumerate(player_seasons):
        players = playerestimatedmetrics.PlayerEstimatedMetrics(season = seasons).get_dict()['resultSet']['rowSet']
        print(players)
        for player in players:
            curr_season = list(all_players.keys())
            all_players[curr_season[idx]][player[0]] = [player[6], player[9]]
    
    with open("players_v2.json", "w") as outfile:
        json.dump(all_players, outfile)
    

f = open('database/games.json')
g = open('database/players_v2.json')
data = json.load(f) #data is all games
pdata = json.load(g) #pdata is all players

def get_all_stats():
    #season is a list of all games in that season
    #change [1:] to get diff season
    init_teams()
    for i, season in enumerate(list(data.values())):
        print(season)
        #game is game_id
        for idx, game in enumerate(season):
            holder = idx
            while holder == idx:
                try:
                    print(holder)
                    curr_game = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id = game).get_dict()['resultSets'][1]
                    team1 = curr_game["rowSet"][0]
                    team2 = curr_game["rowSet"][1]

                    traditional_game = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id = game).get_dict()['resultSets'][1]['rowSet']
                    trad1 = traditional_game[0]
                    trad2 = traditional_game[1]
                    #write to excel the old teams stats and trad1[23] trad2[23]

                    hustle = hustlestatsboxscore.HustleStatsBoxScore(game_id = game).get_dict()['resultSets'][2]['rowSet']
                    hust1 = hustle[0]
                    hust2 = hustle[1]
                    inactive = boxscoresummaryv2.BoxScoreSummaryV2(game_id = game).get_dict()['resultSets']
                    #non additive stats
                    
                    TEAM_STATS[trad1[1]]['PTS'] = trad1[23]
                    TEAM_STATS[trad2[1]]['PTS'] = trad2[23]
                    #1 = home
                    TEAM_STATS[inactive[0]['rowSet'][0][6]]['H/A'] = "1"
                    #0 = away
                    TEAM_STATS[inactive[0]['rowSet'][0][7]]['H/A'] = "0"
                    b2b(team1, inactive)
                    b2b(team2, inactive)
                    
                    #This checks for inactive players min and if abover thershold then adds their net rating
                    THRESHOLD = 12
                    year = list(data.keys())[i]
                    #player looks like [1628444, 'Jabari', 'Bird', '26', 1610612738, 'Boston', 'Celtics', 'BOS']           
                    for j, player in enumerate(inactive[3]['rowSet']):                        
                        idv = inactive[3]['rowSet'][j]
                        try:
                            stats = pdata[year][str(idv[0])]
                            if stats[0] > THRESHOLD:
                                TEAM_STATS[idv[4]]["INJ"] += stats[1]
                        except:
                            stats = pdata[year].get(str(idv[0]), [0])
                            if stats[0] > THRESHOLD:
                                TEAM_STATS[idv[4]]["INJ"] += stats[1]
                    #write to csv
                    if TEAM_STATS[team1[1]]['GP'] >= 10 and TEAM_STATS[team2[1]]['GP'] >= 10:
                        with open("data.csv", mode = "a") as csvfile:
                            writer_object = writer(csvfile)
                            t1 = list(TEAM_STATS[team1[1]].values())
                            del t1[-1]
                            t2 = list(TEAM_STATS[team2[1]].values())
                            del t2[-1]
                            print(t1)
                            writer_object.writerow(t1 + t2)
                            writer_object.writerow(t2 + t1)
                            csvfile.close()
                    #update TEAMSTATS dict
                    update_recent(team1, trad1, hust1)
                    update_recent(team2, team2, team2)
                    update_stats(team1, trad1, hust1)
                    update_stats(team2, team2, team2)
                    holder += 1
                    #print(TEAM_STATS)

                except ReadTimeout:
                    pass
        print(season)
        return(season)
get_all_stats()
#ex, get the players who inactive and total their counting stats or advanced stats or something
#days since last played

'''pd.set_option('display.max_rows', None, 'display.max_columns', None)
df = pd.read_csv("data.csv")
print(df)'''
