--In every auction, the Number_of_Bids attribute corresponds to the actual number of bids for that particular item
PRAGMA foreign_keys = ON; 
drop trigger if exists trigger5_add;

CREATE  TRIGGER trigger5_add AFTER INSERT 
ON Bids
for each row
BEGIN
	select raise(rollback, "the Number_of_Bids attribute  should corresponds to the actual number of bids for that particular item.") where (select numberOfBids from Items where Items.itemID == new.itemID) != (select count(*) from Bids where Bids.itemID == new.itemID);
END;
