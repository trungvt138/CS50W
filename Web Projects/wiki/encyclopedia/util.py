import re
import markdown
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from streamlit import markdown


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    message = ""
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    else:
        message = "The entry was successfully created."

    # Save the content to the file (overwrites if exists)
    file_content = ContentFile(f"# {title}\n\n{content}")
    default_storage.save(filename, file_content)
    return message

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        content = f.read().decode("utf-8")
        print(content)
        return content
    except FileNotFoundError:
        return None
