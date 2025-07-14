import time
import random
from colorama import init, Fore, Style

init(autoreset=True)

HUMAN = 'O'
AI = 'X'
EMPTY = ' '

# Draw the board
def draw_board(board):
    print("\n")
    for i in range(3):
        for j in range(3):
            cell = board[i * 3 + j]
            if cell == HUMAN:
                print(Fore.CYAN + f" {cell} ", end='')
            elif cell == AI:
                print(Fore.GREEN + f" {cell} ", end='')
            else:
                print(Fore.WHITE + f" {i * 3 + j} ", end='')
            if j < 2:
                print(Fore.WHITE + "|", end='')
        if i < 2:
            print("\n" + Fore.WHITE + "---+---+---")
    print("\n")

# Winning combinations
WIN_COMBOS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
    [0, 4, 8], [2, 4, 6]              # Diagonal
]

def is_winner(board, player):
    return any(all(board[pos] == player for pos in combo) for combo in WIN_COMBOS)

def is_draw(board):
    return all(cell != EMPTY for cell in board)

def get_available_moves(board):
    return [i for i, cell in enumerate(board) if cell == EMPTY]

def minimax(board, depth, alpha, beta, maximizing_player):
    if is_winner(board, AI):
        return 10 - depth
    if is_winner(board, HUMAN):
        return depth - 10
    if is_draw(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_available_moves(board):
            board[move] = AI
            eval = minimax(board, depth + 1, alpha, beta, False)
            board[move] = EMPTY
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_available_moves(board):
            board[move] = HUMAN
            eval = minimax(board, depth + 1, alpha, beta, True)
            board[move] = EMPTY
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board):
    best_score = float('-inf')
    best_move = None
    for move in get_available_moves(board):
        board[move] = AI
        score = minimax(board, 0, float('-inf'), float('inf'), False)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def human_move(board):
    while True:
        try:
            move = int(input("Choose your move (0-8): "))
            if board[move] == EMPTY:
                return move
            else:
                print("Cell already taken.")
        except (ValueError, IndexError):
            print("Invalid input. Try again.")

def play_game():
    print(Fore.MAGENTA + "Welcome to Tic-Tac-Toe! You are 'O'. AI is 'X'.\n")
    board = [EMPTY] * 9
    current_player = HUMAN if random.choice([True, False]) else AI
    print(f"{Fore.YELLOW}Randomly selected: {'You' if current_player == HUMAN else 'AI'} will go first.")

    while True:
        draw_board(board)
        if current_player == HUMAN:
            move = human_move(board)
            board[move] = HUMAN
        else:
            print(Fore.LIGHTGREEN_EX + "AI is thinking...\n")
            time.sleep(1)
            move = find_best_move(board)
            board[move] = AI

        if is_winner(board, current_player):
            draw_board(board)
            if current_player == HUMAN:
                print(Fore.CYAN + "🎉 You win!")
            else:
                print(Fore.GREEN + "🤖 AI wins! Better luck next time.")
            break
        elif is_draw(board):
            draw_board(board)
            print(Fore.YELLOW + "😐 It's a draw!")
            break

        current_player = AI if current_player == HUMAN else HUMAN

if __name__ == "__main__":
    play_game()

