

***

# 🚀 Startup Funding Dashboard

An interactive, modern data dashboard built with **Streamlit, Pandas, NumPy, and Plotly** for data analysis of Indian startup funding. Instantly explore investments, top industries, investors, deal sizes, and city trends—no code required.

***

## ✨ Features

- **Automatic CSV Loading:** Reads your `startup_funding.csv` (handles absolute/relative path + encoding)
- **Smart Data Cleaning:** Handles messy, missing, or oddly-named columns seamlessly
- **Sidebar Filtering:** Interactive multi-select for year, industry, and city
- **Key Metrics:** Shows Total Funding, Startups, Deals, Avg Deal, Investors
- **Tabbed Visuals (No Trends Tab!):**
  - **Industries:** Top-funded sectors, deal breakdowns, round distribution, performance table
  - **Investors & Startups:** Most active investors, top funded startups, investment stage funnel, deal size breakdown
  - **Geography & Analysis:** Funding by city, city ecosystem bubble plot, heatmap (city vs industry), city leaderboard
- **Data Export:** Download your custom-filtered view as a CSV
- **Beautiful UI:** Custom CSS, professional chart colors, responsive layouts
- **Fail-safe Sample Data:** If no CSV found, instantly generates realistic demo data so you can always show your dashboard

***

## 📂 Folder Structure

```
your_project/
├── app.py                   # Main Streamlit app
├── data/
│   └── startup_funding.csv  # Data file (put here)
├── requirements.txt         # Libraries to install
```

***

## 🚦 Quick Start

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2. **Put your CSV:**  
   Place your actual funding data at `data/startup_funding.csv`.
3. **Run the dashboard:**
    ```bash
    streamlit run app.py
    ```
4. **Visit the App:**  
   Open the browser link (usually (http://localhost:8501)).

***

## 🖥️ Usage

- Use the left sidebar to filter by years, industries, and cities.
- Click the dashboard tabs to analyze by Industry, Investor/Startup, or Geography.
- Hover over charts for drilldown details.
- Download your filtered data with one click.

***

## 🧠 Concepts & Tech Used

- **Pandas DataFrame & GroupBy:** All stats, groupings, and aggregations use pandas best practices
- **NumPy:** Fast random/sample data generation, numerical operations
- **Plotly Express:** Modern interactive bar, pie, scatter, funnel, and heatmap charts
- **Defensive Programming:**  
  Data loads robustly from various formats, and the dashboard never crashes thanks to fallback sample data

***

## 🔑 Customization

- Add/replace any CSV columns, the code auto-recognizes standard names.
- To add new charts or KPIs, use pandas groupby/filter as patterns.
- For a time-based trends tab or other new sections, simply use new tabs via `st.tabs([...])`.

***

## ✍️ Author

Made by AADITYA JAISWAL
Inspired by the Indian startup ecosystem.

***

## 📜 License

MIT License (add actual license text if desired)

***



