#define M5STACK_MPU6886
#include <M5Core2.h>
#include "BluetoothSerial.h"
#include <ArduinoJson.h>

BluetoothSerial SerialBT;

// 初期設定 ----------------------------------------------------------
void setup()
{
  // Bluetooth
  SerialBT.begin("M5stack Core2");

  M5.begin(true, true, true, true); // 本体初期化
  // Serial.begin(115200);              // シリアル出力初期化
  M5.IMU.Init();                     // 6軸センサ初期化
  M5.IMU.SetAccelFsr(M5.IMU.AFS_8G); // 加速度センサースケール初期値設定 ±8G(2,4,8,16) ※GRAYは「setAccelFsr」（先頭のsが小文字）
}

// メイン処理 --------------------------------------------------------
void loop()
{
  // 変数宣言
  float accX, accY, accZ;    // 加速度格納用
  float gyroX, gyroY, gyroZ; // 角速度格納用
  float pitch, roll, yaw;    // 姿勢角格納用

  M5.IMU.getAccelData(&accX, &accY, &accZ);   // 加速度データ取得
  M5.IMU.getGyroData(&gyroX, &gyroY, &gyroZ); // 角速度データ取得
  M5.IMU.getAhrsData(&pitch, &roll, &yaw);    // 姿勢角データ取得

  // JSONオブジェクト作成
  StaticJsonDocument<200> jsonDoc;
  jsonDoc["acc"]["x"] = accX;
  jsonDoc["acc"]["y"] = accY;
  jsonDoc["acc"]["z"] = accZ;
  jsonDoc["gyro"]["x"] = gyroX;
  jsonDoc["gyro"]["y"] = gyroY;
  jsonDoc["gyro"]["z"] = gyroZ;
  jsonDoc["angle"]["pitch"] = pitch;
  jsonDoc["angle"]["roll"] = roll;
  jsonDoc["angle"]["yaw"] = yaw;

  // JSON文字列にシリアライズ
  char jsonBuffer[200];
  serializeJson(jsonDoc, jsonBuffer);

  // Bluetoothで送信
  SerialBT.println(jsonBuffer);
  // Serial.println(jsonBuffer);

  delay(10);
}