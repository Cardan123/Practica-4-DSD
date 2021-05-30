create database Central;
use Central;

create table requestBooks(
id      int(10), 
ip      varchar(100),
hora    varchar(100),
libros  varchar(100)
)ENGINE=InnoDB;

create table requestBooksBackup(
id      int(10), 
ip      varchar(100),
hora    varchar(100),
libros  varchar(100)
)ENGINE=InnoDB;

create table Sincronizar(
    id      int(10), 
    hora varchar(100)
)ENGINE=InnoDB;




