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
        _email_list_helper = EmailListHelper()
        _raw_emails = re.findall(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[(?!png|webp|svg|jpeg|jpg|ico)a-zA-Z_-]+)', response.text)
        _cleaned_emails = _email_list_helper.remove_catch_all_emails([email.lower() for email in _raw_emails])
        emails_found.update(_cleaned_emails)
        self.data['email'] = emails_found
    
    def close(spider, reason):
        # print(f"{Colors.GREEN}{'•'*30}\nEmails Found:\n{emails_found}\n{'•'*30}{Colors.END}")
        pass

if(__name__=="__main__"):
    pass    
    # res_path, src_path, web  = CMDArgsHelper().handle_cmd_args()
    
    # print(web)
        
    # print(f"{Colors.PURPLE}{'+'*30}\nCrawl Started\n{'+'*30}{Colors.END}")
    # ProcessCreator(spider=SingleEmailSpider).create_spider_and_crawl({'website':web})
    # print(f"{Colors.BLUE + Colors.BOLD + Colors.ITALIC}{'-'*12} Process Ended {'-'*12}{Colors.END}")
    
    

# python single_email_spider.py --web "https://example.com"
