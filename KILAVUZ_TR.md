# F4HWN Fusion Firmware — Türkçe Kullanım Kılavuzu

UV-K1 ve UV-K5 V3 (PY32F071 MCU) telsizleri için F4HWN özel firmware'inin Türkçe
kullanım kılavuzudur. Ayrıntılı ve güncel İngilizce bilgi için
[README.md](README.md) dosyasına ve projenin
[Wiki sayfasına](https://github.com/armel/uv-k1-k5v3-firmware-custom/wiki) bakın.

> [!WARNING]
> Bu firmware'i tamamen kendi sorumluluğunuzda kullanın. Telsizinizde çalışacağına
> dair hiçbir garanti yoktur; hatalı bir yükleme cihazı kullanılamaz hâle getirebilir.

> [!CAUTION]
> Firmware'i yükledikten hemen sonra kalibrasyon verilerinizi
> [UV Studio](https://armel.github.io/uvstudio/#dump-calib) ile yedekleyin.

## İçindekiler

1. [Sürümler (Edition)](#1-sürümler-edition)
2. [Firmware yükleme](#2-firmware-yükleme)
3. [Kalibrasyon yedekleme ve geri yükleme](#3-kalibrasyon-yedekleme-ve-geri-yükleme)
4. [Açılış tuş kombinasyonları](#4-açılış-tuş-kombinasyonları)
5. [Temel kullanım ve tuşlar](#5-temel-kullanım-ve-tuşlar)
6. [F tuşu kısayolları](#6-f-tuşu-kısayolları)
7. [Menü sistemi](#7-menü-sistemi)
8. [Menü öğeleri](#8-menü-öğeleri)
9. [Çıkış gücü seviyeleri](#9-çıkış-gücü-seviyeleri)
10. [Tarama (Scan)](#10-tarama-scan)
11. [Full Watch (çoklu dinleme)](#11-full-watch-çoklu-dinleme)
12. [Multiboot ve Multiconfig](#12-multiboot-ve-multiconfig)
13. [Overlay uygulamaları ve APRS](#13-overlay-uygulamaları-ve-aprs)
14. [Fox Hunt ve Beacon](#14-fox-hunt-ve-beacon)
15. [RF Log](#15-rf-log)
16. [AirCopy ve kablo ile kopyalama](#16-aircopy-ve-kablo-ile-kopyalama)
17. [UV Studio ve K5Viewer](#17-uv-studio-ve-k5viewer)
18. [CHIRP](#18-chirp)
19. [Kaynaktan derleme](#19-kaynaktan-derleme)
20. [Sık karşılaşılan durumlar](#20-sık-karşılaşılan-durumlar)

---

## 1. Sürümler (Edition)

| Sürüm | Açıklama |
|-------|----------|
| **Fusion** | Günlük kullanım için genel referans sürüm. Spektrum analizörü, FM radyo, VOX, UV Studio / K5Viewer, RF Log, Full Watch, Multiboot, Multiconfig ve overlay uygulama platformunu içerir. |
| **Service** | Fusion'a ek olarak AirCopy, BEAM ve harici Flash servis işlemlerini içerir. |
| **Custom** | Gizli teknik varsayılan ayarlara dayanan, elle yapılandırılan derleme. |

> [!NOTE]
> Fusion sürümünde DTMF çağrı ve scrambler (ses karıştırıcı) özellikleri kapalıdır.

## 2. Firmware yükleme

Firmware, tarayıcı üzerinden [UV Studio](https://armel.github.io/uvstudio/) ile
yüklenir. Kurulum, sunucu veya hesap gerekmez. Web Serial destekli bir masaüstü
tarayıcı kullanın (Chrome, Brave, Edge, Opera veya Firefox 151+).

1. UV Studio'da [Flash Firmware](https://armel.github.io/uvstudio/#flash) sayfasını açın.
2. Telsizi uyumlu bir programlama kablosuyla (USB-C veya Baofeng/Kenwood tipi çift
   jaklı USB kablo) bilgisayara bağlayın.
3. Telsizi **DFU (flash) moduna** alın.
4. Katalogdan resmi bir F4HWN Fusion sürümü seçin veya yerel bir `.bin` dosyası yükleyin.
5. `Flash Firmware` düğmesine tıklayın ve telsize ait seri portu seçin.
6. İlerleme çubuğu tamamlanınca telsiz yeni firmware ile yeniden başlar.

## 3. Kalibrasyon yedekleme ve geri yükleme

Kalibrasyon dosyası her telsize özeldir. F4HWN'yi kurduktan hemen sonra yedek alın;
başka bir firmware'e ya da orijinal firmware'e dönmeden önce geri yükleyin.

**Yedekleme (Dump)**

1. [Dump Calibration](https://armel.github.io/uvstudio/#dump-calib) sayfasını açın.
2. Telsizi **normal modda** açın.
3. `Dump Calibration Data` → işlem bitince `Download calibration.dat`.

> [!TIP]
> Dosyayı telsizin seri numarasıyla adlandırın (pilin altındaki etikette yazar).
> Birden fazla telsiziniz varsa dosyaları karıştırmazsınız.

**Geri yükleme (Restore)**

1. [Restore Calibration](https://armel.github.io/uvstudio/#restore-calib) sayfasını açın.
2. Telsizi **normal modda** açın ve `calibration.dat` dosyanızı seçin.
3. `Restore Calibration Data` düğmesine tıklayıp işlemin tamamen bitmesini bekleyin.

## 4. Açılış tuş kombinasyonları

Telsiz kapalıyken aşağıdaki tuşları basılı tutup telsizi açın; ilgili ekran
görününce tuşları bırakın.

| Kombinasyon | Sonuç |
|-------------|-------|
| `MENU` | **Multiboot** firmware seçicisi |
| `PTT` + `SIDE1` (üst yan tuş) | Gizli (servis) menü öğeleri açılır |
| `PTT` + `SIDE2` (alt yan tuş) | **AirCopy** modu (derlemede varsa) |
| `PTT` + gizli tuş (`SetKey`) | Menü kilidini (Rescue Ops) açar/kapatır |

## 5. Temel kullanım ve tuşlar

| Tuş | Görev |
|-----|-------|
| `PTT` | Gönderme (Classic modda basılı tutun; OnePush modda bir kez basıp bir kez daha basarak bırakın) |
| `MENU` | Menüye giriş / seçimi onaylama |
| `EXIT` | Geri / iptal. Uzun basış: VFO durumunu tamamen geri yükler |
| `UP` / `DOWN` | Frekans veya kanal değiştirme, menüde gezinme |
| `0`–`9` | Doğrudan frekans veya kanal numarası girişi |
| `*` | Tarama (Scan) |
| `F` (`#`) | Fonksiyon tuşu; uzun basış tuş takımını kilitler |
| `SIDE1` / `SIDE2` | Kısa ve uzun basışa atanabilen yan tuşlar (`F1Shrt`, `F1Long`, `F2Shrt`, `F2Long`) |

**Ekran modları:** `MAIN ONLY`, `DUAL`, `FULL` ve `CROSS`. Aktif VFO'da alım
göstergesi, susturma (squelch), monitor, adım ve CTCSS/DCS bilgileri, son alım ve
RX/TX süre sayaçları gösterilir.

## 6. F tuşu kısayolları

Önce `F` tuşuna, ardından ilgili tuşa basın.

| Kısayol | İşlev |
|---------|-------|
| `F` + `0` | FM yayın radyosu |
| `F` + `1` | Bant değiştirme (kanal modunda kanalı VFO'ya kopyalar) |
| `F` + `2` | VFO A / VFO B geçişi |
| `F` + `3` | VFO / Hafıza (MR) modu geçişi |
| `F` + `4` | Frekans/ton tarayıcı (Close Call) |
| `F` + `5` | Spektrum analizörü (uzun `5`: kanalın tarama listesini değiştirir) |
| `F` + `6` | Çıkış gücü değiştirme |
| `F` + `7` | Overlay uygulama menüsü (uzun `7`: VOX) |
| `F` + `8` | Arka ışığı geçici olarak min/maks arasında değiştirir (uzun `8`: frekans ters çevirme) |
| `F` + `9` | Ayarlı arka ışık stratejisine döner (uzun `9`: 1 Call kanalı) |
| `F` + `UP` / `DOWN` | Susturma (squelch) seviyesi — kalıcı olarak kaydedilir. Tarama sırasında tarama listesini değiştirir |
| `F` + `SIDE1` / `SIDE2` | Frekans adımını (step) değiştirir |

## 7. Menü sistemi

`MENU` tuşuyla menüye girilir. Fusion'da menü öğeleri kategorilere ayrılmıştır:

`Channels` · `Scan` · `Keys` · `Power` · `Display` · `Timers` · `Audio` ·
`Radio` · `DTMF` · `Service` (yalnızca gizli menü açıkken) · `All`

- `All` kategorisi tüm öğeleri orijinal sıra ve numaralarıyla düz liste olarak gösterir.
- `UP` / `DOWN` ile gezinin, `MENU` ile düzenleyin, tekrar `MENU` ile kaydedin,
  `EXIT` ile iptal edin.
- Rakam tuşlarıyla menü numarasını yazarak doğrudan öğeye gidebilirsiniz.
- Düzenleme sırasında menü numarası ekranda görünmeye devam eder.

## 8. Menü öğeleri

> Not: Bazı öğeler yalnızca ilgili özellik derlemede etkinse görünür.

### Kanal / VFO ayarları

| Menü | Açıklama |
|------|----------|
| `Step` | Frekans adımı |
| `Power` | Çıkış gücü (`USER`, `LOW 1`–`LOW 5`, `MID`, `HIGH`) |
| `RxDCS` / `RxCTCS` | Alım DCS / CTCSS tonu (`*` ile ton taraması) |
| `TxDCS` / `TxCTCS` | Gönderme DCS / CTCSS tonu |
| `TxODir` | Röle kayma yönü (`OFF`, `+`, `-`) |
| `TxOffs` | Röle kayma (offset) miktarı |
| `W/N` | Geniş / dar bant (`WIDE`, `NARROW`) |
| `BusyCL` | Meşgul kanal kilidi |
| `Compnd` | Compander |
| `Mode` | Demodülasyon (FM / AM / USB) |
| `TXLock` | Kanal bazında gönderme kilidi |

### Hafıza kanalları

| Menü | Açıklama |
|------|----------|
| `ChList` | Kanal listesi |
| `ChSave` | Geçerli ayarları kanala kaydet |
| `ChDele` | Kanalı sil |
| `ChName` | Kanal adı düzenleme |

### Tarama

| Menü | Açıklama |
|------|----------|
| `ScList` | Taranacak liste (`ALL`, `01`–`24`, `MIX`) |
| `ScPri` | Öncelikli tarama açık/kapalı |
| `PriCh1` / `PriCh2` | Öncelikli kanal 1 / 2 |
| `ScnRev` | Taramanın devam etme davranışı |
| `SetScn` | Tarama hızı (`NORMAL`, `FAST`) |

### Tuşlar

| Menü | Açıklama |
|------|----------|
| `F1Shrt` / `F1Long` | SIDE1 kısa / uzun basış işlevi |
| `F2Shrt` / `F2Long` | SIDE2 kısa / uzun basış işlevi |
| `M Long` | `MENU` uzun basış işlevi |
| `KeyLck` | Otomatik tuş kilidi |
| `SetLck` | Kilit kapsamı (`KEYS`, `KEYS ACTIONS`, `KEYS PTT`, `KEYS ACTIONS PTT`) |
| `SetPTT` | PTT modu (`CLASSIC`, `ONEPUSH`) |
| `SetNav` | Gezinme düzeni (`LEFT/RIGHT` UV-K1, `UP/DOWN` UV-K5) |
| `SetKey` | Rescue Ops gizli tuşu |

Atanabilir işlevler: `NONE`, `FLASHLIGHT`, `POWER`, `MONITOR`, `SCAN`, `VOX`,
`FM RADIO`, `1750Hz`, `LOCK KEYPAD`, `VFO A/B`, `VFO/MEM`, `MODE`, `RX MODE`,
`MAIN ONLY`, `PTT`, `WIDE/NARROW`, `MUTE`, `RxA`, `RF LOG`, `BEAM`,
`POWER HIGH`, `REMOVE OFFSET`, `FOX HUNT`, `BEACON`, `TONE CALL`.

### Ekran

| Menü | Açıklama |
|------|----------|
| `ChDisp` | Kanal görünümü (`FREQ`, `CHANNEL NUMBER`, `NAME`, `NAME + FREQ`) |
| `POnMsg` | Açılış ekranı (`ALL`, `SOUND`, `MESSAGE`, `VOLTAGE`, `LOGO`, `NONE`) |
| `BLTime` | Arka ışık süresi |
| `BLMin` / `BLMax` | Arka ışık minimum / maksimum parlaklığı |
| `BLTxRx` | TX/RX sırasında arka ışık (`OFF`, `TX`, `RX`, `TX/RX`) |
| `BatTxt` | Durum çubuğunda pil (`NONE`, `VOLTAGE`, `PERCENT`) |
| `MicBar` | Mikrofon seviye çubuğu |
| `SetCtr` | Ekran kontrastı |
| `SetInv` | Ters (negatif) ekran |
| `SetMet` | S-metre stili (`TINY`, `CLASSIC`) |
| `SetGUI` | VFO bilgi düzeni |
| `SetSav` | Ekran koruyucu (`OFF`, `LOGO`, `LOGO+`, `MATRIX`) |

### Zamanlayıcılar ve güç

| Menü | Açıklama |
|------|----------|
| `TxTOut` | Gönderme zaman aşımı (TOT) |
| `SetTOT` | TOT uyarısı (`OFF`, `SOUND`, `VISUAL`, `ALL`) |
| `SetEOT` | Gönderme sonu uyarısı (aynı seçenekler) |
| `SetTmr` | RX / TX süre sayaçları |
| `SetOff` | Otomatik derin uyku süresi |
| `BatSav` | Pil tasarrufu |
| `SetPwr` | `USER` güç seviyesinin değeri |
| `BatVol` / `SysInf` | Pil ve sistem bilgisi |

### Ses

| Menü | Açıklama |
|------|----------|
| `Mic` | Mikrofon kazancı |
| `Beep` | Tuş sesi |
| `Roger` | Gönderme sonu sinyali (`OFF`, `ROGER`, `MDC`) |
| `STE` / `RP STE` | Kuyruk sesi (squelch tail) bastırma / röle için |
| `VOX` | Sesle gönderme seviyesi |
| `SetRxA` | RX ses profili — FM: `FLAT`, `CLEAN`, `MID`, `BOOST`, `MAX`; AM: `SHARP`, `STOCK`, `OPEN` |
| `SetVol` | RX ses seviyesi |

### Radyo

| Menü | Açıklama |
|------|----------|
| `RxMode` | Alım modu (bkz. [Full Watch](#11-full-watch-çoklu-dinleme)) |
| `Sql` | Susturma seviyesi (0–9) |
| `SetNFM` | Dar FM bant genişliği (`NARROW` 12,5 kHz / `NARROWER` 6,25 kHz) |
| `SetCfg` | Başka bir Multiconfig bankasını yeniden başlatmadan uygular |
| `1 Call` | Tek tuş çağrı kanalı |

### DTMF

`ANI ID`, `UPCode`, `DWCode`, `PTT ID` (`OFF`, `UP CODE`, `DOWN CODE`,
`UP+DOWN CODE`, `APOLLO QUINDAR`), `D ST`, `D Decd`, `D List`, `D Live`
(canlı DTMF çözücü).

### Gizli (servis) menü

`PTT` + `SIDE1` ile açılışta görünür:

| Menü | Açıklama |
|------|----------|
| `F Lock` | Bölgesel frekans kilidi (`DEFAULT+`, `FCC HAM`, `CE HAM`, `GB HAM`, `PMR 446`, `GMRS/FRS/MURS`, `DISABLE ALL`, `UNLOCK ALL` vb.) |
| `Tx 200` / `Tx 350` / `Tx 500` | İlgili bantlarda gönderime izin |
| `350 En` | 350 MHz bandını etkinleştirir |
| `FrCali` | Referans kristal (frekans) kalibrasyonu |
| `BatCal` | Pil voltajı kalibrasyonu |
| `BatTyp` | Pil tipi (`1600mAh K5`, `2200mAh K5`, `3500mAh K5`, `1400mAh K1`, `2500mAh K1`) |
| `Reset` | Sıfırlama (`VFO` veya `ALL`) |

> [!CAUTION]
> Gönderme yaparken yalnızca lisansınızın ve yerel mevzuatın izin verdiği
> frekans, güç ve modları kullanın.

## 9. Çıkış gücü seviyeleri

| Seviye | Yaklaşık güç |
|--------|--------------|
| `LOW 1` | < 20 mW |
| `LOW 2` | 125 mW |
| `LOW 3` | 250 mW |
| `LOW 4` | 500 mW |
| `LOW 5` | 1 W |
| `MID` | 2 W |
| `HIGH` | 5 W |
| `USER` | `SetPwr` menüsünden ayarlanır |

S-metre, IARU Bölge 1 VHF/UHF önerisine göre kalibre edilmiştir (sabit S0–S9+ değerleri).

## 10. Tarama (Scan)

- 24 adlandırılmış tarama listesi + 1 karma (`MIX`) liste desteklenir.
- Her hafıza kanalı `OFF`, `01`–`24` arasından bir listeye veya `ALL`'a atanabilir.
- `ALL` listesi, `OFF` olanlar dışındaki tüm kanalları tarar.
- `MIX`, seçtiğiniz listeleri tek bir tarama kümesinde birleştirir.
- Tarama sırasında doğrudan liste seçimi: `00` = `ALL`, `01`–`24` = ilgili liste, `25` = `MIX`.
- Tarama sırasında `MENU` uzun basış: geçerli kanalı taramadan çıkarır.
- 64 adede kadar frekans hariç tutulabilir.
- Hızlı tarama modunda saniyede yaklaşık 150 frekans taranır (`SetScn` = `FAST`).
- Tarama durdurulduğunda `EXIT` başlangıç frekansına döner; `MENU` son bulunan
  yayında kalır.

## 11. Full Watch (çoklu dinleme)

`RxMode` menüsündeki seçenekler:

| Seçenek | Açıklama |
|---------|----------|
| `MAIN ONLY` | Yalnızca ana VFO'da alım ve gönderme |
| `DUAL RX RESPOND` | İki VFO'yu dinler, sinyal gelen VFO'dan cevap verir |
| `CROSS BAND` | Ana VFO'da gönderir, ikincil VFO'da alır |
| `MAIN TX DUAL RX` | İki VFO'yu dinler, her zaman ana VFO'dan gönderir |
| `FULL RX RESPOND` | VFO A, VFO B ve 2 öncelikli kanalı dinler; sinyal gelen kanaldan cevap verir |
| `MAIN TX FULL RX` | Hepsini dinler, her zaman seçili ana VFO'dan gönderir |

Öncelikli kanallar `PriCh1` / `PriCh2` ayarlarından alınır. Tekrarlanan, geçersiz
veya zaten VFO A/B'de yüklü olan kanallar otomatik olarak atlanır. Ekrandaki
hareketli oklar arka plandaki dinleme döngüsünü gösterir.

## 12. Multiboot ve Multiconfig

**Multiboot**, harici Flash'ta otomatik güncellenen bir **Main** yedek ve dört ek
firmware yuvası tutar.

1. Telsizi kapatın, `MENU` tuşunu basılı tutarak açın.
2. Seçici görününce tuşu bırakın.
3. `UP` / `DOWN` ile yuvayı seçin, `MENU` ile geri yükleyin, `EXIT` ile değişiklik
   yapmadan çıkın.

> [!CAUTION]
> Bir yuva geri yüklenirken telsizi asla kapatmayın.

**Multiconfig**, Main ve her yuva için ayrı bir yapılandırma bankası sağlar
(kanallar ve adları, VFO ayarları, tarama listeleri, radyo ayarları). Durum
çubuğunda etkin banka `CFG M` veya `CFG 1`–`CFG 4` olarak görünür.

- `SetCfg` menüsü başka bir bankayı yeniden başlatmadan anında uygular.
- `SetCfg` seçimi normal kapama/açmalarda korunur.
- Multiboot ile firmware değiştirildiğinde doğal eşleşme geri gelir
  (`Main` → `CFG M`, yuva `N` → `CFG N`).

## 13. Overlay uygulamaları ve APRS

`F` + `7` ile uygulama menüsü açılır. Harici Flash'ta 64 uygulamaya kadar yer
vardır; her uygulama çalışırken 4 KiB'lık bir RAM alanına yüklenir.

| Grup | Uygulamalar |
|------|-------------|
| Radyo araçları | Broadcast FM, Fox Hunt, Beacon, Beam, Signal Finder, Spectrum3D, ToneCall |
| Dijital / sinyal | ACARS RX, AIS RX, ATIS RX, ATIS DSC RX, APRS RX, APRS TX, APRS Edit, APRS DIGI, KISS TNC, CW Decode, CW Keyer, CW Trainer, CW USB, SSTV, POCSAG RX, Sonde M10/M20/RS41, GeoNav, EPIRB 406 |
| Araçlar | AF Scope, AF Spectro, QR Map, Resistor, System Info, Flash Map |
| Oyunlar / demolar | Breakout, Cube3D, Hell Maze, Minesweeper, Plasma, Rapid Roll, Snake, Sokoban, Space Impact, Tetris |

**Öne çıkanlar**

- **APRS RX:** 1200 baud Bell 202 AFSK AX.25 çerçevelerini alır, konum ve Mic-E
  verisini gösterir, son 5 çerçeveyi saklar.
- **APRS TX / APRS Edit:** Çağrı işareti, SSID, digipeater yolu, konum, sembol ve
  89 karakterlik yorum düzenlenip konum beacon'ı gönderilir.
- **APRS DIGI:** Sınırlı bir `WIDE1-1` dolgu digipeater'ı.
- **KISS TNC:** USB-C kablo üzerinden telsizi APRSdroid (veya herhangi bir KISS
  istemcisi) için TNC olarak kullanır.
- **GeoNav:** APRS konumunu ev QTH'si olarak alır, radyosonda uygulamasından gelen
  konuma yön ve mesafe gösterir.
- **AF Scope / AF Spectro:** Demodüle edilmiş RX sesi için osiloskop, frekans
  sayacı, akort göstergesi, spektrum ve sonogram. `MENU` ile ikisi arasında geçilir.

> [!IMPORTANT]
> Overlay uygulamaları deneyseldir. Uyumluluk için her zaman kurulu firmware ile
> **aynı sürümde** yayımlanan uygulama dosyalarını kullanın.

## 14. Fox Hunt ve Beacon

**Fox Hunt** (tilki avı alıcısı): kalibre S-metre, kayan sinyal geçmişi grafiği,
tepe/minimum/eğilim göstergeleri, seçilebilir RF zayıflatma, sessiz / Geiger
tarzı / alınan ses modları. `F` uzun basış tuş takımını kilitler (zayıflatma ok
tuşlarıyla ayarlanabilir kalır).

**Beacon** (Mors vericisi): `MOE`, `MOI`, `MOS`, `MOH`, `MO5`, `MO`
tanımlayıcıları, isteğe bağlı çağrı işareti, ayarlanabilir TX ve bekleme
süreleri, canlı geri sayım, kalıcı ayarlar, TX kilidi ve pil güvenlik kontrolleri.

Her iki ekran da UV Studio'daki K5Viewer'a yansıtılır. Yan tuşlara `FOX HUNT` veya
`BEACON` işlevi atanabilir.

## 15. RF Log

RF Log etkinken RX ve TX etkinliği otomatik olarak harici Flash'a kaydedilir:
yön (RX/TX), frekans ve kanal, kanal adı, süre, S-metre seviyesi ve pil voltajı.
Telsizde RX/TX filtreli geçmiş ve ayrıntı görünümü vardır; UV Studio'da canlı
pano, analiz ve CSV dışa aktarma kullanılabilir. Yan tuşa `RF LOG` atanabilir.

## 16. AirCopy ve kablo ile kopyalama

*(Service sürümünde)*

AirCopy, bir 128 kanallık bankayı, radyo ayarlarını veya tüm bankalar + ayarları
tek seferde aktarır. Her iki yönde onaylı (ACK) protokol kullanılır; kayıp onayda
3 kez yeniden denenir. CRC32 karşılaştırmasıyla yalnızca farklı bloklar gönderilir.

**Kullanım**

1. Her iki telsizde AirCopy'yi açın (`PTT` + `SIDE2` ile açılış).
2. `*` ile `AIR COPY` ve `CABLE COPY` arasında geçin.
3. `UP` / `DOWN` ile bir bankayı, `Settings` veya `All (Mem+Set)` seçin.
4. Gönderici telsizde `MENU`, alıcı telsizde `EXIT` tuşuna basın.

**Kablo modu** UART üzerinden 460800 baud hızında çalışır ve ayrıca tüm 2 MiB
harici Flash'ı kopyalayan `Flash 2M` seçeneğini sunar. Cihaza özel kalibrasyon
sektörü asla kopyalanmaz; işlemden sonra alıcı telsizi yeniden başlatın.

> [!IMPORTANT]
> Yeni AirCopy formatı eski sürümlerle uyumlu değildir. İki telsiz de aynı
> firmware sürümünü kullanmalıdır.

## 17. UV Studio ve K5Viewer

[UV Studio](https://armel.github.io/uvstudio/) tek bir tarayıcı arayüzünde şunları sunar:

- Firmware yükleme
- Kalibrasyon yedekleme / geri yükleme
- Açılış logosu yönetimi
- **K5Viewer:** USB seri bağlantı üzerinden canlı ekran yansıtma, ekran görüntüsü
  ve uzaktan tuş takımı kontrolü (USB kopunca otomatik yeniden bağlanır)
- RF Log izleme, analiz ve CSV dışa aktarma

## 18. CHIRP

Bu firmware için özel bir CHIRP sürücüsü gerekir. Uygun sürücü her sürümle birlikte
[Releases](https://github.com/armel/uv-k1-k5v3-firmware-custom/releases) sayfasında
yayımlanır; firmware ile sürücüyü aynı sürümden indirin.

## 19. Kaynaktan derleme

Gereksinimler: Docker ve Bash ortamı (Linux, macOS, WSL veya Windows'ta Git Bash).

```bash
./compile-firmware.sh [Preset] [ek CMake seçenekleri]
```

Hazır ayarlar (preset): `Fusion` (varsayılan), `Service`, `Custom`, `All`
(Fusion + Service). Çıktılar `build/<Preset>` dizinine `.elf`, `.bin` ve `.hex`
olarak yazılır.

Örnekler:

```bash
./compile-firmware.sh Fusion
```

```bash
./compile-firmware.sh Service -DENABLE_VOX=OFF
```

```bash
./compile-firmware.sh Fusion -DDEV=ON
```

İlk çalıştırmada Docker imajı oluşturulduğu için birkaç dakika sürebilir.

## 20. Sık karşılaşılan durumlar

| Durum | Çözüm |
|-------|-------|
| AM alımı bozuk / parazitli | Telsizin ön katında bant filtresi yoktur; güçlü RF ortamlarında bu donanımsal bir sınırlamadır. RF zayıflatma veya FM kullanın. |
| Menü öğeleri eksik | Kilitli olabilir (Rescue Ops); `PTT` + `SetKey` tuşuyla açılışta kilidi kaldırın. Servis öğeleri için `PTT` + `SIDE1` ile açın. |
| Gönderme yapılamıyor | `F Lock` bölge ayarını, kanalın `TXLock` durumunu ve `SetLck` kilit kapsamını kontrol edin. |
| Overlay uygulaması açılmıyor | Uygulama dosyalarının kurulu firmware ile aynı sürümden olduğundan emin olun. |
| Firmware değişince ayarlar farklı | Multiboot doğal bankayı geri yükler; gerekirse `SetCfg` ile istenen bankayı tekrar seçin. |
| Ok tuşları ters çalışıyor | `SetNav` menüsünden telsiz modelinize uygun düzeni seçin (UV-K1 / UV-K5). |

---

73! İyi kullanımlar.
