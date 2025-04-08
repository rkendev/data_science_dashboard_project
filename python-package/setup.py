from pathlib import Path
from setuptools import setup, find_packages


cwd = Path(__file__).resolve().parent
# Read requirements from 'employee_events/requirements.txt'
requirements = (cwd / "employee_events" / "requirements.txt").read_text().split("\n")


setup_args = dict(
    name="employee_events",
    version="0.0",
    description="SQL Query API",
    packages=find_packages(),
    # "package_data" tells setuptools which extra files to include in the
    # package. If your "employee_events.db" is inside the "employee_events"
    # folder, you can do:
    #   package_data={'employee_events': ['employee_events.db']},
    # or if you'd prefer the wildcard approach:
    package_data={"": ["employee_events.db", "requirements.txt"]},
    # This is the correct keyword argument, recognized by setuptools:
    install_requires=requirements,
    # (Optional) If you want to ensure that package_data is included in
    # wheels/sdist:
    include_package_data=True,
)


if __name__ == "__main__":
    setup(**setup_args)
