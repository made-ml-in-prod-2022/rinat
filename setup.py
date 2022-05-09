from setuptools import find_packages, setup


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name="ml_example",
    packages=find_packages(),
    version="0.1.0",
    description="ml_project_train",
    author="Xrenya",
    entry_points={
        "console_scripts": [
            "ml_project_train = ml_project.train:run"
        ]
    },
    install_requires=required,
    license="MIT",
)