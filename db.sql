create database tiempo;
use tiempo;

create table Tiempo(
tiempo varchar(300),
CONSTRAINT pk_horacentral PRIMARY KEY(id)
)ENGINE=InnoDB;

create table TiempoBackup(
tiempo varchar(300),
CONSTRAINT pk_horacentral PRIMARY KEY(id)
)ENGINE=InnoDB;
