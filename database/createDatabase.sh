#!/bin/bash

sqlite3 auction.db < create.sql
sqlite3 auction.db < load.txt 
sqlite3 auction.db < constraints_verify.sql
sqlite3 auction.db < trigger1_add.sql 
sqlite3 auction.db < trigger2_add.sql
sqlite3 auction.db < trigger3_add.sql
sqlite3 auction.db < trigger4_add.sql
sqlite3 auction.db < trigger5_add.sql
sqlite3 auction.db < trigger6_add.sql
sqlite3 auction.db < trigger7_add.sql
#we need the ability to modify the "current_time", so I remove this trigger 
#sqlite3 auction.db < trigger8_add.sql

