-- p.102 「カラム名の変更」
DROP TABLE IF EXISTS customer;

-- MEMO: customer_id のデータ型を CHAR(40) にしている
CREATE TABLE customer
(
    customer_id CHAR(40) PRIMARY KEY,
    fname       VARCHAR(40)
);



INSERT INTO customer (customer_id, fname)
VALUES ('32dc0ab2-e40d-431d-847b-90b5d4018890', 'Martin'),
       ('94f79825-c32f-4e1e-acec-5524d991b256', 'Ford'),
       ('fd10a16c-c7cc-4f8a-8114-7dc5d61c36c0', 'Tanaka')
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
VALUES ('843d5511-48c5-4b55-ba83-cabd0ff6253e', 'Suzuki');
select *
from customer;

-- 実験その2: 新しいカラム(first_name)にだけINSERTする
INSERT INTO customer (customer_id, first_name)
VALUES ('df566fbc-dc76-46cb-9560-14e5bfe16e2d', 'Yamada');

select *
from customer;

-- 実験その3: 元のカラム(fname)にだけUPDATEする
update customer
set fname = 'updated Suzuki'
where customer_id = '843d5511-48c5-4b55-ba83-cabd0ff6253e';

select *
from customer;

-- 実験その4: 新しいカラム(first_name)にだけUPDATEする
UPDATE customer
SET first_name = 'updated Yamada'
where customer_id = 'df566fbc-dc76-46cb-9560-14e5bfe16e2d';

select *
from customer;

-- 2007/06/14に実行する
-- DROP TRIGGER sample_trigger ON customer;
-- ALTER TABLE customer
--     DROP COLUMN fname;