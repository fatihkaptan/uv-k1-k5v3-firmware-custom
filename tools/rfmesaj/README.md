# rfkopru — RF Mesaj için PC köprüsü

`rfkopru.py`, USB-C ile bilgisayara bağlı ve **RF Mesaj** uygulaması açık
bir telsizi, telsiz mesajları ile dış dünya arasında bir **ağ geçidine**
çevirir. Tek dosya; `uvterm.py`'yi (`../uvterm`) kullanır.

```bash
pip install pyserial
```

## Sohbet

```bash
python3 tools/rfmesaj/rfkopru.py --anahtar bolu-ortak-anahtar
```

Yazdığınız her satır havaya gider (48 karakterden uzunsa bölünür, Türkçe
harfler ASCII'ye çevrilir); gelen mesajlar zaman damgasıyla görünür.
`--anahtar` telsizin grup anahtarını USB'den ayarlar (telsizde F+2 ile
yazmaktan kolay); iki telsizde de aynı olmalı.

## Telegram köprüsü

Sahadaki arkadaşınız telsizden yazar → evdeki telsiz alır → bilgisayar
Telegram'a iletir; Telegram'dan yazdığınız da evdeki telsizden yayınlanır.

1. Telegram'da **@BotFather** ile bir bot oluşturun, *token*'ı alın.
2. Bota bir mesaj yazın; sohbet kimliğinizi (chat id) öğrenin
   (`https://api.telegram.org/bot<TOKEN>/getUpdates` çıktısındaki `chat.id`).
3. Çalıştırın:

```bash
python3 tools/rfmesaj/rfkopru.py telegram --token 123456:ABC... --sohbet 987654321 --anahtar bolu-ortak-anahtar
```

Token'ı komut satırına yazmak istemezseniz `RFKOPRU_TOKEN` ve
`RFKOPRU_SOHBET` ortam değişkenlerini kullanın. Yalnızca verilen sohbetten
gelen mesajlar yayınlanır. Telegram'a gidenler: `📻 TA2AAA: ...`,
şifreliyse `🔒`, imzasızsa `⚠️`; onaylar `✅ telsizde alindi: TA2BBB`,
başarısızlık `❌ iletilemedi`.

> [!CAUTION]
> Amatör bantta üçüncü kişiler adına (Telegram'daki herkes) yayın yapmak bazı
> ülkelerde kısıtlıdır; köprüyü lisansınızın kurallarına göre kullanın.
> Yayınlanan her pakette telsizin çağrı işareti bulunur.

## Otomatik cevaplar (`!komut`)

```bash
python3 tools/rfmesaj/rfkopru.py komut --anahtar bolu-ortak-anahtar
```

Sizin anahtarınızla imzalı bir mesaj `!` ile başlarsa bilgisayar cevabı
telsizden geri gönderir:

| Komut | Cevap |
|---|---|
| `!saat` | Bilgisayarın saati ve tarihi |
| `!ping` | `pong <çağrı işareti>` |
| `!hava [şehir]` | wttr.in'den hava durumu (varsayılan Bolu; internet gerekir) |
| `!yardim` | Komut listesi |

Kendi komutlarınız için bir betik verin: `--betik ./komutlarim.sh`. Betik
`<komut> <argüman> <çağrı>` ile çağrılır, çıktısının **ilk satırı** cevap
olur; boş çıktı → yerleşik komutlara bakılır. Örnek:

```sh
#!/bin/sh
case "$1" in
  isik) curl -s "http://192.168.1.50/role?durum=$2" >/dev/null && echo "Isik $2 ($3)";;
  sicaklik) echo "Ev: $(cat /sys/class/thermal/thermal_zone0/temp | cut -c1-2) C";;
esac
```

## Testler

```bash
python3 tools/rfmesaj/test_rfkopru.py
```

19 kontrol: Türkçe→ASCII, 48 karakter bölme, satır ayrıştırma, sahte bir
Bot API'ye karşı Telegram köprüsü (izinsiz sohbetin yayın yapamaması dahil),
otomatik cevaplar ve kendi betiğiniz, ayrıca bilgisayar için derlenmiş
RF Mesaj uygulamasına sanal seri port üzerinden **uçtan uca** bağlantı.
Gerçek Telegram ve gerçek telsizle henüz denenmedi.
