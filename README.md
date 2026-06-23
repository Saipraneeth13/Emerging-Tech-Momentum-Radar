# 🚀 Emerging Tech Momentum Radar

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Analysis](https://img.shields.io/badge/Data-Analysis-green.svg)](#)

A comprehensive data analysis project that tracks and evaluates the momentum of emerging technologies by correlating **Google Search Trends** with **GitHub Open-Source Activity**.

---

## 💼 Business Problem
In the rapidly evolving tech landscape, businesses and developers often struggle to distinguish between **short-lived hype** and **sustainable adoption**. Investing in the wrong technology stack can lead to technical debt, while missing a "Rising Star" can result in a competitive disadvantage.

## 🎯 Objectives
- **Quantify Momentum:** Develop a composite "Momentum Score" using search interest and developer engagement.
- **Identify Lifecycle Stages:** Cluster technologies into "Rising Stars", "Stable/Mature", and "Speculative/Hype".
- **Forecast Trends:** Predict search interest for the next quarter using time-series forecasting.
- **Actionable Insights:** Provide a visual dashboard for strategic decision-making in recruitment and product development.

---

## 📊 Key Insights & Visualizations

### 1. Technology Momentum Radar
This visualization maps search growth against the calculated momentum score. The size of each bubble represents GitHub stars, providing a multi-dimensional view of tech health.

![Momentum Radar](assets/images/Dashbord.jpeg)
*Figure 1: Interactive Dashboard showing the relationship between search growth, momentum, and developer adoption.*

> **Key Finding:** **Large Language Models (LLMs)** exhibit the highest momentum, characterized by both explosive search growth and massive GitHub engagement, firmly placing them in the "Rising Star" category.

### 2. Search Interest Over Time (5-Year Trend)
A historical view of how interest has shifted, highlighting the dramatic surge in specific technologies.

![Search Trends](assets/images/search_trends.png)
*Figure 2: 5-year historical search interest trends for analyzed technologies.*

---

## 🛠️ Tools & Technologies
- **Data Collection:** `pytrends` (Google Trends API), `requests` (GitHub API).
- **Data Processing:** `Pandas`, `NumPy`.
- **Machine Learning:** `Scikit-learn` (K-Means Clustering), `Statsmodels` (Exponential Smoothing).
- **Visualization:** `Plotly`, `Dash`, `Matplotlib`, `Seaborn`.

---

## ⚙️ Workflow
1. **Data Acquisition:** Scraped 5 years of Google Trends data and current GitHub repository metrics.
2. **Feature Engineering:** Calculated YoY growth rates and normalized metrics for cross-comparison.
3. **Momentum Scoring:** Applied a weighted formula:
   - 40% Search Growth
   - 30% GitHub Stars
   - 20% StackOverflow Questions
   - 10% GitHub Forks
4. **Clustering:** Used K-Means to categorize technologies based on their adoption profile.
5. **Dashboarding:** Built a responsive Dash application for real-time exploration.

---

## 📈 Results & Recommendations
- **Rising Stars (High Priority):** LLMs and WebAssembly. Recommended for immediate R&D investment.
- **Speculative/Hype (Monitor):** Rust Programming. High developer interest but search growth is stabilizing; monitor for broader enterprise adoption.
- **Stable/Mature (Maintain):** Edge Computing. Consistent performance with predictable growth.

---

## 📂 Project Structure
```text
├── assets/
│   └── images/             # Visualizations used in README
├── data/
│   ├── raw/                # Original CSV files
│   └── processed/          # Cleaned and engineered datasets
├── src/                    # Refactored Python scripts
│   ├── data_processor.py   # Cleaning & Feature Engineering
│   └── analysis_engine.py  # ML & Forecasting logic
├── reports/
│   └── figures/            # Interactive HTML exports
├── app.py                  # Dash Web Application
└── requirements.txt        # Project dependencies
```
