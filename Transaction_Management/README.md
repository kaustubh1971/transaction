There are 4 APIs

1. Create Transaction('POST') - As the name says it is used to create transction along with multiple transaction lines

2. Add Inventory(POST) - Used to add mulitple inventories for a single Transaction Line

3. Delete Transaction('DELETE') - We can delete the Transaction objects only if the Inventory is not present for th given Transaction ID.

4. Get Tran Details('GET') -  We can get all the data linked to a single Transaction using this API

I have provided POSTMAN collection link:
https://www.getpostman.com/collections/e7dd44064439ed2428a7