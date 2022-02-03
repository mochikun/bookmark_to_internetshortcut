import pprint
import json
import glob
import os
import re


def remove_invalid_char(str):
    return re.sub(r'^ |[\\/:*?"<>|]+','',str)

def recur_bookmarks(children, cdir):
    #pprint.pprint(children)
    for child in children:
        #pprint.pprint(child)
        #pprint.pprint(type(child))
        if child['type'] == 'folder':
            ndir = cdir + '/' + remove_invalid_char(child['name'])
            os.makedirs(ndir, exist_ok=True)
            recur_bookmarks(child['children'], ndir)
        elif child['type'] == 'url':
            name = cdir + '/' + remove_invalid_char(child['name'])
            f = open(name[:150] + '.url', 'w')
            f.write('[InternetShortcut]\nIDList=\nURL='+child['url'])


bookmark_f = os.path.expanduser('~') + "/AppData/Local/Vivaldi/User Data/Default/Bookmarks"
cdir = './' + os.path.splitext(os.path.basename(bookmark_f))[0]
with open(bookmark_f, 'r', encoding="utf-8_sig") as f:
    os.makedirs(cdir, exist_ok=True)
    bookmarks = json.load(f)
    for bookmark in bookmarks['roots']:
        bdir = cdir + '/' + remove_invalid_char(bookmarks['roots'][bookmark]['name'])
        os.makedirs(bdir, exist_ok=True)
        recur_bookmarks(bookmarks['roots'][bookmark]['children'], bdir)

