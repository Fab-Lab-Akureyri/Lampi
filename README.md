# Lampi

**Verk í vinnslu**

Kaótíkin ræður ríkjum

## Uppsetning

- Setja upp Visual Studio Code
- Setja up PlatformIO
   - Hægt að ná í extension í [VScode](https://docs.platformio.org/en/latest/integration/ide/vscode.html)
- Opna Lampi.io með [platformIO](https://platformio.org/)   
- ýtta á `Build` sem býr til ýmsar skrár
- Laga línu í `AsyncWebSocket.cpp` [sjá neðar](https://github.com/hanndoddi/Lampi/tree/main#villa-%C3%AD-aspasyncwebserver)
- Framkvæma þessi skref:
    1. Build filesystem Image
    2. Upload filesystem Image
    3. Upload and monitor

| ![Skref](myndir/skref.jpg) | 
|:--:| 
| *Skref* |

## TODO: 

- _Útbúa verkefnalýsingu og efni fyrir rafmagns/forritunarnámskeið_

## Kröfur, í vinnslu

Lágmarks kröfur:

- Hreyfanlega hluti
- Stillanlega hluti
- 3D prentaða hluti
- Sérhannaða rafrás
- Laserskorna hluti
- Virka án nets - takkar líka
- SPIFFS?
  - https://randomnerdtutorials.com/install-esp32-filesystem-uploader-arduino-ide/
  - https://randomnerdtutorials.com/esp32-vs-code-platformio-spiffs/

Gott að hafa: 

- Nettengingu
- Vefviðmót
- Bluetooth?
- Og góða skapið 😁

## Myndir

| ![Víraflækja](myndir/tangle.jpg) | 
|:--:| 
| *Víraflækja* |

| ![Jón að setja saman](myndir/assembly.jpg) | 
|:--:| 
| *Jón að setja saman* |

| ![Vefviðmót](myndir/screenshot.png) | 
|:--:| 
| *Vefviðmót* |


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
