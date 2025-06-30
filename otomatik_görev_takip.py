import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from reportlab.lib.utils import ImageReader
from scipy.stats import gaussian_kde
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, blue, green
import datetime
import os
def logla(mesaj):
    with open("hata_dosyam.txt","a+",encoding="utf-8") as file:
        file.write("\n" + " " + "HATA MESAJI : " + " " + mesaj + " " + "HATANIN ALINDIĞI TARİH : " + " " + str(datetime.datetime.now()))
class System:
    def __init__(self):
        self.dosya_adı="görev_listesi.csv"
        if os.path.exists(self.dosya_adı):
            self.df=pd.read_csv(self.dosya_adı)
        else:
            self.df=pd.DataFrame(columns=["Görevin İsmi", "Görevin Kategorisi", "Görevin Süresi (dakika cinsinden)", "Görevin Kaydedilme Tarihi"])
    def görev_ekle(self):
        try:
            görev_sayısı=int(input("Kaç görev eklemek istiyorsunuz : "))
        except ValueError as v:
            print(f"Hata Kodu : {v} , Lütfen sayı giriniz⚠️")
            return
        for _ in range(görev_sayısı):
            görev=input("Görevinizi Giriniz : ")
            kategori=input("Görevinizin Kategorisini Giriniz (eğitim,eğlence,spor vb.) : ")
            try:
                görev_süresi=float(input("Lütfen Görevinizin Kaç Dakika Sürdüğünü Giriniz : "))
            except ValueError as qwe:
                print(f"Lütfen dakika cinsinden girin⚠️ , Hata Kodu : {qwe}")
            görevin_kaydedilme_tarihi=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yeni_görev=pd.DataFrame({"Görevin İsmi":[görev],"Görevin Kategorisi":[kategori],"Görevin Süresi (dakika cinsinden)":[görev_süresi],"Görevin Kaydedilme Tarihi":[görevin_kaydedilme_tarihi]})
            self.df=pd.concat([self.df,yeni_görev],ignore_index=True)
            print(self.df)
        self.df.to_csv(self.dosya_adı,index=False)
        #self.df=self.df.fillna("Bilinmiyor")
        print(self.df)
    def haftalık_analiz(self):
        kac_dakika_çalışıldı=self.df["Görevin Süresi (dakika cinsinden)"].sum()
        print(f"Görevlere Ayrılan Süre : {kac_dakika_çalışıldı} Dakikadır")
        kac_görev_yapıldı=self.df.value_counts()
        print(kac_görev_yapıldı)
        en_fazla_süre=self.df.nlargest(1,"Görevin Süresi (dakika cinsinden)")[["Görevin İsmi","Görevin Süresi (dakika cinsinden)"]]
        print(f"En Fazla Süre Ayrılan Görev : {en_fazla_süre['Görevin İsmi'].values} , Ayrılan Toplam Süre : {en_fazla_süre['Görevin Süresi (dakika cinsinden)'].values}")
        en_az_süre=self.df.nsmallest(1,"Görevin Süresi (dakika cinsinden)")[["Görevin İsmi","Görevin Süresi (dakika cinsinden)"]]
        print(f"En Az Süre Ayrılan Görev : {en_az_süre['Görevin İsmi'].values} , Ayrılan Toplam Süre : {en_az_süre['Görevin Süresi (dakika cinsinden)'].values}")
        kac_tane_kategori_var=self.df["Görevin Kategorisi"].value_counts()
        print(f"Kullanıcı {kac_tane_kategori_var} farklı kategoride görev yapmıştır")
    def grafik_çiz(self):
        print("GRAFİK ÇİZME FONKSİYONUNA HOŞGELDİNİZ!")
        print("YAPABİLECEKLERİNİZ:\n1=Pasta Grafiği ile Sürenin İncelenmesi\n2=Bar Grafiği ile Sürenin İncelenmesi\n3=İleri Düzey Analiz")
        try:
            decision=int(input("Yapmak İstediğiniz İşlemin Numarasını Giriniz : "))
            if decision==1:
                plt.style.use("seaborn-v0_8-darkgrid")
                plt.pie(self.df["Görevin Süresi (dakika cinsinden)"], shadow=True,colors=["Red", "Blue", "Pink", "Yellow", "Purple"], autopct="%1.1f%%",labels=self.df["Görevin Kategorisi"])
                plt.title("KATEGORİLERE GÖRE AYRILAN SÜRENİN İNCELENMESİ", color="Black", fontsize=20)
                plt_filename="pasta_grafiği.png"
                plt.savefig(plt_filename, dpi=300, bbox_inches='tight')
                try:
                    qwe=int(input("Bu dosyayı pdf haline getirmek istiyorsanız 1 , istemiyorsanız 0 tuşlayınız : "))
                    if qwe==1:
                        pdf_filename="rapor1.pdf"
                        c=canvas.Canvas(pdf_filename)
                        c.setFont("Times-Roman",16)
                        c.drawString(150,792,"KATEGORILERE GÖRE ZAMAN GRAFIGI")
                        img=ImageReader(plt_filename)
                        img_width, img_height = 400, 200
                        c.drawImage(img, 100, 500, width=img_width, height=img_height)
                        c.setFont("Helvetica",12)
                        c.drawString(25,400,"BU GRAFIK KULLANICININ GÖREVLERINE AYIRDIGI ZAMANI PASTA GRAFIGI ILE INCELER")
                        c.setFont("Helvetica",12)
                        c.drawString(0,250,f"BU DOSYANIN OLUSTURULMA ZAMANI {datetime.datetime.now()}")
                        c.save()
                    elif qwe==0:
                        print("Lütfen Bekleyin,PNG dosyası oluşturluyor 📁")
                        time.sleep(5)
                        plt.show()
                    else:
                        print("Lütfen Belirtilen İşlem Değerlerini Giriniz")
                        logla("Kullanıcı Belirtilen Değeri Girmedi")
                except ValueError as asdf:
                    print(f"Hata Kodu : {asdf} , Lütfen Belirtilen İşlem Değerlerini Giriniz!")
                    logla("Kullanıcı Belirtilen Değeri Girmedi")
            elif decision==2:
                plt.bar(self.df["Görevin İsmi"],self.df["Görevin Süresi (dakika cinsinden)"],color="BLue",linewidth=3)
                plt.xlabel("KATEGORİLER",color="Black",fontsize=15)
                plt.ylabel("SÜRE",color="Black",fontsize=15)
                plt.title("KATEGORİLERE GÖRE AYRILAN SÜRENİN İNCELENMESİ",color="Black",fontsize=20)
                plt.grid(True)
                plt_filename="bar_grafiği.png"
                plt.savefig(plt_filename, dpi=300, bbox_inches='tight')
                try:
                    qwe=int(input("Bu dosyayı pdf haline getirmek istiyorsanız 1 , istemiyorsanız 0 tuşlayınız : "))
                    if qwe==1:
                        pdf_filename="bar_grafiği.pdf"
                        c=canvas.Canvas(pdf_filename)
                        c.setFont("Helvetica",16)
                        c.drawString(150,792,"KATEGORILERE GÖRE ZAMAN GRAFIGI")
                        ımage=ImageReader(plt_filename)
                        ımage_width,ımage_height=400,500
                        c.drawImage(ımage,100,200,width=ımage_width,height=ımage_height)
                        c.setFont("Helvetica",12)
                        c.drawString(75,100,"BU GRAFIK KULLANICIDAN ALINAN VERIYLE OLUSTURULMUSTUR")
                        c.setFont("Helvetica",12)
                        c.drawString(75,25,f"BU DOSYA {datetime.datetime.now()} TARIHINDE OLUSTURULMUSTUR")
                        c.save()
                    elif qwe==0:
                        print("PNG dosyası oluşturuluyor...")
                        time.sleep(5)
                        plt.show()
                    else:
                        print("Lütfen Belirtilen Değerleri Giriniz!")
                        logla("Kullanıcı Belirtilen Değeri Girmedi")
                except ValueError as tyu:
                    print(f"Hata Kodu : {tyu} , Lütfen Belirtilen Değerleri Giriniz!")
                    logla("Kullanıcı Belirtilen Değeri Girmedi")
            elif decision==3:
                plt.hist(self.df["Görevin Süresi (dakika cinsinden)"],bins=8,color="Yellow",edgecolor="Red",linewidth=3,density=True)
                kde=gaussian_kde(self.df["Görevin Süresi (dakika cinsinden)"])
                x=np.linspace(self.df["Görevin Süresi (dakika cinsinden)"].min(),self.df["Görevin Süresi (dakika cinsinden)"].max(),100)
                plt.plot(x,kde(x),color="Black",linestyle=":",linewidth=3,label="Yoğunluk Eğrisi")
                plt.title("İLERİ DÜZEY ANALİZ",color="Black",fontsize=20)
                plt.legend()
                plt_filename="hist.jpg"
                plt.savefig(plt_filename, dpi=300, bbox_inches='tight')
                try:
                    karar=int(input("Bu dosyayı pdf haline getirmek istiyorsanız 1 ,istemiyorsanız 0 giriniz : "))
                    if karar==1:
                        dosya_adı="hist.pdf"
                        c=canvas.Canvas(dosya_adı)
                        c.setFont("Helvetica",16)
                        c.drawString(200,792,"ILERI DÜZEY ANALIZ")
                        ımg=ImageReader(plt_filename)
                        c.drawImage(ımg,100,200,width=400,height=500)
                        c.setFont("Helvetica",16)
                        c.drawString(50,100,"BU GRAFIK ILERI DÜZEY ANALIZ KULLANILARAK OLUSTURULMUSTUR")
                        c.setFont("Helvetica",16)
                        c.drawString(50,50,f"BU DOSYA {datetime.datetime.now()} TARIHINDE OLUSTURULMUSTUR")
                        c.save()
                    elif karar==2:
                        print("Matplotlib kütüphanesi hazırlanıyor...")
                        time.sleep(5)
                        plt.show()
                    else:
                        print("Lütfen Belirtilen Değerleri Tuşlayınız!")
                        logla("Kullanıcı Belirtilen Değeri Girmedi")
                except ValueError as uıo:
                    print(f"Hata Kodu : {uıo} ,Lütfen Belirtilen Değerleri Girin...")
                    logla("Kullanıcı Belirtilen Değeri Girmedi")
            else:
                print("Lütfen Belirtilen İşlem Değerlerini Giriniz😤")
                logla("Kullanıcı Belirtilen Değeri Girmedi")
        except ValueError as asd:
            print(f"Hata kodu : {asd} , Lütfen Belirtilen İşlem Değerlerini Giriniz😤")
            logla("Kullanıcı Belirtilen Değeri Girmedi")
def main():
    system = System()
    print("GÖREV TAKİP SİSTEMİNE HOŞGELDİNİZ 😄".center(50,"*"))
    print("Yapabilecekleriniz:\n1=Görev Ekleme\n2=Görevsel Analiz🧠\n3=Grafik veya Rapor Oluşturma📊\n4=Sistemden Çıkış🥲")
    while True:
        try:
            karar=int(input("Yapmak istediğiniz işlemin numarasını giriniz : "))
            if karar==1:
                system.görev_ekle()
            elif karar==2:
                system.haftalık_analiz()
            elif karar==3:
                system.grafik_çiz()
            elif karar==4:
                print("Sistemden Çıkıldı🥲")
                quit()
            else:
                print("Lütfen Belirtilen Değerleri Giriniz⚠️")
                logla("Kullanıcı Belirtilen Değeri Girmedi")
        except ValueError as qwer:
            print(f"Hata Kodu : {qwer} , Lütfen Belirtilen İşlem Numaralarını Giriniz😤")
            logla("Kullanıcı Belirtilen Değeri Girmedi")
if __name__ == "__main__":
    main()











































































