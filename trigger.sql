DELIMITER //

create procedure notify(in author integer, in book integer)
BEGIN
  DECLARE done BOOLEAN default false;
  DECLARE uid integer;
  DECLARE follower CURSOR FOR SELECT user_id FROM follows WHERE author_id=author; 
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done := TRUE;

  OPEN follower;

  followerLoop: LOOP
    FETCH follower INTO uid;
    IF done THEN
      LEAVE followerLoop;
    END IF;
    insert into notifications (user, body, date)
      VALUES(uid, concat('Author ', (select name from authors where id=author) , ' added a new book: ' , (select title from books where book_id= book)) ,now());
  END LOOP followerLoop;

  CLOSE follower;
END

//


Create trigger create_notifications
Before insert on wrote
for each row
Call Notify (NEW.author_id, NEW.book_id);
