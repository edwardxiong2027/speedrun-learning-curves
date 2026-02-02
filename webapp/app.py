#!/usr/bin/env python3
"""
Speedrun Learning Curve Visualization Web App
Author: Edward Xiong
Diamond Bar High School, 11th Grade
JEI Research Project: The Mathematics of Speedrunning

Interactive web visualization of speedrun world record progressions
and mathematical learning curve analysis.
"""

from flask import Flask, render_template, jsonify, request
import json
import os
import numpy as np
from datetime import datetime

app = Flask(__name__)

# Load data
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
ANALYSIS_DIR = os.path.join(os.path.dirname(__file__), '..', 'analysis')


def load_data():
    """Load speedrun data and analysis results."""
    speedrun_data = []
    analysis_results = []

    speedrun_path = os.path.join(DATA_DIR, 'speedrun_data.json')
    if os.path.exists(speedrun_path):
        with open(speedrun_path) as f:
            speedrun_data = json.load(f)

    analysis_path = os.path.join(ANALYSIS_DIR, 'analysis_results.json')
    if os.path.exists(analysis_path):
        with open(analysis_path) as f:
            analysis_results = json.load(f)

    return speedrun_data, analysis_results


@app.route('/')
def index():
    """Main page with interactive visualizations."""
    return render_template('index.html')


@app.route('/api/games')
def get_games():
    """Get list of games with data."""
    speedrun_data, _ = load_data()
    games = []

    for game in speedrun_data:
        categories = []
        for cat in game.get('categories', []):
            if len(cat.get('wr_progression', [])) >= 5:
                categories.append({
                    'name': cat['name'],
                    'n_records': len(cat['wr_progression']),
                    'total_runs': cat.get('total_runs', 0)
                })

        if categories:
            games.append({
                'name': game['name'],
                'id': game['id'],
                'categories': categories
            })

    return jsonify(games)


@app.route('/api/progression/<game_name>/<category_name>')
def get_progression(game_name, category_name):
    """Get world record progression for a specific game/category."""
    speedrun_data, analysis_results = load_data()

    # Find game and category
    progression = None
    analysis = None

    for game in speedrun_data:
        if game['name'] == game_name:
            for cat in game.get('categories', []):
                if cat['name'] == category_name:
                    progression = cat.get('wr_progression', [])
                    break

    for result in analysis_results:
        if result['game'] == game_name and result['category'] == category_name:
            analysis = result
            break

    if not progression:
        return jsonify({'error': 'Data not found'}), 404

    return jsonify({
        'game': game_name,
        'category': category_name,
        'progression': progression,
        'analysis': analysis
    })


@app.route('/api/summary')
def get_summary():
    """Get summary statistics for the research."""
    _, analysis_results = load_data()

    if not analysis_results:
        return jsonify({'error': 'No analysis results available'}), 404

    # Calculate summary stats
    good_fits = [r for r in analysis_results if r.get('best_r_squared', 0) > 0.7]

    model_counts = {}
    for r in good_fits:
        model = r.get('best_model', 'unknown')
        model_counts[model] = model_counts.get(model, 0) + 1

    avg_r2 = np.mean([r['best_r_squared'] for r in good_fits]) if good_fits else 0
    avg_improvement = np.mean([r['improvement_percent'] for r in good_fits]) if good_fits else 0

    return jsonify({
        'total_categories': len(analysis_results),
        'good_fits': len(good_fits),
        'model_distribution': model_counts,
        'avg_r_squared': avg_r2,
        'avg_improvement': avg_improvement,
        'results': analysis_results
    })


# HTML Template
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Mathematics of Speedrunning</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #eee;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            text-align: center;
            padding: 40px 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            margin-bottom: 30px;
        }

        h1 {
            font-size: 2.5rem;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #aaa;
            font-size: 1.1rem;
        }

        .author {
            margin-top: 15px;
            color: #888;
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: rgba(255,255,255,0.08);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .card h2 {
            color: #00d4ff;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }

        select {
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            border: none;
            background: rgba(255,255,255,0.1);
            color: #fff;
            font-size: 1rem;
            margin-bottom: 15px;
            cursor: pointer;
        }

        select option {
            background: #1a1a2e;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }

        .stat-box {
            background: rgba(0,212,255,0.1);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }

        .stat-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #00d4ff;
        }

        .stat-label {
            color: #888;
            font-size: 0.9rem;
            margin-top: 5px;
        }

        .chart-container {
            height: 500px;
        }

        .full-width {
            grid-column: 1 / -1;
        }

        .model-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9rem;
            margin: 3px;
        }

        .model-exponential { background: #e74c3c; }
        .model-power_law { background: #3498db; }
        .model-logarithmic { background: #2ecc71; }
        .model-hyperbolic { background: #9b59b6; }
        .model-wright { background: #f39c12; }

        .methodology {
            margin-top: 30px;
        }

        .methodology p {
            line-height: 1.8;
            color: #ccc;
            margin-bottom: 15px;
        }

        .formula {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
            overflow-x: auto;
        }

        footer {
            text-align: center;
            padding: 30px;
            color: #666;
            margin-top: 30px;
        }

        @media (max-width: 900px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>The Mathematics of Speedrunning</h1>
            <p class="subtitle">Analyzing Human Learning Curves and Optimization in Video Game Speed Completion</p>
            <p class="author">Edward Xiong | Diamond Bar High School | JEI Research Project</p>
        </header>

        <div class="grid">
            <div class="card">
                <h2>Select Game</h2>
                <select id="gameSelect" onchange="loadCategories()">
                    <option value="">Loading games...</option>
                </select>

                <h2>Select Category</h2>
                <select id="categorySelect" onchange="loadProgression()">
                    <option value="">Select a game first</option>
                </select>

                <div id="analysisStats" class="stats-grid" style="margin-top: 20px;">
                    <!-- Populated dynamically -->
                </div>
            </div>

            <div class="card">
                <h2>World Record Progression</h2>
                <div id="progressionChart" class="chart-container"></div>
            </div>
        </div>

        <div class="grid">
            <div class="card full-width">
                <h2>Model Comparison Across All Games</h2>
                <div id="modelChart" class="chart-container"></div>
            </div>
        </div>

        <div class="card methodology">
            <h2>Research Methodology</h2>
            <p>
                This research analyzes world record progressions from speedrun.com, fitting multiple
                mathematical learning curve models to understand the dynamics of human optimization
                in video game completion.
            </p>

            <p><strong>Mathematical Models Tested:</strong></p>

            <div class="formula">
                <strong>Exponential Decay:</strong> T(t) = a × e<sup>-bt</sup> + c<br><br>
                <strong>Power Law:</strong> T(t) = a × (t+1)<sup>-b</sup> + c<br><br>
                <strong>Wright's Learning Curve:</strong> T<sub>n</sub> = T<sub>1</sub> × n<sup>b</sup><br><br>
                <strong>Logarithmic:</strong> T(t) = a / (1 + b × ln(t+1)) + c<br><br>
                <strong>Hyperbolic:</strong> T(t) = a / (1 + bt) + c
            </div>

            <p>
                Where T is completion time, t is days since first record, n is record number,
                and a, b, c are fitted parameters. The asymptotic parameter c represents the
                theoretical limit of human performance for each game.
            </p>
        </div>

        <footer>
            <p>Data sourced from speedrun.com API | Analysis powered by Python + SciPy</p>
            <p>&copy; 2026 Edward Xiong | Diamond Bar High School</p>
        </footer>
    </div>

    <script>
        let gamesData = [];
        let summaryData = null;

        async function init() {
            // Load games
            const gamesResponse = await fetch('/api/games');
            gamesData = await gamesResponse.json();

            const gameSelect = document.getElementById('gameSelect');
            gameSelect.innerHTML = '<option value="">Select a game...</option>';

            gamesData.forEach(game => {
                const option = document.createElement('option');
                option.value = game.name;
                option.textContent = game.name;
                gameSelect.appendChild(option);
            });

            // Load summary for model chart
            const summaryResponse = await fetch('/api/summary');
            summaryData = await summaryResponse.json();
            drawModelChart();
        }

        function loadCategories() {
            const gameSelect = document.getElementById('gameSelect');
            const categorySelect = document.getElementById('categorySelect');
            const gameName = gameSelect.value;

            const game = gamesData.find(g => g.name === gameName);
            categorySelect.innerHTML = '<option value="">Select a category...</option>';

            if (game) {
                game.categories.forEach(cat => {
                    const option = document.createElement('option');
                    option.value = cat.name;
                    option.textContent = `${cat.name} (${cat.n_records} records)`;
                    categorySelect.appendChild(option);
                });
            }
        }

        async function loadProgression() {
            const gameName = document.getElementById('gameSelect').value;
            const categoryName = document.getElementById('categorySelect').value;

            if (!gameName || !categoryName) return;

            const response = await fetch(`/api/progression/${encodeURIComponent(gameName)}/${encodeURIComponent(categoryName)}`);
            const data = await response.json();

            if (data.error) {
                console.error(data.error);
                return;
            }

            drawProgressionChart(data);
            updateStats(data.analysis);
        }

        function drawProgressionChart(data) {
            const progression = data.progression;
            const analysis = data.analysis;

            const dates = progression.map(r => r.date);
            const times = progression.map(r => r.time_seconds);

            const traces = [{
                x: dates,
                y: times,
                mode: 'markers+lines',
                name: 'World Records',
                marker: { size: 12, color: '#e74c3c' },
                line: { dash: 'dot', color: '#e74c3c' }
            }];

            // Add fitted curve if analysis exists
            if (analysis && analysis.best_model) {
                const firstDate = new Date(dates[0]);
                const lastDate = new Date(dates[dates.length - 1]);
                const extendedDays = (lastDate - firstDate) / (1000 * 60 * 60 * 24) * 1.3;

                // Generate points for smooth curve
                const fittedDates = [];
                const fittedTimes = [];

                for (let d = 0; d <= extendedDays; d += extendedDays/100) {
                    const date = new Date(firstDate.getTime() + d * 24 * 60 * 60 * 1000);
                    fittedDates.push(date.toISOString().split('T')[0]);

                    // Calculate fitted value based on model
                    const params = analysis.models[analysis.best_model].params;
                    let fittedTime;

                    switch(analysis.best_model) {
                        case 'exponential':
                            fittedTime = params[0] * Math.exp(-params[1] * d) + params[2];
                            break;
                        case 'power_law':
                            fittedTime = params[0] * Math.pow(d + 1, -params[1]) + params[2];
                            break;
                        case 'logarithmic':
                            fittedTime = params[0] / (1 + params[1] * Math.log(d + 1)) + params[2];
                            break;
                        case 'hyperbolic':
                            fittedTime = params[0] / (1 + params[1] * d) + params[2];
                            break;
                        default:
                            fittedTime = times[0];
                    }
                    fittedTimes.push(fittedTime);
                }

                traces.push({
                    x: fittedDates,
                    y: fittedTimes,
                    mode: 'lines',
                    name: `${analysis.best_model.replace('_', ' ')} fit (R²=${analysis.best_r_squared.toFixed(3)})`,
                    line: { width: 3, color: '#3498db' }
                });

                // Add asymptote
                if (['exponential', 'power_law', 'hyperbolic'].includes(analysis.best_model)) {
                    const asymptote = analysis.models[analysis.best_model].params[2];
                    traces.push({
                        x: [dates[0], fittedDates[fittedDates.length - 1]],
                        y: [asymptote, asymptote],
                        mode: 'lines',
                        name: `Theoretical limit: ${asymptote.toFixed(2)}s`,
                        line: { dash: 'dash', width: 2, color: '#2ecc71' }
                    });
                }
            }

            const layout = {
                title: `${data.game} - ${data.category}`,
                xaxis: { title: 'Date', color: '#888' },
                yaxis: { title: 'Time (seconds)', color: '#888' },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0.2)',
                font: { color: '#eee' },
                legend: { x: 1, y: 1, xanchor: 'right' },
                margin: { t: 50, r: 50, b: 50, l: 60 }
            };

            Plotly.newPlot('progressionChart', traces, layout, { responsive: true });
        }

        function updateStats(analysis) {
            const container = document.getElementById('analysisStats');

            if (!analysis) {
                container.innerHTML = '<p>No analysis available</p>';
                return;
            }

            container.innerHTML = `
                <div class="stat-box">
                    <div class="stat-value">${analysis.n_records}</div>
                    <div class="stat-label">World Records</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">${analysis.improvement_percent.toFixed(1)}%</div>
                    <div class="stat-label">Total Improvement</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">${analysis.best_r_squared?.toFixed(3) || 'N/A'}</div>
                    <div class="stat-label">R² (Best Fit)</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">${analysis.best_model?.replace('_', ' ') || 'N/A'}</div>
                    <div class="stat-label">Best Model</div>
                </div>
            `;
        }

        function drawModelChart() {
            if (!summaryData || !summaryData.results) return;

            // Aggregate R² values by model
            const modelR2 = {};
            summaryData.results.forEach(result => {
                if (result.models) {
                    Object.entries(result.models).forEach(([model, data]) => {
                        if (!modelR2[model]) modelR2[model] = [];
                        modelR2[model].push(data.r_squared);
                    });
                }
            });

            const models = Object.keys(modelR2);
            const avgR2 = models.map(m => {
                const values = modelR2[m];
                return values.reduce((a, b) => a + b, 0) / values.length;
            });
            const stdR2 = models.map(m => {
                const values = modelR2[m];
                const avg = values.reduce((a, b) => a + b, 0) / values.length;
                const variance = values.reduce((sum, val) => sum + Math.pow(val - avg, 2), 0) / values.length;
                return Math.sqrt(variance);
            });

            const colors = {
                'exponential': '#e74c3c',
                'power_law': '#3498db',
                'logarithmic': '#2ecc71',
                'hyperbolic': '#9b59b6',
                'wright': '#f39c12'
            };

            const trace = {
                x: models.map(m => m.replace('_', ' ')),
                y: avgR2,
                error_y: { type: 'data', array: stdR2, visible: true },
                type: 'bar',
                marker: { color: models.map(m => colors[m] || '#888') }
            };

            const layout = {
                title: 'Average R² by Mathematical Model',
                xaxis: { title: 'Model', color: '#888' },
                yaxis: { title: 'Average R²', range: [0, 1], color: '#888' },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0.2)',
                font: { color: '#eee' },
                margin: { t: 50, r: 50, b: 80, l: 60 },
                shapes: [{
                    type: 'line',
                    x0: -0.5, x1: models.length - 0.5,
                    y0: 0.9, y1: 0.9,
                    line: { color: '#2ecc71', dash: 'dash', width: 2 }
                }]
            };

            Plotly.newPlot('modelChart', [trace], layout, { responsive: true });
        }

        // Initialize on load
        init();
    </script>
</body>
</html>
'''

# Create templates directory and save HTML
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
os.makedirs(TEMPLATE_DIR, exist_ok=True)

with open(os.path.join(TEMPLATE_DIR, 'index.html'), 'w') as f:
    f.write(INDEX_HTML)


if __name__ == '__main__':
    print("="*60)
    print("SPEEDRUN LEARNING CURVE VISUALIZATION")
    print("="*60)
    print("\nStarting web server...")
    print("Open http://localhost:5000 in your browser")
    print("\nPress Ctrl+C to stop the server")

    app.run(debug=True, port=5000)
