import sys
import json
from compiler import *

def json_to_html(json_data):
    id_to_text = {}
    id_to_svg = {}
    id_to_style = {}
    scripts = {}
    if json_data["text"] != None:
        texts = json_data["text"]
        for text in texts:
            id_to_text[text['id']] = text["content"].split("\n")
            id_to_svg[text['id']] = text["svg"]
            id_to_style[text['id']] = text["style"]
    if json_data["image"] != None:
        imgs = json_data["image"]
        for img in imgs:
            id_to_text[img['id']] = img["content"]
            id_to_svg[img['id']] = img["svg"].replace("href", "data-src").replace("<image", '<image referrerpolicy="no-referrer"')
            id_to_style[img['id']] = img["style"]
    if json_data["table"] != None:
        table = json_data["table"]
        for tab in table:
            id_to_text[tab['id']] = tab["content"].split(";")
            
            for row in range(len(id_to_text[tab['id']])):
                
                id_to_text[tab['id']][row] = id_to_text[tab['id']][row].split(",")
            id_to_svg[tab['id']] = tab["svg"]
            id_to_style[tab['id']] = tab["style"]
            

    if json_data["katex"] != None:
        katex = json_data["katex"]
        for kat in katex:
            id_to_text[kat['id']] = kat["content"]
            id_to_svg[kat['id']] = kat["svg"]
            id_to_style[kat['id']] = kat["style"]
            
        
    for diagram in json_data["diagram"]:
        scripts[diagram['id']] = diagram["script"].replace("\n", "")
        # print(scripts)

    start = 0	# <
    end = 0	# >
    current_frame = 0
    current_id = ''
    parsed = {}
    custom_pos = False
    try:
        for script in scripts:
            parsed[script] = parse_script(scripts[script])
        print(parsed)
    except: 
        return "err"
    
    #print(frame_to_id)
        
    html_output = "<!doctype html>\n \
     <html lang=\"en\">\n \
	<head>\n \
		<meta charset=\"utf-8\">\n \
		<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no\">\n \
		<title>reveal.js</title>\n \
		<link rel=\"stylesheet\" href=\"dist/reset.css\">\n \
		<link rel=\"stylesheet\" href=\"dist/reveal.css\">\n \
		<link rel=\"stylesheet\" href=\"dist/theme/white.css\">\n \
		<!-- Theme used for syntax highlighted code -->\n \
		<link rel=\"stylesheet\" href=\"plugin/highlight/monokai.css\">\n \
	</head>\n \
	<body>\n \
		<div class=\"reveal\">\n \
			<div class=\"slides\">"
    
    # sorted_frame_to_id = dict(sorted(frame_to_id.items()))
    for diagram in parsed:
        for frame in parsed[diagram]['frames']:
            if frame != set():
                frame = sorted(frame)
            html_output += "<section data-auto-animate "
            for id in frame:
                if ("Text" in id or "Code" in id or "Equation" in id):
                    end = ""
                    start = ""
                    if ('Code' in id):
                        if  html_output.strip()[-1]!='>' and html_output.strip()[-1]!=']' :
                            html_output+='>'
                        html_output += '<pre data-id="code"> <code class="hljs python" data-trim data-line-numbers data-noescape >' 
                    #parsed script pos
                    if '\\' in id:
                        ids = id.split("\\")
                        num = ids[1:]
                        print(num)

                        if num[0] == 'p':
                            custom_pos = True
                        else:
                            if len(num) > 1:
                                end = num[1]
                            start = int(num[0])
                        id = ids[0]
                    content = id_to_text[id]
                    if end == "" and start !="":
                        if start > len(content):
                            pass
                        else: content = list([content[start]])
                    if end =="e":
                        content = content[start:]
                    elif end.isdigit(): content = content[start:int(end)]
                    # print(content)
                    if (custom_pos):
                        html_output += f" style='text-align:left!important; position: absolute!important; padding-bottom: {(1 - int(id_to_style[id]['position'].split(' ')[0])/800)*100}%!important;'>"
                        custom_pos = False
                    if not custom_pos and (html_output.strip()[-1]!='>' and html_output.strip()[-1]!=']') :
                        html_output+='>'
                    if "Equation" in id:
                        html_output += '\[' + content + '\]'
                    else:
                        for i in content:
                            if ('Text' in id):
                                html_output += '<p>'
                            html_output += i + "\n"
                            if ('Text' in id):
                                html_output += '</p>'

                    if ('Code' in id):
                        html_output += "</code></pre>"
                #For Table
                elif "Table" in id:
                    if  html_output.strip()[-1]!='>'  and  html_output.strip()[-1]!=']' :
                        html_output+='>'
                    html_output += '<table style="empty-cells: show!important;" >'
                    selected_row = ""
                    selected_collumm = ""
                    is_select = False
                    if '\\' in id:
                        is_select = True
                        ids = id.split("\\")
                        num = ids[1:]
                        print(num)
                        if len(num) > 1:
                            selected_collumm = num[1]
                        selected_row = int(num[0])
                        id = ids[0]
                    content = id_to_text[id]
                    #set no. of row and collumn
                    rows = len(content)
                    cols  = len(content[0])
                    
                    if selected_row !="":

                        if selected_row > len(content):
                            is_select = False
                        else: 
                            content = content[selected_row]
                        
                    if selected_collumm !="":
                        if int(selected_collumm) > len(content[0]):
                            is_select = False
                    
                    for row in range(rows):
                        html_output+= " <tr>"
                        for col in range(cols):
                            html_output+= "<th>"
                            
                            if content[row][col] != "":
                                html_output+= content[row][col]
                            
                            html_output+= "</th>"
                            
                        html_output+= "</tr>"
                        
                    html_output += '</table>'
                    
                else:
                    if  html_output.strip()[-1]!='>' and  html_output.strip()[-1]!=']':
                        print(html_output[-1])
                        html_output+='>'
                    html_output += id_to_svg[id]+ "\n"
            if  html_output.strip()[-1]!='>' and  html_output.strip()[-1]!=']' :
                html_output+='>'
            html_output += "</section>\n"
        
    html_output += "</div>\n \
		</div>\n \
		<script src=\"dist/reveal.js\"></script>\n \
		<script src=\"plugin/notes/notes.js\"></script>\n \
		<script src=\"plugin/markdown/markdown.js\"></script>\n \
		<script src=\"plugin/highlight/highlight.js\"></script>\n \
        <script src=\"plugin/math/math.js\"></script>\n \
		<script>\n \
			Reveal.initialize({\n \
				hash: true,\n \
				plugins: [ RevealMarkdown, RevealHighlight, RevealNotes , RevealMath.KaTeX]\n\
			});\n \
		</script>\n \
	</body>\n \
    </html>"	
			
    return html_output

def main():
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    
    # input_file_path = "compiler/tmp/1716118137263.json"
    # output_file_path = "./reveal.js/out.html"

    with open(input_file_path, 'r') as file:
        data = json.load(file)
    with open(output_file_path, 'w') as file:
        file.write(json_to_html(data))

if __name__ == "__main__":
    main()
