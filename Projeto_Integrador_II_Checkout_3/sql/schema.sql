PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS catmat_itens(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 codigo_catmat TEXT NOT NULL UNIQUE,
 descricao TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS consultas(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 catmat_item_id INTEGER NOT NULL,
 data_analise TEXT NOT NULL,
 criterio_saneamento TEXT NOT NULL,
 preco_final REAL NOT NULL CHECK(preco_final>=0),
 criada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(catmat_item_id) REFERENCES catmat_itens(id) ON UPDATE CASCADE ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS registros_precos(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 consulta_id INTEGER NOT NULL,
 numero_ata TEXT NOT NULL,
 unidade_gerenciadora TEXT NOT NULL,
 fornecedor TEXT NOT NULL,
 cnpj TEXT NOT NULL,
 quantidade REAL NOT NULL CHECK(quantidade>=0),
 valor_unitario REAL NOT NULL CHECK(valor_unitario>=0),
 valor_total REAL NOT NULL CHECK(valor_total>=0),
 link_pncp TEXT,
 considerado INTEGER NOT NULL DEFAULT 0 CHECK(considerado IN(0,1)),
 FOREIGN KEY(consulta_id) REFERENCES consultas(id) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_consultas_catmat ON consultas(catmat_item_id);
CREATE INDEX IF NOT EXISTS idx_registros_consulta ON registros_precos(consulta_id);
