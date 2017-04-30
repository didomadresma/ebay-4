--A user may not bid on an item he or she is also selling
PRAGMA foreign_keys = ON; 
drop trigger if exists trigger2_add;

CREATE  TRIGGER trigger2_add BEFORE INSERT 
ON Bids
for each row
BEGIN
	 select raise(rollback, "A user may not bid on an item he or she is also selling.") where new.userID == (select sellerID from Items where Items.itemID == new.itemID) ;
END;
