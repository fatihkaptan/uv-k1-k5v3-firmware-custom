# 14. Sorun Giderme ve Sık Sorulan Sorular

[← Önceki: Sözlük](13-sozluk.md) · [İçindekiler](README.md)

Belirtiye göre düzenlenmiş sorun giderme tabloları ve sık sorulan sorular.

## İçindekiler

1. [Alım sorunları](#141-alım-sorunları)
2. [Gönderim sorunları](#142-gönderim-sorunları)
3. [Röle sorunları](#143-röle-sorunları)
4. [Tuş, menü ve ekran sorunları](#144-tuş-menü-ve-ekran-sorunları)
5. [Pil ve güç sorunları](#145-pil-ve-güç-sorunları)
6. [Tarama ve spektrum sorunları](#146-tarama-ve-spektrum-sorunları)
7. [Uygulama sorunları (Labs)](#147-uygulama-sorunları-labs)
8. [Bilgisayar bağlantısı sorunları](#148-bilgisayar-bağlantısı-sorunları)
9. [Sık sorulan sorular](#149-sık-sorulan-sorular)

---

## 14.1 Alım sorunları

| Belirti | Olası sebep | Çözüm |
|---------|-------------|-------|
| Hiçbir şey duyulmuyor, hışırtı da yok | Ses kısık, `MUTE` açık, `SetVol` düşük | Ses düğmesini açın; `MUTE`'u kapatın; `SetVol`'u artırın |
| Hışırtı duyuluyor ama sinyal yok | Frekans yanlış veya kimse konuşmuyor | Spektrumda (`F` + `5`) sinyal arayın |
| Sinyal var (S-metre oynuyor) ama ses yok | `RxCTCS` / `RxDCS` yanlış bir değerde | `RxCTCS` ve `RxDCS`'yi `OFF` yapın; gerekirse `F` + `*` ile tonu bulun |
| Sinyal var ama squelch açılmıyor | Squelch çok yüksek | `F` + `DOWN` ile squelch'i düşürün veya `MONITOR` kullanın |
| Sürekli hışırtı, squelch kapanmıyor | Squelch 0 veya yakında parazit | Squelch'i 3–4'e çıkarın; parazit kaynağını (adaptör, bilgisayar) uzaklaştırın |
| Ses yüksek, bozuk, cızırtılı | Karşı taraf geniş FM, siz dar FM'desiniz | `W/N` → `WIDE` |
| Ses kısık ve uzak | Karşı taraf dar FM, siz geniş FM'desiniz | `W/N` → `NARROW` |
| Ses "ördek gibi", anlaşılmıyor | AM veya SSB sinyali FM'de dinleniyor (veya tersi) | `Mode`'u değiştirin (havacılık: `AM`) |
| Havacılık bandında çok parazit, hayalet sinyaller | Alıcı yakındaki güçlü vericilerle doyuyor | Uzaklaşın, daha dar bantlı anten deneyin, spektrumda `LNA`/`PGA`'yı düşürün |
| Olmaması gereken frekanslarda sinyal | İntermodülasyon, imaj veya harmonik | [2.10](02-radyo-dalgalari-ve-spektrum.md#210-parazit-türleri-harmonik-imaj-intermodülasyon-doyma) |
| Uzak istasyonlar duyulmuyor | Anten, yükseklik, engeller | Yükseğe çıkın, uzun anten veya kaplan kuyruğu deneyin |
| Sinyal yürürken hızla gidip geliyor | Çok yollu yayılım ("çit kazığı") | Normaldir; birkaç adım ilerleyip durun |
| İki VFO'dan biri yayının başını kaçırıyor | Çift dinlemenin doğası | Önemli kanalı ana VFO yapın veya `MAIN ONLY` |
| Yaz aylarında çok uzak röleler duyuluyor | Troposferik kanal | Doğa olayı; arıza değil |

## 14.2 Gönderim sorunları

| Belirti | Olası sebep | Çözüm |
|---------|-------------|-------|
| `TX DISABLE` | Frekans `F Lock` bölgesinin dışında | Frekansı kontrol edin; belgeliyseniz `F Lock` = `CE HAM` amatör bantları kapsar |
| `TX DISABLE` (doğru frekansta) | Bilgisayardan ayar aktarımı sürüyor | Bağlantıyı bitirip tekrar deneyin |
| `BUSY` | `BusyCL` açık ve kanal meşgul | Kanalın boşalmasını bekleyin veya `BusyCL`'yi kapatın |
| `BAT LOW` | Pil çok düşük | Şarj edin |
| `VOLT HIGH` | Gerilim 8,9 V'un üstünde | Pili, şarj cihazını ve `BatCal` ayarını kontrol edin |
| `TIMEOUT` | `TxTOut` süresi doldu | `PTT`'yi bırakıp tekrar basın; gerekirse süreyi uzatın |
| `PTT`'ye basınca hiçbir şey olmuyor | Tuş kilidi `PTT`'yi de kapsıyor (`SetLck`) | Uzun `F` ile kilidi açın |
| Bırakmama rağmen gönderim sürüyor | `SetPTT` = `ONEPUSH` | `PTT`'ye bir kez daha basın; isterseniz `CLASSIC`'e alın |
| Kendi kendine gönderime geçiyor | VOX açık | Uzun `7` veya `VOX` menüsüyle kapatın; VOX seviyesini yükseltin |
| Karşı taraf beni kısık duyuyor | Mikrofon kazancı düşük; telsiz ağızdan uzak | `Mic`'i artırın; 5–10 cm'den konuşun |
| Karşı taraf beni bozuk duyuyor | Mikrofon kazancı yüksek, bağırıyorsunuz, `W/N` uyumsuz | `Mic`'i azaltın; normal sesle konuşun; `W/N`'yi kontrol edin |
| İlk hecem kayboluyor | Röle/ton çözücü açılmadan konuşuyorsunuz | `PTT`'den sonra 1 saniye bekleyin |
| Gönderimde telsiz kapanıyor/yeniden başlıyor | Eski pil, düşük gerilim, gevşek pil kontakları | Pili şarj edin veya değiştirin; kontakları temizleyin |
| USB bağlıyken gönderimde bağlantı kopuyor | Kablo RF topluyor | Kabloya ferrit takın, gücü azaltın, anteni kablodan uzaklaştırın |

## 14.3 Röle sorunları

| Belirti | Kontrol |
|---------|---------|
| Röleyi duyuyorum ama açamıyorum | `TxCTCS` değeri; `TxODir` yönü (`-`); `TxOffs` (0,600); güç; mesafe; röle 1750 Hz istiyor olabilir |
| Röle açılıyor ama hemen kapanıyor | Ton doğru değil veya sinyaliniz röleye zayıf ulaşıyor |
| Röle hiç duyulmuyor | Çıkış frekansı doğru mu? `RxCTCS` yanlış değerde olabilir; kapatın |
| Röle kendi kendine kesiliyor | Rölenin zaman aşımı; daha kısa konuşun |
| Gönderirken ekranda yanlış frekans görünüyor | `TxODir` / `TxOffs` ters; ya da `R` (reverse) açık: uzun `8` ile kapatın |

## 14.4 Tuş, menü ve ekran sorunları

| Belirti | Olası sebep | Çözüm |
|---------|-------------|-------|
| "Long press # to unlock" | Tuş takımı kilitli | Uzun `F` (`#`) |
| Tuşlar kendiliğinden kilitleniyor | `KeyLck` (otomatik kilit) açık | `KeyLck` → `OFF` veya daha uzun süre |
| `MENU` ile menüye girilemiyor | Rescue Ops kilidi açık (durum çubuğunda `RO`) | Telsizi `PTT` + gizli tuş (`SetKey`, varsayılan `MENU`) ile açın |
| Menüde `F Lock`, `BatTyp`, `SetNav`, `Reset` yok | Gizli menü kapalı | Telsizi `PTT` + `SIDE1` basılı tutarak açın |
| Bazı menü öğeleri yok | Sürümünüzde derlenmemiş | Sürümünüzü `SysInf`'ten kontrol edin ([8.1](08-cihaz-donanimi-ve-ekran.md#81-firmware-sürümleri-edition)) |
| `UP`/`DOWN` ters çalışıyor | `SetNav` modelinize uygun değil | Gizli menüde `SetNav`'ı değiştirin |
| `F` + `7` uygulama menüsünü açmıyor, VOX açıp kapatıyor | Sürümünüz uygulama içermiyor | Labs sürümünü kullanın |
| Ekran çok soluk veya çok koyu | Kontrast | `SetCtr` |
| Ekran ters renkte | `SetInv` açık | `SetInv` → `OFF` |
| Arka ışık hemen sönüyor / hiç sönmüyor | `BLTime` ayarı veya `F` + `8` ile elle ayar | `BLTime`'ı ayarlayın; `F` + `9` ile normal davranışa dönün |
| Ekranda bir logo/animasyon var, tuşa basınca kayboluyor | Ekran koruyucu (`SetSav`) | Normal; isterseniz `SetSav` → `OFF` |
| Kanal yerine frekans görünüyor | VFO modundasınız veya `ChDisp` = `FREQ` | `F` + `3`; `ChDisp` |
| Spektrum açılışta kendiliğinden açılıyor | Telsiz spektrumdayken kapatılmış | Spektrumdan `EXIT` ile çıkıp sonra kapatın |

## 14.5 Pil ve güç sorunları

| Belirti | Olası sebep | Çözüm |
|---------|-------------|-------|
| Pil yüzdesi hızlı düşüyor veya tutarsız | Yanlış `BatTyp` | Gizli menüde doğru pil tipini seçin |
| Ekrandaki gerilim yanlış | Kalibrasyon | Multimetreyle ölçüp `BatCal` ile eşitleyin |
| Pil çabuk bitiyor | Yüksek güç, uzun arka ışık, sürekli tarama, pil tasarrufu kapalı | `Power`, `BLTime`, `BatSav`, `SetOff` |
| Telsiz kendi kendine kapanıyor | `SetOff` (derin uyku) | Süreyi uzatın veya `OFF` |
| USB-C ile şarj olmuyor | Pil USB-C şarjını desteklemiyor, kablo/adaptör uygun değil | Şarj tabanını deneyin; farklı kablo kullanın |

## 14.6 Tarama ve spektrum sorunları

| Belirti | Olası sebep | Çözüm |
|---------|-------------|-------|
| Tarama hiç durmuyor | Squelch çok yüksek | Squelch'i düşürün |
| Tarama sürekli aynı gürültülü frekansta duruyor | Parazit kaynağı | Uzun `MENU` ile o frekansı/kanalı hariç tutun |
| Tarama bazı kanalları atlıyor | Kanal listesi `OFF` veya `EX` | Uzun `5` ile listeye ekleyin / hariç tutmayı kaldırın |
| Kanal taraması başlamıyor | Seçili liste boş | `ScList`'i değiştirin; kanallara liste atayın |
| Frekans taraması sinyalleri atlıyor | Adım, kanal aralığından büyük | `Step`'i 12,5 veya 25 kHz yapın |
| Tarama aralığı yerine bütün bant taranıyor | `ScnRng` açık değil | VFO modunda uzun `5` |
| Spektrumda bütün grafik yükseliyor | Güçlü sinyal alıcıyı doyuruyor | STILL modunda `LNA`/`PGA`'yı düşürün; uzaklaşın |
| Spektrumda dar sinyaller görünmüyor | Tarama adımı çok büyük | `1`/`7` ile adımı küçültün |

## 14.7 Uygulama sorunları (Labs)

| Belirti | Olası sebep | Çözüm |
|---------|-------------|-------|
| `NOT SUPPORTED` | Uygulama ile firmware sürümü uyumsuz | Firmware ile **aynı sürümün** uygulama paketini yükleyin |
| `No callsign` (APRS TX) | Profilde ve açılış mesajında geçerli çağrı işareti yok | APRS Edit ile çağrı işaretini girin |
| `TX OFF` | Frekans yasak, pil düşük/yüksek veya VFO FM değil | Ayarları kontrol edin |
| `No APRS Edit` | APRS Edit yüklü değil | UV Studio ile yükleyin |
| Veri uygulaması hiç çözmüyor (`WAIT` kalıyor) | Yanlış frekans, mod veya bant genişliği; zayıf sinyal | Modu (FM/AM) ve `W/N`'yi kontrol edin; sondalarda `WIDE`; frekansı ±5 kHz kaydırmayı deneyin |
| Sonda yakınken çerçeve gelmiyor | Alıcı doyuyor | Zayıflatıcıyı artırın (`3`) |
| KISS TNC bağlantısı gönderimde kopuyor | USB kablosu RF topluyor | Ferrit takın, gücü azaltın |
| Uygulama ayarları kayboldu | Uygulama açıkken telsiz kapatıldı | Uygulamadan her zaman `EXIT` ile çıkın |

## 14.8 Bilgisayar bağlantısı sorunları

| Belirti | Olası sebep | Çözüm |
|---------|-------------|-------|
| UV Studio seri portu göstermiyor | Tarayıcı Web Serial desteklemiyor | Chrome, Edge, Brave, Opera veya Firefox 151+ kullanın |
| Port görünüyor ama bağlanmıyor | Başka bir program (CHIRP) portu kullanıyor | Diğer programı kapatın |
| Kablo ile bağlanmıyor | Kablo yalnızca şarj kablosu; jak tam oturmamış | Veri destekli USB-C kablo kullanın; programlama kablosunun jaklarını sonuna kadar itin |
| CHIRP telsizi tanımıyor | Doğru sürücü yüklenmemiş | Firmware ile aynı sürümün CHIRP sürücüsünü **Load Module** ile yükleyin |
| Firmware yükleme yarıda kesildi | Bağlantı koptu | Telsizi yeniden DFU moduna alıp yüklemeyi tekrarlayın |

## 14.9 Sık sorulan sorular

**Bu telsizle belgesiz konuşabilir miyim?**
Hayır. Amatör bantlarda gönderim için BTK belgesi gerekir. PMR446 lisanssızdır ama yalnızca
tip onaylı, sabit antenli ve 0,5 W'lık cihazlarla; UV-K5/K1 bu şartları karşılamaz.
Belgeniz yoksa `F Lock` = `DISABLE ALL` yapıp telsizi alıcı olarak kullanın.

**Telsizin menzili ne kadar?**
Güçten çok **yükseklik ve araziye** bağlıdır. Düz arazide iki el telsizi arasında birkaç km–10 km;
yüksek bir tepedeki röle ile 50–100 km'ye kadar. Bkz. [5.10](05-antenler-ve-yayilim.md#510-radyo-ufku-ve-görüş-hattı).

**Daha yüksek güç neden pek fark etmiyor?**
1 W'tan 5 W'a çıkmak yalnızca +7 dB'dir: yaklaşık bir S birimi. İyi bir anten veya birkaç
metre yükseklik çoğu zaman daha büyük fark yaratır. Bkz. [3.2](03-desibel-ve-sinyal-olcumu.md#32-akılda-tutulacak-db-kuralları).

**Hangi anteni almalıyım?**
Stok antenden daha uzun, çift bantlı (2 m / 70 cm) kaliteli bir el telsizi anteni başlangıç için
yeterlidir. Konnektör tipini (SMA erkek/dişi) kontrol edin. Evde J-pole veya toprak düzlemli
anten büyük fark yaratır.

**Firmware'i yüklersem telsizi bozar mıyım?**
Risk düşüktür ama sıfır değildir. Önyükleyici firmware tarafından değiştirilmediği için çoğu
hatalı yükleme yeniden yüklemeyle düzelir. **Kalibrasyon yedeğinizi** mutlaka alın.

**Orijinal firmware'e dönebilir miyim?**
Evet. Önce **kalibrasyon yedeğinizi geri yükleyin**, sonra üreticinin firmware'ini yükleyin.

**Labs mı Fusion mı?**
Günlük kullanım için **Fusion**. APRS, uydu, sonda, CW gibi uygulamalar istiyorsanız **Labs**.
Multiboot sayesinde ikisini de telsizde tutup açılışta `MENU` ile seçebilirsiniz.

**DMR, D-STAR veya TETRA dinleyebilir miyim?**
Hayır. Bu dijital sistemler özel ses kodlayıcıları gerektirir; bu telsizde yalnızca gürültü
olarak duyulur. Bkz. [4.9](04-modulasyon-ve-sinyal-turleri.md#49-çözülemeyen-dijital-sistemler).

**Kanallarımı nasıl yedeklerim?**
CHIRP ile telsizden indirip dosya olarak kaydedin. AirCopy ile başka bir telsize de kopyalayabilirsiniz.

**`TXLock` nedir, kapatmalı mıyım?**
Kapatmayın. `ON` iken telsiz `F Lock` dışındaki frekanslarda gönderim yapmaz. `OFF` yapılırsa
o kanal bölge kilidini aşar.

**Telsizi nereden öğrenmeye başlamalıyım?**
[README.md](README.md) dosyasındaki okuma sırasını izleyin. Önce dinleyin, sonra yerel bir
kulübe katılıp sınava hazırlanın.

---

[← Önceki: Sözlük](13-sozluk.md) · [İçindekiler](README.md)
