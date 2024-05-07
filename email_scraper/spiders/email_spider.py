import re, tldextract, logging
import pandas as pd
import argparse
from colors import Colors
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process

# logging.configure_logging(install_root_handler=False)
logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.DEBUG
)

# HELPER
def _get_domain(website:str):
    ext = tldextract.extract(website)
    return ext.domain+'.'+ext.suffix

def _create_res_if_not_present(res_file, src_file):
    import os
    
    if(os.path.isfile(res_file)):
        if(os.stat(res_file).st_size != 0):
            return
  
    df = pd.read_csv(src_file)
    res_df = pd.DataFrame()
    columns = df.columns.to_list()
    columns.append('email')
    for col in columns:
        res_df[col]=""
    res_df.to_csv(res_file, index=False, mode='a')

def remove_catch_all_emails(emails:list):
    ex_list = ["mail", "info", "contact", "support", "johndoe", "logo", "exams", "media", "service", "recruitment", "enquiries", "team", "@sentry","business","jpeg","png","jpg","assistant", "hello","example","example.com","press","office","wixpress.com"]
    res = []
    for email in emails:
        _break=False
        for ex in ex_list:
            if(ex in email):
                _break=True
                break
        if(_break):
            continue
        res.append(email)

    return res

class EmailSpider(CrawlSpider):
    emails_found = set()
    name = "email_spider"
        
    rules = [
        Rule(LinkExtractor(allow='about'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow='about-me'), callback='parse_item',follow=True),
        Rule(LinkExtractor(allow='about-us'), callback='parse_item',follow=True),
        Rule(LinkExtractor(allow='contact-us'), callback='parse_item',follow=True),
        Rule(LinkExtractor(allow='contactus'), callback='parse_item',follow=True),
        Rule(LinkExtractor(allow='contact'), callback='parse_item',follow=True),
        Rule(LinkExtractor(allow='contact-me'), callback='parse_item',follow=True),
        Rule(LinkExtractor(allow='company'), callback='parse_item',follow=True),
        Rule(LinkExtractor(allow='meet-the-team'), callback='parse_item',follow=True),
        Rule(LinkExtractor(allow='meet-our-agents'), callback='parse_item',follow=True),
        Rule(LinkExtractor(allow='our-agents'), callback='parse_item',follow=True),
        Rule(LinkExtractor(allow='agent'), callback='parse_item',follow=True),
        Rule(LinkExtractor(allow='agents'), callback='parse_item',follow=True),
        Rule(LinkExtractor(allow='team-page'), callback='parse_item',follow=True),     
    ]
    def parse_item(self, response):
        _raw_emails = re.findall(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[(?!png|webp|svg|jpeg|jpg|ico)a-zA-Z_-]+)', response.text)
        _cleaned_emails = remove_catch_all_emails([email.lower() for email in _raw_emails])
        self.emails_found.update(_cleaned_emails)
    
    def close(spider, reason):
        print(Colors.GREEN,"="*40+'\n',spider.emails_found,'\n'+"="*40, Colors.END)
        
        if(len(spider.emails_found) > 0):
            spider.data['email'] = [', '.join(spider.emails_found)] 
            _create_res_if_not_present(spider.res_file, spider.src_file)
            df = pd.DataFrame(spider.data)
            df.to_csv(spider.res_file, mode='a', index=False, header=False)

      
def create_spider(data, src_file, res_file) -> EmailSpider:
    website = data['website']
    
    process = CrawlerProcess()
    spider = EmailSpider
    
    spider.data = data
    spider.res_file = res_file
    spider.src_file = src_file
    spider.allowed_domains = [_get_domain(website)]
    spider.start_urls = [website]
    process.crawl(spider)
    process.start()
    
def process_creation():
    df = pd.read_csv(src_file)
    for _, row in df.iterrows():
        try:
            if(len(row['website']) < 1):
                continue
            
            row['email'] = ''
            data = row.to_dict()
            p1 = Process(name=data['website'], target=create_spider, args=[data, src_file, res_file])
            p1.start()
            p1.join()
        except TypeError as e:
            print(f"{Colors.RED}ALERT: Could not find any 'website' in the cell. Possibly the value for website in your csv file has been left blank{Colors.END}")
        except KeyError as e:
            print(f"{Colors.RED}ALERT: Possibly the column 'website' is not present in your csv file Either try adding such column or renaming an existing one{Colors.END}")
        except Exception as e:
           print(f"{Colors.RED}{e}{Colors.END}")
           
           
def handle_cmd_args():
    global res_file, src_file
    parser = argparse.ArgumentParser(description='Crawls given websites in the csv file and returns the data with the email against their names.')
    parser.add_argument('--src', metavar='src', type=str, help='Enter the path of the source file which consists of websites needed to crawl')
    parser.add_argument('--res', metavar='res', type=str, help='Enter the path of the file in which the results needs to be stored.')
    
    args = parser.parse_args()
    if (args.src):
        src_file = args.src

    if (args.res):
        res_file = args.res
    else:
        res_file = 'res-'+src_file
    
    return res_file,src_file


def verify_emails(src_file_name:str):
    res_file_name = 'res-' + src_file_name
    
    # make request to the workflow.
    

if(__name__=="__main__"):
    res_file='res.csv'
    src_file='src.csv'
    
    res_file, src_file = handle_cmd_args()
    
        
    print(f"{Colors.PURPLE}{'+'*30}\nsrc:{src_file}\nres:{res_file}\n{'+'*30}{Colors.END}")
    process_creation()
    print(f"{Colors.BLUE + Colors.BOLD + Colors.ITALIC}{'-'*12} Process Ended {'-'*12}{Colors.END}")

# python email_spider.py --src "source_file.csv"
