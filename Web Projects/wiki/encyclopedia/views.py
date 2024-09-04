import random

import markdown

from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_entry(request, entry):
    entry_content = util.get_entry(entry)

    # If the entry does not exist, handle the case (e.g., raise 404 or display an error)
    if entry_content is None:
        return render(request, "encyclopedia/page_not_found.html", {})

    entry_content = markdown.markdown(entry_content)

        # If entry exists, render it using the 'display_entry.html' template
    return render(request, "encyclopedia/display_entry.html", {
        "entry": entry_content,
        "title": entry  # Pass the title for use in the template
    })

def search(request):
    query = request.GET.get('q', '').strip()

    if query:
        all_entries = util.list_entries()

        # Check for exact match
        if query in all_entries:
            return redirect('display_entry', entry=query)

        # Find entries containing the query as a substring
        matching_entries = [entry for entry in all_entries if query.lower() in entry.lower()]

        if matching_entries.__len__() > 0:
            # Return a rendered template with matching entries
            return render(request, 'encyclopedia/index.html', {
                'entries': matching_entries,
                'query': query
            })

        return render(request, "encyclopedia/no_result.html", {})

    # If no query is provided, redirect to index
    return redirect('index')

class EntryForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, required=True)
    content = forms.CharField(label='Content', widget=forms.Textarea, required=False)

def create_entry(request):
    message = ""
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            if any(entry.lower() in title.lower() for entry in util.list_entries()):
                form.add_error(None, "This entry already exists.")
                return render(request, 'encyclopedia/create_entry.html', {
                    'form': form
                })

            util.save_entry(title, content)
            return redirect(reverse('display_entry', args=[title]))
    else:
        form = EntryForm()
    return render(request, 'encyclopedia/create_entry.html', {
        'form': form})


def edit_entry(request, title):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect('display_entry', title)
    else:
        current_content = util.get_entry(title)
        initial_content = current_content.split('\n\n', 1)[1] if '\n\n' in current_content else ''
        form = EntryForm(initial={'title': title, 'content': initial_content})
    return render(request, 'encyclopedia/edit_entry.html', {'form': form, 'title': title})


def random_entry(request):
    list = util.list_entries()
    random_entry = random.sample(list, 1)[0]
    return redirect(reverse('display_entry', args=[random_entry]))