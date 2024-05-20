from email_scraper.spiders.email_spider import EmailSpider
from email_scraper.spiders.single_email_spider import SingleEmailSpider
from helpers.utils import ProcessCreator, CMDArgsHelper, ExcelHelper, FileHandlingHelper
from helpers.colors import Colors


# Main Functions
def encapsulate_func(function, title:str='START'):
    print(f"{Colors.PURPLE}{'+'*30}\n{title}\n{'+'*30}{Colors.END}")
    function()
    print(f"{Colors.BLUE + Colors.BOLD + Colors.ITALIC}{'-'*12} Process Ended {'-'*12}{Colors.END}")

def clean_file(src_path:str, prefix:str=None,_res_path:str=None):
    df = excel_helper.auto_cleanup('website')
    if(_res_path):
        df.to_csv(_res_path)
        return df
    helper = FileHandlingHelper()
    _res_path = helper.make_res_path(src_path, prefix=prefix)
    df.to_csv(_res_path)
    return df

def keep_columns(columns:list['str'], prefix:str=None,_res_path:str=None):
    df=excel_helper.choose_columns_to_keep(columns=columns)
    if(_res_path):
        df.to_csv(_res_path)
        return df
    _res_path = file_helper.make_res_path(src_path, prefix=prefix)
    
    df.to_csv(_res_path, index=False)
    return df
        

# Entry Point
if __name__ == "__main__":
    args  = CMDArgsHelper().handle_cmd_args()
    res_path =args['res_path']
    src_path=args['src_path']
    web=args['web']
    crawl_csv = args['crawl_csv']
    keep_cols=args['keep_cols']
    cleanup = args['cleanup']

    if(src_path):
        excel_helper = ExcelHelper(src_path)
        file_helper = FileHandlingHelper()
        
        if(crawl_csv==True):
            ProcessCreator(src_path=src_path, res_path=res_path, spider=EmailSpider).create_spider_processes()
            
        if(cleanup):
            clean_file(src_path, prefix='cleaned-')
            
        if(keep_cols):
            keep_columns(columns=keep_cols, prefix='trimmed')
    
    if(web):
        data = ProcessCreator(spider=SingleEmailSpider).create_spider_and_crawl({'website':web})
        print(f'{Colors.BROWN}\n+{"+"*10}\n{data}\n{"+"*10}{Colors.END}')
        