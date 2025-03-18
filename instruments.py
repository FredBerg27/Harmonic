import time
import os
from pygame import mixer
from pygame.mixer import Sound

class Instrument:
    def __init__(self):
        self.note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        mixer.init()
        self.sounds = {}
        self.bind_notes()
    
    def set_notes(self, number, first_note):
        # medium is that by which notes are played
        medium = [None] * number 
        
        current_note = first_note.copy()
        medium[0] = current_note.copy()
        
        for i in range(1, number):
            note_idx = self.note_names.index(current_note["note_name"])
            
            if note_idx == 11:
                current_note["note_name"] = "C"
                current_note["number"] = int(current_note["number"]) + 1
            else:
                current_note["note_name"] = self.note_names[note_idx + 1]
                
            medium[i] = current_note.copy()
            
        return medium
    
    def bind_notes(self):
        sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
        if not os.path.exists(sounds_dir):
            os.makedirs(sounds_dir)
            print(f"Created sounds directory at {sounds_dir}")
            print("Please add sound files in format Note+Octave.wav (e.g., C3.wav)")
            return
            
        for file_name in os.listdir(sounds_dir):
            if file_name.endswith(".wav"):
                note_part = file_name.split(".")[0]
                if "+" in note_part:
                    parts = note_part.split("+")
                    note_name = parts[0]
                    number = parts[1]
                    note_key = f"{note_name}+{number}"
                    self.sounds[note_key] = Sound(os.path.join(sounds_dir, file_name))
                
    def play_note(self, note):
        file_match = f"{note['note_name']}+{note['number']}"
        if file_match in self.sounds:
            self.sounds[file_match].play()
        else:
            print(f"No sound file found for {file_match}")
            

class Fretboard(Instrument):
    def __init__(self):
        super().__init__()  
        self.num_frets = 21  # includes empty fret
        self.strings = [None] * 6  # 6 strings for guitar
        self.current_tuning = "standard"
        self.set_tuning(self.current_tuning)

    def set_tuning(self, tuning):
        tunings = [
            {
                "name": "standard",
                "notes": [
                    {"note_name": "E", "number": 1},
                    {"note_name": "A", "number": 1},
                    {"note_name": "D", "number": 2},
                    {"note_name": "G", "number": 2},
                    {"note_name": "B", "number": 2},
                    {"note_name": "E", "number": 3}
                ]
            },
            {
                "name": "Atmospheric",
                "notes": [
                    {"note_name": "E", "number": 1},
                    {"note_name": "B", "number": 1},
                    {"note_name": "E", "number": 2},
                    {"note_name": "F#", "number": 2},
                    {"note_name": "B", "number": 2},
                    {"note_name": "E", "number": 3}
                ]
            },
            {
                "name": "Drop D",
                "notes": [
                    {"note_name": "D", "number": 1},
                    {"note_name": "A", "number": 1},
                    {"note_name": "D", "number": 2},
                    {"note_name": "G", "number": 2},
                    {"note_name": "B", "number": 2},
                    {"note_name": "E", "number": 3}
                ]
            },
            {
                "name": "Open G",
                "notes": [
                    {"note_name": "D", "number": 1},
                    {"note_name": "G", "number": 1},
                    {"note_name": "D", "number": 2},
                    {"note_name": "G", "number": 2},
                    {"note_name": "B", "number": 2},
                    {"note_name": "D", "number": 3}
                ]
            }
        ]
    
        selected_tuning = next((t for t in tunings if t["name"].lower() == tuning.lower()), tunings[0])
        self.current_tuning = selected_tuning["name"]

        for string_idx, note in enumerate(selected_tuning["notes"]):
            # Need to use a copy of the note to avoid modifying the original
            self.strings[string_idx] = self.set_notes(self.num_frets, note.copy())
    
    def get_note_at_position(self, string_idx, fret):
        if 0 <= string_idx < len(self.strings) and 0 <= fret < self.num_frets:
            return self.strings[string_idx][fret]
        return None
              

class Keyboard(Instrument):
    def __init__(self):
        super().__init__()
        self.num_keys = 88
        self.first_note = {"note_name": "A", "number": 0}  # A0 is the first note on an 88-key piano
        self.keys = self.set_notes(self.num_keys, self.first_note)
    
    def get_note_at_key(self, key_idx):
        if 0 <= key_idx < self.num_keys:
            return self.keys[key_idx]
        return None


class Sheet_Music(Instrument):
    def __init__(self):
        super().__init__()
        self.song = []  # List of chords, where each chord is a list of notes
        self.song_name = "Untitled"
    
    def add_chord(self, chord):
        self.song.append(chord)
    
    def remove_chord(self, index):
        if 0 <= index < len(self.song):
            self.song.pop(index)
    
    def clear_song(self):
        self.song = []
    
    def set_song_name(self, name):
        self.song_name = name
    
    def play_song(self):
        for chord in self.song:
            # Play all notes in the chord simultaneously
            for note in chord:
                self.play_note(note)
            time.sleep(1)  # Wait 1 second between chords