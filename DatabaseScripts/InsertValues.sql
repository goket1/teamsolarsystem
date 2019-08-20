use solarsystem;

insert into CelestialBody(
Name,Radius,Description,Gravity,RotationSpeed,SurfaceTempAverage,CoreTemp,BodyType) 
values
("Sun",	696265	,"This is the life giving Star we know as the sun",	273.6153,	30,	5505,	17000000,	"Star"),
("Mercury",	2439.5	,"This planet that is the closest to the sun",	3.72666,	58.7,	14.9,	1250,	"Planet"),
("Venus",	6052	,"This is the second planet from the sun often seen of Earth twin planet",	8.8263,	-243,	482,	4926.85,	"Planet"),
("Earth",	6378	,"This is the blue planet we call home",	9.807,	1,	15,	6000,	"Planet"),
("Mars",	3402.5	,"The Red planet that located a further out in the solar system",	3.72666,	1.025833333,	-55,	1230,	"Planet"),
("Jupiter",	71490	,"The Biggest Gas planet we there is around the sun",	24.81171,	0.41,	-153,	35000, 	"Planet"),
("Saturn",	60270	,"The planet with large rings",	10.39542,	0.42625,	-185,	11.700,	"Planet"),
("Uranus",	25560	,"This is the  Third largest planet Neptune and Uranus is similar to each other",	8.8263,	0.712083333,	-197,	4737,	"Planet"),
("Neptune",	24765	,"This Is a blue gas planet that is far from that have",	11.17998,	0.8,	-225,	7000,	"Planet"),
("Pluto",	1153	,"Pluto was once considered to be a planet",	0.78456,	6.4,	-233,	null,	"Dwarf Planet"),
("Moon", 1737.1,"This the object that lights up the night", 1.62,27.322,-53.15,1426.667,"Satelite");



insert into PlanetRFIDMapping(RFIDTag,CelestialBody) values
("04a9f9aaa24080", "Earth"),
("0458f8aaa24080","Mars");

insert into orbitrelation(Centralbody,OrbitingBody,Distance,OrbitalSpeed) values
("Sun",	"Mercury",	57910000,	47.89),
("Sun",	"Venus",	108200000,	35.03),
("Sun",	"Earth",	149597870,	29.79),
("Sun",	"Mars",	227940000,	24.13),
("Sun",	"Jupiter",	778330000,	13.06),
("Sun",	"Saturn",	1426980000,	9.64),
("Sun",	"Uranus",	2870990000,	6.81),
("Sun",	"Neptune",	4497070000,	5.43),
("Sun",	"Pluto",	5913520000,	4.74);
