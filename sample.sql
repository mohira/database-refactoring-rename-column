-- p.102 「カラム名の変更」
DROP TABLE IF EXISTS customer;

-- https://www.postgresql.jp/document/9.4/html/datatype-numeric.html#DATATYPE-SERIAL
CREATE TABLE customer
(
    customer_id SERIAL,
    fname       VARCHAR(40)
);

INSERT INTO customer (fname)
VALUES ('Martin'),
       ('Ford'),
       ('Tanaka')
;

-- 1. 新しいカラムを導入する
ALTER TABLE customer
    ADD COLUMN first_name VARCHAR(40);

-- 2. 元のカラムを廃止予定にする
COMMENT ON COLUMN customer.first_name IS 'FNameカラムの名前を変更したもの。最終期日 = 2007/06/14';
COMMENT ON COLUMN customer.fname IS 'FirstNameに名前を変更。最終期日 = 2007/06/14';

-- 3. 同期用のトリガーを導入する
-- 試行錯誤用
DROP FUNCTION IF EXISTS synchronize_first_name() CASCADE;

CREATE OR REPLACE FUNCTION synchronize_first_name() RETURNS trigger AS
$synchronize_first_name$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        IF NEW.first_name IS NULL THEN
            NEW.first_name := NEW.fname ;
        END IF;
        IF NEW.Fname IS NULL THEN
            NEW.Fname := NEW.first_name;
        END IF;
    END IF;

    IF (TG_OP = 'UPDATE') THEN
        IF NOT (NEW.first_name = OLD.first_name) THEN
            NEW.fname := NEW.first_name;
        END IF;
        IF NOT (NEW.fname = OLD.fname) THEN
            NEW.first_name := NEW.fname;
        END IF;
    END IF;

    RETURN NEW;
END;
$synchronize_first_name$ LANGUAGE plpgsql;

CREATE TRIGGER sample_trigger
    BEFORE INSERT OR UPDATE
    ON customer
    FOR EACH ROW
EXECUTE function synchronize_first_name();



-- データの移行: FNameのすべての値を、first_nameにコピーする
-- MEMO: ゴリ押しだけど、ええんか？
UPDATE customer
SET first_name = fname;

-- 実験その1: 元のカラム(fname)にだけINSERTする
INSERT INTO customer (customer_id, fname)
VALUES (4, 'Suzuki');
select *
from customer;

-- 実験その2: 新しいカラム(first_name)にだけINSERTする
INSERT INTO customer (customer_id, first_name)
VALUES (5, 'Yamada');

select *
from customer;

-- 実験その3: 元のカラム(fname)にだけUPDATEする
update customer
set fname = 'updated Suzuki'
where customer_id = 4;

select *
from customer;

-- 実験その4: 新しいカラム(first_name)にだけUPDATEする
UPDATE customer
SET first_name = 'updated Yamada'
where customer_id = 5;

select *
from customer;

-- 2007/06/14に実行する
-- DROP TRIGGER sample_trigger ON customer;
-- ALTER TABLE customer
--     DROP COLUMN fname;