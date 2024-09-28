# Lampi

**Hætt við þetta, RP2040 notaður. Sjá `main` branch.**

Þetta er fyrri ítrun, þar sem notast var við Seeed Xiao ESP32C3.


## Markmið

Búa til snjalllampa til að nýta til kennslu í Fab Lab. 

## Samsetning

TODO: 
- Uppfæra bretti
- Mynd af tengingum
- Lóðningar
- Samsetning á PCB & prentuðum hlutum. 

## Íhlutir

- ESP32C3
- Neopixel hringur (12LED, RGBW)
- 3 vírar, notaði jumpera og klippti endana af öðru megin
- 3 pinnar (e. _headers_) til að tengja jumperana. 

- 3D prentaðir hlutir:
    - Hólkur
    - Sæti fyrir Neopixel (toppur)
    - Sæti fyrir ESP32C3 (botn)
    - Spöng til að halda ESP32C3

## Uppsetning (VSCode & PlatformIO)

- Setja upp Visual Studio Code
- Setja up PlatformIO
   - Viðbót fyrir [VScode](https://docs.platformio.org/en/latest/integration/ide/vscode.html)
- Opna þetta repo með [platformIO](https://platformio.org/)
- Laga línu í `AsyncWebSocket.cpp` [sjá neðar](https://github.com/hanndoddi/Lampi/tree/main#villa-%C3%AD-aspasyncwebserver)
- Ýta á `Build` sem býr til ýmsar skrár
- Framkvæma þessi skref:
    1. Build filesystem Image
    2. Upload filesystem Image
    3. Upload and monitor

| ![Skref](myndir/skref.jpg) | 
|:--:| 
| *Skref* |

## TODO: 

- _Útbúa verkefnalýsingu og efni fyrir rafmagns/forritunarnámskeið_
- Endurskrifa rútur (e. _routes_) með AJAX til að 
    - Slóð í vafra haldist eins
    - Nótera endanlega API punkta
- Fjarlægja FABXIAO led úr kóða/viðmóti
- Prófa "flottur.lampi" með mdns
- Fjarlægja .vscode úr sögunni
- Gera mismunandi útgáfur af kúplum
    - [x] Vacuum formaðan
    - [ ] 3D prentaðan (PLA)
    - [ ] 3D prentaðan (PVB)
    - ???
- Bæta við WifiManager, t.d. [þessum](https://randomnerdtutorials.com/esp32-wi-fi-manager-asyncwebserver/)

## Eiginleikar

- [x] Vefviðmót
- [x] Þægilegt hýsisnafn (e. _hostname_)
- [ ] API
- [x] Breytilegt birtustig
- [x] Velja lit
- [ ] Nokkrar fyrir fram ákveðnar stillingar
    - [x] Rólegt
    - [ ] Norðurljós?
    - ...

## Myndir

| ![Í vinnslu](myndir/tangle.jpg) | 
|:--:| 
| *Í vinnslu, FABXIAO notaður til prufu* |

| ![Vefviðmót](myndir/screenshot.png) | 
|:--:| 
| *Vefviðmót* |

## 3D Módel (Fusion 360)

| ![Módel](myndir/model.jpg) | 
|:--:| 
| *Módel* |

| ![Módel þverskurður](myndir/model-skurdur.jpg) | 
|:--:| 
| *Módel þverskurður* |

## Samsetning

| ![Vírar](myndir/jumperar.jpg) | 
|:--:| 
| *Vírar, jumperar* |

| ![Gegnumtak](myndir/gegnum.jpg) | 
|:--:| 
| *Vírar settir í gegn um rétt göt* |

| ![Neopixel lóðaður](myndir/neopixel-lodadur.jpg) | 
|:--:| 
| *Neopixel lóðaður* |

| ![Pinnar](myndir/pinnar.jpg) | 
|:--:| 
| *Pinnar (e. headers)* |

| ![Pinnar lóðaðir](myndir/pinnar-lodadir.jpg) | 
|:--:| 
| *Pinnar lóðaðir, gætið að því láta langa hlutann snúa upp.* |

| ![ESP32C3 á sínum stað](myndir/xiao.jpg) | 
|:--:| 
| *ESP32C3 á sínum stað* |

| ![Samsett](myndir/samsett.jpg) | 
|:--:| 
| *Samsett* |

| ![USB-tengi](myndir/usb-tengi.jpg) | 
|:--:| 
| *Passið að USB-tengið vísi út |

| ![Tilbúið](myndir/tilbuid.jpg) | 
|:--:| 
| *Tilbúið, með kúpli* |

## Nótur

### Villa í ASPAsyncWebServer 

Sjá: https://github.com/me-no-dev/ESPAsyncWebServer/pull/1142

í `AsyncWebSocket.cpp` þarf að breyta eftirfarandi:

    IPAddress AsyncWebSocketClient::remoteIP() {
        if(!_client) {
            return IPAddress(0U);
        }
        return _client->remoteIP();
    }

svona: 

    IPAddress AsyncWebSocketClient::remoteIP() {
        if(!_client) {
            return IPAddress();
        }
        return _client->remoteIP();
    }
