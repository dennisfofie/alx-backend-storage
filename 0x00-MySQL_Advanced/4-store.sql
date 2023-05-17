-- script that create a trigger

CREATE TRIGGER quantity_trigger AFTER INSERT ON orders FOR EACH ROW UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW>item_name;