import re, os


class CMDArgsHelper():
    '''
    This is an API for creating Arguments
    '''
    def __init__(self) -> None:
        pass

class FileHandlingHelper():
    '''
    An easier way to handle file creation,saving and updating.
    '''
    def __init__(self) -> None:
        pass
    
    def make_res_path(self, src_path:str, prefix:str='res-') -> str:
        path = os.path.split(src_path)
        if (not len(path[0]) > 0):
            return f'res-{src_path}'
        # This will give problems on Linux or any OS apart from Windows.
        return f"{path[0]}\\{prefix}{path[1]}"

class ExcelHelper():
    import pandas as pd
    from copy import copy
    def __init__(self, filename:str) -> None:
        self.base_df = self.pd.read_csv(filename, index_col=False)
    
    
    def drop_na(self, column_name:str, dataframe=None) -> pd.DataFrame:
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
            before = _df.at[row.Index, column_name]   
            base_url = re.match(r'^(https?:\/\/[^\/]+)', before)
            _df.at[row.Index, column_name] = base_url.group()
            # after = _df.at[row.Index, column_name]
            # print(f"\nBefore: {before}\nAfter: {after}")
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
        res = self.drop_na(column_name)
        res1 = self.strip_slug(column_name, dataframe=res)
        res2 = self.remove_duplicates(column_name, dataframe=res1)
        
        return res2

if __name__ == "__main__":
    filename="..\\data\\doctors.csv"
    res = FileHandlingHelper().make_res_path(filename, prefix="cleaned-")
    
    helper = ExcelHelper(filename)

    df = helper.auto_cleanup('website')
    df.to_csv(res, index=False)

    
    