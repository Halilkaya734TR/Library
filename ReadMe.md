# <center>Kütüphane Ödevi(Yapım Aşamasında)</center>

## Yenilikler (15.12.25) (Büyük Güncelleme)
- Yeni bi tasarıma geçildi. Sol tarafta panel sağ tarafta sayfa gözükecek bi tasarım yaptım.
- Üye tarafında ana sayfa, kitaplar da ödünç alma işlevi kitaplarım adında kullanıma hazır bi yer yapıldı. Ödünç alınan kitapları detaylarını ve iade edebiliyorsunuz.
- Admin tarafında epey yenilikler var. Ana sayfa, kitap, kategori, yazar ve yayınevi işlemleri yapıldı. Kitap, kategori, yazar ve yayınevleri eklenebilir, düzenlenebilir ve silinebilir. Tabi silinmeden önce ödünç alınmışsa silmiyor.


## İçindekiler
- [Sayfa Görünümü](#sayfa-görünümü)  
- [ER Diyagramı](#er-diyagramı)  

## Sayfa Görünümü
- **NOT:** En son hali değildir. Proje bitene kadar değişiklikler olabilir. Bunlar şuanki yaptıklarım ve üstüne koyup ya da değiştirip daha iyisini yapacaklarımdır.

### Giriş Üye Sayfası:
![login-üye](Resimler/login%20üye.png)
- Kutucukların içine veri yazılıp butona basınca üye panel yönlendiriyor. Artık bilgiler doğruysa üye panel geçiş sağlar. Değilse geçiş olmaz.

### Giriş Admin Sayfası:
![login-admin](Resimler/login%20admin.png)
- Üye ile aynı işlevlere sahip. Doğruysa admin panele ulaşırsınız.

### Giriş Kayıt Ol Sayfası:
![login-kayıt-ol](Resimler/login%20kayıt.png)
- Kayıt olmak için olan sayfadır. Aynı login.html içindedir. Aynı mail varsa kaydetmez! Yoksa kaydeder ve üyeden giriş yapabilirsiniz!

### Üye Panel Sayfası:
![üye-panel](Resimler/üye%20panel.png)
- Üyenin işlemlerini yapacağı paneldir. Şuanlık 5 buton var. Şuanlık sadece Kitaplar ve Çıkış butonu çalışmaktadır.

### Kitaplar Sayfası:
![kitaplar](Resimler/kitaplar.png)
- Database kitapları gösterir. Sayfada en fazla 10 tane kitap gösterir. Önceki ve Sonraki butonlarıyla diğerlerine ulaşılabilir. Arama yerinde arama yapılabilir. En fazla bi üye 3 tane kitap ödünç alabilir. Fazlasına izin vermez! Ödünç alındığında stoktan kitap miktarı düşer. Stok sayısı 0 olan kitaplar gözükmez!

### Kitaplarım Sayfası:
![kitaplarım](Resimler/kitaplarım.png)
- Ödünç alınan kitapları gösterir. Kitaplar hakkında bilgileri görebilir ve iade edebilirsiniz. İade edildiğinde stokta kitap sayısı artar.

### Admin Panel Sayfası:
![admin-panel](Resimler/admin%20panel.png)
- Admin işlemlerini yaptığı paneldir. Butonlar sonradan ekleme ya da düzenleme yapılabilir. Bunda da şuanlık sadece çıkış butonu çalışmaktadır.

### Admin Kitap İşlemleri Sayfası:
![admin-kitapİşlemleri](Resimler/kitap%20işlemler.png)
- Kütüphane kitaplarını gösterir. Kitaplarda arama, ekleme, düzenleme ve silme yapılabilir. Eğer bi kitap bir üyeye ödünç verilmişse o kitap iade edilene kadar kitap silinemez!

### Admin Kitap İşlemleri Kitap Ekle:
![admin-kitapİşlemleri-kitapekle](Resimler/kitap%20işlemler%20ekle.png)
- Kitap ekleme arayüzü.

### Admin Kitap İşlemleri Kitap Düzenleme:
![admin-kitapİşlemleri-kitapdüzenle](Resimler/kitap%20işlemler%20düzenle.png)
- Kitap düzenleme arayüzü. Checkbox seçilen sadece 1 kitaba düzenleme yapar. Kitaba ait bilgiler hazır gelir

### Admin Yazar İşlemleri Sayfası:
![admin-yazarİşlemleri](Resimler/yazar.png)
- Yazarları gösterir. Yazar arama, ekleme, düzenleme ve silme yapılır. Eğer yazarın bi kitabı varsa o kitap silinmeden silinemez!

### Admin Yazar İşlemleri Yazar Ekle:
![admin-yazarişlemleri-yazarekle](Resimler/yazar%20ekle.png)
- Yazar ekleme arayüzü.

### Admin Yazar İşlemleri Yazar Düzenleme:
![admin-yazarİşlemleri-yazardüzenle](Resimler/yazar%20düzenle.png)
- Yazar düzenleme arayüzü. Checkbox seçilen sadece 1 yazar düzenleme yapar. Yazar adı hazır gelir.

### Admin Kategori İşlemleri Sayfası:
![admin-kategoriİşlemleri](Resimler/kategori.png)
- Kategorileri gösterir. Kategori arama, ekleme, düzenleme ve silme yapılabilir. Eğer o kategoriye ait kitap varsa silinemez!

### Admin Kategori İşlemleri Kategori Ekle:
![admin-kategoriİşlemleri-kategoriekle](Resimler/kategori%20ekle.png)
- Kategori ekleme arayüzü.

### Admin Kategori İşlemleri Kategori Düzenleme:
![admin-kategoriİşlemleri-kategoridüzenle](Resimler/kategori%20düzenle.png)
- Kategori düzenleme arayüzü. Checbox seçilen sadece 1 kategori düzenleme yapar. Kategori adı hazır gelir.

### Admin Yayınevi İşlemleri Sayfası:
![admin-yayıneviİşlemleri](Resimler/yayınevi.png)
- Yayınevleri gösterir. Yayınevi arama, ekleme, düzenleme ve silme yapılabilir. Eğer o yayınevi ait kitap varsa silinemez!

### Admin Yayınevi İşlemleri Yayınevi Ekle:
![admin-yayıneviİşlemleri-yayıneviekle](Resimler/yayınevi%20ekle.png)
- Yayınevi ekleme arayüzü.

### Admin Yayınevi İşlemleri Yayınevi Düzenleme:
![admin-yayıneviİşlemleri-yayınevidüzenle](Resimler/yayınevi%20düzenle.png)
- Yayınevi düzenleme arayüzü. Checbox seçilen sadece 1 yayınevi düzenleme yapar. Yayınevi adı hazır gelir.

## ER Diyagramı
![ER-Diyagramı](Resimler/ER%20ilişkisi.png)
- Daha iyi bir ER diyagramı. Yeni şeyler eklendikçe daha da güzel ve düzenli olacaktır.

## Kapanış

- Üye sayfasına üye bilgilerini değiştirme, üye işlem geçmişi, admin sayfasına ise admin bilgileri değiştirme, genel log, mail gönderme eklemeyi düşünüyorum. Ama bugün değil. Bi sonraki commit dediklerimi bir çoğunu yapmış olurum.