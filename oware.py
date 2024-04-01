import copy

NUM_HOLES = 16
NUM_SEEDS = 2
RED = 'R'
BLUE = 'B'
TRANSPARENT = 'T'

board = [[(RED, NUM_SEEDS), (BLUE, NUM_SEEDS),(TRANSPARENT, NUM_SEEDS-1)] for _ in range(NUM_HOLES)]

# Function to check if the game is over
def is_game_over(board):
    total_seeds = sum(sum(seed[1] for seed in hole) for hole in board)
    return total_seeds < 10

# Function to print the current state of the board
def print_board(board):
    for i, hole in enumerate(board, start=1):
        seeds = ' '.join(f"{color}{count}" for color, count in hole if count > 0)
        print(f"{i} ({seeds}) ", end='')
    print()

# Function to get all possible moves for a given player
def get_possible_moves(board, player):
    moves = []
    for i, hole in enumerate(board, start=1):
        if ((i-1) % 2 == 1 and player == 1) or ((i-1) % 2 == 0 and player == 2):            
            for color, count in hole:
                if count > 0:
                    moves.append((i, color))
    return moves

# Function to make a move on the board
def make_move(board, move):
    hole, color = move
    hole -= 1  # Adjust for zero-based indexing

    # Remove seeds from the selected hole
    seeds = [(seed_color, count) for seed_color, count in board[hole] if seed_color == color]
    board[hole] = [(seed_color, count) for seed_color, count in board[hole] if seed_color != color]

    # Distribute the seeds
    current_hole = hole
    for seed_color, count in seeds:
        current_hole = (current_hole + 1) % NUM_HOLES
        board[current_hole].append((seed_color, count))

    # Capture seeds if applicable
    captured_seeds = []
    current_hole = (current_hole + 1) % NUM_HOLES
    while len(board[current_hole]) in [2, 3]:
        captured_seeds.extend(board[current_hole])
        board[current_hole] = []

        current_hole = (current_hole - 1) % NUM_HOLES

    return captured_seeds

# Function to evaluate the score of the board for a given player
def evaluate(board, player):
    player_score = sum(count for hole in board for color, count in hole if color == RED and player == 1)
    opponent_score = sum(count for hole in board for color, count in hole if color == RED and player == 2)
    return player_score - opponent_score

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_game_over(board):
        return evaluate(board, 1)
    
    if maximizing_player:
        max_eval = float('-inf')
        moves = get_possible_moves(board, 1)
        for move in moves:
            new_board = copy.deepcopy(board)
            captured_seeds = make_move(new_board, move)
            eval = minimax(new_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        moves = get_possible_moves(board, 2)
        for move in moves:
            new_board = copy.deepcopy(board)
            captured_seeds = make_move(new_board, move)
            eval = minimax(new_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Function to find the best move for the AI player using the Minimax algorithm
def find_best_move(board):
    best_score = float('-inf')
    best_move = None
    moves = get_possible_moves(board, 2)
    for move in moves:
        new_board = copy.deepcopy(board)
        captured_seeds = make_move(new_board, move)
        score = minimax(new_board, 3, float('-inf'), float('inf'), False)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

# Main game loop
current_player = 1
while not is_game_over(board):
    print_board(board)
    # Get the move from the current player
    if current_player == 1:
        hole = int(input("Enter the hole number: "))
        color = input("Enter the color (R, B, T): ")
        move = (hole, color)
    else:
        move = find_best_move(board)
    
    # Make the move and capture seeds
    captured_seeds = make_move(board, move)
    
    # Print the move and captured seeds
    print(f"Player {current_player} played {move}")
    print(f"Captured seeds: {captured_seeds}")
    
    # Switch to the next player
    current_player = 3 - current_player  # Switch between player 1 and 2 (1 -> 2 or 2 -> 1)

# Game over, print the final board and determine the winner
print_board(board)
player1_score = sum(count for hole in board for color, count in hole if color == RED and current_player == 1)
player2_score = sum(count for hole in board for color, count in hole if color == RED and current_player == 2)
if player1_score > player2_score:
    print("Player 1 wins!")
elif player1_score < player2_score:
    print("Player 2 wins!")
else:
    print("It's a tie!")