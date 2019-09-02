use SolarSystem;

delimiter //
create procedure GetSessions()
begin
	select Session,LastscannedTs from Session left outer join LastScanned on LastScanned.SessionID=Session.Session group by Session order by -LastscannedTs desc;
end //
delimiter ;
delimiter //
create
  procedure InsertSession(sessionID varchar(8))
BEGIN
    INSERT INTO `SolarSystem`.`Session` (`Session`) VALUES (sessionID);
END;
delimiter ;
delimiter //
create
    procedure PlanetScanned(sessionID varchar(8), rfid_uid varchar(32))
begin
    insert into LastScanned(rfidtag, sessionid) values(rfid_uid, sessionID);
end;
delimiter ;

delimiter //
create procedure GetPlanetInformation(session_id Varchar(32))
begin
	select Name,Radius,Description,Gravity,RotationSpeed,SurfaceTempAverage,CoreTemp,BodyType from CelestialBody join PlanetRFIDMapping on CelestialBody.Name = PlanetRFIDMapping.CelestialBody where PlanetRFIDMapping.RFIDTag = 
	(select RFIDTag from LastScanned where SessionID = session_id order by LastScannedTs desc limit 1);
end //
delimiter ;