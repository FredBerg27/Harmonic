import tkinter as tk
from tkinter import ttk, simpledialog
from instruments import Fretboard, Sheet_Music

class HarmonicAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Harmonic Analysis Tool")
        self.root.geometry("1200x800")
        
        # Initialize instruments
        self.fretboard = Fretboard()
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
        
        # Create two main sections
        self.create_fretboard_section(main_frame)
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
        
        # Create fretboard display with explicit width
        self.fretboard_canvas = tk.Canvas(fretboard_frame, bg="white", height=150, width=1000)
        self.fretboard_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw fretboard
        string_height = 20
        fret_width = 40
        start_x = 100  # Increased to make room for labels
        start_y = 25
        
        # Draw strings
        for i in range(6):
            y = start_y + i * string_height
            self.fretboard_canvas.create_line(start_x, y, start_x + fret_width * self.fretboard.num_frets, y, width=1 + (5-i)/2)
            
            # String label with note name and octave - make it more visible
            note = self.fretboard.strings[i][0]
            self.fretboard_canvas.create_text(80, y, text=f"{note['note_name']}{note['number']}", 
                                           font=("Arial", 14, "bold"), fill="blue")
            
            # String number (1-6, from bottom to top) - make it more visible
            self.fretboard_canvas.create_text(40, y, text=str(6-i), font=("Arial", 14, "bold"), fill="red")
        
        # Draw frets
        for i in range(self.fretboard.num_frets + 1):
            x = start_x + i * fret_width
            self.fretboard_canvas.create_line(x, start_y, x, start_y + 5 * string_height, width=2 if i == 0 else 1)
            
            # Fret number (starting from 0) - make it more visible
            if i > 0:  # Skip the 0th fret (nut)
                self.fretboard_canvas.create_text(x - fret_width/2, 10, text=str(i-1), 
                                               font=("Arial", 14, "bold"), fill="green")
        
        # Add a title for the fretboard
        self.fretboard_canvas.create_text(start_x + (fret_width * self.fretboard.num_frets)/2, 5,
                                       text=f"Fretboard - {self.fretboard.current_tuning} Tuning",
                                       font=("Arial", 16, "bold"), fill="purple")
        
        # Create clickable positions
        self.fretboard_buttons = []
        for string in range(6):
            string_buttons = []
            for fret in range(self.fretboard.num_frets):
                x = start_x + fret * fret_width + fret_width/2
                y = start_y + string * string_height
                
                note = self.fretboard.strings[string][fret]
                button = self.fretboard_canvas.create_oval(x-8, y-8, x+8, y+8, fill="white", outline="black")
                
                # Bind click event
                self.fretboard_canvas.tag_bind(button, "<Button-1>", 
                                         lambda event, s=string, f=fret: self.select_fretboard_note(s, f))
                
                string_buttons.append(button)
            self.fretboard_buttons.append(string_buttons)
        
        # Control buttons
        button_frame = ttk.Frame(fretboard_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        add_chord_button = ttk.Button(button_frame, text="Add Chord", 
                                     command=lambda: self.add_current_chord("Fretboard"))
        add_chord_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="Clear Selection", command=self.clear_selection)
        clear_button.pack(side=tk.LEFT, padx=5)
    
    def create_sheet_music_section(self, parent):
        sheet_frame = ttk.LabelFrame(parent, text="Sheet Music", padding="10")
        sheet_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create listbox for chords
        self.chord_listbox = tk.Listbox(sheet_frame, height=10)
        self.chord_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Update chord list
        self.update_chord_list()
    
    def select_fretboard_note(self, string, fret):
        # Check if a note is already selected on this string
        for note in self.current_chord:
            if note.get('string') == string:
                # If a note is already selected on this string, deselect it first
                self.fretboard_canvas.itemconfig(self.fretboard_buttons[string][note.get('fret')], fill="white")
                self.current_chord.remove(note)
                break
        
        note = self.fretboard.get_note_at_position(string, fret)
        if note:
            # Add string and fret information to the note
            note['string'] = string
            note['fret'] = fret
            self.current_chord.append(note)
            # Highlight selected note in blue
            self.fretboard_canvas.itemconfig(self.fretboard_buttons[string][fret], fill="lightblue")
    
    def clear_selection(self):
        self.current_chord = []
        # Reset button colors
        for string in self.fretboard_buttons:
            for button in string:
                self.fretboard_canvas.itemconfig(button, fill="white")
    
    def add_current_chord(self, source):
        if self.current_chord:
            self.sheet_music.add_chord(self.current_chord.copy())
            self.update_chord_list()
            self.clear_selection()
    
    def update_chord_list(self):
        self.chord_listbox.delete(0, tk.END)
        for chord in self.sheet_music.song:
            chord_text = " ".join(f"{note['note_name']}{note['number']}" for note in chord)
            self.chord_listbox.insert(tk.END, chord_text)
    
    def clear_song(self):
        self.sheet_music.clear_song()
        self.update_chord_list()
    
    def play_full_song(self):
        self.sheet_music.play_song()

if __name__ == "__main__":
    root = tk.Tk()
    app = HarmonicAnalysisApp(root)
    root.mainloop()
