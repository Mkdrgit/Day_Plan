# 📅 Masaüstü Planlama ve Günlük Uygulaması

Modern, kullanıcı dostu ve işlevsel bir masaüstü planlama ve günlük tutma uygulaması. Günlük görevlerinizi organize edin, kişisel notlarınızı kaydedin ve geçmiş kayıtlarınıza kolayca erişin.

## ✨ Özellikler

### 📋 Görev Yönetimi
- Modern ve sezgisel takvim arayüzü
- Görev ekleme ve silme
- Görevleri tamamlandı olarak işaretleme (Buton görünümü ve işlevselliği aktif geliştirme altındadır)
- Görevler için başlık ve açıklama desteği
- Tarih bazlı görev organizasyonu

### 📝 Günlük Tutma
- Günlük notları oluşturma ve düzenleme
- Geçmiş günlük kayıtlarına erişim
- Tarih bazlı günlük organizasyonu
- Kolay silme ve düzenleme özellikleri

### 🎨 Arayüz
- Modern ve kullanıcı dostu tasarım
- Sezgisel navigasyon
- Temel CSS özellikleri ile stilize edilmiş (bazı gelişmiş CSS özellikleri Qt tarafından tam desteklenmeyebilir)
- Kolay erişilebilir menü yapısı

## 🛠️ Gereksinimler

- Python 3.13.3
- PyQt5
- SQLite3 (Python'un standart kütüphanesi ile birlikte gelir)

## 📥 Kurulum

1. Python 3.13.3'ü [Python'un resmi web sitesinden](https://www.python.org/downloads/) indirin ve yükleyin.
2. **Windows Kullanıcıları İçin Önemli Not:** `PyQt5` gibi bazı paketlerin kurulumu sırasında derleme işlemi gerekebilir. Bu işlem için sisteminizde **Microsoft C++ Build Tools**'un kurulu olması gerekmektedir. Visual Studio Installer aracılığıyla "C++ ile Masaüstü Geliştirme" iş yükünü ve ilgili derleme araçlarını (MSVC v142/v143 ve Windows SDK) yüklediğinizden emin olun. Kurulum detayları için [bu linki](https://visualstudio.microsoft.com/visual-cpp-build-tools/) ziyaret edebilirsiniz.
3. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

## 🚀 Kullanım

Uygulamayı başlatmak için iki yöntem vardır:

### 1. Terminal/Komut İstemcisi üzerinden:
```bash
python main.py
```

### 2. Windows'ta:
`Uygulamayi_Baslat.bat` dosyasına çift tıklayarak.

## 📱 Uygulama Kullanımı

### Takvim ve Görevler
1. Sol menüden "Takvim ve Görevler" seçeneğine tıklayın.
2. Takvimden istediğiniz tarihi seçin.
3. "+ Görev Ekle" butonu ile yeni görev ekleyin.
4. Görevlerinizi tamamlandı olarak işaretleyin (bu özellik şu anda geliştirilmektedir) veya silin.

### Günlük Notlar
1. Sol menüden "Günlük Notlar" seçeneğine tıklayın.
2. Seçili tarih için günlük notunuzu yazın.
3. "Kaydet" butonu ile notunuzu kaydedin.
4. "Geçmiş Kayıtlar" ile önceki notlarınıza erişin.

## 🔧 Bilinen Sorunlar ve Geliştirmeler
- **Görev Tamamlama Butonu:** Görev kartlarındaki "Tamamlandı" butonu şu anda düzgün görüntülenmeyebilir ve bu özelliğin kullanıcı arayüzü entegrasyonu aktif olarak geliştirilmektedir.
- **CSS Uyumluluğu:** Bazı modern CSS özellikleri (`transform`, `transition`, `box-shadow` gibi) Qt tarafından tam olarak desteklenmeyebilir ve bu durum terminalde "Unknown property" uyarılarına neden olabilir. Bu, genellikle uygulamanın temel işlevselliğini etkilemez ancak görsel sunumda küçük farklılıklar yaratabilir.

## 🔒 Veri Güvenliği ve Veritabanı

### planner.db
- Uygulamanın tüm verileri `planner.db` adlı SQLite veritabanı dosyasında saklanır.
- Bu dosya, görevlerinizi ve günlük notlarınızı kalıcı olarak depolar.
- Veritabanı dosyası otomatik olarak oluşturulur ve yönetilir.
- Veritabanı yapısı:
  - `events` tablosu: Görevlerin başlık, açıklama, tarih ve tamamlanma durumu.
  - `diary_entries` tablosu: Günlük notlarının tarih ve içerik bilgileri.

### Veri Güvenliği
- Tüm veriler yerel SQLite veritabanında güvenli bir şekilde saklanır.
- Veriler şifrelenmeden yerel olarak tutulur.
- Düzenli yedekleme önerilir.
- Veritabanı dosyasını (`planner.db`) düzenli olarak yedeklemeniz önerilir.

## 📄 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🤝 Katkıda Bulunma

1. Bu depoyu fork edin.
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`).
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: X'`).
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`).
5. Pull Request oluşturun.