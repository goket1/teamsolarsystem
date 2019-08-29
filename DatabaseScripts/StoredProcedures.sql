use SolarSystem;

delimiter //
create procedure GetSessions()
begin
	select Session,LastscannedTs from Session left outer join LastScanned on LastScanned.SessionID=Session.Session group by Session order by -LastscannedTs desc;
end //
delimiter ;
