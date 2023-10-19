# Lampi

**Verk í vinnslu**

_Útbúa verkefnalýsingu og efni fyrir rafmagns/forritunarnámskeið_


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
