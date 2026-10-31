# 4. Modülasyon ve Sinyal Türleri

[← Önceki: Desibel ve sinyal ölçümü](03-desibel-ve-sinyal-olcumu.md) · [İçindekiler](README.md) · [Sonraki: Antenler ve yayılım →](05-antenler-ve-yayilim.md)

Saf bir taşıyıcı dalga bilgi taşımaz. Ses veya veri göndermek için taşıyıcının
**genliği, frekansı veya fazı** değiştirilir; buna **modülasyon** denir. Bu bölüm
telsizde karşılaşacağınız bütün modülasyon ve sinyal türlerini, nasıl duyulduklarını
ve bu telsizle neyin çözülüp neyin çözülemeyeceğini anlatır.

## İçindekiler

1. [Neden modülasyon?](#41-neden-modülasyon)
2. [AM: genlik modülasyonu](#42-am-genlik-modülasyonu)
3. [FM: frekans modülasyonu](#43-fm-frekans-modülasyonu)
4. [SSB: tek yan bant (USB / LSB)](#44-ssb-tek-yan-bant-usb--lsb)
5. [CW: Mors kodu](#45-cw-mors-kodu)
6. [Dijital modülasyonun temelleri](#46-dijital-modülasyonun-temelleri)
7. [AFSK ve Bell 202: APRS ve paket radyo](#47-afsk-ve-bell-202-aprs-ve-paket-radyo)
8. [Diğer dijital sinyaller ve bu telsizde çözülenler](#48-diğer-dijital-sinyaller-ve-bu-telsizde-çözülenler)
9. [Çözülemeyen dijital sistemler](#49-çözülemeyen-dijital-sistemler)
10. [DTMF](#410-dtmf)
11. [1750 Hz tonu ve selektif çağrı (ZVEI / CCIR)](#411-1750-hz-tonu-ve-selektif-çağrı-zvei--ccir)
12. [CTCSS ve DCS](#412-ctcss-ve-dcs)
13. [Ses işleme: ön vurgu, compander, roger beep](#413-ses-işleme-ön-vurgu-compander-roger-beep)
14. [Emisyon sınıfları (F3E, A3E…)](#414-emisyon-sınıfları-f3e-a3e)
15. [Hangi sinyal nasıl duyulur?](#415-hangi-sinyal-nasıl-duyulur)
16. [Özet tablo](#416-özet-tablo)

---

## 4.1 Neden modülasyon?

- Ses frekansları (300–3000 Hz) doğrudan antenden yayılamaz. Bunun için kilometrelerce
  uzun anten gerekir.
- Herkes aynı ses frekanslarını kullansaydı sinyaller birbirine karışırdı.
- Çözüm: Sesi, **yüksek frekanslı bir taşıyıcının** üstüne yüklemek. Herkes farklı bir
  taşıyıcı frekansı (kanal) kullanır, alıcı istediği kanalı seçer.

Bir sinüs dalgasının değiştirilebilecek üç özelliği vardır:

| Değiştirilen özellik | Analog mod | Dijital karşılığı |
|----------------------|------------|-------------------|
| **Genlik** (yükseklik) | AM | ASK, OOK (CW) |
| **Frekans** | FM | FSK, AFSK, GFSK, MSK |
| **Faz** | PM | PSK, BPSK, QPSK |

Telsizde modülasyon **`Mode`** menüsünden seçilir: **`FM`**, **`AM`**, **`USB`**.

## 4.2 AM: genlik modülasyonu

Taşıyıcının **genliği**, sesin anlık değerine göre büyüyüp küçülür. Frekans sabit kalır.

```
 Ses:          ╭╮    ╭╮    ╭╮
              ╯  ╰──╯  ╰──╯  ╰
 AM sinyali:  ▁▃▅▇█▇▅▃▁▃▅▇█▇▅▃▁   (taşıyıcının "zarfı" sesi taşır)
```

- **Bant genişliği** = 2 × en yüksek ses frekansı. 3 kHz'lik ses için ≈ 6 kHz.
- **Spektrum**: Ortada güçlü bir taşıyıcı, iki yanında simetrik iki yan bant.
- **Verim düşüktür**: Gücün en az üçte ikisi bilgi taşımayan taşıyıcıya gider.
- **Parazite duyarlıdır**: Şimşek, motor ve elektrik parazitleri genliği bozar,
  doğrudan sesin içine "çıtırtı" olarak girer.
- **Nerede kullanılır?** Kısa ve orta dalga yayın, **havacılık bandı (118–137 MHz)**,
  CB'nin bir kısmı.

**Havacılık neden hâlâ AM kullanır?** AM'de iki istasyon aynı anda gönderirse
**ikisi de duyulur**: üst üste binen sesler ve bir ıslık. Kule, birinin kendisini
bastırdığını anlar. FM'de ise güçlü olan zayıfı tamamen bastırır ("yakalama etkisi"),
zayıf istasyon hiç fark edilmez. Havacılıkta bu tehlikelidir.

**Bu telsizde AM**: `Mode` → `AM`. `SetRxA` menüsünde AM için üç ses profili vardır:
`SHARP`, `STOCK`, `OPEN`. Alıcıda ayarlı ön filtre olmadığı için AM, güçlü sinyallerin
yakınında **en çok bozulan moddur**.

## 4.3 FM: frekans modülasyonu

Taşıyıcının **frekansı**, sesin anlık değerine göre bir miktar yukarı ve aşağı kayar.
Genlik sabit kalır.

```
 Ses:          ╭╮        ╭╮
              ╯  ╰──────╯  ╰
 FM sinyali:  │││││ │ │ │ │││││ │ │ │   (çizgiler sıklaşıp seyreliyor = frekans değişiyor)
```

### Temel FM kavramları

- **Sapma (deviation, Δf)**: Taşıyıcının merkez frekanstan en fazla ne kadar kaydığı.
  Ses yüksekliğine bağlıdır.
  - **Geniş FM** (amatör, eski profesyonel): ±5 kHz → `W/N` = `WIDE`
  - **Dar FM** (NFM): ±2,5 kHz → `W/N` = `NARROW`
  - **Yayın FM** (WFM): ±75 kHz (FM radyo, `F` + `0`)
- **Carson kuralı**: FM sinyalinin yaklaşık bant genişliği

  ```
  BW ≈ 2 × (Δf + en yüksek ses frekansı)
  Dar FM:   2 × (2,5 + 3) = 11 kHz  → 12,5 kHz kanala sığar
  Geniş FM: 2 × (5 + 3)   = 16 kHz  → 25 kHz kanala sığar
  ```

- **Modülasyon indeksi**: Δf / ses frekansı. Ne kadar büyükse sinyal o kadar geniştir.

### FM'in avantajları ve dezavantajları

| Avantaj | Dezavantaj |
|---------|------------|
| Genlik parazitlerine bağışıktır; temiz ses | AM ve SSB'den daha fazla bant genişliği ister |
| **Yakalama etkisi**: güçlü sinyal zayıfı bastırır, net dinleme | Zayıf sinyallerde ani kesilmeler (eşik etkisi) |
| Basit, ucuz alıcı ve verici | İki istasyon aynı anda konuşursa zayıf olan duyulmaz |
| Squelch ile sessiz bekleme | |

### Geniş/dar uyumsuzluğu nasıl anlaşılır?

| Durum | Belirti |
|-------|---------|
| Karşı taraf **geniş**, siz **dar** | Ses **yüksek, cızırtılı, bozuk**; tepelerde kesiliyor |
| Karşı taraf **dar**, siz **geniş** | Ses **kısık, uzak**; gürültü daha fazla |

Karşı tarafın modunu seçin: amatör FM'de genellikle `WIDE`; PMR446 ve çoğu
profesyonel sistemde `NARROW`.

## 4.4 SSB: tek yan bant (USB / LSB)

AM sinyalinin iki yan bandı **aynı bilgiyi** taşır ve taşıyıcı hiç bilgi taşımaz. **SSB**,
taşıyıcıyı ve yan bantlardan birini atar; geriye yalnızca tek bir yan bant kalır.

```
   AM:   [alt yan bant] [TAŞIYICI] [üst yan bant]     ≈ 6 kHz
   USB:                             [üst yan bant]     ≈ 2,7 kHz
   LSB:  [alt yan bant]                                ≈ 2,7 kHz
```

- **USB (Upper Side Band)**: Üst yan bant. Gelenek: 10 MHz üstünde ve VHF/UHF'de USB.
- **LSB (Lower Side Band)**: Alt yan bant. 10 MHz altındaki amatör HF bantlarında.
- **Avantajı**: Bütün güç bilgiye gider; bant genişliği yarıya iner. Zayıf sinyallerde
  FM'den çok daha iyidir. VHF'de uzak mesafe (DX) çalışmaları SSB ile yapılır.
- **Dezavantajı**: Frekansı **çok hassas** ayarlamak gerekir. 100–200 Hz hata sesi
  "**Donald Duck**" gibi tizleştirir veya kalınlaştırır. Squelch genellikle kullanılmaz.

**Bu telsizde**: `Mode` → `USB` ile **alım** yapılabilir (deneysel). Frekansı ince
ayarlamak için küçük adımlar (`0,01`–`0,5 kHz`) kullanın. Telsizin kristal hatası,
SSB'de birkaç yüz Hz kaymaya yol açabilir (bkz. [1.15](01-elektrik-ve-elektronik.md#115-kristal-osilatör-ve-ppm)).

## 4.5 CW: Mors kodu

**CW (Continuous Wave)**, taşıyıcının **açılıp kapatılmasıyla** (anahtarlanmasıyla)
Mors kodu göndermektir. En eski ve en dar bantlı moddur.

- **Bant genişliği**: Yalnızca 100–500 Hz. Çok zayıf sinyallerde bile çalışır.
- **Duyulması**: Taşıyıcının kendisi ses değildir. Alıcı **SSB/CW modunda**, frekansın
  biraz yanında dinlediğinde (ör. 700 Hz) bir **ton** duyulur.
- **FM alıcıda**: CW sinyali yalnızca squelch'in açılıp kapanması olarak duyulur, ton duyulmaz.
- **MCW (Modulated CW, F2A)**: Taşıyıcı sürekli açıkken üzerine **sesli ton**
  anahtarlanır. FM alıcıda ton olarak duyulur. Beacon uygulamasının `TONE` modu budur.
  Fox (tilki) avı vericileri genellikle MCW kullanır.

**Hız**: **WPM** (Words Per Minute, dakikadaki kelime) ile ölçülür. Standart kelime
"PARIS"tir: 1 WPM ≈ dakikada 50 nokta süresi. 18 WPM'de bir nokta ≈ 67 ms.

**Zamanlama kuralları**

| Öğe | Süre |
|-----|------|
| Nokta (dit) | 1 birim |
| Çizgi (dah) | 3 birim |
| Harf içindeki boşluk | 1 birim |
| Harfler arası boşluk | 3 birim |
| Kelimeler arası boşluk | 7 birim |

**Mors alfabesi** (`·` nokta, `−` çizgi)

| Harf | Kod | Harf | Kod | Rakam | Kod |
|------|-----|------|-----|-------|-----|
| A | `·−` | N | `−·` | 1 | `·−−−−` |
| B | `−···` | O | `−−−` | 2 | `··−−−` |
| C | `−·−·` | P | `·−−·` | 3 | `···−−` |
| D | `−··` | Q | `−−·−` | 4 | `····−` |
| E | `·` | R | `·−·` | 5 | `·····` |
| F | `··−·` | S | `···` | 6 | `−····` |
| G | `−−·` | T | `−` | 7 | `−−···` |
| H | `····` | U | `··−` | 8 | `−−−··` |
| I | `··` | V | `···−` | 9 | `−−−−·` |
| J | `·−−−` | W | `·−−` | 0 | `−−−−−` |
| K | `−·−` | X | `−··−` | `/` | `−··−·` |
| L | `·−··` | Y | `−·−−` | `?` | `··−−··` |
| M | `−−` | Z | `−−··` | `.` | `·−·−·−` |

**Yaygın CW kısaltmaları**: `CQ` (genel çağrı), `DE` (-den), `K` (geç, cevap bekliyorum),
`AR` (mesaj sonu), `SK` (görüşme sonu), `73` (saygılar), `TNX` (teşekkürler),
`RST` (sinyal raporu), `QTH` (konum), `OP` (operatör), `UR` (senin), `FB` (çok iyi).

**Tilki avı tanımlayıcıları** (Beacon uygulaması): ARDF yarışmalarında her vericinin
tanımlayıcısı `MO` + harftir: `MOE`, `MOI`, `MOS`, `MOH`, `MO5`. `MO` (`−− −−−`) ise
genellikle bitiş vericisidir.

**Bu telsizde CW**:

- **CW Keyer**: `PTT` veya yan tuşlarla elle anahtarlanan taşıyıcı gönderir.
- **CW USB**: USB-C'ye bağlanan bir anahtar veya pedal (paddle) ile gönderir.
- **CW Decode**: Gelen CW'yi çözer ve metne çevirir.
- **CW Trainer**: Mors öğrenme uygulaması.

## 4.6 Dijital modülasyonun temelleri

Dijital veri 0 ve 1'lerden oluşur. Bunlar taşıyıcıya çeşitli yollarla yüklenir:

| Yöntem | Açıklama | Örnek |
|--------|----------|-------|
| **OOK** (On-Off Keying) | Taşıyıcı var = 1, yok = 0 | CW, uzaktan kumandalar |
| **ASK** (Amplitude Shift Keying) | İki farklı genlik | |
| **FSK** (Frequency Shift Keying) | 0 ve 1 için iki farklı RF frekansı | POCSAG, BEAM |
| **AFSK** (Audio FSK) | FM sesin içinde 0 ve 1 için iki farklı **ses tonu** | APRS (Bell 202), DSC, ATIS |
| **GFSK** (Gaussian FSK) | Geçişleri yumuşatılmış FSK; daha dar spektrum | RS41 radyosonda, Bluetooth |
| **MSK / GMSK** | Faz sürekliliği korunan, en dar FSK türü | ACARS (AM üzerinde MSK), AIS (GMSK) |
| **PSK / BPSK** | Fazı 0° veya 180° çevirmek | COSPAS-SARSAT 406 MHz işaretçileri |

**Önemli terimler**

- **Baud**: Saniyede gönderilen **sembol** sayısı. Basit FSK'da 1 sembol = 1 bit,
  yani baud = bit/s.
- **bit/s (bps)**: Saniyede gönderilen bit sayısı.
- **Senkronizasyon (sync)**: Alıcının bir paketin başlangıcını tanıması için
  gönderilen sabit bit dizisi. Uygulamaların teşhis satırlarındaki `SYN`/`sync`
  sayaçları budur.
- **Çerçeve (frame) / paket**: Başı, sonu ve kontrol kodu belli veri bloğu.
- **CRC / FCS / BCS**: Çerçevenin bozulmadan geldiğini doğrulayan kontrol toplamı.
  Uygulamalardaki `CRC` sayacı, kontrolü geçemeyen çerçeveleri sayar.
- **Hata düzeltme (FEC)**: Bozulan bitlerin bir kısmını düzeltebilen ek bilgi
  (BCH, Reed-Solomon, Golay).
- **Manchester kodlama**: Her biti bir geçişle (yüksek→alçak veya alçak→yüksek)
  ifade eder. Uzun sabit dizileri önler. Meteomodem M10/M20 radyosondaları kullanır.
- **NRZ**: Bit 1 ve 0'ı sabit seviyelerle ifade etmek. RS41 ve POCSAG.
- **HDLC / AX.25**: Paket radyonun çerçeve yapısı. Bayraklar (`0x7E`), bit doldurma
  (bit stuffing) ve FCS kullanır.

## 4.7 AFSK ve Bell 202: APRS ve paket radyo

**APRS (Automatic Packet Reporting System)**, amatörlerin konum, mesaj ve telemetri
paylaştığı bir ağdır. VHF'de şöyle çalışır:

- Normal bir **FM** telsizin ses kanalı kullanılır.
- Veri, iki ses tonuyla gönderilir: **1200 Hz = "mark"**, **2200 Hz = "space"**.
  Bu, eski telefon modemlerinden gelen **Bell 202** standardıdır.
- Hız **1200 baud**'dur.
- Çerçeve yapısı **AX.25**'tir: kaynak çağrı işareti, hedef, yol (`WIDE1-1` gibi),
  bilgi alanı, FCS.
- Avrupa'da (IARU Bölge 1) frekans **144,800 MHz**'dir.

Kulağa nasıl gelir? Yaklaşık 0,5–1 saniyelik, "**brrrrt**" diye duyulan bir gürültü
patlaması.

**Twist**: 1200 ve 2200 Hz tonlarının seviye farkıdır. FM'deki ön vurgu ve geri
vurgu (bkz. [4.13](#413-ses-işleme-ön-vurgu-compander-roger-beep)) bu dengeyi değiştirir.
AF Spectro uygulaması twist'i dB olarak ölçer (`TW −3.0dB`). APRS TX uygulamasında
`2` tuşu ile ayarlanır.

**Bu telsizde**: APRS RX (alım), APRS TX (konum gönderme), APRS Edit (profil
düzenleme), APRS DIGI (sınırlı aktarıcı), KISS TNC (APRSdroid ile telefon bağlantısı).
Ayrıntılar [11. bölümde](11-uygulamalar.md#114-aprs-uygulamaları).

## 4.8 Diğer dijital sinyaller ve bu telsizde çözülenler

| Sistem | Ne taşır? | Modülasyon / hız | Tipik frekans | Uygulama |
|--------|-----------|------------------|---------------|----------|
| **APRS** | Amatör konum ve mesaj | AFSK Bell 202, 1200 baud, FM | 144,800 MHz | APRS RX/TX/DIGI, KISS TNC |
| **ACARS** | Uçak–yer veri mesajları | AM üzerinde MSK, 2400 bit/s | 131,525 / 131,725 / 131,825 MHz | ACARS RX |
| **AIS** | Gemi konum ve kimlikleri | GMSK, 9600 bit/s | 161,975 (AIS1) / 162,025 (AIS2) MHz | AIS RX |
| **VHF DSC** | Deniz dijital seçmeli çağrı, imdat | AFSK 1300/2100 Hz, 1200 baud | 156,525 MHz (kanal 70) | ATIS DSC RX |
| **ATIS** | Avrupa iç su yolu gemi kimliği | DSC biçimi, 1200 baud | Çalışma kanalları | ATIS RX |
| **POCSAG** | Çağrı cihazı mesajları | FSK, 512 / 1200 bit/s | 439,9875 MHz (DAPNET) | POCSAG RX |
| **Radyosonda RS41** | Meteoroloji balonu telemetrisi | GFSK, 4800 bit/s | 400–406 MHz | Sonde RS41 |
| **Radyosonda M10/M20** | Meteoroloji balonu telemetrisi | FSK, Manchester, ≈ 9600 çip/s | 400–406 MHz | Sonde M10 / M20 |
| **COSPAS-SARSAT** | Uydu imdat işaretçileri (EPIRB/ELT/PLB) | BPSK, 400 bit/s | 406,0–406,1 MHz | EPIRB 406 |
| **121,5 MHz homer** | İmdat işaretçisinin yön bulma sinyali | AM, süpürülen ton | 121,500 / 243,000 MHz | Sig Finder |
| **SSTV** | Durağan resim | FM ses içinde 1500–2300 Hz tonlar | 145,800 MHz (ISS etkinlikleri) | SSTV |
| **BEAM** | Telsizden telsize kanal ayarı aktarma | BK4829 FSK modemi | Seçilen kanal | BEAM |
| **CW** | Mors | OOK | Bandın CW bölümü | CW Decode |

> [!NOTE]
> Bu uygulamaların çoğu **deneyseldir** ve [11. bölümde](11-uygulamalar.md) ayrıntılı
> anlatılmıştır. Hepsi demodüle edilmiş sesi telsizin ADC'siyle örnekler. Bu yüzden
> ses yolunun sınırları (filtreler, örnekleme hızı) neyin çözülebileceğini belirler.

## 4.9 Çözülemeyen dijital sistemler

Spektrumda göreceğiniz ama bu telsizle **anlaşılır hale getiremeyeceğiniz** sinyaller:

| Sistem | Neden çözülemez? | Nasıl duyulur? |
|--------|------------------|----------------|
| **DMR** (dijital profesyonel / amatör telsiz) | Dijital ses kodlayıcı (AMBE) ve TDMA gerekir | "Tırtırtır" diye ritmik dijital gürültü |
| **D-STAR, C4FM / System Fusion** | Dijital ses kodlayıcıları | Dijital hışırtı |
| **TETRA** (acil servisler) | Dijital, çoğunlukla şifreli | Sürekli "vızzz" |
| **DVB-T** (dijital TV) | 8 MHz geniş OFDM | Geniş düz bir plato |
| **GSM / LTE / 5G** | Çok geniş, dijital, şifreli | Bu bantlar çoğunlukla telsizin kapsamı dışında |
| **ADS-B** (1090 MHz uçak konumu) | 1 Mbit/s darbe kodlama, çok hızlı | Kısa "tık" sesleri |
| **LoRa / Meshtastic** (868 MHz) | Chirp spektrum yayma | Kısa süpürme sesleri |
| **Meteor-M LRPT** (137 MHz meteoroloji uydusu) | Dijital QPSK görüntü | Sürekli hışırtı |

> [!IMPORTANT]
> Şifreli veya kamuya açık olmayan haberleşmeleri çözmeye çalışmak, kaydetmek veya
> içeriğini yaymak yasal sorun doğurur. Bu tablo yalnızca **spektrumda gördüklerinizi
> tanıyabilmeniz** içindir.

## 4.10 DTMF

**DTMF (Dual-Tone Multi-Frequency)**, telefon tuş seslerinin aynısıdır. Her tuşa basıldığında
**iki ton aynı anda** gönderilir: biri satırdan, biri sütundan.

| | 1209 Hz | 1336 Hz | 1477 Hz | 1633 Hz |
|---|---|---|---|---|
| **697 Hz** | 1 | 2 | 3 | A |
| **770 Hz** | 4 | 5 | 6 | B |
| **852 Hz** | 7 | 8 | 9 | C |
| **941 Hz** | * | 0 | # | D |

Telsizcilikte DTMF; röle kontrolü, Echolink/AllStar düğümlerine bağlanma, kimlik
gönderme (**PTT ID**) ve uzaktan komut için kullanılır.

**Bu telsizde**:

- Ana ekranda `*` tuşuna **kısa** basınca DTMF giriş modu açılır. Rakamları yazıp
  `PTT` ile gönderirsiniz.
- `PTT ID` menüsü, her gönderimin başında ve/veya sonunda otomatik DTMF kodu gönderir
  (`UPCode`, `DWCode`). `APOLLO QUINDAR` seçeneği, NASA'nın Apollo görevlerindeki
  "bip" tonlarını taklit eder.
- `D Live` menüsü, gelen DTMF tonlarını canlı olarak ekranda gösterir.
- Fusion sürümünde **DTMF çağrı (DTMF calling)** özelliği kapalıdır.

## 4.11 1750 Hz tonu ve selektif çağrı (ZVEI / CCIR)

- **1750 Hz tonu (tone burst)**: Bazı eski Avrupa röleleri, açılmak için gönderimin
  başında **kısa bir 1750 Hz tonu** ister. Bu firmware'de yan tuşlara `1750Hz`
  işlevi atanabilir. Tuş basılıyken PTT ile birlikte ton gönderilir. AF Scope
  uygulamasının TUNE görünümü bu tonu "1750 CALL TONE" olarak tanır.
- **Selektif çağrı (selcall)**: Arka arkaya gönderilen 5 veya daha fazla tondan oluşan
  bir kod. Belirli bir telsizi veya merkezi çağırmak için kullanılır. Standartları
  **ZVEI-1, ZVEI-2, CCIR-1, CCIR-2**. Avrupa'da itfaiye çağrı cihazları ve Alp
  bölgesindeki acil kanal (Canal E) kullanır. Bu telsizde **ToneCall** uygulaması gönderir.

## 4.12 CTCSS ve DCS

### Ne işe yarar?

Aynı frekansı birden fazla grup kullanıyorsa, herkes herkesi duyar. **CTCSS** ve **DCS**,
sese eklenen ve hoparlörden duyulmayan bir "**erişim kodu**"dur:

- **Gönderirken** (`TxCTCS` / `TxDCS`): Sesinizin altına ton eklenir. Röleler genellikle
  açılmak için belirli bir ton ister.
- **Alırken** (`RxCTCS` / `RxDCS`): Telsiz yalnızca **doğru tonu taşıyan** sinyallerde
  hoparlörü açar. Diğer sinyaller frekansta olsa bile duyulmaz.

> [!WARNING]
> **CTCSS/DCS şifreleme değildir!** Tonu olmayan ya da farklı tonlu herkes sizi
> duyabilir. `RxCTCS` ayarlıyken siz yalnızca başkalarını **duymazsınız**; frekansı
> kullanan biri varken gönderim yaparak onların konuşmasını bozabilirsiniz. Göndermeden
> önce `MONITOR` ile frekansın boş olduğunu kontrol edin.

### CTCSS (Continuous Tone-Coded Squelch System)

- 67,0–254,1 Hz arasında **alçak frekanslı, sürekli bir ses tonu**.
- Ses yolundaki yüksek geçiren filtre (≈ 300 Hz) sayesinde hoparlörden duyulmaz.
- Başka marka isimleri: **PL** (Private Line, Motorola), **CTCSS**, **"ton"**,
  **"subton"**.
- Amatör rölelerde en yaygın değerler bölgeye göre değişir. Sık görülenler: **88,5 Hz**,
  **123,0 Hz** ve **67,0 Hz**.

**Firmware'deki 50 CTCSS tonu (Hz)**

| | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|
| 67,0 | 69,3 | 71,9 | 74,4 | 77,0 | 79,7 | 82,5 | 85,4 | 88,5 | 91,5 |
| 94,8 | 97,4 | 100,0 | 103,5 | 107,2 | 110,9 | 114,8 | 118,8 | 123,0 | 127,3 |
| 131,8 | 136,5 | 141,3 | 146,2 | 151,4 | 156,7 | 159,8 | 162,2 | 165,5 | 167,9 |
| 171,3 | 173,8 | 177,3 | 179,9 | 183,5 | 186,2 | 189,9 | 192,8 | 196,6 | 199,5 |
| 203,5 | 206,5 | 210,7 | 218,1 | 225,7 | 229,1 | 233,6 | 241,8 | 250,3 | 254,1 |

### DCS (Digital-Coded Squelch)

- Ses tonunun yerine, **134,4 bit/s hızında sürekli tekrarlanan 23 bitlik dijital bir
  kod** gönderilir (12 bit veri + Golay hata düzeltme kodu).
- Kodlar **üç haneli sekizlik (octal)** sayılarla gösterilir: `D023`, `D754` gibi.
- **N (Normal)** ve **I (Inverted, ters)** iki polariteye sahiptir. Telsizde `D023N`,
  `D023I` olarak görünür. Firmware **104 kod × 2 polarite = 208 seçenek** sunar.
- Başka marka isimleri: **DPL** (Digital Private Line), **DCG**.

### Ton tarama

Bilmediğiniz bir tonu bulmak için:

- **`F` + `*`**: Dinlediğiniz frekanstaki CTCSS/DCS kodunu tarar.
- `RxCTCS` / `RxDCS` menüsündeyken **`*`**: Menü içinden ton taraması.
- **`F` + `4`** (frekans tarayıcı): Yakındaki bir vericinin önce frekansını, sonra
  tonunu bulur ve kanala kaydetmeyi önerir.

### Ekranda gösterim

Kanal satırında `CT` (CTCSS), `DCS` veya `DCR` (ters DCS) etiketleri görünür.
`TINY` arayüzde `DC` olarak kısalır.

## 4.13 Ses işleme: ön vurgu, compander, roger beep

- **Ön vurgu / geri vurgu (pre-emphasis / de-emphasis)**: FM'de yüksek ses frekansları
  gönderilirken güçlendirilir, alırken aynı oranda zayıflatılır. Sonuç: yüksek
  frekanslı hışırtı azalır. Dijital veri uygulamaları bu yüzden bazen **RAW** yolu
  (geri vurgu kapalı) kullanır.
- **Compander** (compressor + expander, `Compnd` menüsü): Gönderirken sesin dinamik
  aralığını sıkıştırır, alırken genişletir. **İki tarafta da açık olmalıdır.** Yalnızca
  bir tarafta açıksa ses "pompalanır", doğal duyulmaz. Ekranda küçük bir `C` simgesi görünür.
- **Roger beep** (`Roger` menüsü): `PTT` bırakıldığında gönderilen kısa "bip". `ROGER`
  basit bip, `MDC` ise Motorola MDC-1200 tarzı dijital bir kimlik patlamasıdır.
- **STE (Squelch Tail Elimination)**: Karşı taraf `PTT`'yi bıraktığında duyulan kısa
  "şşşt" kuyruk sesini bastırır. `STE` doğrudan bağlantı için, `RP STE` röle için.
- **Scrambler**: Sesi frekans çevirerek anlaşılmaz hale getirir. Fusion sürümünde kapalıdır;
  amatör bantlarda zaten **yasaktır** (anlamı gizlenmiş yayın).

## 4.14 Emisyon sınıfları (F3E, A3E…)

ITU, her yayın türünü üç karakterlik bir kodla tanımlar. Mevzuatta ve lisans
belgelerinde bu kodlarla karşılaşırsınız.

| Karakter | Anlamı | Örnekler |
|----------|--------|----------|
| 1. (ana taşıyıcı) | **A** = AM çift yan bant, **J** = SSB, bastırılmış taşıyıcı, **F** = frekans modülasyonu, **G** = faz modülasyonu | |
| 2. (modüle eden sinyal) | **1** = dijital, alt taşıyıcı yok; **2** = dijital, alt taşıyıcılı; **3** = analog | |
| 3. (bilgi türü) | **A** = telgraf (insan kulağıyla), **B** = otomatik telgraf, **C** = faks/resim, **D** = veri, **E** = ses (telefon), **W** = karma | |

| Kod | Anlamı | Örnek |
|-----|--------|-------|
| **A1A** | CW, Mors | CW Keyer |
| **A3E** | AM ses | Havacılık |
| **J3E** | SSB ses | VHF SSB |
| **F3E** | FM ses | Amatör FM röleleri |
| **G3E** | Faz modülasyonlu ses | Çoğu "FM" telsiz teknik olarak bunu kullanır |
| **F2A** | FM üzerinde tonlu Mors (MCW) | Beacon uygulaması (TONE modu) |
| **F2D** | FM üzerinde AFSK veri | APRS |
| **F1D** | Doğrudan FSK veri | POCSAG |
| **F3C** | FM üzerinde resim | SSTV |

## 4.15 Hangi sinyal nasıl duyulur?

| Duyduğunuz | Muhtemelen |
|------------|------------|
| Temiz konuşma, sinyal kesilince "şşt" | FM ses |
| Konuşma ama arkada sürekli hafif hışırtı, çıtırtılar | AM ses (havacılık) |
| Anlaşılmaz, ördek gibi tiz/kalın konuşma | SSB, yanlış modda veya yanlış ayarlı |
| Kısa "brrrrt" patlamaları | APRS / paket radyo |
| Ritmik "tırtırtır", dijital gürültü | DMR, D-STAR, C4FM |
| Sürekli "vızzzz" | TETRA veya başka sürekli dijital yayın |
| Kısa bip dizisi | DTMF, selcall veya roger beep |
| Yükselip alçalan ıslık, dakikalarca | SSTV |
| Yükselip alçalan "uuu–iii" sireni, sürekli | 121,5 MHz imdat işaretçisi (homer) – **ciddi olabilir** |
| Saniyede birkaç kez "tık" | Radyosonda, ADS-B veya başka veri |
| Düzenli "bip – bip" ve Mors | Beacon veya tilki avı vericisi |
| Sinyal yokken sürekli değişmeyen düz bir ses | Yakındaki elektronik cihaz paraziti |

> [!WARNING]
> **121,5 MHz** veya **406 MHz**'de sürekli bir işaretçi sinyali duyarsanız bu gerçek bir
> imdat çağrısı olabilir. Bulunduğunuz yeri, saati ve gözlemi **112 Acil Çağrı Merkezi**'ne
> bildirin. Sig Finder ve EPIRB 406 uygulamaları bu sinyalleri tanımanıza yardım eder,
> ancak resmî arama-kurtarmanın yerini tutmaz.

## 4.16 Özet tablo

| Mod | Bant genişliği | Telsizde | Tipik kullanım |
|-----|----------------|----------|----------------|
| CW | 0,1–0,5 kHz | CW Keyer / Decode / USB | Uzak mesafe, düşük güç |
| SSB (USB) | ≈ 2,7 kHz | `Mode` → `USB` (alım, deneysel) | VHF DX |
| AM | ≈ 6–8 kHz | `Mode` → `AM` | Havacılık |
| Dar FM | ≈ 11 kHz (12,5 kHz kanal) | `W/N` → `NARROW` | PMR446, profesyonel |
| Geniş FM | ≈ 16 kHz (25 kHz kanal) | `W/N` → `WIDE` | Amatör röleler |
| Yayın FM | ≈ 200 kHz | `F` + `0` | Radyo dinleme |
| APRS (AFSK 1200) | FM kanalı içinde | APRS uygulamaları | Konum, mesaj |
| CTCSS | 67–254 Hz alt ton | `TxCTCS` / `RxCTCS` | Röle erişimi, grup ayırma |
| DCS | 134,4 bit/s alt kod | `TxDCS` / `RxDCS` | Grup ayırma |

---

[← Önceki: Desibel ve sinyal ölçümü](03-desibel-ve-sinyal-olcumu.md) · [İçindekiler](README.md) · [Sonraki: Antenler ve yayılım →](05-antenler-ve-yayilim.md)
