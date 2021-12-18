from menu import *
from settings import *

if __name__ == "__main__":
    lang = optionsValues("language")
    if lang != "ENG" and lang != "EST":
        optionsValues("language", new_value="ENG")
        lang = optionsValues("language")
    app = Menu(lang)
    app.run()