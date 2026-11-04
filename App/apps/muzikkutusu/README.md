# Müzik Kutusu 1.0 — telsizin hoparlöründe melodi, piyano ve MIDI

**Müzik Kutusu**, telsizin hoparlörünü tek sesli bir çalgıya çevirir:
hazır melodiler, tuş takımıyla **piyano** (tuş basılı kaldıkça nota uzar),
**kayıt** (kapatıp açınca kaybolmaz) ve USB üzerinden bilgisayardan
**MIDI**: `.mid` dosyası çalma, MIDI klavyeyle canlı çalma, telsizde
çaldığınızı `.mid` olarak kaydetme ([`tools/muzik/muzik.py`](../../../tools/muzik/README.md)).

Telsiz **hiçbir şey yayınlamaz**: ses yalnızca hoparlörden çıkar (amatör
bantlarda müzik yayını yasaktır).

![Müzik Kutusu ekranları](images/muzikkutusu-ekranlar.png)

*(Menü, melodi listesi, çalar, piyano — test düzeneğinin çizdiği taklitler: `test/test_muzik.py`.)*

## Bölümler

| | |
|---|---|
| **1 Melodiler** | 8 melodi: Daha Dün Annemiz, Neşe Marşı, Für Elise, İyi ki Doğdun, Jingle Bells, Tembel Çocuk, Menuet (Sol majör), CQ CQ (Mors). Çalarken: başlık, çalan nota ve BPM, ilerleme çubuğu, klavyede çalan tuş. `UP`/`DOWN` tempo (%50–%200). |
| **2 Piyano** | Tuş takımı iki oktavlık bir klavye: `1`–`0` = do re mi fa sol la si do re mi, `*` sonraki notayı diyez yapar, `UP`/`DOWN` oktav (3–6). Ekranda notanın adı (büyük), frekansı, oktav ve tuş numaralı klavye. |
| **Kayıt** | Piyanoda `MENU` kaydı başlatır/bitirir (notalar ve aradaki sessizlikler, 20 ms çözünürlük, 255 olay). `F` kaydı çalar. Çıkışta saklanır, sonraki açılışta geri gelir. |
| **3 Ses** | 5 seviye (`###..`), her basışta bir örnek nota. |
| **USB** | Bilgisayardan `n<nota>` (MIDI numarası, 60 = do4) çalar, `x` susturur; menüdeyken piyano ekranı açılır. Piyanoda çalınan notalar bilgisayara aynı biçimde gider. |

Melodiler kamu malıdır (geleneksel ya da 100 yılı aşkın eserler). Kendi
melodinizi `gen_assets.py` içindeki `SONGS` listesine metinle ekleyin:
`"C4/4 D#4/2 R/1"` = nota + oktav, `/` sonrası on altılık cinsinden süre,
`R` sus. Örneğin Bolu türkülerinizi buraya yazıp yeniden derleyebilirsiniz.

## Kurulum

- F4HWN **Labs** v6.3.0+ (API 3, `serial` yeteneği).
- Hazır dosya: [`prebuilt/MuzikKutusu.app`](prebuilt/MuzikKutusu.app).

```bash
python3 tools/uvterm/uvterm.py install App/apps/muzikkutusu/prebuilt/MuzikKutusu.app
```

**F + 7** → Apps → **Muzik Kutusu**.

## Tuşlar

| Yer | Tuş | İşlev |
|---|---|---|
| Menü | `1`–`3`, `UP`/`DOWN` + `MENU` | Bölüm seç; `3` sesi bir kademe artırır |
| | `EXIT` | Çıkış |
| Melodiler | `UP`/`DOWN` | Melodi seç; çalarken tempo |
| | `MENU` ya da `1`–`8` | Çal / dur |
| | `EXIT` | Dur, sonra menü |
| Piyano | `1`–`0` | Nota (basılı tuttukça çalar) |
| | `*` | Sonraki nota diyez (durum çubuğunda `#`) |
| | `UP`/`DOWN` | Oktav |
| | `MENU` | Kayıt başlat / bitir (`REC`) |
| | `F` | Kaydı çal / durdur (`CAL`) |
| | `EXIT` | Menü |

## Nasıl çalışıyor

- Ses, firmware'in kendi bip yolu: `prepare_tone` (ton üretecini ve
  hoparlör yolunu hazırlar), REG_71'e notanın frekansı, REG_50 susturucusu
  `tx_mute` ile açılıp kapanır. Engellemeyen bu kullanım sayesinde notalar
  zamanında başlar, istenen kadar sürer; 2 s sessizlikte amfi kapanır.
  (Firmware'in `play_tone` servisi süre boyunca bekler; piyano için uygun değil.)
- Ton tablosu (do3–do7) `gen_assets.py` içinde firmware'in `scale_freq()`
  formülüyle hesaplanır.
- Melodi notaları %12.5 erken kesilir (art arda aynı notalar ayrı duyulsun).
- **Kalıcı kayıt:** uygulama `--save-screen` bayrağıyla paketlenir. Çıkışta
  kaydı durum çubuğu ve ekran tamponuna (1024 B) yazar; yükleyici bu
  tamponları varlıkların son 1024 baytına saklar, sonraki açılışta uygulama
  `asset_read` ile geri okur. Kayıt yoksa da boş bir blok yazılır (yoksa ekran
  görüntüsü kayıt sanılırdı).
- Kod 3564 B (4096 B overlay), varlıklar 2185 B (1024'ü kayıt alanı).

## Derleme ve testler

```bash
./compile-app.sh muzikkutusu
```

```bash
python3 App/apps/muzikkutusu/test/test_muzik.py
```

Test, çalınan notaları BK4819 yazmalarından (REG_71 = perde) ve susturucu
anahtarlamasından (başlangıç/bitiş, ms) yeniden kurar: ilk üç melodinin her
notası perde ve ±15 ms zamanlamayla, diğerleri sırayla doğrulanır; tempo,
basılı tutulan tuş süreleri, diyez, oktav sınırları, kayıt ve çalma, **yeniden
başlatmadan sonra kaydın geri gelmesi** (yükleyicinin sakladığı blok taklit
edilerek), USB `n`/`x` protokolü, ses seviyesi ve amfinin kapanması (28 kontrol).
Gerçek telsizde henüz denenmedi.
