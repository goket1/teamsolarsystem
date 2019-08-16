create database SolarSystem;
use SolarSystem;

CREATE TABLE CelestialBody(
Name varchar(20) primary key,
Radius int,
Description Varchar(256),
Gravity float,
RotationSpeed float,
SurfaceTempLow float,
SurfaceTempHigh float,
CoreTemp float,
BodyType enum(
"Star","Dwarf Star","Nebula","Planet",
"Dwarf planet","Comet","BlackHole","Satelite")
);

CREATE TABLE OrbitRelation(
Centralbody Varchar(20),
OrbitingBody Varchar(20),
OrbitalSpeed float,
Distance float,
Foreign key(Centralbody) references CelestialBody(name),
Foreign key(OrbitingBody) references CelestialBody(name),
primary key(Centralbody,OrbitingBody)
);

CREATE TABLE PlanetRFIDMapping (
RFIDTag Varchar(32) primary key,
CelestialBody Varchar(20),
foreign key(CelestialBody) references CelestialBody(name)
);


CREATE TABLE Session(
Session Varchar(8) primary key
);

CREATE TABLE LastScanned(
RFIDTag Varchar(32) ,
LastScannedTs timestamp default Current_timestamp,
SessionID varchar(8),
foreign key(SessionID) REFERENCES Session(Session),
primary key(RFIDTag,LastScannedTs)
);