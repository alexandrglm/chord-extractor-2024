import os

def generate_chord_list(diagram_path):
    chord_list = []

    for root, dirs, files in os.walk(diagram_path):
        for file in files:
            if file.endswith(".png"):
                chord_name = os.path.splitext(file)[0]
                chord_list.append(chord_name)

    return chord_list

def generate_html(chord_list, output_file):
    html_content = """<html>
<head>
    <title>Lista de Acordes</title>
</head>
<body>
    <h1>Lista de Acordes de Guitarra</h1>
    <ul>
"""

    for chord in chord_list:
        html_content += f"        <li>{chord}</li>\n"

    html_content += """    </ul>
</body>
</html>"""

    with open(output_file, 'w') as file:
        file.write(html_content)

def main():
    diagram_path = "./engine/diagrams/guitar/"
    output_file = "chord_list.html"

    chord_list = generate_chord_list(diagram_path)
    generate_html(chord_list, output_file)

    print(f"Archivo HTML generado: {output_file}")

if __name__ == "__main__":
    main()
