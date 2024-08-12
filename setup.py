from setuptools import setup, find_packages

setup(
    name='my_project',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Add your runtime dependencies here
    ],
    extras_require={
        'dev': [
            'pytest',
            # Add other development dependencies here
        ],
    },
)
