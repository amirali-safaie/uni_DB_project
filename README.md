we are trying to simulate something like Devar with my friends 
focus on establish database and its problems<br>

to use project create a virtual env.. <br>
you can do it in linux like this :<br>
`python3 -m venv env`<br>
then you should active env :<br>
`source env/bin/activate`<br>
if you use windows (dont use it) you can activate it by this cammand:<br>
`cd env`<br>
`cd scripts`<br>
`.\activate`<br>
then install requirements like this : <br>
`pip install -r requirements.text `<br>
but if you use windows first delete the uvloop package from requirements file and after the install the requirements do this: <br>
`pip install winloop`
to connect to your mysql create a file and name it .env 
inside it store your mysql password as this : <br>
`mysql_password="your_pass"`
and if you use windows set the password in envotiment variable in cmd frist:
1.open the cmd as adminastor
2.use tis command 
`setx MYSQL_PWD "your_mysql_password" `
then continue ..
