#!/usr/bin/env python3
"""
Speedrun Learning Curve Analysis
Author: Edward Xiong
Diamond Bar High School, 11th Grade
JEI Research Project: The Mathematics of Speedrunning

This script analyzes world record progression data to fit mathematical
learning curve models and make predictions about future records.
"""

import json
import numpy as np
import pandas as pd
from scipy import optimize
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

# Set style for publication-quality figures
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16


# =============================================================================
# MATHEMATICAL MODELS FOR LEARNING CURVES
# =============================================================================

def exponential_decay(t, a, b, c):
    """
    Exponential decay model: y = a * exp(-b * t) + c
    - a: initial amplitude above asymptote
    - b: decay rate
    - c: asymptotic limit (theoretical best time)
    """
    return a * np.exp(-b * t) + c


def power_law(t, a, b, c):
    """
    Power law decay model: y = a * (t + 1)^(-b) + c
    - a: scaling factor
    - b: power exponent
    - c: asymptotic limit
    """
    return a * np.power(t + 1, -b) + c


def logarithmic_decay(t, a, b, c):
    """
    Logarithmic decay model: y = a / (1 + b * log(t + 1)) + c
    - a: initial value factor
    - b: logarithmic decay rate
    - c: baseline offset
    """
    return a / (1 + b * np.log(t + 1)) + c


def wright_learning_curve(n, T1, b):
    """
    Wright's Learning Curve (1936): T_n = T_1 * n^b
    - T1: time for first unit
    - b: learning rate exponent (typically negative)

    Learning rate = 2^b (e.g., b=-0.322 gives 80% learning curve)
    """
    return T1 * np.power(n, b)


def hyperbolic_model(t, a, b, c):
    """
    Hyperbolic decay model: y = a / (1 + b * t) + c
    Common in skill acquisition research.
    """
    return a / (1 + b * t) + c


# =============================================================================
# MODEL FITTING AND EVALUATION
# =============================================================================

def fit_model(model_func, x_data, y_data, p0=None, bounds=(-np.inf, np.inf)):
    """Fit a model to data and return parameters and goodness of fit."""
    try:
        popt, pcov = optimize.curve_fit(
            model_func, x_data, y_data,
            p0=p0, bounds=bounds, maxfev=10000
        )

        # Calculate predictions and R-squared
        y_pred = model_func(x_data, *popt)
        ss_res = np.sum((y_data - y_pred) ** 2)
        ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        # Calculate RMSE
        rmse = np.sqrt(np.mean((y_data - y_pred) ** 2))

        # Calculate AIC for model comparison
        n = len(y_data)
        k = len(popt)
        aic = n * np.log(ss_res / n) + 2 * k

        return {
            'params': popt,
            'covariance': pcov,
            'r_squared': r_squared,
            'rmse': rmse,
            'aic': aic,
            'success': True
        }
    except Exception as e:
        return {
            'params': None,
            'error': str(e),
            'success': False
        }


def analyze_category(progression_data, game_name, category_name):
    """Analyze world record progression for a single category."""
    if len(progression_data) < 5:
        return None

    # Prepare data
    dates = [datetime.strptime(r['date'], "%Y-%m-%d") for r in progression_data]
    times = np.array([r['time_seconds'] for r in progression_data])

    # Convert to days since first record
    first_date = dates[0]
    days = np.array([(d - first_date).days for d in dates])

    # Record number (for Wright's curve)
    record_num = np.arange(1, len(progression_data) + 1)

    # Normalize time (percent of first record)
    normalized_times = times / times[0] * 100

    results = {
        'game': game_name,
        'category': category_name,
        'n_records': len(progression_data),
        'first_time': times[0],
        'current_time': times[-1],
        'improvement_percent': (1 - times[-1] / times[0]) * 100,
        'days_span': days[-1],
        'models': {}
    }

    # Initial guesses for fitting
    initial_amplitude = times[0] - times[-1]
    asymptote_guess = times[-1] * 0.95

    # Fit each model
    models = {
        'exponential': {
            'func': exponential_decay,
            'p0': [initial_amplitude, 0.01, asymptote_guess],
            'bounds': ([0, 0, 0], [np.inf, 1, times[0]])
        },
        'power_law': {
            'func': power_law,
            'p0': [initial_amplitude, 0.5, asymptote_guess],
            'bounds': ([0, 0, 0], [np.inf, 5, times[0]])
        },
        'logarithmic': {
            'func': logarithmic_decay,
            'p0': [times[0], 0.1, 0],
            'bounds': ([0, 0, 0], [np.inf, 10, times[0]])
        },
        'hyperbolic': {
            'func': hyperbolic_model,
            'p0': [initial_amplitude, 0.01, asymptote_guess],
            'bounds': ([0, 0, 0], [np.inf, 1, times[0]])
        },
        'wright': {
            'func': wright_learning_curve,
            'p0': [times[0], -0.3],
            'bounds': ([0, -2], [np.inf, 0])
        }
    }

    for model_name, model_info in models.items():
        if model_name == 'wright':
            x_data = record_num
        else:
            x_data = days

        result = fit_model(
            model_info['func'],
            x_data,
            times,
            p0=model_info['p0'],
            bounds=model_info['bounds']
        )

        if result['success']:
            results['models'][model_name] = {
                'params': result['params'].tolist(),
                'r_squared': result['r_squared'],
                'rmse': result['rmse'],
                'aic': result['aic']
            }

    # Find best model (highest R²)
    if results['models']:
        best_model = max(results['models'].items(), key=lambda x: x[1]['r_squared'])
        results['best_model'] = best_model[0]
        results['best_r_squared'] = best_model[1]['r_squared']

    return results


def predict_future_records(results, days_ahead=365):
    """Predict future world records using the best-fit model."""
    if 'best_model' not in results:
        return None

    model_name = results['best_model']
    params = results['models'][model_name]['params']

    model_funcs = {
        'exponential': exponential_decay,
        'power_law': power_law,
        'logarithmic': logarithmic_decay,
        'hyperbolic': hyperbolic_model,
    }

    if model_name not in model_funcs:
        return None

    func = model_funcs[model_name]
    current_days = results['days_span']

    predictions = []
    for future_days in [30, 90, 180, 365, 730]:
        total_days = current_days + future_days
        predicted_time = func(total_days, *params)
        predictions.append({
            'days_from_now': future_days,
            'predicted_time': predicted_time,
            'improvement_from_current': results['current_time'] - predicted_time
        })

    # Calculate asymptotic limit (theoretical best)
    if model_name in ['exponential', 'power_law', 'hyperbolic']:
        asymptote = params[-1]  # c parameter is the asymptote
        results['theoretical_limit'] = asymptote
        results['percent_to_limit'] = (results['current_time'] - asymptote) / (results['first_time'] - asymptote) * 100

    return predictions


def create_visualization(all_results, output_dir):
    """Create publication-quality visualizations."""
    os.makedirs(output_dir, exist_ok=True)

    # Filter results with good fits
    good_results = [r for r in all_results if r and r.get('best_r_squared', 0) > 0.7]

    if not good_results:
        print("No results with good model fits found.")
        return

    # 1. Model Comparison Bar Chart
    fig, ax = plt.subplots(figsize=(12, 6))
    model_r2 = {'exponential': [], 'power_law': [], 'logarithmic': [], 'hyperbolic': [], 'wright': []}

    for result in good_results:
        for model_name, model_data in result.get('models', {}).items():
            model_r2[model_name].append(model_data['r_squared'])

    model_names = list(model_r2.keys())
    avg_r2 = [np.mean(model_r2[m]) if model_r2[m] else 0 for m in model_names]
    std_r2 = [np.std(model_r2[m]) if model_r2[m] else 0 for m in model_names]

    bars = ax.bar(model_names, avg_r2, yerr=std_r2, capsize=5, color='steelblue', edgecolor='black')
    ax.set_ylabel('Average R² Value')
    ax.set_xlabel('Mathematical Model')
    ax.set_title('Comparison of Learning Curve Models for Speedrun Progression')
    ax.set_ylim(0, 1)
    ax.axhline(y=0.9, color='green', linestyle='--', alpha=0.7, label='R² = 0.9 threshold')
    ax.legend()

    for bar, val in zip(bars, avg_r2):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{val:.3f}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'model_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Example Progression with Fit
    best_result = max(good_results, key=lambda x: x.get('best_r_squared', 0))

    # Load original data to plot
    data_file = os.path.join(os.path.dirname(output_dir), 'data', 'speedrun_data.json')
    if os.path.exists(data_file):
        with open(data_file) as f:
            raw_data = json.load(f)

        # Find matching game/category
        for game_data in raw_data:
            if game_data['name'] == best_result['game']:
                for cat_data in game_data['categories']:
                    if cat_data['name'] == best_result['category']:
                        progression = cat_data['wr_progression']

                        # Create plot
                        fig, ax = plt.subplots(figsize=(12, 7))

                        dates = [datetime.strptime(r['date'], "%Y-%m-%d") for r in progression]
                        times = [r['time_seconds'] for r in progression]

                        # Plot actual data
                        ax.scatter(dates, times, s=100, c='red', zorder=5, label='World Records', edgecolors='black')
                        ax.plot(dates, times, 'r--', alpha=0.5)

                        # Plot best fit
                        days = np.array([(d - dates[0]).days for d in dates])
                        params = best_result['models'][best_result['best_model']]['params']

                        model_funcs = {
                            'exponential': exponential_decay,
                            'power_law': power_law,
                            'logarithmic': logarithmic_decay,
                            'hyperbolic': hyperbolic_model,
                        }

                        if best_result['best_model'] in model_funcs:
                            # Create smooth curve
                            days_smooth = np.linspace(0, days[-1] * 1.2, 200)
                            dates_smooth = [dates[0] + timedelta(days=int(d)) for d in days_smooth]
                            times_pred = model_funcs[best_result['best_model']](days_smooth, *params)

                            ax.plot(dates_smooth, times_pred, 'b-', linewidth=2,
                                   label=f'{best_result["best_model"].replace("_", " ").title()} Fit (R²={best_result["best_r_squared"]:.3f})')

                            # Show asymptote if available
                            if best_result['best_model'] in ['exponential', 'power_law', 'hyperbolic']:
                                asymptote = params[-1]
                                ax.axhline(y=asymptote, color='green', linestyle=':', linewidth=2,
                                          label=f'Theoretical Limit: {asymptote:.2f}s')

                        ax.set_xlabel('Date')
                        ax.set_ylabel('Time (seconds)')
                        ax.set_title(f'World Record Progression: {best_result["game"]} - {best_result["category"]}')
                        ax.legend(loc='upper right')

                        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
                        ax.xaxis.set_major_locator(mdates.YearLocator())
                        plt.xticks(rotation=45)

                        plt.tight_layout()
                        plt.savefig(os.path.join(output_dir, 'example_progression.png'), dpi=300, bbox_inches='tight')
                        plt.close()
                        break

    # 3. Improvement Rate Analysis
    fig, ax = plt.subplots(figsize=(10, 6))

    improvements = [(r['game'], r['improvement_percent']) for r in good_results]
    improvements.sort(key=lambda x: x[1], reverse=True)

    games = [imp[0][:20] + '...' if len(imp[0]) > 20 else imp[0] for imp in improvements[:15]]
    percents = [imp[1] for imp in improvements[:15]]

    bars = ax.barh(games, percents, color='coral', edgecolor='black')
    ax.set_xlabel('Total Improvement (%)')
    ax.set_title('World Record Improvement by Game')
    ax.invert_yaxis()

    for bar, val in zip(bars, percents):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}%', va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'improvement_rates.png'), dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Visualizations saved to: {output_dir}")


def main():
    """Main analysis function."""
    print("="*60)
    print("SPEEDRUN LEARNING CURVE ANALYSIS")
    print("JEI Research Project - Edward Xiong")
    print("="*60)

    # Load collected data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'speedrun_data.json')

    if not os.path.exists(data_path):
        print(f"Data file not found: {data_path}")
        print("Please run collect_speedrun_data.py first.")
        return

    with open(data_path) as f:
        data = json.load(f)

    print(f"Loaded data for {len(data)} games")

    # Analyze each game/category
    all_results = []

    for game in data:
        game_name = game['name']
        print(f"\nAnalyzing: {game_name}")

        for category in game.get('categories', []):
            cat_name = category['name']
            progression = category.get('wr_progression', [])

            if len(progression) >= 5:
                print(f"  Category: {cat_name} ({len(progression)} records)")
                result = analyze_category(progression, game_name, cat_name)

                if result:
                    predictions = predict_future_records(result)
                    if predictions:
                        result['predictions'] = predictions

                    all_results.append(result)

                    if 'best_model' in result:
                        print(f"    Best model: {result['best_model']} (R²={result['best_r_squared']:.3f})")
                        print(f"    Improvement: {result['improvement_percent']:.1f}%")

    # Save analysis results
    output_path = os.path.join(os.path.dirname(__file__), 'analysis_results.json')
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2, cls=NumpyEncoder)
    print(f"\nResults saved to: {output_path}")

    # Create visualizations
    viz_dir = os.path.join(os.path.dirname(__file__), 'figures')
    create_visualization(all_results, viz_dir)

    # Summary statistics
    print("\n" + "="*60)
    print("ANALYSIS SUMMARY")
    print("="*60)

    good_fits = [r for r in all_results if r.get('best_r_squared', 0) > 0.7]
    print(f"Categories analyzed: {len(all_results)}")
    print(f"Categories with good fits (R² > 0.7): {len(good_fits)}")

    if good_fits:
        # Best model distribution
        model_counts = {}
        for r in good_fits:
            model = r.get('best_model', 'unknown')
            model_counts[model] = model_counts.get(model, 0) + 1

        print("\nBest-fit model distribution:")
        for model, count in sorted(model_counts.items(), key=lambda x: -x[1]):
            print(f"  {model}: {count} ({count/len(good_fits)*100:.1f}%)")

        avg_r2 = np.mean([r['best_r_squared'] for r in good_fits])
        print(f"\nAverage R² for good fits: {avg_r2:.3f}")

        avg_improvement = np.mean([r['improvement_percent'] for r in good_fits])
        print(f"Average improvement: {avg_improvement:.1f}%")


if __name__ == "__main__":
    main()
