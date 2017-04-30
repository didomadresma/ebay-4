import web

db = web.database(dbn='sqlite', db='auction.db')
######################BEGIN HELPER METHODS######################
# Enforce foreign key constraints
def enforceForeignKey(): db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction(): return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#   sqlitedb.query('[FIRST QUERY STATEMENT]')
#   sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#   t.rollback()
#   print str(e)
# else:
#   t.commit()
######################END HELPER METHODS########################


# returns the current time from your database
def getTime():
    db = web.database(dbn='sqlite', db='auction.db')
    query_string = 'select curtime from Current_Time'
    results = query(query_string)
    return results[0].curtime  # alternatively: return results[0]['time']

def setTime(new_time):
    t = db.transaction()
    try:
        db.update('Current_Time', where="curtime", curtime=new_time)
    except Exception as e:
        t.rollback()
        print str(e)
        return str(e)
    else:
        t.commit()
        return "success"
# returns a single item specified by the Item's ID in the database
def getItemById(item_id):
  q = 'select * from Items where itemID = $itemID'
  result = query(q, { 'itemID': item_id }) 
  try:
    return result
  except IndexError:
    return None

def getBidsByItemId(itemID):
  q = 'select * from Bids where itemID = $itemID order by time desc'
  return query(q, {'itemID': itemID})

# returns a single item specified by the Item's ID in the database
def getUserById(user_id):
  q = 'select * from Users where userID = $userID'
  result = query(q, { 'userID': user_id })

  try:
    return result[0]
  except IndexError:
    return None

def updateItemEndTime(itemID, new_end_time):
    t = db.transaction()
    try:
        db.update('Items', where='itemID = ' + itemID, ends=new_end_time)
    except Exception as e:
        t.rollback()
        print str(e)
        return str(e)
    else:
        t.commit()
        return "success" 

def addBid(itemID, price, userID, current_time):
    t = db.transaction()
    try:
        q = 'select numberOfBids from items where itemID = $itemID'
        result = query(q, {'itemID': itemID})
        new_num_of_bids = result[0].numberOfBids + 1
    
        db.update('Items', where='itemID=$id', vars={'id':itemID}, numberOfBids=new_num_of_bids)
        db.update('Items', where='itemID=$id', vars={'id':itemID}, currently=price)
        db.update('Items', where='itemID=$id', vars={'id':itemID}, firstBid=price)
        db.insert('Bids', itemID=itemID, amount=price, userID=userID, time=current_time)
    except Exception as e:
        t.rollback()
        print str(e)
        return str(e)
    else:
        t.commit()
        return "success"    


def addUser(userID, rating, location, country):
    t = db.transaction()
    try:
        db.insert('Users', userID=userID, rating=rating, location=location, country=country)
    except Exception as e:
        t.rollback()
        print str(e)
        return str(e)
    else:
        t.commit()
        return "success"     

def getCategory(itemID):
    q = 'select category from Categories where itemID = $itemID'
    result = query(q, { 'itemID': itemID })
    try:
        return result
    except IndexError:
        return None
    
def searchItems(category, description, minPrice, maxPrice, status):
    q = 'select * from Items'

    if (minPrice != '') or (maxPrice != '') or (status != 'all') or (category !='') or (description != ''):
        q += ' where '

    if (minPrice != ''):
        q += ' currently >= ' + minPrice
    
    if (maxPrice != ''):
        if (minPrice != ''):
            q += ' AND '
        q += ' currently <= ' + maxPrice
    
    if (status != 'all'):
        if (minPrice != '') or (maxPrice != ''):
            q += ' AND '
        if status == 'open':
            q += 'ends >= (select curtime from current_time) and started <= (select curtime from current_time)'
        if status == 'close':
            q += 'ends < (select curtime from current_time)'
        if status == 'notStarted':
            q += 'started > (select curtime from current_time)'      

    if (category != ''):
        if (minPrice != '') or (maxPrice != '') or (status !='all'):
            q += ' AND '
        q += 'itemID in (select itemID from categories where category like' + "'%" + category + "%')"  
    
    if (description != ''):
        if (minPrice != '') or (maxPrice != '') or (status !='all') or (category !=''):
            q += ' AND '
        q += 'description like ' + "'%" + description + "%'"

    return query(q)
    
def getWinnerId(itemID):
  q = 'select userID from Bids '
  q += 'where itemID = $itemID '
  q += 'and amount = ('
  q += 'select max(amount) from Bids '
  q += 'where itemID = $itemID'
  q += ')'
  
  result = query(q, { 'itemID': itemID })

  try:
    return result[0].userID
  except IndexError:
    return None

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars={}):
  return list(db.query(query_string, vars))



#####################END HELPER METHODS#####################
