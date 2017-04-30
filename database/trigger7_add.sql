--All new bids must be placed at the time which matches the current time of your AuctionBase system
PRAGMA foreign_keys = ON; 
drop trigger if exists trigger7_add;

CREATE  TRIGGER trigger7_add BEFORE INSERT 
ON Bids
for each row
BEGIN
	select raise(rollback, "All new bids must be placed at the time which matches the current time of your AuctionBase system") where new.time != (select curtime from Current_Time);
END;
