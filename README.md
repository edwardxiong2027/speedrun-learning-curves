# The Mathematics of Speedrunning

**JEI Research Project by Edward Xiong**
Diamond Bar High School, 11th Grade

## Abstract

This research project analyzes world record progressions in video game speedrunning to understand the mathematical patterns of human learning and optimization. Using data from speedrun.com's API, we fit multiple learning curve models (exponential, power law, logarithmic, hyperbolic, Wright's curve) to determine which best describes the dynamics of collective skill improvement.

## Repository Structure

```
JEI_Research_Project/
├── data/
│   ├── collect_speedrun_data.py    # Data collection script
│   ├── speedrun_data.json          # Raw collected data
│   └── wr_progression.csv          # Processed progression data
├── analysis/
│   ├── learning_curve_analysis.py  # Statistical analysis
│   ├── analysis_results.json       # Fitted model results
│   └── figures/                    # Generated visualizations
├── webapp/
│   └── app.py                      # Interactive Flask web app
├── paper/
│   └── manuscript.md               # Research paper draft
├── requirements.txt
└── README.md
```

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/speedrun-learning-curves.git
cd speedrun-learning-curves

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Collect Data

```bash
python data/collect_speedrun_data.py
```

This collects world record progression data from speedrun.com for 15 popular games.

### 2. Run Analysis

```bash
python analysis/learning_curve_analysis.py
```

This fits mathematical models and generates visualizations.

### 3. Launch Web App

```bash
python webapp/app.py
```

Open http://localhost:5000 to explore the interactive visualizations.

## Mathematical Models

| Model | Equation | Description |
|-------|----------|-------------|
| Exponential Decay | T(t) = ae^(-bt) + c | Rapid initial improvement, slowing over time |
| Power Law | T(t) = a(t+1)^(-b) + c | Classic learning curve pattern |
| Logarithmic | T(t) = a/(1 + b·ln(t+1)) + c | Slow, sustained improvement |
| Hyperbolic | T(t) = a/(1 + bt) + c | Skill acquisition model |
| Wright's Curve | T_n = T_1·n^b | Manufacturing learning curve |

## Key Findings

| Metric | Value |
|--------|-------|
| Games Analyzed | 5 |
| Categories | 15 |
| World Records | 429 |
| Average R² | **0.935** |
| Best Model | Wright's Learning Curve (46.7%) |
| Average Improvement | 49.8% |

### Model Distribution
- **Wright's Learning Curve**: 7 categories (46.7%)
- **Hyperbolic**: 4 categories (26.7%)
- **Exponential**: 3 categories (20.0%)
- **Power Law**: 1 category (6.7%)

### Key Insight
Wright's 1936 Learning Curve, originally developed for aircraft manufacturing, best describes how speedrunning world records improve over time - demonstrating that collective human optimization follows universal mathematical patterns.

## Web Application Preview

The interactive web application allows users to:
- Select any game and speedrun category
- Visualize world record progression over time
- See fitted mathematical models with R² values
- View predicted theoretical performance limits

## Data Source

All data is collected from [speedrun.com](https://speedrun.com) via their public API. Data is licensed under CC-BY-NC 4.0.

## Citation

If you use this work, please cite:

```
Xiong, E. (2026). The Mathematics of Speedrunning: Analyzing Human Learning
Curves and Optimization Limits in Video Game Speed Completion.
Journal of Emerging Investigators.
```

## License

This project is licensed under the MIT License.

## Contact

Edward Xiong
Diamond Bar High School
Diamond Bar, CA

---

*Prepared for submission to the Journal of Emerging Investigators*
