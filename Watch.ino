#include <WiFi.h>

#include <GxEPD.h>
#include <GxGDEP015OC1/GxGDEP015OC1.h>
#include <GxIO/GxIO_SPI/GxIO_SPI.h>
#include <GxIO/GxIO.h>
#include "BitmapGraphics.h"

#include <Fonts/FreeSansBold24pt7b.h>

//initialise the value
const int PushButton = 15;

const char* ssid = "Nha cun";
const char* password =  "nu26112011";

const uint16_t port = 8888;
String readString1;

WiFiServer wifiServer(port);

GxIO_Class io(SPI, SS, 22, 21);
GxEPD_Class display(io, 16, 4);

// Function: Displaying the Message to E-INK monitor1
void showPartialUpdate(String message)
{

  const char* name = "FreeSansBold24pt7b";
  const GFXfont* f = &FreeSansBold24pt7b;
  uint16_t box_x = 60;
  uint16_t box_y = 60;
  uint16_t box_w = 90;
  uint16_t box_h = 100;
  uint16_t cursor_y = box_y + 16;

  display.setRotation(45);
  display.setFont(f);
  display.setTextColor(GxEPD_BLACK);

  display.fillRect(box_x, box_y, box_w, box_h, GxEPD_WHITE);
  display.setCursor(box_x, cursor_y + 38);
  display.print(message);
  display.updateWindow(box_x, box_y, box_w, box_h, true);
}

//Function: Display the message to the Serial
void printToSerial(String message) {
  Serial.println("Starting printing ....");
  delay(10);
  Serial.println(message);
}

void setup() {
  display.init();

  pinMode(PushButton, INPUT);

  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }

  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());


  wifiServer.begin();
}

void loop() {

  WiFiClient client = wifiServer.available();
  char c;
  int buttonStatus = digitalRead(PushButton);

  if (client) {
    Serial.println("Nurse Watch connecting to BayMax");
    while (client.connected()) {
  

      while (client.available() > 0) {
        if ( buttonStatus != HIGH) {
          c = client.read();

          if (readString1.length() < 100) {
            readString1 += c;
          }

          if (c == '\n') {
            printToSerial(readString1);
            delay(10);
            showPartialUpdate(readString1);
          }
        }

        else {
          Serial.println("Button Pressed");
          client.print("Confirmed");
          readString1 = "";
          delay(10);
        }

      }


      delay(10); 
    }

    client.stop();
    Serial.println("Client disconnected");

  }
}
