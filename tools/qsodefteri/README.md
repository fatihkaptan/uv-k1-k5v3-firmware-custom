# qsodefteri — QSO Defteri için PC aracı

Telsizdeki **QSO Defteri**'nin saatini ayarlar, defteri alır ve logger
programlarının okuduğu **ADIF 3.1.4** dosyası yazar. `pyserial` ve
`../uvterm/uvterm.py` gerekir.

| Komut | Ne yapar |
|---|---|
| `python3 qsodefteri.py saat` | Telsizin UTC saatini bu bilgisayardan ayarlar (sahaya çıkmadan önce) |
| `python3 qsodefteri.py al defter.adi --cagri TA2XX --kare KN50TR` | Saati ayarlar, defteri alır → `defter.adi` + `defter.csv` |
| `… al defter.adi --temizle [-y]` | Aktardıktan sonra telsizdeki defteri boşaltır (sorar; `-y` sormaz) |
| `python3 qsodefteri.py adif defter.csv defter.adi` | Kaydedilmiş CSV'den yeniden ADIF |
| `--zamansiz "2026-11-04 14:00"` | Saatsiz kaydedilen QSO'lara verilecek UTC zaman |

ADIF alanları: `CALL`, `QSO_DATE`, `TIME_ON`, `FREQ` (MHz), `BAND` (ADIF bant
tablosundan: 2m, 70cm, 6m …), `MODE` (SSB ise `SUBMODE` USB), `RST_SENT`,
`RST_RCVD`; verilirse `STATION_CALLSIGN` ve `MY_GRIDSQUARE`.

```bash
python3 tools/qsodefteri/test_qsodefteri_pc.py
```

10 kontrol: bantlar, ADIF alanları (uzunluklar bayt cinsinden), SSB alt modu,
saatsiz QSO'lar, ve QSO Defteri uygulamasına sanal seri porttan canlı
bağlanıp saat ayarlama, alma, boşaltma.
