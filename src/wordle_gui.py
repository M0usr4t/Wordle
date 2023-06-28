from tkinter import *
from tkinter import messagebox
from wordle import Game, WORD_SIZE, MAX_ATTEMPTS, Match, play
from spell_check import is_spelling_correct
from word_picker import get_a_random_word

class WordleGui:
    def __init__(self):
        self.target = get_a_random_word()
        self.root = Tk() 
        self.grid_container = Frame(self.root)
        self.root.configure(bg="light blue")
        self.grid = []
        self.current_row = 0
        self.current_column = 0
        self.guess_button = Button(self.root, text="Guess", font=('Arial', 18), state="disabled", command = self._evaluate_guess)
        
    def run(self):
        self.root.geometry("500x600")
        self.root.title("Wordle Clone")

        label = Label(self.root, text="Wordle", font=('Arial', 18))
        label.pack(padx=20, pady=20) 
        
        self._generate_grid()
        self.grid_container.pack(pady=20)
        
        self.guess_button.pack()
        
        self.root.bind('<Key>', self._input_key)
        self.root.mainloop()
    
    def _generate_grid(self):
        for i in range(MAX_ATTEMPTS):
            row = []
            for j in range(WORD_SIZE):
                box = Label(self.grid_container, width=5, bg="grey", fg="grey")
                box.grid(row=i, column=j, pady=5, padx=5)
                row.append(box)
            self.grid.append(row)
        self._activate_row(self.current_row)
   
    def _evaluate_guess(self):
        guess = "".join([self.grid[self.current_row][col].cget("text") for col in range(0, WORD_SIZE)])
        
        info = play(self.target, guess, self.current_row, is_spelling_correct)
        
        if(info["game_status"] == Game.WRONG_SPELLING):
            self._retry()
        elif(info["game_message"]):
            messagebox.showinfo("Game Message", info["game_message"])
            self._exit_window()
        else:
            self._fill_out_row(info, self.current_row)
            self._start_next_guess()
    
    def _retry(self):
        messagebox.showinfo("Game Message", "Not a word")
        
        self.root.focus_force()
        self.guess_button.config(state="disabled")
    
    def _fill_out_row(self, info, row):
        for col in range(WORD_SIZE):
            if info["response"][col] == Match.EXACT:
                self.grid[row][col].configure(bg="green")
            elif info["response"][col] == Match.EXISTS:
                self.grid[row][col].configure(bg="yellow")
            else:
                self.grid[row][col].configure(bg="gray")
    
    def _activate_row(self, row):
        if row >= MAX_ATTEMPTS: return
        
        for col in range(WORD_SIZE):
            self.grid[row][col].configure(bg="light blue")

    def _start_next_guess(self):
        self.current_row += 1
        self.current_column = 0
        self._activate_row(self.current_row)
        self._activate_button_if_ready_to_guess(self.current_column)
        
    def _activate_button_if_ready_to_guess(self, guess_length):
        status = "normal" if guess_length == WORD_SIZE else "disabled"
        self.guess_button.config(state=status)
        
    def _input_key(self, event):      
        if self.current_row >= MAX_ATTEMPTS: return
        
        event_key = event.keysym

        if(event_key == "BackSpace"):
            self._delete_letter()
        elif(event_key == "Return" and not self.guess_button.cget("state") == "disabled"):
            self._evaluate_guess()
        else:    
            self._place_key(event_key)
            
    def _place_key(self, event_key):
        if(self._check_if_key_is_alphabet(event_key) and self.current_column < WORD_SIZE):
            self.grid[self.current_row][self.current_column].configure(text=event_key.upper(), fg="black")
            self.current_column += 1
            
            self._activate_button_if_ready_to_guess(self.current_column) 
        
    def _delete_letter(self):
        if(self.current_column <= 0): return
        
        self.current_column -= 1
        self.grid[self.current_row][self.current_column].configure(text="")
        
        self.guess_button.config(state="disabled")
    
    def _check_if_key_is_alphabet(self, key):
        return len(key) == 1 and key.isalpha()
        
    def _exit_window(self):
        self.root.after(0, self.root.destroy)
        
gui = WordleGui()
gui.run()
