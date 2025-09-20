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


