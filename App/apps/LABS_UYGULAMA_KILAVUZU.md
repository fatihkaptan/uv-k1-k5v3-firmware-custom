# F4HWN Labs — Overlay uygulaması geliştirme ve yükleme kılavuzu

Bu kılavuz UV-K1 / UV-K5 V3 (PY32F071) için F4HWN **Labs** firmware'inde
"overlay uygulamalarının" nasıl çalıştığını, nasıl derlenip telsize
yüklendiğini ve sıfırdan nasıl yeni bir uygulama yazılacağını anlatır. Örnek
olarak bu depodaki **USB Term** uygulaması (`App/apps/usbterm/`) ve PC tarafı
**uvterm** (`tools/uvterm/`) kullanılır.

Bilgiler deponun kaynak kodundan alınmıştır; asıl referans dosyalar:
`App/apps/app_api.h` (servis tablosu), `App/apps/app_overlay.h` (slot ve
başlık biçimi), `App/apps/pack_app.py` (paketleyici), `compile-app.sh`.

İçindekiler

1. [Labs ve overlay uygulamaları nedir?](#1-labs-ve-overlay-uygulamaları-nedir)
2. [Hazırlık: Labs firmware'ini telsize yüklemek](#2-hazırlık-labs-firmwareini-telsize-yüklemek)
3. [Uygulamaları derlemek](#3-uygulamaları-derlemek)
4. [Uygulamayı telsize yüklemek](#4-uygulamayı-telsize-yüklemek)
5. [Uygulamayı çalıştırmak](#5-uygulamayı-çalıştırmak)
6. [Kendi uygulamanızı yazmak (adım adım)](#6-kendi-uygulamanızı-yazmak-adım-adım)
7. [Altın kurallar](#7-altın-kurallar)
8. [API'nin özeti](#8-apinin-özeti)
9. [USB seri port ile çalışmak](#9-usb-seri-port-ile-çalışmak)
10. [Bilgisayarda test etmek](#10-bilgisayarda-test-etmek)
11. [Sorun giderme](#11-sorun-giderme)

---

## 1. Labs ve overlay uygulamaları nedir?

F4HWN firmware'i birkaç "sürüm" (edition) halinde derlenir (`CMakePresets.json`).
Overlay uygulama altyapısı (`ENABLE_FEAT_F4HWN_OVERLAY_APPS`) sadece **Labs**
sürümünde (ve geliştirici ön ayarı `Fusion_`'da) açıktır. Fusion, Transfer,
FieldOps ve Max sürümlerinde Apps menüsü yoktur.

Bir overlay uygulaması, telsizin dahili 118 KiB'lık program belleğine değil,
**harici SPI flash'a** (PY25Q16, 2 MiB) kaydedilen bağımsız bir kod parçasıdır
(`.app` dosyası). Çalıştırılacağı zaman:

1. Yükleyici (loader) slotun başlığını okur: sihirli sayı `FAP1`, ABI/API
   seviyesi, gereken yetenekler (capability), boyutlar.
2. Kodu **4 KiB'lık RAM overlay alanına** kopyalar (harici flash'ın sektör
   önbelleği olarak kullanılan RAM bölgesi, adres `0x20000280`), CRC-32'sini
   kontrol eder, `.bss` alanını sıfırlar.
3. Kodun 0. baytındaki giriş noktasını çağırır:
   `void app_main(const app_api_t *api);`
4. Uygulama `app_main`'den dönünce kaydedilmesi istenen ayarları flash'a
   yazar ve Apps menüsüne (ya da ana ekrana) döner.

Uygulama firmware'in hiçbir sembolüne doğrudan erişmez (bağlayıcı
`NOCROSSREFS` ile ayrılır): ekran, tuşlar, ses, BK4819 radyo çipi, USB seri
port gibi tüm servislere `api` işaretçisiyle gelen **`app_api_t` tablosu**
üzerinden ulaşır. Bu sayede aynı `.app` dosyası farklı derlemelerde çalışır.

### Harici flash'taki yerleşim

```text
0x102000  slot 0   ┐  48 slot × 8 KiB = 384 KiB
0x104000  slot 1   │  her slot:
   ...             │
0x160000  slot 47  ┘

slot + 0x000   app_header_t (64 B): FAP1, sürüm, boyutlar, CRC, ad, VMA, yetenekler
slot + 0x040   uygulamanın ayarları (en fazla 16 B, cfg_save ile)
slot + 0x050   ayarların sahibi olan uygulamanın adı (16 B)
slot + 0x100   salt okunur varlıklar / assets (en fazla 3840 B, asset_read ile)
slot + 0x1000  kod (en fazla 4096 B: kod + sabitler + .data + .bss)
```

`.app` dosyası ise sırasıyla: 64 baytlık başlık + kod + varlıklar.

### Sürümler ve uyumluluk

- **ABI ana sürümü** (`APP_ABI_MAJOR = 1`) ve **API seviyesi**
  (`APP_API_LEVEL`): tablo sadece sona eklenerek büyür. Seviye 1 = v6.0.0,
  seviye 2 = zaman/rastgele/varlık/bölme servisleri, seviye 3 = sayı
  biçimleme, ses yakalama, hand-off, **USB seri port** (`serial_*`), sayfa
  bazlı ekran servisleri, `vfo_stage`.
- Uygulama başlığında `api_min` yazar; firmware daha düşük seviyedeyse menü
  `UPDATE FIRMWARE` der.
- **Yetenekler** (`required_caps`): `fm`, `sysinfo`, `beam2`, `cfgproxy`,
  `serial`. Firmware'de olmayan bir yetenek isteyen uygulama `NOT SUPPORTED`
  ile reddedilir.
- Kod sabit bir RAM adresine (VMA `0x20000280`) bağlanır; farklı VMA'lı
  firmware `UPDATE APP` der.

> [!WARNING]
> Overlay uygulaması bir güvenlik kum havuzu (sandbox) **değildir**: çalışan
> uygulama tam yetkili yerel koddur. Hatalı bir uygulama telsizi kilitleyip
> watchdog ile yeniden başlatabilir. Yalnızca güvendiğiniz uygulamaları
> yükleyin. Uygulamalar dahili firmware'e dokunmaz; bozuk bir slot sadece
> açılışta reddedilir.

---

## 2. Hazırlık: Labs firmware'ini telsize yüklemek

1. **Kalibrasyonu yedekleyin.** [UV Studio](https://armel.github.io/uvstudio/)
   → *Dump Calibration*, telsiz normal modda. Dosyayı telsizin seri
   numarasıyla adlandırıp saklayın.
2. **Labs firmware dosyası:**
   - Hazır: `archive/f4hwn.labs.v6.3.0.bin` (bu depodaki en yeni Labs sürümü), ya da
   - Derleyin: `./compile-firmware.sh Labs` → `build/Labs/f4hwn.labs.bin`.
3. **Yükleyin:** UV Studio → *Flash Firmware*, telsiz **DFU (flash) modunda**
   (çoğu Quansheng modelinde telsiz kapalıyken PTT basılı tutularak açılır),
   *Flash Firmware* → seri portu seçin. Bitince telsiz yeniden başlar.
4. Kontrol: telsizde **F + 7** "F4HWN APPS" menüsünü açmalıdır. Açmıyorsa
   Labs dışında bir sürüm yüklüdür.

> [!CAUTION]
> Yayın yapan uygulamaları yalnızca lisansınızın ve yerel mevzuatın izin
> verdiği frekans, güç ve modlarda kullanın. (USB Term hiç yayın yapmaz.)

---

## 3. Uygulamaları derlemek

### Docker ile (önerilen, ortam kurmadan)

Depo kökünde:

```bash
./compile-app.sh
```

```bash
./compile-app.sh usbterm
```

```bash
./compile-app.sh usbterm kisstnc resistor
```

- Argümansız / `All`: test uygulamaları hariç hepsi.
- Betik `App/apps/*/build.sh` içeren her dizini uygulama sayar.
- Çıktılar `build/Apps/<Ad>.app` (ad, başlıktaki etiketin boşluksuz hali:
  "USB Term" → `USBTerm.app`).
- Sonda her uygulamanın 4 KiB bütçesinin ne kadarını kullandığını gösteren
  bir tablo basılır; taşan uygulama `OVERFLOW` olarak işaretlenir.

İlk çalıştırmada `uvk1-uvk5v3` Docker imajı (ARM GCC 13.3) oluşturulur.

### Docker'sız (yerel ARM derleyicisi ile)

`arm-none-eabi-gcc` ve Python 3 yeterli:

- Debian/Ubuntu: `sudo apt install gcc-arm-none-eabi` (bazı sürümlerde
  `binutils-arm-none-eabi` ve `libnewlib-arm-none-eabi` paketleri de gerekir)
- macOS: `brew install --cask gcc-arm-embedded`
- Windows: Arm GNU Toolchain kurulum dosyası ya da WSL içinde Ubuntu paketi.

```bash
cd App/apps/usbterm && ./build.sh
```

Çıktı uygulama dizininde oluşur (`App/apps/usbterm/USBTerm.app`). Ara dosyalar
(`*.elf`, `*.bin`, `*.map`, `*_assets.h`) `.gitignore` ile dışarıda tutulur.

### Hazır uygulamalar

Resmî sürümlerin `.app` dosyaları `archive/apps/v6.x.x/` altındadır.
**Telsizdeki firmware ile aynı sürümün klasörünü** kullanın; eski bir
firmware yeni bir uygulamayı API seviyesi yüzünden reddedebilir.

---

## 4. Uygulamayı telsize yüklemek

Yükleme yalnızca harici flash'ın Apps bölgesine yazar; firmware'e ve
kalibrasyona dokunmaz. Telsiz **normal modda** (DFU değil) olmalı; ana ekranda
ya da Apps menüsünde durmalıdır. Açık bir uygulama varsa önce `EXIT` ile
kapatın (uygulama çalışırken firmware'in komut ayrıştırıcısı çalışmaz).

### Yol A — UV Studio

[UV Studio](https://armel.github.io/uvstudio/)'yu Web Serial destekleyen bir
masaüstü tarayıcıda (Chrome, Edge, Brave, Opera, Firefox 151+) açın, telsizi
bağlayın ve uygulama (Apps) yönetiminden `.app` dosyasını boş bir slota
yükleyin. (Arayüzdeki adlar UV Studio sürümüne göre değişebilir.)

### Yol B — Terminalden `uvterm.py`

```bash
pip install pyserial
```

```bash
python3 tools/uvterm/uvterm.py install build/Apps/USBTerm.app
```

```bash
python3 tools/uvterm/uvterm.py apps
```

- Aynı adlı uygulama zaten yüklüyse **onun slotu kullanılır** (güncelleme;
  uygulamanın kayıtlı ayarları korunur), yoksa ilk boş slot.
- `--slot N` ile slot seçilebilir; başka bir uygulamanın üzerine yazmadan
  önce onay sorar (`-y` sormaz).
- Port otomatik bulunur (USB VID:PID `36B7:FFFF`); gerekirse `-p COM5` /
  `-p /dev/ttyACM0`.

> [!NOTE]
> `uvterm.py install`, firmware kaynağındaki protokole (`App/app/uart.c`)
> göre yazıldı ve bu protokolü bayt bayt taklit eden bir simülatörde test
> edildi (`tools/uvterm/test_uvterm.py`), ancak henüz gerçek bir telsizde
> denenmedi. Sorun yaşarsanız UV Studio'yu kullanın.

### Yükleme protokolü (meraklısına)

Firmware'in seri komut ayrıştırıcısı (USB CDC portu) şu çerçeveyi kullanır:

```text
AB CD | uzunluk (2 B, LE) | XOR-gizlenmiş [ ID (2) | boyut (2) | veri | CRC-16/XMODEM (2) ] | DC BA
```

Gizleme (obfuscation) 16 baytlık sabit bir anahtarla XOR'dur (`uart.c`
içindeki `Obfuscation[]`). Bir paket en fazla 256 bayt olabilir.

| Komut | Yanıt | Veri |
|---|---|---|
| `0x0514` merhaba | `0x0515` | 4 B zaman damgası → firmware sürüm dizesi; bu damga sonraki yazma/silme komutlarında tekrar gönderilmeli |
| `0x0730` slot bilgisi | `0x0731` | `slot` → durum + 64 B başlık |
| `0x0732` slot sil | `0x0733` | `slot, 0, damga` → 8 KiB silinir, ayarlar korunur |
| `0x0734` slota yaz | `0x0735` | `slot, 0, ofset(4), uzunluk(2), damga(4), baytlar` |
| `0x0736` doğrula | `0x0737` | `slot` → başlık geçerli mi (`0` = OK) |

`uvterm.py` sırası: merhaba → sil → varlıkları `+0x100`'e → kodu `+0x1000`'e
→ **en son** başlığı `+0x000`'a (yarıda kesilen bir yükleme geçersiz kalsın
diye) → doğrula.

---

## 5. Uygulamayı çalıştırmak

1. Ana ekranda **F + 7** → "F4HWN APPS" menüsü.
2. `UP` / `DOWN` ile uygulamayı seçin. `*` sağ sütunda kod boyutu yerine
   sürümü gösterir.
3. `MENU` = **RUN** (çalıştır), `EXIT` = menüden çık.
4. Uygulamadan çıkış genelde `EXIT` iledir (uygulamaya göre değişir).

Bazı uygulamalar bir kısayol (shortcut) bildirir (FM, Fox Hunt, Beacon, BEAM,
ToneCall): o zaman menüdeki `F1Shrt`, `F1Long`, `F2Shrt`, `F2Long`, `M Long`
tuş atamalarından doğrudan açılabilir.

Açılış hata mesajları:

| Ekranda | Anlamı | Çözüm |
|---|---|---|
| `UPDATE FIRMWARE` | Uygulama daha yüksek bir API seviyesi istiyor | Firmware'i güncelleyin |
| `UPDATE APP` | Eski biçim, yanlış VMA ya da geçersiz boyut | Uygulamayı bu firmware'in sürümünden yeniden derleyin / indirin |
| `NOT SUPPORTED` | Gereken yetenek (ör. `serial`) bu derlemede yok | Labs firmware kullanın |
| `REINSTALL APP` | CRC hatası ya da yarım kalmış yükleme | Uygulamayı yeniden yükleyin |
| `NO APP` | Slot boş | — |

---

## 6. Kendi uygulamanızı yazmak (adım adım)

### 6.1 Dizin

En kolayı mevcut bir uygulamayı kopyalamak. Seri port kullanacaksanız
`usbterm`, basit bir ekran/tuş uygulaması için `resistor` iyi şablonlardır.

```text
App/apps/merhaba/
├── build.sh          # derleme betiği (compile-app.sh bunu çağırır)
├── app.ld            # bağlayıcı betiği: 4 KiB overlay, app_main en başta
├── gen_assets.py     # (isteğe bağlı) metinler/tablolar -> varlık blob'u + .h
└── merhaba_app.c     # kaynak: dosya adı <dizin>_app.c olmalı
```

```bash
cp -r App/apps/usbterm App/apps/merhaba
```

```bash
cd App/apps/merhaba && rm -rf test images prebuilt README.md && mv usbterm_app.c merhaba_app.c
```

`build.sh` içinde `APP_NAME` (menüde görünen ad, en fazla 15 karakter),
`APP_VER`, `APP_API_MIN` ve `pack_app.py` seçeneklerini düzenleyin;
`app.ld` içindeki hata mesajında uygulama adını değiştirin.

### 6.2 En küçük uygulama

```c
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "../app_api.h"

/* C kütüphanesi yok: GCC'nin kendiliğinden çağırabileceği iki fonksiyon. */
void *memset(void *d, int c, size_t n) { uint8_t *p = d; while (n) p[--n] = (uint8_t)c; return d; }
void *memcpy(void *d, const void *s, size_t n) {
    uint8_t *p = d; const uint8_t *q = s; while (n) { --n; p[n] = q[n]; } return d;
}

static char *put(char *o, const char *s) { while (*s) *o++ = *s++; return o; }

__attribute__((section(".text.entry"), used))
void app_main(const app_api_t *api)
{
    uint8_t prev = APP_KEY_INVALID;
    uint32_t n = 0;

    api->backlight_on();
    for (;;) {
        uint8_t key = api->get_key();            /* basılı tuş, yoksa APP_KEY_INVALID */
        if (key != prev && key == APP_KEY_EXIT)  /* basma anı (kenar) */
            break;
        if (key != prev && key == APP_KEY_MENU) {
            n++;
            api->play_tone(1000, 50);
        }
        prev = key;

        char s[16];
        *api->append_u32(put(s, "Sayac: "), n) = '\0';   /* "Sayac: 3" */
        api->display_clear();
        api->status_clear();
        api->print_inverse("MERHABA", 2, 0, true, true, 30);   /* durum çubuğu */
        api->print_normal("Merhaba telsiz!", 0, 127, 2);      /* ortalanmış   */
        api->print_normal(s, 0, 127, 4);
        api->print_tiny("MENU say  EXIT cik", 0, 50, false, true);
        api->blit_status();
        api->blit_full();

        api->backlight_update();   /* ekran ışığı zaman aşımı + kararma */
        api->delay_ms(20);
    }
}
```

`build.sh` için en az şunlar gerekir (varlık yoksa `gen_assets` adımını ve
`--assets` seçeneğini çıkarın):

```bash
CFLAGS="-mcpu=cortex-m0plus -mthumb -Os -std=gnu11 -ffreestanding -fno-builtin \
  -fno-common -ffunction-sections -fdata-sections -Wall -Wextra"
LDFLAGS="-nostdlib -nostartfiles -T app.ld -Wl,--defsym,APP_VMA=0x20000280 -Wl,--gc-sections"
arm-none-eabi-gcc $CFLAGS $LDFLAGS merhaba_app.c -lgcc -o merhaba.elf
arm-none-eabi-objcopy -O binary merhaba.elf merhaba.bin
python3 ../pack_app.py merhaba.bin Merhaba.app --name "Merhaba" --ver 1.0 \
  --api-min 3 --vma 0x20000280
```

### 6.3 `pack_app.py` seçenekleri

| Seçenek | Anlamı |
|---|---|
| `--name "USB Term"` | Menüde görünen ad (≤ 15 karakter). Ayarlar bu ada bağlıdır. |
| `--ver 1.0` | Sürüm dizesi (menüde `*` ile görünür) |
| `--api-min N` | Gereken en düşük API seviyesi (varlık kullanan ≥ 2, seri port ≥ 3) |
| `--vma 0x20000280` | Bağlanılan RAM adresi (firmware ile aynı olmalı) |
| `--require serial` | Gereken yetenek; tekrarlanabilir: `fm`, `sysinfo`, `beam2`, `cfgproxy`, `serial` |
| `--assets dosya.bin` | Salt okunur varlıklar (≤ 3840 B), `asset_read` ile okunur |
| `--screensaver` | Uygulama boşta iken firmware'in ekran koruyucusuna izin ver |
| `--exit-main` | Çıkınca Apps menüsü yerine ana ekrana dön |
| `--shortcut fm\|foxhunt\|beacon\|beam\|tonecall` | Kısayol tuşu atanabilir uygulama |
| `--save-screen` | Çıkıştaki ekranı varlıkların son 1024 baytına sakla |

### 6.4 Varlıklar (assets) ile metinleri koddan çıkarmak

4 KiB'ın her baytı değerlidir. Metinleri ve tabloları `gen_assets.py` ile
varlık dosyasına koyun; derleme sırasında bir C başlığı (`<ad>_assets.h`)
üretilir:

```python
from app_assets import Assets
a = Assets("MERHABA")
a.text("T_TITLE", "MERHABA")                 # NUL ile biten metin
a.table("T_MODES", ["abc", "ABC", "123"])    # sabit adımlı tablo (+ T_MODES_STRIDE)
a.u16("TABLO", [1, 2, 3])                    # ham veri
a.main()                                     # argv: <çıktı.bin> <çıktı.h>
```

```c
char t[TEXT_MAX];
api->asset_read(T_TITLE, t, TEXT_MAX);                      /* metni oku */
api->asset_read(T_MODES + mode * T_MODES_STRIDE, t, T_MODES_STRIDE);
```

---

## 7. Altın kurallar

1. **4 KiB sınırı:** kod + sabitler + `.data` + `.bss` toplamı 4096 baytı
   geçemez (bağlayıcı `ASSERT` ile durur). Büyük tamponları `app_main`
   içinde **yerel değişken** yapın (yığında durur, overlay'den yemez):
   USB Term 1 KiB'lık geçmişi böyle tutar. Metinleri varlıklara taşıyın.
2. **Firmware sembolü yok:** `printf`, `strlen`, `memcpy`… bağlanmaz.
   GCC'nin kendiliğinden çağırdığı `memset`/`memcpy`'yi kendiniz tanımlayın
   (bkz. `usbterm_app.c`). Sayı yazdırmak için `api->append_u32` /
   `append_i32`.
3. **Bölme:** Cortex-M0+'da bölme komutu yoktur. `/` ve `%` kullanacaksanız
   `__aeabi_uidivmod` / `__aeabi_idivmod`'u `api->uidivmod` / `idivmod`'a
   yönlendirin (bkz. `afscope_app.c`), ya da doğrudan
   `api->uidivmod(n, d)` çağırın (bölüm alt 32 bit, kalan üst 32 bit).
   2'nin kuvvetleri için maske/kaydırma kullanın.
4. **Giriş noktası:** `app_main` `__attribute__((section(".text.entry")))`
   ile kodun 0. baytına konmalıdır.
5. **Çalışırken flash'a yazmak yasak:** overlay RAM'i aynı zamanda harici
   flash'ın sektör önbelleğidir. `cfg_save` (en fazla 16 B) yalnızca
   "sahneler"; asıl yazma uygulama döndükten sonra yapılır. Telsiz uygulama
   içindeyken kapatılırsa o oturumun değişiklikleri kaybolur.
6. **Tuşlar:** `get_key()` o anda basılı tuşu verir (olay değil). Basma
   anını önceki değerle karşılaştırarak bulun; gerekirse iki okuma ile
   sıçrama (debounce) filtresi uygulayın; uzun basışı `ticks_ms()` ile ölçün.
   `--screensaver` ile paketlenen uygulamada `APP_KEY_SAVER` (ekran koruyucu
   açık: çizme) ve `APP_KEY_WAKE` (uyandı: sadece yeniden çiz) gelir.
7. **Döngüde düzenli olarak** `backlight_update()` çağırın; durum çubuğunda
   pil gösteriyorsanız arada `battery_sample()` + `draw_battery()`.
8. **Zaman:** `ticks_ms()` 10 ms çözünürlüklüdür, işaretsiz çıkarma ile
   karşılaştırın: `(api->ticks_ms() - t0) >= süre`. Hassas zamanlama için
   `cycles_48mhz()` ve `app_cycles_reached()`.
9. **Uygulama telsiz değildir:** çalışırken normal telsiz döngüsü durur
   (dinleme, tarama, PTT). BK4819'a `bk_read`/`bk_write` ile erişebilirsiniz.
10. **Yayın (TX):** `tx_state()` 0 değilse yayın yapmayın; yasal frekans ve
    güç sınırlarına uyun.

---

## 8. API'nin özeti

Tam liste ve ayrıntılar: `App/apps/app_api.h`.

| Grup | Servisler |
|---|---|
| Ekran | `fb` (7 satır × 128 bayt çerçeve tamponu, her bayt 8 dikey piksel), `status_line`, `display_clear`, `status_clear`, `print_tiny` (3×5 font, 4 px/karakter, 32 sütun), `print_normal` / `print_bold` (6×7, 7 px/karakter, 18 sütun), `print_inverse` (ters kapsül), `print_string` / `display_freq` / `draw_frequency` (büyük rakamlar), `draw_line`, `draw_rect`, `blit_full`, `blit_status`, `blit_line`, `blit_page`, `lcd_feed`, `viewer_update` |
| Giriş / zaman | `get_key`, `nav_dir` (UV-K1/K5 ok tuşu farkı), `delay_ms`, `ticks_ms`, `cycles_48mhz`, `rand32` |
| Ses / gösterge | `play_tone(hz, ms)`, `led`, `audio_path`, `set_af`, `backlight_on`, `backlight_update` |
| Radyo | `rx_freq`, `tx_freq`, `rssi_dbm`, `bk_read`, `bk_write`, `set_agc`, `tx_*` (yayın), `af_capture_*` (RX sesini örnekleme), `vfo_stage` |
| Ayar / veri | `cfg_load`, `cfg_save` (16 B), `asset_read` |
| Sayı / bölme | `append_u32`, `append_i32`, `uidivmod`, `idivmod` |
| Sistem bilgisi (`sysinfo`) | `sys_edition`, `sys_version`, `sys_battery_voltage` (10 mV birimi), `sys_battery_percent`, `sys_stack_free_now/min`… |
| Uygulamalar arası | `handoff`, `handoff_read` (çıkışta başka bir uygulamayı mesajla başlatma) |
| Seri port (`serial`) | `serial_read`, `serial_write`, `serial_ctl` |
| Broadcast FM (`fm`) | `fm_enter`, `fm_exit`, `fm_set_freq`, … |

Ekran düzeni: üstte 8 piksellik durum çubuğu (`status_line`), altında
7 satırlık (56 piksel) çerçeve tamponu. `print_tiny`'nin `y` parametresi
piksel cinsindendir (0–55), `print_normal`'ın `line` parametresi satır
(0–6) cinsindendir.

---

## 9. USB seri port ile çalışmak

API seviyesi 3 ve `--require serial` gerekir (Labs v6.3.0+). Kaynak:
`app_api.h` içindeki `serial_*` açıklaması; örnekler: `usbterm`, `kisstnc`.

- Telsiz USB-C'de bir **USB aygıtıdır** (CDC ACM seri port). Bilgisayar ya
  da OTG ile telefon ana makinedir (host). Baud hızı önemsizdir.
- `serial_*` servislerinden birini ilk çağırdığınız andan uygulama dönene
  kadar firmware'in komut ayrıştırıcısı ve K5Viewer portu bırakır; port
  tamamen uygulamanındır.
- **Alma:** 256 baytlık halka tampon. Bilgisayar hızlı gönderirse tampon
  birkaç milisaniyede dolar: sık okuyun (USB Term her 10 ms'de) ve PC
  tarafında yavaş gönderin. Taşmayı `serial_ctl` `APP_SERIAL_LOST` ile bildirir.
- **Gönderme:** `serial_write` bilgisayar veriyi alana kadar bekler; bilgisayar
  portu açmamışsa (DTR yok) ya da 50 ms içinde almazsa `false` döner ve
  kalan veri atılır. 64 baytlık parçalar halinde yazın.
- **Durum:** `serial_ctl(APP_SERIAL_USB, 0)` →
  `APP_SERIAL_OK` (port var), `APP_SERIAL_HOST` (bir program portu açık),
  olaylar: `APP_SERIAL_LOST`, `APP_SERIAL_TIMEOUT`, `APP_SERIAL_ENUM`
  (USB yeniden tanıtıldı). Bağlantı gelişini `HOST` bitinin yükselmesinden
  anlayın (USB Term o anda karşılama satırını gönderir).
- K-plug (programlama kablosu) portu (`APP_SERIAL_KPLUG`) API'de ayrılmış
  ama henüz uygulanmamıştır.
- Yayın sırasında antenden kabloya binen RF USB bağlantısını sıfırlayabilir
  (KISS TNC README'sine bakın): ferrit, kısa kablo, anteni kablodan uzak tutun.

---

## 10. Bilgisayarda test etmek

Donanıma yüklemeden önce uygulama mantığının çoğu bilgisayarda test
edilebilir: uygulama kaynağını `HOST_TEST` tanımıyla, sahte bir `app_api_t`
dolduran bir C dosyasının içine `#include` edin. Örnek: `App/apps/usbterm/test/`.

- `host_term.c` sahte servisleri sağlar (gerçek 3×5 fontla çizim, simüle
  zaman, betikten tuş basışları ve seri veri) ve bir betik dili çalıştırır.
- `test_term.py` derler, senaryoları çalıştırır, ekranı PNG olarak çizer;
  ayrıca uygulamayı canlı modda bir sanal seri porta (pty) bağlayıp
  `uvterm.py` ile uçtan uca konuşturur.
- 64 bit bilgisayarda işaretçiler 8 bayt olduğundan `app_api.h` içindeki
  düzen kontrolleri `#define _Static_assert(...)` ile kapatılır.

```bash
python3 App/apps/usbterm/test/test_term.py
```

Diğer örnekler: `App/apps/kisstnc/test/`, `App/apps/resistor/test/`.

---

## 11. Sorun giderme

| Belirti | Olası neden / çözüm |
|---|---|
| F+7 Apps menüsünü açmıyor | Labs dışında bir firmware yüklü. |
| Menüde `NOT SUPPORTED` | Uygulama bu firmware'de olmayan bir yetenek istiyor (ör. `serial`): Labs v6.3.0+ kullanın. |
| Menüde `UPDATE FIRMWARE` | Uygulama daha yeni API seviyesi istiyor. |
| `uvterm.py`: "Telsiz bulunamadı" | Kablo veri kablosu mu? Telsiz açık mı? `uvterm.py ports` ile bakın, `-p` ile verin. |
| `uvterm.py`: "...açılamadı" | Port başka bir programda açık (UV Studio, CHIRP, başka terminal). Linux'ta `sudo usermod -aG dialout $USER`, sonra oturumu kapatıp açın. |
| `uvterm.py install`: "komut protokolüne yanıt vermedi" | Telsiz bir uygulamanın içinde ya da DFU modunda. Ana ekrana dönün. |
| USB Term'de `NO USB` | Bilgisayarda portu açan bir program yok (DTR). |
| Yazdıklarım terminalde iki kez görünüyor | Terminalin yerel echo'su açık: telsize `/echo off` gönderin ya da terminalde local echo'yu kapatın. |
| Uzun metnin bir kısmı eksik | Telsizin 256 B alma tamponu taştı (`/info` → `lost`): daha yavaş gönderin. |
| Uygulama içinde telsiz yeniden başladı | Uygulamada bir hata (çökme → watchdog). Bilgisayar testleriyle ayıklayın. |

---

**Bağlantılar:** `App/apps/app_api.h` · `App/apps/app_overlay.h` ·
`App/apps/pack_app.py` · `App/apps/app_assets.py` · `compile-app.sh` ·
USB Term: `App/apps/usbterm/README.md` · uvterm: `tools/uvterm/README.md`
