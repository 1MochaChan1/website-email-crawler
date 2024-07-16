from scrapy.signals import spider_closed
import re, os, argparse, tldextract
from .colors import Colors
import pandas as pd
from multiprocessing import Process, Pool
from scrapy.crawler import CrawlerProcess


class CMDArgsHelper():
    '''
    This is an API for creating Arguments
    '''
    
    def handle_cmd_args(self):
        res_path=None
        src_path=None
        web=None
        cleanup=False
        keep_cols = False
        crawl_csv=False
        make_csv_for_verif=False
        map_verified_emails=None
        
        parser = argparse.ArgumentParser(description='Crawls given websites in the csv file and returns the data with the email against their names.')
        parser.add_argument('--src', metavar='src', type=str, help='src-dependent Enter the path of the source file which consists of websites needed to crawl')
        parser.add_argument('--res', metavar='res', type=str, help='Enter the path of the file in which the results needs to be stored.')
        parser.add_argument('--web', metavar='web', type=str, help='Enter the url of the website you want to crawl for emails.')
        parser.add_argument('--cleanup',  action='store_true', help='Enter the path of the csv file containing the column "website" to clean it.')
        parser.add_argument('--keep_cols', metavar='keep_cols', nargs='+', help='Enter the list of columns that you want keep from a csv file and the rest of them will be dropped in the final file.')
        parser.add_argument('--crawl_csv',  action='store_true', help='Use this flag if you want to crawl websites inside a csv file.')
        parser.add_argument('--make_csv_for_verif', action='store_true', help='Enter the path of the file containing the scraped emails in single cells. This will prepare the document for verification')
        
        parser.add_argument('--map_verified_emails', metavar='map_verified_emails', type=str, help='Enter the path of the file in which the verified emails are stored.')

        
        args = parser.parse_args()
        if(args.web):
            web = args.web
        
        if (args.src):
            src_path = args.src

            if (args.res):
                res_path = args.res
            else:
                if(src_path):
                    os.path.split(src_path)
                    res_path = FileHandlingHelper().make_res_path(src_path)
            
            
            if (args.cleanup == True):
                cleanup = args.cleanup
                
            if (args.keep_cols):
                keep_cols = args.keep_cols
                
            if (args.crawl_csv):
                crawl_csv = args.crawl_csv
            
            if (args.make_csv_for_verif == True):
                make_csv_for_verif = args.make_csv_for_verif
            
            if(args.map_verified_emails):
                map_verified_emails = args.map_verified_emails
        else:
            print(f'{Colors.RED}To use the other opertaions, you have to pass in the source file first{Colors.END}')
        
        return {'res_path':res_path,'src_path':src_path,'web':web, 'cleanup':cleanup, 'keep_cols':keep_cols, 'crawl_csv':crawl_csv, 'make_csv_for_verif':make_csv_for_verif, 'map_verified_emails':map_verified_emails}


class EmailListHelper():
    '''
    This class provides helpers that aid in cleaning the emails
    '''
    
    def get_domain(self, website:str):
        ext = tldextract.extract(website)
        return ext.domain+'.'+ext.suffix

    def remove_catch_all_emails(self, emails:list):
        ex_list = [ "info@", "contact@", "support@", "help@", "service@", "admin@", 
                   "team@", "hello@", "sales@", "inquiries@", "webmaster@", "office@", 
                   "management@", "all@", "hr@", "johndoe@", "logo", "exams@", "media@", 
                   "recruitment@", "enquiries@", "@sentry", "business@", "jpeg", "png", 
                   "jpg", "assistant@", "example", "example.com", "press@", "wixpress.com", 
                   "user@", "@domain.com", "communications@", ".gif", 'internship@',
                   'career@', 'attorneys@', 'outreach@', 'members@', 'member@', 'marketing@', 'inquiry@',
                   'receptionist@', 'staff@', 'administration@', 'partners@', 'admin@', 'apline@',
                   'sentri.io','learnmore@']
        
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

    def extract_emails(self, src_path:str):
        '''
        Takes the `website` and the `email` column and creates and array of dicts with key, value pairs being `website` and `email` respectively.
        You can upload this file to MillionVerifiers.com.
        '''
        email_data = []
        
        _df = pd.read_csv(src_path)
        for _, row in _df.iterrows():
            emails = row['email'].split(', ')
            for email in emails:
                email_data.append({'website':row['website'], 'email':email})
            
        email_csv = pd.DataFrame.from_records(email_data)
        return email_csv        
        
        
    def map_verified_email(self, src_path:str, verif_path:str, separate:bool=False):
        '''
        This function returns a dcitionary with verified emails in their own columns, provided the columns passed to it has a column named `website`.
        
        The `verif_path` here refers to the file that was downloaded from MillionVerifiers.com after verification.
        '''
    
        _df_emails = pd.read_csv(verif_path)
        _df_src = pd.read_csv(src_path)
        _df_map = []
        if(separate):
            for _, row in _df_src.iterrows():
                curr_website = row['website']
                verified_col_idx=0
                
                for _, e_row in _df_emails.iterrows():
                    if(curr_website==e_row['website']):
                        row[f'verified_email_{verified_col_idx}'] = e_row['email']
                        final_row = row.drop('email')
                        _df_map.append(final_row.to_dict())
                        verified_col_idx += 1
        else:
            for _, row in _df_src.iterrows():
                curr_website = row['website']
                
                for _, e_row in _df_emails.iterrows():
                    if(curr_website==e_row['website']):
                        final_row = row.to_dict()
                        final_row.pop('email')
                        final_row['verified_email'] = e_row['email']
                        _df_map.append(final_row)
        _res = pd.DataFrame.from_records(_df_map)
        # if(separate):
        #     _res.drop_duplicates('website', keep='last', inplace=True)
        return _res



class FileHandlingHelper():
    '''
    An easier way to handle file creation,saving and updating.
    '''
    def __init__(self) -> None:
        pass
    
    def make_res_path(self, src_path:str, prefix:str='res-') -> str:
        '''
        Automatically creates a path in the same directory of the `src_path`.
        
        A `prefix` could be added before the file naem to avoid conflicts. default is 'res-'
        '''
        path = os.path.split(src_path)
        if (not len(path[0]) > 0):
            return f'{prefix}{src_path}'
        # This will give problems on Linux or any OS apart from Windows.
        return f"{path[0]}\\{prefix}{path[1]}"


    def create_res_if_not_present(self,src_path:str,res_path:str=None):   
        '''
        Creates a CSV file with only headers from the `src_files` along with an extra column 'email' and saves as `res_path`
        '''
         
        if(res_path==None):
            res_path = self.make_res_path(src_path)
            
        if(os.path.isfile(res_path)):
            if(os.stat(res_path).st_size != 0):
                return
        
            
        df = pd.read_csv(src_path)
        _res_df = pd.DataFrame()
        columns = df.columns.to_list()
        columns.append('email')
        for col in columns:
            _res_df[col]=""
        _res_df.to_csv(res_path, index=False, mode='a')


# TODO: 1. Create a Spider Extension
#       2. Connect it to the spider close signal and call a function that stores yielded data.
class ProcessCreator():
    '''
    Class that is responsible for creating spider processes to crawl the websites passed to it.
    '''
    def __init__(self, spider, src_path:str=None, res_path:str=None) -> None:
        self.src_path = src_path
        self.res_path = res_path
        self.spider = spider
        self.mapped_data = []
        
    def create_spider_and_crawl(self, data:dict):
        '''
        Creates a spider processes to crawl given website in `data`
        Example:
        `{'website':'http://example.com'}`
        '''
        website = data['website']
        process = CrawlerProcess()
        self.spider.res_path = self.res_path
        self.spider.data = data
        self.spider.src_path = self.src_path
        self.spider.allowed_domains = [EmailListHelper().get_domain(website)]
        self.spider.start_urls = [website]
        process.crawl(self.spider)
        # for crawler in process.crawlers:
        #     crawler.signals.connect(self.spider_ended, signal=spider_closed)
        process.start()   
        process.join()
        return self.spider.data
    

    
    def create_spider_processes_sequence(self):
        '''
        Creates individual instances of spider processes to crawl multiple websites
        '''
        df = pd.read_csv(self.src_path)
        for _, row in df.iterrows():
            try:
                if(len(row['website']) < 1):
                    continue

                row['email'] = ''
                data = row.to_dict()
                p1 = Process(name=data['website'], target=self.create_spider_and_crawl, args=[data])
                p1.start()
                p1.join()
            except TypeError as e:
                print(f"{Colors.RED}ALERT: Could not find any 'website' in the cell. Possibly the value for website in your csv file has been left blank{Colors.END}")
            except KeyError as e:
                print(f"{Colors.RED}ALERT: Possibly the column 'website' is not present in your csv file Either try adding such column or renaming an existing one{Colors.END}")
            except Exception as e:
                print(f"{Colors.RED}{e}{Colors.END}")
        
        return self.mapped_data
    
    
    # def get_params(self):
    #     df = pd.read_csv(self.src_path)
    #     data = df.to_dict('records')
    #     for rec in data:
    #         yield rec
    
    def create_spider_processes_pool(self):
        '''
        Creates a pool of spider processes to crawl multiple websites
        '''
        data=None
        pool = Pool()
        
        df = pd.read_csv(self.src_path)
        data = df.to_dict('records')
        
        data = pool.map(self.create_spider_and_crawl, data)
        
        pool.close()
        pool.join()
        
        return data
        # try:
            
        # except Exception as e:
        #     print(f'{Colors.RED} {e}\n')
        #     print(f'Something went wrong when running the pooled processes{Colors.END}')
        #     return data
        # finally:
        #     return data



class ExcelHelper():
    '''
    A class responsible for handling operations related to csv files.
    '''
    import pandas as pd
    def __init__(self, filename:str) -> None:
        self.base_df = self.pd.read_csv(filename, index_col=False)
    
    
    def drop_na(self, column_name:str, dataframe=None) -> pd.DataFrame:
        '''
        Drops the records having null values in the column: `column_name`
        '''
        if(dataframe is not None):
            _df = dataframe
        else:
            _df = self.base_df.loc[:]
            
        _df = _df.dropna(subset=[column_name])
        return _df
    
    def strip_slug(self, column_name:str, dataframe=None):
        '''
        Strips the slug of a web url leaving only the base url
        '''
        if(dataframe is not None):
            _df = dataframe
        else:
            # Making a copy to supress warning (https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas#:~:text=(recommended)%20Use%20loc%20to%20slice%20subsets%3A)
            _df = self.base_df.loc[:]

        for row in _df.itertuples():
            try:
                before = _df.at[row.Index, column_name]   
                base_url = re.match(r'^(https?:\/\/[^\/]+)', before)
                _df.at[row.Index, column_name] = base_url.group()
            except AttributeError as e:
                print(f'{Colors.RED} {e} {Colors.END}')
        return _df
        
    
    def remove_duplicates(self, column_name:str, dataframe=None):
        '''
        Cleans the sheet of redundant data for the given `column_name`
        ''' 
        if(dataframe is not None):
            _df = dataframe
        else:
            _df = self.base_df.loc[:]


        _df.drop_duplicates(subset=[column_name], keep='first', ignore_index=True, inplace=True)
        
        return _df

    def auto_cleanup(self, column_name:str)-> pd.DataFrame:
        '''
        Does three things in one command.
        
        1. Drops records with `null` values in given `column_name`
        2. Strips the slug of website to keep only the base URL
        3. Removes duplicate base URLs.
        '''
        res = self.drop_na(column_name)
        res1 = self.strip_slug(column_name, dataframe=res)
        res2 = self.remove_duplicates(column_name, dataframe=res1)
        
        return res2
    
    def choose_columns_to_keep(self, columns:list[str], dataframe=None) -> pd.DataFrame:
        '''
        Choose which columns to keep in a csv file. Returns a Datafarme
        '''
        _df:pd.DataFrame
        if(dataframe is not None):
            _df = dataframe
        else:
            _df = self.base_df.loc[:]

        return _df[columns]

if __name__ == "__main__":
    pass
    # filename="D:\\1_Downloads\\ConsultingMerge.csv"
    # res = FileHandlingHelper().make_res_path(filename, prefix="cleaned-")
    
    # helper = ExcelHelper(filename)

    # df = helper.auto_cleanup('website')
    # df.to_csv(res, index=False)

    # filename = '..\\data\\res-cleaned-ConsultingMerge_1.csv'
    # res_sheet = ExcelHelper(filename)
    # res_sheet.choose_column(['name','phone_number','email', 'website' ,'review_count', 'rating'])



# python email_spider.py --src "source_file.csv"
    
    