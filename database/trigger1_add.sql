--The Current_Price of an item must always match the Amount of the most recent bid for that item
PRAGMA foreign_keys = ON; 
drop trigger if exists trigger1_add;

CREATE  TRIGGER trigger1_add BEFORE INSERT 
ON Items
for each row
BEGIN
	 select raise(rollback, "The Current_Price of an item must always match the Amount of the most recent bid for that item.") where new.currently != (select max(amount) from Bids where itemID == new.itemID) ;
END;
