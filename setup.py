import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='eipy',
    py_modules=['eipy'],
    version='2017.8.4',
    author='Gabriel Pelouze',
    author_email='gabriel@pelouze.net',
    description='An simple embedded IPython shell for an easy code inspection',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gpelouze/eipy',
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=['IPython>=6.1.0', 'traitlets>=4.3.2'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
)
