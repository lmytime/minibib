from setuptools import setup, find_packages

setup(
    name='minibib',
    version='1.0.1',
    description='A simple script to create a clean `.bib` file containing only the references cited in your `.tex` document.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mingyu Li',
    author_email='lmytime@hotmail.com',
    url='https://github.com/lmytime/minibib',
    license='MIT',
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'minibib = minibib.minibib:main',
        ],
    },
    python_requires='>=3.6',
)