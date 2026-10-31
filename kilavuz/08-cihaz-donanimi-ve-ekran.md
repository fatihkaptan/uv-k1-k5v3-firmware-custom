# 8. Cihaz Donanımı, Tuşlar ve Ekran

[← Önceki: Frekans rehberi](07-frekans-rehberi.md) · [İçindekiler](README.md) · [Sonraki: Cihaz kullanımı →](09-cihaz-kullanimi.md)

Bu bölüm UV-K5 V3 ve UV-K1 telsizlerinin içini, tuşlarını, göstergelerini ve F4HWN
firmware'inin ekranında gördüğünüz her simgenin anlamını açıklar. Bilgiler bu deponun
kaynak kodundan derlenmiştir.

## İçindekiler

1. [Firmware sürümleri (edition)](#81-firmware-sürümleri-edition)
2. [Blok şema: telsizin içi](#82-blok-şema-telsizin-içi)
3. [Ana bileşenler](#83-ana-bileşenler)
4. [Bellek: neyin nerede saklandığı](#84-bellek-neyin-nerede-saklandığı)
5. [Güç, pil ve şarj](#85-güç-pil-ve-şarj)
6. [Dış bağlantılar](#86-dış-bağlantılar)
7. [Tuşlar](#87-tuşlar)
8. [LED'ler ve fener](#88-ledler-ve-fener)
9. [Ekranın genel düzeni](#89-ekranın-genel-düzeni)
10. [Durum çubuğu simgeleri](#810-durum-çubuğu-simgeleri)
11. [VFO alanı: frekans satırı ve bilgi satırı](#811-vfo-alanı-frekans-satırı-ve-bilgi-satırı)
12. [Uyarı ve durum mesajları](#812-uyarı-ve-durum-mesajları)
13. [Teknik sınırlar özeti](#813-teknik-sınırlar-özeti)

---

## 8.1 Firmware sürümleri (edition)

F4HWN firmware'i, aynı kaynak koddan farklı özellik kümeleriyle derlenen **sürümler**
hâlinde yayımlanır. Telsizin `SysInf` menüsünde ve Multiboot seçicisinde kurulu sürümün
adı görünür. v6 sürümlerinde yayımlanan sürümler (`archive/` klasörü):

| Sürüm | İçerdiği ek özellikler | Kimler için |
|-------|------------------------|-------------|
| **Fusion** | Temel sürüm: spektrum analizörü, FM radyo, VOX, Full Watch, Multiboot, Multiconfig, RF Log, menü kategorileri, ekran koruyucu, PMR ve GMRS bölge kilitleri | Günlük kullanım |
| **FieldOps** | Fusion + **Rescue Ops** (menü kilidi; saha ekipleri için sadeleştirilmiş kullanım) + yerleşik **Fox Hunt** ve **Beacon** | Saha ekipleri, tilki avı |
| **Transfer** | Fusion + **AirCopy** (kablosuz, kablolu ve `Flash 2M` kopyalama) + **BEAM** | Birden fazla telsizi programlayanlar |
| **Labs** | Fusion + **overlay uygulamaları** (APRS, AIS, ACARS, sondalar, CW, SSTV, Fox Hunt, Beacon, BEAM, oyunlar…) + kablosuz AirCopy + Rescue Ops | Deney yapmak isteyenler |

Depoda ayrıca **Custom** (elle yapılandırılan) ve **Max** (oyunlar dahil, Full Watch
hariç) gibi derleme hazır ayarları da bulunur.

> [!IMPORTANT]
> **`F` + `7` ile açılan uygulama menüsü yalnızca overlay uygulamalarını içeren
> sürümlerde (Labs) vardır.** Uygulama içermeyen sürümlerde `F` + `7` **VOX**'u açıp
> kapatır. Bu dokümanda uygulamalardan söz eden bölümler Labs sürümü içindir.

## 8.2 Blok şema: telsizin içi

```
                             ┌─────────────────────────────┐
  Anten (SMA) ──┬── [TX/RX   │  BK4829  RF alıcı-verici    │
                │   anahtar] │  • PLL sentezleyici         │
                │      │     │  • LNA, karıştırıcı, IF     │
     [Alçak     │      ├────▶│  • FM/AM/SSB demodülatör    │──▶ [Ses yükselteci] ──▶ Hoparlör
      geçiren   │      │     │  • CTCSS/DCS/DTMF kod-çöz   │
      filtre]◀──┘      │     │  • FSK modem, RSSI, AGC     │◀── Mikrofon
        ▲              │     └──────────┬──────────────────┘
        │              │                │ SPI / kontrol
  [PA güç yükselteci]◀─┘                │
   (VHF ve UHF yolu,                    ▼
    ~280 MHz'de ayrılır)   ┌──────────────────────────────┐      ┌──────────────────┐
                           │ PY32F071 mikrodenetleyici    │◀────▶│ PY25Q16 2 MiB    │
  Tuş takımı ─────────────▶│ (Arm Cortex-M0+, 48 MHz)      │ SPI  │ harici flash     │
  PTT, yan tuşlar ────────▶│ • 128 KB flash, 16 KB RAM    │      └──────────────────┘
  Pil ölçümü (ADC) ───────▶│ • ADC, zamanlayıcılar, USB   │──▶ ST7565 128×64 LCD + arka ışık
  USB-C ◀─────────────────▶│                              │──▶ LED'ler, fener
  K tipi jak (UART) ◀─────▶│                              │◀─▶ BK1080 FM yayın alıcısı
                           └──────────────────────────────┘
```

## 8.3 Ana bileşenler

| Bileşen | Görevi | Firmware'deki karşılığı |
|---------|--------|--------------------------|
| **BK4829** (Beken) | Tek yongalı RF alıcı-verici: frekans sentezi, alım, demodülasyon, modülasyon, ton kodlama/çözme, RSSI ölçümü, FSK veri modemi | `App/driver/bk4829.c`, `bk4819.c` (uyumlu sürücü) |
| **PY32F071** (Puya) | Telsizi yöneten mikrodenetleyici: Arm Cortex-M0+, 48 MHz, 128 KB flash, 16 KB RAM | `Core/` |
| **PY25Q16** | 2 MiB (16 Mbit) SPI flash: ayarlar, kanallar, uygulamalar, Multiboot yuvaları, RF Log | `App/driver/py25q16.c` |
| **BK1080** | Ayrı FM yayın radyosu alıcısı | `App/driver/bk1080.c` |
| **ST7565** | 128 × 64 piksel tek renkli LCD sürücüsü | `App/driver/st7565.c` |
| **Güç yükselteci (PA)** | Vericinin ~5 W'lık son katı. VHF ve UHF için ayrı yollar vardır. | Güç seviyeleri `Power` menüsünde |
| **Alçak geçiren filtreler** | Verici harmoniklerini bastırır | Donanım |
| **Ses yükselteci + hoparlör** | Alınan sesi çalar | `SetVol`, `SetRxA` |
| **Kristal osilatör** | Bütün frekansların referansı | `FrCali` (gizli menü) |

**Mikrodenetleyicinin belleği** (`Core/py32f071xb.ld`):

- İlk **10 KB** önyükleyiciye (bootloader) ayrılmıştır. Firmware'i USB/kablo üzerinden
  yazan program budur; F4HWN firmware'i onu değiştirmez.
- Kalan **118 KB** firmware'in kendisidir.
- **16 KB RAM**'in 4 KiB'lık bir bölümü overlay uygulamalarının çalıştığı alandır.
  Bu yüzden her uygulama 4 KiB'a sığacak şekilde yazılmıştır.

## 8.4 Bellek: neyin nerede saklandığı

| Bilgi | Kapasite / sınır | Nerede |
|-------|------------------|--------|
| Hafıza kanalları | **1024 kanal**, her biri 10 karakterlik adla | Harici flash |
| Tarama listeleri | 24 adlandırılmış liste + `ALL` + `MIX` | Harici flash |
| Tarama hariç tutmaları | 64 frekans | Harici flash |
| FM radyo kanalları | 48 | Harici flash |
| Overlay uygulamaları | 64 yuva (Labs) | Harici flash |
| Multiboot | 1 Main + 4 kullanıcı firmware yuvası | Harici flash |
| Multiconfig | 5 yapılandırma bankası (`CFG M`, `CFG 1`–`CFG 4`) | Harici flash |
| RF Log kayıtları | Harici flash'ın ayrılmış bölümü | Harici flash |
| Açılış logosu | 1024 bayt (128 × 64 piksel) | Harici flash |
| **Kalibrasyon verisi** | Cihaza özel | Harici flash'ın korunan sektörü |

> [!CAUTION]
> **Kalibrasyon verisi her telsize özeldir** (güç seviyeleri, RSSI düzeltmesi, pil
> ölçümü vb.). Kaybolursa telsiz yanlış güçte gönderebilir, S-metre ve pil göstergesi
> yanlış çalışır. Firmware'i yükledikten hemen sonra **UV Studio ile yedekleyin**.
> AirCopy'nin `Flash 2M` kablo kopyası bile bu sektörü kopyalamaz.

## 8.5 Güç, pil ve şarj

- **Pil**: 2 hücreli seri Li-ion (2S), nominal 7,4 V, tam dolu ~8,3–8,4 V.
- **Pil tipleri** (`BatTyp`): `1600mAh K5`, `2200mAh K5`, `3500mAh K5`, `1400mAh K1`,
  `2500mAh K1`. Gerilim–yüzde tabloları için bkz. [1.17](01-elektrik-ve-elektronik.md#117-piller-li-ion-temelleri-ve-telsizin-pili).
- **Şarj**: Masaüstü şarj tabanı veya **USB-C**. USB-C ile şarj sırasında durum çubuğunda
  USB fiş simgesi görünür.
- **Koruma eşikleri** (firmware):
  - Gerilim 8,90 V'u aşarsa: `VOLT HIGH`, gönderim engellenir.
  - Gerilim, pil tipine göre ~6,0–6,3 V'un altına inerse: `LOW BATTERY`, `BAT LOW`,
    gönderim engellenir.
- **Tüketimi azaltmak için**: `BatSav` (pil tasarrufu), kısa `BLTime` (arka ışık süresi),
  düşük `Power`, `SetOff` (otomatik derin uyku).

## 8.6 Dış bağlantılar

| Bağlantı | Görevi |
|----------|--------|
| **Anten konnektörü (SMA)** | Anten. Tipini kontrol etmeden adaptör almayın (bkz. [5.8](05-antenler-ve-yayilim.md#58-konnektörler)). |
| **USB-C** | Şarj ve **USB seri veri bağlantısı**: UV Studio, K5Viewer, KISS TNC, CW USB, firmware yükleme |
| **K tipi (Kenwood) çift jak** | Harici hoparlör/mikrofon ve **seri programlama kablosu** (UART) |
| **Ses / güç düğmesi** | Telsizi açar/kapatır, ses seviyesini ayarlar |

## 8.7 Tuşlar

### Ön panel (UV-K5 V3 düzeni)

```
 ┌───────────────────────────┐
 │        [ EKRAN ]          │
 ├───────────────────────────┤
 │  MENU    ▲ UP    ▼ DOWN   EXIT │
 │   1        2        3      │
 │  BAND     A/B    VFO/MR    │
 │   4        5        6      │
 │   FC      NOAA    H/M/L    │
 │   7        8        9      │
 │   VOX      R       CALL    │
 │   *        0        #      │
 │  SCAN      FM      F 🔒    │
 └───────────────────────────┘
   Yan: PTT · SIDE1 (üst) · SIDE2 (alt)
```

Tuşların altındaki küçük yazılar, **`F` ile birlikte basıldığında** (veya bazılarında
uzun basıldığında) yapılan işi gösterir. F4HWN bazılarını değiştirmiştir:

| Tuş | Fabrika etiketi | F4HWN'de `F` + tuş | Uzun basış |
|-----|-----------------|---------------------|------------|
| `1` | BAND | Bant değiştir (kanal modunda: kanalı VFO'ya kopyala) | Aynı |
| `2` | A/B | VFO A ↔ VFO B | Aynı |
| `3` | VFO/MR | VFO ↔ kanal modu | Aynı |
| `4` | FC | Frekans yakalama tarayıcısı | Aynı |
| `5` | NOAA | **Spektrum analizörü** | **Kanalın tarama listesini değiştir** |
| `6` | H/M/L | Güç seviyesini değiştir | Aynı |
| `7` | VOX | **Uygulama menüsü** (Labs); diğer sürümlerde VOX | **VOX** |
| `8` | R | **Arka ışığı min/maks arasında geçici değiştir** | **Ters frekans (reverse)** |
| `9` | CALL | **Ayarlı arka ışık davranışına dön** | **1 Call kanalına git** |
| `0` | FM | FM yayın radyosu | Aynı |
| `*` | SCAN | **CTCSS/DCS ton taraması** | Tarama başlat/durdur |
| `#` | F 🔒 | — | Tuş kilidi |

**UV-K1**: Tuş düzeni farklıdır; yön tuşları **sol/sağ** biçimindedir. Gezinme yönünün
doğru çalışması için `SetNav` menüsünde `LEFT/RIGHT UV-K1` seçin.

### Yan tuşlar

| Tuş | Varsayılan kısa basış | Varsayılan uzun basış | Menü |
|-----|-----------------------|------------------------|------|
| **PTT** | Gönderim | — | `SetPTT` (`CLASSIC` / `ONEPUSH`) |
| **SIDE1** (üst) | `MONITOR` | Yok | `F1Shrt`, `F1Long` |
| **SIDE2** (alt) | `SCAN` | Yok | `F2Shrt`, `F2Long` |
| **MENU** (uzun) | — | Yok | `M Long` |

Atanabilecek işlevlerin tam listesi [10. bölümde](10-menu-referansi.md#105-tuşlar-keys).

## 8.8 LED'ler ve fener

| Gösterge | Anlamı |
|----------|--------|
| **Yeşil LED** | Alım (squelch açık). `SetEOT` = `VISUAL` veya `ALL` ise karşı tarafın yayını bittiğinde birkaç kez yanıp söner. Bazı uygulamalarda yeni veri geldiğinde iki kez yanıp söner. |
| **Kırmızı LED** | Gönderim |
| **Fener (üstteki beyaz LED)** | `FLASHLIGHT` işlevi atanmış bir tuşla: kapalı → açık → yanıp sönme → SOS |

## 8.9 Ekranın genel düzeni

Ekran 128 × 64 pikseldir ve satırlara bölünür:

```
 ┌────────────────────────────────────────────────┐
 │ CM S  DWR VX OP        🔒  F   🔇 💡  ▮▮▮ 85%  │ ← Durum çubuğu
 ├────────────────────────────────────────────────┤
 │ ▶ 0001 ROLE IST                                │ ← VFO A: kanal no / ad
 │   145.650  ₀₀                       S9 ▮▮▮▮▮   │ ← VFO A: frekans + S-metre
 │ FM H CT - W SQL3                      ALL      │ ← VFO A: bilgi satırı
 │                                                │
 │ ▷ VFO                                          │ ← VFO B
 │   433.500  ₀₀                                  │
 │ FM L       W                                   │
 └────────────────────────────────────────────────┘
   (Görünüm `SetGUI`, `SetMet`, `ChDisp` ve `RxMode` ayarlarına göre değişir.)
```

- **Dolu üçgen (▶)**: Etkin (ana) VFO. `PTT`'ye basınca bu VFO'dan gönderilir.
- **Boş üçgen (▷)**: Diğer VFO.
- `MAIN ONLY` ekran modunda yalnızca ana VFO, daha büyük olarak gösterilir.

## 8.10 Durum çubuğu simgeleri

Soldan sağa yaklaşık sırayla:

| Simge | Anlamı |
|-------|--------|
| `CM`, `C1`–`C4` | Etkin **Multiconfig bankası** (`CFG M` = Main, `CFG 1`–`4`) |
| `PS` | Pil tasarruf modu etkin (Multiconfig göstergesi olmayan derlemelerde) |
| `mm:ss` | RX/TX süre sayacı (`SetTmr` açıksa, alım veya gönderim sırasında) |
| `S` | Frekans (VFO) taraması sürüyor |
| `ALL`, `MIX`, `01`–`24`, liste adı (ters renkli) | Kanal taraması sürüyor ve taranan liste. Sonunda `+` varsa öncelikli kanal taraması (`ScPri`) açık. |
| `DWR` | Çift dinleme (Dual Watch) etkin |
| `FWR` | **Full Watch** etkin (A, B ve öncelikli kanallar) |
| `XB` | Çapraz bant (Cross Band) |
| `MO` | Yalnızca ana VFO (`MAIN ONLY`) |
| `><` (çarpı) | Çift dinleme geçici olarak beklemede (ör. alım veya gönderim sırasında) |
| `RO` | **Rescue Ops** menü kilidi açık (FieldOps / Labs) |
| `VX` | VOX açık |
| `CL` / `OP` | PTT modu: **Classic** / **OnePush** |
| Asma kilit | Tuş takımı kilitli |
| Kutulu `F` | `F` tuşuna basıldı, ikinci tuş bekleniyor |
| Üstü çizili hoparlör | Ses kapatıldı (`MUTE`) |
| Ampul (dolu / boş) | Arka ışık elle ayarlandı (`F` + `8`): dolu = sürekli açık, boş = kapalı |
| USB fiş | USB-C ile şarj oluyor |
| Pil çubuğu, `%` veya `V` | Pil durumu (`BatTxt`: yüzde, voltaj veya yok) |
| `MENU` / kategori adı | Menüdeyken: kategori ekranında `MENU`, kategorinin içinde kategori adı |

## 8.11 VFO alanı: frekans satırı ve bilgi satırı

### Üst satır: kanal ve tarama bilgisi

| Gösterim | Anlamı |
|----------|--------|
| `0001`–`1024` | Kanal numarası (kanal modunda) |
| Kanal adı | `ChDisp` ayarına göre |
| `VFO` veya `F1`…`F7` | VFO modunda bant numarası |
| `ALL`, `OFF`, `01`–`24`, liste adı (sağda) | Kanalın atandığı tarama listesi |
| `EX` | Kanal taramadan **hariç tutulmuş** |
| `P1`, `P2` | Full Watch'ta gösterilen öncelikli kanal |
| `TRIPLE WATCH` / `QUAD WATCH` | Full Watch'un izlediği kanal sayısı |
| `>>` | **Son alımın** yapıldığı VFO (diğer VFO'dayken) |

### Frekans ve sinyal

- **Büyük rakamlar**: MHz ve kHz. **Küçük rakamlar**: 10 Hz basamakları.
- **`RX`**, **`TX`** etiketleri: o VFO'da alım veya gönderim yapılıyor. Alım sırasında
  `RX` yerine etkin **ses profilinin adı** görünebilir: FM'de `FLAT`, `CLEAN`, `MID`,
  `BOOST`, `MAX`; AM'de `SHARP`, `STOCK`, `OPEN`; ya da `USB`.
- **S-metre**: Çubuklar, `S1`–`S9`, `+10`–`+40` ve dBm (bkz. [3.6](03-desibel-ve-sinyal-olcumu.md#36-s-metre-ve-rssi)).
  Gönderim sırasında aynı alan **çıkış gücü seviyesini** gösterir.

### Alt bilgi satırı

| Gösterim | Anlamı |
|----------|--------|
| `FM`, `AM`, `USB` | Modülasyon (`Mode`) |
| `L1`–`L5`, `M`, `H` (TINY) veya `LOW1`…`HIGH` (CLASSIC) | Çıkış gücü. Yanında küçük üçgen varsa `USER` gücü kullanılıyor. |
| `CT` | CTCSS tonu ayarlı |
| `DCS` / `DCR` (TINY'de `DC`) | DCS normal / ters |
| `+`, `-` | Röle kayma yönü (`TxODir`) |
| `R` | Ters frekans (reverse) açık |
| `W`, `N`, `N+` (veya `WIDE`, `NAR`, `NAR+`) | Bant genişliği: geniş, dar, daha dar (`SetNFM` = `NARROWER`) |
| `C` simgesi | Compander açık |
| Asma kilit simgesi (kanal numarasının yanında) | Bu frekans `F Lock` bölgesinin dışında ve kanalın `TXLock`'u açık: **gönderim engelli** |
| `DTMF` | Bu kanalda DTMF çözme açık |
| `SQL0`–`SQL9` | Susturucu seviyesi |
| `MONI` | Monitör açık (susturucu geçici olarak açıldı) |
| `VFO A` / `VFO B` | Bazı ekran modlarında etkin VFO'nun adı |

## 8.12 Uyarı ve durum mesajları

| Mesaj | Anlamı | Ne yapmalı? |
|-------|--------|-------------|
| `BUSY` | Kanal meşgul, gönderime izin verilmedi (`BusyCL` açık) | Kanalın boşalmasını bekleyin |
| `TX DISABLE` | Bu frekansta gönderim yasak (`F Lock`, `TXLock`) | Frekansı ve `F Lock` ayarını kontrol edin |
| `BAT LOW` / `LOW BATTERY` | Pil çok düşük | Şarj edin |
| `VOLT HIGH` | Pil gerilimi çok yüksek (> 8,9 V) | Pili ve şarj cihazını kontrol edin |
| `TIMEOUT` | Gönderim süresi aşıldı (`TxTOut`) | `PTT`'yi bırakın; gerekiyorsa süreyi uzatın |
| `Long press # to unlock` | Tuş takımı kilitli | `F` (`#`) tuşuna uzun basın |
| `SCAN LIST …` | Tarama listesi değişti | — |
| `ScnRng` | Tarama aralığı (scan range) modu | — |
| `BEAM TX`, `BEAM RX`, `SENDING`, `SENT`, `WAITING`, `RECEIVED`, `MEM FULL`, `ERROR` | BEAM kanal aktarımı durumu | — |
| `N/A` | Bu derlemede bulunmayan özellik | — |

## 8.13 Teknik sınırlar özeti

| Özellik | Değer |
|---------|-------|
| Alım | 18–630 MHz ve 840–1300 MHz (bant uçlarında hassasiyet düşük) |
| Gönderim | `F Lock` ayarına göre (Türkiye için `CE HAM`: 144–146, 430–440 MHz) |
| Çıkış gücü | < 20 mW … ≈ 5 W (8 seviye + `USER`) |
| Modülasyon | FM (geniş/dar/daha dar), AM, USB (alım) |
| Kanal | 1024 hafıza kanalı, 2 VFO |
| Tarama | 24 liste + ALL + MIX, ≈ 150 frekans/saniye (hızlı mod) |
| Ekran | 128 × 64 tek renkli LCD |
| MCU | PY32F071, 48 MHz, 128 KB flash, 16 KB RAM |
| Harici flash | 2 MiB |
| Pil | 2S Li-ion, 7,4 V nominal |

---

[← Önceki: Frekans rehberi](07-frekans-rehberi.md) · [İçindekiler](README.md) · [Sonraki: Cihaz kullanımı →](09-cihaz-kullanimi.md)
