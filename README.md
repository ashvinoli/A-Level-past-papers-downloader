# A-Level-past-papers-downloader
This small program written in python downloads all past-papers from https://papers.gceguide.com/A Levels/ at once. It scrapes the site for the subject chosen and downloads it all and saves it to current directory. The subject name for which the papers are to be generated are to be taken from above site and pasted to the "subjects.json" file.

## Installation
Install all dependencies
```bash
pip install -r requirements.txt
```
## Usage
Using the program is simple, just
```
python get_all_pdfs_from_site.py
python merge_pdfs.py
```

Make sure you have python 3.7 or higher version if available. Beautiful Soup might behave differently or might not even work or install in python 3.5. 
