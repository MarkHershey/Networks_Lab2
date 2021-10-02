# Check-off Demo

## Spin up services

At project root directory, execute:

```bash
docker-compose up --build
```

Check Documentation at: [http://0.0.0.0:8000/api/docs](http://0.0.0.0:8000/api/docs)

## Demo 1.1: User Sign Up

Request:

```bash
curl -i -X 'POST' \
  'http://0.0.0.0:8000/api/auth/signup' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "demo_user",
  "password": "demo_password",
  "name": "Demo Name",
  "email": "demo_name@email.com"
}'
```

Expected response:

```http

```

## Demo 1.2: User Log in

Request:

```bash
curl -i -X 'POST' \
  'http://0.0.0.0:8000/api/auth/signin' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "demo_user",
  "password": "demo_password"
}'
```

Expected response:

```http
HTTP/1.1 200 OK
date: Sat, 02 Oct 2021 07:21:19 GMT
server: uvicorn
content-length: 250
content-type: application/json

{
  "username": "demo_user",
  "name": "Demo Name",
  "email": "demo_name@email.com",
  "admin": false,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjM3MzksImlhdCI6MTYzMzE1ODkzOSwic3ViIjoiZGVtb191c2VyIn0.GqJ1FH7lHv-OJQuqaCnRc4gz3eZILh3reayn9ijdEhE"
}
```

## Demo 2.1: User request rejection due to no authentication header

Request:

```bash
curl -i -X 'GET' \
  'http://0.0.0.0:8000/api/records/' \
  -H 'accept: application/json'
```

Expected response:

```http
HTTP/1.1 403 Forbidden
date: Sat, 02 Oct 2021 07:24:13 GMT
server: uvicorn
content-length: 30
content-type: application/json

{"detail": "Not authenticated"}
```

## Demo 2.2: User request rejection due to an invalid JWT token

Request:

```bash
curl -i -X 'GET' \
  'http://0.0.0.0:8000/api/records/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer OBVIOUSLY_INVALID_JWT_TOKEN_FOR_DEMONSTRATION'
```

Expected response:

```http
HTTP/1.1 401 Unauthorized
date: Sat, 02 Oct 2021 07:26:22 GMT
server: uvicorn
content-length: 26
content-type: application/json

{"detail": "Invalid token"}
```

## Demo 2.3: User request succeeded with a valid JWT token authentication

Request:

```bash
curl -i -X 'GET' \
  'http://0.0.0.0:8000/api/records/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjM3MzksImlhdCI6MTYzMzE1ODkzOSwic3ViIjoiZGVtb191c2VyIn0.GqJ1FH7lHv-OJQuqaCnRc4gz3eZILh3reayn9ijdEhE'
```

Expected response:

```http
HTTP/1.1 200 OK
date: Sat, 02 Oct 2021 07:27:28 GMT
server: uvicorn
content-length: 2
content-type: application/json

[]
```

## Demo 3.1 Authenticated User create a new record

-   POST (that creates a new resource successfully)

Request:

```bash

```

Expected response:

```http

```

## Demo 3.2 Authenticated User tries to create a new record with missing/invalid input data

-   POST (that creates a new resource failed)

Request:

```bash

```

Expected response:

```http

```

## Demo 3.3 Authenticated User GET records

-   GET (with no query parameters)

Request:

```bash

```

Expected response:

```http

```

## Demo 3.4 Authenticated User batch import new records from a DBS bank statement

-   POST (File upload in a POST request, using multipart/form-data)

Request:

```bash

```

Expected response:

```http

```

## Demo 3.5 Authenticated User GET records sorted by absolute transaction amount

-   GET (with a `sortBy` query parameter)

Request:

```bash

```

Expected response:

```http

```

## Demo 3.6 Authenticated User GET records with multiple query parameters

-   GET (with combined query parameters `sortBy`, `offset`, and `count` )

Request:

```bash

```

Expected response:

```http

```

## Demo 4.1 Update a existing record

-   PUT (update a single resource)

Request:

```bash

```

Expected response:

```http

```

## Demo 4.2 Delete a existing record

-   DELETE (remove a single resource)

Request:

```bash

```

Expected response:

```http

```

## Demo 4.3 Trying to Delete a record that does not exist

-   DELETE (remove a single resource)

Request:

```bash

```

Expected response:

```http

```

## Demo 5.1 Archive a record

-   PUT (update a single resource)

Request:

```bash

```

Expected response:

```http

```

## Demo 5.2 Export selected records and download as a file

-   GET (returns a file)

Request:

```bash

```

Expected response:

```http

```

## Demo 5.3 Batch delete archived records

-   DELETE (batch delete resources matching a certain condition)

Request:

```bash

```

Expected response:

```http

```
