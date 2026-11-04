# bklab — BK Lab için PC kabuğu ve Python API'si

Telsizde **BK Lab** açıkken BK4819 register'larını bilgisayardan okur, yazar,
izler ve tarar. `pyserial` ve `../uvterm/uvterm.py` gerekir.

```bash
python3 tools/bklab/bklab.py
```

| Kabuk komutu | Ne yapar |
|---|---|
| `r 13 [n]` | Oku: değer, 16 bit, ad |
| `w 13 03D9` / `w! 30 BFF1` | Yaz ve geri oku (`w!`: korumalı, verici açılabilir) |
| `d` | 128 register'ın hepsi, bitleri ve adlarıyla |
| `s` | RSSI (0.5 dB), gürültü, glitch |
| `m 67 [ms]` | Bir register'ı izle (Ctrl+C) |
| `tara 4F 0400 0A00 100 200` | 0x4F'e 0400'den 0A00'e 100'er adımla yaz, her birinde 200 ms bekleyip RSSI/gürültü/glitch oku, sonra eski değeri geri yaz |
| `kaydet dosya.txt` | Dökümü dosyaya |
| `geri` | Bu oturumda yazılanları açılış değerlerine döndür |

Ayrıca:

```bash
python3 tools/bklab/bklab.py betik deneme.txt
```

```bash
python3 tools/bklab/bklab.py fark once.txt sonra.txt
```

`betik` bir dosyadaki kabuk komutlarını sırayla çalıştırır; `fark` iki
dökümü karşılaştırır ve değişen bitleri gösterir (ör. bir menü ayarını
değiştirmeden önce ve sonra döküm alıp hangi register'a dokunduğunu bulmak).

Python'dan:

```python
import sys; sys.path.insert(0, "tools/bklab")
from bklab import BK
bk = BK.open()
print(hex(bk.read(0x13)), bk.status())
for v, s in bk.sweep(0x13, 0x03D0, 0x03DF):
    print(hex(v), s["rssi"])
bk.restore(); bk.close()
```

```bash
python3 tools/bklab/test_bklab_pc.py
```
