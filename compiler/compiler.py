import io
import sys

def obtain_python(script: str):
    """
    Find the Python code in the input script, which follows
    by <Graph> and <Python> in the input script

    Params:
        script (str): input script
    
    Return:
        code (str): identified Python code from the input
    """
    not_timing = False  # If parsing frame time (i.e <...>) 
    not_quoting = True  # If parsing quotation, assuming '', "", and `` are the same

    start = 0           # Start index
    end = 0             # End index
    code = ''           # All code

    for i in range(len(script)):
        # Flip quoting bool if start/end quotating
        if script[i] == '\'' or script[i] == '\"' or script[i] == '\`':
            not_quoting = not not_quoting

        # Set start index if start timing and not quotating
        elif script[i] == '<' and not_quoting:
            # Append code if not timing
            if not_timing:
                code += script[start:i].strip() + '\n'
            start = i + 1
            not_timing = False

        # Set end index if end timing and not quotating
        elif script[i] == '>' and not_quoting:
            end = i

        # Reset start index if frame time == 'Python' or 'Graph'
        if script[start:end] == 'Python' or script[start:end] == 'Graph':
            start = end + 1
            not_timing = True

        # Append code if end of file but has some frames to add
        if i == len(script) - 1 and not_timing:
            code += script[start:i].strip() + '\n'

    return code

def embed_python(script: str):
    """
    Find, execute, and return printing strings from Python codes.

    Params:
        script (str): input script
    
    Return:
        output (str): string obtained from running identified Python code
    """

    # Redirect stdout to an in-memory buffer
    out_buffer = io.StringIO()
    sys.stdout = out_buffer

    # Execute code and retrieve printing values
    exec(obtain_python(script))
    output = out_buffer.getvalue()

    # Restore stdout to default for print()
    sys.stdout = sys.__stdout__

    return output

def set_frame(frames: list[set], indexes: set, eofs: set, object: str):
    """
    Set displaying object to their desinated frames

    Params:
        frames (list[set]): all frames
        indexes (set): targeted frames
        eofs (set): objects that display to eof
        object (str): object's id to display

    Return:
        frames (list[list]): all (modified) frames
    """
    curr_max = len(frames)
    new_max = len(frames)

    # Set frame
    for index in indexes:
        # Extend total frame if needed
        if index > curr_max:
            frames += [set() for _ in range(index - curr_max)]
            new_max = index
        frames[index - 1].add(object)

    # Add infinite objects
    for i in range(curr_max, new_max):
        for eof in eofs:
            frames[i].add(eof)

    return frames

def parse_script(script):
    """
    Parse input script to list of all frames with displaying object's id

    Params:
        script (str): input script
    
    Return:
        frames (list[list]): all frames
    """
    is_timing = False       # If parsing frame time (i.e <...>)   
    is_eof = False          # If parsing infinity (i.e. 'x-')
    is_next = False         # If parsing period (i.e. 'x-y')

    curr_object = ''        # Object's id
    fr_index = ''           # From index
    to_index = ''           # To index

    indexes = set()         # All indexes
    eofs = set()            # All object displayed to eof
    frames = [set()]        # All frames

    for i in range(len(script)):
        # Set frame and reset objects if start timing
        if script[i] == '<':
            # Put to infinite list if eof
            if is_eof:
                eofs.add(curr_object)

            frames = set_frame(frames, indexes, eofs, curr_object)

            # Reset
            curr_object = ''
            indexes = set()
            is_timing = True
            is_eof = False
        
        # Add index to indexes and reset temp indexes if end timing or see ','
        elif script[i] == '>' or script[i] == ',':
            # Put to eof if see '-' but have no to_index 
            if is_next and to_index == '':
                is_eof = True

            # Continue if indexes are not number (e.g. Python, Graph)
            try:
                start = int(fr_index)
                end = int(to_index) if to_index != '' else len(frames) if is_next else start;
                indexes.update(range(start, end + 1))
            except ValueError:
                continue

            # Reset
            fr_index = ''
            to_index = ''
            if script[i] == '>':
                is_timing = False
                is_next = False

        # Set is_next = True if see '-'
        elif script[i] == '-':
            is_next = True;
        
        # Otherwise, append char to to_index/fr_index/curr_object
        elif script[i] != ' ':
            if is_timing:
                if is_next:
                    to_index += script[i]
                else:
                    fr_index += script[i]
            else:  
                curr_object += script[i]

        # Set frame if end of file but has some frames to add
        if i == len(script) - 1 and len(indexes) != 0:
            frames = set_frame(frames, indexes, eofs, curr_object)
			
    return frames

def main():
    script = """
        <1> Textbox1
        <2> Textbox5
        <1, 5> Textbox1
        <3, 6> Textbox3
        <2-4> Textbox4
        <Graph> Graph1 = {'nodes': ['Shape1', 'Shape2'], 'edges': [['Shape1', 'Shape2']]}
        <Python> 
        print(f'<1-> {Graph1["nodes"][0]}')       
    """
    embed = embed_python(script)
    script = (embed + script).replace("\n", "").strip()
    parsed = parse_script(script)
    print(f'List of size ({len(parsed)},): {parsed}')

if __name__ == "__main__":
    main()