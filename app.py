from flask import Flask, jsonify, request, render_template
import mysql.connector
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)  


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bahabaha2003",
        database="FutbolVeriTabani"
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/takimlar', methods=['GET'])
def takimlari_getir():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Takimlar")
    takimlar = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(takimlar)

@app.route('/antrenorler', methods=['GET'])
def antrenorleri_getir():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT antrenor_id, antrenor_ad, antrenor_soyad FROM Antrenorler")
    antrenorler = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(antrenorler)


@app.route('/antrenor-ekle', methods=['POST'])
def antrenor_ekle():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()

    if not data or 'antrenor_ad' not in data or 'antrenor_soyad' not in data or 'uyruk' not in data or 'antrenor_yas' not in data:
        return jsonify({"error": "Eksik veya hatalı veri gönderildi."}), 400

    try:
        cursor.callproc('get_Antrenor_Ekle', (data['antrenor_ad'], data['antrenor_soyad'], data['uyruk'], data['antrenor_yas']))
        conn.commit()
        return jsonify({"message": "Antrenör başarıyla eklendi."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/takim-ekle', methods=['POST'])
def takim_ekle():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()

    if not data or 'takim_isim' not in data or 'kurulus' not in data or 'antrenor_id' not in data:
        return jsonify({"error": "Eksik veya hatalı veri gönderildi."}), 400

    try:
        cursor.callproc('get_takim_ekle', (data['takim_isim'], data['kurulus'], data['antrenor_id']))
        conn.commit()
        return jsonify({"message": "Takım başarıyla eklendi."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/oyuncu-ekle', methods=['POST'])
def oyuncu_ekle():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()

    if not data or 'oyuncu_isim' not in data or 'oyuncu_soyisim' not in data or 'mevki' not in data or 'uyruk' not in data or 'forma_no' not in data or 'takim_id' not in data or 'oyuncu_yas' not in data:
        return jsonify({"error": "Eksik veya hatalı veri gönderildi."}), 400

    try:
        cursor.callproc('get_oyuncu_ekle', (data['oyuncu_isim'], data['oyuncu_soyisim'], data['mevki'], data['uyruk'], data['forma_no'], data['takim_id'], data['oyuncu_yas']))
        conn.commit()
        return jsonify({"message": "Oyuncu başarıyla eklendi."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/antrenman-ekle', methods=['POST'])
def antrenman_ekle():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()

    if not data or 'antreman_tarih' not in data or 'antreman_yer' not in data or 'antreman_turu' not in data or 'antreman_antrenor_id' not in data or 'takim_id' not in data:
        return jsonify({"error": "Eksik veya hatalı veri gönderildi."}), 400

    try:
        cursor.callproc('get_antreman_ekle', (data['antreman_tarih'], data['antreman_yer'], data['antreman_turu'], data['antreman_antrenor_id'], data['takim_id']))
        conn.commit()
        return jsonify({"message": "Antrenman başarıyla eklendi."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/sezon-ekle', methods=['POST'])
def sezon_ekle():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()

    if not data or 'Baslangic_tarih' not in data or 'Bitis_tarih' not in data:
        return jsonify({"error": "Eksik veya hatalı veri gönderildi."}), 400

    try:
        cursor.callproc('get_sezon_ekle', (data['Baslangic_tarih'], data['Bitis_tarih']))
        conn.commit()
        return jsonify({"message": "Sezon başarıyla eklendi."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 6. Maç Ekle
@app.route('/mac-ekle', methods=['POST'])
def mac_ekle():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()

    if not data or 'mac_tarih' not in data or 'evsahibi_takim_id' not in data or 'konuk_takim_id' not in data or 'evsahibi_skor' not in data or 'konuk_skor' not in data or 'sezon_id' not in data:
        return jsonify({"error": "Eksik veya hatalı veri gönderildi."}), 400

    try:
        cursor.callproc('get_mac_ekle', (data['mac_tarih'], data['evsahibi_takim_id'], data['konuk_takim_id'], data['evsahibi_skor'], data['konuk_skor'], data['sezon_id']))
        conn.commit()
        return jsonify({"message": "Maç başarıyla eklendi."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/takimlar/<int:takim_id>/kazandigi-maclar', methods=['GET'])
def takim_kazandigi_maclar(takim_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('get_takim_kazandigi_maclar', (takim_id,))
        maclar = []
        for result in cursor.stored_results():
            maclar = result.fetchall()
        return jsonify(maclar)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/takimlar-antrenorler', methods=['GET'])
def takimlar_antrenorler():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('takimlar_antrenorler')
        takimlar = []
        for result in cursor.stored_results():
            takimlar = result.fetchall()
        return jsonify(takimlar)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/takimlar-oyuncular', methods=['GET'])
def takimlar_oyuncular():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('takimlar_oyuncular')
        oyuncular = []
        for result in cursor.stored_results():
            oyuncular = result.fetchall()
        return jsonify(oyuncular)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/takimlar/<int:takim_id>/antrenmanlar', methods=['GET'])
def takim_antrenmanlari(takim_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('takim_antramanlari', (takim_id,))
        antrenmanlar = []
        for result in cursor.stored_results():
            antrenmanlar = result.fetchall()
        return jsonify(antrenmanlar)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/takimlar/<int:takim_id>/kaybettigi-maclar', methods=['GET'])
def takim_kaybettigi_maclar(takim_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('get_takim_kaybedilenmac', (takim_id,))
        maclar = []
        for result in cursor.stored_results():
            maclar = result.fetchall()
        return jsonify(maclar)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/takimlar/<int:takim_id>/berabere-maclar', methods=['GET'])
def takim_berabere_maclar(takim_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('get_berabere_maclar', (takim_id,))
        maclar = []
        for result in cursor.stored_results():
            maclar = result.fetchall()
        return jsonify(maclar)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/oyuncu-mac-ekle', methods=['POST'])
def oyuncu_mac_ekle():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()

    if not data or 'oyuncu_id' not in data or 'mac_id' not in data:
        return jsonify({"error": "Eksik veya hatalı veri gönderildi."}), 400

    try:
        cursor.callproc('get_oyuncu_mac_ekle', (data['oyuncu_id'], data['mac_id']))
        conn.commit()
        return jsonify({"message": "Oyuncu-Maç başarıyla eklendi."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/gol-ekle', methods=['POST'])
def gol_ekle():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()

    if not data or 'oyuncu_mac_id' not in data or 'takim_id' not in data:
        return jsonify({"error": "Eksik veya hatalı veri gönderildi."}), 400

    try:
        cursor.callproc('gol_ekle', (data['oyuncu_mac_id'], data['takim_id']))
        conn.commit()
        return jsonify({"message": "Gol başarıyla eklendi."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/takimlar/<int:takim_id>/en-golcu-oyuncu', methods=['GET'])
def takim_en_golcu_oyuncu(takim_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('get_takim_en_golcu_oyuncu', (takim_id,))
        oyuncu = {}
        for result in cursor.stored_results():
            oyuncu = result.fetchone()
        return jsonify(oyuncu)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True,port=5001)