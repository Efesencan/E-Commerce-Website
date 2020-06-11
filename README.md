# CS308 SOFTWARE ENGINEERING COURSE BACKEND REPOSITORY

## GÖKBERK YAR / EFE ŞENCAN / YİĞİT TEKİNALP

### Used Technologies:

    Python - Django

### Setting Virtual Environment for Windows:

py -m venv env
.\env\Scripts\activate
pip install -r Requirements.txt

### For Uploading Requirements.txt:

pip3 install pipenv<br/>
pipenv shell<br/>
pip3 install -r Requirements.txt<br/>



## Project Description:

1.5 Online Store Project
    This is a web site that presents a number of products in categories and let user to select and buy the desired product. Store has a limited stock, when user selects a product, number of items in the stock must be shown. When the shopping is done, that product should be decreased from the stock and forwarded to delivery department. Each user must be registered before shopping. Just after the payment is confirmed, it must show the invoice on the screen, send it as an email and let the user to download it as a pdf file. There are 4 types of users of this system detailed below. This web site should also as an attractive design so people should find it professional and trust to buy product. This is not just a web site but the shop window of your store. Site should be be good looking and consistent.
 <br/>   Sales Managers are responsible for setting the prices of the products. Sales manager can set a discount on the selected items. When the discount rate and the products are given, web site automatically set the new price and notify the registered
users about the discount. A product has the following properties: ID, name, model
number, description, quantity in stocks, and warranty status and distributor information. Furthermore, sales manager can view all the invoices in a given date range, can
print them or save as “pdf”. He should also calculate the revenue and loss/profit in
between given dates and makes a chart of it.
<br/>   Product managers are capable of adding, removing the products, setting the number of items in the stock, etc. Everything related to stock is done by the product
manager. ProductManager is also in the role of delivery department since it controls
the stock. This means, product manager can view the invoices, products to be send
and the corresponding address to deliver. A delivery list has the following properties:
delivery ID, customer ID, product UD, quantity, total price, delivery address, and is
delivered.
<br/>   Customers must register to the system. They can view the products, buy the
products and pay its price by the credit card. A customer has the following properties:
ID, name, tax ID, e-mail address, home address, and password. A customer should
enter his/her credit card information to buy a product. Credit card verification and
limit issues are out of scope of the project.
<br/>   Since every user (including administrators but excluding root) will remotely access your service, your software shall provide a means of remote accessibility. Furthermore, the users (except for the root user) shall be able to use their internet
browsers for any function they want to use, without installing any additional software
(aside from system libraries like Java or .NET framework), therefore a client-server
type of software package will not be accepted.

<br/>   Since the registration and payment process is a sensitive system, your project development and programming should reflect the necessary amount of security aware-
ONLINE STORE PROJECT 9
ness. The various user roles have their own security privileges and they should not
be mixed. Whatever your method of information storage (databases, XML files etc.)
sensitive information should be kept encrypted so that its not easily compromised.
Note that sensitive information includes at least the following: invoices and user accounts. Needless to say, your software is expected to run smoothly and not to display
any unexpected behavior while functioning within its normal parameters. Additionally, since this system will serve a potentially large number of users, you should keep
concurrency in mind: Your system should be able to handle multiple users of various
roles working on it at the same time and retain its normal functionality under such
circumstances
