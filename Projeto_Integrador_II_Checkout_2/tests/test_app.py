import os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
os.environ["DEMO_MODE"]="1"
from app import app,fetch_data,process_result

def test_dataset():
    p=fetch_data("462546")
    assert len(p["resultado"])==53
    r=process_result(p)
    assert r["original_count"]==53
    assert r["sanitized_count"]==28
    assert len(r["rows"])==53
    assert sum(x["considerado"] for x in r["rows"])==28
    assert r["final_price"]==0.49

def test_api():
    r=app.test_client().get("/api/consulta?catmat=462546")
    assert r.status_code==200
    assert len(r.get_json()["rows"])==53

def test_validation():
    r=app.test_client().get("/api/consulta?catmat=abc")
    assert r.status_code==400
