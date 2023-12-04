import sys 
import json 
import pandas as pd

def preprocess_script(script):
    script = script.replace("&lt;", "<")
    script = script.replace("&gt;", ">")
    return script

def get_script_map(script):
    script_map = {}
    script_line = script.split("\n")
    for line in script_line: 
        for i in range(len(line)): 
            if line[i] == "<":
                start = i+1
            if line[i] == ">":
                stop = i
                object_id = line[stop+1:].strip()
                object_sequence_slice = line[start:stop]
                script_map[object_id] = object_sequence_slice
    return script_map

def get_text_script_map(script_map, textbox_list):
    text_script_map = {}
    keylist = list(script_map.keys())
    for i in range(len(keylist)): 
        for id in textbox_list: 
            if keylist[i].startswith(id): 
                text_script_map.update({keylist[i] : script_map[keylist[i]]})
    return text_script_map

def get_enumerated_text_script_map(text_script_map, textbox_shape): 
    enum_text_script_map = {}
    for obj_id, obj_seq in text_script_map.items():
        start_tbox_cell = 0 
        stop_tbox_cell = 0 
        new_obj_id = ""

        # case 1: whole box, no slicing 
        if "[" not in obj_id: 
            start_tbox_cell = 1; 
            stop_tbox_cell = textbox_shape[obj_id]
            new_obj_id = obj_id

            for i in range(start_tbox_cell, stop_tbox_cell+1):
                enum_text_script_map[new_obj_id + "[" + str(i) + "]"] = obj_seq
        # case 2: slicing 
        elif ":" in obj_id: 
            start_left_index = 0 
            end_left_index = 0 
            start_right_index = 0 
            end_right_index = 0 
            for i in range(len(obj_id)): 
                if obj_id[i] == "[": 
                    start_left_index = i+1 
                elif obj_id[i] == ":": 
                    end_left_index = i 
                    start_right_index = i+1 
                elif obj_id[i] == "]": 
                    end_right_index = i 
            
            str_start_tbox_cell = obj_id[start_left_index : end_left_index]
            str_stop_tbox_cell = obj_id[start_right_index : end_right_index]
            new_obj_id = obj_id[:start_left_index-1]
            start_tbox_cell = 0 if str_start_tbox_cell == "" else int(str_start_tbox_cell)
            stop_tbox_cell = textbox_shape[new_obj_id] if str_stop_tbox_cell == "" else int(str_stop_tbox_cell)
            
            for i in range(start_tbox_cell, stop_tbox_cell+1): 
                enum_text_script_map[new_obj_id + "[" + str(i) + "]"] = obj_seq
        
        # case 3: one cell of textbox already identified, append as is 
        else: 
            enum_text_script_map[obj_id] = obj_seq

    return enum_text_script_map

def get_split_text_map(data): 
    split_text_map = {} # text_id: [text_line]
    for i in range(len(data["text"])):
        this_text_box_id = data["text"][i]["id"]
        this_text_box = data["text"][i]["content"].split("\n")
        split_text_map[this_text_box_id] = this_text_box
    return split_text_map

def get_textbox_shape(split_text_map):
    textbox_shape = {} # text_id: n_line
    textbox_list = list(split_text_map.keys())
    for i in range(len(textbox_list)): 
        textbox_shape[textbox_list[i]] = len(split_text_map[textbox_list[i]])
    return textbox_shape


def strip_sugarcoat(data, script): 
    script_lines = script.split("\n")
    new_script_lines = [] 

    # find all items that is NOT a textbox and add it to new_script_lines
    # add more (table, shape) when these objects are available 
    not_textbox_list = [] 
    for i in range(len(data["image"])):
        not_textbox_list.append(data["image"][i]["id"])
    for i in range(len(data["katex"])):
        not_textbox_list.append(data["katex"][i]["id"])
    
    for line in script_lines:
        for id in not_textbox_list: 
            if id in line: 
                new_script_lines.append(line)
    
    # now de-sugarcoat textbox script lines
    script_map = get_script_map(script)
    split_text_map = get_split_text_map(data)
    textbox_shape = get_textbox_shape(split_text_map)
    textbox_id_list = list(textbox_shape.keys())
    text_script_map = get_text_script_map(script_map, textbox_id_list)
    enum_script_map = get_enumerated_text_script_map(text_script_map, textbox_shape)

    for obj_id, obj_seq in enum_script_map.items():
        new_script_line = "<" + obj_seq + "> " + obj_id
        new_script_lines.append(new_script_line)
    
    new_script = "\n".join(new_script_lines)
    return new_script


def get_number_of_unit_items(data, split_text_map): 
    '''n_col, ended up not using this function at all'''
    n_text_line = 0
    for item in split_text_map.values(): 
        n_text_line += len(item)

    n_unit_sized_items = len(data["image"]) + len(data["katex"]) + n_text_line 
    return n_unit_sized_items


def get_number_of_frames(script_map):
    '''n_row'''
    sequence_slice = list(script_map.values())
    sequence_num = [] 
    for i in range(len(sequence_slice)): 
        if sequence_slice[i].find("-") == -1: 
            sequence_num.append(int(sequence_slice[i]))
        elif sequence_slice[i][-1] == "-": 
            sequence_num.append(int(sequence_slice[i][:-1])) 
        else: 
            tmp = sequence_slice[i].split("-")
            tmp = [int(k) for k in tmp]
            sequence_num.extend(tmp)

    n_frame = max(sequence_num)
    return n_frame

def get_object_index_map(script, n_frame):
    script_line = script.split("\n")
    object_index_map = {} # object_id: [object_index]

    for line in script_line: 
        for i in range(len(line)): 
            if line[i] == "<":
                start = i+1
            if line[i] == ">":
                stop = i
                object_id = line[stop+1:].strip()
                object_index_slice = line[start:stop]
                object_index = []
                if object_index_slice.find("-") == -1: 
                    object_index.append(int(object_index_slice))
                elif object_index_slice[-1] == "-": 
                    all_visible_frames = list(range(int(object_index_slice[:-1]), n_frame + 1))
                    object_index.extend(all_visible_frames)
                else: 
                    tmp = object_index_slice.split("-")
                    tmp = [int(k) for k in range(int(tmp[0]), int(tmp[1])+1)]
                    object_index.extend(tmp)
                object_index_map[object_id] = object_index

    return object_index_map

def get_parse_matrix(object_index_map, n_frame):
    col_label = object_index_map.keys()
    row_label = list(range(n_frame + 1))
    mat = pd.DataFrame(0, index=row_label, columns=col_label)

    for key, value in object_index_map.items(): 
        for i in value: 
            mat.loc[i, key] = 1
    
    return mat

def wrapper_get_parse_matrix(data, script):
    script_map = get_script_map(script)
    n_frame = get_number_of_frames(script_map)
    stripped_script = strip_sugarcoat(data, script)
    script_frame_map = get_object_index_map(stripped_script, n_frame)

    mat = get_parse_matrix(script_frame_map, n_frame)

    return mat

#------------- READ INPUT FILE -------------
# i don't know how to do the sys.argv thing so i put the input json 
# file in the same directory as this script and name it input.json :) 
with open('input.json') as f:
    data = json.load(f)

script = data["diagram"][0]["script"] 
script = preprocess_script(script)

print(wrapper_get_parse_matrix(data, script))
