from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import db

def test_crud(tmp_path,monkeypatch):
    monkeypatch.setattr(db,'DB_PATH',tmp_path/'t.db'); db.init_db()
    cid=db.upsert_catmat('462546','Caneta'); q=db.create_consulta(cid,'2026-09-04','criterio',.49)
    db.create_registro(q,{'numeroAtaRegistroPreco':'00001/2026','nomeUnidadeGerenciadora':'UG','nomeRazaoSocialFornecedor':'Fornecedor','niFornecedor':'12345678000190','quantidadeHomologadaVencedor':'10','valorUnitario':'0,49','valorTotal':'4,90','numeroControlePncpCompra':''},True)
    assert len(db.list_consultas())==1 and len(db.list_registros(q))==1
    db.update_consulta_data(q,'2026-09-05'); assert db.list_consultas()[0]['data_analise']=='2026-09-05'
    db.delete_consulta(q); assert db.list_consultas()==[]
