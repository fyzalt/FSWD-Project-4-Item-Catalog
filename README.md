## Item-Catalog
### About this Project

Project 4 for Udacity's Full Stack Web Developer Nanodegree. This is an application that provides a list of Clash of Clan buildings within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own base layout.

### Prerequisites

1.Python 2.x

2.SQL

3.Vagrant and Virtual Box

4.Oauth 2.0

5.Google Account



### Preparation and Setup

1.Install Virtual Box and Vagrant follow the instruction on this [link] (https://www.udacity.com/wiki/ud197/install-vagrant)

2.Clone this repository and put it under the directory called "vagrant"

3.Start the virtual machine.

4.This project comes with a prebuilt data base for testing purposes. To build your own data base, please follow the steps below:
  -Delete the prebuilt database called "cocbuildingwithuser.db"
  -Initial an empty databse using the following comment
  ```
  python database_setup.py
  ```
  -Populate the database
  ```
  python database_populate.py
  ```
  -You can modify the database_populate.py file to build your own database.
  
5.Run "catalog.py".

6.Access and test the application by visiting http://localhost:8000 locally

### Project Display Example
Home Page

![qq 20170609153315](https://user-images.githubusercontent.com/28365233/26991672-552b148e-4d29-11e7-9e1d-8cee5362d713.png)

Buildings for each base layout

![qq 20170609153342](https://user-images.githubusercontent.com/28365233/26991736-953fa148-4d29-11e7-8c2b-030e4a46b775.png)
