from tkinter import *
from tkinter import messagebox
from random import randint

FONT = ("Verdana", 40, "bold")
SCORE_FONT = ("Verdana", 10, "bold")


def new_game():
    board = [[0 for i in range(4)] for i in range(4)]
    return board


def add_two(board):
    zero_block = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                zero_block.append((i, j))
    if len(zero_block) != 0:
        tup = randint(0, len(zero_block) - 1)
        tup = zero_block[tup]
        board[tup[0]][tup[1]] = 2
    return board


def can_move_horizontal(board):
    count = 1
    for i in range(4):
        for j in range(1,4):
            if board[i][j] == board[i][j-1]:
                return True
        count += 1
    if count != 4:
        return  True
    return False


def can_move_verticle(board):
    count = 0
    for i in range(1,4):
        for j in range(4):
            if board[i][j] == board[i-1][j]:
                return True
        count += 1
    if count != 4:
        return True
    return False


def current_state(board):
    # winning state
    for i in range(4):
        for j in range(4):
            if board[i][j] == "2048":
                return "win"
    # check if any entry if 0, then continue
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return "continue"
    # check row above and on right, if any can combine
    for i in range(3):
        for j in range(3):
            if board[i][j] == board[i+1][j] or board[i][j] == board[i][j+1]:
                return "continue"
    for i in range(1,4):
        if board[3][i] == board[3][i-1] or board[i][3] == board[i-1][3]:
            return "continue"
    # else you lost!
    return "lose"


def up(board, score):
    if (not can_move_verticle(board)) and can_move_horizontal(board):
        return board, score

    for i in range(4):
        for j in range(1,4):
            if board[j][i] == board[j-1][i]:
                score += board[j][i]
                board[j-1][i] *= 2
                board[j][i] = 0

    for i in range(4):
        for j in range(4):
            if board[j][i] == 0:
                count = 0
                while board[j+count][i] == 0 and (j+count) < 3:
                    count += 1
                if board[j+count][i] != 0:
                    board[j][i] = board[j+count][i]
                    board[j+count][i] = 0
    add_two(board)
    return board, score


def down(board, score):
    if (not can_move_verticle(board)) and can_move_horizontal(board):
        return board, score

    for i in range(3,-1,-1):
        for j in range(3,-1,-1):
            if board[j][i] == board[j-1][i]:
                score += board[j][i]
                board[j][i] *= 2
                board[j-1][i] = 0

    for i in range(3,-1,-1):
        for j in range(3,-1,-1):
            if board[j][i] == 0:
                count = 0
                while board[j-count][i] == 0 and (j-count) >0:
                    count += 1
                if board[j-count][i] != 0:
                    board[j][i] = board[j-count][i]
                    board[j-count][i] = 0
    add_two(board)
    return board, score


def right(board, score):
    if (can_move_verticle(board)) and (not can_move_horizontal(board)):
        return board, score

    for i in range(3,-1,-1):
        for j in range(3,-1,-1):
            if board[i][j] == board[i][j-1]:
                score += board[i][j]
                board[i][j] *= 2
                board[i][j-1] = 0
    for i in range(3,-1,-1):
        for j in range(3,-1,-1):
            if board[i][j] == 0:
                count = 0
                while board[i][j-count] == 0 and (j-count) >0:
                    count += 1
                if board[i][j-count] != 0:
                    board[i][j] = board[i][j-count]
                    board[i][j-count] = 0
    add_two(board)
    return board, score


def left(board, score):
    if (can_move_verticle(board)) and (not can_move_horizontal(board)):
        return board, score

    for i in range(4):
        for j in range(1,4):
            if board[i][j] == board[i][j-1]:
                score += board[i][j]
                board[i][j-1] *= 2
                board[i][j] = 0

    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                count = 0
                while board[i][j+count] == 0 and (j+count) < 3:
                    count += 1
                if board[i][j+count] != 0:
                    board[i][j] = board[i][j+count]
                    board[i][j+count] = 0
    add_two(board)
    return board, score


class Grid:
    def __init__(self, master):
        frame = Frame(master, height=500, width=500, bg="grey")
        frame.grid()
        self.score = 0
        scoreFr = Frame(master, height=25, width=25, bg="dark grey")
        self.scoreLb = Label(scoreFr, text="Score: ", height = 2, width = 10, font = SCORE_FONT)
        self.scoreLb.pack()
        scoreFr.grid(row = 0, column = 2, padx = 8, pady = 8)
        self.board = new_game()
        self.board = add_two(self.board)
        self.grid = []
        frame.bind("<Up>", self.up)
        frame.bind("<Down>", self.down)
        frame.bind("<Right>", self.right)
        frame.bind("<Left>", self.left)
        frame.focus_set()
        self.game_status = "continue"
        for i in range(4):
            row = []
            for j in range(4):
                cell = Frame(frame, height=125, width=125, bg="dark grey")
                lb = Label(cell, text="", justify=CENTER, height=2, width=4, font=FONT)
                row.append(lb)
                lb.pack()
                cell.grid(row=i, column=j, padx=4, pady=4)
            self.grid.append(row)

        self.update_board()
        master.mainloop()

    def up(self, event):
        self.board, self.score = up(self.board, self.score)
        self.update_board()
        self.current_status()

    def down(self, event):
        self.board, self.score = down(self.board, self.score)
        self.update_board()
        self.current_status()

    def right(self, event):
        self.board, self.score = right(self.board, self.score)
        self.update_board()
        self.current_status()

    def left(self, event):
        self.board, self.score = left(self.board, self.score)
        self.update_board()
        self.current_status()

    def current_status(self):
        self.game_status = current_state(self.board)
        print(self.game_status)
        if self.game_status == "win" or self.game_status == "lose":
            messagebox.showinfo("Game Status", self.game_status)
            self.score = 0
            for i in range(4):
                for j in range(4):
                    self.board[i][j] = 0
        self.update_board()

    def update_board(self):
        self.scoreLb.configure(text = "Score: "+str(self.score))
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    self.grid[i][j].configure(text=str(""))
                else:
                    self.grid[i][j].config(text=str(self.board[i][j]))
root = Tk()
root.geometry("790x580+100+100")
g = Grid(root)