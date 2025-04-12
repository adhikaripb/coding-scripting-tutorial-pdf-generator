from setuptools import setup, find_packages

setup(
    name='tutorial-text2pdf-style',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fpdf',
    ],
    entry_points={
        'console_scripts': [
            'txt2pdf-style=tutorial_text2pdf_style:main',
        ],
    },
    author='Prakash Babu Adhikari',
    author_email='your_email@example.com',
    description='Convert cleanly formatted .txt documentation into color-styled PDF files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/adhikaripb/coding-scripting-tutorial-pdf-generator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
