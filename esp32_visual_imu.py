import bluetooth
import time
import threading
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # ３Dグラフ作成のため
import numpy as np

class IMU_Viewer:
    def __init__(self, target_name) -> None:
        self.received_data = ""  # 受信データを格納するリスト
        self.data_thread = threading.Thread(target=self.receive_data)  # データ処理スレッド
        self.angle_data = {'pitch': [], 'roll': [], 'yaw': []}  # 角度データを格納する辞書
        self.fig, self.ax = plt.subplots(subplot_kw={'projection': '3d'})  

        # bluetooth接続
        esp32_address = self.find_esp32_device(target_name)
        port = 1
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((esp32_address, port))
        print(f"Connected to {esp32_address} on port {port}")
        
        if esp32_address is not None:
            self.data_thread.daemon = True  # メインスレッド終了時に自動終了
            self.data_thread.start()  # データ処理スレッド開始
            self.view_data()


    def find_esp32_device(self, target_name):
        """
        bluetoothの探索
        """
        target_address = None
        nearby_devices = bluetooth.discover_devices()

        for address in nearby_devices:
            if target_name == bluetooth.lookup_name(address):
                target_address = address
                break

        if target_address is not None:
            print(f"Found target bluetooth device with address: {target_address}")
        else:
            print("Could not find target bluetooth device nearby.")
        
        return target_address
    
    def view_data(self):
        try:
            while True:
                if self.received_data != "":
                    data_str = self.received_data
                    try:
                        data_json = json.loads(data_str)
                        angle = data_json.get("angle", {})
                        if angle:
                            pitch = angle.get("pitch", 0)
                            roll = angle.get("roll", 0)
                            yaw = angle.get("yaw", 0)
                            # self.ax.quiver(0, 0, 0, np.cos(np.radians(yaw)), np.sin(np.radians(yaw)), np.sin(np.radians(pitch)), length=1, normalize=True)
                            # plt.show()
                            self.update_plot(pitch, roll, yaw)
                    except json.JSONDecodeError:
                        print(f"Received data is not valid JSON: {data_str}")
                time.sleep(0.01)
        except Exception as e:
            print(f"An error occurred in data processing: {e}")

    def receive_data(self):
        try:
            while True:
                data = self.sock.recv(1024)
                self.received_data = data
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.sock.close()
            print("Connection closed")

    def update_plot(self, pitch, roll, yaw):
        print(pitch, roll, yaw)
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')
        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])
        self.ax.set_zlim([-1, 1])

        # 角度をラジアンに変換
        pitch_rad = np.radians(pitch)
        roll_rad = np.radians(180-roll)
        yaw_rad = np.radians(yaw)

        # 法線ベクトルを計算
        x = np.cos(pitch_rad)
        y = np.cos(roll_rad)
        z = 0.5

        # 法線ベクトルをプロット
        self.ax.quiver(0, 0, 0, x, y, z, length=1, normalize=True)
        
        """
        # self.ax.scatter(pitch, roll,yaw)
        arrow_X = [0, np.cos(np.radians(pitch))]
        arrow_Y = [0, np.cos(np.radians(pitch))]
        arrow_Z = [0, np.cos(np.radians(pitch))]
        self.ax.plot(arrow_X,arrow_Y,arrow_Z)
        print(np.cos(np.radians(pitch)))
        # self.ax.quiver(0, 0, 0, np.cos(np.radians(pitch)), 0,0 , length=1, normalize=True)
        # """
        plt.draw()
        plt.pause(0.0001)
        plt.cla()

if __name__ == "__main__":
    IMU_Viewer("M5stack Core2")
