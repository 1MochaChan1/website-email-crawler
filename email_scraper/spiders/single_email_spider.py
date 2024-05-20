import re
from helpers.colors import Colors
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from helpers.utils import FileHandlingHelper, EmailListHelper, CMDArgsHelper, ProcessCreator

emails_found = set()


# CRAWLER
class SingleEmailSpider(CrawlSpider):
    name = "email_spider"
    
    rules = [
        Rule(LinkExtractor(), callback='parse_item', follow=True), 
    ]
    def parse_item(self, response):
        _email_list_helper = EmailListHelper()
        _raw_emails = re.findall(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[(?!png|webp|svg|jpeg|jpg|ico)a-zA-Z_-]+)', response.text)
        _cleaned_emails = _email_list_helper.remove_catch_all_emails([email.lower() for email in _raw_emails])
        emails_found.update(_cleaned_emails)
    
    def close(spider, reason):
        print(f"{Colors.GREEN}{'•'*30}\nEmails Found:\n{emails_found}\n{'•'*30}{Colors.END}")
        
    #     if(len(spider.emails_found) > 0):
    #         spider.data['email'] = [', '.join(spider.emails_found)] 
    #         FileHandlingHelper().create_res_if_not_present(spider.res_path, spider.src_path)
    #         df = pd.DataFrame(spider.data)
    #         df.to_csv(spider.res_path, mode='a', index=False, header=False)


if(__name__=="__main__"):
    
    res_path, src_path, web  = CMDArgsHelper().handle_cmd_args()
    
    print(web)
        
    print(f"{Colors.PURPLE}{'+'*30}\nCrawl Started\n{'+'*30}{Colors.END}")
    ProcessCreator(spider=SingleEmailSpider).create_spider_and_crawl({'website':web})
    print(f"{Colors.BLUE + Colors.BOLD + Colors.ITALIC}{'-'*12} Process Ended {'-'*12}{Colors.END}")
    
    

# python single_email_spider.py --web "https://example.com"
