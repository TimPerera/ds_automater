"""
Set up data science project in user-defined location.

# Set up virtual environment, install requirements
# Create requirements.txt file
# Create notebook
# Create .gitignore file (populate it with basics)
 
"""
import logging 
import argparse
import os
import subprocess
import sys
import shutil
import nbformat as nbf

PACKAGES = ['numpy','pandas',
            'openpyxl',
            'scikit-learn',
            'matplotlib','seaborn',
            'notebook']

ignore_file_types = ['*.txt','*.csv','*.xlsx','*.xls','*.ipynb_checkpoints','*.vscode','.git']
logger = logging.getLogger(__name__)

def verify_directory(file_path):
    """Argparse argument checker. Checks to see if file path provided by user exists. 

    Args:
        file_path: directory path to setup data science project.

    Returns:
        file_path

    Raises:
        argparse.ArgumentTypeError
    """
    if os.path.exists(file_path):
        return file_path
    else:
        raise argparse.ArgumentTypeError('Invalid file path supplied.')
    
def validate_name(fname):
    """Argparse argument checker. Checks to see if name contains any invalid characters.

    Args:
        fname (str): folder name
    
    Returns:
        None

    Raises:
        argparse.ArgumentTypeError
    """
    bad_syntax = [',','.','/','\\','\n','\t','?']
    res = any([letter in bad_syntax for letter in fname])
    if res: # Bad character detected in name
        return argparse.ArgumentTypeError('Invalid folder name supplied.')
    
def safe_delete(file_path):
        folders_to_remove = ['.venv','data','.git']
        files_to_remove = ['solution.py','solution.ipynb','requirements.txt','.gitignore','.DS_Store']
        for folder in folders_to_remove:
            if os.path.exists(os.path.join(file_path, folder)):
                shutil.rmtree(os.path.join(file_path, folder))
        for file in files_to_remove:
            if os.path.exists(os.path.join(file_path, file)):
                os.remove(os.path.join(file_path, file)) 
        os.rmdir(file_path)               
        logger.info(f'Removed directory at {file_path}')

def main(file_path, folder_name, project_type, git, cleanup, verbose):
    """Main app logic. Sets up environment for data science project. 

    Args:
        file_path (str): Directory where data science project will be created.
        folder_name (str): Folder name for data science project.
        type (str): Determines if file created is a jupyter notebook or python file.
        git (bool): Defines whether to instantiate a git repository.
        cleanup (bool): Instead of creating a new data science project, setting this to True
                        will remove the path directory/folder_name provided. 
        verbose (bool): Produce more output to console.
    Returns:
        None
    
    """
    full_fpath = os.path.abspath(os.path.join(file_path,folder_name))
    if cleanup and verify_directory(full_fpath): # remove directory
        safe_delete(full_fpath)
        return 
    logger.debug(f'Creating Data Science Environment under {full_fpath}.\nVerbose: {verbose}')
    # ensure latest version of pip is available 
    
    if not os.path.exists(full_fpath):
        os.mkdir(full_fpath)
        logger.debug(f'Created new file path {full_fpath}.')
    os.chdir(full_fpath) # navigate to defined file path
    logger.debug(f'Full fpath is {full_fpath}')
    
    ####
    # Environment Setup
    ###
    # setup virtual environment
    if os.path.exists(full_fpath):
        subprocess.run([sys.executable,'-m','venv','.venv'])
        logger.debug('Virtual env created.')
    venv_path = os.path.join(full_fpath, '.venv')
    logger.debug(f'Venv path is {venv_path}')
    if os.name == 'nt':
        activate_script = os.path.join(venv_path,'Scripts','activate')
        subprocess.run(f"{activate_script} && pip install  {' '.join(PACKAGES)}",shell=True)
        # subprocess.run(f'{activate_script} && jupyter notebook --generate-config')
    elif os.name=='posix':
        activate_script = os.path.join(venv_path, 'bin','activate')
        logger.debug(f'Activate script is {activate_script}')
        subprocess.run(f"source '{activate_script}' && \
                       python -m pip install --upgrade pip && \
                       pip install {' '.join(PACKAGES)}",shell=True)
        logger.debug('Completed installing packages.')
        # if type=='jupyter-notebook':
        #     subprocess.run(f'jupyter notebook --generate-config')
    if git:
        subprocess.run(['git','init'])
        logger.info('Instantiated git')
    ####
    # File creations.
    ####
    # Create a folder to store data
    if not os.path.exists('./data'):
        os.mkdir('./data',)

    # Create requirements.txt file 
    requirements_text = '\n'.join(PACKAGES)
    with open('requirements.txt','w') as file:
        file.write(requirements_text)
    
    # Create .gitignore file
    with open('.gitignore','w') as file:
        file.write('\n'.join(ignore_file_types))

    if project_type == 'jupyter-notebook':
        nb = nbf.v4.new_notebook()
        cells = [
            nbf.v4.new_markdown_cell('# Solution Notebook'),
            nbf.v4.new_code_cell('import numpy as np\nimport pandas as pd')
        ]
        nb['cells'].extend(cells)
        with open('solution.ipynb','w') as file:
            nbf.write(nb, file)
        logger.debug('Created jupyter notebook.')
    elif project_type == 'python':
        with open('solution.py','w') as file:
            file.write('import pandas as pd\nimport numpy as np')
        logger.debug('Created python file.')

if __name__ == '__main__':
    logging.basicConfig(
    #level=logging.INFO,
    level=logging.DEBUG,
    format = '%(asctime)s - %(name)s - %(lineno)d: \n%(message)s',
    datefmt = '%H:%M:%S'
    )
    
    parser = argparse.ArgumentParser(
    prog = 'DataScienceProjectSetup',
    description='Setup environment and files necessary to conduct a Data Science project'
    )
    parser.add_argument('--file_path', '-f', 
                        action='store',
                        required=True, 
                        type=verify_directory,
                        help='Directory to setup DS Project.')
    parser.add_argument('--name','-n',
                        action='store',
                        required=True,
                        )
    parser.add_argument('--project_type','-p',
                        action='store',
                        choices=['jupyter-notebook','python'],
                        help='Choose whether create a jupyter notebook or normal python file.')
    parser.add_argument('--verbose','-v', 
                        action='store',
                        default=True, 
                        dest='verbose',
                        help='Provide more logging information.')
    parser.add_argument('--cleanup','-c',
                        action='store',
                        default=False)
    parser.add_argument('--git',
                        '-g',
                        action='store',
                        type=bool,
                        help='Choose whether to instantiate a git repository.')
    args = parser.parse_args()
    
    main(args.file_path, args.name, args.project_type, args.git, args.cleanup, args.verbose)
