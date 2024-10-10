import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import math

from tournament import Card, Player, Tournament

def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{:.1f}%\n({v:d})'.format(pct, v=val)
    return my_format

def scrape_tournament_data():
    print("Scraping tournament data")
    tournament_list_parsed = []

    url = 'https://limitlesstcg.com/tournaments/jp?page='

    #TODO Add initial and final date
    for i in range(1, 100):
        break_loop = False
        response = requests.get(url+str(i))
        soup = BeautifulSoup(response.text, 'html.parser')

        tournament_list = soup.find_all('table', class_='completed-tournaments')[0].find_all('tr')[1:]

        for tournament in tournament_list:
            date = tournament.attrs['data-date']
            player_list = tournament.find_all('td')[0].a.attrs['href']
            city = tournament.find_all('td')[1].a.text
            shop = tournament.find_all('td')[2].a.text
            if tournament.find_all('td')[3].a is not None:
                winner = tournament.find_all('td')[3].a.attrs['href']

            if date == '2024-10-05':
                break_loop = True
                break

            poke_deck = []
            for poke in tournament.find_all('td')[3].find_all('img'):
                poke_deck.append((poke.attrs['alt'], poke.attrs['src']))

            single_tournament = Tournament(date, city, shop, winner, poke_deck, player_list)
            tournament_list_parsed.append(single_tournament)

        if break_loop:
            break

    df = pd.DataFrame([vars(t) for t in tournament_list_parsed])
    df.to_csv('tournament_list.csv', index=True)

def scrape_tournament_players(dfTournament):
    print("Scraping players data")
    player_list_parsed = []
    for tournament in dfTournament.iterrows():
        tournament_id = tournament[1]
        tournament_url = tournament_id['player_list']
        response = requests.get(tournament_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        player_list = soup.find_all('table', class_='data-table')[0].find_all('tr')[1:]

        for player in player_list:
            rank = player.find_all('td')[0].text
            name = player.find_all('td')[1].text
            poke_deck = []
            for poke in player.find_all('td')[2].find_all('img'):
                poke_deck.append((poke.attrs['alt'], poke.attrs['src']))
            if (player.find_all('td')[2].a is not None):
                deck_list = player.find_all('td')[2].a.attrs['href']
            else:
                deck_list = None
            player = Player(tournament_id[0], rank, name, poke_deck, deck_list)
            player_list_parsed.append(player)

    df = pd.DataFrame([vars(t) for t in player_list_parsed])
    df.to_csv('player_list.csv', index=True)


def scrape_deck_list(dfPlayer):
    print("Scraping deck list")
    dfPlayer = dfPlayer.dropna(subset=['deck_list'])
    deck_list_parsed = []
    for player in dfPlayer.iterrows():
        player_id = player[1]
        pokes = player_id['pokes']
        if (player_id['deck_list'] is not None) and (player_id['deck_list'] != 'nan'):
            response = requests.get(player_id['deck_list'])
            soup = BeautifulSoup(response.text, 'html.parser')
            deck_list = soup.find_all('div', class_='decklist-column')
            for column in deck_list:
                cards = column.find_all('div', class_='decklist-card')
                for card in cards:
                    card_data = card.find_all('a')
                    card_count = card_data[0].find('span', class_='card-count').text
                    card_name = card_data[0].find('span', class_='card-name').text
                    card = Card(card_name, card_count, card.attrs['data-set'], card.attrs['data-number'], card.attrs['data-lang'], player_id['deck_list'], pokes)
                    deck_list_parsed.append(card)
    df = pd.DataFrame([vars(t) for t in deck_list_parsed])
    df = df.drop_duplicates()
    df.to_csv('deck_list.csv', index=True)


def generate_player_list():
    df = pd.read_csv('tournament_list.csv')
    scrape_tournament_players(df)

def generate_most_winning_decks():
    print('Generating most winning decks')

    plt.figure(1)
    threshold = 0.02
    tournament_data = pd.read_csv('tournament_list.csv')
    winning_decks = tournament_data['pokes'].value_counts()
    totals_df = winning_decks.groupby(['pokes']).sum()
    proportion = totals_df / totals_df.sum()
    below_thresh_mask = proportion < threshold
    plot_data = proportion[~below_thresh_mask]
    plot_data.loc['other'] = proportion[below_thresh_mask].sum()
    plt.pie(plot_data, labels=plot_data.index, autopct=autopct_format(totals_df))
    plt.title('Most Winning Decks')
    plt.tight_layout()
    plt.savefig('winning_decks.png', bbox_inches='tight')


def generate_most_played_decks():
    print('Generating most played decks')
    plt.figure(2)
    player_data = pd.read_csv('player_list.csv')
    threshold = 0.02
    played_decks = player_data['pokes'].value_counts()
    totals_df_played = played_decks.groupby(['pokes']).sum()
    proportion_played = totals_df_played / totals_df_played.sum()
    below_thresh_mask = proportion_played < threshold
    plot_data_played = proportion_played[~below_thresh_mask]
    plot_data_played.loc['other'] = proportion_played[below_thresh_mask].sum()
    plt.pie(plot_data_played, labels=plot_data_played.index, autopct=autopct_format(totals_df_played))
    plt.title('Most Played Decks')
    plt.tight_layout()
    plt.savefig('played_decks.png', bbox_inches='tight')

def generate_most_played_list():
    player_data = pd.read_csv('player_list.csv')
    scrape_deck_list(player_data)


def analyze_deck_structures():
    deck_list = pd.read_csv('deck_list.csv')
    played_decks = pd.read_csv('player_list.csv')
    used_decks = deck_list[['pokes','name','set','number']].value_counts()
    number_of_decks = played_decks['pokes'].value_counts()

    print(used_decks)

    print(number_of_decks)

    merged_df_decks_vs_list = number_of_decks.to_frame().merge(used_decks, on='pokes')
    print(merged_df_decks_vs_list.info())

    merged_df_decks_vs_list.rename(columns={'count_x': 'used_in_list', 'count_y': 'total_of_decks'}, inplace=True)

    merged_df_decks_vs_list['percentage'] = merged_df_decks_vs_list['used_in_list'] / merged_df_decks_vs_list['total_of_decks'] * 100

    print(merged_df_decks_vs_list.info())

def analyze_data():
    generate_most_played_list()
    generate_most_played_decks()
    generate_most_winning_decks()
    # print('Most Played Decks on top 16')
    # print(player_data['pokes'].value_counts())
    #analyze_deck_structures()

analyze_data()
#scrape_tournament_data()
#scrape_tournament_players('https://limitlesstcg.com/tournaments/jp/344')
#generate_player_list()
#generate_most_played_list()
#analyze_deck_structures()

