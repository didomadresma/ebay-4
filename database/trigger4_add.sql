--No auction may have a bid before its start time or after its end time
PRAGMA foreign_keys = ON; 
drop trigger if exists trigger4_add;

CREATE  TRIGGER trigger4_add BEFORE INSERT 
ON Bids
for each row
BEGIN
	select raise(rollback, "No auction may have a bid before its start time or after its end time.") where exists (select * from Items where itemID==new.itemID and started > new.time) or exists (select * from Items where itemID == new.itemID and ends < new.time);
END;
