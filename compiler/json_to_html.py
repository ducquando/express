import sys
import json

def json_to_html(json_data):
    texts = json_data["text"]
    id_to_text = {}
    for text in texts:
        id_to_text[text["id"]] = text["content"]
        
    script = json_data["animationScript"]
    script = script.replace("&lt;", "<")
    script = script.replace("&gt;", ">")
    script = script.replace("\n", "")

    start = 0	# <
    end = 0	# >
    current_frame = 0
    current_id = ''
    frame_to_id = {}
    for i in range(len(script)):
        if script[i] == '<':
            start = i
            if current_id != '':
                frame_to_id[current_frame] = current_id
        elif script[i] == '>':
            current_frame = int(script[start+1:i])
            current_id = ''
        elif script[i] != ' ':
            current_id += script[i]
        if i == len(script) - 1:
            if current_id != '':
                frame_to_id[current_frame] = current_id        
    
    #print(frame_to_id)
        
    html_output = "<!doctype html>\n \
     <html lang=\"en\">\n \
	<head>\n \
		<meta charset=\"utf-8\">\n \
		<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no\">\n \
		<title>reveal.js</title>\n \
		<link rel=\"stylesheet\" href=\"dist/reset.css\">\n \
		<link rel=\"stylesheet\" href=\"dist/reveal.css\">\n \
		<link rel=\"stylesheet\" href=\"dist/theme/black.css\">\n \
		<!-- Theme used for syntax highlighted code -->\n \
		<link rel=\"stylesheet\" href=\"plugin/highlight/monokai.css\">\n \
	</head>\n \
	<body>\n \
		<div class=\"reveal\">\n \
			<div class=\"slides\">"
    
    sorted_frame_to_id = dict(sorted(frame_to_id.items()))
    for frame, id in sorted_frame_to_id.items():
        if id in id_to_text:
            html_output += "<section>" + id_to_text[id] + "</section>\n"
    			
    html_output += "</div>\n \
		</div>\n \
		<script src=\"dist/reveal.js\"></script>\n \
		<script src=\"plugin/notes/notes.js\"></script>\n \
		<script src=\"plugin/markdown/markdown.js\"></script>\n \
		<script src=\"plugin/highlight/highlight.js\"></script>\n \
		<script>\n \
			// More info about initialization & config:\n \
			// - https://revealjs.com/initialization/\n \
			// - https://revealjs.com/config/\n \
			Reveal.initialize({\n \
				hash: true,\n \
				// Learn about plugins: https://revealjs.com/plugins/\n\
				plugins: [ RevealMarkdown, RevealHighlight, RevealNotes ]\n\
			});\n \
		</script>\n \
	</body>\n \
    </html>"	
			
    return html_output

def main():
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    with open(input_file_path, 'r') as file:
        data = json.load(file)
    with open(output_file_path, 'w') as file:
        file.write(json_to_html(data))

if __name__ == "__main__":
    main()
