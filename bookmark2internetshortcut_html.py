import pprint
import bookmarks_parser
import glob
import os
import re

def remove_invalid_char(str):
    return re.sub(r'^ |[\\/:*?"<>|]+','',str)

def recur_bookmarks(children, cdir):
    for child in children:
        pprint.pprint("1"+child)
        if 'type' in child:
            if child['type'] == 'bookmark':
                name = cdir + '/' + remove_invalid_char(child['title'])
                f = open(name[:150] + '.url', 'w')
                f.write('[InternetShortcut]\nIDList=\nURL='+child['url'])
        if 'children' in child:
            if 'ns_root' in child:
                if child['ns_root'] == 'menu':
                    ndir = cdir + '/' + remove_invalid_char(child['title'])
                    os.makedirs(ndir, exist_ok=True)
            if 'type' in child:
                if child['type'] == 'folder':
                    ndir = cdir + '/' + remove_invalid_char(child['title'])
                    os.makedirs(ndir, exist_ok=True)
            pprint.pprint("2"+child)
            recur_bookmarks(child['children'], ndir)

files = glob.glob("./*.html")
for file in files:
    cdir = './' + os.path.splitext(os.path.basename(file))[0]
    os.makedirs(cdir, exist_ok=True)
    bookmarks = bookmarks_parser.parse(file)
    recur_bookmarks(bookmarks, cdir)

