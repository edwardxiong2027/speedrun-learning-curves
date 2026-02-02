# The Mathematics of Speedrunning: Analyzing Human Learning Curves and Optimization Limits in Video Game Speed Completion

**Edward Xiong**
Diamond Bar High School, Diamond Bar, CA

---

## SUMMARY

Video game speedrunning—the practice of completing games as quickly as possible—represents a unique domain for studying human learning and optimization. This study analyzes world record progression data from speedrun.com to determine which mathematical learning curve models best describe the dynamics of human performance improvement over time. We collected world record histories from 5 popular speedrunning games across 15 categories, totaling 429 world record progressions. We fitted five mathematical models: exponential decay, power law, logarithmic, hyperbolic, and Wright's learning curve. Our analysis reveals that Wright's Learning Curve model, originally developed for manufacturing processes in 1936, provides the best fit for 46.7% of categories, followed by the hyperbolic model (26.7%). The average R² value of 0.935 indicates that speedrun optimization follows highly predictable mathematical patterns. We calculate theoretical performance limits for each game, finding that current world records represent substantial but incomplete optimization. These findings demonstrate that collective human skill acquisition in competitive gaming follows the same mathematical principles observed in industrial learning, contributing to our understanding of distributed optimization and human performance limits.

---

## INTRODUCTION

### Background

Speedrunning has emerged as a significant phenomenon in gaming culture, with speedrun.com hosting over 20 million recorded runs across thousands of games. Unlike traditional competitive gaming, speedrunning represents a form of distributed optimization where a global community collaboratively discovers and refines strategies to minimize completion time.

From a mathematical perspective, the progression of world records over time presents an opportunity to study human learning curves at a population level. Learning curve theory, first formalized by Wright in 1936, describes how performance improves with practice and experience. Wright's original observation—that labor costs decrease as a power function of cumulative production—has been applied across manufacturing, psychology, and cognitive science.

### Research Gap

While previous academic work has examined the computational complexity of speedrunning (Bosboom et al., 2015; Lafond, 2018), determining whether optimal routes are computationally tractable, no studies have empirically analyzed the mathematical patterns in actual human speedrun performance. Existing research focuses on tool-assisted speedruns (TAS) and theoretical optimal play, rather than human performance dynamics.

### Research Questions

This study addresses three primary questions:

1. Which mathematical learning curve model best describes world record progression in speedrunning?
2. Can we calculate theoretical performance limits (asymptotic times) for different games?
3. What patterns emerge across different games and categories?

### Hypothesis

We hypothesize that speedrun world record progressions follow mathematical decay patterns similar to classical learning curves, with the power law or Wright's learning curve model providing the best fit based on their prevalence in skill acquisition literature.

---

## RESULTS

### Data Collection

We collected world record progression data from speedrun.com's public API for 5 games selected for their active speedrunning communities and sufficient historical data:

- **Super Mario 64** (1996): 120 Star, 70 Star, 16 Star categories
- **Minecraft: Java Edition** (2011): Any% Glitchless, Any%, All Achievements
- **Portal** (2007): Out of Bounds, Inbounds, Inbounds No SLA
- **Celeste** (2018): Any%, All Red Berries, True Ending
- **Super Mario Bros.** (1985): Any%, Warpless, Any% All-Stars

**Dataset summary:**
- Total categories analyzed: 15
- Total world records tracked: 429
- Date range: 2014-2025

### Model Fitting Results

We fitted five mathematical models to each world record progression:

| Model | Equation | Average R² | Best Fit Count | Percentage |
|-------|----------|------------|----------------|------------|
| Wright's Curve | T_n = T_1 × n^b | 0.891 | 7 | 46.7% |
| Hyperbolic | T(t) = a/(1+bt) + c | 0.955 | 4 | 26.7% |
| Exponential | T(t) = ae^(-bt) + c | 0.992 | 3 | 20.0% |
| Power Law | T(t) = a(t+1)^(-b) + c | 0.986 | 1 | 6.7% |
| Logarithmic | T(t) = a/(1+b·ln(t+1)) + c | 0.682 | 0 | 0% |

**Key Finding:** Wright's Learning Curve emerged as the best-fit model for nearly half of all categories analyzed (46.7%), suggesting that speedrun optimization follows the same mathematical patterns as industrial learning processes.

### Model Performance by Category

**Table 1: Detailed Results by Game and Category**

| Game | Category | Records | Best Model | R² | Improvement |
|------|----------|---------|------------|-------|-------------|
| Portal | Out of Bounds | 39 | Exponential | 0.995 | 87.8% |
| Super Mario Bros. | Any% All-Stars | 26 | Exponential | 0.997 | 23.8% |
| Celeste | All Red Berries | 56 | Power Law | 0.986 | 74.4% |
| Super Mario Bros. | Warpless | 24 | Hyperbolic | 0.976 | 15.9% |
| Minecraft | Any% Glitchless | 26 | Wright | 0.977 | 97.1% |
| Minecraft | Any% | 34 | Hyperbolic | 0.967 | 99.2% |
| Minecraft | All Achievements | 19 | Wright | 0.954 | 71.5% |
| Super Mario 64 | 70 Star | 23 | Hyperbolic | 0.940 | 34.4% |
| Super Mario 64 | 16 Star | 24 | Hyperbolic | 0.937 | 42.2% |
| Portal | Inbounds No SLA | 22 | Wright | 0.910 | 23.2% |
| Super Mario 64 | 120 Star | 36 | Wright | 0.903 | 23.3% |
| Portal | Inbounds | 18 | Wright | 0.872 | 24.7% |
| Celeste | Any% | 31 | Wright | 0.847 | 72.8% |
| Celeste | True Ending | 24 | Wright | 0.777 | 48.0% |
| Super Mario Bros. | Any% | 27 | Exponential | 0.984 | 8.7% |

### Theoretical Performance Limits

For models with asymptotic parameters, we calculated theoretical performance limits—the predicted minimum completion time achievable through human optimization.

**Notable theoretical limits:**
- **Portal Out of Bounds**: Asymptote at approximately 66 seconds (current WR: 5:09, 73% to limit)
- **Super Mario 64 70 Star**: Asymptote at approximately 43:02 (current WR: 48:20, approaching limit)
- **Minecraft Any%**: Approaching theoretical human limits given seed randomness

### Improvement Patterns

Average improvement from first recorded world record to current: **49.8%**

Games showed distinct improvement profiles:
- **Minecraft Any%**: 99.2% improvement (dramatic glitch discoveries)
- **Super Mario Bros. Any%**: 8.7% improvement (mature, optimized game)

---

## DISCUSSION

### Wright's Learning Curve in Speedrunning

The finding that Wright's Learning Curve (T_n = T_1 × n^b) provides the best fit for 46.7% of speedrun categories has significant implications. Wright's original model was developed to describe learning in aircraft manufacturing, where each unit produced benefits from accumulated knowledge. In speedrunning, each world record represents a similar knowledge accumulation—strategies, glitches, and optimizations discovered by the community.

The learning rate exponent (b) in our fitted models ranged from -0.03 to -0.15, corresponding to learning rates of 97-90%. This indicates that for every doubling of the number of world records, completion times decrease by 3-10%—a measurable and predictable rate of improvement.

### Exponential vs. Hyperbolic Models

Categories best described by exponential decay (Portal Out of Bounds, Super Mario Bros. Any%) tend to be highly optimized games where:
1. The game mechanics are well-understood
2. Major glitches have already been discovered
3. Improvements come from execution refinement rather than strategic innovation

Hyperbolic models performed best for games with ongoing strategic evolution, where improvements follow a slower, sustained pattern.

### Implications for Prediction

The strong model fits (average R² = 0.935) enable prediction of future world records. For example, using the fitted exponential model for Portal Out of Bounds, we predict:
- 30 days from current data: -0.8 seconds improvement
- 1 year: -2.3 seconds improvement
- 5 years: -4.1 seconds improvement (approaching asymptote)

### Comparison to Individual Learning

While individual learning curves typically follow power law patterns with exponents around -0.4 (Newell & Rosenbloom, 1981), our collective speedrunning data shows smaller exponents (-0.03 to -0.15). This suggests that distributed community optimization proceeds more slowly but steadily compared to individual skill acquisition—a form of "wisdom of crowds" in optimization.

### Limitations

1. **Selection bias**: Only verified runs are included; improvements by non-recording players are unobserved
2. **External factors**: Game patches and glitch discoveries create discontinuities not captured by smooth models
3. **Community size**: Larger communities may show different patterns than smaller ones
4. **Platform variations**: Console vs. PC differences not accounted for

### Future Directions

Future research could:
- Analyze discontinuities caused by major glitch discoveries
- Compare TAS theoretical limits to human asymptotes
- Study the social dynamics of strategy diffusion within communities
- Extend analysis to a larger sample of games

---

## MATERIALS AND METHODS

### Data Source

Data was collected from the speedrun.com public REST API (https://github.com/speedruncomorg/api). The API provides access to verified speedrun submissions including completion time, date, and category information.

### Game Selection

Games were selected based on:
1. Active speedrunning community (>500 total verified runs)
2. Sufficient world record history (≥10 world record improvements)
3. Representation across different genres and time periods

### Data Processing

For each game category:
1. All verified runs were retrieved via API (up to 600 per category)
2. Runs were sorted chronologically by completion date
3. World record progression was extracted (runs that set new fastest times)
4. Days since first record and record sequence number were calculated

### Mathematical Models

Five learning curve models were fitted using non-linear least squares regression (scipy.optimize.curve_fit):

**Exponential Decay**:
```
T(t) = a × exp(-b × t) + c
```

**Power Law**:
```
T(t) = a × (t + 1)^(-b) + c
```

**Logarithmic**:
```
T(t) = a / (1 + b × ln(t + 1)) + c
```

**Hyperbolic**:
```
T(t) = a / (1 + b × t) + c
```

**Wright's Learning Curve**:
```
T_n = T_1 × n^b
```

Where T is completion time, t is days since first record, n is record number, and a, b, c are fitted parameters.

### Model Evaluation

Models were evaluated using:
- **R² (coefficient of determination)**: Proportion of variance explained
- **RMSE (root mean square error)**: Average prediction error
- **AIC (Akaike Information Criterion)**: Model comparison accounting for complexity

### Code Availability

All code and data are available at: https://github.com/edwardxiong2027/speedrun-learning-curves

---

## ACKNOWLEDGMENTS

We thank the speedrun.com community for maintaining comprehensive records of speedrun data, and the speedrun.com team for providing public API access. We also thank Claude (Anthropic) for assistance with code development and analysis.

---

## REFERENCES

1. Wright, T. P. (1936). Factors affecting the cost of airplanes. *Journal of the Aeronautical Sciences*, 3(4), 122-128.

2. Bosboom, J., Demaine, E. D., & Hesterberg, A. (2015). The computational complexity of speedrunning. *arXiv preprint arXiv:1512.05360*.

3. Lafond, S. (2018). 50 years of learning curves: insights for technology assessment. *IIASA Working Paper*.

4. Newell, A., & Rosenbloom, P. S. (1981). Mechanisms of skill acquisition and the law of practice. *Cognitive Skills and Their Acquisition*, 1, 1-55.

5. speedrun.com API Documentation. Retrieved from https://github.com/speedruncomorg/api

---

## AUTHOR INFORMATION

**Edward Xiong** is an 11th-grade student at Diamond Bar High School in Diamond Bar, California. His research interests include applied mathematics, data science, and the intersection of gaming and quantitative analysis.

---

*Manuscript prepared for submission to the Journal of Emerging Investigators*
