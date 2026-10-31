# UV-K1 / UV-K5 V3 ve F4HWN Firmware: Türkçe Rehber

Radyo ve elektrik temellerinden amatör telsizciliğe, frekans haritasından telsizin her
menüsüne ve uygulamasına kadar kapsamlı bir Türkçe rehber.

Bu rehber iki tür okur için yazıldı:

- **Amatör telsizciliğe yeni başlayanlar**: Frekans, spektrum, desibel, anten, modülasyon
  gibi kavramları sıfırdan öğrenmek isteyenler.
- **Telsizi yeni alanlar**: UV-K1 veya UV-K5 V3 telsizine F4HWN firmware'ini kurup
  bütün özelliklerini kullanmak isteyenler.

> [!WARNING]
> **Dinlemek serbesttir, göndermek değil.** Amatör bantlarda yayın yapmak için Türkiye'de
> **BTK**'nın verdiği amatör telsizci belgesi gerekir. Belgeniz yoksa telsizi yalnızca alıcı
> olarak kullanın: gizli menüde `F Lock` → `DISABLE ALL` (bkz. [9.3](09-cihaz-kullanimi.md#93-kurulum-adım-adım)).

> [!CAUTION]
> Firmware'i yükledikten hemen sonra **kalibrasyon verilerinizi** [UV Studio](https://armel.github.io/uvstudio/#dump-calib)
> ile yedekleyin. Firmware'i kullanmanın riski tamamen size aittir.

## Bölümler

### Kısım I: Temeller

| # | Bölüm | İçerik |
|---|-------|--------|
| 1 | [Elektrik ve elektronik temelleri](01-elektrik-ve-elektronik.md) | Gerilim, akım, direnç, Ohm Yasası, güç, AC/DC, kondansatör, bobin, empedans, rezonans, filtreler, kristal ve ppm, ADC, Li-ion pil, renk kodları, multimetre |
| 2 | [Radyo dalgaları, frekans ve spektrum](02-radyo-dalgalari-ve-spektrum.md) | Elektromanyetik dalga, dalga boyu, ITU bantları, kanal ve adım, bant genişliği, gürültü, parazit türleri, Doppler, spektrum analizörünü okuma, alıcı ve verici mimarisi |
| 3 | [Desibel, güç ve sinyal ölçümü](03-desibel-ve-sinyal-olcumu.md) | dB kuralları, dBm, µV, S-metre tablosu, gürültü ve SNR, squelch, anten kazancı, yol kaybı, menzil hesabı, sinyal raporu |
| 4 | [Modülasyon ve sinyal türleri](04-modulasyon-ve-sinyal-turleri.md) | AM, FM, SSB, CW ve Mors alfabesi, dijital modlar, APRS, DTMF, 1750 Hz, CTCSS/DCS ve ton listesi, emisyon sınıfları, sinyalleri kulaktan tanıma |
| 5 | [Antenler, kablolar ve yayılım](05-antenler-ve-yayilim.md) | Anten boyları, ışıma, polarizasyon, anten türleri, SWR, koaksiyel kablo kayıpları, konnektörler, radyo ufku, Fresnel bölgesi, yayılım türleri, RF güvenliği |

### Kısım II: Amatör telsizcilik ve spektrum

| # | Bölüm | İçerik |
|---|-------|--------|
| 6 | [Amatör telsizcilik](06-amator-telsizcilik.md) | Belge, çağrı işareti, IARU Bölge 1 bant planları, V/RV/U kanalları, röleler, fonetik alfabe, Q kodları, görüşme usulü, log ve UTC, kurallar, acil durum, etkinlikler, uydu, APRS ağı |
| 7 | [Frekans rehberi](07-frekans-rehberi.md) | 18 MHz – 1,3 GHz arası spektrum haritası, telsizin RX/TX aralıkları ve `F Lock`, havacılık, denizcilik, PMR446, LPD433, sondalar, işaretçiler, ilk denemeler için frekanslar |

### Kısım III: Telsiz

| # | Bölüm | İçerik |
|---|-------|--------|
| 8 | [Cihaz donanımı, tuşlar ve ekran](08-cihaz-donanimi-ve-ekran.md) | Firmware sürümleri (Fusion, FieldOps, Transfer, Labs), blok şema, entegreler, bellek, pil, bağlantılar, tuşlar, LED'ler, durum çubuğu ve ekrandaki her simge, uyarı mesajları |
| 9 | [Cihaz kullanımı](09-cihaz-kullanimi.md) | Kurulum, frekans girme, VFO'lar, kanallar ve ad verme, röle programlama, gönderim, dinleme ayarları, Dual/Full Watch, tarama, ton yakalama, spektrum, FM radyo, yan tuşlar, RF Log, Multiboot, Multiconfig, Rescue Ops, Fox Hunt, Beacon, BEAM, AirCopy, UV Studio, CHIRP |
| 10 | [Menü referansı](10-menu-referansi.md) | Kategorilere göre bütün menü öğeleri, değer aralıkları ve atanabilir işlevler |
| 11 | [Uygulamalar (Labs)](11-uygulamalar.md) | APRS, AIS, ACARS, DSC, radyosondalar, EPIRB, POCSAG, SSTV, CW, Sig Finder, Spectrum3D, AF Scope/Spectro, araçlar ve oyunlar |

### Kısım IV: Uygulama ve başvuru

| # | Bölüm | İçerik |
|---|-------|--------|
| 12 | [Uygulamalı senaryolar](12-uygulamali-senaryolar.md) | Dinleme turu, röle bulma, havacılık, ISS ve SSTV, APRS, radyosonda avı, deniz, tilki avı, acil durum hazırlığı, Multiconfig senaryoları, bilinmeyen sinyali tanıma, ilk görüşme |
| 13 | [Sözlük](13-sozluk.md) | 250'yi aşkın kısaltma ve terim, ilgili bölüm bağlantılarıyla |
| 14 | [Sorun giderme ve SSS](14-sorun-giderme.md) | Belirtiye göre sorun giderme tabloları ve sık sorulan sorular |

Kısa bir hızlı başvuru için depo kökündeki [KILAVUZ_TR.md](../KILAVUZ_TR.md) dosyasına bakın.

## Önerilen okuma sırası

### "Hiçbir şey bilmiyorum, telsiz yeni geldi"

1. [9.3 Kurulum adım adım](09-cihaz-kullanimi.md#93-kurulum-adım-adım): Telsizi güvenli hale getirin.
2. [12.1 Birinci gün: dinleme turu](12-uygulamali-senaryolar.md#121-birinci-gün-dinleme-turu)
3. [2. Radyo dalgaları ve spektrum](02-radyo-dalgalari-ve-spektrum.md)
4. [7. Frekans rehberi](07-frekans-rehberi.md): Nerede ne var?
5. [8. Cihaz donanımı ve ekran](08-cihaz-donanimi-ve-ekran.md): Ekrandaki simgeler.
6. [9. Cihaz kullanımı](09-cihaz-kullanimi.md)
7. Kalan temel bölümler: [1](01-elektrik-ve-elektronik.md), [3](03-desibel-ve-sinyal-olcumu.md), [4](04-modulasyon-ve-sinyal-turleri.md), [5](05-antenler-ve-yayilim.md)

### "Amatör telsizci sınavına hazırlanıyorum"

[1](01-elektrik-ve-elektronik.md) → [2](02-radyo-dalgalari-ve-spektrum.md) →
[3](03-desibel-ve-sinyal-olcumu.md) → [4](04-modulasyon-ve-sinyal-turleri.md) →
[5](05-antenler-ve-yayilim.md) → [6](06-amator-telsizcilik.md), ardından resmî sınav kaynakları.

### "Telsizi biliyorum, F4HWN'nin özelliklerini öğrenmek istiyorum"

[8](08-cihaz-donanimi-ve-ekran.md) → [9](09-cihaz-kullanimi.md) → [10](10-menu-referansi.md) →
[11](11-uygulamalar.md) → [12](12-uygulamali-senaryolar.md).

## Gösterim kuralları

| Gösterim | Anlamı |
|----------|--------|
| `MENU`, `EXIT`, `PTT`, `5` | Telsizin tuşları |
| **uzun `5`** | Tuşa yaklaşık yarım saniye basılı tutmak |
| `F` + `5` | Önce `F`'ye basıp bırakmak, sonra `5`'e basmak |
| `UP` / `DOWN` | Yön tuşları (UV-K1'de `SetNav`'a göre sol/sağ) |
| `SIDE1` / `SIDE2` | Üst / alt yan tuş |
| `Sql`, `ChSave` | Menü öğeleri (telsizdeki yazımıyla) |
| `145,500 MHz` | Metinde Türkçe ondalık virgül; telsiz ekranında `145.500` |

## Kaynaklar ve doğruluk

- Cihaza özgü bilgiler (menüler, tuşlar, değer aralıkları, simgeler, uygulamalar) bu deponun
  **kaynak kodundan ve uygulama belgelerinden** derlenmiştir. Bir sürümde farklılık görürseniz
  kendi sürümünüzün davranışı geçerlidir.
- Mevzuat, bant planı ve servis frekansları **genel bilgi** amaçlıdır ve değişebilir.
  Bağlayıcı bilgi için **BTK**, **TRAC** ve ilgili resmî kurumların güncel yayınlarına başvurun.
- Proje sayfası: [github.com/armel/uv-k1-k5v3-firmware-custom](https://github.com/armel/uv-k1-k5v3-firmware-custom)
  · [Wiki](https://github.com/armel/uv-k1-k5v3-firmware-custom/wiki) · [UV Studio](https://armel.github.io/uvstudio/)

73!
