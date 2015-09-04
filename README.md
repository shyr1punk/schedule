schedule
========

MSTUCA schedule


Install python package manager `pip` and MySQL lib for Python
```sudo apt-get install python-pip python-mysqldb```

Install Django
    ```pip install django```
    
Django modules:

xlrd
BeautifulSoup

MySQL: Create user, add database:

    ```CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';
    FLUSH PRIVILEGES;
    CREATE DATABASE schedule CHARACTER SET utf8 COLLATE utf8_general_ci;```

Write models to database:
`python manage.py syncdb`

Load data from `schedule/DB/dump/schedule_init.sql`


