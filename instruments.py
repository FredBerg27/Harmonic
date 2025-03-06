class Instrument:
    def __init__(self):
        self.note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    def set_notes(self, number, first_note):
        # medium is that by which notes are played
        medium = [None] * number 
        
        current_note = first_note.copy()
        medium[0] = current_note.copy()
        
        for i in range(1, number):
            note_idx = self.note_names.index(current_note["note_name"])
            
            if note_idx == 11:
                current_note["note_name"] = "C"
                current_note["number"]  = int(current_note["number"]) + 1
            else:
                current_note["note_name"] = self.note_names[note_idx + 1]
                
            medium[i] = current_note.copy()
            
        return medium

class Fretboard(Instrument):
    def __init__(self):
        super().__init__()  
        self.num_frets = 21  # includes empty fret
        self.current_tuning = "standard"  # Add this line to track current tuning
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
            }
        ]
    
        selected_tuning = next((t for t in tunings if t["name"].lower() == tuning.lower()), tunings[0])

        for string_idx, note in enumerate(selected_tuning["notes"]):
            # Need to use a copy of the note to avoid modifying the original
            self.strings[string_idx] = self.set_notes(self.num_frets, note.copy())

    def get_note_at(self, string_idx, fret):
        if 0 <= string_idx < len(self.strings) and 0 <= fret < self.num_frets:
            return self.strings[string_idx][fret]
        return None              

class Keyboard(Instrument):
    def __init__(self):
        super().__init__()
        self.num_keys = 88
        self.keys = [{}]
        self.first_note = {"note_name" : "C", "number" : "1"}
        self.set_notes(self.num_keys, self.first_note)




                






            