from django.shortcuts import render, redirect
from django.http import HttpResponse
from markdown2 import markdown
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def pages(request, title):
    page = util.get_entry(title.strip())
    if page == None:
        page = "# Page not found"
    page = markdown(page)
    return render(request, "encyclopedia/pages.html", {
        "content": page,
        "title": title
    })


def search(request):
    query = request.GET.get('q').strip()
    if query in util.list_entries():
        return redirect("pages", title=query)
    else:
        return render(request, "encyclopedia/search.html", {"entries": util.search(query), "q": query})


def new(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title == "" or content == "":
            return render(request, "encyclopedia/new.html", {
                "message": "Can't save empty fields",
                "title": title,
                "content": content
            })
        if title in util.list_entries():
            return render(request, "encyclopedia/new.html", {
                "message": "Already Exsists",
                "title": title,
                "content": content
            })
        util.save_entry(title, content)
    return render(request, "encyclopedia/new.html")


def edit(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        return render(request, "encyclopedi/edit.html", {
            "error": "404 Page not found"
        })

    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedi/edit.html", {
                "message": "Cant save empty file ",
                "title": title,
                "content": content
            })
        util.save_entry(title, content)
        return redirect("pages", title=title)
    return render(request, "encyclopedia/edit.html", {'content': content, 'title': title})


def RandomPage(request):
    allPages = util.list_entries()
    randomPages = allPages[random.randint(0, len(allPages)-1)]
    return redirect("pages", title=randomPages)
