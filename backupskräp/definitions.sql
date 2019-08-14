/* Schema for lab2. By Hariz Hasecic, KTH 2014*/

CREATE TABLE Items(
  name VARCHAR(100) CONSTRAINT itemkey PRIMARY KEY,
  unit VARCHAR(10));

CREATE TABLE Containers(
  name VARCHAR(10) CONSTRAINT containerkey PRIMARY KEY);

CREATE TABLE Recipes(
  name VARCHAR(100) CONSTRAINT recipkey PRIMARY KEY,
  type VARCHAR(50),
  description VARCHAR(500));

CREATE TABLE RecipeItems(
  name VARCHAR(100) REFERENCES Recipes(name),
  item VARCHAR(100) REFERENCES Items(name),
  Qty NUMERIC CONSTRAINT RcontainQty 
    CHECK (Qty > 0),
  CONSTRAINT Rcontainkey PRIMARY KEY(name, item));

CREATE TABLE ContainerItems(
  name VARCHAR(10) REFERENCES Containers(name),
  item VARCHAR(100) REFERENCES Items(name),
  Qty NUMERIC ,
  CONSTRAINT ccontainkey PRIMARY KEY(name, item));
  
CREATE VIEW kitchensum(item, qty, unit) AS
 (SELECT kitchenitems.item, kitchenitems.sum, items.unit
  FROM 	(SELECT item, sum(qty)
		FROM containeritems
		GROUP BY containeritems.item
		ORDER BY item) as kitchenitems, items
  WHERE kitchenitems.item = items.name);

/* sample data, remember to add the recipie in the FOLLOWING ORDER AS SHOWN BELOW !!!. Add all items first, then connect up RecipieItems*/  

BEGIN;  /* Komiåg att alltid DEFINIERA ITEMS FÖRST!! INNAN du lägger in dom i recipies eller containers  */
  INSERT INTO items VALUES('long grain rice','g');
  INSERT INTO items VALUES('olive oil','ml');
  INSERT INTO items VALUES('red chili pepper','x');
  INSERT INTO items VALUES('tomato','x');
  INSERT INTO items VALUES('onion','x');
  INSERT INTO items VALUES('cloves garlic','x');
  INSERT INTO items VALUES('champion mushrooms','g');
  INSERT INTO items VALUES('tortillas','x');
  INSERT INTO items VALUES('basil','g');
  INSERT INTO items VALUES('green bell pepper','x');
  INSERT INTO items VALUES('taco cheese','g');
  INSERT INTO items VALUES('broccoli','g');
  INSERT INTO items VALUES('sesame oil','ml');
  INSERT INTO items VALUES('soy sauce','ml');
  INSERT INTO items VALUES('brown sugar','g');
COMMIT;

BEGIN;
  INSERT INTO Recipes VALUES ('Mexican Fried Rice','sloppy', 'Delicious garbage from the land of the scum');
  INSERT INTO Recipes VALUES ('Mushroom Quesadillas','dusty', 'When you eat this you will wish you werent born');
  INSERT INTO Recipes VALUES ('Broccoli Stir Fry','frozen', 'For those with teeth made of steel');
COMMIT;

BEGIN;
  INSERT INTO RecipeItems VALUES('Mexican Fried Rice','long grain rice',300);
  INSERT INTO RecipeItems VALUES('Mexican Fried Rice','olive oil',30);
  INSERT INTO RecipeItems VALUES('Mexican Fried Rice','red chili pepper',1);
  INSERT INTO RecipeItems VALUES('Mexican Fried Rice','tomato',2);
  INSERT INTO RecipeItems VALUES('Mexican Fried Rice','onion',1);
  INSERT INTO RecipeItems VALUES('Mexican Fried Rice','cloves garlic',2);
  
  INSERT INTO RecipeItems VALUES('Mushroom Quesadillas','champion mushrooms',200);
  INSERT INTO RecipeItems VALUES('Mushroom Quesadillas','tomato',1);
  INSERT INTO RecipeItems VALUES('Mushroom Quesadillas','tortillas',2);
  INSERT INTO RecipeItems VALUES('Mushroom Quesadillas','basil',20);
  INSERT INTO RecipeItems VALUES('Mushroom Quesadillas','green bell pepper',1);
  INSERT INTO RecipeItems VALUES('Mushroom Quesadillas','taco cheese',100);
  
  INSERT INTO RecipeItems VALUES('Broccoli Stir Fry','onion',1);
  INSERT INTO RecipeItems VALUES('Broccoli Stir Fry','broccoli',300);
  INSERT INTO RecipeItems VALUES('Broccoli Stir Fry','olive oil',40);
  INSERT INTO RecipeItems VALUES('Broccoli Stir Fry','sesame oil',30);
  INSERT INTO RecipeItems VALUES('Broccoli Stir Fry','soy sauce',20);
  INSERT INTO RecipeItems VALUES('Broccoli Stir Fry','brown sugar',50);
  INSERT INTO RecipeItems VALUES('Broccoli Stir Fry','long grain rice',200);
COMMIT;

BEGIN;			/* Komihåg att alltid skapa containern först, innan du lägger något i den.*/
  INSERT INTO containers VALUES('Kitchen');
COMMIT;
BEGIN;
  INSERT INTO containeritems VALUES('Kitchen','long grain rice','400');
  INSERT INTO containeritems VALUES('Kitchen','tomato','4');
  INSERT INTO containeritems VALUES('Kitchen','onion','3');
  INSERT INTO containeritems VALUES('Kitchen','cloves garlic','7');
  INSERT INTO containeritems VALUES('Kitchen','red chili pepper','3');
  INSERT INTO containeritems VALUES('Kitchen','broccoli','700');
  INSERT INTO containeritems VALUES('Kitchen','olive oil','400');
  INSERT INTO containeritems VALUES('Kitchen','basil','50');
  INSERT INTO containeritems VALUES('Kitchen','sesame oil');
  INSERT INTO containeritems VALUES('Kitchen','brown sugar');
  INSERT INTO containeritems VALUES('Kitchen','soy sauce');
COMMIT;