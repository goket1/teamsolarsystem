use SolarSystem;

delimiter //
create procedure GetSessions()
begin
	select Session,LastscannedTs from Session left outer join LastScanned on LastScanned.SessionID=Session.Session group by Session order by -LastscannedTs desc;
end //
delimiter ;

create
  procedure InsertSession(sessionID varchar(8))
BEGIN
    INSERT INTO `SolarSystem`.`Session` (`Session`) VALUES (sessionID);
END;

create
    procedure PlanetScanned(sessionID varchar(8), rfid_uid varchar(32))
begin
    insert into LastScanned(rfidtag, sessionid) values(rfid_uid, sessionID);
end;
