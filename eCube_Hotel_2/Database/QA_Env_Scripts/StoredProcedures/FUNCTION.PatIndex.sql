DELIMITER ;;

CREATE FUNCTION `PatIndex`(pattern VARCHAR(255), tblString VARCHAR(255)) RETURNS int(11)
    DETERMINISTIC
BEGIN

    DECLARE i INTEGER;
    SET i = 1;

    myloop: WHILE (i <= LENGTH(tblString)) DO

        IF SUBSTRING(tblString, i, 1) REGEXP pattern THEN
            RETURN(i);
            LEAVE myloop;        
        END IF;    

        SET i = i + 1;

    END WHILE; 

    RETURN(0);

END ;;
