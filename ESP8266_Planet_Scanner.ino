/**
   BasicHTTPClient.ino

    Created on: 24.05.2015

*/

#define DEBUG 1

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <SPI.h>      // Include the spi library for comunication with the mfrc522 rfid scanner
#include <MFRC522.h>  // Include the mfrc522 rfid scanner library

#include <ESP8266HTTPClient.h>

#include <WiFiClient.h>

ESP8266WiFiMulti WiFiMulti;

#ifndef STASSID
#define STASSID "DEV"
#define STAPSK  "Kaffe10ko"
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;

#define RST_PIN         5 
#define SS_PIN          15

String scanner_id;

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

void setup() {
  #ifdef DEBUG
  Serial.begin(115200);
  #endif
  
  SPI.begin();            // Init SPI bus
  mfrc522.PCD_Init();     // Init MFRC522

  pinMode(LED_BUILTIN, OUTPUT);     // Initialize the LED_BUILTIN pin as an output
  
  // We start by connecting to a WiFi network

  #ifdef DEBUG
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  #endif
  
  /* Explicitly set the ESP8266 to be a WiFi-client, otherwise, it by default,
     would try to act as both a client and an access-point and could cause
     network-issues with your other WiFi-devices on your WiFi-network. */
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    
    #ifdef DEBUG
    Serial.print(".");
    #endif
  }

  #ifdef DEBUG
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  #endif

  bool donthaveid = true;
  while(donthaveid){
    #ifdef DEBUG
    Serial.println("Getting scanner id from server");
    #endif
    
    scanner_id = get("http://10.108.169.133:5000/planet_scanner?get_new_id=1");
    
    if(scanner_id != "0"){
      donthaveid = false;
      #ifdef DEBUG
        Serial.println("Got ID: " + scanner_id);
      #endif
    }else{
      #ifdef DEBUG
        Serial.println("Didn't get ID from server, trying again");
      #endif
      
    } 
  }
}

String get(String address) {

  String response;
  
  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {

    WiFiClient client;

    HTTPClient http;

    #ifdef DEBUG
    Serial.print("[HTTP] begin...\n");
    #endif
    
    if (http.begin(client, address)) {  // HTTP

      #ifdef DEBUG
      Serial.print("[HTTP] GET...\n");
      #endif
      
      // start connection and send HTTP header
      int httpCode = http.GET();

      // httpCode will be negative on error
      if (httpCode > 0) {
        #ifdef DEBUG
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTP] GET... code: %d\n", httpCode);
        #endif
        
        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          response = http.getString();
          #ifdef DEBUG
          Serial.println("HTTP Response: " + response);
          #endif
          
        }
      } else {
        response = "0";
        #ifdef DEBUG
        Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
        #endif
      }

      http.end();
    } else {
      response = "0";
      #ifdef DEBUG
      Serial.printf("[HTTP} Unable to connect\n");
      #endif
    }
  }else{
    response = "0";
  }
  if(response == "0"){
    digitalWrite(LED_BUILTIN, LOW);
  }else{
    digitalWrite(LED_BUILTIN, HIGH);
  }
  return response;
}

void loop() {
    // Getting ready for Reading PICCs
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  
  get("http://10.108.169.133:5000/planet_scanner?scanner_id=" + scanner_id + "&planet_id=" + String((char*)mfrc522.uid.uidByte));
  
  #ifdef DEBUG
  Serial.println("Card Read"); // Print to the serial "Card Read"
  #endif
  mfrc522.PICC_HaltA(); // Stop reading 
}
