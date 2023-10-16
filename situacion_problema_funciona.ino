#include <Wire.h>
#include <RtcDS1302.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <WiFi.h>

ThreeWire myWire(14, 12, 27);
RtcDS1302<ThreeWire> Rtc(myWire);
LiquidCrystal_I2C lcd(0x27, 16, 2);
DHT dht(5, DHT11);
const int mq135Pin = 34;
const char* ssid = "Tec-Contingencia";
const char* password = "";
const int buttonPin1 = 2;
const int buttonPin2 = 4;
const char* apiEndpoint = "https://fictional-space-spoon-979j4x67jrq43pp65-5000.app.github.dev/sensor_data";

enum DisplayMode {
  SHOW_TIME,
  SHOW_DHT,
  SHOW_MQ135
};

DisplayMode currentMode = SHOW_TIME;
float temperature;
float humidity;
float gasValue;


void setupWifi() {
  Serial.begin(9600);
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.print(" Connected: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  currentMode = SHOW_TIME;
  setupWifi();
  pinMode(buttonPin1, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);

  dht.begin();
  Rtc.Begin();

  RtcDateTime compiled = RtcDateTime(__DATE__, __TIME__);
  if (!Rtc.IsDateTimeValid()) {
    Serial.println("RTC no válido. Configurando la fecha y hora...");
    Rtc.SetDateTime(compiled);
  }
}



void loop() {
  RtcDateTime now = Rtc.GetDateTime();
  lcd.clear();
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  gasValue = readMQ135();
  sendData(temperature, humidity, gasValue, now);
  
  if (digitalRead(buttonPin1) == HIGH) {
    currentMode = SHOW_DHT;
  } else if (digitalRead(buttonPin2) == HIGH) {
    currentMode = SHOW_MQ135;
  } else {
    currentMode = SHOW_TIME;
  }

  switch (currentMode) {
    case SHOW_TIME:
      lcd.print(now.Day(), DEC);
      lcd.print('/');
      lcd.print(now.Month(), DEC);
      lcd.print('/');
      lcd.print(now.Year(), DEC);
      lcd.setCursor(0, 1);
      lcd.print(now.Hour(), DEC);
      lcd.print(':');
      lcd.print(now.Minute(), DEC);
      lcd.print(':');
      lcd.print(now.Second(), DEC);
      break;

    case SHOW_DHT:
      temperature = dht.readTemperature();
      humidity = dht.readHumidity();
      lcd.print("Temp: ");
      lcd.print(temperature);
      lcd.setCursor(0, 1);
      lcd.print("Humedad: ");
      lcd.print(humidity);
      break;

    case SHOW_MQ135:
      gasValue = readMQ135();
      displayMQ135Value();
      break;
  }

  delay(1000);
}

void sendData(float temperature, float humidity, float gasValue, const RtcDateTime& timestamp) {
 Serial.print("Sending data to API: ");

  Serial.print(temperature);
  Serial.print(humidity);
  Serial.print(gasValue);

  HTTPClient http;
  http.begin(apiEndpoint);
  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument <200> doc; // Use DynamicJsonDocument
  doc["temperature"] = temperature;
  doc["humidity"] = humidity;
  doc["gasValue"] = gasValue;

  char datestring[20];
  snprintf_P(datestring, sizeof(datestring), PSTR("%04u-%02u-%02u %02u:%02u:%02u"),
             timestamp.Year(), timestamp.Month(), timestamp.Day(),
             timestamp.Hour(), timestamp.Minute(), timestamp.Second());
  doc["date_time"] = datestring;

  String json;
  serializeJson(doc, json);

  int httpResponseCode = http.POST(json);
  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    String responseString = http.getString();
    Serial.println("Received response: " + responseString);
  } else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  http.end();
}

float readMQ135() {
  // Leer la lectura analógica del nuevo pin del sensor MQ135
  int sensorValue = analogRead(mq135Pin);
  
  float gasValue = (float)sensorValue / 1024.0 * 10000.0;
  
  return gasValue;
}
void displayMQ135Value() {
  float gasValue = readMQ135();
  lcd.print("Gas: ");
  lcd.print(gasValue);
  // Display the calculated gas concentration value on the LCD
}
