import sys  
from PyQt5.QtWidgets import (  
    QApplication,  
    QMainWindow,  
    QWidget,  
    QVBoxLayout, QHBoxLayout,  
    QCalendarWidget,  
    QTextEdit,  
    QPushButton,  
    QTabWidget,  
    QDialog,  
    QLabel,  
    QLineEdit,  
    QMessageBox,  
    QListWidget,  
    QStackedWidget,  
    QSizePolicy,  
    QComboBox,  
    QSpinBox,  
    QTimeEdit,  
    QCheckBox,  
    QScrollArea,  
    QFrame,  
    QSplitter,  
    QMenu,  
    QAction,  
    QSystemTrayIcon,  
    QStyle, 
    QToolButton  
)
from PyQt5.QtCore import Qt, QDate, QTimer, QDateTime, QSize  
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QPixmap, QImage  
from database import Database  
from datetime import datetime  

# Modern ikonlar için unicode karakterler
IKON_TAKVIM = "��"  # Takvim simgesi, sol menüde kullanılır.
IKON_GUNLUK = "📝"  # Günlük simgesi, sol menüde kullanılır.
IKON_TAKVIM_PATH = "icon_calendar.png"  # Takvim için PNG/SVG ikon yolu
IKON_GUNLUK_PATH = "icon_note.png"  # Günlük için PNG/SVG ikon yolu

class GorevKarti(QWidget):  # Her bir görev için kart/kutu widget'ı.
    def __init__(self, gorev_id, baslik, aciklama, yapildi_mi, yapildi_callback, sil_callback):
        super().__init__()  
        self.gorev_id = gorev_id  
        self.yapildi_callback = yapildi_callback  
        self.sil_callback = sil_callback  
        duzen = QHBoxLayout(self)  
        duzen.setContentsMargins(10, 6, 10, 6)  
        duzen.setSpacing(10)  
        self.setStyleSheet("""
            background: #fff;
            border-radius: 10px;
            margin-bottom: 7px;
            box-shadow: 0 1px 6px rgba(44,62,80,0.06);
        """)  # Kartın arka planı ve gölgesi.
        self.etiket = QLabel(f"{baslik}: {aciklama}") 
        self.etiket.setFont(QFont("Segoe UI", 10))  
        self.etiket.setStyleSheet(f"color: {'#bbb' if yapildi_mi else '#23272e'};")  
        duzen.addWidget(self.etiket)  
        self.yapildi_buton = QPushButton("✔")  # Görev tamamlandı butonu
        self.yapildi_buton.setEnabled(not yapildi_mi)  # Tamamlanan görevde buton devre dışı.
        self.yapildi_buton.setCursor(Qt.PointingHandCursor)  # El imleci.
        self.yapildi_buton.setStyleSheet("""
            QPushButton {
                background: #43e97b;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 4px 10px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:disabled {
                background: #bbb;
                color: #fff;
            }
            QPushButton:hover:!disabled {
                background: #38f9d7;
            }
        """)
        self.yapildi_buton.clicked.connect(self.yapildi_yap)  # Tıklanınca görev tamamlandı fonksiyonu çağrılır.
        duzen.addWidget(self.yapildi_buton)  # Butonu karta ekle.
        self.sil_buton = QPushButton("✖")  
        self.sil_buton.setCursor(Qt.PointingHandCursor) 
        self.sil_buton.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 4px 10px;
                font-weight: bold;
                font-size: 11pt;
                margin-left: 5px;
            }
            QPushButton:hover {
                background: #c0392b;
                color: #fff;
            }
        """)  # Sil butonunun görünümü.
        self.sil_buton.clicked.connect(self.sil_gorev)  
        duzen.addWidget(self.sil_buton)  
        self.setLayout(duzen)  
    def yapildi_yap(self):
        self.yapildi_callback(self.gorev_id) 
        self.yapildi_buton.setEnabled(False)  
        self.etiket.setStyleSheet("color: #bbb;")  
    def sil_gorev(self):
        self.sil_callback(self.gorev_id)  

class EkleEventDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Görev Ekle")
        self.setModal(True)
        self.setFixedWidth(340)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 18, 24, 18)
        layout.setSpacing(12)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Başlık (zorunlu)")
        self.title_input.setFont(QFont("Segoe UI", 10))
        self.title_input.setStyleSheet("padding: 7px; border-radius: 7px; border: 1px solid #e1e1e1;")
        layout.addWidget(self.title_input)
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Açıklama (isteğe bağlı)")
        self.desc_input.setFont(QFont("Segoe UI", 10))
        self.desc_input.setStyleSheet("padding: 7px; border-radius: 7px; border: 1px solid #e1e1e1;")
        layout.addWidget(self.desc_input)
        btn = QPushButton("Ekle")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: #43e97b;
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 7px 18px;
                font-size: 10pt;
                font-weight: bold;
                margin-top: 4px;
            }
            QPushButton:hover {
                background: #38f9d7;
                color: #23272e;
            }
        """)
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)
    def get_data(self):
        return self.title_input.text().strip(), self.desc_input.toPlainText().strip()

class PlannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setWindowTitle("Planlayıcı")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("font-family: 'Segoe UI', Arial, sans-serif; background: #f5f6fa;")
        # Ana layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Sol menü (sidebar)
        sidebar = QWidget()
        sidebar.setFixedWidth(70)
        sidebar.setStyleSheet("background: #23272e; border-top-right-radius: 14px; border-bottom-right-radius: 14px;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 30, 0, 30)
        sidebar_layout.setSpacing(18)
        # Menü butonları
        self.btn_calendar = QPushButton()
        self.btn_calendar.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.btn_calendar.setIconSize(QSize(32, 32))  # İkon boyutu
        self.btn_calendar.setFixedSize(48, 48)  # Buton boyutu
        self.btn_calendar.setToolTip("Takvim Görünümü")
        self.btn_calendar.setCheckable(True)
        self.btn_calendar.setChecked(True)
        self.btn_calendar.setStyleSheet(self.sidebar_btn_style(True))
        self.btn_calendar.clicked.connect(lambda: self.switch_page(0))
        sidebar_layout.addWidget(self.btn_calendar)
        self.btn_diary = QPushButton("📝")  # Günlük butonu, emoji ile
        self.btn_diary.setIconSize(QSize(32, 32))  # İkon boyutu
        self.btn_diary.setToolTip("Günlük")
        self.btn_diary.setCheckable(True)
        self.btn_diary.setStyleSheet(self.sidebar_btn_style(False))
        self.btn_diary.clicked.connect(lambda: self.switch_page(1))
        sidebar_layout.addWidget(self.btn_diary)
        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)
        # Orta alan (üst başlık + içerik)
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        # Üst başlık
        header = QWidget()
        header.setFixedHeight(54)
        header.setStyleSheet("background: #fff; border-bottom: 1px solid #e1e1e1;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        header_layout.setSpacing(0)
        self.lbl_title = QLabel("Planlayıcı")
        self.lbl_title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        self.lbl_title.setStyleSheet("color: #23272e;")
        header_layout.addWidget(self.lbl_title)
        header_layout.addStretch()
        self.lbl_date = QLabel(datetime.now().strftime("%d %B %Y"))
        self.lbl_date.setFont(QFont("Segoe UI", 10))
        self.lbl_date.setStyleSheet("color: #888;")
        header_layout.addWidget(self.lbl_date)
        center_layout.addWidget(header)
        # İçerik alanı (takvim/günlük)
        self.pages = QStackedWidget()
        # Takvim sayfası
        calendar_page = QWidget()
        cal_layout = QHBoxLayout(calendar_page)
        cal_layout.setContentsMargins(18, 18, 18, 18)
        cal_layout.setSpacing(18)
        # Takvim
        self.calendar = QCalendarWidget()
        self.calendar.setFixedWidth(320)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)  # Hafta numaralarını gizle
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background: #fff;
                color: #23272e;
                border-radius: 12px;
                font-size: 10pt;
                padding: 8px;
                border: 1px solid #e1e1e1;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background: #f5f6fa;
                border-radius: 12px 12px 0 0;
            }
            QCalendarWidget QToolButton {
                color: #23272e;
                background: #f5f6fa;
                border: none;
                font-size: 11pt;
                font-weight: bold;
                padding: 4px 10px;
                border-radius: 6px;
            }
            QCalendarWidget QToolButton:hover {
                background: #43e97b;
                color: #fff;
            }
            QCalendarWidget QSpinBox {
                color: #23272e;
                background: #f5f6fa;
                border: none;
                border-radius: 6px;
                font-size: 10pt;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: #43e97b;
                background: #fff;
            }
        """)
        self.calendar.clicked.connect(self.date_selected)
        cal_layout.addWidget(self.calendar)
        # Görevler alanı
        self.event_list = QWidget()
        self.event_list_layout = QVBoxLayout(self.event_list)
        self.event_list_layout.setAlignment(Qt.AlignTop)
        self.event_list.setStyleSheet("background: transparent;")
        cal_layout.addWidget(self.event_list)
        # Etkinlik ekle butonu
        add_event_button = QPushButton("+ Görev Ekle")
        add_event_button.setCursor(Qt.PointingHandCursor)
        add_event_button.clicked.connect(self.add_event)
        add_event_button.setStyleSheet("""
            QPushButton {
                background: #43e97b;
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 7px 18px;
                font-size: 10pt;
                font-weight: bold;
                margin-top: 4px;
            }
            QPushButton:hover {
                background: #38f9d7;
                color: #23272e;
            }
        """)
        cal_layout.addWidget(add_event_button)
        self.pages.addWidget(calendar_page)
        # Günlük sayfası
        diary_page = QWidget()
        diary_layout = QVBoxLayout(diary_page)
        diary_layout.setContentsMargins(32, 16, 32, 16)
        diary_layout.setSpacing(14)
        # Günlük metin alanı
        self.diary_text = QTextEdit()
        self.diary_text.setFont(QFont("Segoe UI", 10))
        self.diary_text.setStyleSheet("""
            QTextEdit {
                background: #fff;
                color: #23272e;
                border-radius: 10px;
                padding: 12px;
                font-size: 10pt;
                border: 1px solid #e1e1e1;
                box-shadow: 0 1px 6px rgba(44,62,80,0.06);
            }
        """)
        diary_layout.addWidget(self.diary_text)
        # Kaydet butonu
        save_button = QPushButton("Kaydet")
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.clicked.connect(self.save_diary)
        save_button.setStyleSheet("""
            QPushButton {
                background: #43e97b;
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 7px 18px;
                font-size: 10pt;
                font-weight: bold;
                margin-top: 4px;
            }
            QPushButton:hover {
                background: #38f9d7;
                color: #23272e;
            }
        """)
        diary_layout.addWidget(save_button)
        # Günlük sil butonu
        delete_diary_button = QPushButton("Günlüğü Sil ✖")
        delete_diary_button.setCursor(Qt.PointingHandCursor)
        delete_diary_button.clicked.connect(self.delete_diary)
        delete_diary_button.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 7px 18px;
                font-size: 10pt;
                font-weight: bold;
                margin-top: 4px;
            }
            QPushButton:hover {
                background: #c0392b;
                color: #fff;
            }
        """)
        diary_layout.addWidget(delete_diary_button)
        # Geçmiş kayıtlar butonu
        history_button = QPushButton("Geçmiş Kayıtlar")
        history_button.setCursor(Qt.PointingHandCursor)
        history_button.clicked.connect(self.show_history)
        history_button.setStyleSheet("""
            QPushButton {
                background: #23272e;
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 7px 18px;
                font-size: 10pt;
                font-weight: bold;
                margin-top: 4px;
            }
            QPushButton:hover {
                background: #38f9d7;
                color: #23272e;
            }
        """)
        diary_layout.addWidget(history_button)
        self.pages.addWidget(diary_page)
        center_layout.addWidget(self.pages)
        main_layout.addWidget(center_widget)
        # İlk tarih seçimini yap
        self.date_selected(self.calendar.selectedDate())
        self.switch_page(0)
    def sidebar_btn_style(self, checked):
        if checked:
            return """
                QPushButton {
                    background: #43e97b;
                    color: #23272e;
                    border: none;
                    border-radius: 16px;
                    font-size: 22pt;
                    font-weight: bold;
                    padding: 18px 0;
                    margin: 0 12px;
                }
            """
        else:
            return """
                QPushButton {
                    background: transparent;
                    color: #fff;
                    border: none;
                    border-radius: 16px;
                    font-size: 22pt;
                    font-weight: bold;
                    padding: 18px 0;
                    margin: 0 12px;
                }
                QPushButton:hover {
                    background: #23272e;
                    color: #43e97b;
                }
            """
    def switch_page(self, idx):
        self.pages.setCurrentIndex(idx)
        self.btn_calendar.setChecked(idx == 0)
        self.btn_diary.setChecked(idx == 1)
        self.btn_calendar.setStyleSheet(self.sidebar_btn_style(idx == 0))
        self.btn_diary.setStyleSheet(self.sidebar_btn_style(idx == 1))
        if idx == 0:
            self.lbl_title.setText("Takvim ve Görevler")
        else:
            self.lbl_title.setText("Günlük Notlar")
    def date_selected(self, date):
        # Etkinlikleri listele
        for i in reversed(range(self.event_list_layout.count())):
            widget = self.event_list_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        events = self.db.get_events(date.toString('yyyy-MM-dd'))
        for event_id, title, desc, is_done in events:
            item = GorevKarti(event_id, title, desc, is_done, self.mark_event_done, self.delete_event)
            self.event_list_layout.addWidget(item)
        # Günlük kaydını yükle
        diary_entry = self.db.get_diary_entry(date.toString('yyyy-MM-dd'))
        self.diary_text.setText(diary_entry if diary_entry else "")
    def mark_event_done(self, event_id):
        self.db.mark_event_done(event_id)
        self.date_selected(self.calendar.selectedDate())
    def delete_event(self, event_id):
        self.db.delete_event(event_id)
        self.date_selected(self.calendar.selectedDate())
    def save_diary(self):
        content = self.diary_text.toPlainText()
        date = self.calendar.selectedDate().toString('yyyy-MM-dd')
        self.db.add_diary_entry(date, content)
        QMessageBox.information(self, "Başarılı", "Günlük kaydı kaydedildi!")
    def delete_diary(self):
        date = self.calendar.selectedDate().toString('yyyy-MM-dd')
        self.db.delete_diary_entry(date)
        self.diary_text.clear()
        QMessageBox.information(self, "Silindi", "Günlük kaydı silindi!")
    def show_history(self):
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle("Geçmiş Kayıtlar")
        history_dialog.setModal(True)
        layout = QVBoxLayout(history_dialog)
        history_list = QListWidget()
        entries = self.db.get_all_diary_entries()
        for date, content in entries:
            history_list.addItem(f"{date}: {content[:50]}...")
        layout.addWidget(history_list)
        history_dialog.setStyleSheet("""
            QDialog {
                background: #fff;
                color: #23272e;
                border-radius: 14px;
            }
            QListWidget {
                background: #f5f6fa;
                color: #23272e;
                border: none;
                border-radius: 10px;
                font-size: 12pt;
            }
        """)
        history_dialog.exec_()
    def add_event(self):
        dialog = EkleEventDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            title, description = dialog.get_data()
            if not title:
                QMessageBox.warning(self, "Hata", "Başlık boş olamaz!")
                return
            self.db.add_event(
                self.calendar.selectedDate().toString('yyyy-MM-dd'),
                title,
                description
            )
            self.date_selected(self.calendar.selectedDate())
            QMessageBox.information(self, "Başarılı", "Görev eklendi!")

if __name__ == '__main__':
    app = QApplication(sys.argv)  # PyQt5 uygulamasını başlat
    pencere = PlannerApp()  # Ana pencereyi oluştur
    pencere.show()  # Pencereyi göster
    sys.exit(app.exec_())  # Uygulama döngüsünü başlat
