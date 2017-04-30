#!/usr/bin/env python
import sys; sys.path.insert(0, 'lib')  # this line is necessary for the rest
import os  # of the imports to work!
import web
import sqlitedb
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

######################BEGIN HELPER METHODS######################
def string_to_time(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})
    
    jinja_env = Environment(autoescape=True,
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        extensions=extensions,)
    jinja_env.globals.update(globals)
    
    web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
    return jinja_env.get_template(template_name).render(context)
#####################END HELPER METHODS#####################

# first parameter => URL, second parameter => class name
urls = (
    '/', 'index',
    '/current_time', 'current_time',
    '/select_time', 'select_time',
    '/add_bid', 'add_bid',
    '/add_user', 'add_user',
    '/search_item', 'search_item',
    '/view_item', 'view_item',
    '/search_result', 'search_result'
    
)


class index:
    def GET(self):
        return render_template('index.html')

class current_time:
    def GET(self):
        current_time = sqlitedb.getTime()
        return render_template('curr_time.html', time=current_time)

class select_time:
    def GET(self):
        return render_template('select_time.html')

    def POST(self):
        post_params = web.input()
        
        MM = post_params['MM']
        dd = post_params['dd']
        yyyy = post_params['yyyy']
        HH = post_params['HH']
        mm = post_params['mm']
        ss = post_params['ss'];
        enter_name = post_params['entername']

        selected_time = '%s-%s-%s %s:%s:%s' % (yyyy, MM, dd, HH, mm, ss)
        update_message = '(Hello, %s. Previously selected time was: %s.)' % (enter_name, selected_time)
        
        # function setTime will return "error" or "success" to represent the status of the database operation
        result = sqlitedb.setTime(selected_time)
        if result != "success":
           return render_template('select_time.html', message="ERROR! " + result) 
        # print result
        return render_template('select_time.html', message=update_message)

class add_bid:

    # A GET request to the URL '/add_bid'
    def GET(self):
        return render_template('add_bid.html')

    # A POST request to the URL '/add_bid'
    def POST(self):
        post_params = web.input()

        itemID = post_params['itemID']
        price = post_params['price']
        userID = post_params['userID']
        current_time = sqlitedb.getTime()

        ### Many ways to fail... #######################################
        # (1) All fields must be filled
        if (itemID == '') or (price == '') or (userID == ''):
            return render_template('add_bid.html', message='You must fill out every field')
   
        # (2) There must be an item with that ID
        if not len(sqlitedb.getItemById(itemID)):
            return render_template('add_bid.html', message='There are no items with that ID')
        
        item_row = sqlitedb.getItemById(itemID)[0]
        # (3) Users can't bid on closed auction items
        if (string_to_time(item_row.ends) <= string_to_time(current_time)):
            return render_template('add_bid.html', message='That auction is already closed for time')

        # (4) Users can't bid on auction items that have not been opened
        if (string_to_time(item_row.started) >= string_to_time(current_time)):
            return render_template('add_bid.html', message='That auction has not started yet, Please wait')
        # (4) UserID must correspond to an existing user in User table
        user_row = sqlitedb.getUserById(userID);
        if user_row == None:
            return render_template('add_bid.html', message='There are no users with that ID')
      
        # (5) An user may not bid on an item he or she is also selling
        if userID == item_row.sellerID:
            return render_template('add_bid.html', message='You can not bid on the item you are selling')
        
        # (6) Don't accept bids <= current highest bid
        if float(price) <= float(item_row.currently):
            return render_template('add_bid.html', message='You must make a bid higher than the current price ' 
                               + str(item_row.currently))

        ### ... but it's possible to succeed :P ########################

        # A bid at the buy_price closes the auction
        if(item_row.buyPrice != None):
            if (float(price) >= float(item_row.buyPrice)):
                r1 = sqlitedb.addBid(itemID, price, userID, current_time)
                if r1 != "success":
                    return render_template("add_bid.html", message="ERROR! " + r1)
                # Update ends to current_time
                r2 = sqlitedb.updateItemEndTime(itemID, current_time);
                if r2 != "success":
                   return render_template("add_bid.html", message="ERROR! " + r1) 
                
                return render_template('add_bid.html',
                        message='Congratulations! You just closed that auction by making a bid at or above the buy price',
                        add_result="success")
                
        # Add bid to Bid table in db
        r3 = sqlitedb.addBid(itemID, price, userID, current_time)
        if r3 != "success":
            return render_template("add_bid.html", message="ERROR! " + r3)
        elif r3 == "success":
            return render_template('add_bid.html',
                message='Success! You\'ve just placed a bid on ' + item_row.name + '(' + itemID + ')',
                add_result="success")

class add_user:
    def GET(self):
        return render_template('add_user.html')
    
    def POST(self):
        post_params = web.input()

        userID = post_params['userID']
        rating = 0.0
        location = post_params['location']
        country = post_params['country']

        # (1) All fields must be filled
        if (userID == '') or (location == '') or (country == ''):
            return render_template('add_user.html', message='You must fill out every field')

        user_row = sqlitedb.getUserById(userID)
        
        # (2) The user should not register before
        if user_row != None:
            return render_template('add_user.html', message='You have already been an auction user!')
        
        result = sqlitedb.addUser(userID, rating, location, country)
        if result != "success":
            return render_template("add_user.html", message="ERROR! " + result)
        
        return render_template('add_user.html', message='Welcome ' + userID + ' to the Auction System', add_result="success")

class search_item:
    def GET(self):
        return render_template('search_item.html')


class search_result:
    def GET(self): 
        return render_template('search_result.html')
    
    def POST(self):
        post_params = web.input()

        itemID = post_params['itemID']
        category = post_params['category']
        description = post_params['description']
        minPrice = post_params['min']
        maxPrice = post_params['max']
        status = post_params['status']

        if (itemID == '') and (category == '') and (description == '') and (minPrice == '') and (maxPrice == ''):
            return render_template('search_item.html', message="At least ONE condition should be taken")
         
        if itemID != "":
            result = sqlitedb.getItemById(itemID)
            if len(result):
                return render_template('search_result.html', result=result)
            else:
                return render_template('search_item.html', message="This Auction does not exist")
         
        result = sqlitedb.searchItems(category,description,minPrice,maxPrice,status)
        return render_template('search_result.html', result=result)
    
class view_item:
    def GET(self):
        current_time = sqlitedb.getTime()
        if web.input() :
            get_params = web.input()
            itemID = get_params['itemID']
            categories = sqlitedb.getCategory(itemID)
            category=''
            for i in categories:
                print i
                category += i['category']+";"
            if len(sqlitedb.getItemById(itemID)):
                item = sqlitedb.getItemById(itemID)[0]
                stime = item.started
                etime = item.ends
                bids = sqlitedb.getBidsByItemId(itemID)
                status = "Closed"
                if (string_to_time(current_time) >= string_to_time(stime)) and (string_to_time(current_time) <= string_to_time(etime)):
                    status = "Opening"
                if status == "Closed":
                    winner = sqlitedb.getWinnerId(itemID)
                    return render_template('item_detail.html', result=item, status=status, winner=winner, bids=bids,category=category)
                else:
                    return render_template('item_detail.html', result=item, status=status, bids=bids,category=category)
            else:
                return render_template('item_detail.html', error="Sorry, this auction does not exist!")
        else:
            return render_template('item_detail.html')

###########################################################################################
##########################DO NOT CHANGE ANYTHING BELOW THIS LINE!##########################
###########################################################################################

if __name__ == '__main__':
  web.internalerror = web.debugerror
  app = web.application(urls, globals())
  app.add_processor(web.loadhook(sqlitedb.enforceForeignKey))
  app.run()
