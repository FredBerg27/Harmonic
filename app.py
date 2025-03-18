import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import time
import threading
from instrument import Fretboard, Keyboard, Sheet_Music

class HarmonicAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Harmonic Analysis Tool")
        self.root.geometry("1200x800")
        
        # Initialize instruments
        self.fretboard = Fretboard()
        self.keyboard = Keyboard()
        self.sheet_music = Sheet_Music()
        
        # Selected notes for the current chord
        self.current_chord = []
        
        # Initial welcome screen
        self.show_welcome_screen()
    
    def show_welcome_screen(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        welcome_frame = ttk.Frame(self.root, padding="20")
        welcome_frame.pack(expand=True, fill=tk.BOTH)
        
        title_label = ttk.Label(welcome_frame, text="Harmonic Analysis Tool", font=("Arial", 24))
        title_label.pack(pady=20)
        
        add_song_button = ttk.Button(welcome_frame, text="Add New Song", command=self.setup_new_song)
        add_song_button.pack(pady=10)
        
        exit_button = ttk.Button(welcome_frame, text="Exit", command=self.root.quit)
        exit_button.pack(pady=10)
    
    def setup_new_song(self):
        # Get song name
        song_name = simpledialog.askstring("New Song", "Enter song name:", parent=self.root)
        if not song_name:
            song_name = "Untitled"
        
        self.sheet_music.set_song_name(song_name)
        
        # Choose tuning
        self.show_tuning_selection()
    
    def show_tuning_selection(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tuning_frame = ttk.Frame(self.root, padding="20")
        tuning_frame.pack(expand=True, fill=tk.BOTH)
        
        title_label = ttk.Label(tuning_frame, text="Select Guitar Tuning", font=("Arial", 18))
        title_label.pack(pady=20)
        
        tunings = ["Standard", "Drop D", "Atmospheric", "Open G"]
        tuning_var = tk.StringVar(value=tunings[0])
        
        for tuning in tunings:
            tuning_radio = ttk.Radiobutton(tuning_frame, text=tuning, value=tuning, variable=tuning_var)
            tuning_radio.pack(anchor=tk.W, pady=5)
        
        continue_button = ttk.Button(tuning_frame, text="Continue", 
                                     command=lambda: self.setup_main_interface(tuning_var.get()))
        continue_button.pack(pady=20)
        
        back_button = ttk.Button(tuning_frame, text="Back", command=self.show_welcome_screen)
        back_button.pack()
    
    def setup_main_interface(self, tuning):
        # Set the selected tuning
        self.fretboard.set_tuning(tuning)
        
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Title and song info
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=5)
        
        title_label = ttk.Label(info_frame, text=f"Song: {self.sheet_music.song_name}", font=("Arial", 14))
        title_label.pack(side=tk.LEFT, padx=10)
        
        tuning_label = ttk.Label(info_frame, text=f"Tuning: {self.fretboard.current_tuning}", font=("Arial", 12))
        tuning_label.pack(side=tk.RIGHT, padx=10)
        
        # Create three main sections
        self.create_fretboard_section(main_frame)
        self.create_keyboard_section(main_frame)
        self.create_sheet_music_section(main_frame)
        
        # Bottom control panel
        control_frame = ttk.Frame(main_frame, padding="10")
        control_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        play_button = ttk.Button(control_frame, text="Play Song", command=self.play_full_song)
        play_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(control_frame, text="Clear Song", command=self.clear_song)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        new_song_button = ttk.Button(control_frame, text="New Song", command=self.show_welcome_screen)
        new_song_button.pack(side=tk.RIGHT, padx=5)
    
    def create_fretboard_section(self, parent):
        fretboard_frame = ttk.LabelFrame(parent, text="Guitar Fretboard", padding="10")
        fretboard_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create fretboard display
        fretboard_canvas = tk.Canvas(fretboard_frame, bg="white", height=150)
        fretboard_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw fretboard
        string_height = 20
        fret_width = 40
        
        # Draw strings
        for i in range(6):
            y = 25 + i * string_height
            fretboard_canvas.create_line(50, y, 50 + fret_width * self.fretboard.num_frets, y, width=1 + (5-i)/2)
            
            # String label
            note = self.fretboard.strings[i][0]["note_name"] + str(self.fretboard.strings[i][0]["number"])
            fretboard_canvas.create_text(30, y, text=note)
        
        # Draw frets
        for i in range(self.fretboard.num_frets + 1):
            x = 50 + i * fret_width
            fretboard_canvas.create_line(x, 25, x, 25 + 5 * string_height, width=2 if i == 0 else 1)
            
            # Fret number
            if i > 0:
                fretboard_canvas.create_text(x - fret_width/2, 10, text=str(i))
        
        # Create clickable positions
        self.fretboard_buttons = []
        for string in range(6):
            string_buttons = []
            for fret in range(self.fretboard.num_frets):
                x = 50 + fret * fret_width + fret_width/2
                y = 25 + string * string_height
                
                note = self.fretboard.strings[string][fret]
                button = fretboard_canvas.create_oval(x-8, y-8, x+8, y+8, fill="white", outline="black")
                
                # Bind click event
                fretboard_canvas.tag_bind(button, "<Button-1>", 
                                         lambda event, s=string, f=fret: self.select_fretboard_note(s, f))
                
                string_buttons.append(button)
            self.fretboard_buttons.append(string_buttons)
        
        # Control buttons
        button_frame = ttk.Frame(fretboard_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        add_chord_button = ttk.Button(button_frame, text="Add Fretboard Chord", 
                                     command=lambda: self.add_current_chord("Fretboard"))
        add_chord_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="Clear Selection", command=self.clear_selection)
        
