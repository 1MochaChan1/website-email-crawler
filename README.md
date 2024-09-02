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

1. Ideally you need to go to the root folder after cloning `cd website-email-crawler` and now you can use the csv commands for crawling websites for emails.
    1. `--src {path_to_result_file}` - the flag specifies the input file from which you will take the data. By default it is set to _src.csv_.
    2. `--res {path_to_result_file}` - ((optional)) the flag specifies which file you want to store the output in, if the file doesn't exists it will create on with the same headers as the source (src) file. By default it is set to _res.csv_.
2. Finally you can call run the `email_spider.py` file using the following command:
    - `python email_spider.py --src 'path/to/src.csv'`
3. Alternatively you can navigate to the folder root folder `cd email_scraper\spiders`
4. You can either run the file: `email_spider.py` from an IDE.

## More Useful Flags
#### `--res`
    Enter the path of the file in which the results needs to be stored.
#### `--web`
    Enter the url of the website you want to crawl for emails.
#### `--cleanup`
    Enter the path of the csv file containing the column "website" to clean it.
#### `--keep_cols`
    Enter the list of columns that you want keep from a csv file and the rest of them will be dropped in the final file.
#### `--crawl_csv`
    Use this flag if you want to crawl websites inside a csv file.
#### `--make_csv_for_verif`
    Enter the path of the file containing the scraped emails in single cells. 
    This will prepare the document for verification by creating rows for each email found for a specific domain. 
    Creates a **for_verif** file.
#### `--map_verified_emails`
    If your verified list doesn't return the extra data you added to it. 
    This flag helps to map your verified emails to the data in the **for_verif** file.

> [!TIP]
> Also the ideal way of doing this would be, cleaning the sheet using:
> 1. `--cleanup`
> 2. `--keep_colunmns`
> 3. `--crawl_csv`
> 4. `--make_csv_for_verif`
> 5. `--map_verified_emails` _if used MillionVerifier_

### Caveat
1. Still not able to parse header and footer of websites. Will try BS4 for that probably idk.
