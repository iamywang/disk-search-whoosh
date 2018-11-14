from django.shortcuts import render
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import time


def index(request):
    start = time.time()
    result_list = []
    resnum = 0
    if request.method == "POST":
        str = request.POST.get("str", None)
        print("被查询：" + str + "：--disk_search")
        result_list = search(str)
        resnum = len(result_list)
    end = time.time()
    return render(request, "../templates/index.html",
                  {"data": result_list, "time": "%.3f" % (end - start), "resnum": resnum})


def search(key_word):
    result_list = []
    my_index = open_dir("file_index", indexname='list')
    with my_index.searcher() as searcher:
        parser = QueryParser("filename", my_index.schema)
        # parser = QueryParser("filename", my_index.schema)
        # parser = QueryParser("filepath", my_index.schema)
        my_query = parser.parse(key_word)
        results = searcher.search(my_query, limit=None)
        count = 0
        for result_item in results:
            count = count + 1
            result_item = dict(result_item)
            result_item["num"] = count
            result_list.append(result_item)
    return result_list
