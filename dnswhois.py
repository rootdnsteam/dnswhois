import subprocess
import colorama
from colorama import Fore, Style
import dns.resolver
import dns.exception

def dns_sorgula(alan_adi, sorgu_tipi):
    """
    Belirtilen alan adı için belirtilen DNS sorgusu yapar ve sonuçları yazdırır.

    Args:
        alan_adi: Sorgu yapılacak alan adı.
        sorgu_tipi: DNS sorgusu tipi.
    """
    try:
        cevaplar = resolver.query(alan_adi, sorgu_tipi)
        print(f"\n### {sorgu_tipi} Kayıtları ({alan_adi})")
        for cevap in cevaplar:
            print(cevap)
        print(f"\nToplam {len(cevaplar)} adet {sorgu_tipi} kaydı bulundu.")
    except dns.resolver.NXDOMAIN:
        print(f"{alan_adi} için {sorgu_tipi} kaydı bulunamadı.")
    except dns.resolver.Timeout:
        print(f"{alan_adi} için {sorgu_tipi} sorgusu zaman aşımına uğradı.")
    except dns.resolver.NoAnswer:
        print(f"{alan_adi} için {sorgu_tipi} kaydı bulunamadı.")
    except dns.exception.DNSException as e:
        print(f"{alan_adi} için {sorgu_tipi} sorgusunda bir hata oluştu: {str(e)}")

# Gerekli kütüphaneleri kontrol etme ve otomatik kurma
try:
    import dnspython
except ImportError:
    print("Kütüphaneler kuruluyor...")
    subprocess.run(["pip", "install", "dnspython"])

# Renklendirmeyi başlatma
colorama.init()

# Belirli DNS sunucularını kullanarak resolver oluştur
resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ['8.8.8.8', '8.8.4.4']

dns_team_ascii_art = """
    DDD   N   N  SSS    TTTTT  EEEEE  AAAAA  M   M
   D   D  NN  N  S       TT    E      A     A  MM MM
  D   D  N N N   SSS     TT    EEEE  AAAAAAA  M M M
 D   D  N  NN      S     TT    E     A     A  M   M
  DDD   N   N  SSS      TTT   EEEEE A     A  M   M
"""
print(Fore.RED + Style.BRIGHT + dns_team_ascii_art + Style.RESET_ALL)

# Sorgu tipleri sözlüğünü tanımla
sorgu_tipleri = {
    "A": "IPv4 Adresi",
    "AAAA": "IPv6 Adresi",
    "CNAME": "Kanonik Ad",
    "MX": "E-posta Sunucuları",
    "NS": "Alan Adı Sunucuları",
    "TXT": "Metin Kayıtları",
    "PTR": "Ters İşaretçi Kayıtları",
    "SRV": "Hizmet Kayıtları",
    "SOA": "Başlangıç Yetkili Kurumu"
}

# Kullanıcıdan alan adı girdisi alma
while True:
    alan_adi = input("Alan adını giriniz (q ile çıkış): ")
    if alan_adi.lower() == "q":
        break
    
    # Kullanıcıya hangi sorgu tipini seçmek istediğini sor
    print("\nSorgu Tipleri:")
    for index, (tip, aciklama) in enumerate(sorgu_tipleri.items(), start=1):
        print(f"{index}. {aciklama} ({tip})")

    # Kullanıcıdan sorgu tipini seçmesini iste
    secim = input("Hangi sorgu tipini kullanmak istersiniz? (1-9): ")
    
    # Kullanıcının girdisiyle sorgu tipini belirle
    try:
        secim_index = int(secim) - 1
        sorgu_tipi = list(sorgu_tipleri.keys())[secim_index]
    except (ValueError, IndexError):
        print("Geçersiz sorgu tipi seçimi. Varsayılan olarak 'A' kullanılacak.")
        sorgu_tipi = 'A'

    # DNS sorgusunu gerçekleştir
    dns_sorgula(alan_adi, sorgu_tipi)

print("Program sonlandı.")
