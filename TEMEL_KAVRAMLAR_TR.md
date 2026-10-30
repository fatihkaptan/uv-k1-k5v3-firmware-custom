# Temel Kavramlar ve Başlangıç Rehberi

Amatör telsizciliğe yeni başlayanlar ve UV-K1 / UV-K5 V3 telsizini (F4HWN Fusion
firmware) ilk kez kullananlar için hazırlanmıştır. Menü ve tuşların ayrıntıları
için [KILAVUZ_TR.md](KILAVUZ_TR.md) dosyasına bakın.

> [!WARNING]
> **Dinlemek serbesttir ama göndermek değildir.** Amatör bantlarda yayın yapmak
> için Türkiye'de BTK'nın (Bilgi Teknolojileri ve İletişim Kurumu) verdiği
> **amatör telsizci belgesi ve çağrı işareti** gerekir. Belgeniz yoksa `PTT`
> tuşuna basmayın. Hava sahası, deniz, kamu ve acil durum frekanslarında ise
> belgeli olsanız bile yayın yapamazsınız.

## İçindekiler

1. [Amatör telsizcilik nedir?](#1-amatör-telsizcilik-nedir)
2. [Temel kavramlar](#2-temel-kavramlar)
3. [Telsiz jargonu](#3-telsiz-jargonu)
4. [İlk açılışta yapılacaklar](#4-ilk-açılışta-yapılacaklar)
5. [Belgesiz yapabilecekleriniz: dinleme rehberi](#5-belgesiz-yapabilecekleriniz-dinleme-rehberi)
6. [Belge aldıktan sonra: ilk görüşme](#6-belge-aldıktan-sonra-ilk-görüşme)
7. [Röleye çıkmak](#7-röleye-çıkmak)
8. [Telsiz görgü kuralları](#8-telsiz-görgü-kuralları)
9. [Cihazın sınırları ve güvenlik](#9-cihazın-sınırları-ve-güvenlik)
10. [Belge nasıl alınır, nereden öğrenilir?](#10-belge-nasıl-alınır-nereden-öğrenilir)

---

## 1. Amatör telsizcilik nedir?

Amatör telsizcilik (ham radio), kâr amacı gütmeden radyo iletişimiyle ilgilenmenin
adıdır. Telsizciler başka telsizcilerle yerel olarak veya dünya çapında görüşür,
anten ve devre yapar, uydu ve uzay istasyonuyla temas kurar, dijital modları
dener. Afet durumlarında da gönüllü olarak haberleşmeye destek olurlar.

UV-K5 / UV-K1 bir **el telsizidir**. Başlıca VHF (2 metre) ve UHF (70 cm)
bantlarında çalışır, ama alıcısı çok daha geniş bir aralığı dinleyebilir.

## 2. Temel kavramlar

### Frekans ve bant

- **Frekans:** Radyo dalgasının saniyedeki titreşim sayısıdır, MHz cinsinden yazılır
  (ör. `145.500 MHz`). Telsizde "hangi istasyonda" olduğunuzu frekans belirler.
- **Bant:** Belirli bir amaca ayrılmış frekans aralığıdır. Adını çoğunlukla dalga
  boyundan alır:

| Bant | Aralık (Türkiye, amatör) | Not |
|------|---------------------------|-----|
| **2 m (VHF)** | 144–146 MHz | Yeni başlayanların en çok kullandığı bant |
| **70 cm (UHF)** | 430–440 MHz | Şehir içinde ve rölelerde yaygın |

> Bu telsiz başka bantları da (ör. 18–1300 MHz arası geniş bir aralık)
> **dinleyebilir**. Ancak gönderme yalnızca izin verilen amatör bantlarda
> yapılmalıdır. `F Lock` ayarı ile `CE HAM` (144–146 / 430–440) seçilirse
> telsiz yalnızca bu aralıklarda gönderim yapar.

### Modülasyon (Mode)

Sesin radyo dalgasına nasıl yüklendiğini belirtir. Menüde `Mode` öğesinden seçilir.

| Mod | Nerede kullanılır |
|-----|-------------------|
| **FM** | Amatör VHF/UHF görüşmeleri, röleler, PMR, ticari telsizler |
| **AM** | Havacılık bandı (118–137 MHz) |
| **USB** (SSB) | Tek yan bant; bu telsizde yalnızca alım için deneyseldir |

### VFO ve kanal (hafıza)

- **VFO modu:** Frekansı serbestçe yazar veya değiştirirsiniz.
- **Kanal (MR) modu:** Önceden kaydettiğiniz frekanslar arasında geçersiniz.
- İkisi arasında `F` + `3` ile geçilir. Telsizde iki VFO vardır (**A** ve **B**),
  aralarında `F` + `2` ile geçilir.

### Simpleks, dupleks ve röle

- **Simpleks:** İki telsiz aynı frekansta doğrudan konuşur. Menzil kısadır
  (araziye göre birkaç km).
- **Röle (repeater):** Genellikle bir tepeye kurulmuş istasyondur. Bir frekanstan
  aldığı sinyali başka bir frekanstan güçlendirerek tekrar yayınlar. El
  telsiziyle onlarca km uzaklıktaki istasyonlarla konuşmanızı sağlar.
- **Offset (kayma):** Rölenin dinlediği ve yayınladığı frekanslar arasındaki
  farktır. Menüde `TxODir` (yön: `+`/`-`) ve `TxOffs` (miktar) ile ayarlanır.

### CTCSS ve DCS (ton)

- Sese eklenen, duyulmayan bir **erişim tonudur**.
- **CTCSS:** Analog ton (ör. 88.5 Hz). **DCS:** Dijital kod (ör. D023N).
- Röleler çoğunlukla açılmak için belirli bir ton ister. Bunu `TxCTCS` / `TxDCS`
  ile ayarlarsınız.
- `RxCTCS` / `RxDCS` ayarlıysa telsiz yalnızca o tonu taşıyan sinyalleri duyurur.

> [!NOTE]
> Ton bir şifreleme **değildir**. Tonu farklı olan ya da ton kullanmayan herkes
> sizi yine duyabilir.

### Squelch (susturma)

- Sinyal yokken duyulan hışırtıyı keser. `Sql` menüsünden veya `F` + `UP`/`DOWN`
  ile 0–9 arasında ayarlanır.
- **Düşük değer:** Zayıf sinyalleri de duyarsınız, ama hışırtı da daha sık açılır.
- **Yüksek değer:** Yalnızca güçlü sinyaller açılır.
- Başlangıç için **3–4** uygun bir değerdir.

### S-metre ve RSSI

Alınan sinyalin gücünü gösterir: **S0** (yok) → **S9** (güçlü) → **S9+** (çok
güçlü). Görüşmelerde "sinyalin S7 geliyor" gibi raporlar verilir.

### Çıkış gücü

Gönderme gücüdür (`LOW 1` < 20 mW … `HIGH` ≈ 5 W). `F` + `6` veya `Power`
menüsünden değiştirilir.

**Kural:** İletişim için yeterli olan **en düşük gücü** kullanın. Pil daha uzun
dayanır, başkalarına daha az parazit yaparsınız.

### Adım (Step)

`UP`/`DOWN` tuşuna her basışta frekansın ne kadar değişeceğini belirler. Amatör
FM için **12.5 kHz** veya **25 kHz**, havacılık bandı için **8.33 kHz** veya
**25 kHz** uygundur. `Step` menüsünden ya da `F` + `SIDE1`/`SIDE2` ile değiştirilir.

### Geniş / dar bant (W/N)

`WIDE` (25 kHz) veya `NARROW` (12.5 kHz) kanal genişliğidir. Karşı taraf hangisini
kullanıyorsa onu seçin. Amatör FM'de çoğunlukla `WIDE` kullanılır. Sesiniz kısık
veya bozuk geliyorsa bu ayarı kontrol edin.

### Anten ve SWR

- Telsizin menzilini en çok etkileyen şey antendir. Daha iyi bir anten,
  daha yüksek güçten çoğu zaman daha fazla fark yaratır.
- **SWR:** Antenin vericiye ne kadar uyumlu olduğunu gösterir. Uyumsuz anten
  gücü geri yansıtır.

> [!CAUTION]
> **Anten takılı değilken asla gönderme yapmayın (PTT'ye basmayın).** Verici
> zarar görebilir.

### Dual Watch, tarama ve spektrum

- **Dual Watch / RxMode:** İki VFO'yu (Full Watch ile ayrıca 2 öncelikli kanalı)
  aynı anda dinler.
- **Tarama (`*`):** Kanalları veya frekansları sırayla gezip sinyal bulunca durur.
- **Spektrum (`F` + `5`):** Çevredeki frekansları grafik olarak gösterir. Nerede
  sinyal olduğunu görmenin en hızlı yoludur.

## 3. Telsiz jargonu

### Çağrı işareti

Her belgeli telsizcinin BTK tarafından verilen benzersiz bir kimliği vardır
(Türkiye'de ön ekler `TA`, `TB`, `YM` vb.; ör. `TA1ABC`). Yayın yaparken
çağrı işaretinizi söylemek zorunludur.

### Sık kullanılan Q kodları ve ifadeler

| İfade | Anlamı |
|-------|--------|
| **QTH** | Bulunduğum yer |
| **QRZ?** | Beni kim çağırıyor? |
| **QSO** | Telsiz görüşmesi |
| **QSL** | Anlaşıldı / görüşme onayı (kart) |
| **QSY** | Başka frekansa geçmek |
| **QRM** | İnsan kaynaklı parazit |
| **QRN** | Doğal parazit (şimşek vb.) |
| **QRP** | Düşük güçle çalışmak |
| **CQ** | Genel çağrı ("dinleyen herkese") |
| **73** | Saygılar, iyi dilekler (görüşme sonu) |
| **Roger** | Anlaşıldı |

### Fonetik alfabe (ITU)

Çağrı işaretini harf harf okurken kullanılır:

| | | | |
|---|---|---|---|
| A – Alfa | H – Hotel | O – Oscar | V – Victor |
| B – Bravo | I – India | P – Papa | W – Whiskey |
| C – Charlie | J – Juliett | Q – Quebec | X – X-ray |
| D – Delta | K – Kilo | R – Romeo | Y – Yankee |
| E – Echo | L – Lima | S – Sierra | Z – Zulu |
| F – Foxtrot | M – Mike | T – Tango | |
| G – Golf | N – November | U – Uniform | |

Örnek: `TA1ABC` → "Tango Alfa Bir Alfa Bravo Charlie".

## 4. İlk açılışta yapılacaklar

Telsiz elinize geçtiğinde sırasıyla şunları yapın:

1. **Pili tam şarj edin.** USB-C ile şarj edilebilir.
2. **Anteni sıkıca takın.**
3. **Kalibrasyonu yedekleyin.** F4HWN yüklüyse
   [UV Studio](https://armel.github.io/uvstudio/#dump-calib) ile
   `calibration.dat` dosyasını indirip saklayın. Bu en önemli adımdır.
4. **Pil tipini seçin.** Gizli menüden (`PTT` + `SIDE1` basılıyken açın)
   `BatTyp` ayarını pilinize göre yapın. Pil yüzdesi böylece doğru görünür.
5. **Bölge kilidini ayarlayın.** Aynı gizli menüde `F Lock` → `CE HAM`.
   Telsiz böylece yanlışlıkla izinsiz frekansta gönderim yapmaz.
6. **Gezinme düzeni:** Modelinize göre `SetNav` (UV-K1 → `LEFT/RIGHT`,
   UV-K5 → `UP/DOWN`).
7. **Squelch'i ayarlayın:** `F` + `UP`/`DOWN` ile 3–4.
8. **Tuş takımını kilitlemeyi öğrenin:** `F` tuşuna uzun basış. Cepte veya
   çantada yanlışlıkla `PTT`'ye basılmasını önlemek için `SetLck` →
   `KEYS PTT` iyi bir seçimdir.

### Frekans girme

1. VFO modunda olduğunuzdan emin olun (ekranda frekans görünür; değilse `F` + `3`).
2. Rakamları yazın: `1` `4` `5` `5` `0` `0` → `145.500 MHz`.
3. İnce ayar için `UP`/`DOWN` kullanın.

### Kanal kaydetme

1. VFO'da frekansı ve gerekirse tonu ayarlayın.
2. `MENU` → `ChSave` → boş bir kanal seçin → `MENU`.
3. `ChName` ile kanala ad verin (ör. "ROLE IST").
4. Ekranda adın görünmesi için `ChDisp` → `NAME + FREQ`.

## 5. Belgesiz yapabilecekleriniz: dinleme rehberi

Belgeniz olmasa da bu telsizle öğrenebileceğiniz ve dinleyebileceğiniz çok şey
var. Dinleyerek öğrenmek, sınava hazırlanmanın da en iyi yoludur.

> [!NOTE]
> Kamuya açık olmayan haberleşmelerin içeriğini kaydetmek, yaymak veya başkasıyla
> paylaşmak yasal sorun doğurabilir. Dinlediğinizi kendinize saklayın.

| Ne | Frekans / nasıl | Telsizde ayar |
|----|-----------------|---------------|
| **FM radyo** | 88–108 MHz | `F` + `0` |
| **Amatör görüşmeler** | 144–146 ve 430–440 MHz | FM, `*` ile tarayın veya `F` + `5` spektrum |
| **Yerel röleler** | Bölgenizdeki röle çıkış frekansları | FM, kanal olarak kaydedin |
| **Simpleks çağrı frekansları** | 145.500 MHz, 433.500 MHz | FM |
| **Havacılık bandı** | 118–137 MHz | `Mode` → `AM`, adım 25 / 8.33 kHz |
| **ISS (Uluslararası Uzay İstasyonu)** | Ses: 145.800 MHz, APRS: 145.825 MHz | FM; istasyon geçerken (birkaç dakika) |
| **APRS paketleri** | 144.800 MHz (Avrupa) | `F` + `7` → **APRS RX** |
| **Hava sondaları (radyosonda)** | ~400–406 MHz | `F` + `7` → **Sonde RS41 / M10 / M20** |
| **Uçak veri bağlantısı** | ACARS (ör. 131.725 MHz) | `F` + `7` → **ACARS RX** |
| **Gemi konumları** | AIS: 161.975 / 162.025 MHz | `F` + `7` → **AIS RX** |
| **Sinyal analizi** | Herhangi bir sinyal | `F` + `7` → **AF Scope / AF Spectro** |
| **Mors öğrenmek** | — | `F` + `7` → **CW Trainer / CW Decode** |

### Pratik ipuçları

- **Spektrumla başlayın:** `F` + `5` ile 2 m bandına bakın. Tepe görünen yerde
  bir yayın var demektir.
- **Tarama listesi oluşturun:** Bulduğunuz röleleri kaydedip `ScList` ile bir
  listeye ekleyin, sonra `*` ile tarayın.
- **Dual Watch:** `RxMode` → `DUAL RX RESPOND`. Böylece bir röleyi ve çağrı
  frekansını aynı anda dinlersiniz.
- **RF Log:** Hangi frekansta ne zaman yayın olduğunu otomatik kaydeder.
  Bölgenizdeki aktif frekansları keşfetmek için çok kullanışlıdır.
- **Yükseklik önemlidir:** Pencere kenarı, balkon veya tepe gibi yüksek ve açık
  yerlerde çok daha fazla sinyal duyarsınız.

### PMR446 hakkında

446.0–446.2 MHz PMR446 bandı Avrupa'da belgesiz kullanılabilir. Ancak bu yalnızca
**tip onaylı, sabit antenli ve en fazla 0,5 W** cihazlar için geçerlidir.
UV-K5/K1 bu şartları karşılamaz. Bu yüzden belgesiz PMR yayını için uygun bir
cihaz **değildir**; PMR kanallarını yalnızca dinleyebilirsiniz.

## 6. Belge aldıktan sonra: ilk görüşme

1. **Önce dinleyin.** Frekansın boş olduğundan emin olun. Bir süre dinleyip
   "Frekans kullanımda mı?" diye sorun.
2. **Kendinizi tanıtın:**
   > "TA1ABC dinlemede, frekansı dinleyen var mı?"
3. **Konuşurken:** `PTT`'ye basın, **1 saniye bekleyin**, sonra telsizi ağzınızdan
   5–10 cm uzakta tutup normal sesle konuşun. Bitirdiğinizde `PTT`'yi bırakın.
4. **Kısa tutun.** Röle meşgul edilmemeli; uzun konuşmaları simplekse taşıyın (QSY).
5. **Kapanış:**
   > "Görüşme için teşekkürler, 73, TA1ABC dinlemede."

> [!TIP]
> Sesinizin nasıl gittiğini öğrenmek için başka bir telsizciden "sinyal ve ses
> raporu" isteyebilirsiniz. `Mic` (mikrofon kazancı) ayarını buna göre yapın.

## 7. Röleye çıkmak

Bir röleyi kullanmak için genellikle üç bilgiye ihtiyacınız vardır:
**çıkış frekansı**, **offset** ve **erişim tonu**. Bölgenizdeki rölelerin
güncel listesini TRAC veya yerel telsiz kulüplerinden öğrenin.

Örnek (tamamen temsilidir; gerçek değerleri yerel listeden alın):

| Bilgi | Değer | Telsizde |
|-------|-------|----------|
| Çıkış (dinlediğiniz) | 145.650 MHz | VFO'ya yazın |
| Offset | −600 kHz | `TxODir` → `-`, `TxOffs` → `0.600` |
| Ton | 88.5 Hz | `TxCTCS` → `88.5` |

Ardından `ChSave` ile kaydedin. `PTT`'ye bastığınızda telsiz otomatik olarak
144.950 MHz'de gönderir, röle de sizi 145.650 MHz'de tekrar yayınlar.

**Röleyi duyuyor ama açamıyorsanız:** tonu, offset yönünü ve `F Lock` ayarını
kontrol edin.

## 8. Telsiz görgü kuralları

- **Göndermeden önce mutlaka dinleyin.**
- **Çağrı işaretinizi** görüşmenin başında, sonunda ve belirli aralıklarla söyleyin.
- **Acil çağrıya her zaman öncelik verin.** "Acil" veya "Mayday" duyarsanız
  frekansı boşaltın.
- Siyaset, reklam, küfür, müzik yayını ve şifreli konuşma yapmayın.
- Röleyi uzun süre meşgul etmeyin; aralarda başkalarına fırsat bırakın.
- Gereğinden yüksek güç kullanmayın.
- Yeni başlayanlara yardımcı olun. Herkes bir gün ilk kez `PTT`'ye bastı.

## 9. Cihazın sınırları ve güvenlik

- **Alıcı sınırlıdır:** Bu telsizin ön katında bant filtresi yoktur. Güçlü verici
  istasyonlarına (baz istasyonu, yayın kulesi) yakın yerlerde, özellikle AM'de
  parazit ve bozulma normaldir. Bu donanımsal bir sınırlamadır.
- **Anten takılı değilken göndermeyin.**
- **Uzun süreli yüksek güçte göndermeyin.** Cihaz ısınır. `TxTOut` (zaman aşımı)
  ayarını açık tutun.
- **Firmware güncellerken** pilin dolu olduğundan emin olun. Multiboot geri
  yüklemesi sırasında telsizi asla kapatmayın.
- **Gönderme yapan uygulamalar** (APRS TX, Beacon, CW Keyer vb.) yalnızca
  belgeyle ve izin verilen frekanslarda kullanılmalıdır.

## 10. Belge nasıl alınır, nereden öğrenilir?

- Türkiye'de amatör telsizci belgesi **BTK**'nın düzenlediği sınavla alınır.
  Sınav konuları genellikle mevzuat, temel elektronik/radyo bilgisi ve işletme
  kurallarıdır. Güncel sınav tarihleri ve başvuru koşulları için BTK'nın resmî
  sitesini takip edin.
- **TRAC** (Türkiye Radyo Amatörleri Cemiyeti) ve yerel telsiz kulüpleri sınava
  hazırlık kursları düzenler, röle listeleri yayımlar ve yeni başlayanlara
  rehberlik eder.
- Bölgenizdeki bir kulübe katılmak; anten yapımı, saha etkinlikleri ve afet
  haberleşmesi tatbikatlarıyla öğrenmenin en hızlı yoludur.

---

İyi dinlemeler, şimdiden 73! 📻
