# Plans:
# related keys
# tone recognition
# tone playing
# image acquisition
# image classification (different script)
# conversion of wavelength values to HZ to tones
# GUI with a guitar neck


standard_tuning = ['E','A','D','G','B','E']

chromatic_scale = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']

chromatic_scale_doubled = chromatic_scale + chromatic_scale

scale_patterns = {
    'major_scale': [2,4,5,7,9,11],
    'minor_scale': [2,3,5,7,8,10],
    'pentatonic_scale': [2,4,7,9],
    'minor_pentatonic_scale': [3,5,7,9],
    'melodic_minor_scale': [2,3,5,7,9,11],
    'harmonic_minor_scale': [2,3,5,7,8,11],
    'dorian_scale': [2,3,5,7,9,10],
    'phrygian_scale': [1,3,5,7,8,10],
    'lydian_scale': [2,4,6,7,9,11],
    'mixolydian_scale': [2,4,5,7,9,10],
    'locrian_scale': [1,3,5,6,8,10],
    }

chord_patterns = {
    'major': [1,3,5],
    'minor': [1,'3b',5],
    'diminished': [1,'3b','5b'],
    'suspended_4th': [1,4,5],
    'suspended_2nd': [1,2,5],
    'fifth': [1,5],
    'minor_sixth': [1,'3b',5,6],
    'minor_flat_sixth': [1,'3b',5,'6b'],
    'major_add_9': [1,3,5,9],
    'minor_add_9': [1,'3b',5,9],
    'sixth': [1,3,5,6],
    'major_6_add_9': [1,3,5,6,9],
    'minor_6_add_9': [1,'3b',5,6,9],
    'major_7': [1,3,5,7],
    'seventh_dominant': [1,3,5,'7b'],
    'seventh_dominant_suspended_4': [1,4,5,'7b'],
    'minor_7': [1,'3b',5,'7b'],
    'minor_7_flat_5': [1,'3b','5b','7b'],
    'ninth_dominant': [1,3,5,'7b',9],
    'ninth_dominant_suspended_4': [1,4,5,'7b',9],
    'major_9': [1,3,5,7,9],
    'minor_9': [1,'3b',5,'7b',9],
    'major_7_flat_9': [1,3,5,'7b','9b'],
    'major_7_sharp_9': [1,3,5,'7b','10b'],
    'major_7_sharp_11': [1,3,5,'7b',9,'12b'],
    'eleventh_dominant': [1,5,'7b',9,11],
    'major_11': [1,3,5,7,9,11],
    'minor_11': [1,'3b',5,'7b',9,11],
    'thirteenth_dominant': [1,5,'7b',9,11,13],
    'thirteenth_dominant_suspended_4': [1,4,5,'7b',9,13],
    'major_13_flat_9': [1,3,5,'7b','9b',13],
    'major_13_sharp_9': [1,3,5,'7b','10b',13],
    'major_13': [1,3,5,7,9,13],
    'minor_11': [1,'3b',5,'7b',9,13],                
    }

def scale_builder(scale_pattern, key):

    key = key.upper()
    scale = []
    scale.append(key)
    key_index = chromatic_scale_doubled.index(key)

    for interval in scale_pattern:
        tonic = key_index
        subsequent_note_index = interval + tonic
        scale.append(chromatic_scale_doubled[subsequent_note_index])

    return scale

def chord_builder(scale_pattern, root, chord_pattern):

    root = root.upper()
    scale = scale_builder(scale_pattern, root)
    scale_extended = scale + scale
    chord = []
    for interval in chord_patterns.get(chord_pattern):
        if type(interval) is str:
            chord.append(chromatic_scale_doubled[chromatic_scale_doubled.index(scale_extended[int(interval[:-1])-1])-1])
        else:
            index = interval - 1
            chord.append(scale_extended[index])

    return scale, chord, scale_pattern

def all_scales_and_chords():

    all_scales = {scale: [scale_builder(scale_patterns.get(scale),tone) for tone in chromatic_scale] for scale in scale_patterns}

    all_chords = {tone + " " + chord: chord_builder(scale_patterns.get('major_scale'),tone,chord)[1]
                                       for chord in chord_patterns for tone in chromatic_scale}
    
    return all_scales, all_chords

def scale_chords(scale_pattern, key):

    scale = scale_builder(scale_pattern, key)

    all_chords = all_scales_and_chords()[1]

    chords_in_key_dictionary = {}

    for note in scale:
        key = scale_builder(scale_pattern, note)
        chords = {chord: all_chords[chord] for chord in all_chords if all_chords[chord][0] == note}
        chords_in_interval = {chord: chords[chord] for chord in chords if set(chords[chord]).issubset(scale) is True}
        chords_in_key_dictionary[scale.index(note) + 1] = chords_in_interval

    return chords_in_key_dictionary

def all_chords_with_scales(scale_pattern):

    #all_chords_in_all_keys_in_all_scales = {scale_pattern: {tone: scale_chords(scale_pattern, tone) for tone in chromatic_scale for scale_pattern in scale_patterns}}
        
    all_chords_in_all_keys = {tone: scale_chords(scale_pattern, tone) for tone in chromatic_scale}

    return all_chords_in_all_keys

def key_finder(chords):
    
    #all_chords_in_all_keys = all_chords_with_scales(scale_pattern)

    #keys = {}
    scales_with_keys = {}
    
    for scale_pattern in scale_patterns:
        all_chords_in_all_keys = all_chords_with_scales(scale_patterns.get(scale_pattern))
        scale = scale_patterns.get(scale_pattern)
        keys = {}

        for tone in all_chords_in_all_keys:
            key_chords = {}
            for interval in all_chords_in_all_keys[tone]:
                for chord in chords:
                    if chord in all_chords_in_all_keys[tone][interval].keys():
                        key_chords[interval] = chord
            if len(key_chords) >= len(chords):
                keys[tone] = key_chords

        if len(keys) > 0:
            scales_with_keys[scale_pattern] = keys
        
    return chords, scales_with_keys, all_chords_in_all_keys

def chord_finder(notes):
    # pass a list of notes and get a list of possible chords
    # and a separate list of possible chords where the root is not first
    print (notes)

# GET DATA!!!

## EXAMPLE OF GETTING A SCALE
'''
scale_pattern = scale_patterns.get('major_scale')
key = "C"

scale = scale_builder(scale_pattern, key)
'''
## EXAMPLE OF GETTING A CHORD
'''
scale_pattern = scale_patterns.get('major_scale')
root = "C"
chord_pattern = 'major'

chord = chord_builder(scale_pattern, root, chord_pattern)[1]
'''
## EXAMPLE OF GETTING ALL OF THE CHORDS THAT GO WITH A KEY - includes a print
'''
scale_pattern = scale_patterns.get('major_scale')
key = "F"

chords_in_key = scale_chords(scale_pattern, key)

for interval in chords_in_key:
    for chord in chords_in_key[interval]:
        print (interval, chord, chords_in_key[interval][chord])
 '''
## EXAMPLE OF GETTING ALL CHORDS FOR ALL KEYS
'''
scale_pattern = scale_patterns.get('major_scale')

all_chords = all_chords_with_scales(scale_pattern)

for note in all_chords:
    print (note, '----------')
    for interval in all_chords[note]:
        print (interval)
        print (all_chords[note][interval])
'''
## EXAMPLE OF GETTING ALL KEYS FOR SOME SPECIFIC CHORDS
# chords for a version of high and dry - NOT FINDING THE KEY OF A!!!!!
chords = ['F# seventh_dominant', 'A major', 'E major', 'E suspended_4th']

chords, keys, all_chords_in_all_keys = key_finder(chords)

for key in keys:
    print (key, keys[key])

