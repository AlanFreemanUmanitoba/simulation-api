## Re-install sqldb
### extend the userlist
endpoint to lock a user @router.get("lock/{user}")  
  1. If user is not locked, generate and send an apikey (status code 200)  [NB IS THIS NEEDED?]
  2. If user is locked, send a refusal (status code)  
  3. If there is no such user, send a failure (status code 400?)  
### Test the user list
Test lock with non-existent user  
Test lock with unlocked user  
Test lock with locked user  

## endpoint to unlock a user @router.get("unlock/user")  
  1. if user does not exist, send a failure (status code 400?)  
  2. if user does exist but is not locked, send an anodyne message (status code 200?)  
  3. if user does exist and is locked, unlock the user and send status code 200  

### Test  
    non-existent user  
    unlocked user  
    locked user  

## CLIENT  
## Status check (for all APIs)
get a cookie and find out who is the user; get the api from this
(get in as guest?)
(guest could look at other simulations but is barred from making one or undertaking any action)

### if status-check returns a failure  
revert to guest user.  
### Restrict guest.     
Inspect other people's simulations (problematic - would need a second cookie to say who I'm looking at - also could guest use the arrows?)  
Initially, until later in the development phase the ONLY page guest gets to see is the 'choose a user' page (and maybe the register page),

## Create 'choose user' menu item
   Send a 'lock user' request to the server
### Looks at the server response and:  
   1. If it says OK, set a new cookie.  
## Create 'unlock' option.
Send 'unlock' request to server. 
   In every case, just go back to logging in as guest.  
Options are:    
  1. status code 400  
  2. status code 200  
But does it even matter?
