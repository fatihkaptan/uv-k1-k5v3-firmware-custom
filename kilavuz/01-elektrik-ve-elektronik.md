# 1. Elektrik ve Elektronik Temelleri

[← İçindekiler](README.md) · [Sonraki: Radyo dalgaları ve spektrum →](02-radyo-dalgalari-ve-spektrum.md)

Bir telsiz, temelde elektriği radyo dalgasına, radyo dalgasını yeniden elektriğe
çeviren bir cihazdır. Bu bölüm, sonraki bölümlerde geçecek elektrik kavramlarını
sıfırdan anlatır. Formüller kısa tutuldu; her formülün yanında telsizden bir örnek var.

## İçindekiler

1. [Yük, gerilim, akım](#11-yük-gerilim-akım)
2. [Direnç ve Ohm Yasası](#12-direnç-ve-ohm-yasası)
3. [Güç ve enerji](#13-güç-ve-enerji)
4. [Seri ve paralel bağlantı](#14-seri-ve-paralel-bağlantı)
5. [Doğru akım (DC) ve alternatif akım (AC)](#15-doğru-akım-dc-ve-alternatif-akım-ac)
6. [Frekans ve periyot](#16-frekans-ve-periyot)
7. [Tepe, tepeden tepeye ve RMS değer](#17-tepe-tepeden-tepeye-ve-rms-değer)
8. [Kondansatör (kapasitör)](#18-kondansatör-kapasitör)
9. [Bobin (endüktör)](#19-bobin-endüktör)
10. [Reaktans ve empedans](#110-reaktans-ve-empedans)
11. [Rezonans](#111-rezonans)
12. [Filtreler](#112-filtreler)
13. [Transformatör ve balun](#113-transformatör-ve-balun)
14. [Yarı iletkenler: diyot, transistör, entegre](#114-yarı-iletkenler-diyot-transistör-entegre)
15. [Kristal osilatör ve ppm](#115-kristal-osilatör-ve-ppm)
16. [Analog ve dijital, ADC ve DAC](#116-analog-ve-dijital-adc-ve-dac)
17. [Piller: Li-ion temelleri ve telsizin pili](#117-piller-li-ion-temelleri-ve-telsizin-pili)
18. [Direnç renk kodları](#118-direnç-renk-kodları)
19. [Multimetre kullanımı](#119-multimetre-kullanımı)
20. [Güvenlik](#120-güvenlik)
21. [Özet tablo](#121-özet-tablo)

---

## 1.1 Yük, gerilim, akım

Elektriği anlamanın en kolay yolu **su borusu benzetmesidir**:

| Elektrik | Su benzetmesi | Birim | Sembol |
|----------|---------------|-------|--------|
| **Yük** (elektron miktarı) | Su miktarı | Coulomb (C) | Q |
| **Gerilim** (voltaj, potansiyel farkı) | Su basıncı | Volt (V) | V veya U |
| **Akım** (saniyede geçen yük) | Saniyede akan su | Amper (A) | I |
| **Direnç** (akışa karşı koyma) | Borunun darlığı | Ohm (Ω) | R |

- **Gerilim**, iki nokta arasındaki "itme kuvvetidir". Telsizin pili yaklaşık
  **7,4 V** (tam doluyken ~8,3–8,4 V) gerilim sağlar.
- **Akım**, devreden saniyede geçen elektrik yüküdür. Telsiz dinlemedeyken birkaç
  on mA, 5 W'ta gönderirken 1–1,5 A civarı akım çekebilir (değerler cihaza göre değişir).
- Akım yalnızca **kapalı bir devrede** akar: kaynaktan çıkar, yükten geçer, kaynağa döner.

**Birim önekleri** (radyoda sürekli karşınıza çıkar):

| Önek | Sembol | Çarpan | Örnek |
|------|--------|--------|-------|
| piko | p | 10⁻¹² | 10 pF kondansatör |
| nano | n | 10⁻⁹ | 100 nH bobin |
| mikro | µ | 10⁻⁶ | 0,2 µV alıcı hassasiyeti |
| mili | m | 10⁻³ | 500 mW çıkış gücü, 1600 mAh pil |
| — | — | 1 | 1 V, 1 A, 1 Ω |
| kilo | k | 10³ | 12,5 kHz kanal aralığı, 4,7 kΩ direnç |
| mega | M | 10⁶ | 145 MHz |
| giga | G | 10⁹ | 1,2 GHz |

## 1.2 Direnç ve Ohm Yasası

**Direnç**, akımın akmasını zorlaştıran özelliktir. Bütün iletkenlerin biraz
direnci vardır; direnç elemanları (rezistörler) bilerek belirli bir değerde üretilir.

**Ohm Yasası** elektriğin en temel formülüdür:

```
V = I × R        I = V / R        R = V / I
```

Akılda tutmak için üçgen:

```
      ┌───┐
      │ V │
   ┌──┴───┴──┐
   │ I  ×  R │
   └─────────┘
 Bulmak istediğinizi kapatın; kalan ikisi formülü verir.
```

**Örnekler**

| Soru | Çözüm |
|------|-------|
| 7,4 V'luk pile 1 kΩ direnç bağlanırsa ne kadar akım geçer? | I = 7,4 / 1000 = **7,4 mA** |
| Bir LED devresinde 5 V kaynaktan 20 mA geçirmek, LED üzerinde 2 V düşmesi isteniyor. Seri direnç? | Dirençte kalan 3 V → R = 3 / 0,02 = **150 Ω** |
| Telsiz 7,4 V'ta 1,5 A çekiyorsa devrenin eşdeğer direnci? | R = 7,4 / 1,5 ≈ **4,9 Ω** |

> [!NOTE]
> Ohm yasası **doğru akımda** doğrudan geçerlidir. Radyo frekanslarında direncin
> yerini **empedans** alır (bkz. [1.10](#110-reaktans-ve-empedans)), ama mantık aynıdır.

## 1.3 Güç ve enerji

**Güç** (P), birim zamanda harcanan veya aktarılan enerjidir. Birimi **Watt (W)**.

```
P = V × I        P = I² × R        P = V² / R
```

**Örnekler**

- Telsiz 7,4 V'ta 1,5 A çekiyorsa pilden çekilen güç: P = 7,4 × 1,5 ≈ **11 W**.
  Antene giden güç ise ~5 W'tır. Aradaki fark **ısıya** dönüşür. Bu yüzden uzun
  gönderimde telsiz ısınır. Vericinin **verimi** burada yaklaşık %45'tir.
- 50 Ω'luk bir antene 5 W veriliyorsa antendeki RMS gerilim:
  V = √(P × R) = √(5 × 50) ≈ **15,8 V**.

**Enerji** gücün zamanla çarpımıdır: **E = P × t**. Pillerde enerji genellikle
**Wh (watt-saat)** veya dolaylı olarak **mAh (miliamper-saat)** ile ifade edilir:

```
Wh = V × Ah        (1600 mAh = 1,6 Ah)
```

| Pil | Nominal gerilim | Kapasite | Enerji |
|-----|-----------------|----------|--------|
| UV-K5 standart | 7,4 V | 1600 mAh | ≈ 11,8 Wh |
| UV-K5 büyük | 7,4 V | 2200 mAh | ≈ 16,3 Wh |
| UV-K5 USB-C / yüksek kapasite | 7,4 V | 3500 mAh | ≈ 25,9 Wh |
| UV-K1 | 7,4 V | 1400 mAh | ≈ 10,4 Wh |
| UV-K1 büyük | 7,4 V | 2500 mAh | ≈ 18,5 Wh |

**Pil süresi kabaca** = kapasite / ortalama akım. 1600 mAh'lik pil, ortalama 80 mA
çeken (çoğunlukla dinleme, arada kısa gönderme) bir kullanımda yaklaşık
1600 / 80 = **20 saat** dayanır. Sürekli gönderme yapılırsa bu süre bir saatin
altına iner. Pil tasarrufu (`BatSav`), düşük güç ve kısa arka ışık süresi bu
yüzden önemlidir.

## 1.4 Seri ve paralel bağlantı

| | Seri | Paralel |
|---|------|---------|
| Şekil | `──R1──R2──` | `──┬─R1─┬──` / `  └─R2─┘  ` |
| Akım | Her elemandan **aynı** akım geçer | Akım kollara **bölünür** |
| Gerilim | Gerilim elemanlara **bölünür** | Her elemanda **aynı** gerilim |
| Direnç | R = R1 + R2 | 1/R = 1/R1 + 1/R2 |
| Pil hücreleri | Gerilim toplanır (2 × 3,7 V = 7,4 V) | Kapasite toplanır |

Telsizin pili **iki Li-ion hücrenin seri** bağlanmasıyla oluşur. Literatürde bu
**"2S"** olarak yazılır: 2 × 3,7 V = 7,4 V nominal, 2 × 4,2 V = 8,4 V tam dolu.

**Gerilim bölücü**: İki seri direnç, gerilimi oranlarında böler. Telsiz pil
voltajını ölçerken bu yöntemi kullanır. 8,4 V doğrudan mikrodenetleyiciye
verilemez; bir bölücü onu ADC'nin ölçebileceği aralığa indirir. `BatCal` menüsü
bu ölçümün kalibrasyonudur.

```
Vçıkış = Vgiriş × R2 / (R1 + R2)
```

## 1.5 Doğru akım (DC) ve alternatif akım (AC)

- **DC (Direct Current)**: Akım tek yönde ve sabit akar. Pil, USB, telsizin iç
  besleme hatları DC'dir.
- **AC (Alternating Current)**: Akımın yönü ve büyüklüğü periyodik olarak değişir.
  Şebeke elektriği (230 V, 50 Hz), ses sinyali ve **bütün radyo sinyalleri** AC'dir.

```
DC:  ────────────────────        AC (sinüs):   ╭─╮   ╭─╮   ╭─╮
                                               ╯   ╰─╯   ╰─╯   ╰
```

Telsizin içinde ikisi bir aradadır: pil DC verir. Osilatörler, karıştırıcılar ve
yükselteçler bu DC'yi kullanarak **çok yüksek frekanslı AC** (radyo sinyali) üretir.

## 1.6 Frekans ve periyot

**Frekans** (f), bir AC sinyalin saniyede kaç kez tekrarlandığıdır. Birimi
**Hertz (Hz)**; 1 Hz = saniyede 1 tekrar.

**Periyot** (T), bir tam tekrarın süresidir:

```
T = 1 / f        f = 1 / T
```

| Sinyal | Frekans | Periyot |
|--------|---------|---------|
| Şebeke elektriği | 50 Hz | 20 ms |
| CTCSS tonu | 88,5 Hz | ≈ 11,3 ms |
| Ses (insan konuşması) | 300–3000 Hz | 3,3 ms – 0,33 ms |
| Röle açma tonu | 1750 Hz | ≈ 0,57 ms |
| FM yayın radyosu | 100 MHz | 10 ns |
| 2 m amatör bandı | 145 MHz | ≈ 6,9 ns |
| 70 cm amatör bandı | 435 MHz | ≈ 2,3 ns |

Frekans, radyoda "**hangi istasyonda olduğunuzu**" belirler. Ayrıntılar
[2. bölümde](02-radyo-dalgalari-ve-spektrum.md).

## 1.7 Tepe, tepeden tepeye ve RMS değer

Bir sinüs sinyalinin büyüklüğü üç şekilde ifade edilir:

```
     +Vtepe ┤   ╭──╮
            │  ╱    ╲             Vtepe-tepe = 2 × Vtepe
          0 ┼─╯──────╲──────╱─    Vrms = Vtepe / √2 ≈ 0,707 × Vtepe
            │          ╲    ╱
     −Vtepe ┤           ╰──╯
```

- **Tepe (peak)**: Sıfırdan en yüksek noktaya.
- **Tepeden tepeye (peak-to-peak, PP)**: En alttan en üste. AF Scope uygulaması
  sinyal genliğini `PP` olarak gösterir.
- **RMS (etkin değer)**: Aynı ısıyı üreten eşdeğer DC değeri. Güç hesapları RMS ile
  yapılır. Şebekenin 230 V'u bir RMS değeridir; tepe değeri ≈ 325 V'tur.

## 1.8 Kondansatör (kapasitör)

**Kondansatör**, iki iletken plaka arasında yalıtkan bulunan ve **elektrik yükü
depolayan** elemandır. Birimi **Farad (F)**; radyoda pF ve nF, besleme devrelerinde
µF kullanılır.

Davranışı:

- **DC'yi geçirmez** (dolduktan sonra akım kesilir).
- **AC'yi geçirir**; frekans yükseldikçe daha kolay geçirir.

Telsizdeki görevleri:

- **Kuplaj**: İki katı birbirine bağlarken DC'yi engelleyip sinyali geçirmek.
- **Dekuplaj / filtreleme**: Besleme hatlarındaki gürültüyü toprağa atmak.
- **Ayarlı devreler**: Bobinle birlikte rezonans devresi kurmak.
- **Zamanlama**: RC devreleri (direnç + kondansatör) ile gecikme ve filtre.

## 1.9 Bobin (endüktör)

**Bobin**, sarılmış bir iletkendir ve akım geçtiğinde **manyetik alanda enerji
depolar**. Birimi **Henry (H)**; radyoda nH ve µH kullanılır.

Davranışı kondansatörün tersidir:

- **DC'yi kolayca geçirir** (yalnızca telin küçük direnci vardır).
- **AC'ye karşı koyar**; frekans yükseldikçe daha çok karşı koyar.

Telsizdeki görevleri: RF şoklar (RF'nin besleme hattına kaçmasını önlemek),
ayarlı devreler, filtreler, empedans uyumlandırma ve vericinin çıkışındaki
**alçak geçiren filtre** (harmonikleri bastırmak için).

## 1.10 Reaktans ve empedans

Kondansatör ve bobinin AC'ye gösterdiği "frekansa bağlı direnç" **reaktans** (X)
olarak adlandırılır; birimi yine Ω'dur.

```
Bobin:        XL = 2π × f × L          (frekans ↑ → XL ↑)
Kondansatör:  XC = 1 / (2π × f × C)    (frekans ↑ → XC ↓)
```

**145 MHz'de örnek**

| Eleman | Değer | Reaktans |
|--------|-------|----------|
| Bobin | 100 nH | XL = 2π × 145·10⁶ × 100·10⁻⁹ ≈ **91 Ω** |
| Kondansatör | 10 pF | XC = 1 / (2π × 145·10⁶ × 10·10⁻¹²) ≈ **110 Ω** |

Aynı 10 pF'lık kondansatör 1 kHz'lik ses sinyaline yaklaşık **16 MΩ** gösterir.
Yani küçük bir kondansatör RF'i geçirip sesi neredeyse tamamen durdurabilir.
Filtrelerin temeli budur.

**Empedans** (Z), direnç (R) ile reaktansın (X) birleşimidir ve AC'deki toplam
"karşı koymayı" ifade eder:

```
Z = R + jX          |Z| = √(R² + X²)
```

`j`, reaktansın dirençle 90° faz farkında olduğunu gösteren matematiksel bir işarettir.
Pratikte bilmeniz gerekenler:

- Telsiz, kablo ve anten dünyasında standart empedans **50 Ω**'dur.
- Verici en iyi verimi, çıkışına **50 Ω'luk saf direnç** gibi davranan bir yük
  bağlandığında verir.
- Empedans uyumsuzluğu gücün bir kısmının **geri yansımasına** yol açar; bunun
  ölçüsü **SWR**'dir (bkz. [5. bölüm](05-antenler-ve-yayilim.md#56-swr-duran-dalga-oranı)).

## 1.11 Rezonans

Bir bobin ile bir kondansatör aynı devrede olduğunda, **XL = XC** olduğu tek bir
frekans vardır. Buna **rezonans frekansı** denir:

```
f₀ = 1 / (2π × √(L × C))
```

**Örnek**: L = 100 nH ve C = 12 pF → f₀ ≈ **145,3 MHz**. Bu devre 2 m bandına ayarlıdır.

Rezonansın radyodaki önemi:

- **Ayar (tuning)**: Eski radyolardaki ayar düğmesi aslında bir kondansatörü
  değiştirip rezonans frekansını kaydırır.
- **Seçicilik**: Rezonans devresi kendi frekansını geçirir, diğerlerini zayıflatır.
- **Antenler** de rezonans yapan yapılardır. Belirli bir uzunluktaki tel, belirli
  bir frekansta en iyi çalışır (bkz. [5. bölüm](05-antenler-ve-yayilim.md)).

**Q faktörü**: Rezonansın ne kadar "keskin" olduğunu gösterir. Yüksek Q, dar bant
ve iyi seçicilik; düşük Q, geniş bant demektir.

## 1.12 Filtreler

| Filtre | Geçirdiği | Telsizde örnek |
|--------|-----------|----------------|
| **Alçak geçiren (LPF)** | Belirli frekansın **altını** | Verici çıkışında harmonikleri bastırır; ses yolunda 3 kHz üstünü keser |
| **Yüksek geçiren (HPF)** | Belirli frekansın **üstünü** | Ses yolunda 300 Hz altını keser; CTCSS tonlarının hoparlörden duyulmasını önler |
| **Bant geçiren (BPF)** | Yalnızca bir **aralığı** | Ara frekans (IF) filtresi: istenen kanalı seçer |
| **Bant durduran (notch)** | Bir aralık **dışını** | Belirli bir paraziti yok etmek |

**Kesim frekansı**: Filtrenin sinyali yarı güce (−3 dB) indirdiği frekanstır.

> [!IMPORTANT]
> UV-K5 / UV-K1 alıcısının girişinde **dar, ayarlı bir bant filtresi yoktur**. Alıcı
> çok geniş bir frekans aralığını aynı anda "görür". Güçlü bir verici (baz istasyonu,
> yayın kulesi) yakınsa alıcı doyabilir ve **parazit, hışırtı, hayalet sinyaller**
> duyulur. Bu donanımsal bir sınırlamadır; firmware yalnızca kısmen iyileştirebilir.
> Uygulamalardaki "ATT" (zayıflatıcı) ayarları bu yüzden vardır.

Firmware'in ses yolundaki filtrelerin bir kısmını kapatan **RAW** modu (AF Scope,
radyosonda uygulamaları), sinyali filtrelenmeden görmek içindir.

## 1.13 Transformatör ve balun

**Transformatör**, iki bobinin manyetik olarak bağlanmasıdır. Gerilimi ve empedansı
dönüştürür:

```
V2 / V1 = N2 / N1          Z2 / Z1 = (N2 / N1)²       (N: sarım sayısı)
```

**Balun** (BALanced–UNbalanced), dengeli bir anteni (dipol) dengesiz koaksiyel
kabloya bağlamak için kullanılan özel bir transformatördür. Kablonun dış
yüzeyinden akan istenmeyen akımları (**ortak mod akımı**) engeller.

**Ferrit**: Kablo üzerine takılan manyetik halkalar. Kablodan geçen yüksek frekanslı
istenmeyen akımı bastırır. KISS TNC uygulamasında USB kablosuna ferrit takılması
önerilmesinin sebebi budur: telsiz gönderime geçtiğinde kablonun topladığı RF,
USB bağlantısını sıfırlayabilir.

## 1.14 Yarı iletkenler: diyot, transistör, entegre

- **Diyot**: Akımı yalnızca bir yönde geçirir. Doğrultma (AC → DC), koruma ve
  **AM demodülasyonu** (zarf algılama) için kullanılır. **LED**, ışık veren diyottur.
  Telsizdeki yeşil (RX) ve kırmızı (TX) LED'ler ve fener LED'i buna örnektir.
- **Transistör**: Küçük bir sinyalle büyük bir akımı kontrol eder. İki ana görevi
  vardır: **yükselteç** (sinyali büyütmek) ve **anahtar** (açıp kapamak).
  Vericinin son katındaki **güç yükselteci (PA)**, ~5 W üreten MOSFET
  transistörlerden oluşur.
- **Entegre devre (IC)**: Binlerce, milyonlarca transistörün tek bir yonga
  üzerinde birleşimidir. Telsizin kalbi birkaç entegredir:
  - **BK4829**: Bütün alıcı ve vericiyi tek yongada barındıran RF entegresi
  - **PY32F071**: Telsizi yöneten mikrodenetleyici
  - **BK1080**: FM yayın radyosu alıcısı
  - **PY25Q16**: 2 MiB harici flash bellek
  - **ST7565**: Ekran sürücüsü

  Ayrıntılar [8. bölümde](08-cihaz-donanimi-ve-ekran.md).

## 1.15 Kristal osilatör ve ppm

Telsizin bütün frekansları bir **kuvars kristalinden** türetilir. Kristal,
mekanik olarak çok kararlı bir rezonatördür. **PLL (faz kilitlemeli döngü)**
devresi bu referansı çarparak 145 MHz gibi yüksek frekanslar üretir.

Kristaller kusursuz değildir. Sapmaları **ppm** (parts per million, milyonda bir)
ile ifade edilir:

```
Frekans hatası (Hz) = Frekans (Hz) × ppm / 1 000 000
```

| Sapma | 145 MHz'de hata | 435 MHz'de hata |
|-------|-----------------|-----------------|
| 1 ppm | 145 Hz | 435 Hz |
| 2,69 ppm | ≈ 390 Hz | ≈ 1,17 kHz |
| 5 ppm | 725 Hz | 2,2 kHz |

FM konuşmada birkaç yüz Hz'lik hata fark edilmez. CW ve SSB'de ise ton
yüksekliğini doğrudan değiştirir. Bu yüzden:

- Bazı derlemelerin gizli menüsündeki **`FrCali`** öğesi referans kristalin kalibrasyonudur
  (v6 yayın sürümlerinde bu öğe yoktur).
- CW Keyer ve CW Decode uygulamalarındaki **`XTAL`** düzeltmesi aynı amaçla vardır.
  Varsayılan +14 adım, yani +2,69 ppm'dir.
- Kristalin frekansı **sıcaklıkla** da değişir. Soğuk bir sabahta ve sıcak bir
  arabada ölçülen hata farklı olabilir.

> [!CAUTION]
> `FrCali` değerini, bilinen doğru bir frekans referansı (kalibre sayaç, iyi bir
> SDR, GPS disiplinli kaynak) olmadan değiştirmeyin.

## 1.16 Analog ve dijital, ADC ve DAC

- **Analog sinyal**: Sürekli değişen bir büyüklük. Mikrofondan gelen ses, anten
  sinyali.
- **Dijital sinyal**: Sayılarla (0 ve 1) temsil edilen bilgi.
- **ADC (Analog-Digital Converter)**: Analog gerilimi belirli aralıklarla ölçüp
  sayıya çevirir. Telsizde pil gerilimini ölçer. Overlay uygulamaları da
  demodüle edilmiş sesi ADC ile örnekler (APRS RX'te 9,6 kHz, radyosonda
  uygulamalarında 19,2 kHz, AIS RX'te 38,4 kHz).
- **Örnekleme hızı** ve **Nyquist kuralı**: Bir sinyali doğru örneklemek için
  örnekleme hızı, sinyaldeki en yüksek frekansın **en az iki katı** olmalıdır.
  9,6 kHz örnekleme en fazla 4,8 kHz'lik sesi temsil edebilir. AF Spectro'nun
  "0–4,8 kHz" ekseni buradan gelir.
- **DAC (Digital-Analog Converter)**: Sayıyı gerilime çevirir. Ton üretimi ve
  ses çıkışı için kullanılır.

## 1.17 Piller: Li-ion temelleri ve telsizin pili

UV-K5 / UV-K1 pilleri **lityum-iyon (Li-ion)** hücrelerden oluşur.

| Özellik | Tek hücre | Telsiz pili (2S) |
|---------|-----------|------------------|
| Tam dolu | 4,2 V | ~8,3–8,4 V |
| Nominal | 3,6–3,7 V | 7,2–7,4 V |
| Boş kabul edilen | ~3,0–3,15 V | ~6,0–6,3 V |

**Firmware'in kullandığı gerilim–yüzde tabloları** (`App/helper/battery.c`):

| Pil tipi (`BatTyp`) | %100 | ≈ %50–60 | ≈ %5 | %0 |
|---------------------|------|----------|------|-----|
| 1600 mAh K5 | 8,28 V | 7,60 V'ta %25 | 7,29 V'ta %6 | 6,30 V |
| 2200 mAh K5 | 8,32 V | 7,40 V'ta %60 | 6,82 V'ta %5 | 6,30 V |
| 3500 mAh K5 | 8,37 V | 7,50 V'ta %50 | 6,20 V'ta %5 | 6,00 V |
| 1400 mAh K1 | 8,28 V | 7,58 V'ta %25 | 7,26 V'ta %6 | 6,30 V |
| 2500 mAh K1 | 8,39 V | 7,45 V'ta %55 | 6,68 V'ta %5 | 6,23 V |

- Yüzde göstergesinin doğru çalışması için gizli menüdeki **`BatTyp`** ayarı,
  takılı pile uygun olmalıdır.
- Ölçülen gerilim **8,90 V'u aşarsa** firmware aşırı gerilim kabul eder ve
  gönderimi engeller (ekranda `VOLT HIGH`).
- Gerilim kritik eşiğin altına inerse `LOW BATTERY` uyarısı çıkar, gönderim
  engellenir (`BAT LOW`).
- Gönderim sırasında gerilim kısa süreli düşer. Pil yaşlandıkça iç direnci
  arttığından bu düşüş büyür. Dinlemede iyi görünen eski bir pil, gönderimde
  telsizi kapatabilir.

**Li-ion bakım kuralları**

1. **Tamamen boşaltmayın.** Li-ion pillerde "hafıza etkisi" yoktur. Sık sık ve kısmen
   şarj etmek pile zarar vermez, aksine ömrünü uzatır.
2. **Uzun süre kullanmayacaksanız** pili yaklaşık %50–60 doluluğa getirip serin bir
   yerde saklayın.
3. **Aşırı sıcakta şarj etmeyin**, güneş altındaki araçta bırakmayın.
4. **Şişmiş, ezilmiş veya delinmiş pili kullanmayın.** Yangın riski vardır.
5. Orijinal veya uygun nitelikte şarj cihazı kullanın. USB-C girişli pillerde
   kaliteli kablo ve adaptör tercih edin.

**Pil gerilimi kalibrasyonu (`BatCal`)**: Ekrandaki gerilim gerçek değerden farklıysa,
pilin gerilimini multimetreyle ölçüp `BatCal` menüsünde ekrandaki değeri ölçtüğünüz
değere eşitleyin.

## 1.18 Direnç renk kodları

Dirençlerin değeri üzerlerindeki renkli bantlarla belirtilir. Telsizdeki
**Resistor** uygulaması (`F` + `7` → Resistor) bunu hesaplar.

| Renk | Rakam | Çarpan | Tolerans |
|------|-------|--------|----------|
| Siyah | 0 | ×1 | — |
| Kahverengi | 1 | ×10 | ±%1 |
| Kırmızı | 2 | ×100 | ±%2 |
| Turuncu | 3 | ×1 k | ±%0,05 |
| Sarı | 4 | ×10 k | ±%0,02 |
| Yeşil | 5 | ×100 k | ±%0,5 |
| Mavi | 6 | ×1 M | ±%0,25 |
| Mor | 7 | ×10 M | ±%0,1 |
| Gri | 8 | ×100 M | ±%0,01 |
| Beyaz | 9 | ×1 G | — |
| Altın | — | ×0,1 | ±%5 |
| Gümüş | — | ×0,01 | ±%10 |

**4 bantlı örnek**: Sarı – Mor – Kırmızı – Altın → 4, 7, ×100, ±%5 → **4,7 kΩ ±%5**.

## 1.19 Multimetre kullanımı

Multimetre, gerilim, akım ve direnç ölçen temel ölçü aletidir.

| Ölçüm | Ayar | Bağlantı | Dikkat |
|-------|------|----------|--------|
| DC gerilim | `V⎓` | Ölçülen elemana **paralel** | Kırmızı uç + tarafa |
| AC gerilim | `V~` | Paralel | Şebekede çok dikkatli olun |
| Direnç | `Ω` | Devre **enerjisizken** | Elemanı devreden ayırmak daha doğru sonuç verir |
| Akım | `A` | Devreye **seri** | Yanlış bağlanırsa sigorta atar; problar `A` soketine takılır |
| Süreklilik | `🔊` | İki nokta arası | Kablo kopukluğu bulmak için |

**Telsizle ilgili pratik ölçümler**

- **Pil gerilimi**: Pilin kontaklarından DC gerilim ölçün. `BatCal` kalibrasyonu
  için kullanın.
- **Kablo kontrolü**: Programlama kablosunun ya da anten kablosunun iç iletkeni ile
  dış zırhı arasında **kısa devre olmamalıdır**. Uçtan uca her iletken ise sürekli olmalıdır.

> [!NOTE]
> Multimetre RF ölçemez. Anten ve verici ölçümleri için SWR metre, wattmetre,
> NanoVNA gibi RF aletleri gerekir (bkz. [5. bölüm](05-antenler-ve-yayilim.md)).

## 1.20 Güvenlik

- **Şebeke elektriği öldürür.** Şebekeye bağlı cihazların içini açmayın.
- **Li-ion piller** kısa devre edildiğinde çok büyük akım verir; tel, anahtar,
  bozuk para ile kutup uçlarını birleştirmeyin. Pili çantada metal eşyalarla
  birlikte taşımayın.
- **RF yanığı**: Gönderim sırasında antenin ucuna dokunmayın. 5 W'lık el
  telsizinde bu risk düşüktür ama yüksek güçlü sistemlerde ciddi yanık yapar.
- **Statik elektrik (ESD)**: Telsizi açıp elektronik kartla çalışacaksanız
  topraklama bilekliği kullanın.
- **Yıldırım**: Dış ortam antenleri ve direkleri mutlaka topraklanmalıdır. Fırtınada
  anten kablosunu cihazdan ayırın.

## 1.21 Özet tablo

| Kavram | Formül / değer | Akılda kalacak cümle |
|--------|----------------|----------------------|
| Ohm Yasası | V = I × R | Gerilim, akımı dirençten geçirmeye çalışır |
| Güç | P = V × I | Watt, işin yapılma hızıdır |
| Enerji | Wh = V × Ah | 7,4 V × 1,6 Ah ≈ 11,8 Wh |
| Frekans | f = 1 / T | Saniyedeki tekrar sayısı |
| Bobin reaktansı | XL = 2πfL | Frekans arttıkça artar |
| Kondansatör reaktansı | XC = 1 / (2πfC) | Frekans arttıkça azalır |
| Rezonans | f₀ = 1 / (2π√LC) | XL = XC olduğu frekans |
| Standart RF empedansı | 50 Ω | Telsiz, kablo ve anten 50 Ω'a göre tasarlanır |
| Kristal hatası | Hz = f × ppm / 10⁶ | 2,69 ppm, 145 MHz'de ≈ 390 Hz eder |
| Nyquist | fs ≥ 2 × fmax | Örnekleme, en yüksek frekansın iki katı olmalı |

---

[← İçindekiler](README.md) · [Sonraki: Radyo dalgaları ve spektrum →](02-radyo-dalgalari-ve-spektrum.md)
