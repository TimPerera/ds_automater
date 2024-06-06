# Data Science Environment Setup

## Introduction
When working on data science projects frequently, you may find yourself repeating operations to set up your workspace. This project automates the creation of virtual environments (installation of common data science packages), jupyter notebooks, and git repositories. 

## Installation
To set up the project follow these steps. 

1. Clone the repo
~~~
git clone https://github.com/TimPerera/ds_automater.git
~~~

2. Navigate to the project directory
~~~
cd ds_automater
~~~

3. Create virtual env
~~~
python -m venv .venv
~~~

4. Activate virtual env
- For Windows:
    ~~~
    .venv\Scripts\activate
    ~~~
- For MacOS/Linux
    ~~~
    source .venv/bin/activate
    ~~~

5. Install required packages:
    ~~~
    pip install -r requirements.txt
    ~~~

### Usage
Run the command below to setup a data science environment:
~~~
python src/main.py --file_path /path/to/your/directory --name my_project --project_type jupyter-notebook 
~~~