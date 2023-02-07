from django.shortcuts import render, redirect
from random import choice

from . import util
from markdown import markdown


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def get_title(request, TITLE):
    content = util.get_entry(TITLE)
    return render(request, "encyclopedia/title.html", {
        "content": markdown(content),
        "title": TITLE
    })

def search_results(request):
    entries = util.list_entries()
    query = request.GET.get('q')
    
    if query:
        results = list(filter(lambda x: query.capitalize() in x or query.upper() in x , entries))

    return render(request, 'encyclopedia/search_result.html', {'entries': results})
        
def create_entry(request):
    entries = util.list_entries()

    if request.method == "POST":
        new_entry_title = request.POST.get('title')
        new_entry_content = request.POST.get('content')

        if new_entry_title not in entries and new_entry_title != '':
            util.save_entry(new_entry_title, new_entry_content)
            
            return redirect("encyclopedia:index")

        else:
            error_message = f"The entry with <{new_entry_title}> already exists!>"
            return render(request, 'encyclopedia/create_entry.html', {'error_message': [error_message]})
            
    return render(request, 'encyclopedia/create_entry.html')

def edit_entry(request, title):
     content = util.get_entry(title)

     if request.method == "POST":
        edited_content = request.POST.get('edited_content')

        if edited_content != '':
            util.save_entry(title, edited_content)
            return redirect("encyclopedia:index")

        else:
            return render(request, 'encyclopedia/edit.html', {"content": edited_content, "title":title})
        
     return render(request, 'encyclopedia/edit.html', {"content": content, "title":title})

def random(request):
    entries = util.list_entries()
    random_title = choice(entries)

    content = util.get_entry(random_title)

    return render(request, 'encyclopedia/random.html', {"content": markdown(content), "title": random_title}) 

    