import time

import pgpy
from django.shortcuts import render
from whoosh.index import open_dir
from whoosh.qparser import QueryParser




def index(request):
    start = time.time()
    result_list = []
    resnum = 0
    if request.method == "POST":
        key_word = request.POST.get("str", None)
        result_list = search(key_word)
        # skey, _ = pgpy.PGPKey.from_file("file_index/pgp")  # 私钥
        resnum = len(result_list)
    end = time.time()
    return render(request, "../templates/index.html",
                  {"data": result_list, "time": "%.3f" % (end - start), "resnum": resnum})


def search(key_word):
    result_list = []
    my_index = open_dir("file_index", indexname='list')
    with my_index.searcher() as searcher:
        parser1 = QueryParser("filename", my_index.schema)
        parser2 = QueryParser("file", my_index.schema)
        # parser = QueryParser("filepath", my_index.schema)
        my_query = parser1.parse(key_word) and parser2.parse(key_word)
        results = searcher.search(my_query, limit=None)
        count = 0
        # key, _ = pgpy.PGPKey.from_file("file_index/pgp.pub")  # 公钥
        for result_item in results:
            count = count + 1
            result_item = dict(result_item)
            result_item["num"] = count
            result_item["file"] = pgpy.PGPMessage.new(result_item["file"])
            result_item["filename"] = pgpy.PGPMessage.new(result_item["filename"])
            result_item["filepath"] = pgpy.PGPMessage.new(result_item["filepath"])
            result_list.append(result_item)
    return result_list
