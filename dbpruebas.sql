CREATE DATABASE IF NOT EXISTS RelojPrueba;
use RelojPrueba;

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

insert into HoraCentral (id,hPrev,hRef) values (1,"13:00:00","14:00:00");
insert into HoraCentral (id,hPrev,hRef) values (2,"15:00:00","16:00:00");
insert into HoraCentral (id,hPrev,hRef) values (3,"17:00:00","18:00:00");
insert into HoraCentral (id,hPrev,hRef) values (4,"19:00:00","20:00:00");

insert into Equipos (id,ip,nombre,latencia) values (1,"192.168.1.2","CardanPC","90ms");
insert into Equipos (id,ip,nombre,latencia) values (2,"192.168.1.3","CardanPC","90ms");
insert into Equipos (id,ip,nombre,latencia) values (3,"192.168.1.4","CardanPC","90ms");
insert into Equipos (id,ip,nombre,latencia) values (4,"192.168.1.5","CardanPC","90ms");

insert into HoraEquipos (id,idhSincr,idEquipo,hEquipo,aEquipo) values (1,1,1)