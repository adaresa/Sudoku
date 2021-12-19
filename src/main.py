from menu import *

if __name__ == "__main__":
    theme = optionsValues("theme")
    lang = optionsValues("language")
    app = Menu(theme, lang)
    app.run()