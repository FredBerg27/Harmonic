import tkinter as tk
from tkinter import ttk
import instruments

Fretboard = instruments.Fretboard()
Keyboard = instruments.Keyboard()

class GuitarUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Guitar Fretboard Visualizer")
        
        self.guitar = Fretboard()
        self.selected_notes = []
        
        self.create_widgets()
        self.draw_fretboard()
        
    def create_widgets(self):
        # Create frame for controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, sticky="w")
        
        # Tuning selector
        ttk.Label(control_frame, text="Tuning:").grid(row=0, column=0, padx=5, pady=5)
        self.tuning_var = tk.StringVar(value=self.guitar.current_tuning)
        tuning_combo = ttk.Combobox(control_frame, textvariable=self.tuning_var, 
                                    values=["standard", "atmospheric"], width=15) #Change this line to add tunings
        tuning_combo.grid(row=0, column=1, padx=5, pady=5)
        tuning_combo.bind("<<ComboboxSelected>>", self.change_tuning)
        
        # Clear selection button
        clear_btn = ttk.Button(control_frame, text="Clear Selection", command=self.clear_selection)
        clear_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Play button
        play_btn = ttk.Button(control_frame, text="Play Selected Notes", command=self.play_notes)
        play_btn.grid(row=0, column=3, padx=5, pady=5)
        
        # Create frame for fretboard
        self.fretboard_frame = ttk.Frame(self.root, padding="10")
        self.fretboard_frame.grid(row=1, column=0, sticky="nsew")
        
        # Selected notes display
        ttk.Label(self.root, text="Selected Notes:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.notes_display = ttk.Label(self.root, text="")
        self.notes_display.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        
    def draw_fretboard(self):
        # Clear the frame first
        for widget in self.fretboard_frame.winfo_children():
            widget.destroy()
        
        # Draw fret numbers
        for i in range(self.guitar.num_frets):
            fret_label = ttk.Label(self.fretboard_frame, text=str(i), width=4, 
                                   borderwidth=1, relief="solid", padding=5)
            fret_label.grid(row=0, column=i+1)
        
        # Draw strings and frets
        for string_idx in range(6):
            # String label (shows open string note)
            open_note = self.guitar.strings[string_idx][0]
            string_label = ttk.Label(self.fretboard_frame, 
                                    text=f"{open_note['note_name']}{open_note['number']}", 
                                    width=4, borderwidth=1, relief="solid", padding=5)
            string_label.grid(row=string_idx+1, column=0)
            
            # Draw each fret on this string
            for fret in range(self.guitar.num_frets):
                note = self.guitar.strings[string_idx][fret]
                btn = tk.Button(self.fretboard_frame, 
                               text=f"{note['note_name']}{note['number']}", 
                               width=4, height=2, 
                               bg="white")
                btn.grid(row=string_idx+1, column=fret+1)
                
                # Command to handle note selection
                btn.config(command=lambda s=string_idx, f=fret, b=btn: self.select_note(s, f, b))
    
    def select_note(self, string_idx, fret, button):
        note = self.guitar.get_note_at(string_idx, fret)
        note_info = {
            "string": string_idx,
            "fret": fret,
            "note": f"{note['note_name']}{note['number']}",
            "button": button
        }
        
        # Check if already selected
        for i, selected in enumerate(self.selected_notes):
            if selected["string"] == string_idx and selected["fret"] == fret:
                # Deselect
                self.selected_notes.pop(i)
                button.config(bg="white")
                self.update_notes_display()
                return
        
        # Add to selected
        self.selected_notes.append(note_info)
        button.config(bg="light blue")
        self.update_notes_display()
    
    def update_notes_display(self):
        if not self.selected_notes:
            self.notes_display.config(text="No notes selected")
            return
            
        notes_text = ", ".join([f"String {n['string']+1}, Fret {n['fret']}: {n['note']}" 
                               for n in self.selected_notes])
        self.notes_display.config(text=notes_text)
    
    def clear_selection(self):
        for note in self.selected_notes:
            note["button"].config(bg="white")
        self.selected_notes = []
        self.update_notes_display()
    
    def change_tuning(self, event):
        new_tuning = self.tuning_var.get()
        self.guitar.set_tuning(new_tuning)
        self.clear_selection()
        self.draw_fretboard()
    
    def play_notes(self):
        # This would integrate with an audio library to play the selected notes
        # For now, we'll just print what would be played
        if not self.selected_notes:
            print("No notes to play")
            return
            
        print("Playing notes:")
        for note in self.selected_notes:
            print(f"- {note['note']} (String {note['string']+1}, Fret {note['fret']})")
        
        # Here you would add code to actually play the sounds
        # This could use a library like pygame.mixer, pyo, or pysynth


if __name__ == "__main__":
    root = tk.Tk()
    app = GuitarUI(root)
    root.mainloop()