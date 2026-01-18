from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """
    This function will return list of requirements
    """
    requirement_list:List[str] = []
    
    try:
        # Open and read the requirements.txt file
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            # Process each line
            for line in lines:
                requirement = line.strip()
                # Ignore empty lines and -e .
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")

    
        
    return requirement_list
print(get_requirements())

setup(
    name="BasketVision",
    version="0.0.1",
    author="wasim hassan",
    author_email="wasim7x@gamil.com",
    packages = find_packages(),
    install_requires=get_requirements()
)