# uvterm — USB Term için PC terminali

`uvterm.py`, telsizdeki **USB Term** overlay uygulamasının
(`App/apps/usbterm/`) bilgisayar tarafıdır. Tek bir Python dosyasıdır;
Windows, Linux ve macOS'ta çalışır.

```bash
pip install pyserial
```

| Komut | Ne yapar |
|---|---|
| `python3 uvterm.py` | Telsizle sohbet (telsizde F+7 → USB Term açık olmalı) |
| `python3 uvterm.py --log sohbet.txt` | Sohbeti dosyaya da yazar |
| `python3 uvterm.py send "metin"` | Bir (veya birkaç) satır gönderip çıkar |
| `python3 uvterm.py ports` | Seri portları listeler, telsizi işaretler |
| `python3 uvterm.py apps` | Telsizde yüklü overlay uygulamalarını listeler |
| `python3 uvterm.py install X.app` | `.app` dosyasını telsize yükler (`--slot N`, `-y`) |

Telsiz otomatik bulunur (USB VID:PID `36B7:FFFF`); başka bir port için
`-p COM5` ya da `-p /dev/ttyACM0` ekleyin.

Sohbette: yazıp Enter → telsizin ekranına gider. Telsizde yazılıp `MENU` ile
gönderilen satırlar yeşil `TELSİZ>` ile görünür. `/info`, `/ping`, `/beep`,
`/clear` telsize gider; `/send dosya.txt`, `/help`, `/quit` yereldir.

`apps` ve `install` telsiz **ana ekrandayken** (bir uygulamanın içinde
değilken) çalışır; firmware'in kendi seri protokolünü kullanır ve yalnızca
harici flash'taki uygulama slotlarına yazar.

Ayrıntılı kullanım: [`App/apps/usbterm/README.md`](../../App/apps/usbterm/README.md) ·
Labs uygulama kılavuzu: [`App/apps/LABS_UYGULAMA_KILAVUZU.md`](../../App/apps/LABS_UYGULAMA_KILAVUZU.md)

Testler (telsiz gerekmez):

```bash
python3 tools/uvterm/test_uvterm.py
```
