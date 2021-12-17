# vehicle_register
Application share rides between users 

User will need to have PostgeSQL installed Prior for this application to work. 

Step 1. Clone git repo.

	1) Changed into the directory where you want the repo saved. 

	2) Clone git repo to the directory with the following command.
     git clone https://github.com/samuelparkin1/SamuelParkin_T3A3.git

Step 2. Change into cloned directory with the following command.
        cd SamuelParkin_T3A3/


Step 2. Setup virtual enviroment. 

	1) setup a virtual enviroment with the following command. 
        virtualenv venv

	2) Activate virtual enviroment with the following command. 
        source venv/bin/activate

Step 3. Run the follow command in terminal window pip installs needed:
		pip install -r requirements.txt

Step 4. Start PostgreSQL.

 macOS command:

    brew services start postgresql
Linux command:

    sudo service postgresql start

Step 5. Run PostgreSQL.

macOS command:

        brew services run postgresql

Linux command:

        sudo service postgresql run

Step 6. create a database for the app 

    CREATE DATABASE rideshareapp;

Step 7. Create a role within PostgreSQL.

        CREATE USER exampleuser WITH PASSWORD 'example1';
        *note: change "exampleuser" and 'example1' to desired.   


step 8. Grant the user account permission to act on the database:

    GRANT ALL PRIVILEGES ON DATABASE rideshareapp to 'exampleuser';
    *note: change "exampleuser" user just created. 

Step 9. Quit PostgreSQL

    \q

Step 10. Open directory in VS Code with this command. 
     
     code . 

step 11. create a new file called .env and save this information to it.

    DB_USER = "exampleuser"     * change this to newly created PostgreSQL user
    DB_PASS = 'example1"        * change this to newly created PostgreSQL password    
    DB_NAME = "rideshareapp"
    DB_DOMAIN = "localhost:5432"
    SECRET_KEY = "secretkey"   * change this to any desired key

 Step 12. In the terminal window change into the Ride_share_app directory.
    
    cd Ride_share_app/
 
 step 13. Create all database table.
    
    flask db-custom reset

step 14. Start flask within the terminal window.

    flask run

    * note that it should display Running on http://127.0.0.1:5000/

step 15 open app in browser window by going to:

    http://127.0.0.1:5000/

step 16. Once finished using the app close browser and terminate flack by running the follow command.

    ctrl c

## Saving the database. 

If you wish to made a copy of to database tables to there own txt files run the following command.

    flask db-custom export



    




