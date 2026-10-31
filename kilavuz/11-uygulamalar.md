# 11. Overlay Uygulamaları (Labs)

[← Önceki: Menü referansı](10-menu-referansi.md) · [İçindekiler](README.md) · [Sonraki: Uygulamalı senaryolar →](12-uygulamali-senaryolar.md)

**Labs** sürümü, telsize sonradan yüklenebilen **uygulamaları** destekler. Bu bölüm
uygulama sistemini, ortak kullanım kurallarını ve her uygulamayı tek tek anlatır.
Bilgiler `App/apps/*/README.md` belgelerinden ve uygulama kaynak kodlarından derlenmiştir.

> [!IMPORTANT]
> - Uygulamaların çoğu **deneyseldir** ("work in progress"). Beklendiği gibi çalışmayabilir.
> - Uygulama dosyalarını her zaman kurulu firmware ile **aynı sürümden** alın. Farklı
>   sürümler arasında uygulama arayüzü (ABI/API) uyumsuz olabilir; uyumsuz uygulama
>   `NOT SUPPORTED` hatası verir.
> - **Gönderim yapan uygulamalar** (APRS TX, APRS DIGI, KISS TNC, Beacon, BEAM, CW Keyer,
>   CW USB, SSTV, ToneCall) yalnızca **belgeyle** ve **izin verilen frekanslarda** kullanılmalıdır.

## İçindekiler

1. [Uygulama sistemi nasıl çalışır?](#111-uygulama-sistemi-nasıl-çalışır)
2. [Ortak kurallar ve kavramlar](#112-ortak-kurallar-ve-kavramlar)
3. [Radyo araçları](#113-radyo-araçları)
4. [APRS uygulamaları](#114-aprs-uygulamaları)
5. [Havacılık ve denizcilik](#115-havacılık-ve-denizcilik)
6. [Radyosondalar ve konum](#116-radyosondalar-ve-konum)
7. [Acil durum işaretçileri](#117-acil-durum-işaretçileri)
8. [Diğer veri modları: POCSAG, SSTV](#118-diğer-veri-modları-pocsag-sstv)
9. [Mors (CW) uygulamaları](#119-mors-cw-uygulamaları)
10. [Ölçüm ve yardımcı araçlar](#1110-ölçüm-ve-yardımcı-araçlar)
11. [Oyunlar ve demolar](#1111-oyunlar-ve-demolar)
12. [Hangi iş için hangi uygulama?](#1112-hangi-iş-için-hangi-uygulama)

---

## 11.1 Uygulama sistemi nasıl çalışır?

- Uygulamalar telsizin **harici flash belleğinde** (2 MiB) saklanır. **64 yuva** vardır.
- Bir uygulama çalıştırıldığında, mikrodenetleyicinin RAM'indeki **4 KiB'lık özel bir alana**
  ("overlay") yüklenir ve çalışır. Çıkınca bu alan bir sonraki uygulamaya kalır.
- Büyük, salt okunur veriler (metinler, yazı tipleri, simgeler, tablolar) flash'ta kalır;
  uygulama gerektikçe okur.
- Uygulamalar **UV Studio** ile yüklenir, kaldırılır ve güncellenir.
- Bir uygulamanın ayarları, kendi yuvasının yapılandırma alanında saklanır ve çoğunlukla
  **`EXIT` ile çıkarken** yazılır. Telsizi uygulama açıkken kapatırsanız o oturumdaki
  değişiklikler kaybolabilir.

### Uygulama menüsü (`F` + `7`)

| Tuş | İşlev |
|-----|-------|
| `UP` / `DOWN` | Uygulama seç |
| `MENU` | Uygulamayı başlat |
| `*` | Sağ sütunda boyut ↔ sürüm |
| `EXIT` | Çık |

Bazı uygulamalar (FM, Fox Hunt, Beacon, BEAM, ToneCall) yan tuşlara atanarak doğrudan da açılabilir.

## 11.2 Ortak kurallar ve kavramlar

### Ortak tuş alışkanlıkları

| Tuş | Çoğu uygulamada |
|-----|-----------------|
| `EXIT` | Çık (ayarları kaydet) |
| `UP` / `DOWN` | Kaydır, geçmişte gezin. UV-K1'de `SetNav`'a göre sol/sağ. |
| `*` | Normal ↔ sıkışık (compact) görünüm |
| `1` | Hoparlör aç/kapat (alıcı uygulamalarında) |
| `2` | Listeyi/sayaçları temizle |
| `F`, sonra tuş | Ayarın **ters yönü** (azaltma) veya ikincil işlev. Durum çubuğunda kutulu `F`. |
| Uzun `F` | Tuş kilidi (bazı uygulamalarda) |

### Ekran alışkanlıkları

- Durum çubuğunda uygulamanın adı ve ilk veri gelene kadar **`WAIT`** kapsülü.
- Hoparlör simgesi: Ses açık.
- ▲ / ▼: Yukarıda veya aşağıda görünmeyen satırlar ya da başka kayıtlar var.
- `2/5` gibi kapsül: Gösterilen kayıt / saklanan kayıt sayısı (1 = en yeni).
- Noktalı ayırıcı çizginin altında büyük rakamlarla frekans; en altta seviye (dBm) ve sayaçlar.

### Ses yolu: STD ve RAW

Veri çözen uygulamalar, BK4829'un **demodüle edilmiş ses çıkışını** mikrodenetleyicinin
ADC'si ile örnekler.

- **STD**: Telsizin normal ses yolu: 300 Hz yüksek geçiren, geri vurgu, 3 kHz alçak geçiren
  filtre. Normal bir alıcının duyduğu sinyal. APRS, ACARS, ATIS bunu kullanır.
- **RAW**: Ses filtreleri ve AFC kapatılmış, FM'de diskriminatör doğrudan alınır. Geniş bantlı
  veriler (radyosondalar, POCSAG, AIS, EPIRB) için gereklidir. Bu yolda squelch biti kapalı
  kaldığından hoparlör squelch'e bağlı olmadan çalar.

### Zayıflatıcı (ATT)

Çok yakın ve güçlü bir verici alıcıyı doyurur (bkz. [2.10](02-radyo-dalgalari-ve-spektrum.md#210-parazit-türleri-harmonik-imaj-intermodülasyon-doyma)).
Birçok uygulamada ön kat zayıflatıcısı vardır: **`0 dB`, `6 dB`, `15 dB`, `27 dB`, `BYP`,
`BYP+`**. `BYP+` en yüksek kazançtır; güçlü sinyalde kullanmayın.

### Test frekansı 433,650 MHz

Uygulama belgelerinde sık geçen **433,650 MHz**, geliştiricilerin Flipper Zero veya
LimeSDR ile ürettikleri test sinyalleri için kullandıkları masa başı frekansıdır.
Gerçek kullanımda ilgili hizmetin frekansını seçin.

## 11.3 Radyo araçları

### Broadcast FM

FM yayın radyosu, uygulama olarak. Çalışırken telsizi tamamen kullanır (arka planda VHF/UHF
dinleme yapmaz). Tuşları yerleşik FM radyo ile aynıdır (bkz. [9.15](09-cihaz-kullanimi.md#915-fm-yayın-radyosu-f--0)):
rakamlarla frekans/kanal, `UP`/`DOWN`, `*` arama, `F` + `*` otomatik tarama (48 kanal),
`MENU` kaydet/sil, `F` + `1` bant, `F` + `3` VFO ↔ hafıza, `F` + `0` veya `EXIT` çıkış.

### Fox Hunt

Gizli vericiyi (tilki) bulmak için sinyal gücü göstergesi: düzeltilmiş dBm büyük rakamla,
IARU S-metre merdiveni veya kayan geçmiş, tepe/minimum, 1 saniyelik eğilim, zayıflatıcı
ve Geiger tarzı ses.

| Tuş | İşlev |
|-----|-------|
| `1` | Gösterge: çubuk / geçmiş |
| `2` | Ses: kapalı / bip / istasyon sesi |
| `3`, `UP` / `DOWN` | Zayıflatıcı |
| `MENU` | Tepe/minimum değerlerini sıfırla |
| Uzun `F` | Tuş kilidi |
| `EXIT` | Çık |

### Beacon

Telsizi gizli bir ARDF vericisine dönüştürür (bkz. [9.22](09-cihaz-kullanimi.md#922-fox-hunt-beacon-ve-beam)).

| Tuş | İşlev |
|-----|-------|
| `1` | Gönderim penceresi |
| `2` | Bekleme aralığı |
| `3` | Tanımlayıcı (`MOE` … `MO5`, `MO`, çağrı işareti, çağrı işareti + `MOE`) |
| `4` | `TONE` (MCW, taşıyıcı sürekli) / `CARR` (taşıyıcı da kesilir) |
| `F` + tuş | Geri |
| `MENU` | Beklemeyi yeniden başlat |
| Uzun `F` | Tuş kilidi |
| `EXIT` | Çık |

### Beam

Seçili VFO'nun ayarlarını telsizden telsize radyo üzerinden aktarır. Alıcı, gelen ayarı
ilk boş kanala kaydeder. `UP`/`DOWN`: gönder ↔ al modu, `MENU`: başlat, `EXIT`: çık.

### Sig Finder (sinyal bulucu, yön bulma)

Yönlü bir antenle herhangi bir taşıyıcının yönünü bulur: 121,5 / 243 MHz imdat işaretçisi,
tilki, parazit kaynağı. Ayrıca sinyalin gerçek bir **ELT (uçak imdat işaretçisi)** olup
olmadığını, süpürülen sesinden tanır ve durum çubuğunda `ELT` gösterir.

**Kullanım**

1. VFO'yu sinyale ayarlayın: 121,5 / 243 MHz işaretçi için **AM**, diğerleri için FM veya USB.
2. Sig Finder'ı açın. Anteni önünüzde tutup **yavaşça dönün**.
3. Gösterge **mutlak değil, görülen en güçlü seviyeye göre** çalışır: `0` = tepedesiniz.
   Kaynağa yaklaştıkça sinyal güçlense bile çalışmaya devam eder.

| Tuş | İşlev |
|-----|-------|
| `1` | `FOLLOW` (tepe yavaşça düşer, yürürken) / `SWEEP` (tepe sabit, 360° tarama için) |
| `2` | Ses: kapalı / bip (tepeye yaklaştıkça hızlanır ve tizleşir) / dinle / USB dinle |
| `3`, `UP` / `DOWN` | Zayıflatıcı (elle) |
| `4` | Otomatik zayıflatıcı aç/kapat |
| `5` | FOLLOW düşüş hızı: 0,5 / 1 / 2 / 4 dB/s |
| `6` | Arka ışığı açık tut |
| `MENU` | Tepeyi sıfırla; SWEEP'te yeni tarama |
| `F` (kısa) | Sonraki `2`, `3`, `5` geri yönde |
| `F` (0,5 s) | Tuş kilidi |
| `EXIT` | Çık |

**İşaretçi aramada önerilen sıra**: Ses **kapalı** iken `ELT` doğrulansın, sonra **bip**
moduyla yönü bulun. Gerçek bir işaretçi bulursanız **112**'ye bildirin.

### Spectrum3D

VFO çevresindeki bandı zamanla birlikte **3B bir dağ manzarası** gibi çizer. Tepeler istasyonlardır.

| Tuş | İşlev |
|-----|-------|
| `UP` / `DOWN` | Merkezi bir nokta kaydır |
| `1` / `F` + `1` | Merkezi 6,25 kHz yukarı / aşağı |
| `3` / `F` + `3` | Açıklığı genişlet / daralt |
| `4` / `6` | Döndür |
| `2` / `8` | Eğ |
| `5` | Görünümü sıfırla |
| `0` | En güçlü tepeyi FM ile dinle |
| `*` | Hız |
| `MENU` | Dondur |
| `EXIT` | Çık |

### ToneCall

**Ardışık ton çağrısı (selcall)** gönderir: ZVEI-1, ZVEI-2, CCIR-1, CCIR-2. 4 ön ayar saklanır.
Başlıca kullanım alanı Alp bölgesindeki acil kanaldır (Canal E). Amatör röleleri açmak için kullanılmaz.

| Ekran | Tuş | İşlev |
|-------|-----|-------|
| Liste | `UP` / `DOWN` | Ön ayar seç |
| Liste | `MENU` / `PTT` | Seçili çağrıyı gönder |
| Liste | `F` | Ön ayarı düzenle |
| Düzenleme | `0`–`9` | Rakam ekle (en fazla 8) |
| Düzenleme | `F` | Son rakamı sil |
| Düzenleme | `*` | Tür: ZVEI-1 → ZVEI-2 → CCIR-1 → CCIR-2 |
| Düzenleme | `MENU` / `EXIT` | Kaydet / vazgeç |

Çağrı, kanalın normal TX ayarlarıyla (frekans, güç, CTCSS/DCS) gönderilir. Ardından uygulama
aynı kanalda dinlemede kalır; karşı tarafın onayı duyulur.

## 11.4 APRS uygulamaları

APRS'in ne olduğu için bkz. [4.7](04-modulasyon-ve-sinyal-turleri.md#47-afsk-ve-bell-202-aprs-ve-paket-radyo)
ve [6.16](06-amator-telsizcilik.md#616-aprs-ağı). Avrupa'da frekans **144,800 MHz, FM**.

### APRS RX (alım)

AX.25 / Bell 202 1200 baud paketlerini çözer, **son 5 paketi** saklar. Mic-E (çoğu Yaesu/Kenwood
cihazı) ve standart konum biçimlerini çözüp enlem, boylam, hız, yön, sembol ve yorumu gösterir.
Paketin APRS sembolü 20 × 20 piksellik bir simge olarak görünür.

1. VFO: **144,800 MHz, FM**.
2. `F` + `7` → **APRS RX**.
3. Hoparlör varsayılan olarak kapalıdır (çözücünün buna ihtiyacı yoktur). `1` ile açın;
   squelch'e bağlıdır, paketler duyulur, aradaki gürültü duyulmaz.

| Tuş | İşlev |
|-----|-------|
| `UP` / `DOWN` (basılı) | Paket gövdesini kaydır |
| `UP` / `DOWN` (en başta/sonda tekrar) | Daha yeni / daha eski paket |
| `*` | Normal (18 karakter) ↔ sıkışık (32 karakter) görünüm |
| `1` | Hoparlör |
| `2` | Paketleri ve sayaçları temizle |
| `EXIT` | Çık (geçmiş silinir) |

### APRS TX (konum gönderme)

Her `PTT` veya `MENU` basışında **bir APRS konum paketi** gönderir. İsteğe bağlı olarak
belirli aralıklarla otomatik gönderir (beacon).

**Varsayılan paket**: kaynak = profil çağrı işareti (boşsa açılış mesajının ilk satırı) + SSID `-7`,
hedef `APZK5`, yol `WIDE1-1`, konum, sembol `/[` (yaya), yorum.

> [!IMPORTANT]
> **Konumunuzu ve çağrı işaretinizi mutlaka APRS Edit ile ayarlayın.** Varsayılan konum
> geliştiricinin örnek konumudur. Geçerli bir çağrı işareti yoksa uygulama `No callsign`
> gösterir ve gönderim yapmaz.

| Tuş | İşlev |
|-----|-------|
| `PTT` veya `MENU` | Bir paket gönder |
| `UP` / `DOWN` | Paket metnini kaydır |
| `1` / `F` + `1` | Ton seviyesini (sapma) artır / azalt |
| `2` / `F` + `2` | Twist (1200/2200 Hz dengesi) artır / azalt |
| `3` / `F` + `3` | Otomatik gönderim aralığı: kapalı, 1, 5, 15, 30, 60 dk / kapat |
| `0` | APRS Edit'i aç |
| `*` | Kaydırmalı ↔ sıkışık görünüm |
| `EXIT` | Çık (otomatik gönderim yalnızca uygulama açıkken çalışır) |

**Yollar**: `DIRECT` (aktarıcı yok), `WIDE1-1` (bir aktarım), `WIDE1-1,WIDE2-1` (mobil/taşınabilir
için olağan, iki aktarım), `ARISS` (ISS digipeater'ı; VFO'yu 145,825 MHz'e ayarlayın).

**Otomatik gönderim aralığı** seçerken ağı düşünün: sabit durumdaysanız 15–30 dk yeterlidir.
Gereksiz sık gönderim kanalı tıkar.

### APRS Edit (profil düzenleyici)

APRS TX'in profilini düzenler: çağrı işareti, SSID, enlem, boylam, yol, sembol, yorum.

| Tuş | İşlev |
|-----|-------|
| `UP` / `DOWN` | Alan seç |
| `MENU` | Alanı düzenle / onayla |
| `EXIT` | Alan düzenlemesinde: vazgeç. Ana ekranda: kaydet ve çık (APRS TX'ten açıldıysa ona dön) |

**Alanlar**

- **Call**: Telefon tuş takımı gibi büyük harf girişi. `*` = `ABC`/`123`, uzun rakam = rakam,
  `F` = sil, `UP`/`DOWN` = imleç. Boş = `AUTO` (açılış mesajındaki çağrı işareti).
- **SSID**: 0–15 (rakam veya `UP`/`DOWN`).
- **Lat / Lon**: Rakamlar yazıp ilerler; `UP`/`DOWN` imleç; `*` = K/G (N/S) veya D/B (E/W).
  Biçim **derece + dakika**: `4100.50N` = 41° 00,50' K.
- **Path**: `DIRECT`, `WIDE1-1`, `WIDE1-1,WIDE2-1`, `ARISS`.
- **Symbol**: 48 sembol, önizlemeli.
- **Comm.** (yorum): 64 karakterlik giriş; `*` = `ABC`/`abc`/`123`; `PTT` = hazır mesajlar.

> **Ondalık dereceyi dereceye-dakikaya çevirme**: 41,0085° → 41° + 0,0085 × 60 = 41° 00,51'.

### APRS DIGI (aktarıcı)

Duyduğu uygun paketleri bir kez daha yayınlayan, **sınırlı bir dolgu (fill-in) digipeater'ıdır**.

- `1`: `W1` (yalnızca `WIDE1-1`) / `W12` (`WIDE1-1` ve `WIDE2-1`).
- Açılış mesajının ilk satırında 1–6 karakterlik bir çağrı işareti gerekir. Aktarıcı kendini
  bu çağrı işareti ve SSID `-3` ile tanıtır.
- Squelch 0 olmamalıdır. Kanal en az 100–227 ms boş kalmadan gönderim yapmaz.
- Son 30 saniyedeki aynı paketleri tekrar göndermez.

> [!IMPORTANT]
> İnsansız çalışan bir aktarıcı kurmak ayrıca izne tabi olabilir. Mevcut APRS ağına zarar
> vermemek için yerel APRS sorumlularıyla görüşün.

### KISS TNC (telefonla APRS)

Telefonu harita ve mesajlaşma ekranı, telsizi **TNC (modem)** olarak kullanırsınız:
Android'deki **APRSdroid** veya bilgisayardaki herhangi bir KISS istemcisi.

**Gerekenler**

- Telefon için **USB OTG adaptörü** (telefon USB ana cihaz olur).
- Low üstü güçlerde, kablonun **telsiz ucuna ferrit** (VHF tipi 31 veya 43, kablo 2–4 tur
  sarılarak). Yoksa gönderim anında kablonun topladığı RF, USB bağlantısını koparır.

**Kurulum**

1. VFO: 144,800 MHz, FM. **KISS TNC**'yi açın.
2. APRSdroid → Tercihler → Bağlantı: protokol **TNC (KISS)**, tür **USB serial**, KISS başlangıç
   dizgesi **boş**.
3. Telsizi OTG ile telefona bağlayın, izlemeyi başlatın, USB iznini verin.

| Tuş | İşlev |
|-----|-------|
| `1` | Hoparlör |
| `2` | Bilgisayara/telefona RF'siz test paketi gönder (USB bağlantısını kontrol eder) |
| `3` | Yalnızca alım: telefondan gelen paketler gönderilmez |
| `EXIT` | Çık |

Durum çubuğu: `USB` (bağlı), `NO USB`, `TX`, `RX ONLY`.

### GeoNav

APRS profilindeki konumu "ev" olarak alır ve bir radyosonda uygulamasından aktarılan konuma
**yön ve mesafe** gösterir. Düşen bir radyosondayı aramak için kullanılır.

## 11.5 Havacılık ve denizcilik

### ACARS RX

Uçaklarla yer istasyonları arasındaki **ACARS** veri mesajlarını (2400 bit/s, AM-MSK) çözer.
Son 3 mesajı saklar: uçak kuyruk tescili, uçuş numarası, etiket ve metin.

1. VFO: **AM**, yerel ACARS frekansı (Avrupa'da 131,525, 131,725, 131,825 MHz'i deneyin).
2. **ACARS RX**'i açın.

| Tuş | İşlev |
|-----|-------|
| `UP` / `DOWN` | Kaydır / mesajlar arasında gez |
| `*` | Normal ↔ sıkışık görünüm |
| `1` | Hoparlör (yalnızca geçerli bir ACARS başlığı tanındığında açılır) |
| `F` | Çözülmüş ↔ ham metin |
| `2` | Geçmişi ve sayaçları temizle |
| `EXIT` | Çık |

Alt satır: seviye, `RX` (geçerli mesaj sayısı), `FIX` (eşlik biti onarılarak kurtarılanlar).
Mesaj gelmezken: `SYN` (bulunan başlıklar), `CRC` (kontrol hatası), `PAR` (eşlik hatası).
ACARS mesajları kısa ve teknik operasyon mesajlarıdır; çoğu insan için okunaklı değildir.

### AIS RX

Gemilerin **AIS** konum ve kimlik yayınlarını (9600 bit/s GMSK) çözer, **son 4 gemiyi**
MMSI numarasına göre birleştirerek saklar: ad, MMSI, seyir durumu, konum, hız (SOG), rota (COG),
pruva (HDG), varış yeri; iç su yolu gemileri için ENI ve boyutlar.

1. VFO: **FM**, **161,975 MHz (AIS 1)** veya **162,025 MHz (AIS 2)**. Uygulama tek kanalı dinler.
2. **AIS RX**'i açın.

| Tuş | İşlev |
|-----|-------|
| `UP` / `DOWN` (basılı) | Kaydır |
| `UP` / `DOWN` (en başta/sonda) | Daha yeni / eski gemi |
| `*` | Normal ↔ sıkışık |
| `1` | Hoparlör (squelch'e bağlı değil) |
| `2` | Listeyi temizle |
| `EXIT` | Çık |

Gemi ilk gelene kadar alt satırda `sync` (bulunan patlamalar) ve `crc` (geçerli çerçeveler)
sayaçları görünür. Deniz kenarında veya yüksek bir yerde çok daha iyi sonuç alırsınız.

### ATIS RX

Avrupa **iç su yollarında** (Ren, Tuna vb.) gemi telsizlerinin her gönderimin sonunda yolladığı
**ATIS** kimliğini çözer: çağrı işareti, 10 haneli kimlik, ülke. Çalışma kanalının kendisinde
yayınlanır. Türkiye'deki denizlerde yaygın değildir.

`UP`/`DOWN`: istasyonlar (8 adede kadar), `1`: hoparlör, `2`: temizle, `EXIT`: çık.

### ATIS DSC RX

Deniz VHF **kanal 70 (156,525 MHz)** üzerindeki **DSC** (dijital seçmeli çağrı) mesajlarını
çözer: çağrının türü (imdat, imdat onayı/aktarımı, acil, emniyet, rutin, test), gönderen
(MMSI, ülke), alıcı ve imdat çağrılarında doğanın türü, saat ve konum.

- **İmdat veya acil çağrı** geldiğinde ekran üç kez ters döner, yeşil LED yanar ve bip çalar.
- `UP`/`DOWN`: çağrılar (6 adede kadar), `1`: hoparlör, `2`: temizle, `EXIT`: çık.

> [!WARNING]
> Gerçek bir **DISTRESS (imdat)** çağrısı görürseniz bu genellikle zaten sahil istasyonları
> tarafından alınmıştır. Yine de konum ve saat bilgisiyle **112**'ye veya Kıyı Emniyeti'ne
> bildirebilirsiniz. Kanal 70'te **asla gönderim yapmayın**.

## 11.6 Radyosondalar ve konum

Radyosondalar için genel bilgi: [7.8](07-frekans-rehberi.md#78-400470-mhz-sondalar-işaretçiler-70-cm-pmr-lpd).
Ortak ayar: **FM, WIDE**, sondanın frekansı (SondeHub gibi sitelerden bakın).

| Uygulama | Sonda tipi | Gösterilenler |
|----------|------------|---------------|
| **Sonde RS41** | Vaisala RS41 (4800 bit/s GFSK) | Seri numarası, konum, irtifa, dikey/yatay hız, yön, sondanın pil gerilimi |
| **Sonde M10** | Meteomodem M10 | Seri no, konum, irtifa, sıcaklık, nem, hızlar, yön |
| **Sonde M20** | Meteomodem M20 | Seri no, konum, irtifa, dikey/yatay hız, yön, sıcaklık, nem |
| **Sonde MRZ** | (Bu depoda kaynak kodu yok) | — |

**Ortak tuşlar**

| Tuş | İşlev |
|-----|-------|
| `1` | Hoparlör |
| `2` / `F` + `2` | Frekansı ±5 kHz kaydır (±50 kHz'e kadar) |
| `3` / `F` + `3` | Zayıflatıcı ileri / geri |
| `4` | VFO frekansına dön |
| `5` | Çözme bipi aç/kapat |
| `EXIT` | Çık |

- Her geçerli çerçevede yeşil LED iki kez yanıp söner.
- Sonda **çok yakınsa** (fırlatma noktasına yakın veya yere inmiş) zayıflatıcıyı artırın.
  M20'nin varsayılan zayıflatıcısı 27 dB'dir.
- RS41 uygulaması hata düzeltme yapmaz; **temiz bir sinyal** gerekir.

### Düşen sondayı bulmak

1. Sonda uygulamasıyla son konumu alın. Sonda alçaldıkça yer seviyesindeki menzil azalır;
   son konumlar en değerli olanlardır.
2. **GeoNav** ile bu konuma yön ve mesafeyi görün.
3. Yakına geldiğinizde **Sig Finder** ile sinyalin yönünü bulun.
4. Özel arazilere izinsiz girmeyin. Sondanın üzerindeki etikette bulana yönelik bilgiler olabilir.

## 11.7 Acil durum işaretçileri

### EPIRB 406

**COSPAS-SARSAT 406 MHz** imdat işaretçilerinin (EPIRB, ELT, PLB) birinci nesil mesajlarını çözer:
15 haneli onaltılık kimlik, ülke, protokol, konum, BCH hata kontrolü.

1. VFO: **406,031 MHz** (gerçek işaretçiler), **FM, WIDE**.
2. Ortamda patlama yokken **EPIRB 406**'yı açın; gürültü tabanı açılışta ölçülür.
3. Çözülen her mesaj, hoparlör kapalı olsa bile **üç bip** çalar.

| Tuş | İşlev |
|-----|-------|
| `UP` / `DOWN` | Kaydır / mesajlar arasında gez (5 mesaj) |
| `*` | Normal ↔ sıkışık |
| `4` / `6` | VFO'dan −5 / +5 kHz kaydır (±50 kHz) |
| `5` | VFO frekansına dön |
| `1` | Hoparlör |
| `MENU` | Mesajları ve sayaçları temizle |
| `EXIT` | Çık |

Alt satır: `FR` (tam çerçeve), `ER` (başarısız yakalama), son hata (`NS`: senkron yok,
`CUT`: eksik mesaj), `BCH OK/OK`. `SELF-TEST` işaretli mesajlar işaretçinin kendi testidir.

> [!WARNING]
> `SELF-TEST` olmayan bir mesaj **gerçek bir imdat** olabilir. Kimliği, konumu ve saati not
> edip **112**'ye bildirin. **Scan406** uygulaması (bu depoda kaynak kodu yok) 406 MHz
> bandını taramak içindir.

### Sig Finder

121,5 / 243 MHz işaretçilerin yönünü bulmak için: bkz. [11.3](#113-radyo-araçları).

## 11.8 Diğer veri modları: POCSAG, SSTV

### POCSAG RX (çağrı cihazı)

**POCSAG** çağrı cihazı mesajlarını 1200 ve 512 baud'da çözer. Amatör **DAPNET** ağı bu biçimi kullanır.

1. VFO: **439,9875 MHz** (DAPNET; kapsama alanını hampager.de'den kontrol edin), **FM, WIDE**.
2. **POCSAG RX**'i açın. Yeni mesaj gelince arka ışık yanar, yeşil LED iki kez yanıp söner.

| Tuş | İşlev |
|-----|-------|
| `UP` / `DOWN` | Metni kaydır / mesajlar arasında gez (10 mesaj) |
| `*` | Normal ↔ sıkışık (tam 80 karakterlik mesaj) |
| `1` | Hoparlör |
| `2` | Temizle |
| `3` | Teşhis satırı (önsöz hızı, sayaçlar) |
| `4` | Metinsiz (yalnızca ton) mesajları da sakla |
| `EXIT` | Çık |

Okunamayan karakterler `?` olarak gösterilir. 2400 baud tanınır ama çözülemez.

> [!IMPORTANT]
> Amatör DAPNET dışındaki çağrı cihazı sistemleri (hastane, itfaiye, ticari) özel
> haberleşmedir. Bu mesajları okumak ve aktarmak yasal sorun doğurabilir.

### SSTV

**Durağan resim** alır ve telsizin açılış logosunu resim olarak gönderir. 14 mod destekler:
Robot 36/72, Martin M1/M2, Scottie S1/S2/DX, PD50/90/120/160/180/240/290. ISS genellikle
**PD120** veya **PD180** gönderir.

1. VFO: **FM**. ISS için **145,800 MHz**, geniş FM, duyurulmuş bir ARISS SSTV etkinliği sırasında.
2. **SSTV**'yi açın: hemen dinlemeye başlar. Bilinen bir VIS kodu duyunca resim satır satır çizilir.

| Tuş | İşlev |
|-----|-------|
| `MENU` | Açılış logosunu seçili modda **gönder** |
| `PTT` | **Bilerek yok sayılır** (yanlışlıkla gönderimi önlemek için) |
| `1` / `F` + `1` | Gönderim modu: sonraki / önceki |
| `2` | Çizim: `1-BIT` (keskin) / `DITHER` (fotoğraflar için) |
| `3` | Hoparlör |
| `4` | Resim ↔ bilgi ekranı |
| `EXIT` | Alımı/gönderimi iptal et, sonra resimden, sonra uygulamadan çık |

- Son alınan resim (yarım bile olsa) kaydedilir; bir sonraki açılışta `4` ile görülür.
- Uzun modlar vericiyi **dakikalarca** açık tutar (Scottie DX 269 s, PD290 289 s). Düşük güç kullanın.

## 11.9 Mors (CW) uygulamaları

Mors kodunun temelleri: [4.5](04-modulasyon-ve-sinyal-turleri.md#45-cw-mors-kodu).

### CW Decode

Gelen CW sinyalini RSSI zarfından çözüp metne çevirir. Sinyali duymak için telsiz 700 Hz
aşağıda USB modunda dinler. Otomatik yakalama yaklaşık **8–22 WPM**'dir.

1. Sessiz bir 2 m veya 70 cm frekansına geçin, **CW Decode**'u açın.
2. `KEEP CHANNEL QUIET` yazarken kanal sessiz kalmalıdır (sessiz kanal kalibrasyonu).
3. Karşı istasyon önce `VVV` gönderirse zamanlama oturur.

| Tuş | İşlev |
|-----|-------|
| `UP` / `DOWN` | Geçmişi kaydır |
| `0` | CW sesini aç/kapat |
| `*` | Normal ↔ sıkışık yazı |
| `1` / `F` + `1` | Algılama eşiğini artır / azalt |
| `2` / `F` + `2` | WPM eğilimini artır / azalt |
| `3` | AGC aç/kapat (sonra yeniden kalibrasyon) |
| `4` | Sessiz kanal kalibrasyonunu tekrarla |
| `5` | Geçmişi temizle |

### CW Keyer

Geçerli TX VFO'sunda **elle anahtarlanan taşıyıcı (A1A)** gönderir. Anahtar olarak `PTT`
ve yan tuşlar kullanılır. VFO **FM**'de olmalıdır. Karşı tarafın tonu duyması için CW veya SSB
alıcısı gerekir; FM alıcı yalnızca squelch'in açılıp kapandığını duyar.

| Tuş | İşlev |
|-----|-------|
| `PTT` | Düz anahtar (her modda) |
| `SIDE1` / `SIDE2` | Düz anahtar veya nokta/çizgi (moda göre) |
| `1` | `STRAIGHT` (düz anahtar) / `PADDLE` (otomatik nokta-çizgi) |
| `2` | Hız (5–60 WPM, varsayılan 18) |
| `3` | Alım ve yan ton (300–900 Hz, varsayılan 700) |
| `4` | Yarı break-in gecikmesi (250–1500 ms) |
| `5` | Nokta/çizgi kontaklarını takas et |
| `6` | Kristal düzeltmesi (`XTAL`, −50 … +50 adım, varsayılan +14 = +2,69 ppm) |
| `F` + `2`/`3`/`4`/`6` | İlgili ayarı azalt |
| `0` | CW alım sesini aç/kapat |
| `UP` / `DOWN` | 100 Hz adımla ince ayar (±50 kHz) |
| `MENU` | Yardım sayfası |
| `EXIT` | Çık |

- Yasak frekansta, düşük/yüksek pilde veya VFO FM değilse gönderim reddedilir (`TX OFF`).
- **Takılı anahtar koruması**: Kesintisiz taşıyıcı 10 saniyeyle sınırlıdır.

### CW USB

CW Keyer'ın, **USB-C konnektörüne bağlanan** bir Mors anahtarı veya pedal (paddle) ile çalışan
türüdür. Ayarları CW Keyer ile aynıdır; ayrıca `8` ile pedal modu: `AUTO`, `IAMB A`, `IAMB B`.

- **Her açılışta verici kilitlidir** (durum çubuğunda asma kilit). Kilidi açmak için:
  bütün kontakları bırakın, uç (tip) kontağı **5 saniye** kapalı tutun, onay işareti
  görününce bırakın.
- Ayarlar ilk kurulumda varsayılandır; `XTAL` değerini CW Keyer ile aynı yapın.

### CW Trainer, CW Mem, CW Mem Edit, CW QSO Auto

v6.3.0 uygulama paketinde bulunan ek CW uygulamalarıdır (bu depoda kaynak kodları yok):
Mors öğrenme (**CW Trainer**), hafızalı mesaj gönderme (**CW Mem**, **CW Mem Edit**) ve
otomatik CW görüşmesi (**CW QSO Auto**). Ayrıntılar için uygulamaların kendi yardım ekranlarına
ve proje sayfasına bakın.

## 11.10 Ölçüm ve yardımcı araçlar

### AF Scope (ses osiloskobu ve akort göstergesi)

Demodüle edilmiş alım sesini **zamana göre** gösterir. `MENU` ile AF Spectro'ya geçilir.

| Görünüm | Ne gösterir? |
|---------|--------------|
| **SCOPE** | Osiloskop izi; frekans sayacı (`1750Hz` veya FSK için `1227 / 2079Hz`), tepeden tepeye ve DC |
| **TUNE** | Sabit bir tonun frekansı büyük rakamlarla ve en yakın bilinen tona göre bir ibre (`1750 CALL TONE -2`) |

| Tuş | İşlev |
|-----|-------|
| `MENU` | SCOPE → TUNE → AF Spectro |
| `UP` / `DOWN` | SCOPE: zaman tabanı (0,8–13 ms/bölme). TUNE: ibre aralığı |
| `*` (basılı) | Ekranı dondur |
| `1` | Ses yolu: STD / RAW |
| `2` | Hoparlör |
| `3` | Kazanç: AUTO, ×1 … ×16 |
| `4` | Tetik kenarı: yükselen / düşen |
| `5` | Kalıcılık (izler üst üste) |
| `0` | Kalıcılığı temizle |
| `EXIT` | Çık |

**Kullanım alanları**: CTCSS/1750 Hz/DTMF tonunu ölçmek, bir APRS paketinin tonlarını
görmek, kırpılma (clipping) tespit etmek, CW ton yüksekliğini okumak.

### AF Spectro (ses spektrumu)

Demodüle edilmiş sesin **frekans içeriğini** gösterir: spektrum (tepe tutmalı) ve sonogram (şelale).
İki ana tepeyi ve aralarındaki seviye farkını (twist) ölçer.

| Tuş | İşlev |
|-----|-------|
| `MENU` | SPECTRO → SONO → AF Scope |
| `UP` / `DOWN` | Ölçek aralığı: 80 / 60 / 40 dB |
| `*` (basılı) | Dondur |
| `1` | STD / RAW |
| `2` | Hoparlör |
| `3` | Örnekleme hızı: 9,6 / 19,2 / 38,4 kHz |
| `0` | Temizle |
| `EXIT` | Çık |

**APRS TX twist ayarı**: İkinci bir telsizde AF Spectro'yu açın, APRS TX'ten paket gönderin.
Ekranda `1200 / 2200Hz  TW -5.1dB` gibi bir değer görünür. APRS TX'te `2` tuşuyla bu değeri
0 dB'ye yaklaştırın.

### Resistor

Direnç renk kodu hesaplayıcısı (3, 4, 5, 6 bantlı; IEC 60062:2016 tabloları).

| Tuş | İşlev |
|-----|-------|
| Yön tuşları | Bant seç |
| `*` / `F` + `*` | Seçili bandın rengi: sonraki / önceki |
| `0`–`9` | Bandı o rakamın rengine ayarla ve ilerle (`4` `7` `2` → 4,7 kΩ) |
| `MENU` | Bant sayısı: 3 → 4 → 5 → 6 |
| `EXIT` | Çık |

### System Info

Sistem bilgisi: mikrodenetleyici kimliği, saat ayarları, flash ve RAM, ADC (iç sıcaklık, referans
gerilimi), kanal kullanımı vb. Satırlar `UP`/`DOWN` ile kaydırılır, `EXIT` ile çıkılır.

### Flash Map

Harici flash'ın fiziksel haritası: firmware yuvaları, yapılandırma bankaları, uygulama yuvaları,
çalışan yuva ve etkin bölgeler (`LIVE`). Yalnızca okur, hiçbir şeyi değiştirmez.
`MENU`: üstteki bölgenin içeriğini göster (`*` = onaltılık ↔ metin, `UP`/`DOWN` = sayfa,
`0`–`9` = bölgenin onda biri kadar atla).

### QR Map

Bu depoda kaynak kodu bulunmayan, v6.3.0 paketindeki bir uygulamadır. Adından konum
bilgisini QR kodu olarak göstermeye yönelik olduğu anlaşılmaktadır; ayrıntılar için proje sayfasına bakın.

## 11.11 Oyunlar ve demolar

Telsizin 128 × 64 ekranını ve tuşlarını kullanan, radyo gönderimi yapmayan uygulamalar:

| Uygulama | Tür | Temel tuşlar |
|----------|-----|--------------|
| **Breakout** | Tuğla kırma | `MENU`: başla / duraklat, `UP`/`4`: sola, `DOWN`/`0`: sağa |
| **Tetris** | Blok yerleştirme | `4`/`6` veya yön tuşları: hareket, `MENU`/`2`: döndür, `8`: hızlı düşür |
| **Snake** | Yılan | `2`/`4`/`6`/`8`: yön |
| **Space Impact** | Uzay nişancı | `2`/`8` veya `UP`/`DOWN`: hareket, `5`/`MENU`: ateş |
| **Rapid Roll** | Platform | `4`/`6` veya `UP`/`DOWN`: yuvarlan, `F`: duraklat |
| **Minesweeper** | Mayın tarlası | `1`–`9`: imleç (8 yön) |
| **Sokoban** | Kutu itme bulmacası (24 bölüm) | `2`/`4`/`6`/`8`: yön, `*`: geri al, `0` `0`: bölümü baştan başlat, `3`/`9`: bölüm |
| **Hell Maze** | Birinci şahıs labirent | `2`/`8`: ileri/geri, `4`/`6`: dön, `1`/`3`: yana, `PTT`/`5`: ateş, `MENU`: yardım |
| **Cube3D** | 3B şekiller | `1`–`9`: şekil, `*`: sonraki, `UP`/`DOWN`: hız, `F` + `UP`/`DOWN`: yakınlaştır, `F` + `*`: tel/katı |
| **Plasma** | Grafik demo | `1`–`9`: sahne, `UP`/`DOWN`: hız, `*`: stil, `0`: ters |

Oyunlarda `PTT` gönderim yapmaz.

## 11.12 Hangi iş için hangi uygulama?

| Amaç | Uygulama | Frekans / ayar |
|------|----------|----------------|
| Yakındaki APRS istasyonlarını görmek | APRS RX | 144,800 FM |
| Konumumu APRS ağına göndermek (belgeli) | APRS Edit → APRS TX | 144,800 FM |
| Telefonda APRS haritası | KISS TNC + APRSdroid | 144,800 FM |
| ISS'ten resim almak | SSTV | 145,800 FM (etkinlikte) |
| Uçak veri mesajları | ACARS RX | 131,525 / 131,725 AM |
| Gemi konumları | AIS RX | 161,975 / 162,025 FM |
| Deniz imdat/DSC çağrıları | ATIS DSC RX | 156,525 FM |
| Meteoroloji balonu takibi | Sonde RS41 / M10 / M20, GeoNav | 400–406 FM WIDE |
| İmdat işaretçisi tespiti | EPIRB 406, Sig Finder | 406,031 FM / 121,5 AM |
| Tilki avı | Fox Hunt, Sig Finder (bulmak); Beacon (vermek) | 2 m |
| Mors öğrenmek / çözmek | CW Trainer, CW Decode | — |
| Bir tonu veya sinyali incelemek | AF Scope, AF Spectro | Herhangi |
| Bandı görsel keşfetmek | Spectrum3D (veya `F` + `5`) | Herhangi |
| Telsizden telsize kanal göndermek | Beam | Ortak frekans |
| Amatör çağrı cihazı mesajları | POCSAG RX | 439,9875 FM |

---

[← Önceki: Menü referansı](10-menu-referansi.md) · [İçindekiler](README.md) · [Sonraki: Uygulamalı senaryolar →](12-uygulamali-senaryolar.md)
