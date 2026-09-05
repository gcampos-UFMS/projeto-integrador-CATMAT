import sqlite3
from pathlib import Path
BASE=Path(__file__).resolve().parent
DB_PATH=BASE/'data/projeto.db'
SCHEMA=BASE/'sql/schema.sql'

def conn():
    c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON'); return c

def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    with conn() as c: c.executescript(SCHEMA.read_text(encoding='utf-8'))

def upsert_catmat(codigo,descricao):
    with conn() as c:
        c.execute('INSERT INTO catmat_itens(codigo_catmat,descricao) VALUES(?,?) ON CONFLICT(codigo_catmat) DO UPDATE SET descricao=excluded.descricao',(codigo,descricao))
        return c.execute('SELECT id FROM catmat_itens WHERE codigo_catmat=?',(codigo,)).fetchone()['id']

def create_consulta(catmat_id,data_analise,criterio,preco_final):
    with conn() as c:
        return c.execute('INSERT INTO consultas(catmat_item_id,data_analise,criterio_saneamento,preco_final) VALUES(?,?,?,?)',(catmat_id,data_analise,criterio,preco_final)).lastrowid

def create_registro(consulta_id,r,considerado):
    def n(v):
        s=str(v)
        if ',' in s: s=s.replace('.','').replace(',','.')
        return float(s)
    with conn() as c:
        return c.execute('INSERT INTO registros_precos(consulta_id,numero_ata,unidade_gerenciadora,fornecedor,cnpj,quantidade,valor_unitario,valor_total,link_pncp,considerado) VALUES(?,?,?,?,?,?,?,?,?,?)',(consulta_id,r['numeroAtaRegistroPreco'],r['nomeUnidadeGerenciadora'],r['nomeRazaoSocialFornecedor'],r['niFornecedor'],n(r['quantidadeHomologadaVencedor']),n(r['valorUnitario']),n(r['valorTotal']),r.get('numeroControlePncpCompra',''),int(considerado))).lastrowid

def list_consultas():
    with conn() as c: return [dict(x) for x in c.execute('SELECT c.id,i.codigo_catmat,i.descricao,c.data_analise,c.criterio_saneamento,c.preco_final FROM consultas c JOIN catmat_itens i ON i.id=c.catmat_item_id ORDER BY c.id DESC')]

def list_registros(qid):
    with conn() as c: return [dict(x) for x in c.execute('SELECT * FROM registros_precos WHERE consulta_id=? ORDER BY id',(qid,))]

def update_consulta_data(qid,data):
    with conn() as c: c.execute('UPDATE consultas SET data_analise=? WHERE id=?',(data,qid))

def delete_consulta(qid):
    with conn() as c: c.execute('DELETE FROM consultas WHERE id=?',(qid,))
