import tkinter as tk
from tkinter import messagebox
import random

# Funcție care creează tabla de joc (o matrice 3x3)
def create_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

# Funcție care verifică dacă există un câștigător
def check_winner(board):
    # Verifică liniile
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]

    # Verifică coloanele
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]

    # Verifică diagonalele
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]

    return None  # Nu există câștigător

# Funcție care returnează mutările disponibile pe tablă
def get_available_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                moves.append((i, j))
    return moves

# Clasa Node reprezintă un nod în arborele de decizie pentru joc
class Node:
    def __init__(self, board, player):
        self.board = [row[:] for row in board]  # Copie a tablei de joc
        self.player = player  # Jucătorul curent
        self.children = []  # Lista de copii (mutările posibile)
        self.score = None  # Scorul asociat nodului

    # Verifică dacă nodul este terminal (câștigător sau remiză)
    def is_terminal(self):
        return check_winner(self.board) is not None or not get_available_moves(self.board)

    # Generează copii pentru toate mutările posibile
    def generate_children(self):
        if self.is_terminal():
            return
        next_player = 'O' if self.player == 'X' else 'X'
        for move in get_available_moves(self.board):
            new_board = [row[:] for row in self.board]  # Creează o copie a tablei curente
            new_board[move[0]][move[1]] = self.player  # Aplică mutarea
            child = Node(new_board, next_player)  # Creează un nod copil
            self.children.append(child)  # Adaugă copilul în lista de copii
            child.generate_children()  # Generează copii recursiv

# Funcție care construiește arborele de decizie pornind de la tabla curentă și jucătorul curent
def build_decision_tree(board, player):
    root = Node(board, player)  # Creează nodul rădăcină
    root.generate_children()  # Generează toți copiii (mutările posibile)
    return root

# Funcție care evaluează arborele de decizie și atribuie scoruri nodurilor
def evaluate_tree(node):
    winner = check_winner(node.board)  # Verifică dacă există un câștigător
    if winner == 'X':
        node.score = 1  # 'X' câștigă -> scor 1
    elif winner == 'O':
        node.score = -1  # 'O' câștigă -> scor -1
    else:
        node.score = 0  # Remiză sau jocul nu s-a terminat -> scor 0

    if node.is_terminal():
        return node.score

    scores = []
    for child in node.children:
        scores.append(evaluate_tree(child))  # Evaluează recursiv scorurile copiilor

    if node.player == 'X':
        node.score = max(scores)
    else:
        node.score = min(scores)

    return node.score

# Funcție care determină cea mai bună mutare pe baza arborelui de decizie
def best_move_from_tree(node):
    best_score = -float('inf')
    best_moves = []

    for child in node.children:
        if child.score > best_score:
            best_score = child.score
            best_moves = [child]  # Dacă găsește un scor mai bun, resetează lista de mutări
        elif child.score == best_score:
            best_moves.append(child)  # Dacă scorul e egal, adaugă copilul în lista de mutări

    # Posibilitatea de alegere aleatorie pentru o dificultate mai scazuta a jocului
    if random.random() < 0.8:  # Cu 80% probabilitate, alege cea mai bună mutare
        best_move = random.choice(best_moves)
    else:  # Cu 20% probabilitate, alege o mutare aleatorie
        best_move = random.choice(node.children)

    return best_move.board  # Returnează tabla de joc după cea mai bună mutare

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Space Edition")
        self.root.geometry("600x600")

        # Creează canvas pentru animația de fundal
        self.canvas = tk.Canvas(self.root, width=600, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Desenează fundalul cu tema spațială
        self.draw_space_background()

        # Inițializează tabla de joc
        self.board = create_board()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'O'
        self.create_buttons()

    def draw_space_background(self):
        # Desenează fundalul negru
        self.canvas.create_rectangle(0, 0, 600, 600, fill="black")

        # Desenează stelele
        for _ in range(70):
            x = random.randint(0, 600)
            y = random.randint(0, 600)
            brightness = random.choice([2, 3, 4])  # Strălucirea stelei
            self.canvas.create_oval(x, y, x + brightness, y + brightness, fill="white")

        # Stele strălucitoare și cu detalii
        for _ in range(30):
            x = random.randint(0, 600)
            y = random.randint(0, 600)
            brightness = random.choice([5, 6, 7])
            self.canvas.create_oval(x, y, x + brightness, y + brightness, fill="yellow")
            if random.choice([True, False]):
                # Adaugă inele în jurul stelei
                self.canvas.create_oval(x - 2, y - 2, x + brightness + 2, y + brightness + 2, outline="lightyellow")

        # Desenează planeta albastră cu detalii
        self.canvas.create_oval(50, 100, 120, 170, fill="lightblue")  # Planeta 1 (mutată la stânga)
        self.canvas.create_oval(60, 110, 110, 160, outline="white")  # Inelul planetei
        self.canvas.create_oval(60, 110, 80, 130, fill="lightgray")  # Crater 3, mai mare și mai deschis la culoare
        self.canvas.create_oval(90, 120, 120, 150, fill="lightgray")  # Crater 4, mai mare și mai deschis la culoare
        self.canvas.create_oval(70, 120, 80, 130, fill="gray")  # Crater 1
        self.canvas.create_oval(90,130, 105, 145, fill="gray")  # Crater 2
        self.canvas.create_oval(65, 145, 90, 170, fill="lightgray")  # Crater 4, mai mare și mai deschis la culoare

        # Desenează celelalte planete
        self.canvas.create_oval(400, 50, 470, 120, fill="orange")  # Planeta 2

        # Desenează racheta mare în centrul de jos
        self.canvas.create_polygon(300, 480, 320, 450, 280, 450, fill="white", tags="rocket")
        self.canvas.create_rectangle(285, 450, 315, 490, fill="gray", tags="rocket")
        self.canvas.create_polygon(285, 490, 315, 490, 300, 520, fill="red", tags="rocket")
        self.canvas.create_polygon(290, 490, 280, 510, 300, 490, fill="gray", tags="rocket")  # Aripioare lângă foc
        self.canvas.create_polygon(310, 490, 320, 510, 300, 490, fill="gray", tags="rocket")  # Aripioare lângă foc

        # Desenează o rachetă suplimentară în colțul din dreapta jos
        self.canvas.create_polygon(530, 530, 570, 530, 550, 500, fill="white", tags="rocket_small")  # Corpul rachetei (orientat în sus)
        self.canvas.create_rectangle(535, 530, 565, 570, fill="gray", tags="rocket_small")  # Corpul principal
        self.canvas.create_polygon(535, 570, 565, 570, 550, 600, fill="orange", tags="rocket_small")  # Focul din spatele rachetei
        self.canvas.create_polygon(540, 570, 530, 590, 550, 570, fill="red", tags="rocket_small")  # Aripioare lângă foc
        self.canvas.create_polygon(560, 570, 570, 590, 550, 570, fill="red", tags="rocket_small")  # Aripioare lângă foc

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        for i in range(3):
            for j in range(3):
                button = tk.Button(frame, text='', font='normal 20 bold', height=3, width=6,
                                   command=lambda i=i, j=j: self.on_button_click(i, j),
                                   bg="darkblue", fg="white", activebackground="blue", activeforeground="white")
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def on_button_click(self, i, j):
        if self.board[i][j] == ' ' and self.current_player == 'O':
            self.buttons[i][j]['text'] = 'O'
            self.board[i][j] = 'O'
            if check_winner(self.board) or not get_available_moves(self.board):
                self.end_game()
            else:
                self.current_player = 'X'
                self.computer_move()

    def computer_move(self):
        tree = build_decision_tree(self.board, 'X')
        evaluate_tree(tree)
        best_board = best_move_from_tree(tree)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != best_board[i][j]:
                    self.buttons[i][j]['text'] = 'X'
                    self.board[i][j] = 'X'
                    break
        if check_winner(self.board) or not get_available_moves(self.board):
            self.end_game()
        else:
            self.current_player = 'O'

    def end_game(self):
        winner = check_winner(self.board)
        if winner == 'O':
            self.show_confetti()
            messagebox.showinfo("Tic Tac Toe", f"Congratulations, {winner} wins!")
        elif winner == 'X':
            self.explode_rocket()
            messagebox.showinfo("Tic Tac Toe", f"Sorry, {winner} wins! The rocket has exploded")
        else:
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
        self.reset_board()

    def show_confetti(self):
        for _ in range(50):
            x = random.randint(0, 600)
            y = random.randint(0, 600)
            size = random.randint(10, 20)
            color = random.choice(["red", "blue", "green", "yellow", "pink", "orange"])
            self.canvas.create_oval(x, y, x + size, y + size, fill=color, tags="confetti")

    def explode_rocket(self):
        # Explozia rachetei din colțul din dreapta jos
        for _ in range(20):
            x = random.randint(530, 570)  # Coordonate specifice rachetei din dreapta jos
            y = random.randint(530, 570)
            size = random.randint(10, 30)
            color = random.choice(["orange", "red", "yellow"])
            self.canvas.create_oval(x, y, x + size, y + size, fill=color, tags="explosion")

        # Șterge racheta din dreapta jos
        self.canvas.delete("rocket_small")

    def reset_board(self):
        self.board = create_board()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = ''
        self.current_player = 'O'
        self.canvas.delete("confetti")
        self.canvas.delete("explosion")
        self.canvas.delete("all")
        self.draw_space_background()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
