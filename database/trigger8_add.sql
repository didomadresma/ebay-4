--The current time of your AuctionBase system can only advance forward in time, not backward in time.
PRAGMA foreign_keys = ON; 
drop trigger if exists trigger8_add;

CREATE  TRIGGER trigger8_add BEFORE UPDATE
ON Current_Time
for each row
BEGIN
	select raise(rollback, "The current time of your AuctionBase system can only advance forward in time, not backward in time.") where new.curtime <= (select curtime from Current_Time);
END;
