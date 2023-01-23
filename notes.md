Auth Routes

-get users/id
-put users/id

Admin Routes
-utilitiy functions (seed-all, seed-x, delete-all)
-delete /users/id
-get /users


https://www.youtube.com/watch?v=PEfH_nIGLJk

- Next:
POST requests requring auth are failing due to missing CSRF token error
figure out how to send this token/send as the header?
- Potentially just try/except ignore the exception
Other wise the posting logic on the front end seems fine
- if we find a solution may look into refactoring the "GET" routes that really should be "POSTS"
- otherwise turn off CSRF feature per FastAPI JWT docs

- git commit when done with this

Auth Walk through
1 - Configure API
2 - Lockdown auth routes in API (and Admin Routes)
3 - Auth solution generates a JWT HTTPOnly cookie and CSRF token that is accessible
4 - On Login get the JWT cookie (and generate CSRF token)
5 - In the /me useEffect hook update currentUser using the response from /me to include the CSRF token as an attribute
6 - Note: The top of the app the and the PrivateRoute hook make use of the /me useEffect so everytme we hit a protected route or manually refresh 
7 - So now, currentUser has a "csrf" attribute & JWT is still stored in HTTPOnly cookie is
8 - Using axios/fetch include "X-CSRF-TOKEN" header when doing post methods