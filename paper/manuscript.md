# The Mathematics of Speedrunning: Analyzing Human Learning Curves and Optimization Limits in Video Game Speed Completion

**Edward Xiong**
Diamond Bar High School, Diamond Bar, CA

---

## SUMMARY

Video game speedrunning—the practice of completing games as quickly as possible—represents a unique domain for studying human learning and optimization. This study analyzes world record progression data from speedrun.com to determine which mathematical learning curve models best describe the dynamics of human performance improvement over time. We collected world record histories from 15 popular speedrunning games and fitted five mathematical models: exponential decay, power law, logarithmic, hyperbolic, and Wright's learning curve. Our analysis of [N] category progressions reveals that the [MODEL] model provides the best fit (average R² = [VALUE]), suggesting that speedrun optimization follows predictable mathematical patterns. We also calculate theoretical performance limits (asymptotic values) for each game, finding that current world records are approximately [X]% of the way to the predicted human performance ceiling. These findings contribute to our understanding of skill acquisition, human optimization behavior, and the mathematical properties of collective learning in competitive communities.

---

## INTRODUCTION

### Background

Speedrunning has emerged as a significant phenomenon in gaming culture, with speedrun.com hosting over 20 million recorded runs across thousands of games. Unlike traditional competitive gaming, speedrunning represents a form of distributed optimization where a global community collaboratively discovers and refines strategies to minimize completion time.

From a mathematical perspective, the progression of world records over time presents an opportunity to study human learning curves at a population level. Learning curve theory, first formalized by Wright in 1936, describes how performance improves with practice and experience. Wright's original observation—that labor costs decrease as a power function of cumulative production—has been applied across manufacturing, psychology, and cognitive science.

### Research Gap

While previous academic work has examined the computational complexity of speedrunning (determining whether optimal routes are computationally tractable), no studies have empirically analyzed the mathematical patterns in actual human speedrun performance. Existing research by Bosboom et al. (2015), Lafond (2018), and others focuses on tool-assisted speedruns (TAS) and theoretical optimal play, rather than human performance dynamics.

### Research Questions

This study addresses three primary questions:

1. Which mathematical learning curve model best describes world record progression in speedrunning?
2. Can we calculate theoretical performance limits (asymptotic times) for different games?
3. What factors influence the rate of optimization and the fit of different mathematical models?

### Hypothesis

We hypothesize that speedrun world record progressions follow mathematical decay patterns similar to classical learning curves, with the power law model providing the best fit based on its prevalence in skill acquisition literature.

---

## RESULTS

### Data Collection

We collected world record progression data from speedrun.com's public API for 15 games selected for their active speedrunning communities and sufficient historical data. The dataset includes:

- **Games analyzed**: [LIST]
- **Total categories**: [N]
- **Total world records tracked**: [N]
- **Date range**: [RANGE]

### Model Fitting Results

We fitted five mathematical models to each world record progression:

| Model | Equation | Average R² | Best Fit Count |
|-------|----------|------------|----------------|
| Exponential Decay | T(t) = ae^(-bt) + c | [VALUE] | [N] |
| Power Law | T(t) = a(t+1)^(-b) + c | [VALUE] | [N] |
| Logarithmic | T(t) = a/(1 + b·ln(t+1)) + c | [VALUE] | [N] |
| Hyperbolic | T(t) = a/(1 + bt) + c | [VALUE] | [N] |
| Wright's Curve | T_n = T_1 · n^b | [VALUE] | [N] |

**Figure 1**: Comparison of average R² values across mathematical models.

### Best-Fit Model Analysis

The [MODEL] model emerged as the best-fit model for [X]% of analyzed categories, with an average R² of [VALUE]. This suggests that speedrun optimization [INTERPRETATION].

**Figure 2**: Example world record progression with fitted curve for [GAME - CATEGORY].

### Theoretical Performance Limits

For models with asymptotic parameters (exponential, power law, hyperbolic), we calculated the theoretical performance limit (parameter c). This represents the predicted minimum time achievable through human optimization.

| Game | Category | Current WR | Theoretical Limit | % to Limit |
|------|----------|------------|-------------------|------------|
| [DATA ROWS] | | | | |

On average, current world records have achieved [X]% of the predicted improvement from first record to theoretical limit.

### Rate of Optimization

We analyzed factors correlating with optimization rate:

- **Community size**: Categories with more total runs showed [faster/slower] optimization
- **Game age**: Older games showed [PATTERN]
- **Game complexity**: [FINDING]

---

## DISCUSSION

### Interpretation of Results

The finding that [MODEL] provides the best fit for speedrun progressions has several implications:

1. **Collective learning dynamics**: Unlike individual learning curves, speedrunning represents distributed optimization where many individuals contribute discoveries. The [MODEL] pattern suggests [INTERPRETATION].

2. **Theoretical limits**: The asymptotic values represent an empirically-derived estimate of human performance ceilings. These are distinct from TAS times, which represent theoretical computational optima.

3. **Predictive capability**: The fitted models allow prediction of future world records with quantifiable uncertainty.

### Comparison to Classical Learning Curves

Wright's original learning curve (T_n = T_1 · n^b) showed [COMPARATIVE FINDING]. This [supports/contradicts] the application of manufacturing learning theory to competitive gaming.

### Limitations

Several limitations should be noted:

1. **Selection bias**: Only verified runs are included; improvements by non-recording players are unobserved
2. **Category variation**: Different speedrun categories within games have different characteristics
3. **External factors**: Game patches, new glitch discoveries, and community size changes affect progressions
4. **Model assumptions**: All tested models assume monotonic improvement, which may not hold during major strategy shifts

### Future Directions

Future research could:
- Analyze individual player improvement trajectories
- Incorporate game patch data to study discontinuities
- Compare TAS theoretical limits to human asymptotes
- Study the social dynamics of strategy diffusion

---

## MATERIALS AND METHODS

### Data Source

Data was collected from the speedrun.com public REST API (https://github.com/speedruncomorg/api). The API provides access to verified speedrun submissions including completion time, date, and category information.

### Game Selection

Games were selected based on:
1. Active speedrunning community (>1000 total verified runs)
2. Sufficient world record history (≥5 world record improvements)
3. Game availability on major platforms

### Data Processing

For each game category:
1. All verified runs were retrieved via API
2. Runs were sorted chronologically by completion date
3. World record progression was extracted (runs that set new fastest times)
4. Days since first record and record sequence number were calculated

### Mathematical Models

Five learning curve models were fitted using non-linear least squares regression (scipy.optimize.curve_fit):

**Exponential Decay**:
```
T(t) = a × exp(-b × t) + c
```
Where a is initial amplitude, b is decay rate, c is asymptotic limit.

**Power Law**:
```
T(t) = a × (t + 1)^(-b) + c
```
Where a is scale factor, b is power exponent, c is asymptotic limit.

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
Where n is record number and b is learning rate exponent.

### Model Evaluation

Models were evaluated using:
- **R² (coefficient of determination)**: Proportion of variance explained
- **RMSE (root mean square error)**: Average prediction error
- **AIC (Akaike Information Criterion)**: Model comparison accounting for complexity

### Statistical Analysis

All analysis was performed using Python 3.11 with NumPy, SciPy, and Pandas. Visualization used Matplotlib and Plotly. Code is available at [GitHub repository].

---

## ACKNOWLEDGMENTS

We thank the speedrun.com community for maintaining comprehensive records of speedrun data, and the speedrun.com team for providing public API access.

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
