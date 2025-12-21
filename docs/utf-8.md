## Change ASCII to UTF-8

SET client_encoding = 'UTF8';
UPDATE pg_database SET datcollate='ru_RU.UTF-8', datctype='ru_RU' WHERE datname='booking';
UPDATE pg_database set encoding = pg_char_to_encoding('UTF8') where datname = 'booking';