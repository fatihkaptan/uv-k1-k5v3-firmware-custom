# 10. Menü Referansı

[← Önceki: Cihaz kullanımı](09-cihaz-kullanimi.md) · [İçindekiler](README.md) · [Sonraki: Uygulamalar →](11-uygulamalar.md)

Bu bölüm F4HWN firmware'indeki **her menü öğesini**, alabileceği değerleri ve ne işe
yaradığını kategori sırasıyla anlatır. Değer aralıkları kaynak koddan
(`App/ui/menu.c`, `App/app/menu.c`, `App/app/menu_settings.def`) alınmıştır.

> [!NOTE]
> Bazı öğeler yalnızca ilgili özelliği içeren sürümlerde görünür. Örneğin `SetKey`
> yalnızca FieldOps ve Labs'ta bulunur. Bir öğe sizde yoksa sürümünüzde derlenmemiştir.

## İçindekiler

1. [Menü nasıl kullanılır?](#101-menü-nasıl-kullanılır)
2. [Kategori haritası](#102-kategori-haritası)
3. [Kanal ayarları (Channels)](#103-kanal-ayarları-channels)
4. [Tarama (Scan)](#104-tarama-scan)
5. [Tuşlar (Keys)](#105-tuşlar-keys)
6. [Güç (Power)](#106-güç-power)
7. [Ekran (Display)](#107-ekran-display)
8. [Zamanlayıcılar (Timers)](#108-zamanlayıcılar-timers)
9. [Ses (Audio)](#109-ses-audio)
10. [Radyo (Radio)](#1010-radyo-radio)
11. [DTMF](#1011-dtmf)
12. [Servis / gizli menü (Service)](#1012-servis--gizli-menü-service)

---

## 10.1 Menü nasıl kullanılır?

1. **`MENU`**: Menüyü açar. Önce **kategori listesi** gelir; durum çubuğunda `MENU` yazar.
2. **`UP` / `DOWN`**: Kategori seçin, **`MENU`** ile girin. Durum çubuğunda kategori adı görünür.
3. Kategorinin içinde `UP`/`DOWN` ile öğe seçin, **`MENU`** ile düzenlemeye geçin.
4. Değeri `UP`/`DOWN` ile değiştirin (bazı öğelerde rakamlarla da girilir).
5. **`MENU`**: Kaydet. **`EXIT`**: Vazgeç.
6. **`EXIT`** bir üst seviyeye döner; kategori listesinde `EXIT` menüden çıkar.

**Kısayollar**

- Kategori ekranındayken **menü numarasını** yazmak (`1`–`2` hane) doğrudan `All`
  listesindeki o öğeye götürür.
- Telsiz her kategoride en son kaldığınız öğeyi hatırlar.
- Düzenleme sırasında menü numarası ekranda kalır.
- `RxCTCS` / `RxDCS` öğesindeyken **`*`**: Ton taraması.

## 10.2 Kategori haritası

| Kategori | Öğeler |
|----------|--------|
| **Channels** | `Step`, `Power`, `SetPwr`, `RxDCS`, `RxCTCS`, `TxDCS`, `TxCTCS`, `TxODir`, `TxOffs`, `W/N`, `SetNFM`, `BusyCL`, `Compnd`, `Mode`, `TXLock`, `PTT ID`, `ChList`, `ChSave`, `ChDele`, `ChName`, `SetCfg` |
| **Scan** | `ScList`, `ScPri`, `PriCh1`, `PriCh2`, `ScnRev`, `SetScn` |
| **Keys** | `F1Shrt`, `F1Long`, `F2Shrt`, `F2Long`, `M Long`, `KeyLck`, `SetLck`, `SetKey`, `SetPTT`, `1 Call` |
| **Power** | `BatSav`, `BatTxt`, `SetOff`, `SetSav` |
| **Display** | `ChDisp`, `POnMsg`, `BLTime`, `BLMin`, `BLMax`, `BLTxRx`, `SetCtr`, `SetInv`, `SetMet`, `SetGUI`, `SysInf` |
| **Timers** | `TxTOut`, `SetTOT`, `SetEOT`, `SetTmr` |
| **Audio** | `Mic`, `MicBar`, `Beep`, `SetVol`, `SetRxA` |
| **Radio** | `Sql`, `STE`, `RP STE`, `Roger`, `VOX`, `RxMode` |
| **DTMF** | `UPCode`, `DWCode`, `D ST`, `D Prel`, `D Live` |
| **Service** (gizli) | `F Lock`, `350 En`, `BatCal`, `BatTyp`, `SetNav`, `Reset` |
| **All** | Hepsi, orijinal sıra ve numaralarıyla |

## 10.3 Kanal ayarları (Channels)

Bu ayarlar **geçerli VFO'ya veya kanala** uygulanır. Kanala kalıcı olarak yazmak için
VFO'da ayarlayıp `ChSave` ile kaydedin.

| Menü | Değerler | Açıklama |
|------|----------|----------|
| **`Step`** | 0,01 · 0,05 · 0,1 · 0,25 · 0,5 · 1 · 1,25 · 2,5 · 5 · 6,25 · 8,33 · 9 · 10 · 12,5 · 15 · 20 · 25 · 30 · 50 · 100 · 125 · 200 · 250 · 500 kHz | `UP`/`DOWN` adımı ve frekans girişinin yuvarlanacağı ızgara. Amatör FM: 12,5 veya 25 kHz. Havacılık: 25 veya 8,33 kHz. PMR446: 6,25 kHz. |
| **`Power`** | `USER`, `LOW 1`–`LOW 5`, `MID`, `HIGH` | Çıkış gücü (bkz. [3.4](03-desibel-ve-sinyal-olcumu.md#34-telsizin-güç-seviyeleri-dbm-olarak)) |
| **`SetPwr`** | `< 20m`, `125m`, `250m`, `500m`, `1`, `2`, `5` (W) | `USER` gücünün değeri |
| **`RxDCS`** | `OFF`, `D023N` … `D754I` (104 kod × N/I) | Alım DCS kodu. Ayarlıysa yalnızca bu kodu taşıyan sinyaller duyulur. |
| **`RxCTCS`** | `OFF`, 67,0 … 254,1 Hz (50 ton) | Alım CTCSS tonu |
| **`TxDCS`** | `OFF`, DCS kodları | Gönderimde eklenecek DCS kodu |
| **`TxCTCS`** | `OFF`, CTCSS tonları | Gönderimde eklenecek CTCSS tonu (röle erişimi) |
| **`TxODir`** | `OFF`, `+`, `-` | Röle kayma yönü |
| **`TxOffs`** | MHz cinsinden | Kayma miktarı (2 m: 0,600; 70 cm: 1,6 veya 7,6, yerel röleye göre) |
| **`W/N`** | `WIDE`, `NARROW` | Kanal genişliği: 25 / 12,5 kHz (bkz. [4.3](04-modulasyon-ve-sinyal-turleri.md#43-fm-frekans-modülasyonu)) |
| **`SetNFM`** | `NARROW`, `NARROWER` | Dar modun genişliği: 12,5 / 6,25 kHz |
| **`BusyCL`** | `OFF`, `ON` | Meşgul kanal kilidi: kanalda sinyal varken gönderimi engeller |
| **`Compnd`** | `OFF`, `TX`, `RX`, `TX/RX` | Compander: hangi yönde etkin olacağı |
| **`Mode`** | `FM`, `AM`, `USB` | Modülasyon |
| **`TXLock`** | `OFF`, `ON` | `ON` (varsayılan): `F Lock` dışındaki frekansta gönderimi engeller. `OFF`: **bu kanal için bölge kilidini devre dışı bırakır. Dikkat!** |
| **`PTT ID`** | `OFF`, `UP CODE`, `DOWN CODE`, `UP+DOWN CODE`, `APOLLO QUINDAR` | Gönderimin başında/sonunda otomatik DTMF kodu veya Apollo "bip" tonları |
| **`ChList`** | `OFF`, `01`–`24`, `ALL` | Kanalın tarama listesi. `OFF`: hiçbir taramaya girmez. |
| **`ChSave`** | Kanal 1–1024 | Geçerli VFO'yu kanala kaydet |
| **`ChDele`** | Kanal 1–1024 | Kanalı sil |
| **`ChName`** | 10 karakter | Kanal adı (düzenleyici için bkz. [9.7](09-cihaz-kullanimi.md#97-hafıza-kanalları)) |
| **`SetCfg`** | `M`, `1`–`4` | Multiconfig bankasını yeniden başlatmadan uygula (bkz. [9.20](09-cihaz-kullanimi.md#920-multiboot-ve-multiconfig)) |

## 10.4 Tarama (Scan)

| Menü | Değerler | Açıklama |
|------|----------|----------|
| **`ScList`** | `01`–`24`, `ALL`, `MIX` | Kanal taramasında kullanılacak liste. `MIX` seçilip `MENU`'ye basılınca MIX düzenleyici açılır. |
| **`ScPri`** | `OFF`, `ON` | Tarama sırasında öncelikli kanalları kontrol et |
| **`PriCh1`** | Kanal veya `None` | Öncelikli kanal 1 (tarama ve Full Watch) |
| **`PriCh2`** | Kanal veya `None` | Öncelikli kanal 2 |
| **`ScnRev`** | `STOP`; `CARRIER` 0,25 s – 20 s; `TIMEOUT` 5 s – 2 dk | Sinyal bulununca: dur / sinyal kesildikten belirtilen süre sonra devam et / belirtilen süre sonra her durumda devam et |
| **`SetScn`** | `NORMAL`, `FAST` | Tarama hızı. `FAST`: ≈ 150 frekans/saniye |

## 10.5 Tuşlar (Keys)

| Menü | Değerler | Açıklama |
|------|----------|----------|
| **`F1Shrt`** | İşlev listesi | `SIDE1` kısa basış (varsayılan `MONITOR`) |
| **`F1Long`** | İşlev listesi | `SIDE1` uzun basış |
| **`F2Shrt`** | İşlev listesi | `SIDE2` kısa basış (varsayılan `SCAN`) |
| **`F2Long`** | İşlev listesi | `SIDE2` uzun basış |
| **`M Long`** | İşlev listesi | `MENU` uzun basış |
| **`KeyLck`** | `OFF`, 15 s – 10 dk | Bu süre tuşa basılmazsa tuş takımını otomatik kilitle |
| **`SetLck`** | `KEYS`, `KEYS ACTIONS`, `KEYS PTT`, `KEYS ACTIONS PTT` | Kilit neleri kapsasın: tuşlar / tuşlar ve yan tuş aksiyonları / tuşlar ve PTT / hepsi |
| **`SetKey`** | `KEY_MENU`, `KEY_UP`, `KEY_DOWN`, `KEY_EXIT`, `KEY_STAR` | Rescue Ops kilidini açılışta açıp kapatan gizli tuş (`PTT` ile birlikte) |
| **`SetPTT`** | `CLASSIC`, `ONEPUSH` | PTT davranışı |
| **`1 Call`** | Kanal | Uzun `9` ile gidilecek kanal |

### Atanabilir işlevler

| İşlev | Ne yapar? |
|-------|-----------|
| `NONE` | Hiçbir şey |
| `FLASHLIGHT` | Fener: kapalı → açık → yanıp sönme → SOS |
| `POWER` | Çıkış gücünü sırayla değiştir |
| `MONITOR` | Susturucuyu geçici olarak aç |
| `SCAN` | Taramayı başlat/durdur |
| `VOX` | VOX'u aç/kapat |
| `FM RADIO` | FM yayın radyosu |
| `1750Hz` | Gönderimde 1750 Hz tonu (röle açma) |
| `LOCK KEYPAD` | Tuş kilidi |
| `VFO A VFO B` | A ↔ B |
| `VFO MEM` | VFO ↔ kanal modu |
| `MODE` | Modülasyonu değiştir (FM / AM / USB) |
| `RX MODE` | Alım modunu sırayla değiştir (`RxMode`) |
| `MAIN ONLY` | Ekranı tek VFO'ya indir / geri getir |
| `PTT` | Sanal PTT (yan tuşla gönderim) |
| `WIDE NARROW` | `W/N`'yi değiştir |
| `MUTE` | Sesi kapat/aç |
| `RxA` | Alım ses profilini değiştir |
| `RF LOG` | RF Log geçmişini aç. Bu işlev bir tuşa atanınca kayıt da etkinleşir. |
| `BEAM` | BEAM kanal aktarımı (Transfer, Labs) |
| `POWER HIGH` | Geçici olarak en yüksek güç |
| `REMOVE OFFSET` | Röle kaymasını geçici olarak kaldır (simpleks gönderim) |
| `FOX HUNT` | Fox Hunt alıcısı (FieldOps, Labs) |
| `BEACON` | Beacon vericisi (FieldOps, Labs) |
| `TONE CALL` | ToneCall uygulaması (Labs, uygulama yüklüyse; değilse `N/A`) |

## 10.6 Güç (Power)

| Menü | Değerler | Açıklama |
|------|----------|----------|
| **`BatSav`** | `OFF`, `1:1` … `1:5` | Pil tasarrufu. Oran büyüdükçe alıcı daha uzun süre kapalı kalır. Yayınların başı kaçabilir. |
| **`BatTxt`** | `NONE`, `VOLTAGE`, `PERCENT` | Durum çubuğunda pil gösterimi |
| **`SetOff`** | `OFF`, 1 dk – 2 sa | İşlem yapılmazsa otomatik derin uyku |
| **`SetSav`** | `OFF`, `LOGO`, `LOGO+`, `MATRIX` | Ekran koruyucu |

## 10.7 Ekran (Display)

| Menü | Değerler | Açıklama |
|------|----------|----------|
| **`ChDisp`** | `FREQ`, `CHANNEL NUMBER`, `NAME`, `NAME + FREQ` | Kanal modunda ne gösterilsin |
| **`POnMsg`** | `ALL`, `SOUND`, `MESSAGE`, `VOLTAGE`, `LOGO`, `NONE` | Açılış ekranı ve sesi |
| **`BLTime`** | `OFF`, 5 s – 5 dk, `ON` | Arka ışık süresi. `ON`: sürekli açık |
| **`BLMin`** | 0–9 | Arka ışığın kısık parlaklığı |
| **`BLMax`** | 1–10 | Arka ışığın tam parlaklığı |
| **`BLTxRx`** | `OFF`, `TX`, `RX`, `TX/RX` | Gönderim ve/veya alımda arka ışığı aç |
| **`SetCtr`** | 1–15 | Kontrast |
| **`SetInv`** | `OFF`, `ON` | Ters (negatif) ekran |
| **`SetMet`** | `TINY`, `CLASSIC` | S-metre stili |
| **`SetGUI`** | `TINY`, `CLASSIC` | VFO bilgi satırı stili |
| **`SysInf`** | Sayfalar | Sistem bilgisi: sürüm ve sürüm adı, derleme tarihi, pil, flash/RAM kullanımı, proje ve wiki QR kodları. `UP`/`DOWN` ile sayfa değiştirin. |

## 10.8 Zamanlayıcılar (Timers)

| Menü | Değerler | Açıklama |
|------|----------|----------|
| **`TxTOut`** | 30 s – 15 dk | Gönderim zaman aşımı |
| **`SetTOT`** | `OFF`, `SOUND`, `VISUAL`, `ALL` | Zaman aşımı yaklaşırken uyarı |
| **`SetEOT`** | `OFF`, `SOUND`, `VISUAL`, `ALL` | Karşı tarafın yayını bitince uyarı (görsel: yeşil LED yanıp söner) |
| **`SetTmr`** | `OFF`, `ON` | Durum çubuğunda RX/TX süre sayacı |

## 10.9 Ses (Audio)

| Menü | Değerler | Açıklama |
|------|----------|----------|
| **`Mic`** | +1,5 · +4,0 · +8,0 · +12,0 · +16,0 · +20,0 · +24,0 · +28,0 · +31,5 dB | Mikrofon kazancı |
| **`MicBar`** | `OFF`, `ON` | Gönderimde mikrofon seviye çubuğu |
| **`Beep`** | `OFF`, `ON` | Tuş sesleri |
| **`SetVol`** | `OFF`, 1–63 | Dijital alım ses kazancı |
| **`SetRxA`** | FM: `FLAT`, `CLEAN`, `MID`, `BOOST`, `MAX` · AM: `SHARP`, `STOCK`, `OPEN` | Alım ses profili. Seçenekler geçerli modülasyona göre değişir; USB'de profil yoktur. |

## 10.10 Radyo (Radio)

| Menü | Değerler | Açıklama |
|------|----------|----------|
| **`Sql`** | 0–9 | Susturucu seviyesi (bkz. [3.8](03-desibel-ve-sinyal-olcumu.md#38-alıcı-hassasiyeti-sinad-ve-squelch)) |
| **`STE`** | `OFF`, `ON` | Squelch kuyruk sesini bastır |
| **`RP STE`** | `OFF`, 1–10 × 100 ms | Röle kuyruk sesini bastırma süresi |
| **`Roger`** | `OFF`, `ROGER`, `MDC` | Gönderim sonu bipi |
| **`VOX`** | `OFF`, 1–10 | VOX hassasiyeti (düşük değer = daha hassas) |
| **`RxMode`** | `MAIN ONLY`, `DUAL RX RESPOND`, `CROSS BAND`, `MAIN TX DUAL RX`, `FULL RX RESPOND`, `MAIN TX FULL RX` | Alım modu (bkz. [9.11](09-cihaz-kullanimi.md#911-alım-modları-dual-watch-full-watch-cross-band)) |

## 10.11 DTMF

| Menü | Değerler | Açıklama |
|------|----------|----------|
| **`UPCode`** | DTMF dizisi | Gönderim başında gönderilecek kod (`PTT ID`) |
| **`DWCode`** | DTMF dizisi | Gönderim sonunda gönderilecek kod |
| **`D ST`** | `OFF`, `ON` | DTMF gönderirken tonları hoparlörden de duy |
| **`D Prel`** | 30–990 ms | DTMF göndermeden önceki bekleme (karşı tarafın squelch'inin açılması için) |
| **`D Live`** | `OFF`, `ON` | Gelen DTMF tonlarını ekranda canlı göster |

Fusion ve türevlerinde **DTMF çağrı** (ANI, kişi listesi, uzaktan susturma) özellikleri kapalıdır.

## 10.12 Servis / gizli menü (Service)

Yalnızca telsiz **`PTT` + `SIDE1`** basılıyken açıldığında görünür.

| Menü | Değerler | Açıklama |
|------|----------|----------|
| **`F Lock`** | `DEFAULT+`, `FCC HAM`, `CA HAM`, `CE HAM`, `GB HAM`, `137-174 400-430`, `137-174 400-438`, `PMR 446`, `GMRS FRS MURS`, `DISABLE ALL`, `UNLOCK ALL` | Gönderim bölge kilidi. Aralıklar için bkz. [7.1](07-frekans-rehberi.md#71-telsizin-alım-ve-gönderim-aralıkları). **Türkiye: `CE HAM`; belgesiz: `DISABLE ALL`.** |
| **`350 En`** | `OFF`, `ON` | 350–400 MHz bandını etkinleştir |
| **`BatCal`** | 1500–3500 | Pil ölçüm kalibrasyonu. Ekrandaki gerilimi multimetreyle ölçtüğünüz gerçek değere eşitleyin. |
| **`BatTyp`** | `1600mAh K5`, `2200mAh K5`, `3500mAh K5`, `1400mAh K1`, `2500mAh K1` | Pil tipi: yüzde hesabı ve düşük pil eşiği buna göre yapılır |
| **`SetNav`** | `LEFT/RIGHT UV-K1`, `UP/DOWN UV-K5(8)` | Yön tuşlarının düzeni |
| **`Reset`** | `VFO`, `ALL` | Sıfırlama. `ALL` kanalları da siler. |

> [!NOTE]
> Bazı derlemelerde gizli menüde **`FrCali`** (referans kristal kalibrasyonu, −50 … +50)
> de bulunur. v6 yayın sürümlerinde bu öğe derlenmemiştir.

---

[← Önceki: Cihaz kullanımı](09-cihaz-kullanimi.md) · [İçindekiler](README.md) · [Sonraki: Uygulamalar →](11-uygulamalar.md)
