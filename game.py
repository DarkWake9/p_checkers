import tkinter as tk
import numpy as np
import pandas as pd

connections_txt = pd.read_csv('connections.txt', sep='\t', header=None, index_col=0)
connections_txt

connections = np.zeros([36, 36])
occupied = connections_txt[1].values
for from_point in range(1, 37):
    connected_points = [int(i) for i in connections_txt[2][from_point].split(',')]
    for to_point in connected_points:
        connections[from_point-1, to_point-1] = 1

# The player rolls his dice chooses the origin point by clicking on one of his 11 occupied points
# Highlight all the unoccupied points that are connected to the origin point by the same number of lines as the dice roll
# All the points on any given point must be different
# The player chooses the destination point by clicking on one of the highlighted points
# The player moves to the destination point

# import tkinter as tk
# import random

# # Create a random 36x36 connection matrix for demonstration
# # Here, we'll use a symmetric matrix with 0s and 1s
# import numpy as np

# np.random.seed(0)  # For reproducible random results
# connection_matrix = np.random.choice([0, 1], size=(N, N))
# # Make the matrix symmetric to represent undirected graph
# connection_matrix = np.triu(connection_matrix, 1)
# connection_matrix += connection_matrix.T


import tkinter as tk
import random
from tkinter import messagebox

# Constants
GRID_SIZE = 6
NODES = 36
PLAYER1 = 1
PLAYER2 = 2
FREE = 0

# Initialize connection matrix and occupation states
# connections = [[0] * NODES for _ in range(NODES)]
occupation = [0] * NODES


# Initial occupation states
for i in range(11):
    occupation[i] = PLAYER1
for i in range(26, 36):
    occupation[i] = PLAYER2

# Tkinter setup
root = tk.Tk()
root.title("Game")

# Helper function to convert node index to grid position
def node_to_grid(index):
    row = index // GRID_SIZE
    col = index % GRID_SIZE
    return row, col

# Create buttons for nodes
buttons = []
for i in range(GRID_SIZE):
    row_buttons = []
    for j in range(GRID_SIZE):
        btn = tk.Button(root, text='', width=10, height=3, command=lambda i=i, j=j: on_click(i, j))
        btn.grid(row=i, column=j)
        row_buttons.append(btn)
    buttons.append(row_buttons)

# Update buttons based on occupation state
def update_buttons():
    for i in range(NODES):
        row, col = node_to_grid(i)
        if occupation[i] == PLAYER1:
            buttons[row][col].config(text='P1', bg='red')
        elif occupation[i] == PLAYER2:
            buttons[row][col].config(text='P2', bg='blue')
        else:
            buttons[row][col].config(text='', bg='white')

update_buttons()

# Handle dice roll
def roll_dice():
    return random.randint(1, 6)

# Find possible moves
def find_possible_moves(start_node, distance):
    visited = [False] * NODES
    possible_moves = []
    
    def dfs(current_node, current_distance):
        if current_distance == distance:
            if occupation[current_node] == FREE:
                possible_moves.append(current_node)
            return
        if visited[current_node]:
            return
        visited[current_node] = True
        for next_node in range(NODES):
            if connections[current_node][next_node] == 1:
                dfs(next_node, current_distance + 1)
        visited[current_node] = False
    
    dfs(start_node, 0)
    return possible_moves

# Handle button click
current_player = PLAYER1
selected_node = None

def on_click(i, j):
    global selected_node, current_player
    node_index = i * GRID_SIZE + j

    if selected_node is None:
        if occupation[node_index] == current_player:
            selected_node = node_index
            buttons[i][j].config(bg='yellow')
            d = roll_dice()
            possible_moves = find_possible_moves(node_index, d)
            if not possible_moves:
                messagebox.showinfo("No Move", f"No possible destination for distance {d}. Choose another pawn.")
                selected_node = None
                buttons[i][j].config(bg='red' if current_player == PLAYER1 else 'blue')
            else:
                for move in possible_moves:
                    row, col = node_to_grid(move)
                    buttons[row][col].config(bg='green')
    else:
        if occupation[node_index] == FREE and buttons[i][j].cget('bg') == 'green':
            occupation[selected_node] = FREE
            occupation[node_index] = current_player
            update_buttons()
            selected_node = None
            current_player = PLAYER2 if current_player == PLAYER1 else PLAYER1
            check_for_win()
        else:
            messagebox.showinfo("Invalid Move", "Choose a valid green-highlighted destination.")
            reset_highlights()

# Reset button highlights
def reset_highlights():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if occupation[i*GRID_SIZE+j] == PLAYER1:
                buttons[i][j].config(bg='red')
            elif occupation[i*GRID_SIZE+j] == PLAYER2:
                buttons[i][j].config(bg='blue')
            else:
                buttons[i][j].config(bg='white')

# Check for win condition
def check_for_win():
    if all(occupation[i] == PLAYER1 for i in range(26, 36)):
        messagebox.showinfo("Game Over", "Player 1 wins!")
        root.quit()
    elif all(occupation[i] == PLAYER2 for i in range(11)):
        messagebox.showinfo("Game Over", "Player 2 wins!")
        root.quit()

# Start the main game loop
update_buttons()
root.mainloop()
