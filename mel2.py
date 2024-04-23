import random
import midiutil
import matplotlib.pyplot as plt

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

def export_midi(melody, filename, tempo=120, octave_offset=3):
    midi = midiutil.MIDIFile(1)
    track = 0
    time = 0
    midi.addTempo(track, time, tempo)

    ticks_per_bar = 4  # Assuming 4 beats per bar

    for note, duration in melody:
        note_value = note_indices[note] + 12 * octave_offset  # Adjust note value with octave offset
        midi.addNote(track, 0, note_value, time, duration, 100)

        time += duration * ticks_per_bar  # Increment time by duration in ticks

    with open(filename, "wb") as f:
        midi.writeFile(f)
        
def visualize_note_frequency(melody):
    note_counts = {}
    for note, _ in melody:
        note_counts[note] = note_counts.get(note, 0) + 1

    # Prepare data for the pie chart
    labels = list(note_counts.keys())
    sizes = list(note_counts.values())

    # Create the pie chart
    plt.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title("Note Frequency Distribution")
    plt.show()

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

    export_filename = input("Enter MIDI filename (default 'output.mid'): ").strip()
    
    # Set default midi name as 'output' if none entered.
    if not export_filename:
        export_filename = "output.mid"
    export_midi(melody, export_filename)
    print(f"Melody exported to {export_filename}")
    
    visualize_note_frequency(melody)
    
if __name__ == '__main__':
    main()