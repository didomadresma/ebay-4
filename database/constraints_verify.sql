--1
select "error" from Users where (select count(*) from Users) != (select count(distinct userID) from Users);
--2
select "conflict 2" from Items where sellerID not in (select userID from Users);
select "conflict 2" from Bids where userID not in (select userID from Users);
--3
select "conflict 3" from Items where (select count(*) from Items) != (select count(distinct itemID) from Items);

--4
select "conflict 4" from Bids where Bids.itemID not in(select itemID from Items);

--5
select "conflict 5" from Categories where Categories.itemID not in (select itemID from Items);

--6
select "conflict 6" from Categories group by itemID,category having count(*)>1;

--7
select "conflict 7" from Items where started>=ends;

--8
select "conflict 8" from Items where currently != (select amount from Bids where itemID==Items.itemID order by time desc limit 1);
--select itemID,currently from Items where currently == (select amount from Bids where itemID==Items.itemID order by time desc limit 1);

--9
--select "conflict 9" from Users,Items,Bids where Users.userID==Items.sellerID and Users.userID == Bids.userID and Items.itemID == Bids.itemID;

--10
select "conflict 10" from Bids group by itemID,time having count(*) > 1;

--11
select "conflict 11" from Items,Bids where Items.itemID==Bids.itemID and (Items.started>Bids.time or Items.ends < Bids.time);

--12
select "conflict 12" from Bids group by itemID,userID,amount having count(*) > 1;

--13
select "conflict 13" from Items where Items.numberOfBids != (select count(*) from Bids where Bids.itemID == Items.itemID);

--14
select "conflict 14" from Bids a, Bids b where a.itemID == b.itemID and a.time < b.time and a.amount > b.amount;

--15
--select "conflict 15" from Bids,Current_Time where Bids.time > Current_Time.curtime;
select "conflict 15" where (select curtime from Current_Time) < (select max(time) from Bids);

--16
select "conflict 16" where (select count(*) from Current_Time) > 1;


