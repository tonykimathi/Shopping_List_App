[![Build Status](https://travis-ci.org/tonykimathi/Shopping_List_App.svg?branch=Developer)](https://travis-ci.org/tonykimathi/Shopping_List_App)
[![GitHub issues](https://img.shields.io/github/issues/tonykimathi/Shopping_List_App.svg)](https://github.com/tonykimathi/Shopping_List_App/issues)

# Shopping_List_App
This is an application that allows users  to record and share things they want to spend money on meeting the needs of keeping track of their shopping lists.

# Features
1. Users can sign up for new accounts.
2. Users can log in.
3. Users can create, view, update and delete shopping lists.
4. Users can add, update, view and delete items in a shopping list.

# Installation procedure
 Clone this repository:
   * https://github.com/tonykimathi/Shopping_List_App.git

 Install a virtual environment: 
   * $ pip install virtualenv
   
 Activate your virtual environment:
   * $ source yourenvname/bin/activate
   
 Install requirements:
   * $ (yourenvname) pip install -r requirements.txt
   
## Running the tests

This code has been tested using`unittest` and `nosetest`.   

$ nosetests --with-coverage --cover-package=Tests && coverage report

# Samle output
```
...........................
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
Tests\__init__.py              0      0   100%
Tests\test_bucketlist.py      81      0   100%
app\__init__.py                6      3    50%   7-10
app\models.py                 73     56    23%   6-9, 11-24, 27, 31, 34, 37, 42-45, 53-54, 57-59, 61, 66-108
config.py                      6      0   100%
--------------------------------------------------------
TOTAL                        166     59    64%
----------------------------------------------------------------------
Ran 27 tests in 2.885s

OK
Name                       Stmts   Miss  Cover
----------------------------------------------
Tests\__init__.py              0      0   100%
Tests\test_bucketlist.py      81      0   100%
app\__init__.py                6      3    50%
app\models.py                 73     56    23%
config.py                      6      0   100%
----------------------------------------------
TOTAL                        166     59    64%
```

    
## Running the application
   * $ export FLASK_CONFIG=development
   * $ export FLASK_APP=run.py
   * $ flask run
   
## Deployment

This product is still at the development stage

## Author

* [TonyKimathi](https://github.com/tonykimathi)
