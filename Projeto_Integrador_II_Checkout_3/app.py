import json
from flask import Flask,jsonify,render_template,request
import db
app=Flask(__name__); db.init_db(); DATA=app.root_path+'/data/demo.json'

def seed():
    if db.list_consultas(): return
    p=json.load(open(DATA,encoding='utf-8')); cid=db.upsert_catmat(p['catmat'],p['descricao']); q=db.create_consulta(cid,p['data_cotacao'],'50% acima/abaixo da mediana inicial',p['preco_final_sugerido'])
    vals=[float(str(r['valorUnitario']).replace('.','').replace(',','.')) for r in p['resultado']]
    m=sorted(vals)[len(vals)//2]
    for r,v in zip(p['resultado'],vals): db.create_registro(q,r,m*.5<=v<=m*1.5)

@app.get('/')
def home(): seed(); return render_template('index.html')
@app.get('/api/consultas')
def consultas(): seed(); return jsonify(db.list_consultas())
@app.get('/api/consultas/<int:qid>/registros')
def registros(qid): seed(); return jsonify(db.list_registros(qid))
@app.patch('/api/consultas/<int:qid>')
def update(qid):
    p=request.get_json(silent=True) or {}; data=str(p.get('data_analise','')).strip()
    if not data: return jsonify(error='data_analise obrigatoria'),400
    db.update_consulta_data(qid,data); return jsonify(ok=True)
@app.delete('/api/consultas/<int:qid>')
def delete(qid): db.delete_consulta(qid); return jsonify(ok=True)
if __name__=='__main__': app.run(debug=False)
