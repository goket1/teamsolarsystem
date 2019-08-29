use solarsystem;

delimiter //
create procedure GetSessions()
begin
	select Session,LastscannedTs from session left outer join LastScanned on LastScanned.SessionID=session.Session group by session order by -LastscannedTs desc;
end //
delimiter ;