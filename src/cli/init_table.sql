-- テーブルの初期化
DROP TABLE IF EXISTS customer;

CREATE TABLE customer
(
    customer_id CHAR(36) PRIMARY KEY, -- UUID4を使うイメージ(書籍ではデータ型の指定はない)
    fname       VARCHAR(40)
);

-- 分かりやすくするための初期データ
INSERT INTO customer (customer_id, fname)
VALUES ('2c7ccd53-3367-4a7a-bf2c-6d4e3c0be10a', 'Martin'),
       ('ccc512e9-3293-49ea-a318-411abfad485d', 'Ford'),
       ('a6c543af-a582-4e2b-9348-34896575e97a', 'Tanaka')
;
