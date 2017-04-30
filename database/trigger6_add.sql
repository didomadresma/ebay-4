--Any new bid for a particular item must have a higher amount than any of the previous bids for that particular item.
PRAGMA foreign_keys = ON; 
drop trigger if exists trigger6_add;

CREATE  TRIGGER trigger6_add BEFORE INSERT 
ON Bids
for each row
BEGIN
	select raise(rollback, "Any new bid for a particular item must have a higher amount than any of the previous bids for that particular item.") where exists (select * from Bids where itemID==new.itemID and amount >= new.amount); 
END;
