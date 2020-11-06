# python 3.8.1
from os import walk
from re import match, search
from timeit import timeit
from win32api import GetLogicalDriveStrings






default_root_paths = GetLogicalDriveStrings().split('\000')[:-1]
default_path_filter = r''
default_query = r''
default_filter_flag = 0
default_parallel = 1





notNone = lambda val, method: val if val != None else method()

class Search:
    def __init__(
        self,
        root_paths  = None,
        path_filter = None,
        query       = None,
        filter_flag = None,
    ):
        self.root_paths  = notNone(root_paths,  self.get_root_paths)
        self.path_filter = notNone(path_filter, self.get_path_filter)
        self.query       = notNone(query,       self.get_query)
        self.filter_flag = notNone(filter_flag, self.get_filter_flag)
        self.report      = ''
        


    def get_root_paths(self):
        message = """
You can add one or more rootpaths separated by semicolons.
Program will scan only these paths.

Example: c:\Program Files; 
Example: d:\\
Example: c:\\; d:\\; e:\\Documents

[+] """
        userinput = input(message)
        paths = default_root_paths
        if userinput: 
            paths = [path.strip() for path in userinput.split(';') if path.strip()]
        print(paths)
        return paths


    def get_path_filter(self):
        message = """
You can Add path-filter. 
Takes python regex string as input.

Example: files
Example: .*[Pp]rogram files( \(x86\))?

[+] """
        regex = default_path_filter
        userinput = input(message)
        if userinput:
            start = userinput[0] == '^' # 0 or 1
            end   = -(userinput[-1]=='$') or None # -1 or None
            regex = userinput[start : end]
        print(regex)
        return regex

    def get_query(self):
        message = """
You can add search query (optional). 
Takes python regex as input.

Example: music
Example: \.(mp3|wav)$

[+] """
        query = default_query
        userinput = input(message)
        if userinput:
            query = userinput 
        print(query)
        return query
        

    def get_filter_flag(self):
        message = """
You can add one search flag (optional)
d/f/e (d: dirs-only, f: files-only, e: everything,)

Example: d
Example: f

[+] """
        userinput = input(message)
        flag = default_filter_flag
        if userinput:
            index = "edf".find(userinput)
            if index >= 0:
                flag = index
        print("edf"[flag])
        return flag


    def genetate_report(self, name, data):
        match_str = '\n    '.join(data)
        self.report = f"""{self.report}  {name}:
    {match_str}
"""


    def scan_root_path(self, root_path):
        if self.filter_flag == 1:
            if self.path_filter and self.query:
                query = f"({self.path_filter}|{self.query})"
            else:
                query = self.path_filter or self.query
            [print(values[0]) for values in walk(root_path) if match(query, values[0].rpartition('\\')[-1])]
        elif self.path_filter:
            [self.scan_dirs_and_files(values) for values in walk(root_path) \
                if search(self.path_filter, values[0].rpartition('\\')[-1])]
        else:
            list(map(self.scan_dirs_and_files, walk(root_path)))

    def scan_dirs_and_files(self, values):
        root, dirs, files = values

        conditionC, conditionD = False, False

        if self.filter_flag != 2:
            dirs_match  = [dir for dir in dirs if search(self.query, dir)]
            conditionC = bool(dirs_match)
            if conditionC:
                self.genetate_report("dirs", dirs_match)

        if self.filter_flag != 1:
            files_match = [file for file in files if search(self.query, file)]
            conditionD = bool(files_match)
            if conditionD:
                self.genetate_report("files", files_match)
        if conditionC or conditionD:
            self.report = f"""----------------------------------
{root}
{self.report}
"""
            print(self.report)



    def begin(self):
        print('searching...\n')
        [self.scan_root_path(path) for path in self.root_paths]
        

#-----------------end of search class-----------------

def restart(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        input('Press any key to continue...')
        wrapper(*args, **kwargs)
    return wrapper


@restart
def main():
    search = Search()
    t = timeit(search.begin, number=1)
    print("Execution time:", t)


            
if __name__ == '__main__':
    print(('='*50) + '\nSIMPLE SEARCH\n')
    print(f'''Defaults: 
    default_root_paths  = {default_root_paths}
    default_path_filter = {default_path_filter}
    default_query       = {default_query}
    default_filter_flag = {default_filter_flag}
''')
    print('='*50)
    main()
