CREATE DATABASE IF NOT EXISTS Reloj;
use Reloj;

create table HoraCentral(
id      int(10) auto_increment not null,
hPrev   time,
hRef    time,
CONSTRAINT pk_horacentral PRIMARY KEY(id)
)ENGINE=InnoDB;

create table Equipos(
id          int(10) auto_increment not null,
ip          varchar(100) not null,
nombre      varchar(100) not null,
latencia    varchar(100) not null,
CONSTRAINT pk_equipos PRIMARY KEY(id)
)ENGINE=InnoDB;

create table HoraEquipos(
id          int(10) auto_increment not null,
idhSincr    int(10) not null,
idEquipo    int(10) not null,
hEquipo     varchar(100) not null, 
aEquipo     varchar(100) not null,
ralentizar  varchar(100) not null,
CONSTRAINT pk_horaequipos PRIMARY KEY(id),
CONSTRAINT fk_horacentral FOREIGN KEY(idhSincr) REFERENCES HoraCentral(id),
CONSTRAINT fk_equipos FOREIGN KEY(idEquipo) REFERENCES Equipos(id)
)ENGINE=InnoDB;

CREATE DATABASE IF NOT EXISTS RelojBackup;
use RelojBackup;

create table HoraCentral(
id      int(10) auto_increment not null,
hPrev   time,
hRef    time,
CONSTRAINT pk_horacentral PRIMARY KEY(id)
)ENGINE=InnoDB;

create table Equipos(
id          int(10) auto_increment not null,
ip          varchar(100) not null,
nombre      varchar(100) not null,
latencia    varchar(100) not null,
CONSTRAINT pk_equipos PRIMARY KEY(id)
)ENGINE=InnoDB;

create table HoraEquipos(
id          int(10) auto_increment not null,
idhSincr    int(10) not null,
idEquipo    int(10) not null,
hEquipo     varchar(100) not null, 
aEquipo     varchar(100) not null,
ralentizar  varchar(100) not null,
CONSTRAINT pk_horaequipos PRIMARY KEY(id),
CONSTRAINT fk_horacentral FOREIGN KEY(idhSincr) REFERENCES HoraCentral(id),
CONSTRAINT fk_equipos FOREIGN KEY(idEquipo) REFERENCES Equipos(id)
)ENGINE=InnoDB;
    