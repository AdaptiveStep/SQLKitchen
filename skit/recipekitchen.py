import postgresql
db = postgresql.open('pq://postgres:admin@localhost:5432/Lab2')
get_table = db.prepare("""
                       SELECT *
                       FROM Recipeitems
                       """)

ps = db.prepare("SELECT $1::integer, $2::varchar ")
##
gs = db.prepare("SELECt * FROM recipeitems")

#ks = db.prepare("SELECT name FROM recipeitems WHERE name = $1::text[]")

##for x in get_table("name"): ##slänger ut en massa tupler som representerar raderna som fås genom SQL queryn
##    print(x)
##
#
#
# kan användas kanske...
#
# str(ks.first((23,432,324,432532))).split(sep="[")[1].split(sep="]")[0]
#


#tips:
# FROM (VALUES ('hej'), ('då')) AS names(first) 




c2string = ""
lista = ["hej"]

for i in lista:
    if c2string > "":
        c2string = c2string +","+ i
    else: c2string = c2string + i


from decimal import *
hej = Decimal(2000)
da = Decimal(-1000)



lista = ["a","b","c","d"]

lista2 = [("tomat",30),("cheese",10)]

dica = {}
dica["tomato"] = "x"
dica[("cheese","nice")] = "g"



js = db.prepare("SELECT * FROM recipeitems WHERE name ='Mexican Fried Rice'")
