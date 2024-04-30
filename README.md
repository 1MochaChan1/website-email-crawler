# Website Email Crawler
Tool that crawls list of websites given as a csv and finds emails against them and returns another csv similar to the one provided but with an extra column called 'email'.

## Installation
- You will need Python2.7 and above for smooth experience.
- Clone the directory on your machine `git clone https://github.com/1MochaChan1/website-email-crawler.git`.
- Create an environment to be safe `python -m venv env`.
- Install the requirements using the requirement folder `python -m pip install -r requirements.txt`.

## Usage
> [!IMPORTANT]
> Make sure to have a column named `website` in your _src.csv_ file which would contain all the websites that we need to crawl

1. Navigate to the folder spider `cd emaill_scraper\spiders`
2. You can either run the file: `email_spider.py` from an IDE.
3. Alternatively, `email_spider.py` can be given arguements such as
    1. `--src {path_to_result_file}` - the flag specifies the input file from which you will take the data. By default it is set to _src.csv_.
    2. `--res {path_to_result_file}` - ((optional)) the flag specifies which file you want to store the output in, if the file doesn't exists it will create on with the same headers as the source (src) file. By default it is set to _res.csv_.
