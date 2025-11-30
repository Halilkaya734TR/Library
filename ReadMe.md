# <center>Kütüphane Ödevi(Yapım Aşamasında)</center>

## Yenilikler (30.10.25)
- **backend.py** içindeki yeni kodlar sayesinde veri tabanından bilgilerini alıp kullanıcı kontrol edip üye sayfasına geçiyor. Yanlışsa aynı sayfada kalınıyor
- **login.html** içindeki form Flask uygun hale getirildi.
- **login.html** artık Kullanıcı Adı yerine email soruyor.
- html dosyaları templates dosyası altında toplandı.
- ER ilişkisi (Hala çok hatalı zamanla düzelecek.) ve bazı fotoğraftlar yeni halleriyle güncellendi!

## İçindekiler
- [Sayfa Görünümü](#sayfa-görünümü)  
- [ER Diyagramı](#er-diyagramı)  

## Sayfa Görünümü
- **NOT:** En son hali değildir. Proje bitene kadar değişiklikler olabilir. Bunlar şuanki yaptıklarım ve üstüne koyup ya da değiştirip daha iyisini yapacaklarımdır.
### Giriş Üye Sayfası:

![login-üye](Resimler/login%20üye.png)
- Kutucukların içine veri yazılıp butona basınca üye panel yönlendiriyor. Ama şuanda db daha tutmadığımdan ve denetleme yapmadığımdan her türlü giriş izin veriyor. Daha sonraları onu düzelteceğim.

### Giriş Admin Sayfası
![login-adnmin](Resimler/login%20admin.png)
- Üye ile aynı işlevlere sahip. Sadece fark olarak admin panel yönlendiriyor. Aynı şekilde bunda da daha kontrol etme yok.

### Giriş Kayıt Ol Sayfası
![login-kayıt-ol](Resimler/login%20kayıt.png)
- Kayıt olmak için sayfa böyle gözükmektedir. Kayıt ol butonunun şuanlık işlevi yoktur.

### Üye Panel Sayfası
![üye-panel](Resimler/üye%20panel.png)
- Üyenin işlemlerini yapacağı paneldir. Şuanlık 5 buton var. Şuanlık sadece çıkış butonunun işlevi bulunmaktadır.

### Admin Panel Sayfası
![admin-panel](Resimler/admin%20panel.png)
- Admin işlemlerini yaptığı paneldir. Butonlar sonradan ekleme ya da düzenleme yapılabilir. Bunda da şuanlık sadece çıkış butonu çalışmaktadır.

## ER Diyagramı
![ER-Diyagramı](Resimler/ER%20ilişkisi.png)
- Şuanlık yaptığım çok güzel ve detaylı olmayan bi ER ilişkisi. Kesinlikle hatalı unsurlar vardır. Sadece şuanlık fikir olsun ve ilk hallerini de koymak istedim. Projeyi geliştirirken illa daha da güzel, düzgün ve doğru bi ER ilişkisi hazırlayacağım.

## Kapanış

- Yakında yeni commitle backend giriş komutları ve ek şeyler eklenecektir.
