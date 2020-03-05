# python 3.8.1
from os import walk
from re import search
from time import perf_counter
from multiprocessing import Pool
from win32api import GetLogicalDriveStrings

l_default_root_paths = GetLogicalDriveStrings().split('\000')[:-1]
s_default_path_filter = ''
s_default_query = ''
i_default_filter_flag = 0
i_default_parallel = 1

__test__ = True
log = lambda *args, **kwargs: print(*args, **kwargs) if __test__ else None

class Search:
    def __init__(self):
        self.root_paths    = self.get_root_paths()
        self.path_filter   = self.get_path_filter()
        self.e_path_filter = self.edit_regex(self.path_filter)
        self.query         = self.get_query()
        self.filter_flag   = self.get_filter_flag()
        self.parallel      = self.get_parallel()
        self.timer         = 0

    def timeit(func):
        def wrapper(self, *args, **kwargs):
            self.time = perf_counter()
            value = func(self, *args, **kwargs)
            self.time = perf_counter() - self.time
            print(f'\nDone in {int(self.time)} seconds.\n')
            return value
        return wrapper

    def get_root_paths(self):
        '''Add one or more rootpaths separated by semicolons (optional). Default '''
        s_input = input('Enter root-paths. Example: c:\Program Files; d:\\\n: ')
        l_paths = []
        if s_input: l_paths = [s_input]
        if ';' in s_input: l_paths = [path.strip() for path in s_input.split(';') if path.strip()]
        return l_paths or l_default_root_paths

    def get_path_filter(self):
        '''Add path-filter (optional). Takes regular expresion as input.'''
        return input('Enter path-filter (regex). Example: .*[Uu]ser.*\n: ') or s_default_path_filter

    def get_query(self):
        '''Add search query (optional). Takes regular expresion as input.'''
        return input('Enter search-query (regex). Example: \.(mp3|wav)$\n: ') or s_default_query

    def edit_regex(self, regex):
        '''Edited regex is used for faster dir names lookup in paths.'''
        return regex[regex[0]=='^' : -(regex[-1]=='$') or None] if regex else ''

    def get_filter_flag(self):
        '''Add search flag (optional): 1 for dirs-only, 2 for file-only.'''
        s_input = input('enter search-flag ([int], 0:all, 1:dirs-only, 2:files-only)\n: ')
        i_input = i_default_filter_flag
        if s_input and s_input.isdigit() and int(s_input) != i_input:
            i_input = int(s_input)
        return i_input

    def get_parallel(self):
        '''Add multiprocessing support (optional). Root-paths will be scaned in parallel. '''
        s_input = input('Use multiprocessing (0:no, 1:yes)\n: ')
        if s_input and s_input.isdigit():
            return int(s_input[0])
        else:
            return i_default_parallel

    def scan_root_path(self, root_path):
        list(map(self.scan_dirs_files, walk(root_path)))

    def scan_dirs_files(self, root_tuple):
        root, dirs, files = root_tuple
        if self.e_path_filter not in root:
            return
        path_match = [r for r in root.split('\\') if search(self.path_filter, r)]
        if not path_match:
            return
        dirs_match  = [d for d in dirs  if search(self.query, d)]
        files_match = [f for f in files if search(self.query, f)]
        if (dirs_match and self.filter_flag != 2) or (files_match and self.filter_flag != 1):
            print('-' * 50)
            print(root)
        if dirs_match and self.filter_flag != 2:
            print('  dirs:\n    ', end='')
            print(*dirs_match, sep='\n    ')
        if files_match and self.filter_flag != 1:
            print('  files:\n    ', end='')
            print(*files_match, sep='\n    ')

    @timeit
    def start(self):
        print('searching...')
        #self.time = perf_counter()
        if self.parallel:
            p = Pool()
            p.map(self.scan_root_path, self.root_paths)
            p.close()
            p.join()
        else:
            list(map(self.scan_root_path, self.root_paths))
        #self.time = perf_counter() - self.time
        #print(f'\nDone in {int(self.time)} seconds.\n')

#-----------------end of search class-----------------

def restart(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            input('Press any key to continue...')
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
    print(('='*50) + '\nSIMPLE SEARCH multiprocessing version\n')
    print(f'''Defaults: 
    {l_default_root_paths=}
    {s_default_path_filter=}
    {s_default_query=}
    {i_default_filter_flag=}
    {i_default_parallel=}''')
    print('='*50)
    main()
