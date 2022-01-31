from menu import *

if __name__ == "__main__":
    app = Menu(optionsValues("theme"), optionsValues("language"))
    app.run()