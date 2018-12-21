from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM,filedialog,ttk
import tkinter as tk

import backtrack
import imageprocessing
import digitidentifier

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """
    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent
        self.row, self.col = -1, -1
        self.__initUI()

    def __initUI(self):
        """
        Initializes the boaard and the overall GUI.
        """
        self.parent.title("SuDoKu Solver")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,width=WIDTH,height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self, text=" Clear ",command=self.__clear_answers)
        clear_button.pack()
        clear_button.place(x=20,y=HEIGHT-10)
        load_button = Button(self, text=" Load  ",command=self.load)
        load_button.pack()
        load_button.place(x=80,y=HEIGHT-10)
        solve_button = Button(self,text=" Solve ",command=self.solve)
        solve_button.pack()
        solve_button.place(x=140,y=HEIGHT-10)
        correct_button = Button(self,text=" Correct ",command=self.correct)
        correct_button.pack()
        correct_button.place(x=200,y=HEIGHT-10)
        teach_button = Button(self,text=" Teach ",command=self.teach)
        teach_button.pack()
        teach_button.place(x=280,y=HEIGHT-10)
        
        self.__draw_grid()
        self.__draw_puzzle()
        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(10):
            color = "black" if i % 3 == 0 else "light gray"
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        """
        Draws the numbers on the grids.
        """
        self.deleteCanvas()
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(x, y, text=answer, tags="numbers"+str(i)+str(j), fill=color)

    def __draw_cursor(self):
        """
        Highlights the selected box.
        """
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            self.canvas.delete("numbers"+str(self.row)+str(self.col))
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(x0, y0, x1, y1,outline="red", tags="cursor")

    def deleteCanvas(self):
        """
        Deletes the numbers in the grid.
        """
        for i in range(9):
            for j in range(9):
                self.canvas.delete("numbers"+str(i)+str(j))
                
    def __cell_clicked(self, event):
        """
        Happens when a cell is clicked.
        """
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()
            # get row and col numbers from x,y coordinates
            row, col = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE
            row=int(row)
            col=int(col)
            self.canvas.delete("numbers"+str(row)+str(col))
            self.game.puzzle[row][col]=0
            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.puzzle[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __key_pressed(self, event):
        """
        Handles when a number is enterd into the grid.
        """
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()

    def __clear_answers(self):
        """
        Clear Button function.
        """
        self.game.start()
        self.__draw_puzzle()

    def solve(self):
        """
        Solve function
        """
        sudoku=[]
        for i in range(9):
            array=[]
            for j in range(9):
                array.append(self.game.start_puzzle[i][j])
            sudoku.append(array)       
        if backtrack.solve_sudoku(sudoku):
           self.game.puzzle=sudoku
           self.__draw_puzzle()
        else:
            self.popupmsg("    No Solution.    \n\n")


    def popupmsg(self,msg):
        """
        Displays a pop up message when no solution is found.
        """
        popup = tk.Tk()
        popup.wm_title("Result")
        label = ttk.Label(popup, text=msg, font=("Verdana", 12))
        label.pack(side="top", fill="x", pady=12)
        B1 = ttk.Button(popup, text="Ok", command = popup.destroy)
        B1.pack()
        popup.mainloop()

    def load(self):
        """
        For load function. Processes the image and displays the result.
        """
        filename = filedialog.askopenfilename()
        b=imageprocessing.processImage(filename)
        self.board = b
        self.game.start_puzzle=b
        self.game.start()
        self.__draw_puzzle()
        
    def correct(self):
        self.board = self.game.puzzle
        self.game.start_puzzle=self.game.puzzle
        self.game.start()
        self.__draw_puzzle()

    def teach(self):
        sudoku=self.game.start_puzzle
        digitidentifier.update(sudoku)
        

class SudokuBoard(object):
    def __init__(self):
        self.board = self.__create_board()

    def __create_board(self):
        board=[]
        for i in range(9):
            array=[]
            for j in range(9):
                array.append(0)
            board.append(array)
        return board


class SudokuGame(object):
    def __init__(self):
        self.start_puzzle = SudokuBoard().board

    def start(self):
        self.game_over = False
        self.puzzle = []
        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])




if __name__ == '__main__':
        game = SudokuGame()
        game.start()
        root = Tk()
        SudokuUI(root, game)
        root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
        root.mainloop()
