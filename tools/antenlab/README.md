# antenlab — Anten Lab için PC aracı

Telsizdeki **Anten Lab** ölçümünü bilgisayara alır, kutupsal diyagramı SVG
olarak çizer (tarayıcıda açılır, ek kütüphane gerekmez) ve antenleri
karşılaştırır. `al` için `pyserial` ve `../uvterm/uvterm.py` gerekir.

| Komut | Ne yapar |
|---|---|
| `python3 antenlab.py al yagi.csv` | Telsizden ölçümü (ve referansı) alır → `yagi.csv` + `yagi.svg`, sayıları yazar |
| `python3 antenlab.py ciz a.csv b.csv -o kars.svg --baslik "2 m Yagi"` | Birden çok CSV'yi aynı dB ölçeğinde üst üste çizer, her biri için tepe / ön-arka / hüzme |
| `python3 antenlab.py ozet a.csv` | Sayılar: tepe yönü, seviye, ön/arka, −3 dB hüzme |

Sayılar telsizdekiyle aynı yöntemle hesaplanır (tepe = −3 dB noktalarının
ortası, ara değerleme). CSV biçimi: `derece,dBm,ref_dBm`, 36 satır.

```bash
python3 tools/antenlab/test_antenlab_pc.py
```
