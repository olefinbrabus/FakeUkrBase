# FakeUkrBase

## General information

This console application is designed to generate random information that can be used for data analytics or for database load testing.

### install the application via GitHub
```bash 
git clone https://github.com/olefinbrabus/FakeUkrBase
cd FakeUkrBase
python -m venv venv
pip install requirements.txt
```

### example options in app
- in the "files" folder in the application directory
```bash
python main.py --generate 1 --save .csv  # automatically generates a name in the format "Year-Month-Day Hours:Minute:Second uuid4" 
python main.py --generate 4 --save test_file.xml --display
```
- in other folder(only absolute path)
```bash
python main.py --generate 1000 --seed 5 --save /Users/user/Download/my_employee.xlsx
```
## Features

### complete
- generate fictional person with ukrainian full name, birthdate, phone number, address, email
- save any person type in various folder ways and formats(json, xml, xlsx, csv)
- tabulation display persons
- seed
### in process
- read files
- documentation and --help options
- various diagram for analytics
- employee with more data
- fastAPI fork