CREATE TABLE requestBooks(id Serial, ip text, hora text, libro text);

CREATE TABLE requestbooksbackup(id Serial, ip text, hora text, libro text);

INSERT INTO requestBooks(ip, hora, libro) VALUES ('192.0.0.0','12:12','Cracking');

SELECT * from requestBooks;