import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Browserly")
        self.setGeometry(100, 100, 800, 600)
        
        icon = QIcon("C:/Users/ethan/Desktop/RELGO/Apps/Browserly-raw/icon.ico")
        self.setWindowIcon(icon)


        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.setCurrentIndex(0)
        self.setCentralWidget(self.tab_widget)

        self.create_new_tab()
        self.create_toolbar()


    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        new_tab_action = QAction("🆕", self)
        new_tab_action.triggered.connect(self.create_new_tab)
        toolbar.addAction(new_tab_action)

        back_action = QAction("⬅️", self)
        back_action.triggered.connect(self.current_webview().back)
        toolbar.addAction(back_action)

        forward_action = QAction("➡️", self)
        forward_action.triggered.connect(self.current_webview().forward)
        toolbar.addAction(forward_action)

        home_action = QAction("🏠", self)
        home_action.triggered.connect(self.go_to_home)
        toolbar.addAction(home_action)

        zoom_in_action = QAction("➕", self)
        zoom_in_action.triggered.connect(self.zoom_in)
        toolbar.addAction(zoom_in_action)

        zoom_out_action = QAction("➖", self)
        zoom_out_action.triggered.connect(self.zoom_out)
        toolbar.addAction(zoom_out_action)

        reload_action = QAction("🔄", self)
        reload_action.triggered.connect(self.reload_page)
        toolbar.addAction(reload_action)

        self.url_entry = QLineEdit()
        self.url_entry.returnPressed.connect(self.load_url)
        toolbar.addWidget(self.url_entry)

    def create_new_tab(self):
        webview = QWebEngineView()
        webview.loadFinished.connect(self.update_url_entry)
        webview.titleChanged.connect(self.update_tab_text)
        self.tab_widget.addTab(webview, "New Tab")
        self.tab_widget.setCurrentWidget(webview)
        webview.load(QUrl("http://www.google.com/"))

    def close_tab(self, index):
        self.tab_widget.removeTab(index)

    def current_webview(self):
        return self.tab_widget.currentWidget()

    def load_url(self):           
        input_text = self.url_entry.text().strip()
        
        if input_text == "mc":
            url = QUrl("https://minecraft.com")
            self.current_webview().load(url)
        elif input_text.startswith("http://") or input_text.startswith("https://"):
            url = QUrl(input_text)
        else:
            search_query = input_text.replace(" ", "+")
            url = QUrl(f"http://www.google.com/search?q={search_query}")

        self.current_webview().load(url)

    def go_to_home(self):
        self.current_webview().load(QUrl("http://www.google.com/"))

    def update_url_entry(self):
        self.url_entry.setText(self.current_webview().url().toString())

    def update_tab_text(self, title):
        current_index = self.tab_widget.currentIndex()
        self.tab_widget.setTabText(current_index, title)

    def zoom_in(self):
        self.current_webview().setZoomFactor(self.current_webview().zoomFactor() + 0.1)

    def zoom_out(self):
        self.current_webview().setZoomFactor(self.current_webview().zoomFactor() - 0.1)

    def reload_page(self):
        self.current_webview().reload()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()

    sys.exit(app.exec_())
    
