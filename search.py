import os
import sys
import re

def search():
    _debug_ = False

    if _debug_:
        d = 'D:\\My Documents'
        q = '([Kk]aox|[Bb]eat.?[Hh]oven|[Aa]cid.?[Ff]ish|[Kk].?[Ll]edge)'
        f = '-a'
    '''
    else:
        # py search.py 'C:\' '[Mm]usic.*(\.mp3)?$' -a
        args = sys.argv[1:] # ['C:\', '[Mm]usic.*(\.mp3)?$', '-a']
        d = args[0] # 'C:\'
        q = args[1] # '[Mm]usic.*(\.mp3)?$'
        f = ''
        if len(args) > 2:
            f = args[2] # '-a'
    '''

    ds = input('Start folders: ') or 'c:\\ , d:\\'
    ds = [d.strip() for d in ds.split(',')]
    dq = input('Only in folder (regex): ') or ''
    q  = input('Query (regex): ') or ''
    f  = input('Flag [-d, -a]: ') or '-a'

    # search files boolean
    sf = True
    # search dirs boolean
    sd  = False

    if f == '-d':
        sf = False
        sd  = True
    elif f == '-a':
        sd = True

    if q.startswith('^'):
        q_ = q[1:] 
    else:
        q_ = q # '[Mm]usic.*(\.mp3)?$'
    if q.endswith('$'):
        q_ = q_[:-1] # '[Mm]usic.*(\.mp3)?'

    for d in ds:
        for root, dirs, files in os.walk(d):
            flag = True
            # if q_ is not in str then this step will be skipped
            if re.search(q_, ''.join(dirs+files)) and re.search(dq, root):
                if sd:
                    for dir_ in dirs:
                        if re.search(q, dir_):
                            if flag:
                                print('>>>', root)
                                flag = False
                            print('\t DIR:', dir_)
                    print()
                if sf:
                    for file in files:
                        if re.search(q, file):
                            if flag:
                                print('-->', root)
                                flag = False
                            print('\t FILE:', file)
                    print()
                print('-' * 50)
            
def main():
    search()
    print('\nDone\n')
    try:
        main()
    except Exception as e:
        print(e)
        input('...')
        main()
    
            
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        input('...')
        main()