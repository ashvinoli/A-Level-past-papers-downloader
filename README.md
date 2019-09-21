# A-Level-past-papers-downloader
This small program written in python downloads all past-papers from http://onlineexamhelp.com at once. It scrapes the site for the subject chosen and downloads it all and saves it to E:\past_papers folder.
## Installation
Install all dependencies
```bash
pip install beautifulsoup4
```
## Usage
Using the program is simple, just
```
python get_all_pdfs_from_site.py
```
Make sure you have python 3.7 or higher version if available. Beautiful Soup might behave differently or might not even work or install in python 3.5. After the program starts running, you will see a list of subjects and numbers preceding them. Select the appropriate number for the subjects, and then the program will show you which year's papers are available. From the list enter starting year and ending year between (and inculding) which you want to download the papers for that subject you enterd number. Hit enter and wait for download!!
Feel free to change and play around with the code. You might want to add dialog box to get dynamic save folder, but  I was too lazy for that.
