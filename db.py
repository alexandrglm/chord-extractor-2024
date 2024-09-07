import json
import os

DB_FILE = "chords_db.json"

def generate_db_html():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            chords_db = json.load(f)
    else:
        chords_db = []

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Chords Database</title>
        <script src="./scripts/chart.js"></script>
        <script src="./scripts/jquery.min.js"></script>
        <script src="./scripts/jquery.dataTables.min.js"></script>
        <link rel="stylesheet" href="./scripts/jquery.dataTables.min.css">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { text-align: center; margin-bottom: 40px; }
            #buttons { text-align: center; margin-bottom: 20px; }
            button { padding: 10px 20px; margin: 5px; cursor: pointer; }
            canvas { display: block; margin: 20px auto; }
            table { width: 100%; margin-top: 20px; border-collapse: collapse; }
            table, th, td { border: 1px solid #ddd; }
            th, td { padding: 8px; text-align: center; }
            th { background-color: #f4f4f4; cursor: pointer; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
    <h1>Chords Database</h1>
    <div id="buttons">
        <button onclick="showTable()">Show Table</button>
        <button onclick="showBarChart()">Bar Chart</button>
        <button onclick="showLineChart()">Line Chart</button>
        <button onclick="showPieChart()">Pie Chart</button>
    </div>
    <div id="table-container">
        <table id="chords-table">
            <thead>
                <tr>
                    <th>Artist</th>
                    <th>Title</th>
                    <th>Chord</th>
                    <th>Times Used</th>
                    <th>BPM</th>
                    <th>Keynote</th>
                </tr>
            </thead>
            <tbody>
    """

    for entry in chords_db:
        artist = entry.get("artist", "Unknown")
        title = entry.get("title", "Unknown")
        bpm = entry.get("bpm", "N/A")
        keynote = entry.get("keynote", "Unknown")
        for chord, count in entry.get("chords", {}).items():
            html_content += f"<tr><td>{artist}</td><td>{title}</td><td>{chord}</td><td>{count}</td><td>{bpm}</td><td>{keynote}</td></tr>"

    html_content += """
            </tbody>
        </table>
    </div>

    <canvas id="chart-canvas" width="400" height="200"></canvas>

    <script>
        var chart;

        function showTable() {
            document.getElementById("table-container").style.display = "block";
            document.getElementById("chart-canvas").style.display = "none";
        }

        function showBarChart() {
            document.getElementById("table-container").style.display = "none";
            document.getElementById("chart-canvas").style.display = "block";

            if (chart) {
                chart.destroy();
            }

            var ctx = document.getElementById("chart-canvas").getContext("2d");
            chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: [""" + ', '.join(f'"{entry["title"]}"' for entry in chords_db) + """],
                    datasets: [{
                        label: 'Times Used',
                        data: [""" + ', '.join(f'{sum(chord["chords"].values())}' for chord in chords_db) + """],
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        function showLineChart() {
            document.getElementById("table-container").style.display = "none";
            document.getElementById("chart-canvas").style.display = "block";

            if (chart) {
                chart.destroy();
            }

            var ctx = document.getElementById("chart-canvas").getContext("2d");
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [""" + ', '.join(f'"{entry["title"]}"' for entry in chords_db) + """],
                    datasets: [{
                        label: 'Times Used',
                        data: [""" + ', '.join(f'{sum(chord["chords"].values())}' for chord in chords_db) + """],
                        backgroundColor: 'rgba(75, 192, 192, 0.5)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        function showPieChart() {
            document.getElementById("table-container").style.display = "none";
            document.getElementById("chart-canvas").style.display = "block";

            if (chart) {
                chart.destroy();
            }

            var ctx = document.getElementById("chart-canvas").getContext("2d");
            chart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: [""" + ', '.join(f'"{entry["title"]}"' for entry in chords_db) + """],
                    datasets: [{
                        label: 'Times Used',
                        data: [""" + ', '.join(f'{sum(chord["chords"].values())}' for chord in chords_db) + """],
                        backgroundColor: ['rgba(255, 99, 132, 0.5)', 'rgba(54, 162, 235, 0.5)', 'rgba(75, 192, 192, 0.5)'],
                        borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(75, 192, 192, 1)'],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true
                }
            });
        }

        showTable();
    </script>
    </body>
    </html>
    """

    db_html_file = "chords_database.html"
    with open(db_html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\033[92m{db_html_file} has been generated\033[0m")
    return db_html_file
