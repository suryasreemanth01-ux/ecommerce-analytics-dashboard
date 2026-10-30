# E-commerce Business Analytics Dashboard

An interactive, end-to-end analytics dashboard built with Python, Streamlit, SQLite, and Scikit-learn. This application allows users to explore synthetic e-commerce data, filter performance metrics, view interactive visualizations, run SQL analytics, and forecast future sales using Machine Learning.

## Features
- Interactive KPIs: Real-time calculation of Total Revenue, Profit, Orders, and Average Order Value.
- Dynamic Filtering: Filter data by Date Range, Category, and Region.
- Data Visualization: Interactive Plotly charts (Monthly Trends, Category Breakdown, Top Products).
- SQL Analytics: Direct integration with a SQLite database showing top-performing products via raw SQL queries.
- Machine Learning: Linear Regression-based 3-month sales forecasting.
- Data Export: Download the currently filtered dataset as a CSV file.

## Technology Stack
- Language: Python
- Web Framework: Streamlit
- Data Manipulation: Pandas, NumPy
- Database: SQLite (via sqlite3)
- Visualization: Plotly Express
- Machine Learning: Scikit-learn
- Version Control: Git

## Project Structure
ecommerce-analytics-dashboard/
  data/
    synthetic_ecommerce_data.csv  # Generated dataset
    ecommerce.db                  # SQLite database
  src/
    __init__.py
    data_generator.py             # Script to generate synthetic data
    db_setup.py                   # Script to create DB and run SQL
    app.py                        # Main Streamlit dashboard application
  .gitignore                      # Files to ignore in Git
  requirements.txt                # Python dependencies
  README.md                       # Project documentation

## How to Run This Project Locally

1. Clone the repository:
   git clone https://github.com/your-username/ecommerce-analytics-dashboard.git
   cd ecommerce-analytics-dashboard

2. Create and activate a virtual environment:
   python -m venv venv
   .\venv\Scripts\Activate.ps1

3. Install dependencies:
   pip install -r requirements.txt

4. Generate the data and database:
   python .\src\data_generator.py
   python .\src\db_setup.py

5. Run the dashboard:
   streamlit run .\src\app.py

## Note on Data
The dataset used in this project is synthetically generated for demonstration purposes. It does not represent real business data.
