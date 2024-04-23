import random
import mido

# List of all note names
note_names = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]

# Dictionary to map note names and their variations(sharp & flat) to indices
note_indices = {
    "C": 0, "C#": 1, "Db": 1,
    "D": 2, "D#": 3, "Eb": 3,
    "E": 4,
    "F": 5, "F#": 6, "Gb": 6,
    "G": 7, "G#": 8, "Ab": 8,
    "A": 9, "A#": 10, "Bb": 10,
    "B": 11
}

# Function to generate major scale for a given root note
def major_scale(root):
    intervals = [2, 2, 1, 2, 2, 2, 1]
    scale = [root]
    current_note = root
    for interval in intervals:
        current_note += interval
        scale.append(current_note % 12)
    return scale

# Function to generate minor scale for a given root note
def minor_scale(root):
    intervals = [2, 1, 2, 2, 1, 2, 2]
    scale = [root]
    current_note = root
    for interval in intervals:
        current_note += interval
        scale.append(current_note % 12)
    return scale

# Generate major and minor scales for all keys and store in 'scales' dict
scales = {}
for i, note in enumerate(note_names):
    scales[note + " major"] = major_scale(i)
    scales[note + " minor"] = minor_scale(i)

# Define the durations in terms of bars for final output
durations = {
    1: "1 bar",
    0.5: "1/2 bar",
    0.25: "1/4 bar",
    0.125: "1/8 bar",
    0.0625: "1/16 bar"
}

# Function to generate random melody for a specified scale
def generate_melody(scale):
    melody = []
    total_duration = 0
    while total_duration < 4:
        note_index = random.choice(scale)
        note_name = note_names[note_index]
        duration = random.choice(list(durations.keys()))
        if total_duration + duration <= 4:
            melody.append((note_name, duration))
            total_duration += duration
    return melody

# Function to export melody as MIDI file
def export_melody(melody, scale_name, filename="generated_melody.mid"):
    midi = mido.MidiFile(ticks_per_beat=480)  # 480 ticks per beat is standard MIDI resolution
    track = mido.MidiTrack()
    midi.tracks.append(track)

    # Set tempo (default 120 bpm)
    micros_per_beat = int(mido.bpm2tempo(120))
    track.append(mido.MetaMessage('set_tempo', tempo=micros_per_beat))

    for note, duration in melody:
        note_number = note_indices[note] + 60  # Example: Middle C = MIDI note number 60 
        on_time = int(duration * 960)     # Convert duration (in bars) to MIDI ticks
        track.append(mido.Message('note_on', note=note_number, velocity=64, time=0))
        track.append(mido.Message('note_off', note=note_number, velocity=64, time=on_time))

    midi.save(filename)

# Main function
def main():
    scale_choice = input("Select a scale (leave empty for random scale): ").strip().capitalize()  # Capitalize input for consistency
    # If user inputs a scale name
    if scale_choice:
        if scale_choice in scales:
            selected_scale = scales[scale_choice]
            scale_name = scale_choice
        else:
            # Error handling for invalid names entered
            print("Invalid scale choice.")
            return
    # If the user wants a random scale to be chosen
    else:
        scale_name, selected_scale = random.choice(list(scales.items()))

    print(f"Selected Scale: {scale_name}")
    melody = generate_melody(selected_scale)
    print("Generated Melody:")
    for note, duration in melody:
        print(f"{note} ({durations[duration]})")
        
    export_melody(melody, scale_name)

if __name__ == "__main__":
    main()