# 2. Radyo Dalgaları, Frekans ve Spektrum

[← Önceki: Elektrik temelleri](01-elektrik-ve-elektronik.md) · [İçindekiler](README.md) · [Sonraki: Desibel ve sinyal ölçümü →](03-desibel-ve-sinyal-olcumu.md)

Bu bölüm radyo dalgasının ne olduğunu, frekans ile dalga boyunun ilişkisini,
spektrumun nasıl bölündüğünü ve telsizin ekranındaki frekansın nasıl okunacağını
anlatır. Spektrum analizörünü yorumlamayı da burada öğreneceksiniz.

## İçindekiler

1. [Elektromanyetik dalga nedir?](#21-elektromanyetik-dalga-nedir)
2. [Frekans, dalga boyu ve ışık hızı](#22-frekans-dalga-boyu-ve-ışık-hızı)
3. [Elektromanyetik spektrum](#23-elektromanyetik-spektrum)
4. [Radyo bantları (ITU sınıflandırması)](#24-radyo-bantları-itu-sınıflandırması)
5. [Bant, kanal, kanal aralığı ve adım](#25-bant-kanal-kanal-aralığı-ve-adım)
6. [Telsiz ekranında frekans okuma](#26-telsiz-ekranında-frekans-okuma)
7. [Bant genişliği](#27-bant-genişliği)
8. [Taşıyıcı, yan bantlar ve sinyalin "şekli"](#28-taşıyıcı-yan-bantlar-ve-sinyalin-şekli)
9. [Gürültü](#29-gürültü)
10. [Parazit türleri: harmonik, imaj, intermodülasyon, doyma](#210-parazit-türleri-harmonik-imaj-intermodülasyon-doyma)
11. [Doppler kayması](#211-doppler-kayması)
12. [Spektrum analizörü nedir, nasıl okunur?](#212-spektrum-analizörü-nedir-nasıl-okunur)
13. [Alıcı nasıl çalışır? (süperheterodin ve SDR)](#213-alıcı-nasıl-çalışır-süperheterodin-ve-sdr)
14. [Verici nasıl çalışır?](#214-verici-nasıl-çalışır)
15. [Özet](#215-özet)

---

## 2.1 Elektromanyetik dalga nedir?

Bir iletkenden (anten) **hızla yön değiştiren bir akım** geçtiğinde, iletkenin
çevresinde birbirine dik iki alan oluşur:

- **Elektrik alanı (E)**: Gerilim farkından doğar.
- **Manyetik alan (H)**: Akımdan doğar.

Bu iki alan birbirini besleyerek antenden uzaklaşır ve **ışık hızında** yayılır.
Buna **elektromanyetik dalga** denir. Radyo dalgası, ışık, mikrodalga ve röntgen
ışını aynı olgudur; yalnızca **frekansları** farklıdır.

```
            Elektrik alanı (dikey)
              ▲    ╭╮        ╭╮
              │   ╱  ╲      ╱  ╲
  ────────────┼──╯────╲────╯────╲────▶  yayılma yönü
              │        ╲  ╱      ╲  ╱
                        ╰╯        ╰╯
          Manyetik alan sayfaya dik (görünmüyor)
```

- Radyo dalgası **boşlukta da yayılır**; havaya ya da bir ortama ihtiyaç duymaz.
  Uydu ve uzay istasyonu iletişimi bu sayede mümkündür.
- Dalganın **elektrik alanının yönü** "polarizasyon"dur. Dikey tutulan el telsizi
  anteni **dikey polarizasyonlu** dalga yayar (bkz. [5. bölüm](05-antenler-ve-yayilim.md#54-polarizasyon)).

## 2.2 Frekans, dalga boyu ve ışık hızı

- **Frekans (f)**: Dalganın saniyedeki salınım sayısı (Hz).
- **Dalga boyu (λ, lambda)**: Dalganın bir tam salınım süresince aldığı yol (metre).
- **Işık hızı (c)**: ≈ 300 000 km/s = 3 × 10⁸ m/s.

```
λ (metre) = 300 / f (MHz)          f (MHz) = 300 / λ (metre)
```

| Frekans | Dalga boyu | Bandın adı / kullanım |
|---------|------------|-----------------------|
| 1 MHz | 300 m | Orta dalga (AM yayın) |
| 7 MHz | ≈ 43 m | 40 m amatör bandı |
| 27,185 MHz | ≈ 11 m | CB (Sivil Bant), "11 metre" |
| 28,5 MHz | ≈ 10,5 m | 10 m amatör bandı |
| 50 MHz | 6 m | 6 m amatör bandı |
| 100 MHz | 3 m | FM yayın radyosu |
| 121,5 MHz | ≈ 2,47 m | Havacılık acil durum frekansı |
| **145 MHz** | **≈ 2,07 m** | **2 m amatör bandı** |
| 156,8 MHz | ≈ 1,91 m | Denizcilik VHF kanal 16 |
| 406 MHz | ≈ 74 cm | Uydu acil durum işaretçileri (EPIRB) |
| **435 MHz** | **≈ 69 cm** | **70 cm amatör bandı** |
| 446 MHz | ≈ 67 cm | PMR446 |
| 868 MHz | ≈ 35 cm | ISM (LoRa, sensörler) |
| 1296 MHz | ≈ 23 cm | 23 cm amatör bandı |

Amatör bantlarının adlarındaki "**2 metre**", "**70 santim**" bu dalga boylarından
gelir. Dalga boyu, **anten boyunu** doğrudan belirler: 145 MHz için çeyrek dalga
anten yaklaşık 50 cm, 435 MHz için yaklaşık 17 cm'dir.

**Genel kural**: Frekans yükseldikçe

- dalga boyu kısalır, antenler küçülür,
- engellerden geçme ve kırınım yeteneği azalır,
- serbest uzayda aynı mesafede kayıp artar,
- daha geniş bant genişliği (daha çok veri) taşımak kolaylaşır.

## 2.3 Elektromanyetik spektrum

```
 Frekans →
 3 kHz      3 MHz      3 GHz        3 THz          ~400–790 THz      3 EHz
 │──────────│──────────│────────────│──────────────│─────────────────│───
 │   RADYO DALGALARI   │ MİKRODALGA │   KIZILÖTESİ │ GÖRÜNÜR IŞIK     │ UV, X-ışını, gama
 │ (VLF … UHF)         │ (SHF, EHF) │              │                  │
 └──── Bu telsiz: 18 MHz – 1,3 GHz arası (bir boşlukla) ────┘
```

- **Radyo dalgaları** ve **mikrodalgalar**, iyonlaştırıcı olmayan ışınımdır:
  atomları parçalayacak enerjileri yoktur. Yüksek güçte ve çok yakın mesafede
  yalnızca ısıtma etkileri olur.
- **Ultraviyole, X ve gama ışınları** iyonlaştırıcıdır; telsizle hiçbir ilgileri yoktur.

## 2.4 Radyo bantları (ITU sınıflandırması)

Uluslararası Telekomünikasyon Birliği (**ITU**), radyo spektrumunu onluk
basamaklara böler:

| Kısaltma | Açılımı | Türkçe | Frekans | Dalga boyu | Tipik kullanım |
|----------|---------|--------|---------|------------|----------------|
| VLF | Very Low Frequency | Çok alçak frekans | 3–30 kHz | 100–10 km | Denizaltı haberleşmesi |
| LF | Low Frequency | Alçak frekans | 30–300 kHz | 10–1 km | Uzun dalga yayın, zaman sinyalleri |
| MF | Medium Frequency | Orta frekans | 300 kHz–3 MHz | 1 km–100 m | AM yayın, 160 m amatör bandı |
| **HF** | High Frequency | Yüksek frekans ("kısa dalga") | 3–30 MHz | 100–10 m | Kıtalararası amatör, CB, yayın |
| **VHF** | Very High Frequency | Çok yüksek frekans | 30–300 MHz | 10–1 m | FM yayın, hava, deniz, **2 m amatör** |
| **UHF** | Ultra High Frequency | Ultra yüksek frekans | 300 MHz–3 GHz | 1 m–10 cm | **70 cm amatör**, PMR, TV, GSM, GPS |
| SHF | Super High Frequency | Süper yüksek frekans | 3–30 GHz | 10–1 cm | Uydu TV, radar, Wi-Fi 5 GHz |
| EHF | Extremely High Frequency | Aşırı yüksek frekans | 30–300 GHz | 1 cm–1 mm | Radyo astronomi, 5G mmWave |

**UV-K5 / UV-K1'in adındaki "UV"**, **U**HF + **V**HF anlamına gelir: cihaz bu iki
bantta göndermek için tasarlanmıştır. Alıcı, HF'nin üst kısmından (~18 MHz) UHF'nin
ortasına (~1,3 GHz) kadar dinleyebilir. Arada **630–840 MHz** arası bir boşluk vardır
(bkz. [7. bölüm](07-frekans-rehberi.md)).

## 2.5 Bant, kanal, kanal aralığı ve adım

- **Bant**: Belirli bir amaca veya kullanıcıya ayrılmış frekans aralığı
  (ör. 144–146 MHz amatör 2 m bandı).
- **Bant planı**: Bir bandın içinin hangi işe ayrıldığını gösteren tablo:
  CW bölümü, SSB bölümü, röle çıkışları, uydu bölümü vb. (bkz. [6. bölüm](06-amator-telsizcilik.md#65-bant-planları)).
- **Kanal**: Bant içinde, merkez frekansı ve genişliği tanımlı bir "şerit".
- **Kanal aralığı (channel spacing)**: Komşu iki kanalın merkez frekansları
  arasındaki fark.

| Kanal aralığı | Nerede kullanılır |
|---------------|-------------------|
| 6,25 kHz | Bazı dijital sistemler, PMR446 dijital |
| 8,33 kHz | Avrupa havacılık bandı (yeni kanal yapısı) |
| 12,5 kHz | Amatör FM (IARU Bölge 1 kanal ızgarası), PMR446 analog, profesyonel telsiz |
| 25 kHz | Eski amatör kanal ızgarası, havacılık (eski), denizcilik |
| 100 kHz | FM yayın radyosu (Avrupa'da 100 kHz katları) |

- **Adım (step)**: Telsizde `UP`/`DOWN`'a her basışta frekansın değiştiği miktar.
  Firmware **0,01 kHz'den 500 kHz'e kadar** 24 farklı adım sunar:

  `0,01` · `0,05` · `0,1` · `0,25` · `0,5` · `1` · `1,25` · `2,5` · `5` · `6,25` ·
  `8,33` · `9` · `10` · `12,5` · `15` · `20` · `25` · `30` · `50` · `100` · `125` ·
  `200` · `250` · `500` kHz

  Adım, **kanal aralığına eşit** seçilmelidir. Aksi halde `UP`/`DOWN` ile kanal
  merkezlerine denk gelemezsiniz. Çok küçük adımlar (0,01–1 kHz) SSB ve CW'de
  ince ayar içindir.

## 2.6 Telsiz ekranında frekans okuma

Telsiz frekansı **MHz** cinsinden, büyük rakamlarla gösterir:

```
 145.500 00
 └┬┘ └┬┘ └┬┘
  │   │   └── 10 Hz basamakları (küçük rakamlar)
  │   └────── kHz basamakları  (500 → 500 kHz)
  └────────── MHz
```

- `145.500` → 145 MHz + 500 kHz = **145,500 MHz** (Türkçede ondalık ayırıcı virgüldür;
  telsiz İngilizce düzende **nokta** kullanır).
- `433.650` → 433,650 MHz.
- `1296.000` gibi 1 GHz üstü frekanslar 4 haneli MHz ile gösterilir.

**Frekans girme**: VFO modunda rakamları sırayla yazarsınız. `1 4 5 5 0 0` → `145.500`.
Giriş sırasında `EXIT` son rakamı siler (ayrıntılar
[9. bölümde](09-cihaz-kullanimi.md#95-frekans-girme-ve-ayarlama)).

## 2.7 Bant genişliği

**Bant genişliği (bandwidth, BW)**, bir sinyalin spektrumda kapladığı genişliktir.
Bir alıcı filtresinin bant genişliği ise alıcının "ne kadar geniş bir pencereden"
baktığıdır.

| Sinyal | Yaklaşık bant genişliği |
|--------|-------------------------|
| CW (Mors) | 100–500 Hz |
| SSB ses | ≈ 2,4–2,8 kHz |
| AM ses (havacılık) | ≈ 6–8 kHz |
| Dar FM (NFM, ±2,5 kHz sapma) | ≈ 11 kHz → 12,5 kHz kanala sığar |
| Geniş FM (±5 kHz sapma) | ≈ 16 kHz → 25 kHz kanala sığar |
| FM yayın radyosu (WFM) | ≈ 200 kHz |
| DVB-T televizyon | ≈ 8 MHz |

**Neden önemli?**

- Alıcı filtresi sinyalden **dar** ise sinyalin bir kısmı kesilir: ses bozulur,
  dijital veri çözülemez.
- Filtre sinyalden **geniş** ise gereksiz gürültü ve komşu kanal paraziti içeri girer.
- Telsizdeki **`W/N`** (Wide/Narrow) menüsü bu filtreyi seçer: `WIDE` ≈ 25 kHz kanal,
  `NARROW` ≈ 12,5 kHz kanal. **`SetNFM`** ile dar mod daha da daraltılabilir
  (`NARROWER` ≈ 6,25 kHz).
- Radyosonda, EPIRB ve AIS uygulamaları **geniş (WIDE) FM** ister, çünkü veri
  sinyalleri geniştir.

## 2.8 Taşıyıcı, yan bantlar ve sinyalin "şekli"

- **Taşıyıcı (carrier)**: Bilgi taşımayan, tek frekanslı saf sinüs dalgası. Telsizin
  ekranında gördüğünüz frekans genellikle taşıyıcının frekansıdır.
- **Modülasyon**: Taşıyıcının bilgiye (ses, veri) göre değiştirilmesi.
- **Yan bantlar (sidebands)**: Modülasyon sonucunda taşıyıcının iki yanında oluşan
  ve bilgiyi taşıyan spektrum bileşenleri.

```
   Güç
    ▲               AM sinyali (1 kHz ton ile)
    │                    │
    │              │     │     │
    │              │     │     │
    └──────────────┴─────┴─────┴────────▶ Frekans
               f-1 kHz   f   f+1 kHz
               (alt yan) (taşıyıcı) (üst yan)
```

Modülasyon türleri [4. bölümde](04-modulasyon-ve-sinyal-turleri.md) ayrıntılı anlatılıyor.

## 2.9 Gürültü

**Gürültü**, istenen sinyalin dışında kalan her şeydir. Kaynakları:

| Kaynak | Açıklama |
|--------|----------|
| **Termal gürültü** | Her iletkende ısıdan kaynaklanan rastgele elektron hareketi. Fiziksel bir alt sınırdır. |
| **Alıcının kendi gürültüsü** | Yükselteçlerin eklediği gürültü (gürültü figürü, NF) |
| **Atmosferik / kozmik gürültü** | Şimşek, güneş, galaksi. HF'de baskın, VHF/UHF'de azdır. |
| **İnsan kaynaklı gürültü (QRM)** | Anahtarlamalı adaptörler, LED sürücüler, bilgisayarlar, motorlar, elektrik hatları. Şehirde VHF'de en büyük sorun. |

- **Gürültü tabanı (noise floor)**: Sinyal yokken alıcının ölçtüğü seviye. Spektrum
  analizöründe "çimen" gibi görünen alt çizgidir.
- **SNR (Signal-to-Noise Ratio)**: Sinyalin gürültüye oranı. Yüksek SNR temiz ses demektir.
- **Squelch (susturucu)**, gürültüyü duymamak için hoparlörü sinyal gelene kadar kapalı tutar.

Sayısal değerler ve dBm hesapları [3. bölümde](03-desibel-ve-sinyal-olcumu.md#37-gürültü-gürültü-tabanı-ve-snr).

## 2.10 Parazit türleri: harmonik, imaj, intermodülasyon, doyma

Yeni başlayanların en çok şaşırdığı şey, **olmaması gereken frekanslarda sinyal
duymaktır**. Bunun birkaç fiziksel sebebi vardır:

### Harmonikler

Bir verici, temel frekansının **tam katlarında** da zayıf sinyaller üretir. 145 MHz'de
gönderen bir vericinin 2. harmoniği 290 MHz'de, 3. harmoniği 435 MHz'dedir.
Vericilerin çıkışındaki **alçak geçiren filtre** bunları bastırır. Bozuk veya
uygunsuz filtreli bir verici başka servislere parazit yapar.

### İmaj (ayna) frekansı

Süperheterodin alıcılarda (bkz. [2.13](#213-alıcı-nasıl-çalışır-süperheterodin-ve-sdr)),
istenen frekansın dışında, ara frekansın iki katı uzaklıktaki bir sinyal de aynı
sonucu verir. Buna **imaj** denir. Alıcı bu sinyali sanki ayarlı frekanstaymış gibi duyar.

### İntermodülasyon (IMD)

İki güçlü sinyal (f₁ ve f₂) alıcının doğrusal olmayan katlarına girdiğinde
**yeni frekanslar** üretir: `2f₁ − f₂`, `2f₂ − f₁`, `f₁ + f₂` gibi.

**Örnek**: 145,000 ve 145,200 MHz'de iki güçlü verici varsa,
2 × 145,000 − 145,200 = **144,800 MHz**'de (APRS frekansı!) hayalet bir sinyal
duyabilirsiniz. Gerçekte orada kimse yoktur.

### Doyma ve duyarlılığın düşmesi (desensitization)

Çok güçlü bir sinyal, alıcının ön katını **doyurur**. Alıcı zayıf sinyalleri
duyamaz olur, AGC (otomatik kazanç kontrolü) kazancı kısar, ses bozulur.
Şehir merkezinde, tepelerde, verici direklerinin yanında sık görülür.

**Ne yapılabilir?**

- Firmware'in ve uygulamaların **zayıflatıcı (ATT)** ayarlarını kullanın:
  spektrumda `LNA`/`PGA`, Fox Hunt ve Sig Finder'da `0 dB … 27 dB`, radyosonda
  uygulamalarında `3` tuşu.
- Daha **dar bantlı, ayarlı bir anten** kullanın.
- Mümkünse araya harici bir **bant geçiren filtre** koyun.
- Güçlü vericiden uzaklaşın ya da anteni ondan uzağa yönlendirin.

> [!NOTE]
> Bu telsizin alıcısı, fiyatı düşük tutmak için basit bir ön kat kullanır. Pahalı
> telsizlerdeki ayarlı ön filtreler yoktur. Bu yüzden yukarıdaki etkiler, özellikle
> **AM** dinlerken, normalden daha sık görülür.

## 2.11 Doppler kayması

Verici ile alıcı birbirine göre hareket ediyorsa, alınan frekans değişir: yaklaşırken
**yükselir**, uzaklaşırken **düşer**. Ambulans sireninin geçerken sesinin değişmesiyle
aynı olgudur.

```
Δf = f × v / c          (v: bağıl hız, c: ışık hızı)
```

| Kaynak | Bağıl hız | 145,8 MHz'de | 437 MHz'de |
|--------|-----------|--------------|------------|
| Otomobil (100 km/s) | 28 m/s | ≈ 13 Hz | ≈ 40 Hz |
| Uçak (900 km/s) | 250 m/s | ≈ 120 Hz | ≈ 360 Hz |
| ISS (yörünge hızı ≈ 7,66 km/s) | en fazla ≈ 7,6 km/s | **± 3,5 kHz** | **± 10 kHz** |

ISS veya amatör uydu dinlerken frekansı geçiş boyunca elle kaydırmanız gerekir:
geçişin başında biraz yukarı, sonunda biraz aşağı. 2 m'de ±3,5 kHz, geniş FM ile
çoğunlukla tolere edilir.

## 2.12 Spektrum analizörü nedir, nasıl okunur?

**Spektrum analizörü**, belirli bir frekans aralığını tarayıp her frekanstaki sinyal
seviyesini **grafik olarak** gösteren alettir. Bu firmware'de iki tane vardır:

- **Yerleşik spektrum analizörü**: `F` + `5`
- **Spectrum3D uygulaması**: `F` + `7` → Spectrum3D. Spektrumu zaman içinde
  "dağ silsilesi" gibi 3B gösterir.

### Spektrum ekranının anatomisi

```
 ┌──────────────────────────────────────────────┐
 │ durum: adım, tetik seviyesi, modülasyon, BW   │ ← üst satır
 │ 145.500                                       │ ← en güçlü sinyalin frekansı
 │                    ▌                          │
 │                    ▌          ▌               │ ← her sütun bir frekans noktası
 │            ▖       ▌          ▌▖              │   yükseklik = sinyal gücü
 │▂▁▂▁▂▁▂▁▂▁▂█▂▁▂▁▂▁▂█▂▁▂▁▂▁▂▁▂▁█▌▂▁▂▁▂▁▂▁▂▁▂▁▂▁│ ← gürültü tabanı ("çimen")
 │ 145.000          145.500            146.000   │ ← frekans ekseni
 └──────────────────────────────────────────────┘
```

**Okuma kuralları**

1. **Yatay eksen frekanstır.** Soldan sağa frekans artar. Ortadaki çizgi genellikle
   merkez (VFO) frekansıdır.
2. **Dikey eksen sinyal gücüdür.** Çubuk ne kadar yüksekse sinyal o kadar güçlüdür.
3. **Gürültü tabanı** sürekli titreyen, düşük, "çimen" gibi bir çizgidir. Asıl
   sinyaller onun üzerinde **belirgin tepeler** olarak görünür.
4. **Dar ve sabit bir tepe** → Taşıyıcı: FM istasyonu (konuşmuyor olsa bile) veya
   bir veri vericisi.
5. **Aniden çıkıp kaybolan tepe** → Biri gönderip bıraktı (PTT). Röle çıkışında
   bunu sık görürsünüz.
6. **Geniş, düz bir "plato"** → Geniş bantlı sinyal: FM yayın, dijital TV veya
   güçlü bir parazit kaynağı.
7. **Düzenli aralıklarla tekrarlanan tepeler** → Genellikle bir **parazit**
   (anahtarlamalı güç kaynağı, bilgisayar saatinin harmonikleri) veya
   **intermodülasyon** ürünü.
8. **Tüm grafiğin birden yükselmesi** → Alıcı yakındaki çok güçlü bir sinyalle
   doyuyor. Zayıflatmayı artırın.

### Tarama adımı ve nokta sayısı

- **Tarama adımı (scan step)**: İki ölçüm noktası arasındaki frekans farkı.
- **Nokta sayısı**: Ekranda kaç frekansın ölçüleceği (firmware'de 128, 64, 32, 16).
- **Toplam açıklık (span)** = adım × nokta sayısı. 12,5 kHz × 64 nokta = **800 kHz** pencere.
- Adım çok büyükse **dar sinyaller iki ölçüm noktasının arasına düşüp kaybolabilir.**
  Kanal aralığından büyük adım seçmeyin.

Spektrum analizörünün tuşları [9. bölümde](09-cihaz-kullanimi.md#914-spektrum-analizörü-f--5).

### Ses spektrumu ile RF spektrumunu karıştırmayın

- **RF spektrumu** (yerleşik spektrum, Spectrum3D): Antene gelen **radyo frekanslarını**
  gösterir. Birimi MHz'dir.
- **Ses (AF) spektrumu** (AF Spectro uygulaması): Demodüle edilmiş sesin içindeki
  **ses frekanslarını** gösterir. Birimi Hz/kHz'dir. Örneğin bir APRS paketinin
  1200 ve 2200 Hz tonlarını, DTMF tonlarını, CTCSS'yi görmenizi sağlar.

## 2.13 Alıcı nasıl çalışır? (süperheterodin ve SDR)

Antene aynı anda yüzlerce sinyal gelir. Alıcının işi, **istenen tek sinyali seçmek,
yükseltmek ve içindeki bilgiyi çıkarmaktır**.

```
 Anten → [Ön filtre] → [LNA] → [Karıştırıcı] → [IF filtresi] → [IF yükselteç] → [Demodülatör] → [Ses yükselteci] → Hoparlör
                                    ↑
                              [Yerel osilatör (LO)]
                                    ↑
                           [PLL sentezleyici] ← [Kristal referans]
```

| Blok | Görevi |
|------|--------|
| **Ön filtre** | Bant dışı güçlü sinyalleri azaltmak (bu telsizde basittir) |
| **LNA** (Low Noise Amplifier) | Zayıf sinyali, çok az gürültü ekleyerek yükseltmek |
| **Karıştırıcı (mixer)** | Gelen sinyali yerel osilatörle çarpıp sabit bir **ara frekansa (IF)** indirmek |
| **Yerel osilatör (LO)** | Ayarlı frekansa göre değişen bir referans sinyal üretmek |
| **PLL sentezleyici** | LO'yu kristal referansa kilitleyip istenen frekansı üretmek |
| **IF filtresi** | Kanal genişliğini belirlemek: `W/N` ayarı buradadır |
| **AGC** | Sinyal güçlüyse kazancı otomatik azaltmak |
| **Demodülatör** | FM, AM veya SSB sinyalinden sesi çıkarmak |
| **Squelch** | Sinyal yokken sesi kapatmak |
| **Ses yükselteci** | Hoparlörü sürmek |

- **Süperheterodin**: Gelen sinyali sabit bir ara frekansa indirip seçiciliği o
  frekansta sağlayan klasik mimari.
- **Doğrudan dönüşüm / sıfır IF**: Sinyal doğrudan temel banda (0 Hz civarına) indirilir.
  BK4829 gibi tek yongalı alıcılarda bu tür yaklaşımlar ve **dijital sinyal işleme (DSP)**
  birlikte kullanılır.
- **SDR (Software Defined Radio)**: Sinyalin büyük kısmının yazılımla işlendiği radyo.
  BK4829 içinde dijital işleme vardır; tam bir SDR değildir ama birçok ayarı
  yazmaçlarla (register) değiştirilebilir. Uygulamalardaki "REG_xx" ifadeleri bu yazmaçlardır.

## 2.14 Verici nasıl çalışır?

```
 Mikrofon → [Mikrofon yükselteci] → [Modülatör] → [PLL / VCO] → [Sürücü] → [PA güç yükselteci] → [Alçak geçiren filtre] → Anten
                                                       ↑
                                                [Kristal referans]
```

- **Modülatör**: Sesi taşıyıcıya yükler. FM'de VCO'nun frekansını sesle oynatır.
- **PA (Power Amplifier)**: Sinyali watt seviyesine çıkarır. `Power` menüsündeki
  `LOW 1` … `HIGH` seviyeleri PA'nın çıkışını ayarlar.
- **Alçak geçiren filtre**: Harmonikleri bastırır.
- **TX/RX anahtarı**: Aynı anteni alıcı ve verici paylaşır; `PTT`'ye basınca anten
  vericiye bağlanır. Bu yüzden el telsizi **aynı anda hem gönderip hem alamaz
  (simpleks / yarı dupleks)**. Bir uydu üzerinden kendi sesinizi duyamamanızın
  sebebi budur.

## 2.15 Özet

| Kavram | Bir cümlede |
|--------|-------------|
| Elektromanyetik dalga | Elektrik ve manyetik alanın birbirini besleyerek ışık hızında yayılması |
| λ = 300 / f | 145 MHz ≈ 2 m, 435 MHz ≈ 70 cm |
| VHF / UHF | 30–300 MHz / 300 MHz–3 GHz |
| Kanal aralığı | Komşu kanalların merkezleri arasındaki fark (12,5 / 25 kHz) |
| Adım | `UP`/`DOWN`'un frekansı değiştirdiği miktar; kanal aralığına eşit seçilmeli |
| Bant genişliği | Sinyalin spektrumda kapladığı yer; `W/N` alıcı filtresini seçer |
| Gürültü tabanı | Sinyal yokken ölçülen seviye; sinyaller bunun üstünde tepe olarak görünür |
| İntermodülasyon | İki güçlü sinyalin alıcıda üçüncü bir hayalet sinyal üretmesi |
| Doppler | Hareket eden kaynağın frekansının kayması; ISS'te ±3,5 kHz (2 m) |
| Spektrum analizörü | Frekansa karşı sinyal gücü grafiği (`F` + `5`) |

---

[← Önceki: Elektrik temelleri](01-elektrik-ve-elektronik.md) · [İçindekiler](README.md) · [Sonraki: Desibel ve sinyal ölçümü →](03-desibel-ve-sinyal-olcumu.md)
