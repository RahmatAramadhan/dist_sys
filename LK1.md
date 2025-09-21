# LK1

Berikut adalah penjelasan dari tugas percobaan protocol yang tersedia pada docker ini.

---

## 1. REST API

- **Server (Flask)**  
  Server menyediakan beberapa endpoint (`/add`, `/mul`).  
  - Client mengirimkan **request HTTP GET** dengan parameter `a` dan `b`.  (pada percobaan saya mengirimkan a = 100 dan b = 5)
  - Server memproses perhitungan sesuai endpoint.  
  - Server mengembalikan **response dalam format JSON**.

- **Client (Python)**  
  Client menggunakan modul `requests` untuk memanggil server REST API.  
  - Client mengirim request ke server dengan `params={'a':..., 'b':...}`.  
  - Client menerima JSON response.  
  - Hasilnya ditampilkan di terminal.

---

### Endpoint

Kode sebelumnya hanya tersedia **penjumlahan (`/add`)** dan **perkalian (`/mul`)**.  

Saya menambahkan sendiri dua endpoint baru:  yaitu **pengurangan (`/min`)** dan **pembagian (`/div`)**

### Tambahan Saya

```python
//ini untuk pembagian (min)
@app.route('/div', methods=['GET'])
def div_numbers():
    try:
        # Mengambil parameter a dan b dari query string
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        if b == 0:
            return jsonify({'error': 'Division by zero'}), 400
        result = a / b

        return jsonify({'result': result})
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input'}), 400

//ini untuk pengurangan (div)
@app.route('/div', methods=['GET'])
def div_numbers():
    try:
        # Mengambil parameter a dan b dari query string
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        if b == 0:
            return jsonify({'error': 'Division by zero'}), 400
        result = a / b

        return jsonify({'result': result})
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input'}), 400
```
percobaan yang saya lakukan sebagai berikut : 
```console
rahmat@Rahmat:~/dist_sys$ docker compose -f compose/rest.yml exec rest-server python client.py --op both -a 100 -b 5
add(100,5) = 105
mul(100,5) = 500
min(100,5) = 95
div(100,5) = 20.0
```
---
# 2. TCP

## 🔹 Cara Kerja

### Server
1. Membuat socket TCP (`AF_INET`, `SOCK_STREAM`).
2. Bind ke alamat `0.0.0.0:2222`, sehingga bisa diakses dari container lain.
3. Listening dan menunggu koneksi client.
4. Menerima pesan dari client (`recv`) dan mencetaknya.
5. Mengirimkan balasan ke client dalam format `Echo: <pesan>`.
6. Jika client mengirim pesan `bye`, server akan membalas dengan `"Goodbye!"` lalu menutup koneksi.

### Client
1. Membuat socket TCP dan connect ke server (`reqresp-server:2222`).
2. Mengirim pesan teks ke server (`send`).
3. Menerima balasan dari server (`recv`) dan menampilkannya.
4. Proses berulang sampai user mengetik `bye`.
5. Saat user mengetik `bye`, client mengirimkan pesan ke server lalu menerima balasan `"Goodbye!"` sebelum menutup koneksi.

---

## 🔹 Alur Sederhana
Client ---> "Hello" ---> Server
Client <--- "Echo: Hello" <--- Server

Client ---> "bye" ---> Server
Client <--- "Goodbye!" <--- Server

## menambahkan exit untuk keluar
saya mencoba menambahkan perintah exit untuk keluar dari client dan server, penambahaan dilakukan didalam file server.py dan client.py

### server.py
```pyhton
while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Received from client:", data)
        
        if data.lower().strip() == "exit":
            conn.sendall("Server shutting down.".encode())
            print("Exiting server.")
            break
        else:
            response = "Echo: " + data
            conn.send(response.encode())
```
### client.py
```python
while True: 
        message = input("Enter message(type 'exit to exit command'): ")
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024).decode()
        print("Received from server:", data)

        if message.lower().strip() == "exit":
            print("Connection closed.")
            break
```

## percobaan
berikut adalah percobaan menjalankan aplikasi protocol TCP. Percobaan dilakukan setelah perubahan dalam server dan client, dengan menggunakan perintah exit.

### client
```console
rahmat@Rahmat:~/dist_sys$ docker compose -f compose/reqresp.yml exec reqresp-client python client.py
WARN[0000] /home/rahmat/dist_sys/compose/reqresp.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
Enter message(type 'exit to exit command'): nama saya rahmat
Received from server: Echo: nama saya rahmat
Enter message(type 'exit to exit command'): sasaya berkuliah di universitas brawijaya
Received from server: Echo: sasaya berkuliah di universitas brawijaya
Enter message(type 'exit to exit command'): jurusan magister ilmu komputer
Received from server: Echo: jurusan magister ilmu komputer
Enter message(type 'exit to exit command'): exit
Received from server: Server shutting down.
Connection closed.
```

### server
```console
rahmat@Rahmat:~/dist_sys$ docker compose -f compose/reqresp.yml exec reqresp-server python server.py
WARN[0000] /home/rahmat/dist_sys/compose/reqresp.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
Server listening on 0.0.0.0:2222
Connection from: ('172.20.0.3', 38012)
Received from client: nama saya rahmat
Received from client: sasaya berkuliah di universitas brawijaya
Received from client: jurusan magister ilmu komputer
Received from client: exit
Exiting server.
```
## Webshark
Kemudian dapat dilihat juga menggunakan webshark untuk melihat proses pengiriman pesan pada protocol TCP

<img width="2270" height="1125" alt="Image" src="https://github.com/user-attachments/assets/e6d44b40-47be-46e7-9e1e-735630e84c85" />

Pada sisi client dengan alamat ip 172.20.0.3 terlihat adanya pengiriman data ke server melalui port 2222. Kemudian pada sisi server dengan ip 172.20.0.2 merespons paket tersebut. Proses komunikasi dapat dilihat menggunakan protocol TCP, didalamnya berisi data dan konfirmasi penerimaan dari client ke server.

---

# 3. UDP

## 🔹 Cara Kerja

### Server
1. Membuat socket UDP (`AF_INET`, `SOCK_DGRAM`).  
2. Bind ke alamat `0.0.0.0:12345`, sehingga bisa menerima paket dari container lain.  
3. Menunggu pesan dari client (`recvfrom`).  
4. Mencetak pesan yang diterima beserta alamat pengirim.  
5. Mengirim balasan ke client dalam format:

### Client
1. Membuat socket UDP (`AF_INET`, `SOCK_DGRAM`).  
2. Mengirim pesan teks ke server (`sendto`).  
3. Menunggu balasan dari server (`recvfrom`) dan menampilkannya.  
4. Socket ditutup setelah balasan diterima. 

## 🔹 alur Kerja
Client ---> "Hello, UDP server!" ---> Server  
Client <--- "Hello, (IP:Port). You said: Hello, UDP server!" <--- Server  

Berikut adalah percobaan menjalankan aplikasi protocol UDP.  
Client mengirimkan pesan, lalu server merespons balik dengan tambahan informasi alamat pengirim.

### client
```console
rahmat@Rahmat:~/dist_sys$ docker compose -f compose/udp.yml exec udp-client python clientUDP.py
WARN[0000] /home/rahmat/dist_sys/compose/udp.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
Received from server: Hello, ('172.20.0.5', 55179). You said: Hello, UDP server2! nama saya Rahmat dari Brawijaya
```

### server
```console
rahmat@Rahmat:~/dist_sys$ docker compose -f compose/udp.yml exec udp-server python serverUDP.py
WARN[0000] /home/rahmat/dist_sys/compose/udp.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
UDP server up and listening on ('0.0.0.0', 12345)
Received message from ('172.20.0.5', 33428): Hello, UDP server2! nama saya Rahmat dari Brawijaya
Received message from ('172.20.0.5', 55179): Hello, UDP server2! nama saya Rahmat dari Brawijaya
```
saya mengganti inputan pada client agar terlihat perbedaan disisi server. kemudian saya juga mengcapture menggunakan webshark yang akan menampilkan proses pengiriman data dalam protocol UDP. Berikut adalah hasil capture webshark:

<img width="2281" height="811" alt="Image" src="https://github.com/user-attachments/assets/c5baf6c3-0e21-4e35-8298-6f1d80eae4f6" />

- UDP capture ini memperlihatkan komunikasi request–response sederhana: client mengirim pesan → server membalas.
- Tidak ada connection setup seperti pada TCP, hanya pengiriman paket satu arah yang kemudian direspons.
- Terlihat duplicate paket (dua kali kirim & dua kali balas) yang umum dalam eksperimen UDP karena tidak ada jaminan reliabilitas.

  ---
# 4. MQTT
## 🔹 Cara Kerja

