import sys
import json
from compiler import *
from Parser import *

def json_to_html(json_data):
    texts = json_data["text"]
    imgs = json_data["image"]
    id_to_text = {}
    id_to_svg = {}
    for text in texts:
        id_to_text[text['id']] = text["content"]
        id_to_svg[text['id']] = text["svg"]
    for img in imgs:
        id_to_text[img['id']] = img["content"]
        id_to_svg[img['id']] = img["svg"].replace("href", "data-src")
    script = json_data["animationScript"]
    print(script)
    script = script.replace("\n", "")

    start = 0	# <
    end = 0	# >
    current_frame = 0
    current_id = ''
    parsed = {}
    try:
        parsed = parse_script(script)
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
		<link rel=\"stylesheet\" href=\"dist/theme/black.css\">\n \
		<!-- Theme used for syntax highlighted code -->\n \
		<link rel=\"stylesheet\" href=\"plugin/highlight/monokai.css\">\n \
	</head>\n \
	<body>\n \
		<div class=\"reveal\">\n \
			<div class=\"slides\">"
    
    # sorted_frame_to_id = dict(sorted(frame_to_id.items()))
    for frame in parsed["frames"]:
        html_output += "<section data-auto-animate>"
        for id in frame:
            if ('Textbox2' in id):
                html_output += '<pre data-id="code"> <code class="hljs python" data-trim data-line-numbers data-noescape >' + id_to_text[id] + "</code></pre>"
            else:
                html_output += id_to_svg[id]+ "\n"
        html_output += "</section>\n"
        
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
    # input_file_path = sys.argv[1]
    # output_file_path = sys.argv[2]
    
    input_file_path = "compiler/tmp/1710991185850.json"
    output_file_path = "compiler\out.html"

    with open(input_file_path, 'r') as file:
        data = json.load(file)
    with open(output_file_path, 'w') as file:
        file.write(json_to_html(data))

if __name__ == "__main__":
    main()
