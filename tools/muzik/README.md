# muzik — Müzik Kutusu için PC aracı

`muzik.py`, telsizde **Müzik Kutusu** açıkken telsizin hoparlörünü
bilgisayardan bir MIDI çalgısı gibi kullanır. Tek dosya; MIDI okuma/yazma saf
Python (ek kütüphane gerekmez), port için `uvterm.py`'yi (`../uvterm`) kullanır.

```bash
pip install pyserial
```

| Komut | Ne yapar |
|---|---|
| `python3 muzik.py cal sarki.mid` | MIDI dosyasını çalar: her an çalan **en tiz nota** melodi olur, 10. kanal (davul) atlanır |
| `… cal sarki.mid --hiz 1.2 --transpoze -12 --kanal 2` | Hız çarpanı, yarım ses kaydırma, yalnız bir kanal (`--davul` davulu da katar) |
| `python3 muzik.py klavye` | Bilgisayar klavyesi piyano: `a s d f g h j k l` = do re mi fa sol la si do re, `w e t y u o p` diyezler, `z`/`x` oktav, `q` çıkış |
| `python3 muzik.py canli` | USB **MIDI klavye** → telsiz (son basılı tuş çalar). `pip install mido python-rtmidi` gerekir; `--liste` girişleri gösterir, `--giris AD` seçer |
| `python3 muzik.py kaydet benim.mid` | Telsizin **Piyano**'sunda çaldıklarınızı `.mid` dosyasına kaydeder (Ctrl+C ile bitir) |
| `python3 muzik.py bilgi sarki.mid` | Dosyadaki kanallar, nota sayısı, süre |
| `python3 muzik.py gom sarki.mid --baslik "Ad"` | MIDI'nin melodisini uygulamaya **şarkı olarak gömer**: `App/apps/muzikkutusu/sarkilar/kendi.txt` (git'e girmez). Sonra `./compile-app.sh muzikkutusu` ile derleyip yükleyin. `--bas`/`--sure` saniye cinsinden bir bölüm seçer; `--kanal`, `--transpoze`, `--hiz`, `--bpm`, `--makam` (üstte görünen etiket) de var. 1/16'dan kısa susları önceki notaya katar (uygulama notaları zaten ayırır; `--suslar` hepsini korur). Aynı başlık eskisinin yerine yazılır; uygulamanın sınırında (255 nota, 15 perde, 16 uzunluk) kesip söyler |
| `python3 symbtr2kutu.py SymbTr/txt` | SymbTr veritabanından türküleri (53-TET koma) uygulamanın `sarkilar/turkuler.txt` biçimine çevirir |

Port otomatik bulunur; gerekirse `-p COM5` / `-p /dev/ttyACM0`.

Telsiz tek sesli olduğu için akorlarda yalnızca en üst nota duyulur;
melodisi üst seste olan parçalar (piyano eşlikli şarkılar, marşlar, türküler)
en iyi sonucu verir. Melodi alt bir kanaldaysa `--kanal` ile seçin.

## Protokol

Satır başına bir komut, iki yönde de aynı: `n<MIDI nota>` (60 = do4,
69 = la4 440 Hz) notayı başlatır, `x` susturur. Kendi programınızdan da
gönderebilirsiniz:

```python
import serial, time
s = serial.Serial("/dev/ttyACM0")
for n in (60, 64, 67, 72):
    s.write(f"n{n}\r\n".encode()); time.sleep(0.3)
s.write(b"x\r\n")
```

## Testler

```bash
python3 tools/muzik/test_muzik_pc.py
```

18 kontrol: MIDI okuyucu (çalışan durum, çok iz, tempo değişimi, sysex,
davul, RIFF kabuklu `.rmi`), akordan melodi, yazıcı (gidiş-dönüş), zamanlı gönderme, kayıt,
`gom` (1/32 ızgara, oktav katlama, uygulamanın kendi ayrıştırıcısıyla geri
okuma, aynı başlığın değiştirilmesi, perde sınırında kesme, bölüm seçme,
kısa susların notaya katılması) ve
bilgisayar için derlenmiş Müzik Kutusu uygulamasına sanal seri port
üzerinden **gerçek zamanlı uçtan uca** çalma. Gerçek telsiz ve MIDI klavye ile
henüz denenmedi.
