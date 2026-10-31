# 3. Desibel, Güç ve Sinyal Ölçümü

[← Önceki: Radyo dalgaları](02-radyo-dalgalari-ve-spektrum.md) · [İçindekiler](README.md) · [Sonraki: Modülasyon →](04-modulasyon-ve-sinyal-turleri.md)

Telsizcilikte güçler ve sinyaller **çok geniş bir aralıkta** değişir. Vericiniz 5 W
gönderir; 50 km ötedeki alıcıya bunun milyarda birinin de milyarda biri kadarı ulaşır.
Bu kadar farklı sayıları rahatça kullanmak için **desibel (dB)** kullanılır. Bu bölüm
dB'yi, dBm'yi, S-metreyi, gürültüyü ve bir bağlantının menzilinin nasıl
hesaplanacağını anlatır.

## İçindekiler

1. [Desibel (dB) nedir?](#31-desibel-db-nedir)
2. [Akılda tutulacak dB kuralları](#32-akılda-tutulacak-db-kuralları)
3. [dBm, dBW, dBµV: mutlak seviyeler](#33-dbm-dbw-dbµv-mutlak-seviyeler)
4. [Telsizin güç seviyeleri dBm olarak](#34-telsizin-güç-seviyeleri-dbm-olarak)
5. [Alınan sinyal: µV ve dBm](#35-alınan-sinyal-µv-ve-dbm)
6. [S-metre ve RSSI](#36-s-metre-ve-rssi)
7. [Gürültü, gürültü tabanı ve SNR](#37-gürültü-gürültü-tabanı-ve-snr)
8. [Alıcı hassasiyeti, SINAD ve squelch](#38-alıcı-hassasiyeti-sinad-ve-squelch)
9. [Anten kazancı: dBi, dBd, ERP, EIRP](#39-anten-kazancı-dbi-dbd-erp-eirp)
10. [Serbest uzay yol kaybı](#310-serbest-uzay-yol-kaybı)
11. [Bağlantı bütçesi: menzil hesabı](#311-bağlantı-bütçesi-menzil-hesabı)
12. [Sinyal raporu vermek](#312-sinyal-raporu-vermek)
13. [Özet](#313-özet)

---

## 3.1 Desibel (dB) nedir?

**Desibel**, iki değerin **oranını** logaritmik olarak ifade eder. Kendi başına bir
birim değil, bir **karşılaştırmadır**.

```
Güç oranı:     dB = 10 × log₁₀(P2 / P1)
Gerilim oranı: dB = 20 × log₁₀(V2 / V1)     (aynı empedansta)
```

Neden logaritma? Çünkü:

- **Çarpma, toplamaya döner.** Bir yükselteç sinyali 100 kat (20 dB), bir kablo
  yarıya (−3 dB) indiriyorsa toplam etki 20 − 3 = **17 dB**'dir. Çarpım hesabı yapmanıza gerek kalmaz.
- **Çok büyük ve çok küçük sayılar** küçük sayılarla ifade edilir: 1 000 000 000 kat = 90 dB.
- **İnsan kulağı ve algısı** da kabaca logaritmik çalışır.

## 3.2 Akılda tutulacak dB kuralları

| dB | Güç oranı | Gerilim oranı | Akılda kalacak hali |
|----|-----------|---------------|---------------------|
| 0 dB | ×1 | ×1 | Değişiklik yok |
| +1 dB | ×1,26 | ×1,12 | Zar zor fark edilir |
| **+3 dB** | **×2** | ×1,41 | **Güç iki katı** |
| +6 dB | ×4 | **×2** | **Gerilim iki katı** = **1 S birimi** |
| **+10 dB** | **×10** | ×3,16 | **Güç on katı** |
| +20 dB | ×100 | ×10 | |
| +30 dB | ×1000 | ×31,6 | |
| −3 dB | ×0,5 | ×0,71 | Güç yarıya iner |
| −10 dB | ×0,1 | ×0,32 | Güç onda birine iner |

**Pratik çıkarımlar**

- Gücü **1 W'tan 5 W'a** çıkarmak yalnızca **+7 dB** kazanç sağlar: yaklaşık 1 S birimi.
  Karşı taraf bunu biraz daha güçlü duyar ama mucize beklemeyin.
- Antenin kalitesi, yüksekliği ve kablo kaybı sık sık **10 dB ve üzeri** fark yaratır.
  Bu yüzden **"iyi anten, yüksek güçten iyidir."**
- Gücü yarıya indirmek yalnızca −3 dB'dir. Çoğu zaman karşı taraf farkı neredeyse
  duymaz ama pil çok daha uzun dayanır.

## 3.3 dBm, dBW, dBµV: mutlak seviyeler

dB'nin sonuna bir harf eklenince **referans** belirtilmiş olur ve değer mutlak hale gelir:

| Birim | Referans | Kullanım |
|-------|----------|----------|
| **dBm** | 1 miliwatt (mW) | Telsizcilikte en yaygın: hem verici gücü hem alınan sinyal |
| **dBW** | 1 watt | Yüksek güçler (yayın vericileri). dBW = dBm − 30 |
| **dBµV** | 1 mikrovolt | Alıcı giriş gerilimi. 50 Ω'da dBm = dBµV − 107 |
| **dBi** | İzotropik anten | Anten kazancı |
| **dBd** | Yarım dalga dipol | Anten kazancı. dBi = dBd + 2,15 |
| **dBc** | Taşıyıcı | Harmonik ve yan bant seviyeleri ("−60 dBc harmonik") |
| **dBFS** | Tam ölçek | Dijital sistemlerde, ADC'nin en büyük değerine göre |

```
dBm = 10 × log₁₀(P / 1 mW)          P (mW) = 10^(dBm / 10)
```

## 3.4 Telsizin güç seviyeleri dBm olarak

| `Power` seviyesi | Yaklaşık güç | dBm | 5 W'a göre fark |
|------------------|--------------|-----|-----------------|
| `LOW 1` | < 20 mW | < 13 dBm | ≈ −24 dB |
| `LOW 2` | 125 mW | 21 dBm | −16 dB |
| `LOW 3` | 250 mW | 24 dBm | −13 dB |
| `LOW 4` | 500 mW | 27 dBm | −10 dB |
| `LOW 5` | 1 W | 30 dBm | −7 dB |
| `MID` | 2 W | 33 dBm | −4 dB |
| `HIGH` | 5 W | 37 dBm | 0 dB |
| `USER` | `SetPwr` ile seçilen | — | — |

**Diğer referans değerler**

| Güç | dBm | Örnek |
|-----|-----|-------|
| 1 µW | −30 dBm | |
| 1 mW | 0 dBm | |
| 10 mW | 10 dBm | LPD433 cihazları |
| 100 mW | 20 dBm | Wi-Fi yönlendirici, Bluetooth sınıf 1 |
| 500 mW | 27 dBm | PMR446 sınırı (ERP) |
| 5 W | 37 dBm | El telsizi |
| 50 W | 47 dBm | Araç telsizi |
| 100 W | 50 dBm | HF istasyonu |

## 3.5 Alınan sinyal: µV ve dBm

Alıcıya gelen sinyaller çok küçüktür; genellikle **mikrovolt (µV)** veya **dBm** ile
ifade edilir. 50 Ω'luk sistemde:

```
P = V² / R    →    dBm = 20 × log₁₀(V_µV) − 107
```

| Alıcı girişi | dBm | Anlamı |
|--------------|-----|--------|
| 0,1 µV | −127 dBm | Çok iyi bir alıcının zar zor duyabileceği seviye |
| 0,2 µV | −121 dBm | Tipik el telsizi FM hassasiyeti (12 dB SINAD) |
| 0,25 µV | −119 dBm | |
| 0,5 µV | −113 dBm | Zayıf ama anlaşılır FM sinyali |
| 1 µV | −107 dBm | Rahat dinlenen FM sinyali |
| 5 µV | **−93 dBm** | **S9** (VHF/UHF, IARU) |
| 50 µV | −73 dBm | S9 + 20 dB: güçlü yerel istasyon |
| 1 mV | −47 dBm | Çok güçlü: yakındaki verici |
| 10 mV | −27 dBm | Yan yana iki telsiz. Alıcıyı doyurabilir |

Bir alıcı için **−100 dBm**, 0,1 picowatt (10⁻¹³ W) demektir. 5 W'lık bir verici
(+37 dBm) ile arada **137 dB** fark vardır: yaklaşık 50 trilyon kat.

## 3.6 S-metre ve RSSI

- **RSSI (Received Signal Strength Indicator)**: Alıcının ölçtüğü sinyal seviyesi.
  BK4829 entegresi bunu ölçer; firmware **dBm**'ye çevirir.
- **S-metre**: Sinyal gücünü **S1–S9** ve **S9+dB** olarak gösteren geleneksel ölçek.

**IARU Bölge 1 VHF/UHF önerisi**: S9 = **−93 dBm** (5 µV, 50 Ω) ve **her S birimi 6 dB**.
Firmware tam olarak bu ölçeği kullanır (`App/ui/main.c`):

| S | dBm | µV (50 Ω) | Anlamı (FM için kabaca) |
|---|-----|-----------|--------------------------|
| S0 | < −141 | < 0,02 | Gürültü |
| S1 | −141 | 0,02 | Ölçülebilir ama duyulmaz |
| S2 | −135 | 0,04 | |
| S3 | −129 | 0,08 | |
| S4 | −123 | 0,16 | Gürültülü, zor anlaşılır |
| S5 | −117 | 0,32 | Hışırtılı ama anlaşılır |
| S6 | −111 | 0,63 | |
| S7 | −105 | 1,26 | İyi |
| S8 | −99 | 2,5 | Çok iyi |
| **S9** | **−93** | **5** | Mükemmel, gürültüsüz |
| S9+10 | −83 | 16 | |
| S9+20 | −73 | 50 | |
| S9+30 | −63 | 158 | |
| S9+40 | −53 | 500 | Telsizin göstergesinin üst sınırı |

**Ekranda S-metre**

- `SetMet` menüsü iki stil sunar: **`CLASSIC`** (çubuklar) ve **`TINY`** (ince çizgi).
- Çubukların yanında dBm değeri ve `S7`, `+20` gibi etiketler gösterilir.
- RSSI değeri, telsizin bandına göre bir **düzeltme tablosuyla** (`dBmCorrTable`)
  dBm'ye çevrilir. Değerler laboratuvar cihazı kadar kesin değildir ama
  karşılaştırma için çok kullanışlıdır.

> [!TIP]
> Antenleri, konumları veya ayarları karşılaştırırken S-metreyi değil **dBm değerini**
> not edin. "−98 dBm'den −86 dBm'e çıktı" demek "12 dB iyileşme oldu" demektir.

## 3.7 Gürültü, gürültü tabanı ve SNR

### Termal gürültü

Mutlak sıfırın üstündeki her sıcaklıkta, dirençlerde elektronların rastgele hareketi
gürültü üretir. Oda sıcaklığında bunun gücü:

```
N (dBm) = −174 dBm/Hz + 10 × log₁₀(Bant genişliği, Hz)
```

| Alıcı bant genişliği | Termal gürültü |
|----------------------|----------------|
| 500 Hz (CW) | −147 dBm |
| 2,7 kHz (SSB) | ≈ −140 dBm |
| 12,5 kHz (dar FM) | −133 dBm |
| 25 kHz (geniş FM) | −130 dBm |

**Neden önemli?** Dar bant daha az gürültü toplar. CW'nin ve dar dijital modların
zayıf sinyallerde bu kadar iyi çalışmasının sebebi budur.

### Gürültü figürü (NF)

Gerçek bir alıcı, termal gürültünün üstüne **kendi gürültüsünü** ekler. Buna
**gürültü figürü** denir; birkaç dB ile ifade edilir. Gerçek gürültü tabanı:

```
Gürültü tabanı ≈ −174 + 10·log₁₀(BW) + NF
```

12,5 kHz bant genişliği ve 6 dB NF ile ≈ −127 dBm. Şehirdeki insan kaynaklı
gürültü bunu çoğu zaman 10–20 dB yukarı çeker. APRS RX belgesinde, yoğun 144,800 MHz'de
ölçülen gürültü tabanının −132 dBm'den −104 dBm'e yükseldiği not edilmiştir.

### SNR

**SNR (Signal-to-Noise Ratio)** = sinyal seviyesi − gürültü seviyesi (dB).

| SNR | FM ses kalitesi |
|-----|-----------------|
| < 0 dB | Sinyal gürültünün altında. FM'de çoğunlukla hiçbir şey anlaşılmaz. |
| 6–10 dB | Hışırtılı, kesik kesik |
| 12 dB | Anlaşılır ("12 dB SINAD" hassasiyet tanımı) |
| 20 dB | İyi |
| 30 dB+ | Gürültüsüz, temiz |

## 3.8 Alıcı hassasiyeti, SINAD ve squelch

- **Hassasiyet (sensitivity)**: Alıcının anlaşılır bir sinyal verebildiği en düşük
  giriş seviyesi. FM için genellikle **12 dB SINAD** ölçütüyle verilir.
  El telsizlerinde tipik değer **0,15–0,25 µV** (−123 … −119 dBm) civarıdır.
- **SINAD**: (Sinyal + Gürültü + Bozulma) / (Gürültü + Bozulma). FM alıcı ölçümünün
  standart yöntemidir.
- **Seçicilik (selectivity)**: Alıcının komşu kanaldaki güçlü bir sinyali bastırabilme
  yeteneği. Bu telsizde ayarlı ön filtre olmadığı için bant dışı güçlü sinyallere
  karşı seçicilik sınırlıdır.

### Squelch (susturucu)

`Sql` menüsü veya `F` + `UP`/`DOWN` ile **0–9** arasında ayarlanır.

| Değer | Etkisi |
|-------|--------|
| 0 | Susturucu kapalı: hışırtı sürekli duyulur. Çok zayıf sinyalleri yakalamak veya dijital uygulamalar için |
| 1–2 | Çok hassas: zayıf sinyaller açar, arada gürültü de açabilir |
| 3–4 | **Genel kullanım için önerilen** |
| 5–7 | Yalnızca orta ve güçlü sinyaller açar. Gürültülü şehir ortamı |
| 8–9 | Yalnızca çok güçlü sinyaller |

- `MONITOR` işlevi (varsayılan olarak `SIDE1` kısa basış) susturucuyu **geçici olarak
  açar**. Zayıf bir sinyali dinlemek için idealdir. Ekranda `SQL` yerine `MONI` yazar.
- Squelch kapalıyken duyulan "**şşşş**" sesi, alıcının çalıştığının kanıtıdır.
  Sinyal geldiğinde bu ses kesilir (FM'in "yakalama etkisi").
- **CTCSS/DCS** ile squelch farklıdır: CTCSS/DCS yalnızca **doğru tonu taşıyan**
  sinyallerde hoparlörü açar (bkz. [4. bölüm](04-modulasyon-ve-sinyal-turleri.md#412-ctcss-ve-dcs)).

## 3.9 Anten kazancı: dBi, dBd, ERP, EIRP

- **İzotropik anten**: Her yöne eşit yayan, hayali bir referans anten. Kazancı 0 dBi.
- **dBi**: Antenin, en güçlü yönündeki yayınının izotropik antene oranı.
- **dBd**: Yarım dalga dipole göre kazanç. **0 dBd = 2,15 dBi**.

> Bir anten enerji "üretmez". Kazanç, enerjinin bazı yönlere **odaklanması**
> demektir: bir yöne kazanılan, başka yönlerden kaybedilir. Dikey bir el telsizi
> anteni enerjiyi ufka yayar; tam yukarı ve tam aşağı çok az yayar.

| Anten | Tipik kazanç |
|-------|--------------|
| Kısa "lastik" anten (stok) | −5 … 0 dBi (verimsiz) |
| Çeyrek dalga kırbaç | ≈ 0–2 dBi |
| Uzun el telsizi anteni (ör. 40 cm, çift bant) | ≈ 0–3 dBi |
| Yarım dalga dipol | 2,15 dBi |
| 5/8 dalga araç anteni | ≈ 3–5 dBi |
| 3 elemanlı Yagi | ≈ 7 dBi |
| 7–10 elemanlı Yagi | ≈ 10–14 dBi |

**ERP ve EIRP**

```
EIRP (dBm) = Verici gücü (dBm) − Kablo kaybı (dB) + Anten kazancı (dBi)
ERP  (dBm) = EIRP − 2,15
```

**Örnek**: 5 W (37 dBm), kablo kaybı yok, anten −3 dBi → EIRP = 34 dBm ≈ 2,5 W.
Yani "5 W'lık telsiz", kısa bir antenle aslında 2,5 W'lık izotropik bir verici gibi davranır.

**Kablo kaybı** (bkz. [5. bölüm](05-antenler-ve-yayilim.md#57-koaksiyel-kablo)): 10 m ince
RG-58 kablo, 435 MHz'de 3 dB'den fazla kaybettirir; gücünüzün yarısı kabloda ısıya dönüşür.

## 3.10 Serbest uzay yol kaybı

Sinyal antenden uzaklaştıkça küresel bir yüzeye yayılır; birim alana düşen güç
mesafenin karesiyle azalır. **Serbest uzay yol kaybı (FSPL)**, iki izotropik anten
arasındaki kayıptır:

```
FSPL (dB) = 20·log₁₀(d, km) + 20·log₁₀(f, MHz) + 32,44
```

| Mesafe | 145 MHz | 435 MHz |
|--------|---------|---------|
| 100 m | 55,7 dB | 65,2 dB |
| 1 km | 75,7 dB | 85,2 dB |
| 5 km | 89,6 dB | 99,2 dB |
| 10 km | 95,7 dB | 105,2 dB |
| 20 km | 101,7 dB | 111,2 dB |
| 50 km | 109,6 dB | 119,2 dB |
| 100 km | 115,7 dB | 125,2 dB |
| 400 km (ISS) | 127,7 dB | 137,3 dB |
| 2000 km (alçak yörünge uydusu, ufukta) | 141,7 dB | 151,2 dB |

**Kurallar**

- Mesafe **iki katına** çıkınca kayıp **6 dB** artar (1 S birimi).
- Aynı mesafede **435 MHz**, 145 MHz'e göre ≈ **9,5 dB** daha fazla kaybeder
  (izotropik antenlerle). Pratikte UHF antenleri daha kısa olduğundan bu farkın bir
  kısmı kapanır. UHF ayrıca binaların içine pencerelerden daha iyi girer.
- Gerçek dünyada engeller, bina, ağaç, insan vücudu ek kayıp getirir.
  Arazide çoğu zaman bu tablonun **10–40 dB üstünde** kayıp olur.

## 3.11 Bağlantı bütçesi: menzil hesabı

**Bağlantı bütçesi (link budget)**, vericiden alıcıya kadar bütün kazanç ve kayıpların toplamıdır:

```
Alınan güç (dBm) = Verici gücü + Verici anten kazancı − Kablo kayıpları
                   − Yol kaybı − Engel kayıpları + Alıcı anten kazancı
```

**Örnek 1: İki el telsizi, açık arazi, 145 MHz, 10 km**

| Kalem | Değer |
|-------|-------|
| Verici gücü (5 W) | +37 dBm |
| Verici anten (kısa anten) | −3 dB |
| Yol kaybı (10 km, serbest uzay) | −95,7 dB |
| Arazi ve engel kaybı (tahmini) | −20 dB |
| Alıcı anten | −3 dB |
| **Alınan sinyal** | **≈ −85 dBm** (S9 + 8 dB) |

Teoride çok iyi. Ama telsizler yerde, aralarında tepe veya bina varsa ek kayıp 40 dB'i
bulur, sinyal −105 dBm'e (S7) iner. Gerçek menzili çoğu zaman **güç değil, görüş hattı**
belirler (bkz. [5. bölüm, radyo ufku](05-antenler-ve-yayilim.md#510-radyo-ufku-ve-görüş-hattı)).

**Örnek 2: ISS'i dinlemek, 145,8 MHz, 400–2000 km**

| Kalem | Tepe noktasında (≈ 400 km) | Ufukta (≈ 2000 km) |
|-------|-----------------------------|---------------------|
| ISS verici (≈ 5–25 W, alçak kazançlı anten) | ≈ +40 dBm EIRP | ≈ +40 dBm |
| Yol kaybı | −128 dB | −142 dB |
| Alıcı anten (el telsizi) | −3 dB | −3 dB |
| **Alınan sinyal** | **≈ −91 dBm** | **≈ −105 dBm** |

Bu yüzden ISS, el telsiziyle ve basit bir antenle bile duyulabilir. Ufka yakınken
sinyal zayıflar; engeller (bina, ağaç) ise tamamen keser.

## 3.12 Sinyal raporu vermek

Görüşmelerde karşı tarafa sinyalinin nasıl geldiğini söylemek gelenektir.

**FM / ses için**: "Sinyalin **S7**, ses **temiz**" veya "S9+20, çok güçlü".

**RS(T) sistemi**:

| Harf | Ölçüt | Ölçek |
|------|-------|-------|
| **R** (Readability) | Anlaşılırlık | 1 (anlaşılmıyor) – 5 (mükemmel) |
| **S** (Strength) | Güç | 1 (çok zayıf) – 9 (çok güçlü) |
| **T** (Tone) | Ton kalitesi, **yalnızca CW** | 1 (çok kötü) – 9 (kusursuz) |

Örnekler: "**59**" = mükemmel anlaşılır, çok güçlü (ses). "**599**" = CW için aynı, kusursuz ton.

> [!TIP]
> Gerçekçi rapor verin. "Herkese 59" demek bilgi taşımaz. Bu telsizde dBm değerini
> de söyleyebilirsiniz: "−96 dBm geliyorsun, S8".

## 3.13 Özet

| Kural | Değer |
|-------|-------|
| +3 dB | Güç ×2 |
| +6 dB | Gerilim ×2 = 1 S birimi = mesafe ÷2 (serbest uzayda) |
| +10 dB | Güç ×10 |
| 0 dBm | 1 mW |
| 5 W | +37 dBm |
| S9 (VHF/UHF) | −93 dBm = 5 µV |
| 1 µV (50 Ω) | −107 dBm |
| Termal gürültü | −174 dBm/Hz |
| 1 W → 5 W | Yalnızca +7 dB (≈ 1 S birimi) |
| 0 dBd | 2,15 dBi |
| FSPL | 20·log(d km) + 20·log(f MHz) + 32,44 |

---

[← Önceki: Radyo dalgaları](02-radyo-dalgalari-ve-spektrum.md) · [İçindekiler](README.md) · [Sonraki: Modülasyon →](04-modulasyon-ve-sinyal-turleri.md)
