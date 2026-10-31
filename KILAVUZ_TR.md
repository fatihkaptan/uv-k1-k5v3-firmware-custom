# F4HWN Firmware: Türkçe Hızlı Başvuru Kılavuzu

UV-K1 ve UV-K5 V3 (PY32F071 MCU) telsizleri için F4HWN özel firmware'inin Türkçe hızlı
başvuru kılavuzu. Bu sayfa en sık gereken bilgileri bir arada verir.

> [!TIP]
> **Ayrıntılı Türkçe rehber**: [kilavuz/](kilavuz/README.md). Elektrik ve radyo temelleri,
> desibel ve S-metre, modülasyon, antenler, amatör telsizcilik, frekans rehberi, donanım
> ve ekran simgeleri, adım adım kullanım, menü referansı, uygulamalar, senaryolar, sözlük ve
> sorun giderme bölümlerinden oluşur.

> [!WARNING]
> Bu firmware'i tamamen kendi sorumluluğunuzda kullanın. Telsizinizde çalışacağına dair
> hiçbir garanti yoktur. Amatör bantlarda gönderim için **BTK belgesi** gerekir.

> [!CAUTION]
> Firmware'i yükledikten hemen sonra kalibrasyon verilerinizi
> [UV Studio](https://armel.github.io/uvstudio/#dump-calib) ile yedekleyin.

## İçindekiler

1. [Sürümler](#1-sürümler)
2. [Firmware yükleme ve kalibrasyon](#2-firmware-yükleme-ve-kalibrasyon)
3. [Başlangıç ayarları](#3-başlangıç-ayarları)
4. [Açılış tuş kombinasyonları](#4-açılış-tuş-kombinasyonları)
5. [Tuşlar](#5-tuşlar)
6. [F kısayolları ve uzun basışlar](#6-f-kısayolları-ve-uzun-basışlar)
7. [Menü](#7-menü)
8. [Çıkış gücü](#8-çıkış-gücü)
9. [Tarama](#9-tarama)
10. [Alım modları ve Full Watch](#10-alım-modları-ve-full-watch)
11. [Multiboot ve Multiconfig](#11-multiboot-ve-multiconfig)
12. [Uygulamalar (Labs)](#12-uygulamalar-labs)
13. [RF Log, Fox Hunt, Beacon, BEAM, AirCopy](#13-rf-log-fox-hunt-beacon-beam-aircopy)
14. [UV Studio, K5Viewer ve CHIRP](#14-uv-studio-k5viewer-ve-chirp)
15. [Kaynaktan derleme](#15-kaynaktan-derleme)
16. [Sık karşılaşılan durumlar](#16-sık-karşılaşılan-durumlar)

---

## 1. Sürümler

| Sürüm | İçerik |
|-------|--------|
| **Fusion** | Temel sürüm: spektrum analizörü, FM radyo, VOX, Full Watch, Multiboot, Multiconfig, RF Log, menü kategorileri, ekran koruyucu |
| **FieldOps** | Fusion + Rescue Ops (menü kilidi) + yerleşik Fox Hunt ve Beacon |
| **Transfer** | Fusion + AirCopy (kablosuz, kablolu, `Flash 2M`) + BEAM |
| **Labs** | Fusion + **overlay uygulamaları** (APRS, AIS, ACARS, sondalar, CW, SSTV, Fox Hunt, Beacon, BEAM, oyunlar…) + AirCopy + Rescue Ops |

Fusion ve türevlerinde DTMF çağrı ve scrambler özellikleri kapalıdır.
Ayrıntı: [kilavuz/08 §8.1](kilavuz/08-cihaz-donanimi-ve-ekran.md#81-firmware-sürümleri-edition).

## 2. Firmware yükleme ve kalibrasyon

Firmware tarayıcıdan, [UV Studio](https://armel.github.io/uvstudio/) ile yüklenir. Web Serial
destekli bir masaüstü tarayıcı kullanın (Chrome, Brave, Edge, Opera veya Firefox 151+).

**Yükleme**

1. [Flash Firmware](https://armel.github.io/uvstudio/#flash) sayfasını açın.
2. Telsizi USB-C veya Kenwood tipi çift jaklı programlama kablosuyla bağlayın.
3. Telsizi **DFU (flash) moduna** alın.
4. Katalogdan bir F4HWN sürümü seçin veya yerel `.bin` dosyası yükleyin.
5. `Flash Firmware` → seri portu seçin → işlemin bitmesini bekleyin.

**Kalibrasyon yedeği** (telsiz **normal modda**)

- Yedek: [Dump Calibration](https://armel.github.io/uvstudio/#dump-calib) → `Dump Calibration Data` → `Download calibration.dat`.
- Geri yükleme: [Restore Calibration](https://armel.github.io/uvstudio/#restore-calib) → dosyayı seçin → `Restore Calibration Data`.
- Dosyayı telsizin seri numarasıyla adlandırın. Başka bir firmware'e geçmeden önce geri yükleyin.

## 3. Başlangıç ayarları

1. Telsizi **`PTT` + `SIDE1`** basılıyken açın: gizli menü öğeleri açılır.
2. **`F Lock`**: belgeli amatör için **`CE HAM`** (144–146 / 430–440 MHz); belgesiz için **`DISABLE ALL`**.
3. **`BatTyp`**: pilinize uygun tip.
4. **`SetNav`**: UV-K1 için `LEFT/RIGHT`, UV-K5 için `UP/DOWN`.
5. Squelch: `F` + `UP`/`DOWN` ile 3–4.
6. Tuş kilidi kapsamı: `SetLck` → `KEYS PTT`. Kilitlemek/açmak için uzun `F`.

> [!WARNING]
> Varsayılan `F Lock` (`DEFAULT+`) birçok kamu ve profesyonel banda gönderime izin verir.
> Bir kanalda `TXLock` = `OFF` yapmak ise o kanal için bölge kilidini tamamen devre dışı bırakır.

## 4. Açılış tuş kombinasyonları

Telsiz kapalıyken tuşları basılı tutup açın; ekran gelince bırakın.

| Kombinasyon | Sonuç | Sürüm |
|-------------|-------|-------|
| `MENU` | Multiboot firmware seçicisi | Hepsi |
| `PTT` + `SIDE1` | Gizli (servis) menü öğeleri | Hepsi |
| `PTT` + `SIDE2` | AirCopy modu | Transfer, Labs |
| `PTT` + gizli tuş (`SetKey`, varsayılan `MENU`) | Rescue Ops menü kilidini aç/kapat | FieldOps, Labs |

## 5. Tuşlar

| Tuş | Kısa basış | Uzun basış |
|-----|------------|------------|
| `PTT` | Gönderim (`SetPTT`: `CLASSIC` basılı tut / `ONEPUSH` bas-başlat, bas-bitir) | — |
| `MENU` | Menü / onay | `M Long` işlevi; tarama sırasında bulunan kanalı/frekansı hariç tut |
| `EXIT` | Geri, son rakamı sil, taramayı durdurup başa dön | VFO'yu rakam girişinden önceki tam durumuna geri yükle |
| `UP` / `DOWN` | Frekans/kanal değiştir; taramada sonraki sinyale atla | Hızlı ilerleme |
| `0`–`9` | Frekans (6 hane, kHz) veya kanal numarası | `F` işlevi (bkz. §6) |
| `*` | **DTMF giriş modu** | **Taramayı başlat/durdur** |
| `F` (`#`) | Bir sonraki tuşa ikinci işlevini verir | Tuş kilidi |
| `SIDE1` | `F1Shrt` (varsayılan `MONITOR`) | `F1Long` |
| `SIDE2` | `F2Shrt` (varsayılan `SCAN`) | `F2Long` |

## 6. F kısayolları ve uzun basışlar

Önce `F`'ye basıp bırakın, sonra ikinci tuşa basın.

| Kısayol | `F` + tuş | Uzun basış (`F`'siz) |
|---------|-----------|----------------------|
| `0` | FM yayın radyosu | Aynı |
| `1` | Bant değiştir (kanal modunda: kanalı VFO'ya kopyala) | Aynı |
| `2` | VFO A ↔ VFO B | Aynı |
| `3` | VFO ↔ kanal (MR) modu | Aynı |
| `4` | Frekans yakalama tarayıcısı (yakındaki vericinin frekansı ve tonu) | Aynı |
| `5` | Spektrum analizörü | Kanal modunda: kanalın tarama listesini değiştir. VFO modunda: tarama aralığı (`ScnRng`, VFO A–B arası) |
| `6` | Çıkış gücünü değiştir | Aynı |
| `7` | **Labs**: uygulama menüsü. Diğer sürümler: VOX | VOX aç/kapat |
| `8` | Arka ışığı geçici olarak min ↔ maks | Ters frekans (reverse) |
| `9` | Ayarlı arka ışık davranışına dön | `1 Call` kanalına git |
| `*` | CTCSS/DCS ton taraması | — |
| `UP` / `DOWN` | Squelch seviyesi (kalıcı). Taramada: tarama listesi | — |
| `SIDE1` / `SIDE2` | Frekans adımı | `F` + uzun `SIDE1`/`SIDE2`: **aksiyon seçici** |

## 7. Menü

`MENU` önce kategori listesini açar:
`Channels` · `Scan` · `Keys` · `Power` · `Display` · `Timers` · `Audio` · `Radio` · `DTMF` ·
`Service` (yalnızca gizli menü açıkken) · `All`.

- `UP`/`DOWN` ile seçin, `MENU` ile girin/düzenleyin/kaydedin, `EXIT` ile geri dönün.
- Kategori ekranında menü numarasını yazmak, `All` listesindeki o öğeye götürür.

| Kategori | Öğeler |
|----------|--------|
| Channels | `Step`, `Power`, `SetPwr`, `RxDCS`, `RxCTCS`, `TxDCS`, `TxCTCS`, `TxODir`, `TxOffs`, `W/N`, `SetNFM`, `BusyCL`, `Compnd`, `Mode`, `TXLock`, `PTT ID`, `ChList`, `ChSave`, `ChDele`, `ChName`, `SetCfg` |
| Scan | `ScList`, `ScPri`, `PriCh1`, `PriCh2`, `ScnRev`, `SetScn` |
| Keys | `F1Shrt`, `F1Long`, `F2Shrt`, `F2Long`, `M Long`, `KeyLck`, `SetLck`, `SetKey`, `SetPTT`, `1 Call` |
| Power | `BatSav`, `BatTxt`, `SetOff`, `SetSav` |
| Display | `ChDisp`, `POnMsg`, `BLTime`, `BLMin`, `BLMax`, `BLTxRx`, `SetCtr`, `SetInv`, `SetMet`, `SetGUI`, `SysInf` |
| Timers | `TxTOut`, `SetTOT`, `SetEOT`, `SetTmr` |
| Audio | `Mic`, `MicBar`, `Beep`, `SetVol`, `SetRxA` |
| Radio | `Sql`, `STE`, `RP STE`, `Roger`, `VOX`, `RxMode` |
| DTMF | `UPCode`, `DWCode`, `D ST`, `D Prel`, `D Live` |
| Service (gizli) | `F Lock`, `350 En`, `BatCal`, `BatTyp`, `SetNav`, `Reset` |

Her öğenin değerleri ve açıklaması: [kilavuz/10 Menü referansı](kilavuz/10-menu-referansi.md).

## 8. Çıkış gücü

| Seviye | Yaklaşık güç | dBm |
|--------|--------------|-----|
| `LOW 1` | < 20 mW | < 13 |
| `LOW 2` | 125 mW | 21 |
| `LOW 3` | 250 mW | 24 |
| `LOW 4` | 500 mW | 27 |
| `LOW 5` | 1 W | 30 |
| `MID` | 2 W | 33 |
| `HIGH` | 5 W | 37 |
| `USER` | `SetPwr` ile seçilir | — |

S-metre IARU Bölge 1 ölçeğindedir: **S9 = −93 dBm**, her S birimi 6 dB.

## 9. Tarama

- **Başlat/durdur**: uzun `*` veya `SIDE2`. **`EXIT`**: durdur ve başa dön. **`MENU`**: bulunan sinyalde kal.
- **Listeler**: 24 adlandırılmış liste + `ALL` + `MIX`. Kanala liste atamak için kanal modunda uzun `5`.
- Tarama sırasında liste seçimi: `00` = `ALL`, `01`–`24`, `25` = `MIX`; veya `F` + `UP`/`DOWN`.
- `ScList` → `MIX` → `MENU`: MIX düzenleyici (`MENU` ile listeleri ekle/çıkar, `EXIT` ile kaydet).
- Tarama dururken **uzun `MENU`**: bulunan kanalı/frekansı taramadan çıkar (en fazla 64 frekans).
- **Tarama aralığı**: VFO A'ya alt, VFO B'ye üst frekansı yazın, VFO modunda uzun `5`, sonra uzun `*`.
- `SetScn` = `FAST`: saniyede ≈ 150 frekans. `ScnRev`: durma / devam davranışı.

## 10. Alım modları ve Full Watch

`RxMode`:

| Seçenek | Açıklama |
|---------|----------|
| `MAIN ONLY` | Yalnızca ana VFO |
| `DUAL RX RESPOND` | A ve B'yi dinle, sinyal gelenden cevap ver |
| `CROSS BAND` | Ana VFO'dan gönder, diğerinden al |
| `MAIN TX DUAL RX` | İkisini dinle, her zaman ana VFO'dan gönder |
| `FULL RX RESPOND` | A, B ve 2 öncelikli kanalı (`PriCh1`, `PriCh2`) dinle, sinyal gelenden cevap ver |
| `MAIN TX FULL RX` | Hepsini dinle, her zaman ana VFO'dan gönder |

## 11. Multiboot ve Multiconfig

- **Multiboot**: Harici flash'ta 1 Main + 4 firmware yuvası. Telsizi `MENU` basılı açın,
  `UP`/`DOWN` ile seçin, `MENU` ile yükleyin, `EXIT` ile çıkın. **Yükleme sırasında kapatmayın.**
- **Multiconfig**: Her yuvanın kendi yapılandırma bankası (kanallar, VFO'lar, listeler, ayarlar).
  `SetCfg` başka bir bankayı yeniden başlatmadan uygular. Durum çubuğunda `CM`, `C1`–`C4`.

## 12. Uygulamalar (Labs)

`F` + `7` → `UP`/`DOWN` → `MENU`. Uygulamalar UV Studio ile yüklenir; her zaman firmware ile
**aynı sürümün** uygulama paketini kullanın.

| Grup | Uygulamalar |
|------|-------------|
| Radyo araçları | Broadcast FM, Fox Hunt, Beacon, Beam, Sig Finder, Spectrum3D, ToneCall |
| APRS | APRS RX, APRS TX, APRS Edit, APRS DIGI, KISS TNC, GeoNav |
| Havacılık / deniz | ACARS RX, AIS RX, ATIS RX, ATIS DSC RX |
| Sondalar / işaretçiler | Sonde RS41, M10, M20, MRZ, EPIRB 406, Scan406 |
| Diğer veri | POCSAG RX, SSTV |
| CW | CW Decode, CW Keyer, CW USB, CW Trainer, CW Mem, CW Mem Edit, CW QSO Auto |
| Araçlar | AF Scope, AF Spectro, Resistor, System Info, Flash Map, QR Map |
| Oyunlar | Breakout, Cube3D, Hell Maze, Minesweeper, Plasma, Rapid Roll, Snake, Sokoban, Space Impact, Tetris |

Her uygulamanın tuşları ve kullanımı: [kilavuz/11 Uygulamalar](kilavuz/11-uygulamalar.md).

> [!CAUTION]
> Gönderim yapan uygulamaları yalnızca belgeyle ve izin verilen frekanslarda kullanın.

## 13. RF Log, Fox Hunt, Beacon, BEAM, AirCopy

- **RF Log**: Bir yan tuşa `RF LOG` işlevi atanınca kayıt etkinleşir; aynı tuş geçmişi açar.
  `UP`/`DOWN` gezin, `MENU` filtre (hepsi/RX/TX), `*` ayrıntı sütunu, iki kez uzun `MENU` sil.
- **Fox Hunt** (FieldOps, Labs): `1` gösterge, `2` ses, `3` + `UP`/`DOWN` zayıflatıcı, `MENU`
  tepe/minimum sıfırla, uzun `F` kilit.
- **Beacon** (FieldOps, Labs): `1` TX penceresi, `2` bekleme, `3` tanımlayıcı (`MOE`…`MO5`, `MO`,
  çağrı işareti), `4` `TONE`/`CARR`.
- **BEAM** (Transfer, Labs): Bir VFO'nun ayarlarını başka bir telsizin ilk boş kanalına gönderir.
  `UP`/`DOWN` TX/RX modu, `MENU` başlat.
- **AirCopy** (Transfer, Labs): İki telsizi `PTT` + `SIDE2` ile açın. `*` ile `AIR COPY` /
  `CABLE COPY`, `UP`/`DOWN` ile banka, `Settings` veya `All`; alıcıda `EXIT`, göndericide `MENU`.
  İki telsiz aynı firmware sürümünde olmalı. `Flash 2M` kalibrasyon sektörünü kopyalamaz.

## 14. UV Studio, K5Viewer ve CHIRP

- **UV Studio**: Firmware yükleme, Multiboot yuvaları, kalibrasyon, açılış logosu, uygulama
  yükleme, **K5Viewer** (ekran yansıtma, ekran görüntüsü, uzaktan tuş) ve RF Log panosu.
- **CHIRP**: Bu firmware için özel sürücü gerekir; her sürümle birlikte
  [Releases](https://github.com/armel/uv-k1-k5v3-firmware-custom/releases) sayfasında yayımlanır.
  CHIRP'te **File → Load Module** ile yükleyin.

## 15. Kaynaktan derleme

Gereksinimler: Docker ve Bash (Linux, macOS, WSL veya Windows'ta Git Bash).

```bash
./compile-firmware.sh Fusion
```

Hazır ayarlar: `Custom`, `Fusion` (varsayılan), `Transfer`, `FieldOps`, `Labs`, `Max`,
`Fusion_`, `Service_`, `All`. Çıktılar `build/<Preset>` dizinine `.elf`, `.bin` ve `.hex` olarak yazılır.
Ek CMake seçenekleri ön ayar adından sonra verilir:

```bash
./compile-firmware.sh Fusion -DENABLE_VOX=OFF
```

## 16. Sık karşılaşılan durumlar

| Durum | Çözüm |
|-------|-------|
| `TX DISABLE` | Frekans `F Lock` bölgesinin dışında |
| Sinyal var, ses yok | `RxCTCS`/`RxDCS`'yi `OFF` yapın |
| Ses bozuk / kısık | `W/N` ayarını karşı tarafa uydurun |
| AM'de parazit, hayalet sinyaller | Alıcı ön katı doyuyor; donanım sınırı. Uzaklaşın, zayıflatıcı kullanın |
| `MENU` çalışmıyor, durum çubuğunda `RO` | Rescue Ops kilidi: `PTT` + `SetKey` tuşuyla açılışta kaldırın |
| Gizli menü öğeleri yok | `PTT` + `SIDE1` ile açılış |
| `F` + `7` uygulama yerine VOX açıyor | Uygulamalar yalnızca Labs sürümünde |
| Uygulama `NOT SUPPORTED` diyor | Firmware ile aynı sürümün uygulama paketini yükleyin |
| Ok tuşları ters | Gizli menüde `SetNav` |

Daha fazlası: [kilavuz/14 Sorun giderme](kilavuz/14-sorun-giderme.md).

---

73!
