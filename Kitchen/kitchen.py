__author__ = 'HARIZ'

import postgresql
db = postgresql.open('pq://postgres:admin@localhost:5432/Lab2')

class Container():
    def __init__(self):
        self.name = ""
        self.items = []     #Eftersom ett kök kommer ha få element, så används sekventiell lista.
    def updatekitchen(self):
        pass
    def insertitems(self):
        pass
    def deleteitems(self):
        pass

class Recipes():
    def __init__(self):
        self.name=""
        self.latestunits, self.recipeitems, self.latestofthenames = self.getstuff()        #just loads the stuff thats in the database, to be used in the instantiation here
        self.recipetype =""
        self.description = ""
        self.attributes = []        #every element will be a tuple like: (tomato, 3, x)
    def setname(self,name):
        self.name = name
        while 1:
            if self.name in self.latestofthenames:
                print("Name already exists. Try again.")
                self.name = mymenu.confirmnew("recipename")

                continue
            else:
                break
    def printRecipe(self):
        print("\t\tName: ", self.name)
        print("\t\tType: ", self.recipetype)
        print("\t\tDescription: ", self.description)

        if len(self.attributes) == 0:
            print("\t\t\tNo ingredients found, please type item to add new ones ")
            print("\t\tingredient: none  qty: none  unit: none")
        else:
            for i in self.attributes:
                print("\t\tingredient:", i[0], "qty: ", i[1], "unit:", i[2])
    def addItemDialog(self):
        additem = mymenu.confirmnew("ITEM")
        qty = mymenu.confirmnew("QUANTITY")
        if additem in self.latestunits:
            print("\tItem unit found in database.")
            itemunit = self.latestunits[additem]
        else:
            itemunit = mymenu.confirmnew("unit of the item (x for amount, g,kg,ml,m3 etc for volume)?")

        counter = 0

        #If the same ingredient has been added again, it will just replace the old one.
        # Obs, this should have been done with a dictionary. But since ingredients are only a handful of elements, it wont really matter.
        for a in self.attributes:
            if additem == a[0]:
                self.attributes[counter][1] = qty

                return
            counter += 1

        #If it hasen't returned yet, that means that the ingredient doesn't exist, and needs to be added.
        self.attributes.append([additem, qty, itemunit])
    def objectificator(self,name):          # Right now there are 2 modification "menu systems".
                                            # To unify this you need to make all tuples into objects. via this method
        prepare_recipe = db.prepare("SELECT * FROM recipes WHERE name =$1")
        prepare_recipeitems = db.prepare("""
                                SELECT recipeitems.name, recipeitems.item, recipeitems.qty, items.unit
                                FROM recipeitems, items
                                WHERE recipeitems.name = $1 and items.name = recipeitems.item
                                """)                    #tuples like (tomato, 3,x) are wanted.

        get_recipe = prepare_recipe(name)[0]
        get_recipeitems = prepare_recipeitems(name)

        #now the building starts
        self.name = name
        self.recipetype  = str(get_recipe[1])    #assigns is type
        self.description = str(get_recipe[2])    #assigns its description

        for i in get_recipeitems:           #constructs its items , (tomato,3,x)
            self.attributes.append((i[1],float(i[2]),i[3]))
    def getstuff(self):
        """
        Query used every time a hostlevel-rehash is called upon.

        Fetches all items        -> latestunits (dict)
        fetches all recipeitems  -> recipeitems (list)
        fetches all recipe names -> latestofthenames (list)
        """

        #This section reloads all the items and recipes, to help so that duplicates wont form up in database.
        get_units = db.prepare("""SELECT * FROM items""")           #Used to identify already existing units
        latestunits = {}
        get_recipeitems = db.prepare("SELECT * FROM recipeitems")
        recipeitems = {}
        get_recipes = db.prepare("""SELECT name FROM recipes""")    #to indentify already existing recipenames
        latestofthenames = []
        for i in get_units:                   #building all the lists below
            latestunits[i[0]] = i[1]          #building a dict of all registered items
        for k in get_recipeitems:
            recipeitems[(k[0], k[1])] = k[2]             #building a list of all registered recipeitems
        for n in get_recipes:
            latestofthenames.append(n[0])     #building a list of all recipenames

        return latestunits, recipeitems, latestofthenames
    def rehashobject(self):
        self.latestunits, self.recipeitems, self.latestofthenames = self.getstuff()     #updates the objects perception of whats in the database
    def changeingr(self):
        print("Choose one ingredient to remove (type anything else to go back): ")
        counter = 0
        choicelist = []
        for i in self.attributes:
            print("\t" ,counter ,"\tingredient:", i[0], "qty:", i[1], "unit:", i[2])
            choicelist.append(i)
            counter +=1

        val = int(input("Choice: "))
        try:
            self.attributes.remove(choicelist[val])
        except:
            print("Wrong choice, going back.")
    def performer(self):
        #Loading and preparing necessities
        kitchen = Container()
        kitchenload = db.prepare("SELECT item,qty FROM containeritems WHERE name = 'Kitchen' and qty >0")
        kitchenupdate = db.prepare("UPDATE containeritems SET qty = $2 WHERE name='Kitchen' and item =$1")
        kitchenclean = db.prepare("DELETE FROM containeritems WHERE qty = 0") #Make a clean before and after

        for i in kitchenload:                                                 #building up a kitchen object first
            kitchen.items.append([i[0],float(i[1])])                          #[ (tomato, 3), ... }
        doables, probables, nondoables = mymenu.doableRecipes()

        #Now performing substraction
        kitchencounter = 0
        kitchenregister = []
        substractlist = []
        rcounter = 0

        if self.name in doables:
            for recipeitem in self.attributes:      #self.attributes has [ (tomato,3) ]
                kitchencounter = 0
                for kitchenitem in kitchen.items:
                    if recipeitem[0] == kitchenitem[0]:
                        temp = kitchen.items[kitchencounter][1] - self.attributes[rcounter][1]

                        kitchen.items[kitchencounter][1] = temp
                        substractlist.append(temp)
                        kitchenregister.append(kitchencounter)
                        break
                    kitchencounter += 1
                rcounter +=1
            print("\t You performed",self.name, "and subtracted the following items from kitchen." )

            # Now saving latest kitchen state to to database
            counter2 = 0
            for i in kitchenregister:
                print("",kitchen.items[i][0],",",end=" ")
                if counter2 <2:
                    counter2 +=1
                else:
                    print("\n", end="")
                    counter2 %= 2
                t = kitchen.items[i]
                kitchenupdate(t[0],t[1])
            kitchenclean() #removes all items that have qty = 0 in kitchen.
        else:
            print("Not possible to perform the recipe! Returning to main menu.")
            return
    def recipe_selfdestruct(self):
        deletion = db.prepare("DELETE FROM recipes WHERE name =$1")
        print("\t\t -- OBS : THIS WILL REMOVE ALL INGREDIENTS TOO - -!")
        newconfirm = mymenu.confirmnew("DELETE (yes or no): ", "\t\tAre you sure you want to: ")

        if newconfirm == "yes":
            if self.name not in self.latestofthenames:  #Checks to see if it even exists in the database
                pass
            else:
                try:
                    deletion(self.name)      #(newdescr)
                except:
                    print("Didn't work. Try something else.")
        else:
            print("You didn't type yes or no. Going back.")
    def recipebuilder(self):
        """
        Shows menu to create or update a recipe object.

        """
        while 1:
            self.rehashobject()     #gets all the data from database thats relevant to prohibit duplicaton

            #Now the main code for the method
            print("\n\tRecipe built thus far:")
            self.printRecipe()

            print("\n\tChose action: "
                  "\n\t\t 0: add an ingredient item, "
                  "\n\t\t 1: change name, "
                  "\n\t\t 2: change 'type',"
                  "\n\t\t 3: change description."
                  "\n\t\t 4: change ingredients. "
                  "\n\t\t 5: DELETE the entire recipe. \n")
            affirmitive = input("Type anything else to return to menu. Choice: ")

            if affirmitive == str(0):       # item
                self.addItemDialog()
            elif affirmitive == str(1):     # name
                self.name = mymenu.confirmnew("name")
            elif affirmitive == str(2):     # type
                self.recipetype = input("Of what type is the recipe?: ")
            elif affirmitive == str(3):     # desc
                self.description = input("Describe the recipe. Press enter when you are done: ")
            elif affirmitive == str(4):     # ingr
                self.changeingr()
            elif affirmitive == str(5):   # delete
                tempname = self.name
                self.recipe_selfdestruct()
                print("You DELETED ", tempname, ". Returning to main menu.")
                break

                    #       This section will save things to database.
            else:
                newaffirmitive = input("Comfirm! Proceed and save?: Type yes to save and return to main menu: ")
                if newaffirmitive == "yes":
                    insertrecipe = db.prepare("INSERT INTO recipes VALUES($1,$2,$3)")           #1:recipename, 2: type, 3: descr
                    insertitems = db.prepare("INSERT INTO items VALUES($1,$2)")                 #1:item, 2: unit
                    insertrecipeitems = db.prepare("INSERT INTO recipeitems VALUES($1,$2,$3)")  #1:recipename, 2:item, 3:qty

                    updaterecipeitem = db.prepare("UPDATE recipeitems SET (qty) = ($3) WHERE name=$1 AND item=$2")
                    updaterecipe =  db.prepare("UPDATE recipes SET (type,description)= ($2,$3) WHERE name=$1")

                    if self.name in self.latestofthenames:
                        updaterecipe(self.name,self.recipetype,self.description)
                    else:
                        insertrecipe(self.name, self.recipetype, self.description)      #inserts recipe into database relation 'recipes'

                    if len(self.attributes) > 0:                                    #If there are ingredients in the recipe, then add them to the database
                        for attribute in self.attributes:                           #Add them all.
                            if attribute[0] not in self.latestunits:                 #if item doesn't exist in database relation 'items' (dict)
                                insertitems(attribute[0],attribute[2])
                            if (self.name,attribute[0]) not in self.recipeitems:
                                insertrecipeitems(self.name, attribute[0],attribute[1])    #and finally add the ingredient. tex. (tomato,3,x)
                            elif (self.name,attribute[0])  in self.recipeitems:
                                updaterecipeitem(self.name,attribute[0],attribute[1])      #If recipeitem already exists in the relation
                                                                                           # .."recipeitems, just update it.
                            self.rehashobject()
                    break
                else:
                    continue


class Menu():               #Behöver fortfarande objektorienteras bättre, vissa metoder är onödiga. Görs om.
    def __init__(self):
        pass
    def headline(self):
        print("""
            -------------------------------------------------------------------
                            === WELCOME TO KITCHEN-O-MAT ===
            -------------------------------------------------------------------
        """, end="")
    def viewMainMenu(self):
        print("""
    ############################# MAIN MENU #########################################
    |    1: Add recipe      4: See Items in Kitchen     7: See doable recipes       |
    |    2: See recipes     5: Add items to kitchen     8: See probable recipes     |
    |    3: Change Recipe   6: Generate shopping list   9: Perform recipe           |
    ################################################### 00: Quits program ###########
    ---------------------------------------------------------------------------------
                """)
    def printdoables(self):
        recipetuple = mymenu.doableRecipes()

        if len(recipetuple[0]) == 0:
            print("No recipes are definately doable.")
        else:
            print("\n\t\tThefollowing,", len(recipetuple[0]), "recipes are definately make-able : ")
            for name2 in recipetuple[0]:
                print("\t\t\t", name2)
    def makechoice(self):
        mymenu.viewMainMenu()

        val = input("Choose a number: ")
        try:
            val = int(val)
        except:
            print("Only natural numbers allowed. Try again. ", end = "")
            return

        if val == 1: self.addrecipe()
        elif val == 2: self.seerecipe()
        elif val == 3: self.changerecipe()
        elif val == 4: self.seeKitchenItems()
        elif val == 5: self.addKitchenItems()
        elif val == 6: self.generateShopList()
        elif val == 7: self.printdoables()
        elif val == 8: self.probableRecipes()
        elif val == 9: self.performRecipe()
        elif val == 00:
            print("\n\t\t\t  :::::: Thank you for using KITCHEN-O-MAT! :::::: \n\n")
            exit()
        else: print("Wrong choice, choose again")
    def differenceList(self,string):
        """

        :param string:
        :type string:
        :return: list
        :rtype: list of dim5 tuples
        """

        get_table = db.prepare("""
            
                (
                SELECT recipesum.item AS recipeitem, recipesum.sum AS neededqty, kitchensum.qty AS havingqty, (kitchensum.qty-recipesum.sum) AS difference, kitchensum.unit
                FROM    (    (SELECT item
                        FROM recipeitems, unnest(string_to_array($1, ',')) as selectedname
                        WHERE selectedname = recipeitems.name
                        GROUP BY recipeitems.item)

                        INTERSECT
                        (SELECT item FROM kitchensum)
                    ) AS itemdiffset,

                    (    SELECT item, sum(qty)
                        FROM recipeitems, unnest(string_to_array($1, ',')) as selectedname
                        WHERE selectedname = recipeitems.name
                        GROUP BY recipeitems.item
                    ) AS recipesum, kitchensum

                WHERE
                    kitchensum.item = itemdiffset.item
                    AND kitchensum.item = recipesum.item
                    AND (kitchensum.qty < recipesum.sum OR kitchensum.qty IS NULL)
                )
                    UNION
                (SELECT ungrouped.item AS recipeitem, ungrouped.sum AS needqty, 0 AS havingqty, (0 - ungrouped.sum) AS difference, items.unit
                FROM
                    (SELECT recipeitems.item, sum(qty)
                    FROM ((SELECT item
                        FROM recipeitems, unnest(string_to_array($1, ',')) as selectedname
                        WHERE selectedname = recipeitems.name
                        GROUP BY recipeitems.item)

                            EXCEPT
                        (SELECT item FROM kitchensum)) AS missingitems, recipeitems
                    WHERE recipeitems.item = missingitems.item
                    GROUP BY recipeitems.item) AS ungrouped, items
                WHERE ungrouped.item = items.name
                )


        """)
        return get_table(string)
    def addrecipe(self):
        recipename = input("Whats the name of this recipe?: ")
        if recipename in ("", " ", "   "):
            print("\t Wrong value, returning.")
            return
        newrecipe = Recipes()
        newrecipe.setname(recipename)

        newrecipe.recipetype = input("What type is the dish? eg, hot, cold, soup? etc: (optional) ")
        newrecipe.description = input("Describe the recipe. Press enter when you are done: (optional) ")
        newrecipe.recipebuilder()

        print(newrecipe.name,newrecipe.recipetype, newrecipe.description,newrecipe.attributes)
    def recipeList(self):
        "Fetches a list of all recipes"
        recipetable = db.prepare("""
                                SELECT DISTINCT
                                *
                                FROM recipes
                                """)
        recipelist = []
        for name in recipetable:
            recipelist.append(name)
        return recipelist
    def confirmnew(self,instring,strtype=""):
        while 1:
            if strtype != "":
                newstring=input(strtype + str(instring))
                if newstring =="" or " " or "  ":return ""
            else:
                newstring = input("What do you want the " + str(instring) + " to be?: ")
                if newstring == "" or " " or "  ": return ""
            confirm = input("Are you sure you want it to be: " + str(newstring) +"? Type yes, no: ")
            if confirm == "yes":
                return newstring
            elif confirm =="no":
                continue
    def printRecipeList(self):

        counter1 = -1
        recipelist = mymenu.recipeList() #fetches a list of all recipes.

        for name in recipelist:
            counter1 = counter1 + 1
            print("\t", counter1, "|", name[0], " | ", name[1])
    def seerecipe(self):
        self.printRecipeList()

        # print("\nYou can investigate the following recipes: \n")
        recipelist = mymenu.recipeList()

        try:
            val = int(input("\tWhich recipe do you want to see?: "))
            print("")

            name = recipelist[val][0]
        except:
            print("Wrong value, returning to main menu.")
            return
        ## Antar att väljaren väljer 2 , dvs "Mexican Fried Rice"
        #name = 2  #Ta bort denna rad , när du fixat hur man skickar saker genom SQL
        #
        get_table = db.prepare("""
            SELECT
              recipeitems.name,
              recipeitems.item,
              recipeitems.qty,
              items.unit
            FROM
              public.recipeitems,
              public.items
            WHERE
              recipeitems.item = items.name AND recipeitems.name = $1::varchar;
                               """)
        print("--------------------------------------------- \n \
name: ",recipelist[val][0],"\n type: ", recipelist[val][1], "\n \
Description: ", recipelist[val][2], "\n Ingredients:"  )
        for name in get_table(str(recipelist[val][0])):
            print("\t",name[1], str(name[2])+str(name[3]))
        print("---------------------------------------------")
    def changerecipe(self):
        #while 1:   #used with the bottom half (in case objectificator screws up)

        self.printRecipeList()          #Just prints a little pretty menu

        recipelist = mymenu.recipeList()
        choice1 = input("Which recipe do you want to change (type return to return): ")

        if choice1 == "return":
            return
        try:
            choice1 = int(choice1)
        except:
            print("Returning to menu.")
            return
        print("You chose: ", recipelist[choice1][0])
        selectedrecipe = Recipes()                  #constructs a temporary recipe object to work with,
                                                    #then update the database via the recipebuilder method

        selectedrecipe.objectificator(recipelist[choice1][0])
        selectedrecipe.recipebuilder()

            #
            ## Pretty printing menu
            #list2= ["Name", "Type", "Description", "Ingredients", "DELETE", "return"]
            #choice2 = input("\n What do you want to change (type 5 to return to mainmenu)?: \n \t "
            #                    "0: Name | 1: type | 2: Description | 3: Ingredients | 4: Delete it! ")
            #
            #choice2 = int(choice2)
            #print("You want to (change) ",list2[choice2])
            #
            #
            #    #WARNING REPEATING CODE MESS. FIX THIS
            #
            ##Menu logic
            #if choice2 == 0:                                        #this choice changes name
            #    changename = db.prepare("UPDATE recipes SET name = $1 WHERE name =$2")
            #    newname = mymenu.confirmnew("NAME")
            #    try:
            #        changename(newname,recipelist[choice1][0])      #(newname, oldname)
            #    except:
            #        print("Didn't work. Returning to menu.")
            #
            #elif choice2 == 1:                                      #changing type
            #    changetype = db.prepare("UPDATE recipes SET type = $1 WHERE name =$2")
            #    newtype = mymenu.confirmnew("TYPE")
            #    try:
            #        changetype(newtype,recipelist[choice1][0])      #(newtype, oldtype)
            #    except:
            #        print("Didn't work. Try something else.")
            #elif choice2 == 2:
            #    changedescription = db.prepare("UPDATE recipes SET description = $1 WHERE name =$2")
            #    newdesc = mymenu.confirmnew("DESCRIPTION")
            #    try:
            #        changedescription(newdesc,recipelist[choice1][0])      #(newdescr, olddescr)
            #    except:
            #        print("Didn't work. Try something else.")
            #
            #elif choice2 == 3:
            #    while 1:
            #        choice3 = input("Do you want to add or remove ingredients?. Type add or remove: ")
            #        if choice3 =="add":
            #            pass
            #        elif choice3 == "remove":
            #            pass
            #        else:
            #            pass
            #
            #elif choice2 == 4:
            #    deletion = db.prepare("DELETE FROM recipes WHERE name =$1")
            #    print("\t\t -- OBS : THIS WILL REMOVE ALL INGREDIENTS TOO - -!")
            #    newconfirm = mymenu.confirmnew("DELETE (yes or no): ", "\t\tAre you sure you want to: ")
            #    if newconfirm == "yes":
            #        try:
            #            deletion(recipelist[choice1][0])      #(newdescr)
            #        except:
            #            print("Didn't work. Try something else.")
            #    else: print("You didn't type yes or no. Going back.")
            #elif choice2 == 5:
            #    break
            #else:
            #    pass
    def seeKitchenItems(self):
        print("\tHere are all the items in your kitchen! \n")
        get_table = db.prepare("""SELECT * FROM kitchensum""")
        counter = 0
        for tuple in get_table:
            print(" ",counter,"  \t",tuple[0],":" ,tuple[1],tuple[2] )
            counter +=1
    def addKitchenItems(self):
        while 1:
            #loading hashtables of stuff.
            latestunits, recipeitems, latestofthenames = Recipes().getstuff()

            #creating hashtable of kitchen
            latestkitchenitems = db.prepare("SELECT item, qty FROM containeritems WHERE name = 'Kitchen'")
            kitchendict = {}
            for i in latestkitchenitems:
                kitchendict[i[0]] = i[1]

            #Preparing insertions
            inserttoitems = db.prepare ("INSERT INTO items VALUES ($1,$2)")
            inserttokitchen = db.prepare ("INSERT INTO containeritems  VALUES ('Kitchen',$1,$2)")
            updatekitchen = db.prepare("UPDATE containeritems SET qty = $2 WHERE name='Kitchen' and item=$1")

            #Menu logic
            itemexist = False       #used to tell if item exists in database
            newitem = self.confirmnew("ingredient")
            if newitem =="":
                print("Wrong value. Returning to main menu.")
                return
            elif newitem in latestunits:
                newunit = latestunits[newitem]
                itemexist = True
            else:
                newunit =self.confirmnew("UNIT")        #Or it asks for unit
            try:
                qty1 = self.confirmnew("QUANTITY")      #asking for quantity
                qty = int(qty1)
            except: qty = qty1       #in case non-numeral was entered.

            print("\tYou have chosen: \n"               #pretty printing current input
                  "\t\tName: ", newitem, "\n"
                  "\t\tqty: ",qty, "unit: ",newunit)
            confirm = input("Do you accept this new data?: Type yes or no: ")


            if confirm =="yes":
                #### check to see if the item is found in containeritems
                if newitem in kitchendict:
                    val = input("Item already found in kitchen. Do you want to update the QUANTITY?: ")
                    if val =="yes":
                        updatekitchen(newitem,qty)
                        print("Successful update! Returning to main menu.")
                        break
                    else: print("Returning to menu without changes made.")
                else:
                    if not itemexist:
                        inserttoitems(newitem,newunit)      #if the item cant be found in the 'items' relation, then add it.
                        inserttokitchen(newitem,qty)
                        print("Successfully inserted both item and recipe. Returning to main menu.")

                    else:
                        inserttokitchen(newitem,qty)
                        print("Successful insertion. Returning to main menu.")
                    break
            else:
                print("Returning to main menu.")
                break
    def generateShopList(self):

        kitchensum = db.prepare("SELECT * FROM kitchensum")
        print("These are the registered recipes. ")

        self.printRecipeList()
        recipelist = self.recipeList()
        choice = input("\n Chose one or several items, separate with comma. For instance: 1,5,6: ").split(sep=",")
        if choice in ([""],[" "], ["  "]):
            print("\t Returning.")
            return
        choiceNames = []
        for c in choice:
            choiceNames.append(recipelist[int(c)][0])
        print("\tYou chose: ", end="")

        c2string = ""
        for i in choiceNames:
            if c2string > "":
                c2string = c2string + "," + i
            else:
                c2string = c2string + i
        print(c2string, "\n")

        shoppinglist = self.differenceList(c2string)
        if len(shoppinglist) ==0:
            input("\t\tYou have everything you need to perform the recipes! \n\t\tPress enter to return to menu.")
        else:
            print("\tInvestigating items... ")

            for i in shoppinglist:
                if i[2] == None or i[3] ==None:
                    print("\t\tPlease check to see that you have:",i[1],i[4],"of",i[0])
                elif i[2] == 0 or i[2]>0 :
                    print("\t\tYou need:", abs(i[3]),i[4], i[0])
            input("\n\t\t\tInvestigation finished! Press enter to return to menu.")
    def doableRecipes(self):
        recipes = db.prepare("SELECT name FROM recipes")

            #Obs, the lists only have the recipe names as elements.
        doables = []

        probables = []
        checkables = []

        nondoables = []

        for name in recipes:
            shoplist = self.differenceList(name[0])
            if not len(shoplist) >0:
                doables.append(name[0])
            elif len(shoplist)>0:
                for item in shoplist:
                    if item[2] == 0:
                        if name[0] not in probables:
                            nondoables.append(name[0])
                            break
                        else:
                            probables.remove(name[0])
                            nondoables.append(name)
                    elif item[2] is None and item[3] is None:
                        if name[0] not in probables:
                            probables.append(name[0])
                            checkables.append(item)
                        else:
                            checkables.append(item)
        return doables, probables, nondoables
    def probableRecipes(self):
        recipetuple = mymenu.doableRecipes()

        if len(recipetuple[1]) == 0:
            print("\t\tNo recipes are 'probably possible' to do.")
        elif len(recipetuple[1]) > 0:
            print("\n\t\tThefollowing,", len(recipetuple[1]), "recipes are 'possible' : ")
            for name2 in recipetuple[1]:
                print("\t\t\t", name2)

        if len(recipetuple[2]) > 0:
            print("\n\t\tBut the following,", len(recipetuple[2]), "recipes are impossible to do (lacking stuff in kitchen) : ")
            for name2 in recipetuple[2]:
                print("\t\t\t", name2)
    def performRecipe(self):
        doables, probables, nondoables = self.doableRecipes()
        if len(doables)==0:
            print("\t No recipes can currently be performed")
            return
        print("\tYou can perform the following recipes: ")
        counter = 0
        for i in doables:
            print(" \t",counter, ":", i )
            counter +=1
        try:
            choice1 = doables[int(input("\n\t\t Which recipe do you want to perform?: "))]
            print("\t\t you chose:",choice1,"\n")
        except:
            print("\n\t\t Wrong choice, returning to main menu.")
            return

        selectedrecipe = Recipes()
        selectedrecipe.objectificator(choice1)
        selectedrecipe.performer()
        pass

def main():
    mymenu.headline()
    while 1:
        mymenu.makechoice()
mymenu = Menu()
main()