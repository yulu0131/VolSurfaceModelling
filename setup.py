from setuptools import setup, find_packages

install_requires = ["pandas>=1.4.1",
                    "matplotlib>=3.5.1",
                    "openpyxl>=3.0.9",
                    "scipy>=1.8.0"]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    # these rarely change
    name="src",
    description='A package for building the IVV Surface based on the SVI model and using Choice data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='derivatives, finance',
    license='Free for non-commercial use',
    author='Hao Yu',
    author_email='yuhao0126liuer@gmail.com',
    # these may change frequently
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.9',
    install_requires=install_requires,
)