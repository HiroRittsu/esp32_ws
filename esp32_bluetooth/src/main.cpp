#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

void onDataReceived(const uint8_t* buffer, size_t size) {
  // 受信したデータを文字列に変換
  String received = "";
  for (size_t i = 0; i < size; i++) {
    received += (char)buffer[i];
  }
  Serial.println(received);

  // 受信データを送信データとしてそのまま返す
  // SerialBT.print(received);
}

void setup() {
  Serial.begin(115200);  // 一応Serialを初期化
  SerialBT.begin("ESP32");
  SerialBT.onData(onDataReceived);
}

void loop() {
  SerialBT.print("123.0");
  delay(100);
}