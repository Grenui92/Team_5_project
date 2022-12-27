from setuptools import setup, find_namespace_packages

setup(
    name="help_you",
    version="0.1",
    description="Use it with pleasure",
    url="https://github.com/Grenui92/Team_5_project.git",
    author="Team_5",
    packages=find_namespace_packages(),
    include_packge_data=True,
    package_data={"help_you":["database/contacts.bin", "database/notes.bin"]},
    install_requires=["prompt_toolkit"],
    entry_points={"console_scripts": ["pocket_assistant = help_you.main:main"]}
)
