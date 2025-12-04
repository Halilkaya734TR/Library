# <center>Kütüphane Ödevi(Yapım Aşamasında)</center>

## Yenilikler (04.12.25)
- Yenilik olarak şuanlık sadece JWT entegre edildi. Artık token üretip bunu çerezler de tutuyor.


## İçindekiler
- [Sayfa Görünümü](#sayfa-görünümü)  
- [ER Diyagramı](#er-diyagramı)  

## Sayfa Görünümü
- **NOT:** En son hali değildir. Proje bitene kadar değişiklikler olabilir. Bunlar şuanki yaptıklarım ve üstüne koyup ya da değiştirip daha iyisini yapacaklarımdır.
### Giriş Üye Sayfası:

![login-üye](Resimler/login%20üye.png)
- Kutucukların içine veri yazılıp butona basınca üye panel yönlendiriyor. Artık bilgiler doğruysa üye panel geçiş sağlar. Değilse geçiş olmaz.

### Giriş Admin Sayfası
![login-admin](Resimler/login%20admin.png)
- Üye ile aynı işlevlere sahip. Doğruysa admin panele ulaşırsınız.

### Giriş Kayıt Ol Sayfası
![login-kayıt-ol](Resimler/login%20kayıt.png)
- Kayıt olmak için olan sayfadır. Aynı login.html içindedir. Aynı mail varsa kaydetmez! Yoksa kaydeder ve üyeden giriş yapabilirsiniz!

### Üye Panel Sayfası
![üye-panel](Resimler/üye%20panel.png)
- Üyenin işlemlerini yapacağı paneldir. Şuanlık 5 buton var. Şuanlık sadece Kitap Ara ve Çıkış butonu çalışmaktadır.

### Kitaplar Sayfası
![kitaplar](Resimler/kitaplar.png)
- Database kitapları gösterir. Ger. dön butonları çalışır. İlerde eklemeler yapılacaktır.

### Admin Panel Sayfası
![admin-panel](Resimler/admin%20panel.png)
- Admin işlemlerini yaptığı paneldir. Butonlar sonradan ekleme ya da düzenleme yapılabilir. Bunda da şuanlık sadece çıkış butonu çalışmaktadır.

## ER Diyagramı
![ER-Diyagramı](Resimler/ER%20ilişkisi.png)
- Daha iyi bir ER diyagramı. Yeni şeyler eklendikçe daha da güzel ve düzenli olacaktır.

## Kapanış

- login.html sayfası tamamen bitti sayılır. Belki sonradan tasarımsal ya da işlevsel olarak daha farklı şeyler eklenebilir. member.html daha çok odaklanmayı planlıyorum.