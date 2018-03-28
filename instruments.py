# https://github.com/vishnubob/python-midi
import midi
import sys

if len(sys.argv) < 2:
	print "Usage: Send in a midi file"
	sys.exit(1)

pattern = midi.read_midifile(sys.argv[1])

# Manual note dictionary
notes = {}
notes[midi.C_3 ] = "C3"
notes[midi.Cs_3] = "C#3"
notes[midi.D_3 ] = "D3"
notes[midi.Ds_3] = "D#3"
notes[midi.E_3 ] = "E3"
notes[midi.F_3 ] = "F3"
notes[midi.Fs_3] = "F#3"
notes[midi.G_3 ] = "G3"
notes[midi.Gs_3] = "G#3"
notes[midi.A_3 ] = "A3"
notes[midi.As_3] = "A#3"
notes[midi.B_3 ] = "B3"
notes[midi.C_4 ] = "C4"
notes[midi.Cs_4] = "C#4"
notes[midi.D_4 ] = "D4"
notes[midi.Ds_4] = "D#4"
notes[midi.E_4 ] = "E4"
notes[midi.F_4 ] = "F4"
notes[midi.Fs_4] = "F#4"
notes[midi.G_4 ] = "G4"
notes[midi.Gs_4] = "G#4"
notes[midi.A_4 ] = "A4"
notes[midi.As_4] = "A#4"
notes[midi.B_4 ] = "B4"
notes[midi.C_5 ] = "C5"
notes[midi.Cs_5] = "C#5"
notes[midi.D_5 ] = "D5"
notes[midi.Ds_5] = "D#5"
notes[midi.E_5 ] = "E5"
notes[midi.F_5 ] = "F5"
notes[midi.Fs_5] = "F#5"
notes[midi.G_5 ] = "G5"
notes[midi.Gs_5] = "G#5"
notes[midi.A_5 ] = "A5"
notes[midi.As_5] = "A#5"
notes[midi.B_5 ] = "B5"
notes[midi.C_6 ] = "C6"

# Calculate for conversion, if needed
# TODO: Make this if needed!
note_min = midi.C_3
note_max = midi.C_6

# Current resolution
resolution = pattern.resolution

# Storage lists
song = []

invalid_notes = 0
num_notes = 0

# Keepin trak of an instrument(track) and all its bpms
class Instrument:
	def __init__(self):
		self.bpms = []
		self.notes = []

	def __nonzero__(self):
		return len(self.notes)

	def sort(self):
		sort


pattern.make_ticks_abs()
# Get all notes
for track in pattern:
	instrument = Instrument()
	for event in track:
		# Set the current tempo
		if type(event) is midi.SetTempoEvent:
			instrument.bpms.append({
				'bpm': int(event.get_bpm()),
				'tick': event.tick
				})
		# Set the current note event
		elif type(event) is midi.NoteOnEvent:
			if event.data[0] not in notes:
				invalid_notes += 1
				continue
			# Save for later use
			instrument.notes.append({
				'note': notes[event.data[0]],
				'tick': event.tick
				})
			num_notes += 1
	# Need at least one note to be valid
	if instrument:
		song.append(instrument)

# Let the user know
if invalid_notes:
	print "Found " + str(invalid_notes) + " invalid notes"
print "Found " + str(len(song)) + " tracks"
print "Found " + str(num_notes) + " notes"

# Create the charts
for instrument in song:
	chart = ""
	bpms = instrument.bpms[::-1]
	if bpms:
		bpm = bpms.pop()
		chart += "t:" + str(bpm['bpm'])
		if bpms:
			bpm = bpms.pop()
		else:
			bpm = None
	else:
		bpm = None
	prev = None
	for note in instrument.notes:
		# Update bpms
		if bpm and note['tick'] >= bpm['tick']:
			if chart:
				chart += ","
			chart += "t:" + str(bpm['bpm'])
			if bpms:
				bpm = bpms.pop()
			else:
				bpm = None
		if chart:
			# Chord
			if prev and prev['tick'] == note['tick']:
				chart += "+"
			else:
				chart += ","
		chart += note['note']
		prev = note
	print chart
