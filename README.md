# Software Engineering for Data Scientists: Data Science Dashboard



## Project Overview

This project provides a dynamic dashboard application for visualizing and interacting with employee and team data. It is designed as the final project for the Software Engineering for Data Scientists course and includes:

- **Interactive dashboard:** View and filter data using visual components.

- **Data visualizations:** Displays line charts, bar charts, and tables to present employee performance and team statistics.

- **Automated Testing & CI/CD:** Integrated testing with pytest and continuous integration via GitHub Actions.

- **Code Quality Tools:** Uses Flake8 for linting and Black for code formatting.



## Features

- **Employee and Team Views:** Separate dashboards for individual employees and teams.

- **Dynamic Filtering:** Use radio buttons and dropdown menus to update data dynamically.

- **Visual Reports:** Interactive visualizations to track event counts and trends.

- **Robust Backend:** Implemented with a modular code structure for easy enhancements.

- **CI/CD Integration:** Automatically runs tests and linting on every commit using GitHub Actions.



## Repository Structure

```plaintext

+-- README.md

+-- assets

¦   +-- model.pkl

¦   +-- report.css

+-- env

+-- python-package

¦   +-- employee_events

¦       +-- __init__.py

¦       +-- employee.py

¦       +-- employee_events.db

¦       +-- query_base.py

¦       +-- sql_execution.py

¦       +-- team.py

¦   +-- requirements.txt

¦   +-- setup.py

+-- report

¦   +-- base_components

¦       +-- __init__.py

¦       +-- base_component.py

¦       +-- data_table.py

¦       +-- dropdown.py

¦       +-- matplotlib_viz.py

¦       +-- radio.py

¦   +-- combined_components

¦       +-- __init__.py

¦       +-- combined_component.py

¦       +-- form_group.py

¦   +-- dashboard.py

¦   +-- utils.py

+-- requirements.txt

+-- start

+-- tests

    +-- test_employee_events.py
    +-- test_sql_execution.py
```

## Setup & Installation



### Prerequisites



- Python 3.8 or higher

- pip

- Virtual Environment (optional but recommended)



### Instructions



1. **Clone the repository:**

   ```bash

   git clone https://github.com/yourusername/
   
   data_science_dashboard_project.git

   cd data_science_dashboard_project

   python -m venv env
   
   source env/bin/activate  # On Windows: env\Scripts\activate

   pip install -r requirements.txt

   ```

2. **Running the Application:**

   To start the application locally, run:

   ```bash

   uvicorn report.dashboard:app --reload --port 5001
   ```

Then, open your web browser and navigate to: http://localhost:5001

3. **Running Tests:**

To run the tests, use:
   ```bash
   pytest --maxfail=1 --disable-warnings -v
   ```
 