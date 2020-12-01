import os
import sqlite3

from flask import Flask, render_template, request, redirect, url_for

from form import commitChange, newItem, newCombination, rollBack, comboItem

"""
AUTHORS

Trish Beeksma
Alex Mello
Matthew Siebold
"""


# helper function - convert list -> tuple
def convert(list):
    # return tuple
    return tuple(i for i in list)


# helper fuction - combine list of lists -> list
def combine(list):
    newList = []
    for subList in list:
        for item in subList:
            newList.append(item)

    # return list
    return newList


# get checkbox data
def getCheckboxes():
    checkboxData = []
    checkboxData.append(request.form.getlist('restaurant'))
    checkboxData.append(request.form.getlist('foodtype'))
    checkboxData.append(request.form.getlist('price'))
    checkboxData.append(request.form.getlist('calories'))
    checkboxData.append(request.form.getlist('carbs'))
    checkboxData.append(request.form.getlist('protein'))
    checkboxData.append(request.form.getlist('fat'))

    # return data as list of lists
    return checkboxData


# run the query
def runQuery(queryString):
    # execute query
    c.execute(queryString)
    # returns list of tuples
    queryData = c.fetchall()
    # convert list of tuples -> tuple of tuples
    queryData = convert(queryData)

    # return data as tuple of tuples
    return queryData


# create the query string
def createItemsQuery(checkboxData):
    # empty query
    emptyQuery = "select restaurant.restaurantName, itemName, itemPrice, item_foodtype.foodtype, itemCalories, itemCarbs, itemProtein, itemFat \
    from items \
    inner join item_foodtype on items.itemID=item_foodtype.itemID \
    inner join restaurant_items on items.itemID = restaurant_items.itemID \
    inner join restaurant on restaurant_items.restaurantID = restaurant.restaurantID where 1=0;"

    # base query
    queryString = "select subquery.* from (select restaurant.restaurantName, itemName, itemPrice, item_foodtype.foodtype, itemCalories, itemCarbs, itemProtein, itemFat \
    from items \
    inner join item_foodtype on items.itemID=item_foodtype.itemID \
    inner join restaurant_items on items.itemID = restaurant_items.itemID \
    inner join restaurant on restaurant_items.restaurantID = restaurant.restaurantID where ("

    # restaurant part of query
    restaurantPieces = 0
    if checkboxData.__contains__('restaurant1'):
        queryString += 'restaurant.restaurantName = "Burger King" '
        restaurantPieces += 1
    if checkboxData.__contains__('restaurant2'):
        if restaurantPieces > 0:
            queryString += 'or '
        queryString += 'restaurant.restaurantName = "Chick-Fil-A" '
        restaurantPieces += 1
    if checkboxData.__contains__('restaurant3'):
        if restaurantPieces > 0:
            queryString += 'or '
        queryString += 'restaurant.restaurantName = "Wendys" '
        restaurantPieces += 1

    if restaurantPieces == 0:
        return emptyQuery
    queryString += ") and ("

    # foodtype part of query
    foodtypePieces = 0
    if checkboxData.__contains__('foodtype1'):
        if foodtypePieces > 0:
            queryString += 'or '
        queryString += 'item_foodtype.foodtype = "Entree" '
        foodtypePieces += 1
    if checkboxData.__contains__('foodtype2'):
        if foodtypePieces > 0:
            queryString += 'or '
        queryString += 'item_foodtype.foodtype = "Side" '
        foodtypePieces += 1
    if checkboxData.__contains__('foodtype3'):
        if foodtypePieces > 0:
            queryString += 'or '
        queryString += 'item_foodtype.foodtype = "Drink" '
        foodtypePieces += 1
    if checkboxData.__contains__('foodtype4'):
        if foodtypePieces > 0:
            queryString += 'or '
        queryString += 'item_foodtype.foodtype = "Dessert" '
        foodtypePieces += 1

    if foodtypePieces == 0:
        return emptyQuery
    queryString += ") and ("

    # price part of query
    pricePieces = 0
    if checkboxData.__contains__('price1'):
        queryString += "(itemPrice>=0 and itemPrice<=1) "
        pricePieces += 1
    if checkboxData.__contains__('price2'):
        if pricePieces > 0:
            queryString += 'or '
        queryString += "(itemPrice>=1 and itemPrice<=2) "
        pricePieces += 1
    if checkboxData.__contains__('price3'):
        if pricePieces > 0:
            queryString += 'or '
        queryString += "(itemPrice>=2 and itemPrice<=3) "
        pricePieces += 1
    if checkboxData.__contains__('price4'):
        if pricePieces > 0:
            queryString += 'or '
        queryString += "(itemPrice>=3 and itemPrice<=4) "
        pricePieces += 1
    if checkboxData.__contains__('price5'):
        if pricePieces > 0:
            queryString += 'or '
        queryString += "(itemPrice>=4 and itemPrice<=5) "
        pricePieces += 1
    if checkboxData.__contains__('price6'):
        if pricePieces > 0:
            queryString += 'or '
        queryString += "(itemPrice>=5) "
        pricePieces += 1

    if pricePieces == 0:
        return emptyQuery
    queryString += ") and ("

    # calories part of query
    caloriesPieces = 0
    if checkboxData.__contains__('calories1'):
        queryString += "(itemCalories>=0 and itemCalories<=100) "
        caloriesPieces += 1
    if checkboxData.__contains__('calories2'):
        if caloriesPieces > 0:
            queryString += 'or '
        queryString += "(itemCalories>=100 and itemCalories<=300) "
        caloriesPieces += 1
    if checkboxData.__contains__('calories3'):
        if caloriesPieces > 0:
            queryString += 'or '
        queryString += "(itemCalories>=300 and itemCalories<=500) "
        caloriesPieces += 1
    if checkboxData.__contains__('calories4'):
        if caloriesPieces > 0:
            queryString += 'or '
        queryString += "(itemCalories>=500 and itemCalories<=700) "
        caloriesPieces += 1
    if checkboxData.__contains__('calories5'):
        if caloriesPieces > 0:
            queryString += 'or '
        queryString += "(itemCalories>=700 and itemCalories<=900) "
        caloriesPieces += 1
    if checkboxData.__contains__('calories6'):
        if caloriesPieces > 0:
            queryString += 'or '
        queryString += "(itemCalories>=900) "
        caloriesPieces += 1

    if caloriesPieces == 0:
        return emptyQuery
    queryString += ")"

    # return query as string
    queryString += ") subquery;"
    return queryString


# create the query string
def createCombinationsQuery(checkboxData):
    # empty query
    emptyQuery = "select restaurant.restaurantName, combinations.combinationName, \
    sum(items.itemCalories) as calories, sum(items.itemCarbs) as carbs, sum(items.itemProtein) as protein, sum(items.itemFat) as fat from combinations \
    inner join restaurant_combinations on combinations.combinationID=restaurant_combinations.combinationID \
    inner join restaurant on restaurant_combinations.restaurantID=restaurant.restaurantID \
    inner join combination_items on combinations.combinationID = combination_items.combinationID \
    inner join items on combination_items.itemID = items.itemID \
    where 1=0 \
    group by combinations.combinationID;"

    # base query
    queryString = "select subquery.* from (select restaurant.restaurantName, combinations.combinationName, \
    sum(items.itemCalories) as calories, sum(items.itemCarbs) as carbs, sum(items.itemProtein) as protein, sum(items.itemFat) as fat from combinations \
    inner join restaurant_combinations on combinations.combinationID=restaurant_combinations.combinationID \
    inner join restaurant on restaurant_combinations.restaurantID=restaurant.restaurantID \
    inner join combination_items on combinations.combinationID = combination_items.combinationID \
    inner join items on combination_items.itemID = items.itemID \
    group by combinations.combinationID \
    having ("

    # calories part of query
    caloriesPieces = 0
    if checkboxData.__contains__('calories1'):
        queryString += "(calories>=0 and calories<=400) "
        caloriesPieces += 1
    if checkboxData.__contains__('calories2'):
        if caloriesPieces > 0:
            queryString += 'or '
        queryString += "(calories>=400 and calories<=800) "
        caloriesPieces += 1
    if checkboxData.__contains__('calories3'):
        if caloriesPieces > 0:
            queryString += 'or '
        queryString += "(calories>=800 and calories<=1200) "
        caloriesPieces += 1
    if checkboxData.__contains__('calories4'):
        if caloriesPieces > 0:
            queryString += 'or '
        queryString += "(calories>=1200 and calories<=1600) "
        caloriesPieces += 1
    if checkboxData.__contains__('calories5'):
        if caloriesPieces > 0:
            queryString += ' or '
        queryString += "(calories>=1600) "
        caloriesPieces += 1

    if caloriesPieces == 0:
        return emptyQuery
    queryString += ") and ( "

    # carbs part of query
    carbsPieces = 0
    if checkboxData.__contains__('carbs1'):
        queryString += "(carbs>=0 and carbs<=40) "
        carbsPieces += 1
    if checkboxData.__contains__('carbs2'):
        if carbsPieces > 0:
            queryString += 'or '
        queryString += "(carbs>=40 and carbs<=80) "
        carbsPieces += 1
    if checkboxData.__contains__('carbs3'):
        if carbsPieces > 0:
            queryString += 'or '
        queryString += "(carbs>=80 and carbs<=120) "
        carbsPieces += 1
    if checkboxData.__contains__('carbs4'):
        if carbsPieces > 0:
            queryString += 'or '
        queryString += "(carbs>=120 and carbs<=160) "
        carbsPieces += 1
    if checkboxData.__contains__('carbs5'):
        if carbsPieces > 0:
            queryString += ' or '
        queryString += "(carbs>=160) "
        carbsPieces += 1

    if carbsPieces == 0:
        return emptyQuery
    queryString += ") and ( "

    # protein part of query
    proteinPieces = 0
    if checkboxData.__contains__('protein1'):
        queryString += "(protein>=0 and protein<=15) "
        proteinPieces += 1
    if checkboxData.__contains__('protein2'):
        if proteinPieces > 0:
            queryString += 'or '
        queryString += "(protein>=15 and protein<=30) "
        proteinPieces += 1
    if checkboxData.__contains__('protein3'):
        if proteinPieces > 0:
            queryString += 'or '
        queryString += "(protein>=30 and protein<=45) "
        proteinPieces += 1
    if checkboxData.__contains__('protein4'):
        if proteinPieces > 0:
            queryString += 'or '
        queryString += "(protein>=45 and protein<=60) "
        proteinPieces += 1
    if checkboxData.__contains__('protein5'):
        if proteinPieces > 0:
            queryString += ' or '
        queryString += "(protein>=60) "
        proteinPieces += 1

    if proteinPieces == 0:
        return emptyQuery
    queryString += ") and ( "

    # fat part of query
    fatPieces = 0
    if checkboxData.__contains__('fat1'):
        queryString += "(fat>=0 and fat<=20) "
        fatPieces += 1
    if checkboxData.__contains__('fat2'):
        if fatPieces > 0:
            queryString += 'or '
        queryString += "(fat>=20 and fat<=40) "
        fatPieces += 1
    if checkboxData.__contains__('fat3'):
        if fatPieces > 0:
            queryString += 'or '
        queryString += "(fat>=40 and fat<=60) "
        fatPieces += 1
    if checkboxData.__contains__('fat4'):
        if fatPieces > 0:
            queryString += 'or '
        queryString += "(fat>=60 and fat<=80) "
        fatPieces += 1
    if checkboxData.__contains__('fat5'):
        if fatPieces > 0:
            queryString += ' or '
        queryString += "(fat>=80) "
        fatPieces += 1

    if fatPieces == 0:
        return emptyQuery
    queryString += ")"

    # return query as string
    queryString += ") subquery;"
    return queryString


# format restaurant times
def formatRestaurantData(restaurantData):
    # list of data
    dataList = []
    formattedDataList = []

    # convert tuple of tuples -> list of lists
    for i in range(len(restaurantData)):
        dataList.append(list(restaurantData[i]))

    # format individual times
    for i in range(len(dataList)):
        for j in range(5, len(dataList[i])):
            # if value is not None
            if dataList[i][j] != None:
                # remove leading zero
                if dataList[i][j][0] == '0':
                    dataList[i][j] = dataList[i][j][1:]
                # remove trailing zeros
                if dataList[i][j][-2:] == '00':
                    dataList[i][j] = dataList[i][j][:-3]
                # if 10-12 times add AM
                if dataList[i][j][:2] in ['24', '10', '11']:
                    dataList[i][j] = dataList[i][j] + 'AM'
                # if 13-24 times add PM
                elif dataList[i][j][:2] in ['12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']:
                    pass
                # if 1-9 times add AM
                else:
                    dataList[i][j] = dataList[i][j] + 'AM'
                # convert 13-24 to 1-12
                if dataList[i][j][:2] in ['12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']:
                    value = [None, '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'].index(
                        dataList[i][j][:2])
                    dataList[i][j] = str(value) + 'PM'

    # format day times
    for i in range(len(dataList)):
        # duplicate first 5 items
        formattedDataList.append(dataList[i][0:5])

        # merge open and close times
        for j in range(5, len(dataList[i]), 2):
            if dataList[i][j] == None or dataList[i][j + 1] == None:
                formattedDataList[i].append('Closed')
            else:
                formattedDataList[i].append(dataList[i][j] + " - " + dataList[i][j + 1])

    # return list of lists
    return formattedDataList


# initiate app
# secret key set up for WTForms
SECRET_KEY = os.urandom(32)
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = SECRET_KEY

# initiate database
conn = sqlite3.connect('campusFood.db', check_same_thread=False)
c = conn.cursor()

# default items query
defaultView = "select * from default_data"

# default restaurant query
defaultRestaurant = "select * from default_restaurant"

# default combinations query
defaultCombinations = "select * from default_combinations;"

# Query for combinations
queryCombinations = "select combinations.combinationID, restaurant.restaurantName, combinations.combinationName \
          from combinations \
          inner join restaurant_combinations on combinations.combinationID=restaurant_combinations.combinationID \
          inner join restaurant on restaurant_combinations.restaurantID=restaurant.restaurantID \
          inner join combination_items on combinations.combinationID = combination_items.combinationID \
          inner join items on combination_items.itemID = items.itemID \
          group by combinations.combinationID"

# execute items query
c.execute(defaultView)
defaultData = c.fetchall()
defaultData = convert(defaultData)

# execute restaurants query
c.execute(defaultRestaurant)
restaurantData = c.fetchall()
restaurantData = convert(restaurantData)
restaurantData = formatRestaurantData(restaurantData)

# execute combinations query
c.execute(defaultCombinations)
combinationsData = c.fetchall()
combinationsData = convert(combinationsData)


# items webpage
@app.route('/', methods=['GET', 'POST'])
def home():
    # when form is submitted
    if request.method == 'POST':
        # get checkbox data
        checkboxData = getCheckboxes()
        checkboxData = combine(checkboxData)
        # get query string
        itemsQueryString = createItemsQuery(checkboxData)
        # get query data
        itemsQueryData = runQuery(itemsQueryString)

        # return webpage with updated data
        return render_template('frontEnd.html', data=itemsQueryData)
    # return webpage with default data
    return render_template('frontEnd.html', data=defaultData)


@app.route('/comboItems', methods=['GET', 'POST'])
def comboItems():
    # get combination information
    c.execute(queryCombinations)
    combinations = c.fetchall()
    combinations = convert(combinations)
    comboID = c.execute('select combinationID from combinations').fetchall()
    combinationItems = []
    # get item names in each combination
    for i in range(len(comboID)):
        combinationID = combinations[i][0]
        currentCombo = list(combinations[i])
        items = c.execute(
            'select itemName from combination_items inner join items on combination_items.itemID = items.itemID where combination_items.combinationId = :combinationID',
            {'combinationID': combinationID}).fetchall()
        for j in range(len(items)):
            currentCombo.append(items[j][0])

        # Add empty items to keep table structure in html
        if (len(items) == 1):
            currentCombo.append(" ")
            currentCombo.append(" ")
        if (len(items) == 2):
            currentCombo.append(" ")
        combinationItems.append(currentCombo)

    for k in range(len(combinationItems)):
        combinationItems[k].pop(0)

    return (render_template('comboItems.html', data=combinationItems))


# combinations webpage
@app.route('/combinations', methods=['GET', 'POST'])
def combinations():
    if request.method == 'POST':
        # get checkbox data
        checkboxData = getCheckboxes()
        checkboxData = combine(checkboxData)
        # get query string
        combinationsQueryString = createCombinationsQuery(checkboxData)
        # get query data
        combinationsQueryData = runQuery(combinationsQueryString)

        # return webpage with updated data
        return render_template('combinations.html', data=combinationsQueryData)
    c.execute(defaultCombinations)
    combinationsData = c.fetchall()
    combinationsData = convert(combinationsData)
    return render_template('combinations.html', data=combinationsData)


# restaurants webpage
@app.route('/restaurants', methods=['GET', 'POST'])
def restaurants():
    return render_template('restaurants.html', data=restaurantData)


# edit webpage
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    # create new forms
    form = newItem()
    rollback = rollBack()
    commit = commitChange()
    formCombo = newCombination()

    # find unique item ID
    uniqueID = c.execute('select MAX(itemID) from items').fetchall()
    uniqueID = uniqueID[0][0] + 1

    # add all restaurantIDs to select forms
    restaurantID = c.execute('select restaurantID from restaurant').fetchall()
    for i in restaurantID:
        form.restaurantID.choices.append(i[0])
        formCombo.comborestaurantID.choices.append(i[0])

    # add all foodtypes to select form
    types = c.execute('select foodType from foodType').fetchall()
    for i in types:
        form.foodType.choices.append(i[0])

    # if new item submit is clicked
    if (form.validate_on_submit() and form.submit.data):
        # get form data
        name = form.name.data
        price = form.price.data
        calories = form.calories.data
        fat = form.fat.data
        carbs = form.carbs.data
        protein = form.protein.data
        restaurant = form.restaurantID.data
        foodType = form.foodType.data

        # prepared statements inserts
        itemsInsert = (uniqueID, name, price, calories, fat, carbs, protein,)
        restaurantItems = (uniqueID, restaurant,)
        itemFoodType = (uniqueID, foodType,)

        # prepared statements
        c.execute(
            "INSERT INTO items (itemID, itemName, itemPrice,itemCalories,itemFat,itemCarbs,itemProtein) VALUES (?,?,?,?,?,?,?)",
            itemsInsert)
        c.execute("INSERT INTO restaurant_items (itemID, restaurantID) VALUES (?,?)", restaurantItems)
        c.execute("INSERT INTO item_foodtype (itemID, foodtype) VALUES (?,?)", itemFoodType)

        defaultView = "select * from default_data"
        c.execute(defaultView)
        newData = c.fetchall()
        newData = convert(newData)

        return (render_template('frontEnd.html', data=newData))

    # if form insert was clicked
    if (formCombo.validate_on_submit() and formCombo.submitCombo.data):
        # get form data
        comboName = formCombo.comboName.data
        restaurantID = formCombo.comborestaurantID.data
        # redirect to combo url page with passed variables
        return redirect(url_for('combo', restaurantID=restaurantID, comboName=comboName))

    # if rollback was clicked
    elif rollback.validate_on_submit() and rollback.rollback.data:
        # rollback changes
        conn.rollback()
        return (render_template('frontEnd.html', data=defaultData))

    # if commit was clicked
    elif commit.validate_on_submit() and commit.commit.data:
        # commit changes
        conn.commit()
        return (render_template('frontEnd.html', data=defaultData))

    return render_template('edit.html', data=defaultData, form=form, rollback=rollback, commit=commit,
                           formCombo=formCombo)


@app.route('/newCombo/<restaurantID>/<comboName>', methods=['GET', 'POST'])
def combo(restaurantID, comboName):
    # get restaurant name from ID
    restaurantName = c.execute('select restaurantName from restaurant where restaurantID = :restaurantID',
                               {'restaurantID': restaurantID}).fetchall()
    restaurantName = restaurantName[0][0]

    # create new form
    comboItems = comboItem()
    # get item choices for restaurantID
    itemChoices = c.execute(
        'select itemName from items inner join restaurant_items on items.itemID = restaurant_items.itemID where restaurantID = :restaurantID',
        {'restaurantID': restaurantID}).fetchall()

    # add item choices to select form
    for i in itemChoices:
        comboItems.itemOne.choices.append(i[0])
        comboItems.itemTwo.choices.append(i[0])
        comboItems.itemThree.choices.append(i[0])

    # create unique combinationID
    uniqueID = c.execute('select MAX(combinationID) from combinations').fetchall()
    uniqueID = uniqueID[0][0] + 1

    # if submitted
    if comboItems.is_submitted() and comboItems.submitComboItem.data:
        # get selected items
        itemIDOne = c.execute('select itemID from items where itemName = :itemName',
                              {'itemName': comboItems.itemOne.data}).fetchall()
        itemIDTwo = c.execute('select itemID from items where itemName = :itemName',
                              {'itemName': comboItems.itemTwo.data}).fetchall()
        itemIDThree = c.execute('select itemID from items where itemName = :itemName',
                                {'itemName': comboItems.itemThree.data}).fetchall()
        itemIDList = [itemIDOne[0][0], itemIDTwo[0][0], itemIDThree[0][0]]
        print(itemIDList);

        # prepared statements inserts
        combinationInsert = (uniqueID, comboName,)
        restaurantComboInsert = (restaurantID, uniqueID,)

        # prepared statements
        c.execute('INSERT INTO combinations (combinationID, combinationName) VALUES(?,?)', combinationInsert)
        c.execute('INSERT INTO restaurant_combinations(restaurantID, combinationID) VALUES (?,?)',
                  restaurantComboInsert)

        # prepared statements for all items
        for item in itemIDList:
            itemComboInsert = (item, uniqueID,)
            c.execute('INSERT INTO combination_items(itemID, combinationID) VALUES (?,?)', itemComboInsert)
        print(c.execute('select itemID from combination_items where combinationID = :combinationID',
                        {'combinationID': uniqueID}).fetchall())
        return (render_template('frontEnd.html', data=defaultData))

    return render_template('newCombo.html', comboItem=comboItems, restaurantName=restaurantName, comboName=comboName)


# run app
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
