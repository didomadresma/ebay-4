--No auction may have two bids at the exact same time
PRAGMA foreign_keys = ON; 
drop trigger if exists trigger3_add;

CREATE  TRIGGER trigger3_add BEFORE INSERT 
ON Bids
for each row
BEGIN
	 select raise(rollback, "No auction may have two bids at the exact same time.") where new.time in (select time from Bids where itemID == new.itemID) ;
END;
