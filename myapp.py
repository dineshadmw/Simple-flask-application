from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

# Route to display all items in csv file
@app.route('/')
def index():
    players = []
    with open('players.csv', 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            players.append(row)
    return render_template('index.html', players=players)        


# Route to display details of each player
@app.route('/player/<int:player_id>')
def show(player_id):
    # Read data from csv file
    players = []
    with open('players.csv', 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            players.append(row)
    # Get player by id
    player = None
    for row in players:
        if int(row['player_id']) == player_id:
            player = row
            break
    return render_template('show.html', player=player)


# Route to create a new item (add new player)
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Get form data
        id = request.form['player_id']
        name = request.form['player_name']
        country = request.form['country']
        runs = request.form['runs']
        
        # Append new item to csv file
        with open('players.csv', 'a', newline='') as file:
            fieldnames = ['player_id', 'player_name', 'country', 'runs']
            
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({'player_id': id, 'player_name': name, 'country': country, 'runs': runs})
        return redirect(url_for('index'))
    return render_template('create.html')


# Route to edit/update player details
#Function to read player details from the csv file
def read_player_details():
    players = []
    try:
        with open('players.csv', 'r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                players.append(row)
        return players
    except FileNotFoundError as e:
        with open('players.csv', 'w', newline='') as file:
            return players

# Function to write/update new details to the csv file
def write_new_details(players):
    with open('players.csv', 'w', newline='') as file:
        fieldnames = ['player_id', 'player_name', 'country', 'runs']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for player in players:
            writer.writerow(player)

@app.route('/edit/<int:player_id>', methods=['GET', 'POST'])
def edit(player_id):
    players = read_player_details()
    player = players[player_id]
    
    if request.method == 'POST':
        name = request.form['player_name']
        country = request.form['country']
        runs = int(request.form['runs'])
        players[player_id] = {'player_id': player_id, 'player_name': name, 'country': country, 'runs': runs}
        write_new_details(players)
        return redirect('/')
    return render_template('edit.html', player=player, player_id=player_id)


if __name__ == '__main__':
    app.run(debug=True)






