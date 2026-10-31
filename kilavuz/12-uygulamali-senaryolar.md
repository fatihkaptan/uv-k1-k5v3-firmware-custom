# 12. Uygulamalı Senaryolar

[← Önceki: Uygulamalar](11-uygulamalar.md) · [İçindekiler](README.md) · [Sonraki: Sözlük →](13-sozluk.md)

Bu bölüm, öğrendiklerinizi gerçek durumlarda kullanmanız için **adım adım tarifler** içerir.
Senaryoların çoğu **belge gerektirmez** (yalnızca dinleme). Gönderim içerenler ayrıca işaretlenmiştir.

## İçindekiler

1. [Birinci gün: dinleme turu](#121-birinci-gün-dinleme-turu)
2. [Yerel röleleri bulmak ve kaydetmek](#122-yerel-röleleri-bulmak-ve-kaydetmek)
3. [Havacılık bandını dinlemek](#123-havacılık-bandını-dinlemek)
4. [ISS'i dinlemek ve resim almak](#124-issi-dinlemek-ve-resim-almak)
5. [APRS paketlerini almak](#125-aprs-paketlerini-almak)
6. [Telefonla APRS (belgeli)](#126-telefonla-aprs-belgeli)
7. [Radyosonda avı](#127-radyosonda-avı)
8. [Deniz kenarında: AIS, kanal 16, DSC](#128-deniz-kenarında-ais-kanal-16-dsc)
9. [Tilki avı (ARDF)](#129-tilki-avı-ardf)
10. [Acil durum için hazırlık](#1210-acil-durum-için-hazırlık)
11. [Senaryolara göre Multiconfig bankaları](#1211-senaryolara-göre-multiconfig-bankaları)
12. [Telsizleri aynı ayarlara getirmek](#1212-telsizleri-aynı-ayarlara-getirmek)
13. [Bilinmeyen bir sinyalin ne olduğunu anlamak](#1213-bilinmeyen-bir-sinyalin-ne-olduğunu-anlamak)
14. [Belge aldıktan sonra ilk görüşme](#1214-belge-aldıktan-sonra-ilk-görüşme)

---

## 12.1 Birinci gün: dinleme turu

**Amaç**: Telsizin temel işlevlerine alışmak.

1. **FM radyo**: `F` + `0` → `UP`/`DOWN` ile bir istasyon bulun → `EXIT`.
2. **Çağrı frekansı**: VFO modunda `1 4 5 5 0 0` → 145,500 MHz. `W/N` = `WIDE`, squelch 3.
   Bir süre dinleyin.
3. **Spektrum**: `F` + `5`. Ekranda tepeler görüyor musunuz? `UP`/`DOWN` ile 144–146 MHz
   arasında gezin. Bir tepe görürseniz `PTT` ile o sinyale ayarlanıp dinleyin, `EXIT` ile dönün.
4. **Squelch denemesi**: `F` + `DOWN` ile squelch'i 0'a indirin: sürekli hışırtı duyulur.
   `F` + `UP` ile 3'e çıkarın: hışırtı kesilir. Fark, squelch'in ne işe yaradığını gösterir.
5. **Monitör**: `SIDE1`'e basılı tutun: squelch geçici olarak açılır.
6. **Kilit**: Uzun `F` ile kilitleyin, bir tuşa basın (uyarı çıkar), uzun `F` ile açın.

## 12.2 Yerel röleleri bulmak ve kaydetmek

**Amaç**: Bölgenizdeki 2 m rölelerini bulup kanal olarak kaydetmek. **Belge gerekmez.**

1. **Adımı ayarlayın**: `MENU` → `Step` → `12.50kHz`.
2. **Tarama aralığı kurun**:
   - VFO A: `1 4 5 6 0 0` (145,600)
   - `F` + `2` ile VFO B'ye geçin: `1 4 5 8 0 0` (145,800)
   - `F` + `2` ile VFO A'ya dönün, **uzun `5`**: `ScnRng` görünür.
3. **Uzun `*`**: Tarama başlar. Bir röle konuşma yayınladığında tarama durur.
4. Sesi dinleyin. Bu bir röle çıkışıdır (145,600–145,7875 aralığı).
5. **Tonu bulun**: Taramayı `MENU` ile durdurup o frekansta kalın. Bir dahaki yayında
   `F` + `*` ile CTCSS/DCS tonunu tarayın.
6. **Kaydedin**:
   - `TxODir` → `-`, `TxOffs` → `0.600`, `TxCTCS` → bulunan ton.
   - `ChSave` → boş kanal → `ChName` → ör. `ROLE 1`.
7. **Listeye ekleyin**: Kanal modunda kanala gidin, **uzun `5`** ile `01` listesine atayın.
8. **Sonuç**: Artık `ScList` → `01` seçip kanal modunda **uzun `*`** ile yalnızca röleleri
   tarayabilirsiniz.

> [!TIP]
> Bulduğunuz rölelerin sahibini, konumunu ve doğru tonunu yerel kulüpten veya TRAC'tan
> doğrulayın. Bir rölenin her zaman ton ile açılmadığını, bazılarının 1750 Hz istediğini unutmayın.

## 12.3 Havacılık bandını dinlemek

**Amaç**: Kule, yaklaşma ve uçak konuşmalarını dinlemek. **Belge gerekmez; gönderim yasaktır.**

1. **Güvenlik**: Gizli menüde `F Lock` ayarınızın havacılık bandına gönderime izin
   vermediğinden emin olun (`DEFAULT+` 108–137 MHz'i kapsamaz, ama `UNLOCK ALL` kapsar).
2. VFO: `1 1 8 0 0 0` (118,000) → `Mode` → **`AM`** → `Step` → **`25.00kHz`** (veya 8,33 kHz).
3. `SetRxA` ile AM profilini deneyin: `STOCK`, `SHARP` veya `OPEN`.
4. **Tarama aralığı**: VFO A = 118,000, VFO B = 137,000, uzun `5`, uzun `*`.
5. Aktif frekansları bulunca kanal olarak kaydedin (`Mode` = `AM` kanala da kaydedilir).
6. **ACARS** (Labs): 131,725 MHz AM → `F` + `7` → ACARS RX.

**İpuçları**

- Uçaklar yüksekte olduğundan çok uzaktan duyulur; kule yalnızca havalimanına yakınsanız duyulur.
- **ATIS** frekansı sürekli yayın yapar; anteninizi ve ayarlarınızı denemek için idealdir.
- 121,500 MHz (acil durum) genellikle sessizdir. Burada **asla** gönderim yapmayın.

## 12.4 ISS'i dinlemek ve resim almak

**Amaç**: Uluslararası Uzay İstasyonu'nun sesini veya SSTV resimlerini almak. **Belge gerekmez.**

1. **Geçişi öğrenin**: Bir uydu takip sitesinden veya uygulamasından konumunuza göre ISS
   geçiş saatlerini bulun. **Yüksek açılı** (40° ve üstü) geçişler en iyisidir.
2. **Etkinliği kontrol edin**: ISS'in ses yayını her zaman açık değildir. **ARISS SSTV**
   etkinlikleri önceden duyurulur.
3. **Ayar**: `1 4 5 8 0 0` (145,800) → FM, **`WIDE`**, squelch **0** veya **1**.
4. **Anten**: Uzun bir anten kullanın. Açık bir alana çıkın. Telsizi dik tutun ya da hafifçe
   uydunun yönüne eğin.
5. **Doppler**: Geçişin başında sinyal 145,8035 civarında, sonunda 145,7965 civarındadır
   (±3,5 kHz). Geniş FM bunu çoğunlukla tolere eder. Ses bozulursa adımı 2,5 kHz yapıp
   `UP`/`DOWN` ile takip edin.
6. **SSTV** (Labs): `F` + `7` → SSTV. Uygulama dinlemeye başlar. Resmin başlangıcındaki
   VIS kodu duyulduğunda resim satır satır çizilir. `2` ile `DITHER` seçmek fotoğraflarda
   daha iyi görüntü verir.
7. **APRS**: ISS'in digipeater'ı 145,825 MHz'dedir; APRS RX ile paketleri görebilirsiniz.

## 12.5 APRS paketlerini almak

**Amaç**: Çevrenizdeki APRS istasyonlarını görmek. **Belge gerekmez** (yalnızca alım).

1. VFO: `1 4 4 8 0 0` (144,800), FM, `WIDE`.
2. Labs: `F` + `7` → **APRS RX**.
3. Paketler geldikçe çağrı işareti, yol ve konum görünür. `UP`/`DOWN` ile 5 paket arasında gezin.
4. Çağrı işaretlerini **aprs.fi** gibi bir sitede aratarak haritada görebilirsiniz.

**Paket gelmiyorsa**: Bölgenizde APRS trafiği az olabilir. Yüksek bir yere çıkın,
daha uzun anten deneyin. Spektrumda (`F` + `5`) 144,800'de ara ara tepeler görmelisiniz.

## 12.6 Telefonla APRS (belgeli)

> [!IMPORTANT]
> Bu senaryo **gönderim** içerir. Yalnızca belgeli amatörler içindir.

1. **Profil**: APRS Edit ile çağrı işaretinizi, SSID'yi (ör. `-7`), konumunuzu (veya telefon
   konumu kullanılacaksa APRSdroid ayarlarını), sembolünüzü ve yorumunuzu girin.
2. **Ferrit**: USB kablosunun telsiz ucuna VHF ferriti takın.
3. **Bağlantı**: Telsiz → OTG adaptörü → telefon.
4. **Telsiz**: 144,800 MHz, FM, düşük güç ile başlayın. `F` + `7` → **KISS TNC**.
5. **APRSdroid**: Bağlantı türü TNC (KISS), USB serial. İzlemeyi başlatın.
6. **Test**: KISS TNC'de `2` ile RF'siz test paketi gönderin; APRSdroid'de görünmeli.
7. Konumunuz yayınlandıktan birkaç dakika sonra aprs.fi'de görünmelidir (bölgede iGate varsa).

## 12.7 Radyosonda avı

**Amaç**: Meteoroloji balonunun telemetrisini almak ve düştüğü yeri bulmak. **Belge gerekmez.**

1. **Hazırlık**: SondeHub gibi bir siteden bölgenizdeki sondaları, **frekanslarını** ve
   **tiplerini** (RS41, M10, M20…) öğrenin. Fırlatmalar genellikle 00 ve 12 UTC civarındadır
   (Türkiye saati 03:00 ve 15:00).
2. **Ayar**: Sonda frekansı, FM, **`WIDE`**.
3. **Uygulama** (Labs): `F` + `7` → sondanın tipine göre **Sonde RS41 / M10 / M20**.
4. Konum, irtifa ve hızlar ekranda görünür. Her geçerli çerçevede yeşil LED yanıp söner.
5. **Sinyal çok güçlüyse** (sonda yakın veya yere inmiş): `3` ile zayıflatıcıyı artırın.
6. **Frekans kayması**: Sondanın vericisi tam frekansta değilse `2` / `F` + `2` ile ±5 kHz deneyin.
7. **Bulmak için**: GeoNav ile yön ve mesafe; yakına gelince Sig Finder ile yön.

## 12.8 Deniz kenarında: AIS, kanal 16, DSC

**Amaç**: Gemi trafiğini izlemek. **Belge gerekmez; deniz kanallarında gönderim yasaktır.**

1. **Kanal 16**: `1 5 6 8 0 0` (156,800), FM, `WIDE`. Kanal kaydedin: `ChName` = `CH16`.
2. **AIS**: `1 6 1 9 7 5` (161,975) → `F` + `7` → **AIS RX**. Gemilerin adları ve konumları görünür.
3. **DSC**: `1 5 6 5 2 5` (156,525) → **ATIS DSC RX**.
4. **Dual Watch ile**: VFO A'da kanal 16, VFO B'de kanal 13 (156,650) → `RxMode` → `DUAL RX RESPOND`.
   (Gönderim yapmayacağınız için "RESPOND" önemli değildir; bu yüzden `F Lock` = `CE HAM`
   veya `DISABLE ALL` olmalıdır.)

## 12.9 Tilki avı (ARDF)

**Amaç**: Gizlenmiş bir vericiyi yön bulma ile bulmak. **Avcı olarak belge gerekmez;
verici koymak belge ister.**

### Avcı

1. **Anten**: Yönlü bir anten (şerit metre Yagi, HB9CV) şarttır. Stok antenle yön bulmak çok zordur.
2. **Frekans**: Organizatörün verdiği frekans (genellikle 2 m, ör. 144,500 civarı).
3. **Uygulama**: Fox Hunt (FieldOps/Labs) veya Sig Finder (Labs).
4. **Yön bulma**:
   - Anteni yatay veya dikey (vericinin polarizasyonuna göre) tutup yavaşça 360° dönün.
   - Sinyalin **en güçlü** olduğu yönü not edin (Sig Finder'da `0`, Fox Hunt'ta en yüksek dBm).
   - Yagi'de en güçlü yön **ön tarafıdır**; arka lob da sinyal verir, karıştırmayın.
5. **Yaklaştıkça**: Sinyal çok güçlenir ve her yönden gelmeye başlar. **Zayıflatıcıyı artırın**
   (Fox Hunt'ta `3`, Sig Finder'da otomatik). Gerekirse vücudunuzu kalkan olarak kullanın:
   telsizi göğsünüze yaslayıp dönün; sinyalin en zayıf olduğu yön, vericinin **arkanızda** olduğu yöndür.
6. **Üçgenleme**: Farklı noktalardan alınan yönleri haritada çizin; kesiştikleri yer vericinin konumudur.

### Organizatör (belgeli)

- Beacon ile her verici için `MOE`, `MOI`, `MOS`, `MOH`, `MO5` tanımlayıcısı seçin.
- Gönderim penceresi ve bekleme sürelerini birbiriyle çakışmayacak şekilde ayarlayın.
- Düşük güç (`LOW 1`–`LOW 3`) çoğu zaman yeterlidir. Telsizi kapalı bir kaba koymak menzili azaltır.

## 12.10 Acil durum için hazırlık

**Amaç**: Afette haberleşmeye hazır olmak.

1. **Bilgi toplayın**: Bölgenizdeki kulüplerin ve TRAC'ın acil durum frekanslarını, rölelerini
   ve toplanma kanallarını öğrenin.
2. **Kanal planı**: Bunları kanal olarak kaydedin ve ayrı bir tarama listesine (ör. `24`)
   atayın. Adlarını açıklayıcı verin (`ACIL 1`, `ROLE YEDEK`).
3. **Ayrı bir banka**: Multiconfig'de bir bankayı (ör. `CFG 4`) yalnızca acil durum için ayırın
   (bkz. [12.11](#1211-senaryolara-göre-multiconfig-bankaları)).
4. **Kâğıda yazın**: Kanal listesini yazdırıp telsizle birlikte saklayın.
5. **Güç**: Yedek pil, USB-C şarj için powerbank veya güneş paneli.
6. **Anten**: Katlanabilir veya uzun bir yedek anten; araç için mıknatıslı anten.
7. **Tatbikat**: Kulübünüzün tatbikatlarına katılın. Gerçek bir afette ilk kez denemek çok zordur.
8. **Resmî kurumlar**: Gerçek bir acil durumda **112** ve **AFAD** talimatları önceliklidir.

## 12.11 Senaryolara göre Multiconfig bankaları

Multiconfig, telsizi **farklı kullanım senaryoları** arasında saniyeler içinde değiştirmenizi sağlar.

| Banka | Senaryo | İçerik önerisi |
|-------|---------|----------------|
| `CFG M` | Günlük amatör | Yerel röleler, 145,500, 433,500, APRS. `RxMode` = `DUAL RX RESPOND` |
| `CFG 1` | Dağ / SOTA | Simpleks kanallar, uzak röleler, düşük güç varsayılanı, uzun `KeyLck` |
| `CFG 2` | Dinleme (havacılık, deniz) | AM havacılık kanalları, deniz kanalları. `F Lock` = `DISABLE ALL` |
| `CFG 3` | Tilki avı | Avın frekansları, yan tuşa `FOX HUNT` |
| `CFG 4` | Acil durum | Acil durum kanalları ve röleler, tarama listesi `24` |

**Geçiş**: `MENU` → `Channels` → `SetCfg` → banka → `MENU`. Durum çubuğunda `CM`, `C1`… görünür.

## 12.12 Telsizleri aynı ayarlara getirmek

| Yöntem | Ne aktarır? | Gerekenler |
|--------|-------------|------------|
| **CHIRP** | Kanallar ve birçok ayar | Bilgisayar, kablo, aynı sürümün CHIRP sürücüsü |
| **AirCopy** (Transfer, Labs) | 128 kanallık banka, ayarlar veya hepsi | İki telsiz, aynı firmware sürümü |
| **AirCopy kablo** (Transfer) | Aynı + `Flash 2M` (harici flash'ın tamamı, kalibrasyon hariç) | Telsizden telsize kablo |
| **BEAM** (Transfer, Labs) | Tek bir VFO'nun ayarları → alıcının ilk boş kanalı | İki telsiz, ortak frekans |

> [!TIP]
> Bir grup için telsiz hazırlıyorsanız: bir telsizi CHIRP ile hazırlayın, dosyayı kaydedin,
> diğerlerine aynı dosyayı yükleyin. Hızlı ve hatasızdır.

## 12.13 Bilinmeyen bir sinyalin ne olduğunu anlamak

1. **Spektrumda bakın** (`F` + `5`): Sinyal ne kadar geniş? Sürekli mi, patlamalı mı?
   - Dar ve sürekli → taşıyıcı veya dar bantlı veri
   - 12,5–25 kHz genişliğinde, aralıklı → FM ses veya veri
   - Çok geniş (200 kHz+) → yayın FM, TV veya güçlü parazit
2. **Dinleyin** (FM, sonra AM, sonra USB): [4.15'teki tabloyla](04-modulasyon-ve-sinyal-turleri.md#415-hangi-sinyal-nasıl-duyulur) karşılaştırın.
3. **Frekansına bakın**: [7. bölümdeki](07-frekans-rehberi.md) haritada hangi hizmete ait?
4. **Ses içeriğine bakın** (Labs): AF Spectro ile tonları görün.
   - 1200 / 2200 Hz → APRS / paket radyo
   - 1300 / 2100 Hz → DSC / ATIS
   - 697–1633 Hz arası çiftler → DTMF
   - 1500–2300 Hz süpürme → SSTV
   - Yükselip alçalan ton (≈ 300–1600 Hz) → 121,5 MHz işaretçi süpürmesi
5. **Uygun uygulamayı deneyin**: [11.12'deki tablo](11-uygulamalar.md#1112-hangi-iş-için-hangi-uygulama).

## 12.14 Belge aldıktan sonra ilk görüşme

> [!IMPORTANT]
> Gönderim içerir. Belgenizi ve çağrı işaretinizi aldıktan sonra.

1. `F Lock` = `CE HAM` olsun.
2. Tanıdığınız bir telsizciyle **simpleks** bir frekansta (ör. 145,375 / V30) buluşmak için
   önceden sözleşin.
3. **Düşük güçle** başlayın (`LOW 3`–`LOW 5`). Duyulmazsanız artırın.
4. Dinleyin, sonra:
   > "TA2XYZ, TA2XYZ, burası TA1ABC, beni duyuyor musun?"
5. Karşı taraftan **sinyal ve ses raporu** isteyin. Gerekirse `Mic` kazancını ayarlayın.
6. Sonra röleye çıkmayı deneyin ([9.8](09-cihaz-kullanimi.md#98-röle-kanalı-programlama-tam-örnek)).
7. Görüşmelerinizi tarih, UTC saat, frekans, karşı istasyon ve raporla birlikte kaydedin.

---

[← Önceki: Uygulamalar](11-uygulamalar.md) · [İçindekiler](README.md) · [Sonraki: Sözlük →](13-sozluk.md)
