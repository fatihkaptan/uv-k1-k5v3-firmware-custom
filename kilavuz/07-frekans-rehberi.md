# 7. Frekans Rehberi: Spektrumda Ne Nerede?

[← Önceki: Amatör telsizcilik](06-amator-telsizcilik.md) · [İçindekiler](README.md) · [Sonraki: Cihaz donanımı ve ekran →](08-cihaz-donanimi-ve-ekran.md)

Bu bölüm, telsizin alabildiği **18 MHz – 1,3 GHz** aralığında hangi frekansta neyin
bulunduğunu, neyin dinlenebileceğini ve hangi ayarların gerektiğini gösterir.

> [!WARNING]
> **Dinlemek ile göndermek aynı şey değildir.** Bu listedeki frekansların büyük
> çoğunluğunda **gönderim yapmanız yasaktır**. Belgeli bir amatör bile yalnızca amatör
> bantlarda gönderim yapabilir. Kamuya açık olmayan haberleşmelerin içeriğini kaydetmek,
> başkalarına aktarmak veya yayımlamak yasal sorun doğurur.

> [!NOTE]
> Frekansların bir kısmı bölgeden bölgeye değişir. "Doğrulayın" işaretli bilgileri
> kullanmadan önce güncel resmî kaynaklardan kontrol edin.

## İçindekiler

1. [Telsizin alım ve gönderim aralıkları](#71-telsizin-alım-ve-gönderim-aralıkları)
2. [Spektrum haritası (özet)](#72-spektrum-haritası-özet)
3. [HF'nin üst kısmı: 18–30 MHz](#73-hfnin-üst-kısmı-1830-mhz)
4. [VHF alçak bant ve FM yayın: 30–108 MHz](#74-vhf-alçak-bant-ve-fm-yayın-30108-mhz)
5. [Havacılık bandı: 108–137 MHz](#75-havacılık-bandı-108137-mhz)
6. [137–174 MHz: uydular, 2 m, deniz, profesyonel](#76-137174-mhz-uydular-2-m-deniz-profesyonel)
7. [174–400 MHz](#77-174400-mhz)
8. [400–470 MHz: sondalar, işaretçiler, 70 cm, PMR, LPD](#78-400470-mhz-sondalar-işaretçiler-70-cm-pmr-lpd)
9. [470 MHz – 1,3 GHz](#79-470-mhz--13-ghz)
10. [Kanal tabloları: PMR446, denizcilik, LPD433](#710-kanal-tabloları-pmr446-denizcilik-lpd433)
11. [Hızlı başvuru: ilk denemeler için frekanslar](#711-hızlı-başvuru-ilk-denemeler-için-frekanslar)

---

## 7.1 Telsizin alım ve gönderim aralıkları

### Alım (RX)

Firmware'in frekans tablosu (`App/frequencies.c`, geniş alım açık):

| Bant | Aralık |
|------|--------|
| Bant 1 | 18 – 108 MHz |
| Bant 2 | 108 – 137 MHz |
| Bant 3 | 137 – 174 MHz |
| Bant 4 | 174 – 350 MHz |
| Bant 5 | 350 – 400 MHz (gizli menüde `350 En` açıksa) |
| Bant 6 | 400 – 470 MHz |
| Bant 7 | 470 – 1300 MHz |

- RF entegresi **630–840 MHz arasında çalışmaz**. Bu aralıktaki frekanslar reddedilir.
- `F` + `1` bantlar arasında geçiş yapar.
- **Bant uçlarında hassasiyet düşer.** Telsizin anteni ve ön katı 2 m ve 70 cm için
  ayarlıdır. 18–50 MHz veya 1 GHz üstünde "duyabilmek" ile "iyi duymak" farklı şeylerdir.

### Gönderim (TX): `F Lock` ayarına göre

Gönderim izni, gizli menüdeki **`F Lock`** ayarına bağlıdır:

| `F Lock` seçeneği | Gönderime izin verilen aralıklar |
|-------------------|-----------------------------------|
| `DEFAULT+ 137-174 400-470` | 137–350 MHz, 350–400 MHz (`350 En` açıksa), 400–600 MHz. **Çok geniş!** |
| `FCC HAM 144-148 420-450` | 144–148, 420–450 MHz (ABD) |
| `CA HAM 144-148 430-450` | 144–148, 430–450 MHz (Kanada) |
| **`CE HAM 144-146 430-440`** | **144–146, 430–440 MHz (Avrupa / Türkiye için önerilen)** |
| `GB HAM 144-148 430-440` | 144–148, 430–440 MHz (Birleşik Krallık) |
| `137-174 400-430` | 137–174, 400–430 MHz |
| `137-174 400-438` | 137–174, 400–438 MHz |
| `PMR 446` | 446,00625–446,19375 MHz |
| `GMRS FRS MURS` | ABD'ye özgü kişisel telsiz hizmetleri |
| `DISABLE ALL` | **Hiçbir frekansta gönderim yok** (yalnızca alıcı) |
| `UNLOCK ALL` | **Telsizin desteklediği her frekansta.** Önerilmez. |

> [!CAUTION]
> Varsayılan `DEFAULT+` ayarı, telsizin **havacılık dışındaki birçok kamu ve
> profesyonel banda** gönderim yapmasına izin verir. Yanlışlıkla `PTT`'ye basmak
> başka bir hizmeti bozabilir ve yasal sonuç doğurur.
>
> - **Belgeliyseniz**: `CE HAM` seçin.
> - **Belgeniz yoksa**: `DISABLE ALL` seçin. Telsiz böylece tamamen güvenli bir alıcıya dönüşür.

## 7.2 Spektrum haritası (özet)

```
 MHz  18    30      50   88  108 118  137 144 146    174        225       400 406 430 440 470           630···840   1090   1240 1300
      ├─HF──┤        ├6m┤ ├FM┤ ├VOR┤├HAVA┤├M┤├2m┤├DENİZ/PROF┤├DAB┤├ASKERİ HAVA┤├S┤├E┤├70cm┤├PROF┤├DVB-T TV┤ ✗ ├868├GSM├ADS-B├23cm┤
                                       └Uydu 137┘                             └Sonda └EPIRB
```

| Aralık | Hizmet | Mod | Dinlemeye değer mi? |
|--------|--------|-----|---------------------|
| 18–30 MHz | HF amatör, CB | SSB, AM, FM | Kısa antenle zayıf; yalnızca güçlü sinyaller |
| 50–52 MHz | 6 m amatör | SSB, FM | Yaz aylarında sporadik E ile |
| 87,5–108 MHz | **FM yayın radyosu** | WFM | **Evet**, `F` + `0` |
| 108–117,975 MHz | Hava seyrüsefer (VOR, ILS) | AM + Mors kimliği | Mors kimliklerini duymak ilginç |
| 118–136,975 MHz | **Hava trafik sesli haberleşme** | **AM** | **Evet**, `Mode` → `AM` |
| 137–138 MHz | Meteoroloji uyduları | Dijital | Duyulur, çözülemez |
| **144–146 MHz** | **2 m amatör** | FM, SSB, CW, dijital | **Evet** |
| 146–174 MHz | Profesyonel telsiz, deniz VHF | FM (çoğu dar), dijital | Deniz kanalları evet |
| 174–230 MHz | DAB+ dijital radyo | Dijital | Çözülemez |
| 225–400 MHz | Askeri havacılık, uydu, TETRA | AM, dijital | Çoğu dijital/şifreli |
| 400,15–406 MHz | **Radyosondalar** | FSK, GFSK | **Evet**, sonda uygulamaları |
| 406,0–406,1 MHz | COSPAS-SARSAT imdat işaretçileri | BPSK | Nadiren (umarız) |
| **430–440 MHz** | **70 cm amatör** | FM, SSB, dijital, uydu | **Evet** |
| 433,05–434,79 MHz | LPD433 / ISM | FM, OOK | Kumandalar, sensörler |
| 446,0–446,2 MHz | **PMR446** | Dar FM, dijital | **Evet** |
| 450–470 MHz | Profesyonel telsiz | FM, dijital | Kısmen |
| 470–630 MHz | DVB-T televizyon | Dijital | Çözülemez |
| 630–840 MHz | — | — | **Telsiz alamaz** |
| 863–870 MHz | ISM/SRD 868 (LoRa, Meshtastic) | Dijital | Çözülemez |
| 880–960 MHz | GSM / LTE 900 | Dijital | Çözülemez |
| 1030 / 1090 MHz | Uçak transponderi, ADS-B | Darbe | Duyulur, çözülemez |
| 1240–1300 MHz | 23 cm amatör | FM, SSB, ATV | Zayıf (anten uygun değil) |

## 7.3 HF'nin üst kısmı: 18–30 MHz

| Frekans | Hizmet | Not |
|---------|--------|-----|
| 18,068–18,168 MHz | 17 m amatör | SSB/CW. Bu telsizde SSB yalnızca alım ve deneysel. |
| 21,000–21,450 MHz | 15 m amatör | |
| 24,890–24,990 MHz | 12 m amatör | |
| 26,965–27,405 MHz | **CB (Sivil Bant), 40 kanal** | AM/FM. Kanal 9 (27,065) acil, kanal 19 (27,185) yol kanalı olarak bilinir |
| 28,000–29,700 MHz | **10 m amatör** | 29,600 MHz FM simpleks çağrı. Güneş aktivitesi yüksekken dünya çapında açılır |

> Bu bantlarda dalga boyu 10–16 m'dir; telsizin 15–20 cm'lik anteni çok verimsizdir.
> Yalnızca yakın ve güçlü sinyalleri duymayı bekleyin. Uzun bir tel anten (birkaç metre)
> bağlamak alımı belirgin şekilde iyileştirir.

## 7.4 VHF alçak bant ve FM yayın: 30–108 MHz

| Frekans | Hizmet | Not |
|---------|--------|-----|
| 50–52 MHz | 6 m amatör ("sihirli bant") | Kullanım koşulları için BTK'ya bakın. Yazın sporadik E ile 1000+ km açılır. |
| 87,5–108 MHz | **FM yayın radyosu** | `F` + `0` ile ayrı FM alıcısı (BK1080). Yayın FM'i ana alıcının `FM` moduyla dinlenmez, çünkü ±75 kHz sapmalı geniş FM'dir. |

### FM radyonun kullanımı (`F` + `0`)

- `0`–`9`: Frekans girme (VFO) veya kanal numarası (hafıza)
- `UP` / `DOWN`: Frekansı veya kanalı değiştirme
- `*`: Elle tarama (bir sonraki istasyonu bulur)
- `F` + `*`: Otomatik tarama; bulduğu istasyonları **48 FM kanalına** kaydeder
- `MENU`: Kaydet (VFO modunda) veya sil (kanal modunda)
- `F` + `3`: VFO ↔ kanal modu
- `F` + `0` veya `EXIT`: Çıkış

## 7.5 Havacılık bandı: 108–137 MHz

| Frekans | Hizmet | Mod |
|---------|--------|-----|
| 108,000–117,975 MHz | **VOR / ILS** seyrüsefer işaretçileri | AM. Her istasyon kimliğini **Mors kodunda** tekrarlar |
| 118,000–121,400 MHz | Kule, yaklaşma, saha | AM |
| **121,500 MHz** | **Uluslararası havacılık acil durum frekansı** | AM. Burada gönderim **kesinlikle yasaktır** |
| 121,600–123,000 MHz | Yer hizmetleri, kule, ATIS | AM |
| 123,100 MHz | Arama-kurtarma (SAR) | AM |
| 123,450 MHz | Pilotlar arası (gayriresmî) | AM |
| 123,500–136,975 MHz | Bölge kontrol, yaklaşma, ATIS, operasyon | AM |
| 131,525 / 131,725 / 131,825 MHz | **ACARS** veri (Avrupa) | AM-MSK (ACARS RX uygulaması) |

**Ayarlar**

1. `Mode` → **`AM`**.
2. Adım: **25 kHz** veya **8,33 kHz** (Avrupa'da birçok frekans 8,33 kHz ızgarasına geçmiştir).
3. Squelch'i 3–5 civarına ayarlayın. Havacılık sinyalleri kısa ve aralıklıdır.
4. Havalimanınızın kule, yaklaşma ve ATIS frekanslarını havacılık yayınlarından
   (AIP) veya meraklı topluluklardan öğrenin.
5. **ATIS** (Automatic Terminal Information Service, otomatik meydan bilgisi) yayınları
   sürekli tekrarlanan hava durumu ve pist bilgisidir. Denemek için en kolay sinyaldir.

> [!NOTE]
> Uçaklar yüksekte olduğu için **uçağın sesi** 100–200 km uzaktan duyulabilir. **Kule**
> ise yerde olduğundan yalnızca havalimanına yakınsanız duyulur.

## 7.6 137–174 MHz: uydular, 2 m, deniz, profesyonel

### 137–138 MHz: Meteoroloji uyduları

- Bu bant alçak yörüngeli meteoroloji uydularına ayrılmıştır.
- NOAA'nın analog (APT) görüntü yayınlayan eski uyduları **2025 itibarıyla hizmetten
  çıkarılmıştır** (doğrulayın).
- Rus **Meteor-M** uyduları **dijital (LRPT)** yayın yapar. Bu telsizle duyulur, çözülemez.

### 144–146 MHz: 2 m amatör bandı

Ayrıntılı bant planı [6. bölümde](06-amator-telsizcilik.md#65-bant-planları). Öne çıkanlar:

| Frekans | Kullanım |
|---------|----------|
| 144,050 MHz | CW çağrı |
| 144,300 MHz | SSB çağrı |
| 144,500 MHz | SSTV çağrı |
| **144,800 MHz** | **APRS (Avrupa)** |
| 145,000–145,1875 MHz | Röle girişleri |
| 145,200–145,5875 MHz | FM simpleks |
| **145,500 MHz** | **FM simpleks çağrı (V40)** |
| 145,600–145,7875 MHz | **Röle çıkışları** (dinlediğiniz frekans) |
| **145,800 MHz** | **ISS ses / SSTV iniş** |
| 145,825 MHz | ISS APRS digipeater |
| 145,800–146,000 MHz | Uydular |

### 146–174 MHz: Profesyonel telsiz ve denizcilik

- **Profesyonel telsiz (PMR)**: Belediyeler, güvenlik şirketleri, inşaat, ulaşım, sanayi.
  Çoğu **dar FM** (`NARROW`) veya **dijital (DMR)** kullanır. **Dinleme hoş görülse bile
  içeriği aktarmak yasaktır.**
- **Denizcilik VHF (156–162,025 MHz)**: Gemiler, limanlar, sahil istasyonları. Geniş FM
  (`WIDE`), 25 kHz kanallar. Kanal tablosu [7.10'da](#710-kanal-tabloları-pmr446-denizcilik-lpd433).

| Frekans | Kanal | Kullanım |
|---------|-------|----------|
| **156,800 MHz** | **16** | **Denizcilik imdat, emniyet ve çağrı kanalı** |
| 156,525 MHz | 70 | **DSC** dijital seçmeli çağrı (ATIS DSC RX uygulaması). **Ses yasak.** |
| 156,650 MHz | 13 | Köprüden köprüye seyir emniyeti |
| 156,300 MHz | 06 | Gemiler arası, arama-kurtarma |
| **161,975 MHz** | AIS 1 | Gemi otomatik kimlik sistemi (AIS RX) |
| **162,025 MHz** | AIS 2 | Gemi otomatik kimlik sistemi |

> [!CAUTION]
> Denizcilik kanallarında, özellikle **kanal 16 ve 70**'te gönderim yapmak yalnızca
> yetkili deniz telsizlerine aittir. Bu kanallarda yapılacak yanlış bir gönderim
> gerçek bir arama-kurtarma operasyonunu tetikleyebilir.

## 7.7 174–400 MHz

| Frekans | Hizmet | Not |
|---------|--------|-----|
| 174–230 MHz | **DAB+** dijital radyo (Bant III) | Bazı şehirlerde yayın var (doğrulayın). Bu telsizle çözülemez. |
| 225–400 MHz | **Askeri havacılık** (UHF AM) ve askeri uydular | Çoğunlukla şifreli veya dijital |
| **243,000 MHz** | Askeri havacılık acil durum frekansı | 121,5 MHz'in ikinci harmoniği. Eski işaretçiler burada da yayın yapar (Sig Finder). |
| 380–400 MHz | **TETRA** (birçok ülkede acil servisler) | Dijital, şifreli. Sürekli "vızzz" sesi |

## 7.8 400–470 MHz: sondalar, işaretçiler, 70 cm, PMR, LPD

### 400,15–406 MHz: Radyosondalar

- **Radyosonda**, meteoroloji balonlarına bağlanan küçük vericidir. Yükselirken
  sıcaklık, nem, basınç ve GPS konumu gönderir. Yaklaşık 30–35 km'ye çıkar, balon patlar,
  paraşütle iner.
- Dünyada balonlar genellikle **günde iki kez, 00 ve 12 UTC civarında** atılır. Türkiye'de
  Meteoroloji Genel Müdürlüğü'nün belirli istasyonlarından atılır (istasyonları ve saatleri doğrulayın).
- Hangi sondanın hangi frekansta olduğunu **SondeHub** gibi canlı takip sitelerinden
  öğrenebilirsiniz.
- **Ayar**: `FM`, **`WIDE`**, sonda frekansı. Ardından `F` + `7` → **Sonde RS41**,
  **Sonde M10** veya **Sonde M20** (sondanın tipine göre).

### 406,0–406,1 MHz: COSPAS-SARSAT işaretçileri

- **EPIRB** (gemi), **ELT** (uçak) ve **PLB** (kişisel) imdat işaretçileri, kaza anında bu
  bantta uydulara konum gönderir. Her ~50 saniyede bir, yarım saniyelik bir patlama yapar.
- Çoğu işaretçi aynı anda **121,5 MHz**'de sürekli bir yön bulma sinyali (homer) yayınlar.
- **EPIRB 406** uygulaması bu mesajları çözer; **Sig Finder** 121,5 MHz sinyalinin yönünü bulur.

> [!WARNING]
> Gerçek bir işaretçi sinyali alırsanız bu bir **imdat çağrısı** olabilir. Konumunuzu,
> saati ve gördüğünüz kimliği (15 haneli onaltılık ID) not edip **112**'ye bildirin.
> Kendiniz aramaya çıkmayın.

### 430–440 MHz: 70 cm amatör bandı

| Frekans | Kullanım |
|---------|----------|
| 432,050 MHz | CW çağrı |
| 432,200 MHz | SSB çağrı |
| **433,500 MHz** | **FM simpleks çağrı (U280)** |
| 435–438 MHz | **Uydu hizmeti** (iniş frekansları) |
| 438–440 MHz | Röleler (bazı ülkelerde), dijital, ATV |
| **439,9875 MHz** | **DAPNET** amatör çağrı cihazı ağı (POCSAG RX) |

### 433,05–434,79 MHz: LPD433 / ISM

- Lisanssız düşük güçlü cihazlar: **araç ve garaj kumandaları**, **kablosuz hava
  istasyonu sensörleri**, kapı zilleri, bazı LPD telsizler (69 kanal, 10 mW).
- Amatör 70 cm bandıyla **çakışır**. Bu yüzden 433–435 MHz'de kısa "tık" ve
  "brrt" sesleri duymanız normaldir.
- Uygulama belgelerinde sık geçen **433,650 MHz**, Flipper Zero gibi test cihazlarıyla
  masa başı denemeler için kullanılan frekanstır.

### 446,0–446,2 MHz: PMR446

- Avrupa'da **lisanssız** kişisel telsiz bandı. 16 analog kanal, 12,5 kHz aralık, **dar FM**.
- Yalnızca **tip onaylı, sabit antenli ve en fazla 0,5 W ERP** cihazlarla kullanılabilir.
  **UV-K5 / UV-K1 bu şartları karşılamaz**, PMR446'da gönderim için uygun değildir.
- Dinlemek için kanal tablosu [7.10'da](#710-kanal-tabloları-pmr446-denizcilik-lpd433).
  `W/N` → `NARROW` seçin. Kullanıcılar genellikle CTCSS/DCS kodları kullanır;
  `RxCTCS`'yi kapalı tutarsanız herkesi duyarsınız.

### 450–470 MHz: Profesyonel telsiz

Taksi, güvenlik, otel, AVM, fabrika, belediye gibi kullanıcılar. Çoğu dar FM veya DMR.
Dinleme içeriği **aktarılamaz**.

## 7.9 470 MHz – 1,3 GHz

| Frekans | Hizmet | Not |
|---------|--------|-----|
| 470–630 MHz | **DVB-T** dijital karasal TV | Spektrumda 8 MHz genişliğinde düz platolar |
| **630–840 MHz** | — | **RF entegresi bu aralıkta çalışmaz** |
| 863–870 MHz | **ISM/SRD 868**: LoRa, Meshtastic (869,525 MHz), alarm sistemleri, akıllı sayaçlar | Kısa süpürmeler (chirp) ve patlamalar |
| 880–960 MHz | **GSM / LTE 900** mobil telefon | Sürekli dijital gürültü |
| 960–1215 MHz | Havacılık seyrüsefer (DME, TACAN) | Darbe sinyalleri |
| **1030 / 1090 MHz** | Uçak transponderi sorgu / cevap, **ADS-B** | Çok kısa darbeler, "tık" sesi |
| 1227,6 MHz | GPS L2 | Gürültünün altında, duyulmaz |
| **1240–1300 MHz** | **23 cm amatör** | FM, SSB, ATV. Telsizin anteni bu bant için uygun değildir. |

## 7.10 Kanal tabloları: PMR446, denizcilik, LPD433

### PMR446 (analog, 12,5 kHz)

| Kanal | Frekans (MHz) | Kanal | Frekans (MHz) |
|-------|---------------|-------|---------------|
| 1 | 446,00625 | 9 | 446,10625 |
| 2 | 446,01875 | 10 | 446,11875 |
| 3 | 446,03125 | 11 | 446,13125 |
| 4 | 446,04375 | 12 | 446,14375 |
| 5 | 446,05625 | 13 | 446,15625 |
| 6 | 446,06875 | 14 | 446,16875 |
| 7 | 446,08125 | 15 | 446,18125 |
| 8 | 446,09375 | 16 | 446,19375 |

> Telsiz frekans girişini **6 hane (kHz çözünürlüğü)** olarak alır ve sonucu seçili
> **adıma yuvarlar**. PMR446 kanal merkezleri 6,25 kHz'in katları olduğundan önce adımı
> **6,25 kHz** yapın (`Step`), sonra örneğin kanal 1 için `4 4 6 0 0 6` yazın. Telsiz
> bunu en yakın 6,25 kHz katına, yani **446,00625 MHz**'e yuvarlar.

### Denizcilik VHF (seçilmiş kanallar, gemi istasyonu frekansları)

| Kanal | Frekans (MHz) | Kullanım |
|-------|---------------|----------|
| 06 | 156,300 | Gemiler arası, SAR |
| 08 | 156,400 | Gemiler arası |
| 09 | 156,450 | Liman, marinalar (birçok ülkede) |
| 10 | 156,500 | Gemiler arası, liman |
| 12 | 156,600 | Liman işletmeleri |
| 13 | 156,650 | Köprüden köprüye seyir emniyeti |
| 14 | 156,700 | Liman işletmeleri |
| **16** | **156,800** | **İmdat, emniyet, çağrı** |
| 67 | 156,375 | Gemiler arası, SAR (bazı ülkelerde) |
| **70** | **156,525** | **DSC (yalnızca dijital)** |
| 72 | 156,625 | Gemiler arası |
| 77 | 156,875 | Gemiler arası |
| AIS 1 | 161,975 | AIS |
| AIS 2 | 162,025 | AIS |

> Dupleks kanallarda sahil istasyonu frekansı farklıdır (genellikle +4,6 MHz). Ayrıntılar
> için resmî kanal planına bakın. Kanal kullanımı ülkeye göre değişir; Türkiye için
> güncel planı ilgili denizcilik kaynaklarından doğrulayın.

### LPD433 (seçilmiş)

| Kanal | Frekans (MHz) | Not |
|-------|---------------|-----|
| 1 | 433,075 | İlk kanal |
| 18 | 433,500 | Amatör 70 cm FM çağrı frekansıyla aynı |
| 69 | 434,775 | Son kanal |

Kanallar 433,075 MHz'den başlayıp 25 kHz aralıkla ilerler.

## 7.11 Hızlı başvuru: ilk denemeler için frekanslar

| Ne | Frekans | Ayar | Uygulama / tuş |
|----|---------|------|-----------------|
| FM radyo | 88–108 MHz | — | `F` + `0` |
| Amatör FM çağrı | 145,500 MHz | FM, `WIDE` | — |
| Amatör UHF çağrı | 433,500 MHz | FM, `WIDE` | — |
| Yerel röleler | 145,600–145,7875 MHz | FM, `WIDE` | Tarama (uzun `*`) |
| APRS | 144,800 MHz | FM, `WIDE` | APRS RX |
| ISS ses / SSTV | 145,800 MHz | FM, `WIDE` | SSTV (etkinliklerde) |
| ISS APRS | 145,825 MHz | FM, `WIDE` | APRS RX |
| Hava trafik | 118–137 MHz | **AM**, 25 / 8,33 kHz adım | — |
| ACARS | 131,525 / 131,725 MHz | **AM** | ACARS RX |
| Denizcilik kanal 16 | 156,800 MHz | FM, `WIDE` | — |
| AIS | 161,975 / 162,025 MHz | FM, `WIDE` | AIS RX |
| Deniz DSC | 156,525 MHz | FM | ATIS DSC RX |
| Radyosonda | 400–406 MHz (SondeHub'dan bakın) | FM, `WIDE` | Sonde RS41 / M10 / M20 |
| PMR446 | 446,00625–446,19375 MHz | FM, **`NARROW`** | — |
| DAPNET çağrı cihazı | 439,9875 MHz | FM, `WIDE` | POCSAG RX |
| Spektrum keşfi | Herhangi | — | `F` + `5` |

---

[← Önceki: Amatör telsizcilik](06-amator-telsizcilik.md) · [İçindekiler](README.md) · [Sonraki: Cihaz donanımı ve ekran →](08-cihaz-donanimi-ve-ekran.md)
