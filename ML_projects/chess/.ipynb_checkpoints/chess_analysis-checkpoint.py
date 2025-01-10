import kagglehub
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

# +
# Download latest version
path = kagglehub.dataset_download("datasnaek/chess")

print("Path to dataset files:", path)
# -

path = os.path.join(path, os.listdir(path)[0])

chess_df = pd.read_csv(path)

print(chess_df.head())

print("number of rows " + str(len(chess_df)))
print("number of columns " + str(len(chess_df.columns)))
print(chess_df.columns)

print(chess_df.isna().sum())

chess_df.turns.value_counts()

# +
plt.figure(figsize=(10,4))

plt.hist(chess_df.turns)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel("Number of Turns")
plt.ylabel("Frequency")
plt.title("Number Of Turns In A Chess Game")
plt.axvline(chess_df.turns.mean(), color = 'r')
plt.show()
# -

chess_df.victory_status.value_counts()

# +
plt.figure(figsize=(10,4))

plt.hist(chess_df.victory_status)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel("Method of Victory")
plt.ylabel("Frequency")
plt.title("Method of Victory In A Chess Game")
plt.show()
# -

chess_df.opening_name.value_counts()

openings = chess_df.opening_name.value_counts()
top_openings = openings[openings>75]
plt.figure(figsize=(12,10))
plt.barh(top_openings.index, top_openings.values)
plt.gca().invert_yaxis() 
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.xlabel("Frequency")
plt.ylabel("Opening Name")
plt.title("Frequency of Openings")
plt.show()

# +
# Get top 10 openings
top_10_openings = list(openings[:10].index)

# Filter the DataFrame for these openings
top_10_openings_df = chess_df[chess_df.opening_name.isin(top_10_openings)]

# Group by opening_name and winner, then count
top_10_openings_result = top_10_openings_df.groupby(["opening_name", "winner"]).size().unstack(fill_value=0)

# Plot grouped bar chart
ax = top_10_openings_result.plot(kind="bar", figsize=(12, 6), width=0.8)

# Customize the plot
plt.title("Win Counts for Top 10 Openings by Result")
plt.xlabel("Opening Name")
plt.ylabel("Number of Wins")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Result", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

# Show the plot
plt.show()


# +
grouped = top_10_openings_df.groupby(["opening_name", "winner"]).size()
totals = top_10_openings_df.groupby("opening_name").size()
percentages = grouped / totals * 100
percentages = percentages.unstack()

ax = percentages.plot(kind="bar", figsize=(12, 6), width=0.8)

# Customize the plot
plt.title("Win Counts for Top 10 Openings by Result")
plt.xlabel("Opening Name")
plt.ylabel("Percentage")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Result", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

# Show the plot
plt.show()
# -

chess_df.winner.value_counts()

# +
plt.figure(figsize=(10,4))


plt.hist(chess_df.winner)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel("Winner")
plt.ylabel("Frequency")
plt.title("Winner In A Chess Game")
plt.show()
# -

elo_diff = chess_df.white_rating - chess_df.black_rating
print(elo_diff.mean())
# white is approx 8 points higher than black

white_win = chess_df[chess_df.winner == "white"]
elo_diff = white_win.white_rating - white_win.black_rating
print(elo_diff.mean())

black_win = chess_df[chess_df.winner == "black"]
elo_diff = black_win.white_rating - black_win.black_rating
print(elo_diff.mean())

draw = chess_df[chess_df.winner == "draw"]
elo_diff = draw.white_rating - draw.black_rating
print(elo_diff.mean())

# +
chess_df["elo_diff"] = chess_df.white_rating - chess_df.black_rating

bins = range(-1000, 1000, 100)  # Bin size of 100 Elo
chess_df['elo_diff_bin'] = pd.cut(chess_df['elo_diff'], bins)

# Step 3: Calculate win proportions
win_probs = chess_df.groupby('elo_diff_bin')['winner'].value_counts(normalize=True).unstack()

# Get probabilities of White and Black wins
win_probs_white = win_probs.get('white', 0)
win_probs_black = win_probs.get('black', 0)

# Calculate midpoints of bins
bin_midpoints = [interval.mid for interval in win_probs.index]

# Step 4: Plot the results
plt.figure(figsize=(10, 6))
plt.plot(bin_midpoints, win_probs_white, label="White Win Probability", color="blue")
plt.plot(bin_midpoints, win_probs_black, label="Black Win Probability", color="red")
plt.axhline(y=0.5, color='gray', linestyle='--', label='50% Win Rate')
plt.title("Win Probabilities vs Rating Difference")
plt.xlabel("Rating Difference (White - Black)")
plt.ylabel("Win Probability")
plt.legend()
plt.grid()
plt.show()
# -

underdog_win = chess_df[((chess_df.elo_diff > 0) & (chess_df.winner=="black")) | ((chess_df.elo_diff) < 0 & (chess_df.winner=="white"))]
plt.figure(figsize=(10, 6))
plt.hist(underdog_win.elo_diff, bins = 20, color = "Orange")
plt.title("Distribution of Rating Differences in Upsets")
plt.xlabel("Difference in Rating")
plt.ylabel("Frequency")
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(chess_df.elo_diff, bins = 20, color= "Blue", alpha = 0.5, label = "All Games")
plt.hist(underdog_win.elo_diff, bins = 20, color = "Orange", alpha = 0.7, label = "Upsets")
plt.title("Distribution of Rating Differences in Upsets")
plt.xlabel("Difference in Rating")
plt.ylabel("Frequency")
plt.legend()
plt.show()

chess_df.increment_code.value_counts()

# +
plt.figure(figsize=(10,4))

time_control = chess_df.increment_code.value_counts()
time_control = time_control[time_control>500]

plt.bar(time_control.index, time_control.values)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel("Time Control")
plt.ylabel("Frequency")
plt.title("Time Control In A Chess Game")
plt.show()


# -

def time_control(time):
    time = int(time[0])
    if time <= 2:
        return "Bullet"
    elif 3 <= time < 10:
        return "Bltiz"
    elif 10 <= time <= 60:
        return "Rapid"
    else: 
        return "Classical"


chess_df["time_control"] = chess_df["increment_code"].str.split("+").apply(time_control)

chess_df.time_control.value_counts()

# +
plt.figure(figsize=(10,4))

time_control = chess_df.time_control.value_counts()

plt.bar(time_control.index, time_control.values)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel("Time Control")
plt.ylabel("Frequency")
plt.title("Time Control In A Chess Game")
plt.show()

# +
# Win rates grouped by time control
win_rates = chess_df.groupby(["time_control", "winner"]).size().unstack()
win_rates["White Win Rate"] = win_rates["white"] / win_rates.sum(axis=1)
win_rates["Black Win Rate"] = win_rates["black"] / win_rates.sum(axis=1)

# Chi-squared test
from scipy.stats import chi2_contingency

contingency_table = chess_df["winner"].value_counts()
chi2, p_value, _, _ = chi2_contingency([contingency_table])
print(f"Chi-squared Test: p-value = {p_value}")

# Bar chart for win rates by time control
win_rates[["White Win Rate", "Black Win Rate"]].plot(kind="bar", figsize=(10, 6), color=["blue", "orange"])
plt.title("White vs. Black Win Rates by Time Control")
plt.xlabel("Time Control")
plt.ylabel("Win Rate")
plt.legend()
plt.show()


# +
def first_white_move(moves):
    return moves[0]

def first_black_move(moves):
    if len(moves) == 1:
        return "NA"
    return moves[1]


# -

chess_df["first_white_move"] = chess_df.moves.str.split().apply(first_white_move)
chess_df["first_black_move"] = chess_df.moves.str.split().apply(first_black_move)

chess_df.first_white_move.value_counts()

len(chess_df.first_white_move.value_counts())

# +
plt.figure(figsize=(10,4))

first_white_move = chess_df.first_white_move.value_counts()
first_white_move = first_white_move[first_white_move > 100]
plt.bar(first_white_move.index, first_white_move.values)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel("First White Move")
plt.ylabel("Frequency")
plt.title("First White Move In A Chess Game")
plt.show()
# -

chess_df.first_black_move.value_counts()

len(chess_df.first_black_move.value_counts())

# +
plt.figure(figsize=(10,4))

first_black_move = chess_df.first_black_move.value_counts()
first_black_move = first_black_move[first_black_move > 100]
plt.bar(first_black_move.index, first_black_move.values)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel("First Black Move")
plt.ylabel("Frequency")
plt.title("First Black Move In A Chess Game")
plt.show()

# +
plt.figure(figsize=(10,4))

first_white_move = chess_df.first_white_move.value_counts()
first_white_move = first_white_move[:5]
plt.bar(first_white_move.index, first_white_move.values)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel("First White Move")
plt.ylabel("Frequency")
plt.title("Top 5 White Moves In A Chess Game")
plt.show()
# -

top_five_white_moves_df = chess_df[chess_df.first_white_move.isin(["e4", "d4", "Nf3", "c4", "e3"])]

# +
top_five_white_moves = ["e4", "d4", "Nf3", "c4", "e3"]

for move in top_five_white_moves:
    
    plt.figure(figsize=(10,4))

    first_black_move = top_five_white_moves_df[top_five_white_moves_df.first_white_move == move]
    first_black_move = first_black_move.first_black_move.value_counts()[:5]

    plt.bar(first_black_move.index, first_black_move.values)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlabel("First Black Move")
    plt.ylabel("Frequency")
    plt.title(f"Top 5 Black Responses to {move} In A Chess Game")
    plt.show()  


# -
def estimate_duration(row):
    if row.last_move_at == row.created_at:
        start, bonus = row.increment_code.split("+")
        return 2*(int(start)*60 + int(bonus) * row.turns/2)/60
    else:
        return (row.last_move_at - row.created_at)/60


chess_df['game_duration'] = chess_df.apply(estimate_duration, axis=1)

# +
time_controls = list(chess_df.time_control.unique())

for tc in time_controls:
    plt.figure()
    
    plt.hist(chess_df[chess_df.time_control == tc].game_duration, bins = 20)
    plt.title(f"Game Length for {tc} Games")
    plt.xlabel("Minutes")
    plt.ylabel("Frequency")
    plt.show()
# -

plt.figure(figsize=(12, 6))
sns.boxplot(x="time_control", y = "game_duration", data = chess_df)
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x="time_control", y = "game_duration", data = chess_df[chess_df.game_duration < 8000])
plt.title("Boxplot of Game Lengths by Time Control", fontsize=14)
plt.xlabel("Time Control (time_control)", fontsize=12)
plt.ylabel("Game Duration (minutes)", fontsize=12)
plt.show()

# +
vs_tc = chess_df.groupby(["time_control", "victory_status"]).size().unstack()
bar_positions = range(len(vs_tc.columns))

fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(bar_positions, vs_tc["draw"], label = "draw")
ax.bar(bar_positions, vs_tc["mate"], bottom = vs_tc["draw"], label = "mate")
ax.bar(bar_positions, vs_tc["outoftime"], bottom = vs_tc["draw"] + vs_tc["mate"], label = "out of time")
ax.bar(bar_positions, vs_tc["resign"], bottom = vs_tc["draw"] + vs_tc["mate"] +vs_tc["outoftime"], label = "resign")
plt.legend()

ax.set_xticks(bar_positions)
ax.set_xticklabels(["Blitz", "Bullet", "Classical", "Rapid"])
plt.title("Victory Method v. Time Control")
plt.xlabel("Time Control")
plt.ylabel("Frequency")
plt.show()

# +
vs_tc_proportions = vs_tc.div(vs_tc.sum(axis=1), axis=0)
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(bar_positions, vs_tc_proportions["draw"], label = "draw")
ax.bar(bar_positions, vs_tc_proportions["mate"], bottom = vs_tc_proportions["draw"], label = "mate")
ax.bar(bar_positions, vs_tc_proportions["outoftime"], bottom = vs_tc_proportions["draw"] + vs_tc_proportions["mate"], label = "out of time")
ax.bar(bar_positions, vs_tc_proportions["resign"], bottom = vs_tc_proportions["draw"] + vs_tc_proportions["mate"] +vs_tc_proportions["outoftime"], label = "resign")
plt.legend()

ax.set_xticks(bar_positions)
ax.set_xticklabels(["Blitz", "Bullet", "Classical", "Rapid"])
plt.title("Victory Method v. Time Control")
plt.xlabel("Time Control")
plt.ylabel("Proportion")
plt.show()

# +
from stockfish import Stockfish
import chess 



def fen_board(moves):
    board = chess.Board()

    for move in moves:
        board.push_san(move) 
    return board.fen()

def stockfish_eval(fen):
    stockfish_path = r"C:\Users\emmet\OneDrive\Desktop\stockfish\stockfish-windows-x86-64-avx2.exe"
    stockfish = Stockfish(stockfish_path)
    stockfish.update_engine_parameters({"Threads": 2, "Minimum Thinking Time": 30})
    stockfish.set_depth(20)
    stockfish.set_fen_position(fen)
    return stockfish.get_evaluation()

