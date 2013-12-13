select first_name || ' ' || last_name || ' ' || email as document from users;
                   document                    
-----------------------------------------------
 Margaret Leibovic margaret.leibovic@gmail.com
 Laura Cutrona laura.musser@gmail.com
 Katie Thomas katiemthom@gmail.com
 Katie Thomas katiemthom@gmail.com
(4 rows)





select * from users where to_tsvector(first_name || ' ' || last_name || ' ' || email) @@ to_tsquery('katie');
user_id | first_name | last_name |        email         |                           password                           | period |             salt              | is_banned |          profile_picture          | school_id 
---------+------------+-----------+----------------------+--------------------------------------------------------------+--------+-------------------------------+-----------+-----------------------------------+-----------
       1 | Katie      | Thomas    | katiemthom@gmail.com | $2a$12$smQwB0g3TGnRertiLEVZquaAsY7vsbJU6QPmnYMzTBEyA9qXBAG4. |      2 | $2a$12$smQwB0g3TGnRertiLEVZqu | f         | http://katiemthom.com/cat_ph.jpeg |       111
       4 | Katie      | Thomas    | katiemthom@gmail.com | $2a$12$xam0t.9ukwnm8V8cr66ki.1.6ebg2W1vk9etOsbmnvavXEnhrcp0G |      2 | $2a$12$xam0t.9ukwnm8V8cr66ki. | f         | http://katiemthom.com/cat_ph.jpeg |       345




create index user_index on users using gin(to_tsvector('english', first_name || ' ' || last_name || ' ' || email));
CREATE INDEX



alter table users add column user_index_col tsvector;
ALTER TABLE



update users set user_index_col = to_tsvector('english', coalesce(first_name,'') || ' ' || coalesce(last_name,'') || ' ' || coalesce(email,''));
UPDATE 4




select * from users where user_index_col @@ to_tsquery('laura');


to_sequery input must be separated by & 




select * from users where user_index_col @@ to_tsquery('katiem:*');






create trigger tsvectorupdate before insert or update on users for each row execute procedure tsvector_update_trigger(user_index_col,'pg_catalog.english', first_name, last_name, email);
CREATE TRIGGER





users = engine.execute("select * from users where user_index_col @@ to_tsquery('laura');")


>>> u = search_user('katie')
>>> for user in u:
...     print user[0]
... 
1
4
>>>


  