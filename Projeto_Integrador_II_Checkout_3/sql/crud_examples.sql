-- INSERT
INSERT INTO catmat_itens(codigo_catmat,descricao) VALUES('462546','Caneta esferografica');
INSERT INTO consultas(catmat_item_id,data_analise,criterio_saneamento,preco_final) SELECT id,'2026-09-04','50% acima/abaixo da mediana inicial',0.49 FROM catmat_itens WHERE codigo_catmat='462546';
-- SELECT
SELECT c.id,i.codigo_catmat,i.descricao,c.data_analise,c.preco_final FROM consultas c JOIN catmat_itens i ON i.id=c.catmat_item_id;
-- UPDATE
UPDATE consultas SET data_analise='2026-09-05' WHERE id=1;
-- DELETE (exemplo seguro)
DELETE FROM consultas WHERE id=999999;
