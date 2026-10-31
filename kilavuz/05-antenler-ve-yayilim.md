# 5. Antenler, Kablolar ve Yayılım

[← Önceki: Modülasyon](04-modulasyon-ve-sinyal-turleri.md) · [İçindekiler](README.md) · [Sonraki: Amatör telsizcilik →](06-amator-telsizcilik.md)

Bir telsizin performansını en çok değiştiren şey **antendir**. Bu bölüm antenin nasıl
çalıştığını, hangi anteni ne zaman kullanacağınızı, kablo ve konnektörleri, SWR'yi ve
radyo dalgalarının arazide nasıl yayıldığını anlatır.

## İçindekiler

1. [Anten nasıl çalışır?](#51-anten-nasıl-çalışır)
2. [Anten boyu ve dalga boyu](#52-anten-boyu-ve-dalga-boyu)
3. [Işıma diyagramı, kazanç, yönlülük](#53-işıma-diyagramı-kazanç-yönlülük)
4. [Polarizasyon](#54-polarizasyon)
5. [Anten türleri](#55-anten-türleri)
6. [SWR (duran dalga oranı)](#56-swr-duran-dalga-oranı)
7. [Koaksiyel kablo](#57-koaksiyel-kablo)
8. [Konnektörler](#58-konnektörler)
9. [El telsizi antenini iyileştirmenin yolları](#59-el-telsizi-antenini-iyileştirmenin-yolları)
10. [Radyo ufku ve görüş hattı](#510-radyo-ufku-ve-görüş-hattı)
11. [Fresnel bölgesi](#511-fresnel-bölgesi)
12. [Yayılım türleri](#512-yayılım-türleri)
13. [Engeller ve kayıplar](#513-engeller-ve-kayıplar)
14. [RF maruziyeti ve güvenlik](#514-rf-maruziyeti-ve-güvenlik)
15. [Özet](#515-özet)

---

## 5.1 Anten nasıl çalışır?

Anten, kablodaki **elektrik enerjisini** boşlukta yayılan **elektromanyetik dalgaya**
(gönderirken) ve dalgayı yeniden elektrik sinyaline (alırken) çeviren bir **dönüştürücüdür**.

- Aynı anten hem gönderir hem alır (**karşılıklılık / reciprocity** ilkesi). İyi gönderen
  bir anten aynı frekansta iyi de alır.
- Anten, belirli bir frekansta **rezonansa** girer. O frekansta empedansı saf dirence
  (ideal olarak 50 Ω) yaklaşır ve enerjiyi en verimli şekilde yayar.
- Rezonans frekansının dışında anten kötüleşir: SWR yükselir, enerjinin bir kısmı
  vericiye geri döner.

## 5.2 Anten boyu ve dalga boyu

Anten boyu, dalga boyunun belirli kesirleridir:

```
Dalga boyu λ (m) = 300 / f (MHz)
Pratik boy = teorik boy × kısalma faktörü (≈ 0,95; telin kalınlığına bağlı)
```

| Anten | Formül (pratik) | 145 MHz | 435 MHz |
|-------|-----------------|---------|---------|
| Tam dalga (λ) | 300 / f | 2,07 m | 69 cm |
| **Yarım dalga dipol (λ/2)**, toplam | 142,5 / f | **≈ 98 cm** (her kol ≈ 49 cm) | **≈ 33 cm** (her kol ≈ 16,4 cm) |
| **Çeyrek dalga (λ/4)** | 71,25 / f | **≈ 49 cm** | **≈ 16,4 cm** |
| 5/8 dalga | 187,5 / f | ≈ 1,29 m | ≈ 43 cm |

**Diğer frekanslar için çeyrek dalga (teorik)**: 121,5 MHz → 62 cm, 156,8 MHz → 48 cm,
162 MHz → 46 cm, 406 MHz → 18,5 cm, 446 MHz → 16,8 cm.

**Çift bantlı antenler**: Tek bir anten hem 2 m'de hem 70 cm'de rezonans yapacak
şekilde tasarlanabilir. Stok antenin ve çoğu yedek el telsizi anteninin içinde bunun
için yay biçiminde bir bobin ve ek elemanlar bulunur.

**Kısaltılmış (yüklü) antenler**: Çeyrek dalgadan kısa antenler, içlerindeki bir
**yükleme bobini** ile elektriksel olarak uzatılır. Kısa antenler kullanışlıdır ama
**daha verimsizdir** ve bant genişlikleri dardır.

## 5.3 Işıma diyagramı, kazanç, yönlülük

**Işıma diyagramı**, antenin hangi yöne ne kadar enerji yaydığını gösterir.

```
 Dikey çeyrek dalga / dipol           Yagi (yönlü)
 (yandan bakış, "simit" biçimi)       (yukarıdan bakış)

        ╭──╮   │   ╭──╮                      ╭────────╮
      ╭╯    ╰──┼──╯    ╰╮          ╭─╮      ╱          ╲
     (    ←    ║    →    )        (arka)──[■■■■]──→  ön lob
      ╰╮    ╭──┼──╮    ╭╯          ╰─╯      ╲          ╱
        ╰──╯   │   ╰──╯                      ╰────────╯
   Ufka doğru güçlü, yukarı/aşağı zayıf     Bir yöne odaklı
```

- **Her yöne eşit (omnidireksiyonel)**: Dikey antenler yatay düzlemde her yöne eşit yayar.
  Mobil ve el telsizi kullanımı için idealdir.
- **Yönlü (direksiyonel)**: Yagi gibi antenler enerjiyi bir yöne toplar. Uzak röleye
  ulaşmak, **tilki avı / yön bulma** ve uydu takibi için kullanılır.
- **Kazanç (dBi/dBd)**: Bir yöndeki güçlenme (bkz. [3.9](03-desibel-ve-sinyal-olcumu.md#39-anten-kazancı-dbi-dbd-erp-eirp)).
- **Ön/arka oranı (F/B)**: Yönlü antenin önüne ve arkasına giden enerjinin oranı.
  Yön bulmada çok önemlidir: arkadan gelen sinyali önden gelenle karıştırmamanızı sağlar.

## 5.4 Polarizasyon

Dalganın **elektrik alanının yönüdür**. Anten fiziksel olarak hangi yönde duruyorsa
polarizasyon odur.

| Polarizasyon | Kullanım |
|--------------|----------|
| **Dikey** | FM, röleler, el ve araç telsizleri, APRS |
| **Yatay** | VHF/UHF SSB ve CW uzak mesafe (DX) çalışmaları, TV antenleri |
| **Dairesel** | Uydu haberleşmesi (uydu dönerken sinyal kaybolmasın diye) |

- Verici ve alıcı antenlerinin polarizasyonu **aynı olmalıdır**. Biri dikey, diğeri
  yatayken kayıp **20 dB'yi** aşabilir (≈ 3 S birimi).
- El telsizini **dik tutun**. Konuşurken telsizi yatırmak sinyali zayıflatır.
- Yansımalar polarizasyonu karıştırdığından şehirde bu kayıp genellikle daha azdır.

## 5.5 Anten türleri

| Anten | Yapısı | Kazanç | Artısı / eksisi |
|-------|--------|--------|------------------|
| **Stok "lastik" anten** | Kısa, içinde yükleme bobini | −5 … 0 dBi | Kullanışlı ama verimsiz |
| **Uzun el telsizi anteni** (ör. 40 cm çift bant kırbaç) | Daha uzun ışıyan eleman | ≈ 0–3 dBi | Belirgin iyileşme, biraz hantal |
| **Çeyrek dalga kırbaç** | λ/4 tel + toprak düzlemi | ≈ 0–2 dBi | Basit, araç tavanında iyi çalışır |
| **Toprak düzlemli (ground plane)** | λ/4 dikey + 3–4 eğik radyal | ≈ 1–2 dBi | Evde kendin yap için ideal |
| **J-pole / Slim Jim** | λ/2 ışıyan + λ/4 uyumlandırma | ≈ 2–3 dBi | Radyal istemez, ucuz, iyi |
| **Dipol** | İki λ/4 kol | 2,15 dBi | Referans anten; dikey veya yatay kurulabilir |
| **5/8 dalga** | Uzun, tabanda uyumlandırma bobini | ≈ 3–5 dBi | Araç ve sabit istasyon için |
| **Collinear (doğrusal dizi)** | Üst üste dizilmiş λ/2 bölümler | 5–9 dBi | Sabit istasyon, yüksek direk |
| **Yagi-Uda** | Bir sürülen eleman + reflektör + direktörler | 7–15 dBi | Yön bulma, uzak röle, uydu |
| **Şerit metre Yagi** | Elemanları çelik şerit metreden | ≈ 7 dBi | Tilki avı için klasik ucuz anten |
| **Mıknatıslı araç anteni** | Tabanında mıknatıs, araç tavanına | Tipine göre | Aracın metal kafesinin dışına çıkarır |

> [!TIP]
> Aracın içinden el telsiziyle konuşmak, metal kafes yüzünden sinyali **10–20 dB**
> zayıflatabilir. Mıknatıslı bir tavan anteni ve kısa bir kablo büyük fark yaratır.

## 5.6 SWR (duran dalga oranı)

Kablo ve anten empedansı tam uyumlu değilse, vericiden giden gücün bir kısmı antenden
**geri yansır**. İleri ve geri giden dalgalar kabloda üst üste binip "**duran dalga**"
oluşturur. Bunun ölçüsü **SWR**'dir (Standing Wave Ratio).

```
Yansıma katsayısı:  Γ = (Z_yük − Z₀) / (Z_yük + Z₀)
SWR = (1 + |Γ|) / (1 − |Γ|)
Yansıyan güç (%) = |Γ|² × 100
```

| SWR | Yansıyan güç | Dönüş kaybı (return loss) | Uyumsuzluk kaybı | Değerlendirme |
|-----|--------------|---------------------------|-------------------|---------------|
| 1,0 | %0 | ∞ | 0 dB | Kusursuz |
| 1,2 | %0,8 | 20,8 dB | 0,04 dB | Mükemmel |
| 1,5 | %4 | 14,0 dB | 0,18 dB | Çok iyi |
| 2,0 | %11 | 9,5 dB | 0,51 dB | Kabul edilebilir |
| 2,5 | %18 | 7,4 dB | 0,88 dB | Sınırda |
| 3,0 | %25 | 6,0 dB | 1,25 dB | Kötü, verici zorlanır |
| 5,0 | %44 | 3,5 dB | 2,55 dB | Çok kötü |
| 10 | %67 | 1,7 dB | 4,81 dB | Anten yok gibi |

**Bilinmesi gerekenler**

- SWR 2'nin altındaysa iletişim açısından fark çok küçüktür. **1,0'ı kovalamayın.**
- **Yüksek SWR'nin asıl tehlikesi vericiye zarar vermesidir**: geri dönen güç PA
  transistörlerini ısıtır. **Antensiz gönderme** (SWR ≈ ∞) PA'yı bozabilir.
- Uzun ve kayıplı bir kablo SWR'yi **olduğundan iyi gösterir**: yansıyan güç kabloda
  sönümlenir. SWR'yi mümkünse antenin dibinde ölçün.

**Ölçüm aletleri**

| Alet | Ne ölçer |
|------|----------|
| **SWR metre / wattmetre** | Verici ile anten arasına takılır; ileri/geri güç ve SWR |
| **NanoVNA** | Ucuz vektör ağ analizörü: SWR, empedans, rezonans frekansı, kablo uzunluğu, filtre eğrisi |
| **Anten analizörü** | Vericisiz, kendi düşük güçlü sinyaliyle SWR ve empedans |

## 5.7 Koaksiyel kablo

**Koaksiyel kablo**, ortada bir iç iletken, çevresinde yalıtkan, onun üstünde örgülü
zırh ve en dışta kılıftan oluşur. RF'i dışarı sızdırmadan taşır.

- Telsizcilikte standart empedans **50 Ω**'dur. TV kabloları **75 Ω**'dur; telsizde kullanmayın.
- **Kayıp frekansla artar.** UHF'de kablo seçimi VHF'den çok daha önemlidir.
- **Hız faktörü (VF)**: Sinyal kabloda ışık hızından yavaş gider (≈ 0,66–0,85).
  Belirli elektriksel uzunlukta kablo gereken uyumlandırmalarda önemlidir.

**10 metre kablodaki yaklaşık kayıp** (üretici verilerine göre değişir):

| Kablo | Çap | 145 MHz | 435 MHz | Not |
|-------|-----|---------|---------|-----|
| RG-174 | 2,8 mm | ≈ 3,5 dB | ≈ 6 dB | Çok ince, yalnızca kısa bağlantılar |
| RG-316 | 2,5 mm | ≈ 3 dB | ≈ 5,5 dB | İnce, ısıya dayanıklı |
| RG-58 | 5 mm | ≈ 1,7 dB | ≈ 3 dB | Kısa mesafeler için idare eder |
| RG-213 | 10 mm | ≈ 0,8 dB | ≈ 1,5 dB | Ağır ama sağlam |
| Aircell 7 | 7 mm | ≈ 0,8 dB | ≈ 1,4 dB | Esnek, düşük kayıplı |
| LMR-400 / Ecoflex 10 | 10 mm | ≈ 0,5 dB | ≈ 0,9 dB | Sabit istasyon için çok iyi |

**Örnek**: 435 MHz'de 10 m RG-58 → 3 dB kayıp → 5 W'ın yalnızca 2,5 W'ı antene ulaşır.
Alırken de aynı 3 dB kaybedilir.

## 5.8 Konnektörler

| Konnektör | Nerede | Not |
|-----------|--------|-----|
| **SMA** | El telsizleri, küçük cihazlar | Erkek (iç pimli) ve dişi (iç delikli) türleri var |
| **RP-SMA** (ters polariteli) | Wi-Fi cihazları | SMA'ya benzer ama pimler ters. **Karıştırmayın.** |
| **BNC** | Eski el telsizleri, ölçü aletleri | Çeyrek tur kilitlenen, hızlı |
| **PL-259 / SO-239** ("UHF" konnektör) | HF ve VHF araç/sabit istasyon | UHF'de kayıplıdır (adına rağmen) |
| **N** | UHF ve üstü, sabit istasyon | Su geçirmez, düşük kayıplı |

> [!IMPORTANT]
> El telsizlerinde SMA'nın **erkek ve dişi** türü markaya göre değişir. Baofeng telsizlerin
> çoğu ile Quansheng telsizler **farklı tip** kullanır. Yeni bir anten veya adaptör
> almadan önce telsizinizin konnektörüne bakın: gövdede **dişli dış yüzey + ortada pim**
> varsa telsiz erkek, **dişli iç yüzey + ortada delik** varsa telsiz dişidir. Anten
> bunun tersi olmalıdır.

**Konnektör bakımı**

- Elle sıkın, pense kullanmayın. Telsizin SMA yuvası gövdeye ince bir somunla bağlıdır
  ve fazla sıkmak onu gevşetebilir.
- Anteni sık söküp takmak SMA'yı aşındırır. Sık değiştiriyorsanız bir **SMA koruyucu
  adaptör** kullanın.
- Dış ortamda konnektörleri yalıtım bandı veya kendinden kaynaşan bantla su geçirmez yapın.

## 5.9 El telsizi antenini iyileştirmenin yolları

Etki sırasına göre (en etkiliden en aza):

1. **Yüksekliğe çıkın.** Bir kat, bir tepe, bir pencere kenarı. Çoğu zaman her şeyden
   daha etkilidir (bkz. [5.10](#510-radyo-ufku-ve-görüş-hattı)).
2. **Açık alana çıkın.** Metal yapılar, betonarme binalar ve araçlar sinyali keser.
3. **Daha uzun ve kaliteli bir anten** kullanın. Stok antene göre birkaç dB kazandırır.
4. **"Kaplan kuyruğu" (tiger tail / karşı ağırlık)** ekleyin. Telsizin anten
   konnektörünün toprak kısmına bağlanan, aşağı sarkan ~49 cm'lik (2 m için λ/4) bir
   tel. Çeyrek dalga antenin eksik olan "toprak" yarısını tamamlar ve belirgin
   iyileşme sağlayabilir.
5. **Telsizi dik ve vücuttan uzak tutun.** Kemerdeki telsiz, vücudun gölgesinde
   10–20 dB kaybedebilir.
6. **Harici anten** bağlayın. Araçta mıknatıslı anten, evde balkondaki bir J-pole.

## 5.10 Radyo ufku ve görüş hattı

VHF ve UHF sinyalleri büyük ölçüde **düz çizgide** yayılır. Dünya yuvarlak olduğu için
belirli bir mesafeden sonra iki anten birbirini "göremez". Atmosferdeki hafif kırılma
sayesinde radyo ufku, görsel ufuktan biraz daha uzaktır:

```
d (km) ≈ 4,12 × (√h₁ + √h₂)        h₁, h₂: anten yükseklikleri (metre)
```

| Verici yüksekliği | Alıcı yüksekliği | Radyo ufku |
|-------------------|------------------|------------|
| 1,5 m (elde) | 1,5 m (elde) | **≈ 10 km** |
| 1,5 m | 10 m (bina çatısı) | ≈ 18 km |
| 1,5 m | 30 m | ≈ 28 km |
| 1,5 m | 100 m (tepe) | ≈ 46 km |
| 1,5 m | 500 m (dağdaki röle) | ≈ 97 km |
| 1,5 m | 1000 m | ≈ 135 km |
| 2 m | 2000 m (yüksek dağ) | ≈ 190 km |
| 1,5 m | 408 km (ISS) | ≈ 2600 km |

**Çıkarımlar**

- Düz arazide iki el telsizinin gerçek menzili, güçten bağımsız olarak **birkaç km ile
  10 km** arasıdır.
- Rölelerin yüksek tepelere kurulmasının sebebi budur: 500 m'deki bir röle, el
  telsiziyle ~100 km'lik bir alanı kapsayabilir.
- ISS'i 2600 km'ye kadar duyabilirsiniz, çünkü o çok yüksektedir.
- Yüksek bir tepedeyken düşük güç (`LOW`) bile çok uzağa gider. Yüksek gücü yalnızca
  gerektiğinde kullanın; rölelerde başkalarına parazit yapabilirsiniz.

## 5.11 Fresnel bölgesi

Görüş hattının açık olması yetmez. Radyo dalgası, iki anten arasındaki düz çizginin
çevresinde **elips biçiminde bir hacmi** kullanır. Buna **birinci Fresnel bölgesi**
denir. Bu bölgenin en az **%60'ı engelsiz** olmalıdır.

```
r (m) = 17,32 × √( d (km) / (4 × f (GHz)) )     (bağlantının tam ortasında)
```

| Bağlantı | Ortadaki Fresnel yarıçapı |
|----------|---------------------------|
| 10 km, 145 MHz | ≈ 72 m |
| 10 km, 435 MHz | ≈ 42 m |

Yani 10 km'lik bir 2 m bağlantıda, aradaki tepenin üstünden **onlarca metre** boşluk
gerekir. Bir tepenin "tam sınırından" görüş varsa sinyal yine de birkaç dB zayıflar.

## 5.12 Yayılım türleri

| Tür | Açıklama | Hangi bantta | Menzil |
|-----|----------|--------------|--------|
| **Doğrudan dalga (görüş hattı)** | Düz yol | VHF/UHF'nin ana modu | Radyo ufkuna kadar |
| **Yansıma** | Bina, dağ, su yüzeyinden sekme | VHF/UHF, özellikle şehirde | Görüş olmayan yerlere ulaşır |
| **Kırınım (difraksiyon)** | Keskin bir tepenin üstünden "bükülme" | VHF'de UHF'ye göre daha iyi | Tepenin arkasına zayıf sinyal |
| **Çok yollu yayılım (multipath)** | Aynı sinyalin farklı yollardan gelip girişim yapması | VHF/UHF | Hareket ederken hızlı dalgalanma ("çit kazığı etkisi", picket fencing) |
| **Troposferik bükülme / kanal (ducting)** | Sıcaklık terslenmesi olan hava katmanları dalgayı yönlendirir. Yazın, yüksek basınçta, deniz üstünde | VHF/UHF | Yüzlerce, bazen 1000+ km |
| **Sporadik E (Es)** | İyonosferin E katmanında ani yoğun bulutlar. Çoğunlukla Mayıs–Ağustos | Esas olarak 28–50 MHz, nadiren 144 MHz | 500–2500 km |
| **F2 iyonosferik yansıma** | İyonosferin yansıtması | HF; güneş aktivitesi yüksekken 28–50 MHz | Kıtalararası |
| **Meteor saçılması** | Meteorların bıraktığı iyonize izler | 50–144 MHz | 2000 km'ye kadar, saniyelik patlamalar |
| **Ay yansıması (EME)** | Ay yüzeyinden yansıtma | 144 MHz ve üstü | Dünya'nın her yeri. Çok yüksek güç ve büyük anten ister |
| **Uydu** | Amatör uydu veya ISS aktarır | 145 / 435 MHz | Uydunun görünürlük alanı |

**Türkiye için not**: Yaz aylarında Ege ve Akdeniz üzerinde oluşan **troposferik kanallar**
nedeniyle VHF/UHF'de çok uzaktaki röleler ve istasyonlar (Yunanistan, Kıbrıs, İtalya,
Mısır vb.) zaman zaman duyulabilir. Bu bir arıza değildir; doğa olayıdır.

## 5.13 Engeller ve kayıplar

| Engel | Yaklaşık ek kayıp (VHF/UHF) |
|-------|-----------------------------|
| Ahşap / alçıpan duvar | 2–5 dB |
| Tuğla duvar | 5–10 dB |
| Betonarme duvar | 10–20 dB |
| Bina içi (ortalama) | 10–20 dB |
| Metal çatılı / metal kaplamalı bina | 20 dB ve üzeri |
| Araç içi | 6–15 dB |
| Islak, yoğun ağaçlık | Kilometre başına birkaç dB (UHF'de daha fazla) |
| İnsan vücudu (telsiz kemerde) | 10–20 dB |
| Kaplamalı (enerji tasarruflu) cam | 10–30 dB |

## 5.14 RF maruziyeti ve güvenlik

- Radyo dalgaları **iyonlaştırıcı değildir**. El telsizinin ana etkisi çok yakın mesafede
  hafif ısınmadır.
- Uluslararası sınırlar (**ICNIRP**) bu ısınmaya göre belirlenmiştir. Normal kullanımda
  5 W'lık bir el telsizi bu sınırların içindedir. Bunun bir sebebi de gönderimin
  zamanın küçük bir kısmında yapılmasıdır.
- Yine de iyi alışkanlıklar edinin:
  - Gönderirken anteni **yüzünüzden ve gözlerinizden birkaç cm uzak** tutun.
  - Gönderirken antene **dokunmayın**.
  - Uzun süre yüksek güçte gönderim yapmayın. Telsiz ısınır; `TxTOut` zaman aşımını açık tutun.
  - Yönlü bir antenin (Yagi) önünde, yakın mesafede başkasına doğru gönderim yapmayın.
- **Kalp pili** veya tıbbi elektronik cihaz taşıyan kişilerin yakınında, hastanelerde,
  akaryakıt istasyonlarında ve **patlayıcı ortamlarda** gönderim yapmayın.
- **Uçakta** telsizle gönderim yapmayın.

## 5.15 Özet

| Kural | Değer / öneri |
|-------|---------------|
| Çeyrek dalga | 71,25 / f(MHz) m → 145 MHz ≈ 49 cm |
| Yarım dalga dipol | 142,5 / f(MHz) m → 145 MHz ≈ 98 cm |
| Polarizasyon | FM'de dikey. Telsizi dik tutun |
| SWR | 2'nin altı yeterli; antensiz asla göndermeyin |
| Kablo | UHF'de ince kablodan kaçının; kısa tutun |
| Radyo ufku | 4,12 × (√h₁ + √h₂) km → iki el telsizi ≈ 10 km |
| En etkili iyileştirme | Yükseklik ve açık alan, sonra daha iyi anten, en son güç |
| Kaplan kuyruğu | Antenin toprağına ~49 cm tel (2 m için) |

---

[← Önceki: Modülasyon](04-modulasyon-ve-sinyal-turleri.md) · [İçindekiler](README.md) · [Sonraki: Amatör telsizcilik →](06-amator-telsizcilik.md)
