import random
import tkinter as tk
from tkinter import messagebox
import time

# List of colors - added some funky ones!
colours = ['Red', 'Blue', 'Green', 'Yellow', 'Orange', 'Purple', 'Pink', 'Black', 'White', 
           'Turquoise', 'Magenta', 'Gold', 'Salmon']

# Fun messages when you get it right
correct_messages = [
    "Woohoo! Color ninja!",
    "Your eyes don't lie!",
    "Are you a mantis shrimp? Those things see ALL colors!",
    "You're on fire! Not literally though.",
    "Color me impressed!",
    "You've got the eyes of an eagle... or whatever animal has good color vision.",
]

# Sassy messages when time's up
times_up_messages = [
    "Time's up! Color you later!",
    "Tick tock! The clock wins again.",
    "That's all folks! Time waits for no player.",
    "Game over! Time flies when you're confused about colors.",
]

score = 0
timeleft = 30
game_active = False

def check_answer(event=None):
    global score
    
    if not game_active or timeleft <= 0:
        return
        
    # Get what the player typed
    user_input = e.get().lower().strip()
    # The actual color of the text (not the word)
    correct_color = label.cget("fg").lower()
    
    if user_input == correct_color:
        score += 1
        # Show a random fun message
        status_label.config(text=random.choice(correct_messages))
        
        # Increase difficulty as score gets higher
        if score > 10:
            label.config(font=(font, 65))  # Make text bigger
        if score > 15:
            window.after(50, flash_background)  # Add distraction
    else:
        status_label.config(text="Hmm, not quite right...")
        
    # Clear the entry field
    e.delete(0, tk.END)
    
    # Update score display
    score_label.config(text=f"Score: {score}")
    
    # Set up next color
    random.shuffle(colours)
    color_word = colours[0]
    display_color = random.choice([c for c in colours if c != color_word])
    label.config(fg=display_color, text=color_word)

def flash_background():
    # A silly distraction for higher levels
    if score > 15 and game_active:
        current_color = window.cget("bg")
        flash_color = "light gray" if current_color == "SystemButtonFace" else "SystemButtonFace"
        window.config(bg=flash_color)

def countdown():
    global timeleft, game_active
    
    if timeleft > 0:
        timeleft -= 1
        time_label.config(text=f"Time left: {timeleft}")
        
        # Make the countdown more dramatic near the end
        if timeleft <= 5:
            time_label.config(fg="red", font=(font, 12, "bold"))
            
        time_label.after(1000, countdown)
    else:
        game_active = False
        time_label.config(text="TIME'S UP!", fg="red")
        messagebox.showinfo('Game Over', random.choice(times_up_messages))
        scoreshow()

def record_highest_score():
    highest_score = load_highest_score()
    if score > highest_score:
        with open("highest_score.txt", "w") as file:
            file.write(str(score))
        return True
    return False

def load_highest_score():
    try:
        with open("highest_score.txt", "r") as file:
            data = file.read()
            if data:
                return int(data)
            else:
                return 0
    except FileNotFoundError:
        return 0

def scoreshow():
    new_record = record_highest_score()
    highest = load_highest_score()
    
    # Clear the main game elements
    label.config(text="")
    
    # Show the final score with some personality
    if new_record:
        result_text = f"NEW HIGH SCORE: {score}! You're a color genius!"
    else:
        result_text = f"Your score: {score}\nHighest ever: {highest}"
        if score < 5:
            result_text += "\nMaybe colors aren't your thing?"
        elif score < 10:
            result_text += "\nNot bad, not bad at all!"
        else:
            result_text += "\nImpressive color mastery!"
    
    status_label.config(text=result_text, font=(font, 14, "bold"))
    
    # Add a replay button
    replay_button = tk.Button(window, text="Play Again?", command=restart_game)
    replay_button.pack(pady=10)

def restart_game():
    global score, timeleft, game_active
    
    # Reset game state
    score = 0
    timeleft = 30
    game_active = False
    
    # Clear and reset UI
    for widget in window.winfo_children():
        if widget not in (instructions, score_label, time_label, label, e, status_label):
            widget.destroy()
    
    label.config(text="Ready?", fg="black", font=(font, 60))
    score_label.config(text="Press Enter to start", fg="black")
    time_label.config(text=f"Time left: {timeleft}", fg="black", font=(font, 12))
    status_label.config(text="Let's see how colorful your brain is!", font=(font, 12))
    
    # Re-focus on the entry field
    e.focus_set()

def start_game(event=None):
    global timeleft, game_active
    
    if not game_active and timeleft == 30:
        game_active = True
        status_label.config(text="Game on! Type the COLOR, not the word!")
        score_label.config(text="Score: 0")
        
        # Set up the first color
        random.shuffle(colours)
        color_word = colours[0]
        display_color = random.choice([c for c in colours if c != color_word])
        label.config(fg=display_color, text=color_word)
        
        # Start countdown
        countdown()

# Create the main window with a fun title
window = tk.Tk()
font = 'Helvetica'
window.title("😵 Color Confusion Challenge 🤪")
window.geometry("450x350")
window.resizable(False, False)

# Make the window pop up in the center of the screen
window.eval('tk::PlaceWindow . center')

# Instructions
instructions = tk.Label(window, text="Type the COLOR of the text, not the word!", 
                       font=(font, 13, "bold"))
instructions.pack(pady=10)

# Score display
score_label = tk.Label(window, text="Press Enter to start", font=(font, 12))
score_label.pack()

# Time remaining
time_label = tk.Label(window, text=f"Time left: {timeleft}", font=(font, 12))
time_label.pack()

# The main color word display
label = tk.Label(window, text="Ready?", font=(font, 60))
label.pack(pady=20)

# Entry field for user input
e = tk.Entry(window, font=(font, 14), width=15)
e.pack(pady=10)
e.focus_set()

# Status messages
status_label = tk.Label(window, text="Let's see how colorful your brain is!", font=(font, 12))
status_label.pack(pady=5)

# Critical fix: Bind the Enter key for both starting the game AND submitting answers
window.bind('<Return>', lambda event: start_game() if not game_active else check_answer())
e.bind('<Return>', check_answer)  # Also bind directly to the entry widget

# Easter egg - secret key combination gives bonus time
def secret_bonus(event):
    global timeleft
    if event.keysym == 'b' and event.state & 0x4:  # Ctrl+B
        if game_active and timeleft < 25:
            timeleft += 5
            time_label.config(text=f"Time left: {timeleft}")
            status_label.config(text="BONUS TIME! Someone knows the secret...")

window.bind('<KeyPress>', secret_bonus)

# Start the main loop
window.mainloop()