import os
from dotenv import load_dotenv
import requests
import pandas as pd
import tempfile
import psycopg2
from itertools import chain
load_dotenv()



def ask_connection():
    CONN_STRING = os.getenv("PSYCOPG2_CONN_STRING")
    return psycopg2.connect(CONN_STRING)

def read_sql_tmpfile(query):
    conn = ask_connection()
    with tempfile.TemporaryFile() as tmpfile:
        copy_sql = "COPY ({query}) TO STDOUT WITH CSV {head}".format(
           query=query, head="HEADER"
        )
        cur = conn.cursor()
        cur.copy_expert(copy_sql, tmpfile)
        tmpfile.seek(0)
        df = pd.read_csv(tmpfile)
        return df
def get_all_games(player_name, time_control):
    if time_control:
        time_control = f"and game.time_control='{time_control}'"
    else:
        time_control = ''
    data = read_sql_tmpfile(
    f"""
    SELECT * FROM game
    WHere (game.black='{player_name}' 
    OR game.white='{player_name}')
    {time_control}
    ORDER BY game.year, game.month, game.day
    """)
    return data

def get_games_where(player_name, result, color, time_control):
    if time_control:
        time_control = f"and game.time_control='{time_control}'"
    else:
        time_control = ''
    data = read_sql_tmpfile(
            f"""
            SELECT * FROM game
            WHere game.{color}='{player_name}' and game.{color}_result={result}
            {time_control}
            ORDER BY game.year, game.month, game.day
            """)
    return data
def color_results(player_name, color):
    color_result = dict()
    conn = ask_connection()
    with conn.cursor() as curs:
        curs.execute(
        f"""
        select game.{color}_result,  COUNT(*) as how_many
        FROM game
        where game.{color}='{player_name}'
        group by game.{color}_result
        ORDER BY how_many DESC
        """

        )
        result = curs.fetchall()
    color_result['win']  = [x[1] for x in result if x[0] == 1.0][0]
    color_result['lose'] = [x[1] for x in result if x[0] == 0.0][0]
    color_result['draw'] = [x[1] for x in result if x[0] == 0.5][0]
    return color_result
def get_win_draw_lose(player_name):
    black = color_results(player_name, 'black')
    white = color_results(player_name, 'white')
    data = pd.DataFrame( columns = ['win','draw','lose'], index=['white','black'])
    data.loc['white'] = pd.Series({'win':white['win'], 'draw':white['draw'], 'lose':white['lose']})
    data.loc['black'] = pd.Series({'win':black['win'], 'draw':black['draw'], 'lose':black['lose']})
    data.loc['total'] = pd.Series({'win': white['win'] + black['win'], 'draw':white['draw']+black['draw'], 'lose':white['lose']+black['lose']})
    return data