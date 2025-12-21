# <center>Kütüphane Ödevi(Yapım Aşamasında)</center>

## Yenilikler (21.12.25)
- Üye tarafında Hesap bilgisi ve işlem geçmişi eklendi!
- Admin tarafında ise sadece Hesap Bilgisi eklendi. Log tarafı yapmadan önce commit atmak istedim.
- Hesap bilgisinde üye bilgilerini değiştirebilir, şifresini değiştirebilir (Eski şifre soruyor ilk). Hesabını silebilir. Eğer iade edilmemiş kitap varsa hesap silinmiyor ve uyarı geliyor kitap iadesi için.
- İşlem geçmişinde kullanıcının önceden yaptığı işlemler loglar halinde kullanıcı gözükür. Kullanıcı hesabını silse bile verileri tabloda verilerde sorun yaşamadan hala tutulur.
- Artık frontend hashlenip backendte şifreleniyor.
- Postman de kullanıcı ve admin girişinde çerezlerde token gözükmeme sorunu çözüldü.


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

### İşlem Geçmişi Sayfası:
![işlem-geçmişi](Resimler/işlem%20geçmisi.png)
- Kullanıcı işlem geçmişi sayfasından önceden yapmış olduğu işlemleri (loglara) bakabilir. Loglar apayrı bi tabloda tutulur. Kullanıcı hesabını silse bile log tablosunda veri kaybı olmadan bilgiler kalır.

### Hesap Bilgisi Sayfası:
![hesap-bilgisi](Resimler/hesap%20bilgileri.png)
- Kullanıcı kendi hesap bilgilerini görebilir, kullanıcı ismini, emailini ve şifresini değiştirebilir. Ve hatta hesabı silebilir. Eğer hesapta iade edilmemiş kitap varsa önce iadesi istenir. Ceza sistemi entegre edince ceza varsa da izin vermeyecek. İsim değişikliğinde logdaki isim de otomatik değişir. Ve loga bilgi gider.

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

- Bi sonraki committe admin log sayfası, admin mail gönderme ve ceza sayfası yapılacaktır. Son commitlere yaklaştık sayılır.