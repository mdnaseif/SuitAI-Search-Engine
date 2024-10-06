


from scraping_data import AmazonScraper
from scraping_data import NoonScraper
from scraping_data import AnimeScraper
from scraping_data import PrimarkScraper

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QSizePolicy, QDesktopWidget
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

class DataScraperApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Data Scraper')

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        font = QFont()
        font.setPointSize(14)  

        self.type_label = QLabel('Select Data Type:')
        self.type_label.setFont(font)
        self.type_label.setFixedSize(550, 150)

        self.type_combobox = QComboBox()
        self.type_combobox.addItem('Amazon')
        self.type_combobox.addItem('Noon')
        self.type_combobox.addItem('Anime')
        self.type_combobox.addItem('Primark')


        self.type_combobox.setFont(font)
        self.type_combobox.setFixedSize(1100, 100)

        self.link_label = QLabel('Enter Link:')
        self.link_label.setFont(font)
        self.link_label.setFixedSize(400, 150)

        self.link_edit = QLineEdit()
        self.link_edit.setFont(font)
        self.link_edit.setFixedSize(1100, 100)

        self.start_button = QPushButton('Start Scraping')
        self.start_button.setFont(font)
        self.start_button.clicked.connect(self.start_scraping)
        self.start_button.setFixedSize(700, 150)

        # Adjusted layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.type_label, alignment=Qt.AlignLeft)
        layout.addWidget(self.type_combobox, alignment=Qt.AlignLeft)
        layout.addWidget(self.link_label, alignment=Qt.AlignLeft)
        layout.addWidget(self.link_edit, alignment=Qt.AlignLeft)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        screen_rect = QDesktopWidget().screenGeometry()

        x_center = (screen_rect.width() - self.width()) / 2
        y_center = (screen_rect.height() - self.height()) / 2

   
        self.setGeometry(int(x_center), int(y_center), self.width(), self.height())


    def start_scraping(self):
        data_type = self.type_combobox.currentText()
        link = self.link_edit.text()

        if data_type == 'Anime':
            scraper = AnimeScraper(csv_file_path=r'data_try\anime_data.csv', base_url=link)
            scraper.scrape_anime_data()  # Correct method name for AnimeScraper
        elif data_type == 'Amazon':
            scraper = AmazonScraper(csv_file_path=r'data_try\amazon_data.csv', url=link)
            scraper.scrape_amazon_data()
        elif data_type == 'Noon':
            scraper = NoonScraper(csv_file_path=r'data_try\noon_data_v3.csv', url=link)
            scraper.scrape_noon_data()
        elif data_type == 'Primark':
            scraper = PrimarkScraper(csv_file_path=r'data_try\primark_data.csv', url=link)
            scraper.scrape_primark_data()
        else:
            print('Invalid data type selected.')
            return

        print(f'Scraping completed for {data_type}.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataScraperApp()
    window.show()
    sys.exit(app.exec_())


































# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit
# from PyQt5.QtCore import Qt
# from selenium.common.exceptions import WebDriverException
# from scraping_from_amazon import AmazonScraper  # Assuming the AmazonScraper class is in a separate file named amazon_scraper.py
# from PyQt5.QtCore import QObject, pyqtSignal

# class AmazonScraperGUI(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.init_ui()

#     def init_ui(self):
#         self.setWindowTitle('Amazon Scraper GUI')

#         self.link_input = QLineEdit(self)
#         self.link_input.setPlaceholderText('Enter Amazon link...')
#         self.result_display = QTextEdit(self)
#         self.result_display.setReadOnly(True)

#         self.scrape_button = QPushButton('Scrape', self)
#         self.scrape_button.clicked.connect(self.start_scraping)

#         layout = QVBoxLayout(self)
#         layout.addWidget(self.link_input)
#         layout.addWidget(self.scrape_button)
#         layout.addWidget(self.result_display)

#         self.setGeometry(100, 100, 600, 400)
#         self.show()

#     def start_scraping(self):
#         amazon_link = self.link_input.text()
#         if amazon_link:
#             csv_file_path = "amazon_data.csv"
#             scraper = AmazonScraper(csv_file_path=csv_file_path, url=amazon_link)

#             # Redirect stdout to update the QTextEdit
#             emitting_stream = EmittingStream()
#             emitting_stream.text_written.connect(self.append_text)
#             sys.stdout = emitting_stream

#             try:
#                 scraper.scrape_amazon_data()
#                 self.append_text("Scraping completed successfully.")
#             except WebDriverException as e:
#                 self.append_text(f"WebDriverException: {str(e)}. Make sure your ChromeDriver is up-to-date.")
#             except Exception as e:
#                 self.append_text(f"Error during scraping: {str(e)}")

#             # Reset stdout to default
#             sys.stdout = sys.__stdout__


#     def append_text(self, text):
#         self.result_display.append(text)
#         self.result_display.verticalScrollBar().setValue(self.result_display.verticalScrollBar().maximum())


# class EmittingStream(QObject):
#     text_written = pyqtSignal(str)

#     def write(self, text):
#         self.text_written.emit(str(text))


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     gui = AmazonScraperGUI()
#     sys.exit(app.exec_())
