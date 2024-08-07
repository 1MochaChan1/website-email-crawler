import re, sys


import pandas as pd
from helpers.utils import FileHandlingHelper, EmailListHelper, CMDArgsHelper, ProcessCreator
from helpers.colors import Colors
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


def save_csv(data:map,src_path:str, res_path:str=None):
    import pandas as pd
    file_helper = FileHandlingHelper()
    if(res_path==None):
        res_path = file_helper.make_res_path(src_path)
    file_helper.create_res_if_not_present(src_path, res_path)
    df = pd.DataFrame.from_dict(data)
    df.to_csv(res_path, mode='a', index=False, header=False)
    print(f'{Colors.GREEN} file saved as: {res_path}{Colors.END}')

# CRAWLER
class EmailSpider(CrawlSpider):
    emails_found = set()
    name = "email_spider"
        
    rules = [
        Rule(LinkExtractor(allow='about'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='about-me'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='about-us'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='contact-us'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='contactus'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='contact'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='contact-me'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='company'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='meet-the-team'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='meet-our-agents'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='our-agents'), callback='parse live_item', follow=False),
        Rule(LinkExtractor(allow='agent'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='agents'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='team-page'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='our-team'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='staff'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='profile'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='member'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='our-staff'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='our-people'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='leadership'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='management'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='executive-team'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='our-experts'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='support'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='help'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='staff-directory'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='our-experts'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='support-team'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='profile'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='meet-our-team'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='leadership'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='executives'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='our-crew'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='people'), callback='parse_item', follow=False),   
        ]
    
    def parse_item(self, response):
        _email_list_helper = EmailListHelper()
        _raw_emails = re.findall(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[(?!png|webp|svg|jpeg|jpg|ico)a-zA-Z_-]+)', response.text)
        _cleaned_emails = _email_list_helper.remove_catch_all_emails([email.lower() for email in _raw_emails])
        self.emails_found.update(_cleaned_emails)
        yield self.data
    
    def close(spider, reason):
        print(Colors.GREEN,"="*40+'\n',spider.emails_found,'\n'+"="*40, Colors.END)
        
        if(len(spider.emails_found) > 0):
            spider.data['email'] = [', '.join(spider.emails_found)] 
            save_csv(spider.data, spider.src_path)
        
if(__name__=="__main__"):
    pass

