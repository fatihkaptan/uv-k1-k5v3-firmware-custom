# 9. Cihaz Kullanımı: Adım Adım

[← Önceki: Cihaz donanımı ve ekran](08-cihaz-donanimi-ve-ekran.md) · [İçindekiler](README.md) · [Sonraki: Menü referansı →](10-menu-referansi.md)

Bu bölüm telsizin günlük kullanımını en temelden ileri özelliklere kadar adım adım
anlatır. Menü öğelerinin tek tek açıklaması [10. bölümde](10-menu-referansi.md).

**Gösterim kuralları**

- `TUŞ`: Kısa basış. **uzun `TUŞ`**: Tuşu yaklaşık yarım saniye basılı tutmak.
- `F` + `TUŞ`: Önce `F` (`#`) tuşuna basıp bırakın, sonra ikinci tuşa basın. İki tuşu
  aynı anda basılı tutmanız gerekmez. `F`'ye basınca durum çubuğunda kutulu bir `F` görünür.
- **`UP`/`DOWN`**: UV-K1'de bunlar `SetNav` ayarına göre sol/sağ tuşlardır.

## İçindekiler

1. [Firmware yükleme ve kalibrasyon yedeği](#91-firmware-yükleme-ve-kalibrasyon-yedeği)
2. [Açma, kapama, ses](#92-açma-kapama-ses)
3. [Kurulum adım adım](#93-kurulum-adım-adım)
4. [Tuş mantığı: kısa, uzun, F, kilit](#94-tuş-mantığı-kısa-uzun-f-kilit)
5. [Frekans girme ve ayarlama](#95-frekans-girme-ve-ayarlama)
6. [VFO A, VFO B ve bantlar](#96-vfo-a-vfo-b-ve-bantlar)
7. [Hafıza kanalları](#97-hafıza-kanalları)
8. [Röle kanalı programlama (tam örnek)](#98-röle-kanalı-programlama-tam-örnek)
9. [Gönderim (TX)](#99-gönderim-tx)
10. [Dinleme ayarları](#910-dinleme-ayarları)
11. [Alım modları: Dual Watch, Full Watch, Cross Band](#911-alım-modları-dual-watch-full-watch-cross-band)
12. [Tarama](#912-tarama)
13. [Frekans ve ton yakalama (`F` + `4`, `F` + `*`)](#913-frekans-ve-ton-yakalama-f--4-f--)
14. [Spektrum analizörü (`F` + `5`)](#914-spektrum-analizörü-f--5)
15. [FM yayın radyosu (`F` + `0`)](#915-fm-yayın-radyosu-f--0)
16. [Yan tuşlar ve aksiyon seçici](#916-yan-tuşlar-ve-aksiyon-seçici)
17. [Ekran, arka ışık, ekran koruyucu](#917-ekran-arka-ışık-ekran-koruyucu)
18. [Pil yönetimi ve uyku](#918-pil-yönetimi-ve-uyku)
19. [RF Log](#919-rf-log)
20. [Multiboot ve Multiconfig](#920-multiboot-ve-multiconfig)
21. [Rescue Ops (FieldOps, Labs)](#921-rescue-ops-fieldops-labs)
22. [Fox Hunt, Beacon ve BEAM](#922-fox-hunt-beacon-ve-beam)
23. [AirCopy (Transfer, Labs)](#923-aircopy-transfer-labs)
24. [UV Studio, K5Viewer ve CHIRP](#924-uv-studio-k5viewer-ve-chirp)
25. [Sıfırlama](#925-sıfırlama)

---

## 9.1 Firmware yükleme ve kalibrasyon yedeği

Kısa özet (ayrıntılar [KILAVUZ_TR.md](../KILAVUZ_TR.md) dosyasında):

1. **[UV Studio](https://armel.github.io/uvstudio/)** sayfasını Web Serial destekli bir
   masaüstü tarayıcıda açın (Chrome, Edge, Brave, Opera veya Firefox 151+).
2. Telsizi USB-C veya programlama kablosuyla bağlayıp **DFU (flash) moduna** alın.
   Bu mod, telsizin önyükleyicisi tarafından sağlanır. Giriş yöntemi UV Studio'da anlatılır.
3. **Flash Firmware** → sürümü seçin → seri portu seçin → bekleyin.
4. Telsiz yeniden başladıktan sonra, **normal modda**, **Dump Calibration** ile
   `calibration.dat` dosyasını indirip güvenli bir yerde saklayın. Dosya adına telsizin
   seri numarasını yazın.

> [!CAUTION]
> Kalibrasyon yedeği olmadan telsizin özel kalibrasyonunu kaybederseniz geri getirmenin
> kolay bir yolu yoktur. Bu adımı atlamayın.

## 9.2 Açma, kapama, ses

- **Açma / kapama**: Üstteki ses düğmesini çevirin. "Tık" sesiyle açılır.
- **Ses seviyesi**: Aynı düğmeyle. Firmware ayrıca `SetVol` menüsüyle dijital ses
  kazancını (1–63) ayarlamanızı sağlar. Düğme çok açıkken ses bozuluyorsa `SetVol`'u azaltın.
- **Açılış ekranı**: `POnMsg` menüsüne göre logo, mesaj, gerilim veya ses gösterilir.
- **Açılışta tuş basılıysa**: "Tuşları bırakın" ekranı çıkar; özel açılış modları için
  bkz. [9.20](#920-multiboot-ve-multiconfig) ve aşağıdaki tablo.

| Açılışta basılı tutulan | Sonuç | Sürüm |
|-------------------------|-------|-------|
| `MENU` | Multiboot firmware seçicisi | Hepsi |
| `PTT` + `SIDE1` | Gizli (servis) menü öğeleri bu oturum için açılır | Hepsi |
| `PTT` + `SIDE2` | AirCopy modu | Transfer, Labs |
| `PTT` + gizli tuş (`SetKey`, varsayılan `MENU`) | Rescue Ops menü kilidini aç/kapat | FieldOps, Labs |

## 9.3 Kurulum adım adım

Telsizi ilk kez kullanırken sırasıyla:

1. **Pili tam şarj edin.**
2. **Anteni takın.** Antensiz gönderim vericiye zarar verebilir.
3. **Kalibrasyonu yedekleyin** (bkz. [9.1](#91-firmware-yükleme-ve-kalibrasyon-yedeği)).
4. **Gizli menüyü açın**: Telsizi kapatın, `PTT` ve `SIDE1`'i basılı tutarak açın,
   ekran gelince bırakın. Menü doğrudan gizli öğelerin başında açılır.
5. **Bölge kilidi (`F Lock`)**:
   - Belgeli amatör: **`CE HAM 144-146 430-440`**
   - Belgesiz: **`DISABLE ALL`** (telsiz yalnızca alıcı olur)
6. **Pil tipi (`BatTyp`)**: Takılı pile göre seçin.
7. **Gezinme (`SetNav`)**: UV-K1 için `LEFT/RIGHT`, UV-K5 için `UP/DOWN`.
8. `EXIT` ile çıkın. Gizli öğeler yeniden başlatınca gizlenir; ayarlar kalır.
9. **Squelch**: `F` + `UP`/`DOWN` ile 3–4.
10. **Tuş kilidi**: Kemerde veya çantada yanlışlıkla `PTT`'ye basılmasını önlemek için
    `SetLck` → `KEYS PTT` seçin. Kilitlemek ve açmak için **uzun `F`**.
11. **Açılış mesajı ve çağrı işareti**: Açılış mesajı (`POnMsg` = `MESSAGE` veya `ALL`)
    programlama yazılımıyla yazılır. Labs sürümündeki **APRS TX** ve **APRS DIGI**
    uygulamaları, profil boşsa açılış mesajının ilk satırını **çağrı işareti** olarak kullanır.

## 9.4 Tuş mantığı: kısa, uzun, F, kilit

- **Kısa basış**: Tuşun ana işlevi (rakam girme, menü, gezinme).
- **Uzun basış**: Rakam tuşlarında `F` işlevini doğrudan çalıştırır. `5`, `7`, `8`, `9`'da
  ise farklı bir işlev çalıştırır (bkz. [8.7](08-cihaz-donanimi-ve-ekran.md#87-tuşlar)).
- **`F` tuşu**: Bir sonraki tuşa ikinci anlamını verir. Birkaç saniye içinde ikinci tuşa
  basılmazsa iptal olur. İkinci kez `F`'ye basmak da iptal eder.
- **Uzun `F`**: Tuş takımını kilitler veya kilidi açar. Kilitliyken bir tuşa basarsanız
  "Long press # to unlock" yazar.
- **`SetLck`** neyin kilitleneceğini belirler: yalnızca tuşlar, tuşlar ve yan tuş aksiyonları,
  tuşlar ve `PTT`, ya da hepsi.
- **`KeyLck`**: Belirli bir süre tuşa basılmazsa otomatik kilit.
- **Tuş sesi**: `Beep` menüsünden açılıp kapatılır. Çift "bip" bir işlemin reddedildiğini gösterir.

## 9.5 Frekans girme ve ayarlama

### Doğrudan giriş

1. VFO modunda olun (ekranda kanal numarası değil frekans görünmeli; değilse `F` + `3`).
2. Frekansı **kHz çözünürlüğünde** yazın. Telsiz **6 hane** bekler (1 GHz üstünde 7):

   | Yazdığınız | Sonuç |
   |------------|-------|
   | `1 4 5 5 0 0` | 145,500 MHz |
   | `4 3 3 5 0 0` | 433,500 MHz |
   | `1 4 5` (bekle) | Eksik haneler sıfırla tamamlanır → 145,000 MHz |
   | `1 4 5 5` (bekle) | → 145,500 MHz |

3. Sonuç seçili **adıma yuvarlanır**. 12,5 kHz adımda `145506` yazarsanız 145,5000 veya
   145,5125'e yuvarlanır.
4. Giriş sırasında **`EXIT`** son rakamı siler. Bütün rakamlar silinirse VFO önceki
   frekansına döner.
5. Desteklenmeyen frekanslar (ör. 630–840 MHz) en yakın geçerli uca çekilir.

### `UP` / `DOWN` ile

- Her basış frekansı bir **adım** değiştirir. Basılı tutarsanız hızla ilerler.
- **Adım değiştirme**: `F` + `SIDE1` / `F` + `SIDE2` veya `Step` menüsü.
- İzin verilmeyen bir frekansa gelirseniz çift bip duyulur.

### Geri alma

- **Uzun `EXIT`**: VFO'yu, rakam girmeye başlamadan önceki **tam durumuna** (frekans, ton,
  güç vb.) geri yükler.

## 9.6 VFO A, VFO B ve bantlar

- Telsizde iki bağımsız VFO vardır: **A** (üst) ve **B** (alt).
- **`F` + `2`**: Etkin (ana) VFO'yu değiştirir. Dolu üçgen etkin VFO'yu gösterir;
  `PTT` bu VFO'dan gönderir.
- **`F` + `1`**: Bant değiştirir (bkz. [7.1](07-frekans-rehberi.md#71-telsizin-alım-ve-gönderim-aralıkları)).
  Kanal modundayken ise **kanalı VFO'ya kopyalar**: kanalı bozmadan VFO'da değişiklik denemek için.
- **`F` + `3`**: VFO ↔ kanal (MR) modu.
- **`F` + `6`** (veya uzun `6`): Çıkış gücünü sırayla değiştirir.

## 9.7 Hafıza kanalları

Telsiz **1024 kanal** saklar. Her kanal; RX/TX frekansı, kayma, CTCSS/DCS, güç, bant
genişliği, modülasyon, tarama listesi, meşgul kilidi, compander, TX kilidi ve 10 karakterlik
adı içerir.

### Kanal kaydetme (`ChSave`)

1. VFO'da frekansı ve bütün ayarları (ton, kayma, güç, `W/N`) yapın.
2. `MENU` → `Channels` → `ChSave` → `MENU`.
3. `UP`/`DOWN` ile bir kanal numarası seçin veya numarayı yazın. Boş kanallar ayrıca belirtilir.
4. `MENU` ile onaylayın. Dolu bir kanalın üzerine yazmak onay ister.

### Kanal adı verme (`ChName`)

1. `MENU` → `ChName` → `MENU` → kanalı seçin → `MENU`.
2. Ad düzenleyici açılır (en fazla 10 karakter):

   | Tuş | İşlev |
   |-----|-------|
   | `0`–`9` | Telefon tuş takımı gibi çoklu basış: `2` = a → b → c → 2, `7` = p → q → r → s → 7 |
   | `1` | Noktalama: `. , - ( ) @ / \ + = * # < > [ ] ~ 1` |
   | `0` | Boşluk, `0` |
   | Uzun rakam | Doğrudan o rakamı yazar |
   | `UP` / `DOWN` | Mevcut karakteri ASCII sırasında değiştirir |
   | `F` | Büyük / küçük harf geçişi (uzun `F`: `#`) |
   | `*` | `-` yazar (uzun `*`: `*`) |
   | `MENU` | Sonraki karaktere geç (uzun `MENU`: adı bitir) |
   | `EXIT` | Bir karakter geri (en baştayken: çık) |

3. Son karakterden sonra `MENU` adı kaydeder.

### Kanal silme (`ChDele`)

`MENU` → `ChDele` → kanalı seçin → `MENU` → onaylayın.

### Kanalları kullanma

- `F` + `3` ile kanal moduna geçin.
- `UP` / `DOWN` ile kanallar arasında gezinin (boş kanallar atlanır).
- Kanal numarasını doğrudan yazın: `1` `2` → kanal 12 (kısa bekleme sonrası uygulanır).
- **`ChDisp`**: Kanalın nasıl görüneceği: frekans, kanal numarası, ad veya ad + frekans.

### Kanalı tarama listesine atama

- **Uzun `5`** (kanal modunda): Kanalın listesini sırayla değiştirir:
  `OFF` → `01` → … → `24` → `ALL` → `OFF`. Kanal taramadan hariç tutulmuşsa (`EX`) önce
  hariç tutmayı kaldırır.
- Veya `MENU` → `ChList`.

### 1 Call kanalı

`1 Call` menüsünde seçtiğiniz kanala **uzun `9`** ile tek tuşla gidersiniz. Sık kullandığınız
röle veya çağrı frekansı için idealdir.

## 9.8 Röle kanalı programlama (tam örnek)

Örnek röle (tamamen temsilidir; gerçek değerleri yerel röle listesinden alın):
**çıkış 145,650 MHz, kayma −600 kHz, ton 88,5 Hz**.

1. VFO moduna geçin (`F` + `3`).
2. `1 4 5 6 5 0` yazın → 145,650 MHz.
3. `MENU` → `Channels` (veya `All`) → **`TxODir`** → `-` → `MENU`.
4. **`TxOffs`** → `0.60000` → `MENU`.
5. **`TxCTCS`** → `88.5` → `MENU`.
6. (İsteğe bağlı) **`RxCTCS`** → `88.5`. Böylece yalnızca röle açıldığında hoparlör açılır.
   Rölenin çıkışında ton yoksa kapalı bırakın.
7. **`W/N`** → `WIDE`.
8. **`ChSave`** → boş bir kanal → `MENU`.
9. **`ChName`** → örneğin `ROLE TEPE`.
10. `EXIT` ile çıkın. Ekranın bilgi satırında `CT` ve `-` görünmelidir.

**Test**: Kanaldayken `PTT`'ye kısa basın. Röle açılırsa bir "kuyruk" (squelch kuyruğu veya
röle bip sesi) duyarsınız. `PTT` basılıyken ekranda gönderim frekansı **144,050 MHz** görünür.

**Sorun mu var?**

| Belirti | Kontrol |
|---------|---------|
| Röleyi duyuyorum ama açamıyorum | `TxCTCS` değeri, `TxODir` yönü, `F Lock`, güç |
| `TX DISABLE` yazıyor | `F Lock` ayarı gönderim frekansını kapsıyor mu? |
| Röle hiç duyulmuyor | Frekans doğru mu? `RxCTCS` yanlış bir değere ayarlı olabilir; kapatın |
| Ses bozuk | `W/N` ayarı |

## 9.9 Gönderim (TX)

### Temel

1. Frekansın **boş** olduğunu dinleyerek kontrol edin.
2. `PTT`'ye basın, **1 saniye bekleyin**, konuşun. Telsizi ağzınızdan **5–10 cm** uzakta tutun.
3. Bitince `PTT`'yi bırakın.
4. Gönderim sırasında kırmızı LED yanar, S-metre alanı güç seviyesini gösterir.

### PTT modları (`SetPTT`)

| Mod | Davranış |
|-----|----------|
| `CLASSIC` | Basılı tuttuğunuz sürece gönderir |
| `ONEPUSH` | Bir kez basınca gönderime başlar, tekrar basınca durur. **Elleriniz serbest kalır ama gönderimde kaldığınızı unutmayın.** |

Durum çubuğunda `CL` veya `OP` görünür.

### Güç

- `F` + `6` veya `Power` menüsü: `LOW 1` … `HIGH`, `USER`.
- `USER` seviyesinin değeri `SetPwr` ile seçilir.
- **`POWER HIGH`** yan tuş işlevi: Geçici olarak en yüksek güce geçer.
- **İhtiyaç kadar güç** kullanın (bkz. [3.2](03-desibel-ve-sinyal-olcumu.md#32-akılda-tutulacak-db-kuralları)).

### Zaman aşımı ve uyarılar

| Menü | İşlev |
|------|-------|
| `TxTOut` | En uzun kesintisiz gönderim süresi (30 s – 15 dk). Süre dolunca gönderim kesilir: `TIMEOUT` |
| `SetTOT` | Zaman aşımı yaklaşırken uyarı: ses, görsel veya ikisi |
| `SetEOT` | Karşı tarafın gönderimi bittiğinde uyarı: ses, görsel (yeşil LED yanıp söner) veya ikisi |
| `BusyCL` | Kanal meşgulken gönderimi engeller (`BUSY`) |
| `Roger` | `PTT` bırakılınca bip (`ROGER`) veya MDC kimliği |

### Ses ve mikrofon

- **`Mic`**: Mikrofon kazancı (+1,5 dB … +31,5 dB). Karşı taraf sizi kısık duyuyorsa
  artırın; bozuk duyuyorsa azaltın.
- **`MicBar`**: Gönderim sırasında mikrofon seviye çubuğu.
- **`Compnd`**: Compander. Karşı taraf da kullanıyorsa açın.
- **VOX** (`VOX` menüsü, 1–10): Konuşmaya başlayınca otomatik gönderim. Düşük değerler
  daha hassastır. Uzun `7` ile açılıp kapatılır. Gürültülü ortamda istemeden gönderim yapabilir.
- **`1750Hz`** yan tuş işlevi: Eski Avrupa rölelerini açmak için 1750 Hz tonu.

### Çapraz kontrol: gönderimi engelleyen her şey

`F Lock` (bölge), kanalın `TXLock`'u, düşük pil, aşırı gerilim, `BusyCL`, bilgisayar
bağlantısı sırasındaki ayar aktarımı.

> [!WARNING]
> Bir kanalda **`TXLock` = `OFF`** yapılırsa, o kanal **`F Lock` bölge kilidinin dışındaki**
> frekanslarda da gönderim yapabilir. Bu ayarı yalnızca ne yaptığınızı biliyorsanız ve
> o frekansta gönderim yetkiniz varsa değiştirin. Varsayılan `ON`'dur.

## 9.10 Dinleme ayarları

| Ayar | Nasıl | Öneri |
|------|-------|-------|
| **Squelch** | `F` + `UP`/`DOWN` (kalıcı kaydedilir) veya `Sql` | 3–4 |
| **Monitör** | `SIDE1` (varsayılan) | Zayıf sinyali dinlemek için squelch'i geçici açar |
| **Ses kazancı** | `SetVol` (1–63) | Bozulma varsa düşürün |
| **Ses profili** | `SetRxA` veya `RxA` yan tuş işlevi | FM: `FLAT`, `CLEAN`, `MID`, `BOOST`, `MAX` · AM: `SHARP`, `STOCK`, `OPEN` |
| **Kuyruk sesi bastırma** | `STE`, `RP STE` | Açık |
| **Ses kapatma** | `MUTE` yan tuş işlevi | Durum çubuğunda üstü çizili hoparlör |
| **Alım tonu** | `RxCTCS` / `RxDCS` | Yalnızca o tonu duymak istiyorsanız |

**Ses profilleri ne yapar?** Alıcının ses filtrelerini ve seviyesini değiştirir. `FLAT` en doğal,
`BOOST` ve `MAX` gürültülü ortamda daha yüksek ve anlaşılır ses verir. AM'de `SHARP` daha dar
ve temiz, `OPEN` daha geniş ve doğal sestir. Profilin adı alım sırasında VFO satırında görünür.

## 9.11 Alım modları: Dual Watch, Full Watch, Cross Band

`RxMode` menüsü veya `RX MODE` yan tuş işlevi ile seçilir:

| Mod | Ne yapar? | Durum çubuğu |
|-----|-----------|--------------|
| `MAIN ONLY` | Yalnızca ana VFO | `MO` |
| `DUAL RX RESPOND` | A ve B'yi sırayla dinler. Sinyal hangisinden geldiyse `PTT` ile oradan cevap verir. | `DWR` |
| `CROSS BAND` | Ana VFO'dan gönderir, diğer VFO'dan alır | `XB` |
| `MAIN TX DUAL RX` | İkisini de dinler, **her zaman ana VFO'dan** gönderir | `DWR` |
| `FULL RX RESPOND` | A, B ve **iki öncelikli kanalı** dinler; sinyalin geldiği kanaldan cevap verir | `FWR` |
| `MAIN TX FULL RX` | Hepsini dinler, her zaman ana VFO'dan gönderir | `FWR` |

- **Öncelikli kanallar** `PriCh1` ve `PriCh2` menülerinden seçilir. Aynı kanal, geçersiz
  kanallar veya zaten VFO A/B'de olan kanallar otomatik atlanır.
- Full Watch çalışırken ekranda `TRIPLE WATCH` / `QUAD WATCH` ve `P1` / `P2` etiketleri,
  arka plandaki dinleme döngüsünü gösteren hareketli oklarla birlikte görünür.
- **`MAIN ONLY`** yan tuş işlevi: Ekranı tek VFO'ya sadeleştirir.
- **`>>`** işareti, son alımın hangi VFO'da olduğunu gösterir.
- Çift dinlemede iki VFO arasında hızla geçildiği için bir VFO'daki kısa bir yayının
  başı kaçabilir. Bu normaldir.

> [!TIP]
> Yerel röleyi ve çağrı frekansını aynı anda izlemek için: VFO A'ya röle kanalını, VFO B'ye
> 145,500 MHz'i koyun ve `DUAL RX RESPOND` seçin.

## 9.12 Tarama

### Tarama nasıl başlatılır, durdurulur?

| İşlem | Tuş |
|-------|-----|
| Taramayı başlat / durdur | **Uzun `*`** veya `SIDE2` (varsayılan `SCAN`) |
| Durdur ve **başlangıç noktasına dön** | `EXIT` |
| Durdur ve **bulunan sinyalde kal** | `MENU` |
| Bulunan sinyali atlayıp o yönde devam et | `UP` / `DOWN` |
| Tarama sırasında listeyi değiştir | `F` + `UP` / `DOWN` veya iki haneli numara: `00` = `ALL`, `01`–`24`, `25` = `MIX` |
| Bulunan kanalı/frekansı taramadan çıkar | Tarama dururken **uzun `MENU`** |

### Kanal taraması (kanal modunda)

- Telsiz, seçili **tarama listesindeki** kanalları gezer.
- **`ScList`**: Hangi listenin taranacağı: `01`–`24`, `ALL` (listesi `OFF` olmayan bütün kanallar) veya `MIX`.
- **`MIX`**: 24 listeden seçtiklerinizi birleştirir. `ScList` → `MIX` → `MENU` ile **MIX
  düzenleyici** açılır: `UP`/`DOWN` ile liste seçin, `MENU` ile ekleyin/çıkarın, iki haneli
  numara ile doğrudan gidin, `EXIT` ile kaydedip çıkın.
- Seçili liste boşsa telsiz otomatik olarak bir sonraki dolu listeye geçer.
- **Liste adları** (3 karakter) bilgisayardan programlama yazılımıyla verilir. Ad yoksa
  numarası gösterilir.
- **`ScPri`** + **`PriCh1`**/**`PriCh2`**: Tarama sırasında öncelikli kanalları daha sık
  kontrol eder. Durum çubuğundaki liste adının yanında `+` görünür.

### Frekans taraması (VFO modunda)

- Telsiz, VFO frekansından başlayarak **adım** aralıklarla ilerler.
- Adımı kanal aralığına eşit yapın (ör. 12,5 kHz); aksi halde sinyalleri atlayabilir.
- **Hariç tutma**: Sürekli gürültü veren frekansları **uzun `MENU`** ile taramadan çıkarın
  (en fazla 64 frekans).

### Tarama aralığı (scan range)

İki frekans arasını taramak için:

1. VFO A'ya alt frekansı (ör. 144,000), VFO B'ye üst frekansı (ör. 146,000) yazın.
2. Ana VFO'dayken **uzun `5`**: Ekranda `ScnRng` görünür.
3. **Uzun `*`** ile taramayı başlatın. Telsiz yalnızca bu aralığı tarar.
4. Aralık modunu kapatmak için tekrar **uzun `5`**.

### Tarama davranışı ve hızı

| Menü | İşlev |
|------|-------|
| `ScnRev` | Sinyal bulununca ne olacak: `STOP` (durur), `CARRIER` + süre (sinyal kesildikten belirtilen süre sonra devam eder), `TIMEOUT` + süre (belirtilen süre sonra her durumda devam eder) |
| `SetScn` | `NORMAL` veya `FAST`. Hızlı modda saniyede yaklaşık 150 frekans taranır. |

Tarama sırasında ekranda ilerleme, RSSI grafiği ve algılanan CTCSS/DCS bilgisi görünür.

## 9.13 Frekans ve ton yakalama (`F` + `4`, `F` + `*`)

### Frekans yakalama tarayıcısı (`F` + `4`)

Yakındaki bir telsizin **frekansını bilmiyorsanız** (ör. yeni aldığınız bir PMR telsizi):

1. `F` + `4`: Tarayıcı açılır ve geniş bir aralıkta en güçlü yakın vericiyi arar.
2. Diğer telsizi **yakına tutup** `PTT`'ye basın.
3. Frekans bulununca telsiz **tonunu da** (CTCSS/DCS) aramaya geçer.
4. Sonuç ekranda görünür. **`MENU`** ile kaydetmeyi başlatın: kanal numarası seçin
   (`UP`/`DOWN` veya rakamlar), tekrar `MENU` ile onaylayın.
5. `*` aramayı yeniden başlatır, `EXIT` çıkar.

> Bu yöntem birkaç metre mesafede ve güçlü sinyalle çalışır. Uzaktaki istasyonları bulmaz.

### Ton taraması (`F` + `*`)

Frekansı bildiğiniz ama tonunu bilmediğiniz bir sinyalde:

1. Frekansa gidin.
2. `F` + `*`: Telsiz, sinyal geldiğinde CTCSS/DCS kodunu arar.
3. Bulunan kod ekranda görünür; kanala kaydedebilirsiniz.

## 9.14 Spektrum analizörü (`F` + `5`)

Spektrum analizörü, VFO frekansının çevresindeki bandı sürekli tarayıp grafik olarak gösterir.
Yorumlama kuralları için bkz. [2.12](02-radyo-dalgalari-ve-spektrum.md#212-spektrum-analizörü-nedir-nasıl-okunur).

### Tuşlar (tarama ekranı)

| Tuş | İşlev |
|-----|-------|
| `UP` / `DOWN` | Merkez frekansı kaydır. Bir sinyal dinleniyorsa taramayı o yönde sürdürür. |
| `1` / `7` | Tarama adımını artır / azalt |
| `2` / `8` | `UP`/`DOWN`'ın kaydırma miktarını artır / azalt |
| `4` | Nokta sayısı: 128 / 64 / 32 / 16 (pencere genişliği) |
| `5` | Frekans gir (merkez) |
| `3` / `9` | Otomatik modda hassasiyet, elle modda ölçeğin üst sınırı (dB) |
| `*` / `F` | Dinleme tetik seviyesini yükselt / düşür (çizgi). Bunu aşan sinyal otomatik dinlenir. |
| `MENU` | Tetik: otomatik ↔ elle |
| `0` | Modülasyon: FM / AM / USB |
| `6` | Dinleme bant genişliği |
| `SIDE1` | En güçlü sinyali **kara listeye** al (bir daha durma) |
| `SIDE2` | Arka ışık |
| `PTT` | En güçlü sinyale ayarlan ve **sabit (STILL) moda** geç |
| `EXIT` | Çık (ayarlar kaydedilir) |

### Sabit (STILL) mod

Tek bir frekansı ayrıntılı dinlemek ve alıcı kazancını elle ayarlamak için:

| Tuş | İşlev |
|-----|-------|
| `UP` / `DOWN` | Frekansı ince ayarla (menü açıksa: seçili yazmaç değerini değiştir) |
| `MENU` | Alıcı kazanç yazmaçları arasında geç: `LNAs`, `LNA`, `PGA` |
| `5` | Frekans gir |
| `SIDE1` | Monitör (squelch'i aç) |
| `EXIT` | Menüyü kapat; menü kapalıysa tarama ekranına dön |

**Kazanç yazmaçları**: `LNAs` (kısa LNA: −19 / −16 / −11 / 0 dB), `LNA` (−24 … 0 dB),
`PGA` (−33 … 0 dB). Güçlü bir sinyal alıcıyı doyuruyorsa bunları düşürün
(bkz. [2.10](02-radyo-dalgalari-ve-spektrum.md#210-parazit-türleri-harmonik-imaj-intermodülasyon-doyma)).

Spektrum ayarları kaydedilir. Telsiz spektrum açıkken kapatılırsa, açılışta spektrum
otomatik olarak geri gelebilir.

## 9.15 FM yayın radyosu (`F` + `0`)

| Tuş | İşlev |
|-----|-------|
| `0`–`9` | Frekans (VFO) veya kanal numarası (hafıza) gir |
| `UP` / `DOWN` | Frekansı / kanalı değiştir |
| `*` | Sonraki istasyonu ara |
| `F` + `*` | Otomatik tarama: bulduğu istasyonları 48 kanala kaydeder |
| `MENU` | Frekansı kaydet (VFO) / kanalı sil (hafıza) |
| `F` + `3` | VFO ↔ hafıza |
| `F` + `0` veya `EXIT` | Çık |

FM radyo ayrı bir alıcıyla (BK1080) çalışır.

## 9.16 Yan tuşlar ve aksiyon seçici

### Kalıcı atama

`F1Shrt`, `F1Long` (`SIDE1`), `F2Shrt`, `F2Long` (`SIDE2`) ve `M Long` (uzun `MENU`) menüleriyle
her tuşa bir işlev atanır. İşlevler [10.5'te](10-menu-referansi.md#105-tuşlar-keys).

**Önerilen düzen (başlangıç için)**:

| Tuş | İşlev |
|-----|-------|
| `SIDE1` kısa | `MONITOR` |
| `SIDE1` uzun | `RX MODE` |
| `SIDE2` kısa | `SCAN` |
| `SIDE2` uzun | `RF LOG` |
| Uzun `MENU` | `MAIN ONLY` veya `POWER` |

### Aksiyon seçici (Action Picker)

Bir işlevi kalıcı olarak atamadan **bir kez** çalıştırmak için:

1. `F`'ye basın.
2. `SIDE1` veya `SIDE2`'ye **uzun** basın: aksiyon listesi açılır.
3. `UP`/`DOWN` ile işlevi seçin, `MENU` ile çalıştırın. `EXIT` veya `F` iptal eder.
4. Telsiz her yan tuş için son seçiminizi hatırlar. Bir süre işlem yapılmazsa seçici kapanır.

## 9.17 Ekran, arka ışık, ekran koruyucu

| Ayar | İşlev |
|------|-------|
| `BLTime` | Arka ışığın açık kalma süresi (`OFF`, 5 s – 5 dk, `ON` = sürekli) |
| `BLMin` / `BLMax` | Arka ışığın kısık ve tam parlaklığı |
| `BLTxRx` | Alım ve/veya gönderimde arka ışığı aç |
| `F` + `8` | Arka ışığı **geçici olarak** min ↔ maks arasında değiştir (ampul simgesi) |
| `F` + `9` | Ayarlı arka ışık davranışına dön |
| `SetCtr` | Kontrast (1–15) |
| `SetInv` | Ters ekran (açık zemin ↔ koyu zemin) |
| `SetMet` | S-metre: `TINY` / `CLASSIC` |
| `SetGUI` | VFO bilgi satırı: `TINY` / `CLASSIC` |
| `ChDisp` | Kanal görünümü |
| `SetSav` | Ekran koruyucu: `OFF`, `LOGO`, `LOGO+`, `MATRIX` |
| `POnMsg` | Açılış ekranı |
| `BatTxt` | Pil göstergesi: yok, voltaj, yüzde |
| `SetTmr` | Durum çubuğunda RX/TX süre sayacı |

## 9.18 Pil yönetimi ve uyku

- **`BatSav`**: Dinleme sırasında alıcıyı kısa aralıklarla kapatıp açar. `1:1` … `1:5`
  (büyük oran = daha çok tasarruf, ama yayınların başı kaçabilir).
- **`SetOff`**: Belirli süre (1 dk – 2 saat) işlem yapılmazsa **derin uykuya** geçer.
- **`BatTyp`** ve **`BatCal`**: Doğru yüzde ve gerilim göstergesi için (gizli menü).
- **`BatVol` / `SysInf`**: Pil gerilimi, yüzdesi ve sistem bilgileri.

## 9.19 RF Log

RF Log, telsizin **alım ve gönderim etkinliğini** otomatik olarak harici flash'a kaydeder:
yön (RX/TX), frekans, kanal ve adı, süre, S-metre seviyesi ve pil gerilimi.

### Etkinleştirme

RF Log, bir yan tuşa (`F1Shrt`, `F1Long`, `F2Shrt`, `F2Long` veya `M Long`) **`RF LOG` işlevi
atandığında** etkin olur. Bu tuş aynı zamanda kayıt geçmişi ekranını açar.

### Geçmiş ekranının tuşları

| Tuş | İşlev |
|-----|-------|
| `UP` / `DOWN` | Kayıtlar arasında gezin |
| `F` + `UP` / `F` + `DOWN` | İlk / son kayda git |
| `MENU` | Filtre: hepsi → yalnızca RX → yalnızca TX |
| `*` | Ayrıntı sütunu: süre → … → pil gerilimi |
| Uzun `MENU`, sonra tekrar uzun `MENU` | Bütün kayıtları sil (onaylı) |
| Uzun `F` | Tuş kilidi |
| `EXIT` | Çık (silme onayı açıksa iptal eder) |

UV Studio, kayıtları canlı bir panoda gösterir, analiz eder ve CSV olarak dışa aktarır.

## 9.20 Multiboot ve Multiconfig

### Multiboot

Harici flash'ta **Main** (otomatik yedek) ve **4 kullanıcı yuvası** olmak üzere 5 firmware saklanır.

1. Telsizi kapatın, **`MENU`'yü basılı tutarak** açın, seçici görününce bırakın.
2. `UP`/`DOWN` ile yuvayı seçin. Her yuvada sürüm adı ve numarası görünür.
3. `MENU` ile o firmware'i geri yükleyin, `EXIT` ile değişiklik yapmadan çıkın.

Yuvalara firmware UV Studio ile yüklenir. Böylece örneğin Fusion ile Labs arasında
bilgisayarsız geçiş yapabilirsiniz.

> [!CAUTION]
> Geri yükleme sırasında telsizi **asla kapatmayın**.

### Multiconfig

Her firmware yuvasının kendi **yapılandırma bankası** vardır: kanallar ve adları, VFO'lar,
tarama listeleri, radyo ve sürüme özel ayarlar.

- **`SetCfg`** menüsü başka bir bankayı **yeniden başlatmadan** uygular.
- Durum çubuğu etkin bankayı gösterir: `CM` (Main) veya `C1`–`C4`.
- `SetCfg` seçimi kapama/açmada korunur. Ancak Multiboot ile firmware değiştirildiğinde
  doğal eşleşme geri gelir (`Main` → `CFG M`, yuva N → `CFG N`).

**Kullanım fikri**: Bankaları **senaryolara** göre ayırın: `CFG M` günlük amatör kullanım,
`CFG 1` dağ/SOTA, `CFG 2` havacılık ve deniz dinleme, `CFG 3` tilki avı…

## 9.21 Rescue Ops (FieldOps, Labs)

Saha ekiplerine dağıtılan telsizlerin yanlışlıkla yeniden ayarlanmasını önler.

- **Açma / kapama**: Telsizi kapatın, **`PTT` + gizli tuşu** (`SetKey`, varsayılan `MENU`)
  basılı tutarak açın.
- Kilit açıkken:
  - `MENU` ile menüye girilemez.
  - `F` kısayolları (yalnızca `F` + `2` hariç) ve `*` işlevleri devre dışıdır.
  - Durum çubuğunda `RO` görünür.
  - Açılışta `PTT` + `SIDE1` ile gizli menüye de girilemez.
- `SetKey` menüsü gizli tuşu değiştirir: `KEY_MENU`, `KEY_UP`, `KEY_DOWN`, `KEY_EXIT`, `KEY_STAR`.

## 9.22 Fox Hunt, Beacon ve BEAM

Bu işlevler FieldOps sürümünde yerleşik, Labs sürümünde uygulama olarak bulunur. Yan tuşa
`FOX HUNT`, `BEACON` veya `BEAM` atanarak doğrudan açılabilirler.

### Fox Hunt (alıcı)

Gizli bir vericiyi (tilki) yönlü antenle bulmak için sinyal gücü göstergesi:

| Tuş | İşlev |
|-----|-------|
| `1` | Gösterge: çubuk S-metre / kayan geçmiş grafiği |
| `2` | Ses: kapalı / Geiger sayacı gibi bip / alınan ses |
| `3`, `UP` / `DOWN` | RF zayıflatıcı |
| `MENU` | Tepe / minimum değerlerini sıfırla |
| Uzun `F` | Tuş kilidi (zayıflatıcı ok tuşlarıyla ayarlanabilir kalır) |
| `EXIT` | Çık |

Ekranda kalibre S-metre, dBm, tepe/minimum değerleri ve 1 saniyelik eğilim görünür.

### Beacon (verici)

Telsizi gizli bir ARDF vericisine dönüştürür: belirli aralıklarla Mors tanımlayıcısı gönderir.

| Tuş | İşlev |
|-----|-------|
| `1` | Gönderim penceresi süresi |
| `2` | Bekleme süresi |
| `3` | Tanımlayıcı: `MOE`, `MOI`, `MOS`, `MOH`, `MO5`, `MO`, çağrı işareti, çağrı işareti + `MOE` |
| `4` | Anahtarlama: `TONE` (taşıyıcı sürekli, ton anahtarlanır, MCW) / `CARR` (taşıyıcı da kesilir) |
| `F` + tuş | Değeri geri al |
| `MENU` | Bekleme süresini yeniden başlat |
| Uzun `F` | Tuş kilidi |
| `EXIT` | Çık |

> [!IMPORTANT]
> Beacon, insansız ve tekrarlı bir gönderimdir. **Yalnızca belgeyle**, izin verilen
> frekansta, düşük güçte ve organize bir tilki avı etkinliğinde kullanın.

### BEAM (kanal aktarma)

Bir VFO'nun bütün ayarlarını **telsizden telsize radyo üzerinden** gönderir. Alıcı telsiz
ayarı **ilk boş hafıza kanalına** kaydeder.

1. İki telsizi **aynı frekansa** ayarlayın.
2. İki telsizde de BEAM'i açın.
3. `UP` / `DOWN` ile modu seçin: göndericide `BEAM TX`, alıcıda `BEAM RX`.
4. Önce alıcıda, sonra göndericide `MENU`'ye basın.
5. Durum mesajları: `SENDING`, `SENT`, `WAITING`, `RECEIVED`, `MEM FULL` (boş kanal yok), `ERROR`.

## 9.23 AirCopy (Transfer, Labs)

İki telsiz arasında hafıza bankalarını ve ayarları kopyalar.

1. **Her iki telsizi** `PTT` + `SIDE2` basılıyken açın: AirCopy modu.
2. `*` ile `AIR COPY` (radyo üzerinden) veya `CABLE COPY` (kablo ile, Transfer sürümü) seçin.
3. `UP` / `DOWN` ile içerik seçin: bir 128 kanallık banka, `Settings` veya `All (Mem+Set)`.
   Kablo modunda ayrıca `Flash 2M` (bütün harici flash).
4. **Alıcı telsizde `EXIT`**, **gönderici telsizde `MENU`**.
5. İlerleme ekranı yeniden denemeleri ve hataları gösterir. Yalnızca **farklı olan bloklar**
   gönderilir (CRC32 karşılaştırması).

- İki telsiz **aynı firmware sürümünü** kullanmalıdır.
- `Flash 2M` kopyası **kalibrasyon sektörünü kopyalamaz**. İşlemden sonra alıcıyı yeniden başlatın.

## 9.24 UV Studio, K5Viewer ve CHIRP

### UV Studio

[UV Studio](https://armel.github.io/uvstudio/), tarayıcıdan çalışan ve kurulum gerektirmeyen bir araçtır:

- Firmware yükleme, Multiboot yuvalarını doldurma
- Kalibrasyon yedekleme / geri yükleme
- Açılış logosu yükleme
- Overlay uygulamalarını yükleme (Labs)
- **K5Viewer**: Telsiz ekranını bilgisayarda canlı görme, ekran görüntüsü alma, tuşları
  uzaktan kullanma. USB bağlantısı koparsa otomatik yeniden bağlanır.
- RF Log panosu, analizler, CSV dışa aktarma

### CHIRP

[CHIRP](https://chirpmyradio.com/), kanalları bilgisayarda tablo olarak düzenlemenizi sağlar.

- Bu firmware için **özel bir CHIRP sürücüsü** gerekir. Sürücü her sürümle birlikte
  [Releases](https://github.com/armel/uv-k1-k5v3-firmware-custom/releases) sayfasında yayımlanır.
- CHIRP'te: **File → Load Module** ile sürücüyü yükleyin, sonra **Radio → Download From Radio**.
- Kanalları düzenledikten sonra **Radio → Upload To Radio**.
- Firmware ve sürücüyü **aynı sürümden** kullanın.
- Kanal tablosunu **dosya olarak yedekleyin**. Telsiz sıfırlanırsa birkaç dakikada geri yüklersiniz.

## 9.25 Sıfırlama

Gizli menüdeki **`Reset`**:

| Seçenek | Ne sıfırlanır? |
|---------|----------------|
| `VFO` | Ayarlar ve VFO'lar fabrika değerlerine döner; hafıza kanalları korunur |
| `ALL` | **Her şey**: kanallar dahil fabrika ayarları |

> [!WARNING]
> `ALL` sıfırlamasından önce kanallarınızı CHIRP ile yedekleyin. Kalibrasyon verisi sıfırlamadan
> etkilenmemelidir, ama yedeğiniz yine de hazır olsun.

---

[← Önceki: Cihaz donanımı ve ekran](08-cihaz-donanimi-ve-ekran.md) · [İçindekiler](README.md) · [Sonraki: Menü referansı →](10-menu-referansi.md)
