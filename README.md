# OnlineLibraryManagement - Web college project (Django, Oracle database)
This repository contains the source code for the Library Management Application, a web-based project focused on addressing the challenges of library management. The project involves the design and implementation of a database system to model the flow of events within a library.

Library management activities include keeping track of customer records, their personal data, and the books supplied by collaborating publishers. Books can be rented out only if they are in stock.

In addition, the application enables rental transactions with the option for customers to physically take the desired book from the library premises. All rentals are subject to the availability of the respective book in stock. Books must be returned within 7 days, but customers have the option to extend the rental period as per their requirements. It is also allowed to terminate the rental before the 7-day period expires. When returning the book, the condition of the book will be recorded.

## Technologies 
- Python
- HTML
- CSS
- Django
- Data Modeler
- SQL Developer

## Features
- **Rental Operations Tracking**: The application maintains records of book rental operations, including rental start and end dates, customer information, and book details.
- **Customer Management**: The system tracks customer data, such as personal information, contact details, and rental history.
- **Book Management**: The application manages book records, including details like book title, author, publisher, availability status, and condition upon return.

## Scripts
- [The script for creating tables](https://github.com/Carla-Husman/OnlineLibraryManagement/blob/f9106707102476d3628fc5611eddfef6842bc3a5/Scripts%20and%20Documentation/script_creare_tabele.sql)
- [The script for inserting into tables (contains transactions)](https://github.com/Carla-Husman/OnlineLibraryManagement/blob/f9106707102476d3628fc5611eddfef6842bc3a5/Scripts%20and%20Documentation/script_inserare_date.sql)
- [The test script](https://github.com/Carla-Husman/OnlineLibraryManagement/blob/f9106707102476d3628fc5611eddfef6842bc3a5/Scripts%20and%20Documentation/script_testare.sql)

## Documentation
You will find the documentation [here](https://github.com/Carla-Husman/OnlineLibraryManagement/blob/f9106707102476d3628fc5611eddfef6842bc3a5/Scripts%20and%20Documentation/Documenta%C8%9Bie.pdf) and it provides information about:
- project description
- the technologies used for front-end and back-end
- the structure and inter-relationship of the tables (ER diagram, including aspects related to normalization, with explanations)
- the description of the constraints used and why they were necessary
- description of how to connect to the application database
- _screenshots containing the design of the application_
  
## Database
![image](https://github.com/Carla-Husman/OnlineLibraryManagement/assets/125916556/12682f53-2aac-4a61-acbd-79122b99d413)

![image](https://github.com/Carla-Husman/OnlineLibraryManagement/assets/125916556/60d9b90d-32d9-4163-bf1f-1078518b58d2)


