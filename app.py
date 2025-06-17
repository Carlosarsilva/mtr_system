from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from html2image import Html2Image
import os

app = Flask(__name__)
hti = Html2Image(output_path='static/prints')
hti.browser_flags = ['--no-sandbox']

def salvar_dados(dados):
    conn = sqlite3.connect('mtr.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ficha (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            condominio TEXT,
            moto TEXT,
            ronda TEXT,           
            data TEXT,
            hora TEXT,
            turno TEXT,
            km_inicial TEXT,
            km_final TEXT,
            km_total TEXT,
            nivel_bateria TEXT,
            capacete TEXT,
            observacoes TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO ficha (condominio, moto, ronda, data, hora, turno, km_inicial, km_final, km_total, nivel_bateria, capacete, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', dados)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    condominio = request.form['condominio']
    moto = request.form['moto']
    ronda = request.form['ronda']
    data = request.form['data']
    turno = request.form['turno']
    hora = request.form['hora']
    km_inicial = request.form['km_inicial']
    km_final = request.form['km_final']
    km_total = request.form['km_total']
    nivel_bateria = request.form['nivel_bateria']
    capacete = request.form['capacete']
    observacoes = request.form['observacoes']

    salvar_dados((condominio, moto, ronda, data, hora, turno, km_inicial, km_final, km_total, nivel_bateria, capacete, observacoes))

    html_content = f"""<html>
    <body style='font-family:Arial; padding:20px'>
        <h2>Ficha de Controle MTR Elétrica</h2>
        <p><strong>Condomínio:</strong> {condominio}</p>
        <p><strong>Data:</strong> {data}</p>
        <p><strong>Hora:</strong> {hora}</p>
        <p><strong>Turno:</strong> {turno}</p>
        <p><strong>Moto:</strong> {moto}</p>
        <p><strong>Ronda:</strong> {ronda}</p>
        <p><strong>KM Inicial:</strong> {km_inicial}</p>
        <p><strong>KM Final:</strong> {km_final}</p>
        <p><strong>KM Total:</strong> {km_total}</p>
        <p><strong>Nível Bateria:</strong> {nivel_bateria}</p>
        <p><strong>Capacete:</strong><br>{capacete}</p>
        <p><strong>Observações:</strong><br>{observacoes}</p>
    </body>
    </html>"""

    filename = f"ficha_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    hti.screenshot(html_str=html_content, save_as=filename)

    mensagem = f"*Ficha MTR Elétrica*\ncondominio: {condominio}\nturno: {turno}\ndata: {data}\nhora: {hora}\nronda: {ronda}\nkm_inicial: {km_inicial}\nkm_final: {km_final}\nkm_total: {km_total}\nnivel_bateria: {nivel_bateria}\ncapacete: {capacete}\nobservações: {observacoes}"
    numero = "5551996080169"
    link = f"https://wa.me/{numero.strip()}?text=" + mensagem.replace(" ", "%20").replace("\n", "%0A")
    return redirect(link)

if __name__ == '__main__':
    os.makedirs('static/prints', exist_ok=True)
    app.run(debug=True)
