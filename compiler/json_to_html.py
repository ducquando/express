import sys
import json
from bs4 import BeautifulSoup

def json_to_html(json_data):
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
    
    pages = json_data['diagram'] 
    try:
        for page in pages:
            page_html = ''
            section_html = ''
            script = page['script']
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
            # find element in components list 
            components = page["components"]
            sorted_frame_to_id = dict(sorted(frame_to_id.items()))
            # iterate over script dictionary 
            for index, id in sorted_frame_to_id.items():
                print(index, id)
                component = next((item for item in components if item['id'] == id), None)
                # if (component == None):  
                #     raise Exception("component not defined")
                componentType = component["type"]
                print(componentType)
                match componentType: 
                    case "text": 
                        section_html += processText(component["content"], index)
                    case "image":
                        print(f"match content for item id {id}, index {index}")
                        section_html += processImg(component["content"], index)
                    case default: 
                        raise Exception("componentType not found")
            if (len(section_html) > 0):
                print(section_html)
                page_html += f"\n<section> \n" + section_html + "</section>\n "
                html_output += page_html
            else:
                raise Exception("no content found")
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
    except Exception as error: 
        print(error)
    
    # page = diagram = 1 section 
    # every contents must be wrapped within 1 section 
    # for image: 
    # Demo flow: images showed on Click following fragment order  
    # everything's belong to class 'fragment', must specify data-fragment-index
    # example fragment tag: 
    # <p class="fragment" data-fragment-index="3">Appears last</p>
    # <p class="fragment" data-fragment-index="1">Appears first</p>
    # <p class="fragment" data-fragment-index="2">Appears second</p>
    # without prior indexing: use array order 

def processImg(element, index=0): 
    output = ''
    url = element['url']
    styleStr = ''
    styles = []
    size =  tuple(element["size"].split(" "))
    w, h = size[0], size[1]

    if ("style" in element.keys()):
        for styleType, content in element['style'].items():
            match styleType:
                case "position":
                    x, y = content.split(" ")[0], content.split(" ")[1]
                    styles.append(f"position: absolute; left: {x}px; top: {y}px")
                case default:
                    continue
    if (len(styles) > 0) : 
         styleStr = (" ").join(styles)
    output = f"<img class='fragment' data-fragment-index={index}" 
    output += f" src =\"{url}\" width={w} height={h}"
    output+= "\n style=\"" +styleStr + "\"> \n" 
    print(output)
    return output

def processText(element, index=0): 
    output_text = ''
    return f"\t<p class='fragment' data-fragment-index={index}>{element['content']}</p> \n"

def main():
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    with open(input_file_path, 'r') as file:
        data = json.load(file)
    html_out = json_to_html(data)    
    soup = BeautifulSoup(html_out, 'html.parser')
    html_out = soup.prettify()
    with open(output_file_path, 'w') as file:
        file.write(html_out)

if __name__ == "__main__":
    main()
