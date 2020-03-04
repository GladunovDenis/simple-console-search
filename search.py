# python 3.8.1
from os import walk
from re import search
from time import perf_counter
from settings import l_default_root_paths

__test__ = True
log = lambda *args, **kwargs: print(*args, **kwargs) if __test__ else None

class Search:
    def __init__(self):
        self.root_paths         = self.get_root_paths()
        self.dir_filter         = self.get_dir_filter()
        self.query, self._query = self.get_query()
        self.filter_flag        = self.get_filter_flag()
        self.timer              = 0

    def get_root_paths(self):
        '''Add one or more rootpaths separated by coma (optional). Default '''
        s_input = input('enter root-paths (e.g.: c:\, d:\): ')
        l_paths = []
        if s_input: l_paths = [s_input]
        if ',' in s_input: l_paths = [path.strip() for path in s_input.split(',') if path.strip()]
        return l_paths or l_default_root_paths

    def get_dir_filter(self):
        '''Add directories filter (optional). Takes regular expresion as input.'''
        s_input = input('enter dir-filter (regex): ')
        s_modified_input = self.modify_input(s_input)
        return s_modified_input

    def get_query(self):
        '''Add search query (optional). Takes regular expresion as input.'''
        s_input = input('enter search-query (regex): ')
        s_modified_input = self.modify_input(s_input)
        return s_input, s_modified_input

    def modify_input(self, s_input):
        '''Modified input is nesessary for matching dir names in paths otherwise only '^.*$' dirs will be matched'''
        if not s_input: 
            return ''
        s_modified_input = s_input
        if s_input[0] == '^': 
            s_modified_input = s_input[1:]
        if s_input[-1] == '$':
            s_modified_input = s_input[:-1]
        return s_modified_input

    def get_filter_flag(self):
        '''Add search flag (optional): d for dirs-only, f for file-only.'''
        s_input = input('enter search-flag ([int], 0:all, 1:dirs-only, 2:files-only): ')
        i_input = 0
        if s_input and s_input.isdigit() and int(s_input):
            i_input = int(s_input)
        return i_input

    def scan_root_path(self, root_path):
        counter = 1
        for root, dirs, files in walk(root_path):
            self.scan_dirs_files(root, dirs, files)

    def scan_dirs_files(self, root, dirs, files):
        format_flag = True # format_flag is used to produce less output
        if search(self._query, ''.join(dirs + files)) and search(self.dir_filter, root):
            if self.filter_flag != 2:
                format_flag = self.scan_elements(root, self.query, dirs, 'dir', format_flag)
            if self.filter_flag != 1:
                format_flag = self.scan_elements(root, self.query, files, 'file', format_flag)

    def scan_elements(self, root, query, array, query_type, format_flag):
        got_results = False
        for element in array:
            if search(query, element):
                got_results = True
                if format_flag:
                    print(root)
                    format_flag = False
                print(f'    {query_type}:', element)
        if got_results:
            print('-' * 50)
        return format_flag

    def start(self):
        print('searching...')
        self.time = perf_counter()
        for root_path in self.root_paths:
            self.scan_root_path(root_path)
        self.time = perf_counter() - self.time
        print(f'\ndone in {self.time}\n')

#-----------------end of search class-----------------

def restart(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            input('press any key to continue')
            raise Exception('restart')
        except Exception as e:
            if 'restart' not in str(e): 
                print('Exception:', e)
            wrapper(*args, **kwargs)
    return wrapper

@restart
def main():
    search = Search()
    search.start()
            
if __name__ == '__main__':
    main()
