# 6. Amatör Telsizcilik: Mevzuat, Bant Planları ve İşletme Usulleri

[← Önceki: Antenler ve yayılım](05-antenler-ve-yayilim.md) · [İçindekiler](README.md) · [Sonraki: Frekans rehberi →](07-frekans-rehberi.md)

Bu bölüm amatör telsizciliğin ne olduğunu, belgenin nasıl alındığını, bantların nasıl
paylaşıldığını, bir görüşmenin nasıl yapıldığını ve telsizcilerin uyduğu kuralları anlatır.

> [!WARNING]
> Burada verilen mevzuat bilgileri **genel bilgi** amaçlıdır ve değişebilir. Bağlayıcı
> kurallar için her zaman **BTK**'nın (Bilgi Teknolojileri ve İletişim Kurumu) güncel
> yönetmeliklerine başvurun.

## İçindekiler

1. [Amatör telsizcilik nedir, ne değildir?](#61-amatör-telsizcilik-nedir-ne-değildir)
2. [Belge ve çağrı işareti](#62-belge-ve-çağrı-işareti)
3. [Belgesiz neler yapılabilir?](#63-belgesiz-neler-yapılabilir)
4. [ITU bölgeleri ve IARU](#64-itu-bölgeleri-ve-iaru)
5. [Bant planları](#65-bant-planları)
6. [Kanal adlandırma (V, RV, U, RU)](#66-kanal-adlandırma-v-rv-u-ru)
7. [Röleler](#67-röleler)
8. [Fonetik alfabe ve sayılar](#68-fonetik-alfabe-ve-sayılar)
9. [Q kodları ve işletme ifadeleri](#69-q-kodları-ve-işletme-ifadeleri)
10. [Görüşme (QSO) nasıl yapılır?](#610-görüşme-qso-nasıl-yapılır)
11. [Kayıt defteri (log), UTC ve QSL](#611-kayıt-defteri-log-utc-ve-qsl)
12. [Kurallar ve görgü](#612-kurallar-ve-görgü)
13. [Acil durum ve afet haberleşmesi](#613-acil-durum-ve-afet-haberleşmesi)
14. [Amatör telsizcilikte etkinlikler](#614-amatör-telsizcilikte-etkinlikler)
15. [Uydu ve uzay istasyonu](#615-uydu-ve-uzay-istasyonu)
16. [APRS ağı](#616-aprs-ağı)
17. [Öğrenmeye nereden başlamalı?](#617-öğrenmeye-nereden-başlamalı)

---

## 6.1 Amatör telsizcilik nedir, ne değildir?

**Amatör telsizcilik**, kişisel ilgi ve öğrenme amacıyla, **kâr gütmeden** yapılan radyo
haberleşmesidir. Uluslararası Telekomünikasyon Birliği (ITU) bunu ayrı bir **radyo
hizmeti** olarak tanımlar.

**Amatörler neler yapar?**

- Yerel ve uluslararası görüşmeler (sesle, Mors'la, dijital modlarla)
- Anten, alıcı ve verici tasarlayıp yapmak
- Uydular ve Uluslararası Uzay İstasyonu (ISS) ile temas
- Yarışmalar, ödüller, dağ ve park etkinlikleri (SOTA, POTA)
- Tilki avı / radyo yön bulma (ARDF)
- APRS, paket radyo, dijital modlar
- Afet ve acil durumlarda gönüllü haberleşme

**Amatör telsizcilik ne değildir?**

- Ticari bir iletişim aracı değildir: iş, satış veya reklam için kullanılamaz.
- Genel bir sohbet hattı (CB) değildir: belge ister, kurallara tabidir.
- Şifreli veya gizli haberleşme yapılamaz.
- Yayıncılık değildir: müzik, haber yayını vb. yapılamaz.

## 6.2 Belge ve çağrı işareti

### Belge

Türkiye'de amatör bantlarda yayın yapmak için **BTK'nın düzenlediği sınavı** geçip
**amatör telsizci belgesi** almak gerekir.

- Sınavda genellikle **mevzuat**, **temel elektrik-elektronik ve radyo bilgisi** ve
  **işletme usulleri** sorulur.
- Belgeler **sınıflara** ayrılır. Her sınıfın kullanabileceği bantlar ve en yüksek güç
  farklıdır. Güncel sınıflar ve yetkiler için ilgili yönetmeliğe bakın.
- Sınav takvimi, başvuru şartları ve ücretler BTK tarafından duyurulur.

> [!TIP]
> Bu dokümanın [1](01-elektrik-ve-elektronik.md)–[5](05-antenler-ve-yayilim.md).
> bölümleri sınavın teknik konularına iyi bir giriş sağlar. Sınava hazırlanmak için
> TRAC'ın ve yerel kulüplerin kurslarına katılmanız önerilir.

### Çağrı işareti

Belge ile birlikte size **benzersiz bir çağrı işareti** verilir. Yayın yaparken
kimliğiniz budur.

```
   T A 1 A B C
   └┬┘ │ └─┬─┘
    │  │   └── Kişisel ek (1–3 harf)
    │  └────── Rakam (çoğunlukla bölgeyi gösterir)
    └───────── Ülke ön eki
```

- ITU, her ülkeye çağrı işareti blokları ayırır. **Türkiye'nin blokları: TA–TC ve YM.**
- Çağrı işaretine eklenen ifadeler:
  - `/P` (portable): Taşınabilir istasyon, sabit adresiniz dışında
  - `/M` (mobile): Araçta
  - `/MM` (maritime mobile): Denizde
  - Başka bir ülkeden yayında, o ülkenin ön eki başa eklenir (ör. `SV/TA1ABC`).
- **CEPT T/R 61-01** tavsiyesini uygulayan ülkeler, birbirlerinin belgelerini belirli
  koşullarla tanır. Yurt dışında yayın yapmadan önce o ülkenin kurallarını kontrol edin.

## 6.3 Belgesiz neler yapılabilir?

| Etkinlik | Belge gerekir mi? |
|----------|-------------------|
| Amatör bantları **dinlemek** | Genellikle hayır |
| FM yayın radyosu dinlemek | Hayır |
| Hava ve deniz bantlarını dinlemek | Dinleme çoğunlukla hoş görülür, **içeriğini yaymak yasaktır** |
| Amatör bantlarda **yayın yapmak** | **Evet** |
| PMR446'da yayın yapmak | Belge gerekmez **ama tip onaylı, sabit antenli, ≤ 0,5 W cihazla**. UV-K5/K1 bu şartları karşılamaz. |
| Hava, deniz, kamu frekanslarında yayın | **Hayır, kesinlikle yapılamaz** (o servisin kendi lisansı gerekir) |
| Kendi telsizini programlamak, uygulama denemek | Yayın yapmıyorsanız hayır |

> [!IMPORTANT]
> Bu firmware birçok **yayın yapan uygulama** içerir (APRS TX, Beacon, CW Keyer, SSTV,
> ToneCall, BEAM, KISS TNC). Bunları **yalnızca belgeniz varsa ve izin verilen
> frekanslarda** kullanın. Telsizde **`F Lock`** bölge kilidini ayarlayarak yanlışlıkla
> izinsiz frekansta gönderim yapmayı önleyebilirsiniz (bkz. [9. bölüm](09-cihaz-kullanimi.md#93-kurulum-adım-adım)).

## 6.4 ITU bölgeleri ve IARU

- **ITU**, dünyayı üç bölgeye ayırır. Frekans tahsisleri bölgeye göre biraz farklıdır.
  - **Bölge 1**: Avrupa, Afrika, Orta Doğu, eski SSCB ülkeleri. **Türkiye buradadır.**
  - **Bölge 2**: Kuzey ve Güney Amerika
  - **Bölge 3**: Asya-Pasifik
- **IARU (International Amateur Radio Union)**, ulusal amatör derneklerin üst
  kuruluşudur. Bant planlarını önerir. Türkiye'nin IARU üyesi derneği **TRAC**'tır
  (Türkiye Radyo Amatörleri Cemiyeti).

Bu yüzden internetteki ABD kaynaklı bilgiler (ör. 146,52 MHz çağrı frekansı, +600 kHz
röle kayması, 144–148 MHz bandı) **Türkiye için geçerli değildir.**

## 6.5 Bant planları

Bant planı, bir bandın içinin **hangi mod ve amaçla** kullanılacağını gösterir. Uymak
herkesin işini kolaylaştırır: SSB'cilerin zayıf sinyal bölümünde FM ile konuşmazsınız,
APRS frekansında sesli görüşme yapmazsınız.

Aşağıdaki tablolar **IARU Bölge 1** planının **sadeleştirilmiş** özetidir. Ayrıntılı ve
güncel plan için TRAC'ın ve IARU Bölge 1'in yayımladığı planlara bakın; ulusal
farklılıklar olabilir.

### 2 metre (144–146 MHz)

| Aralık (MHz) | Kullanım | Önemli frekanslar |
|--------------|----------|-------------------|
| 144,000–144,110 | CW, EME (ay yansıması) | 144,050 CW çağrı |
| 144,110–144,150 | CW, dijital (MGM) | |
| 144,150–144,400 | SSB, CW, dijital | **144,300 SSB çağrı**, 144,174 FT8 |
| 144,400–144,490 | Yalnızca işaretçiler (beacon) | |
| 144,500–144,794 | Tüm modlar | 144,500 SSTV, 144,750 ATV konuşma |
| 144,794–144,990 | Dijital haberleşme | **144,800 APRS** |
| 144,990–145,194 | **Röle girişleri** (FM/DV) | 145,000–145,1875 |
| 145,194–145,594 | **FM/DV simpleks** | **145,500 FM çağrı (V40)** |
| 145,594–145,794 | **Röle çıkışları** (FM/DV) | 145,600–145,7875 |
| 145,794–145,806 | Uzay haberleşmesi (FM) | **145,800 ISS ses** |
| 145,806–146,000 | Uydu hizmeti | 145,825 ISS APRS |

### 70 santimetre (430–440 MHz)

| Aralık (MHz) | Kullanım | Önemli frekanslar |
|--------------|----------|-------------------|
| 430,000–432,000 | Ulusal planlara göre (röle girişleri, paket, karma) | |
| 432,000–432,100 | CW, EME | 432,050 CW çağrı |
| 432,100–432,400 | SSB, CW, dijital | **432,200 SSB çağrı** |
| 432,400–432,490 | İşaretçiler | |
| 432,500–433,000 | Tüm modlar | |
| 433,000–433,375 | Röle girişleri (1,6 MHz kaymalı sistemler) | |
| 433,400–433,575 | **FM simpleks** | **433,500 FM çağrı (U280)** |
| 433,600–434,000 | Tüm modlar | |
| 434,000–434,594 | Tüm modlar, ATV | |
| 434,594–434,981 | Röle çıkışları (1,6 MHz kaymalı sistemler) | |
| 435,000–438,000 | **Uydu hizmeti** | 436–437 MHz uydu inişleri |
| 438,000–440,000 | ATV, dijital, röleler (7,6 MHz kaymalı sistemler) | 439,9875 DAPNET (çağrı cihazı) |

> [!NOTE]
> 70 cm'de röle kayması ülkeye göre **1,6 MHz** veya **7,6 MHz** olabilir. Türkiye'deki
> bir röleye çıkmadan önce yerel röle listesinden çıkış, kayma ve ton bilgilerini kontrol edin.

**Telsizin bölge kilidi**: Gizli menüdeki `F Lock` → `CE HAM` seçildiğinde telsiz yalnızca
**144–146 MHz** ve **430–440 MHz** aralığında gönderim yapar. Bu, Bölge 1 amatör bantlarına
denk gelir ve Türkiye için önerilen ayardır.

## 6.6 Kanal adlandırma (V, RV, U, RU)

IARU Bölge 1, 12,5 kHz'lik kanal ızgarasında kanalları numaralandırır:

```
2 m:   Vnn  = 145,000 MHz + nn × 12,5 kHz        (simpleks)
       RVnn = röle; nn, ÇIKIŞ frekansını gösterir; giriş 600 kHz aşağıdadır
70 cm: Unnn = 430,000 MHz + nnn × 12,5 kHz       (simpleks)
       RUnnn = röle; nnn, çıkış frekansını gösterir
```

| Kanal | Frekans | Not |
|-------|---------|-----|
| V16 | 145,200 MHz | Simpleks bölümünün başı |
| **V40** | **145,500 MHz** | **FM çağrı frekansı** |
| V47 | 145,5875 MHz | |
| RV48 | Çıkış 145,600 / giriş 145,000 MHz | İlk röle kanalı |
| RV56 | Çıkış 145,700 / giriş 145,100 MHz | |
| RV63 | Çıkış 145,7875 / giriş 145,1875 MHz | Son röle kanalı |
| **U280** | **433,500 MHz** | **70 cm FM çağrı frekansı** |

Eski 25 kHz sistemindeki "R0, R1, … R7" adlarıyla da karşılaşabilirsiniz
(R0 = 145,600, R1 = 145,625 … R7 = 145,775 MHz).

## 6.7 Röleler

**Röle (repeater)**, genellikle yüksek bir tepeye kurulmuş, otomatik çalışan bir
istasyondur. Bir frekansta (**giriş**) aldığını aynı anda başka bir frekanstan
(**çıkış**) yeniden yayınlar.

```
  Siz (el telsizi)                  Röle (tepede)                   Diğer istasyon
  TX: 145,000 MHz  ───────────▶  RX 145,000 / TX 145,600  ───────────▶  RX: 145,600 MHz
  RX: 145,600 MHz  ◀───────────                           ◀───────────  TX: 145,000 MHz
```

**Bir röleyi kullanmak için gereken bilgiler**

| Bilgi | Telsizde | Örnek |
|-------|----------|-------|
| Çıkış frekansı (dinlediğiniz) | VFO'ya yazılır | 145,650 MHz |
| Kayma yönü | `TxODir` | `-` |
| Kayma miktarı | `TxOffs` | 0,600 MHz |
| Erişim tonu | `TxCTCS` veya `TxDCS` | 88,5 Hz (rölenin istediği) |
| Bazı eski rölelerde | `1750Hz` yan tuş işlevi | Gönderim başında 1750 Hz tonu |

**Röle görgüsü**

- **Göndermeden önce dinleyin.** Röle kullanımdaysa araya girmeyin.
- `PTT`'ye bastıktan sonra **1 saniye bekleyin**, sonra konuşun. Rölenin ve ton
  çözücünün açılması zaman alır; ilk heceniz kaybolabilir.
- Karşı taraf konuştuktan sonra **kısa bir ara bırakın**. Acil bir çağrı veya başka bir
  istasyonun katılması için fırsat olsun.
- Rölenin **zaman aşımı** vardır (çoğunlukla 2–3 dakika). Uzun konuşursanız röle sizi keser.
- Uzun sohbetleri **simplekse** taşıyın (QSY). Röle herkesin ortak kaynağıdır.
- **Ters dinleme (reverse)**: `8` tuşuna **uzun basmak**, giriş ve çıkış frekanslarını
  takas eder. Karşı tarafı doğrudan (rölesiz) duyup duyamadığınızı anlamak için kullanılır.
  Duyuyorsanız simplekse geçin, röleyi meşgul etmeyin.

## 6.8 Fonetik alfabe ve sayılar

Çağrı işaretleri ve önemli bilgiler **ITU fonetik alfabesiyle** harf harf okunur.

| Harf | Kelime | Okunuş | Harf | Kelime | Okunuş |
|------|--------|--------|------|--------|--------|
| A | Alfa | AL-fa | N | November | no-VEM-ber |
| B | Bravo | BRA-vo | O | Oscar | OS-kar |
| C | Charlie | ÇAR-li | P | Papa | pa-PA |
| D | Delta | DEL-ta | Q | Quebec | ke-BEK |
| E | Echo | E-ko | R | Romeo | RO-me-o |
| F | Foxtrot | FOKS-trot | S | Sierra | si-E-ra |
| G | Golf | GOLF | T | Tango | TAN-go |
| H | Hotel | ho-TEL | U | Uniform | YU-ni-form |
| I | India | İN-di-a | V | Victor | VİK-tor |
| J | Juliett | CU-li-et | W | Whiskey | VİS-ki |
| K | Kilo | Kİ-lo | X | X-ray | EKS-rey |
| L | Lima | Lİ-ma | Y | Yankee | YEN-ki |
| M | Mike | MAYK | Z | Zulu | ZU-lu |

**Örnek**: `TA1ABC` → "Tango Alfa Bir Alfa Bravo Charlie".

- Türkçe konuşulan görüşmelerde rakamlar genellikle Türkçe okunur ("bir", "iki"…).
  Uluslararası görüşmede İngilizce okunur; **9 "niner"** diye söylenir ki "nein" ile
  karışmasın.
- Türkçe görüşmelerde harfler için zaman zaman Türkçe şehir adları (Adana, Bursa…) da
  kullanılır. Uluslararası standart ise ITU alfabesidir.

## 6.9 Q kodları ve işletme ifadeleri

**Q kodları**, Mors döneminden kalan üç harfli kısaltmalardır. Sesli görüşmede de
kullanılır. Soru olarak kullanıldığında sonuna `?` eklenir.

| Kod | Anlamı (bildirim) | Soru biçimi |
|-----|-------------------|-------------|
| **QRA** | İstasyonumun adı … | İstasyonunuzun adı nedir? |
| **QRG** | Tam frekansınız … | Tam frekansım nedir? |
| **QRK** | Anlaşılırlığınız … (1–5) | Beni nasıl anlıyorsunuz? |
| **QRL** | Meşgulüm | Frekans kullanımda mı? |
| **QRM** | İnsan kaynaklı parazit var | Parazit var mı? |
| **QRN** | Doğal (atmosferik) parazit var | |
| **QRO** | Gücü artırın | Gücü artırayım mı? |
| **QRP** | Gücü azaltın / düşük güçle çalışıyorum | |
| **QRQ** | Daha hızlı gönderin (CW) | |
| **QRS** | Daha yavaş gönderin (CW) | |
| **QRT** | Yayını bitiriyorum, kapatıyorum | |
| **QRV** | Hazırım | Hazır mısınız? |
| **QRX** | Bekleyin, sizi … tekrar çağıracağım | |
| **QRZ** | Sizi … çağırıyor | Beni kim çağırıyor? |
| **QSB** | Sinyaliniz dalgalanıyor (fading) | |
| **QSL** | Anlaşıldı, onaylıyorum / görüşme onay kartı | Onaylıyor musunuz? |
| **QSO** | Görüşme, temas | |
| **QSY** | Başka frekansa geçin | Başka frekansa geçelim mi? |
| **QTH** | Konumum … | Konumunuz neresi? |
| **QTR** | Saat … (UTC) | Saat kaç? |

**Sık kullanılan ifadeler**

| İfade | Anlamı |
|-------|--------|
| **CQ** | Genel çağrı: "Dinleyen herhangi bir istasyon" |
| **DE** | "… dan/den" (CW'de) |
| **73** | Saygılar, iyi dilekler (görüşme sonu) |
| **88** | Sevgiler (samimi, genellikle karşı cinse) |
| **OM / YL / XYL** | Telsizci erkek / kadın / eş |
| **Roger** | Anlaşıldı |
| **Copy** | Aldım, duydum |
| **Over / Tamam** | Konuşmam bitti, sıra sende |
| **Out** | Görüşme tamamen bitti |
| **Break** | Araya girmek istiyorum (önemli durumda) |
| **Standby** | Bekle |
| **Mayday / Panne** | İmdat / Acil durum (hayati tehlike / ciddi sorun) |
| **DX** | Uzak mesafe görüşmesi veya istasyonu |
| **Eyeball** | Yüz yüze görüşme |
| **Shack** | Telsiz odası / istasyon |
| **Rig** | Telsiz cihazı |
| **Harmonic** | Telsizcinin çocuğu (şaka ile) |

## 6.10 Görüşme (QSO) nasıl yapılır?

### Genel çağrı (CQ) yapmak

1. **Doğru frekansı seçin.** Simpleks için 145,500 MHz (çağrı) veya simpleks bölümünde
   boş bir kanal.
2. **En az 10–15 saniye dinleyin.**
3. Sorun: "**Frekans kullanımda mı?** TA1ABC." Cevap yoksa devam edin.
4. Çağrı yapın:
   > "CQ CQ CQ, burası Tango Alfa Bir Alfa Bravo Charlie, TA1ABC, çağırıyor ve dinliyor."
5. Cevap gelirse çağrı frekansından **simpleks bir kanala** geçmeyi önerin:
   > "TA2XYZ, buradan TA1ABC. Seni S8 alıyorum. V30'a, yani 145,375'e geçelim mi?"

### Görüşme sırasında

- Her konuşmanın başında karşı tarafın, sonunda kendi çağrı işaretinizi söyleyin.
- İlk görüşmede genellikle şunlar paylaşılır: **sinyal raporu**, **isim**, **konum (QTH)**,
  bazen kullanılan cihaz ve anten.
- `PTT`'ye basın, 1 saniye bekleyin, telsizi ağzınızdan **5–10 cm uzakta** ve hafif yandan
  tutup normal sesle konuşun. Bağırmak sesi bozar.

### Kapanış

> "Güzel görüşme için teşekkürler, 73. TA2XYZ, buradan TA1ABC, dinlemede."

### Bir röleyi dinlemek ve katılmak

- Röle sessizse: "**TA1ABC dinlemede**" demek yeterlidir.
- Süren bir görüşmeye katılmak istiyorsanız, bir konuşmanın bitiminde kısaca
  çağrı işaretinizi söyleyin: "**TA1ABC**". Söz size verildiğinde konuşun.

## 6.11 Kayıt defteri (log), UTC ve QSL

- **Log (kayıt defteri)**: Yapılan görüşmelerin kaydıdır. Bazı ülkelerde zorunludur;
  her yerde iyi bir alışkanlıktır.
- Kaydedilecek bilgiler: **tarih, saat (UTC), frekans, mod, karşı istasyonun çağrı işareti,
  verilen ve alınan sinyal raporu**, isteğe bağlı isim ve konum.
- **UTC**: Telsizcilikte saat her zaman **Eşgüdümlü Evrensel Zaman** ile yazılır.
  Türkiye saati (TSİ) = **UTC + 3**. Yerel saat 15:00 → 12:00 UTC.
- **QSL kartı**: Görüşmeyi onaylayan kartpostal. Günümüzde elektronik olarak da yapılır
  (eQSL, LoTW gibi sistemler).
- Bu firmware'in **RF Log** özelliği, telsizin RX/TX etkinliğini otomatik kaydeder.
  Resmî bir log yerine geçmez ama hangi frekansta ne zaman trafik olduğunu görmek
  için çok kullanışlıdır (bkz. [9. bölüm](09-cihaz-kullanimi.md#919-rf-log)).

## 6.12 Kurallar ve görgü

### Genel kurallar (çoğu ülkede ortak)

1. **Kimliğinizi bildirin.** Görüşmenin başında, sonunda ve belirli aralıklarla çağrı
   işaretinizi söyleyin.
2. **Şifreli veya anlamı gizlenmiş yayın yapmayın.** (Bu yüzden scrambler kapalıdır.)
3. **Ticari, siyasi, dinî propaganda, reklam yapmayın.**
4. **Müzik veya yayın içeriği göndermeyin.**
5. **Küfür, hakaret, müstehcen konuşma yapmayın.**
6. **Kasıtlı parazit (jamming) yapmayın.**
7. **Belgenizin sınıfına uygun bant ve güçte** çalışın.
8. **Gereğinden yüksek güç kullanmayın.**
9. **Acil çağrılara her zaman öncelik verin.**
10. İnsansız çalışan istasyonlar (işaretçi, röle, digipeater) ayrıca izne tabi olabilir.

### Görgü

- **Önce dinleyin.** Frekansı birkaç saniye dinlemeden asla gönderim yapmayın.
- Yeni başlayanlara sabırlı olun; herkes bir gün ilk kez `PTT`'ye bastı.
- Tartışmaya girmeyin. Rahatsız edici bir istasyona cevap vermemek en iyi yöntemdir.
- APRS frekansında, uydu bölümlerinde ve işaretçi bölümlerinde sesli görüşme yapmayın.
- Röle ve çağrı frekanslarını uzun sohbetlerle meşgul etmeyin.

## 6.13 Acil durum ve afet haberleşmesi

Deprem, sel veya yangın gibi afetlerde cep telefonu ve internet altyapısı çökebilir.
Pille çalışan telsizler ve tepedeki röleler bu durumda **hayati bir yedek** olur.

- Afet haberleşmesine katılmak için **TRAC'ın ve yerel kulüplerin** acil durum
  gruplarına, eğitimlerine ve tatbikatlarına katılın.
- Bölgenizde hangi frekans ve rölelerin acil durumda kullanılacağını **önceden öğrenin**
  ve telsizinize **kanal olarak kaydedin**.
- **Hazırlık listesi**: Dolu yedek pil, şarj için güneş paneli veya powerbank (USB-C
  girişli piller için), uzun anten, kalem ve defter, kanal listesinin kâğıt çıktısı.
- Gerçek bir acil durumda **resmî kurumların (112, AFAD)** talimatlarına uyun. Amatör
  ağlar resmî kurumlara **destek** olur, onların yerini almaz.

> [!IMPORTANT]
> Belgeniz yoksa bile acil bir durumda hayat kurtarmak için telsiz kullanmak çoğu
> mevzuatta istisna olarak kabul edilir. Ancak bu istisna **gerçek ve hayati bir tehlike**
> içindir. Önce 112'yi aramayı deneyin.

## 6.14 Amatör telsizcilikte etkinlikler

| Etkinlik | Açıklama |
|----------|----------|
| **Yarışmalar (contest)** | Belirli sürede en çok görüşmeyi yapmak. VHF/UHF yarışmaları da vardır. |
| **SOTA** (Summits on the Air) | Dağ zirvelerinden yayın yapmak. El telsizi ve iyi bir antenle yapılabilir. |
| **POTA** (Parks on the Air) | Milli park ve korunan alanlardan yayın |
| **ARDF / Tilki avı** | Gizlenmiş vericileri yön bulma antenleriyle bulmak. 2 m'de, `MOE`…`MO5` tanımlayıcılı 5 verici ile yapılır. Bu firmware'in **Fox Hunt**, **Sig Finder** ve **Beacon** uygulamaları bunun için tasarlanmıştır. |
| **Saha günü (Field Day)** | Şebekeden bağımsız, sahada kurulan istasyonlarla yayın tatbikatı |
| **Ödüller (diploma)** | Belirli sayıda ülke, bölge veya istasyonla görüşmeyi belgeleyen ödüller |

## 6.15 Uydu ve uzay istasyonu

- **ISS (Uluslararası Uzay İstasyonu)** ve birçok **amatör uydu** 2 m ve 70 cm bantlarını kullanır.
- **ISS frekansları (Bölge 1)**:
  - Ses iniş (downlink): **145,800 MHz** FM
  - APRS digipeater: **145,825 MHz** (çağrı işareti `RS0ISS`, APRS TX'te `ARISS` yolu)
  - **ARISS**: Okullarla yapılan planlı görüşmeler ve **SSTV etkinlikleri** (ISS'ten resim
    gönderilir, bu firmware'in **SSTV** uygulamasıyla alınabilir)
- **FM amatör uydular**: Bazıları 2 m'den dinler, 70 cm'den yayınlar (veya tersi).
  Tam dupleks çalışma için iki telsiz gerekir. Bu telsizle **iniş sinyalini dinleyebilirsiniz**.
- **Geçiş tahmini**: Uydular ufkun üstünde yalnızca **5–12 dakika** görünür. Ne zaman
  geçeceğini bir uydu takip uygulaması veya web sitesi ile öğrenin.
- **Doppler**: Geçiş boyunca frekans ±3,5 kHz (2 m) / ±10 kHz (70 cm) kayar (bkz.
  [2.11](02-radyo-dalgalari-ve-spektrum.md#211-doppler-kayması)).

## 6.16 APRS ağı

**APRS**, amatörlerin konum, hava durumu, kısa mesaj ve telemetri paylaştığı bir ağdır.

| Bileşen | Görevi |
|---------|--------|
| **İstasyon / tracker** | Konumunu düzenli olarak gönderir |
| **Digipeater** (`WIDE1-1`, `WIDE2-1`) | Duyduğu paketi bir kez daha yayınlar, menzili artırır |
| **iGate** | Duyduğu paketleri internete (APRS-IS) aktarır |
| **aprs.fi** gibi siteler | Paketleri haritada gösterir |

- Avrupa'da frekans **144,800 MHz**'dir.
- **Yol (path)**: Paketin kaç kez aktarılacağını belirtir. Mobil ve taşınabilir
  istasyonlar için genellikle `WIDE1-1,WIDE2-1` önerilir. Gereksiz uzun yol kanalı tıkar.
- **SSID**: Çağrı işaretinin sonundaki `-7`, `-9` gibi ek. İstasyon türünü gösterir
  (ör. `-7` el telsizi, `-9` araç). APRS TX'in varsayılanı `-7`'dir.
- **Sembol**: Haritada görünen simge (insan, araba, ev…). APRS Edit ile 48 sembol arasından seçilir.

Bu firmware ile APRS: [11. bölüm](11-uygulamalar.md#114-aprs-uygulamaları) ve
[12. bölüm, senaryolar](12-uygulamali-senaryolar.md).

## 6.17 Öğrenmeye nereden başlamalı?

1. **Dinleyin.** Yerel röleleri ve 145,500 MHz'i birkaç hafta dinleyin. Görüşmelerin
   nasıl yapıldığını, hangi ifadelerin kullanıldığını öğrenin.
2. **Yerel bir kulübe veya TRAC şubesine** katılın. Kurslar, sınav hazırlığı ve en
   önemlisi tecrübeli telsizcilerle tanışma fırsatı sunar.
3. **Sınava hazırlanın.** Bu dokümanın teknik bölümleri iyi bir başlangıçtır.
4. **Belgenizi aldıktan sonra** ilk görüşmenizi tanıdık bir telsizciyle yapın.
5. **Basit bir anten yapın.** Bir J-pole veya toprak düzlemli anten, el telsizinin
   performansını katlar.
6. **Yeni alanlar keşfedin**: APRS, uydu, SSTV, tilki avı, CW…

---

[← Önceki: Antenler ve yayılım](05-antenler-ve-yayilim.md) · [İçindekiler](README.md) · [Sonraki: Frekans rehberi →](07-frekans-rehberi.md)
