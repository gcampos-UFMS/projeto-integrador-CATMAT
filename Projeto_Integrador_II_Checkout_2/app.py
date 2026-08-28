from datetime import date, datetime
import json, os, re
from pathlib import Path
import pandas as pd
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
API_URL = "https://dadosabertos.compras.gov.br/modulo-arp/2_consultarARPItem"
REQUEST_TIMEOUT = 15
DEMO_PATH = Path(__file__).parent / "data" / "demo.json"

def cnpj_format(value):
    d = re.sub(r"\\D", "", str(value)).zfill(14)
    return f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:]}"

def number(value):
    if isinstance(value,(int,float)): return float(value)
    s=str(value).strip()
    if "," in s: s=s.replace(".","").replace(",",".")
    try: return float(s)
    except ValueError: return 0.0

def pncp_link(value):
    s=str(value)
    if s.startswith("http://") or s.startswith("https://"): return s
    parts=s.replace("/","-").split("-")
    if len(parts)!=4: return ""
    return f"https://pncp.gov.br/app/atas/{parts[0]}/{parts[3].lstrip('0')}/{parts[2].lstrip('0')}/{parts[1]}"

def fetch_data(catmat):
    if os.getenv("DEMO_MODE")=="1":
        payload=json.loads(DEMO_PATH.read_text(encoding="utf-8"))
        return payload if catmat==payload["catmat"] else {"resultado":[]}
    today=date.today().isoformat()
    params={"pagina":1,"tamanhoPagina":500,
            "dataVigenciaInicialMin":f"{date.today().year}-01-01",
            "dataVigenciaInicialMax":today,"codigoItem":catmat}
    r=requests.get(API_URL,params=params,timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()

def process_result(payload):
    rows=payload.get("resultado",[])
    if not rows: return None
    df=pd.DataFrame(rows)
    if "valorUnitario" not in df.columns: raise ValueError("Campo valorUnitario ausente.")
    df["valorUnitario"]=df["valorUnitario"].map(number)
    df=df.dropna(subset=["valorUnitario"]).copy()
    if df.empty: return None
    med=float(df["valorUnitario"].median())
    lo,hi=med*.5,med*1.5
    saneada=df[df["valorUnitario"].between(lo,hi)].copy()
    if saneada.empty: saneada=df.copy()
    ids=set(saneada.index)
    mean=float(saneada["valorUnitario"].mean()); median=float(saneada["valorUnitario"].median())
    final=float(payload.get("preco_final_sugerido",min(mean,median)))
    result_rows=[]
    for idx,row in df.iterrows():
        result_rows.append({"ata":str(row.get("numeroAtaRegistroPreco","")),
          "unidade":str(row.get("nomeUnidadeGerenciadora","")),
          "fornecedor":str(row.get("nomeRazaoSocialFornecedor","")),
          "cnpj":cnpj_format(row.get("niFornecedor","")),
          "quantidade":number(row.get("quantidadeHomologadaVencedor",0)),
          "valor_unitario":number(row.get("valorUnitario",0)),
          "valor_total":number(row.get("valorTotal",0)),
          "link":pncp_link(row.get("numeroControlePncpCompra","")),
          "considerado":idx in ids})
    return {"descricao":payload.get("descricao") or rows[0].get("descricaoItem","Não informada"),
            "original_count":int(payload.get("quantidade_precos",len(df))),
            "sanitized_count":int(payload.get("precos_apos_saneamento",len(saneada))),
            "mean":mean,"median":median,"final_price":final,"rows":result_rows,
            "generated_at":datetime.now().strftime("%d/%m/%Y %H:%M")}

@app.get("/")
def home(): return render_template("index.html")

@app.get("/api/consulta")
def api_consulta():
    catmat=request.args.get("catmat","").strip()
    if not catmat.isdigit(): return jsonify({"error":"Informe somente números no código CATMAT."}),400
    try:
        result=process_result(fetch_data(catmat))
        if result is None: return jsonify({"error":"Nenhum registro foi encontrado para o código CATMAT informado."}),404
        return jsonify(result)
    except requests.RequestException:
        return jsonify({"error":"Não foi possível consultar a fonte externa no momento."}),502
    except (ValueError,KeyError,TypeError):
        return jsonify({"error":"A resposta da fonte não possui a estrutura esperada."}),502

if __name__=="__main__": app.run(debug=False)
