import bluetooth
import time
import threading

def find_esp32_device(target_name):
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

def receive_data(sock, num_pings):
    for i in range(num_pings):
        data = sock.recv(1024)
        recv_time = time.time()
        send_time = float(data.decode('utf-8'))
        round_trip_time = (recv_time - send_time) * 1000
        print(f"Ping {i}: {round_trip_time:.2f} ms")

def ping_esp32(bt_addr, num_pings=100):
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bt_addr, port))
    print(f"Connected to {bt_addr} on port {port}")

    recv_thread = threading.Thread(target=receive_data, args=(sock, num_pings))
    recv_thread.start()

    time.sleep(1)

    try:
        for i in range(num_pings):
            send_time = time.time()
            message = f"{send_time}"
            sock.send(message)
            time.sleep(0.1)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sock.close()
        print("Connection closed")

if __name__ == "__main__":
    target_name = "ESP32"
    esp32_address = find_esp32_device(target_name)

    if esp32_address is not None:
        ping_esp32(esp32_address)
