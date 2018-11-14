import os, time

import docx
from jieba.analyse import ChineseAnalyzer
from whoosh.fields import *
from whoosh.index import create_in


def buildIndex():
    start = time.time()
    analyser = ChineseAnalyzer()
    schema = Schema(file=TEXT(stored=True, analyzer=analyser), filename=TEXT(stored=True, analyzer=analyser),
                    filepath=TEXT(stored=True, analyzer=analyser))
    ix = create_in("file_index", schema=schema, indexname='list')
    writer = ix.writer()
    c = 0
    for fn in traverseFile("/run/media/y_wang/"):
        c += 1
        ext = os.path.splitext(fn)
        res = ""
        if ext[1] == ".docx":
            res = readDocx(fn)
            writer.add_document(file=res, filename=os.path.basename(fn), filepath=fn)
        elif ext[1] == ".txt" or ext[1] == ".py" or ext[1] == ".java" or ext[1] == ".c" or ext[1] == ".cpp" or ext[
            1] == ".h" or ext[1] == ".go" or ext[1] == ".yml" or ext[1] == ".md":
            res = readFile(fn)
            writer.add_document(file=res, filename=os.path.basename(fn), filepath=fn)
        else:
            res = "不支持文件扩展名"
            writer.add_document(file=res, filename=os.path.basename(fn), filepath=fn)
    writer.commit()
    end = time.time()
    print("Finished: " + str(c) + " files added")
    print("Time:" + "%.3f" % (end - start) + "s")


def traverseFile(root):
    flist = []
    for f in os.listdir(root):
        f_path = os.path.join(root, f)
        if os.path.isfile(f_path):
            flist.append(f_path)
        else:
            flist += traverseFile(f_path)
    return flist


def readDocx(fn):
    file = docx.Document(fn)
    str = ""
    for para in file.paragraphs:
        str += para.text + "\n"
    return str


def readFile(fn):
    with open(fn, 'rb') as f:
        lines = 0
        str = ""
        while True:
            line1 = f.readline().decode("utf-8", "ignore")
            if line1:
                str += line1 + "\n"
                lines += 1
            else:
                break
    return str


if __name__ == '__main__':
    buildIndex()
