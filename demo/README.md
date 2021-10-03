# Check-off Demo

## About

-   This is a API service that allows you to track personal spending and incomes, it also can help you parse bank statement downloaded from DBS/POSB iBanking.
-   The API is built using FastAPI and MongoDB, packaged with Docker and Docker-compose.
-   **The API implemented JWT authentication. All user request requires a valid JWT token, which can be obtained by sign-up then sign-in. Please replace the JWT token in the header of all HTTP requests below with a valid token.**

## Run the application

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
HTTP/1.1 201 Created
date: Sat, 02 Oct 2021 08:06:56 GMT
server: uvicorn
content-length: 4
content-type: application/json

"OK"
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
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjY4NDcsImlhdCI6MTYzMzE2MjA0Nywic3ViIjoiZGVtb191c2VyIn0.qqfjCn5W2woCprgswG_ICqhVL8Y1ALGawnTE0YETzcQ"
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
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjY4NDcsImlhdCI6MTYzMzE2MjA0Nywic3ViIjoiZGVtb191c2VyIn0.qqfjCn5W2woCprgswG_ICqhVL8Y1ALGawnTE0YETzcQ'
```

Expected response:

```http
HTTP/1.1 200 OK
date: Sat, 02 Oct 2021 08:10:55 GMT
server: uvicorn
content-length: 168
content-type: application/json

{
  "query_time": "2021-10-02T16:12:41.199611",
  "count": 0,
  "username": "",
  "date_range_start": null,
  "date_range_end": null,
  "total_amount": 0.0,
  "sorted_by": "",
  "records":[]
}
```

## Demo 3.1 Authenticated User create a new record

-   POST (that creates a new resource successfully)

Request:

```bash
curl -i -X 'POST' \
  'http://0.0.0.0:8000/api/records/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjY4NDcsImlhdCI6MTYzMzE2MjA0Nywic3ViIjoiZGVtb191c2VyIn0.qqfjCn5W2woCprgswG_ICqhVL8Y1ALGawnTE0YETzcQ' \
  -H 'Content-Type: application/json' \
  -d '{
  "uid": "id_for_demo",
  "account_id": "DBS1234",
  "amount": -1299,
  "merchant": "Apple",
  "label": "iPhone 13",
  "category": "Electronics",
  "subcategory": "Phone",
  "location": "SG",
  "link": "https://www.apple.com/sg/shop/buy-iphone/iphone-13",
  "starred": true,
  "confirmed": true
}'
```

Expected response:

```http
HTTP/1.1 201 Created
date: Sat, 02 Oct 2021 08:20:55 GMT
server: uvicorn
content-length: 4
content-type: application/json

"OK"
```

## Demo 3.2 Authenticated User tries to create a new record with missing/invalid input data

-   POST (that creates a new resource failed)

Request:

```bash
curl -i -X 'POST' \
  'http://0.0.0.0:8000/api/records/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjY4NDcsImlhdCI6MTYzMzE2MjA0Nywic3ViIjoiZGVtb191c2VyIn0.qqfjCn5W2woCprgswG_ICqhVL8Y1ALGawnTE0YETzcQ' \
  -H 'Content-Type: application/json' \
  -d '{
  "label": "iPad mini",
  "amount": "Not a number"
}'
```

Expected response:

```http
HTTP/1.1 422 Unprocessable Entity
date: Sat, 02 Oct 2021 08:26:18 GMT
server: uvicorn
content-length: 99
content-type: application/json

{
  "detail":[
    {
      "loc": ["body", "amount"],
      "msg": "value is not a valid float",
      "type": "type_error.float"
    }
  ]
}
```

## Demo 3.3 Authenticated User GET records

-   GET (with no query parameters)

Request:

```bash
curl -i -X 'GET' \
  'http://0.0.0.0:8000/api/records/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjY4NDcsImlhdCI6MTYzMzE2MjA0Nywic3ViIjoiZGVtb191c2VyIn0.qqfjCn5W2woCprgswG_ICqhVL8Y1ALGawnTE0YETzcQ'
```

Expected response:

```http
HTTP/1.1 200 OK
date: Sat, 02 Oct 2021 08:37:48 GMT
server: uvicorn
content-length: 690
content-type: application/json

{
  "query_time": "2021-10-02T16:37:49.197719",
  "count": 1,
  "username": "demo_user",
  "date_range_start": "2021-10-02T16:37:18.782000",
  "date_range_end": "2021-10-02T16:37:18.782000",
  "total_amount": -1299.0,
  "sorted_by": "transaction time",
  "records":[
    {
      "uid": "id_for_demo",
      "username": "demo_user",
      "date_time": "2021-10-02T16:37:18.782000",
      "account_id": "DBS1234",
      "amount": -1299.0,
      "amount_abs": 1299.0,
      "merchant": "Apple",
      "label": "iPhone 13",
      "bank_ref_code": null,
      "category": "Electronics",
      "subcategory": "Phone",
      "location": "SG",
      "link": "https://www.apple.com/sg/shop/buy-iphone/iphone-13",
      "tags": [],
      "reference": null,
      "remarks": null,
      "imported": false,
      "starred": true,
      "confirmed": true,
      "excluded": false,
      "archived": false
    }
  ]
}
```

## Demo 3.4 Authenticated User batch import new records from a DBS bank statement

-   POST (File upload in a POST request, using multipart/form-data)

Request:

```bash
curl -i -X 'POST' \
  'http://0.0.0.0:8000/api/records/import' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjY4NDcsImlhdCI6MTYzMzE2MjA0Nywic3ViIjoiZGVtb191c2VyIn0.qqfjCn5W2woCprgswG_ICqhVL8Y1ALGawnTE0YETzcQ' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@dbs_statement.csv;type=text/csv'
```

Expected response:

```http
HTTP/1.1 201 Created
date: Sat,02 Oct 2021 08:40:53 GMT
server: uvicorn
content-length: 147028
content-type: application/json

{
    "accountID": "POSB eSavings Account 435-67581-2",
    "statementDate": " ",
    "availableBalance": 593.92,
    "ledgerBalance": 518.72,
    "records": [{...}, {...}, {...}, {...}, {...}, ...],
    "insertions_count": 307,
    "failed_insertions_count": 0
}
```

## Demo 3.5 Authenticated User GET records sorted by absolute transaction amount

-   GET (with a `sortBy` query parameter)

Request:

```bash
curl -i -X 'GET' \
  'http://0.0.0.0:8000/api/records/?sort_by=absolute%20amount&reverse=true' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjY4NDcsImlhdCI6MTYzMzE2MjA0Nywic3ViIjoiZGVtb191c2VyIn0.qqfjCn5W2woCprgswG_ICqhVL8Y1ALGawnTE0YETzcQ'
```

Expected response:

```http
HTTP/1.1 200 OK
date: Sat,02 Oct 2021 08:51:35 GMT
server: uvicorn
content-length: 147543
content-type: application/json

{
  "query_time": "2021-10-02T16:51:35.989976",
  "count": 308,
  "username": "demo_user",
  "date_range_start": "2021-06-29T00:00:00",
  "date_range_end": "2021-10-02T16:37:18.782000",
  "total_amount": -3938.44,
  "sorted_by": "absolute amount",
  "records":
  [
    {"amount_abs": 1299, ...},
    {"amount_abs": 500, ...},
    {"amount_abs": 388.92, ...},
    {"amount_abs": 132.63, ...},
    {"amount_abs": 118.75, ...},
    {...},
    {...},
    ...
  ]
}
```

## Demo 3.6 Authenticated User GET records with multiple query parameters

-   GET (with combined query parameters `sortBy`, `offset`, and `count` )

Request:

-   We are going to query `top-5` transaction records dated between `2021-08-01` and `2021-08-05` with an offset of `2`, sorted by `amount` in `ascending` order.
-   We should expected a total of 5 records in the response payload, starting with the record with the largest spending amount (it is the smallest number because spending amount is negative).

```bash
curl -i -X 'GET' \
  'http://0.0.0.0:8000/api/records/?start_time=2021-08-01T00%3A00%3A00.000&end_time=2021-08-05T23%3A59%3A59.999&offset=2&count=5&sort_by=amount&reverse=false' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjY4NDcsImlhdCI6MTYzMzE2MjA0Nywic3ViIjoiZGVtb191c2VyIn0.qqfjCn5W2woCprgswG_ICqhVL8Y1ALGawnTE0YETzcQ'
```

Expected response:

```http
content-length: 2594
content-type: application/json
date: Sat,02 Oct 2021 09:04:09 GMT
server: uvicorn

{
  "query_time": "2021-10-02T17:04:10.597189",
  "count": 5,
  "username": "demo_user",
  "date_range_start": "2021-08-01T00:00:00",
  "date_range_end": "2021-08-04T00:00:00",
  "total_amount": -79.4,
  "sorted_by": "amount",
  "records": [
    {
      "uid": "R_20211002-164054-135495",
      "username": "demo_user",
      "date_time": "2021-08-04T00:00:00",
      "account_id": "POSB eSavings Account 435-67581-2",
      "amount": -30,
      ...
    },
    {...},
    {...},
    ...
  ]
}
```

## Demo 4.1 Update a existing record

-   PUT (update a single resource)

Request:

-   Let's modify the first record that we created in this demo, which has the `uid="id_for_demo"` because we explicitly allocated this uid during the record creation.
-   Let's overwrite the `amount` to `-2500.88` and change the `label` to `MacBook Pro`

```bash
curl -i -X 'PUT' \
  'http://0.0.0.0:8000/api/records/id_for_demo/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjY4NDcsImlhdCI6MTYzMzE2MjA0Nywic3ViIjoiZGVtb191c2VyIn0.qqfjCn5W2woCprgswG_ICqhVL8Y1ALGawnTE0YETzcQ' \
  -H 'Content-Type: application/json' \
  -d '{
  "amount": -2500.88,
  "label": "MacBook Pro"
}'
```

Expected response:

-   We can observe that the changes were applied, and the field `amount_abs` is also updated because it is a derived value of the `amount` field.

```http
HTTP/1.1 200 OK
date: Sat, 02 Oct 2021 09:23:16 GMT
server: uvicorn
content-length: 679
content-type: application/json

{
  "query_time": "2021-10-02T17:21:59.465297",
  "count": 1,
  "username": "demo_user",
  "date_range_start": "2021-10-02T16:37:18.782000",
  "date_range_end": "2021-10-02T16:37:18.782000",
  "total_amount": -2500.88,
  "sorted_by": "",
  "records": [
    {
      "uid": "id_for_demo",
      "username": "demo_user",
      "date_time": "2021-10-02T16:37:18.782000",
      "account_id": "DBS1234",
      "amount": -2500.88,
      "amount_abs": 2500.88,
      "merchant": "Apple",
      "label": "MacBook Pro",
      "bank_ref_code": null,
      "category": "Electronics",
      "subcategory": "Phone",
      "location": "SG",
      "link": "https://www.apple.com/sg/shop/buy-iphone/iphone-13",
      "tags": [],
      "reference": null,
      "remarks": null,
      "imported": false,
      "starred": true,
      "confirmed": true,
      "excluded": false,
      "archived": false
    }
  ]
}
```

## Demo 4.2 Delete a existing record

-   DELETE (remove a single resource)

Request:

```bash
curl -i -X 'DELETE' \
  'http://0.0.0.0:8000/api/records/id_for_demo/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjY4NDcsImlhdCI6MTYzMzE2MjA0Nywic3ViIjoiZGVtb191c2VyIn0.qqfjCn5W2woCprgswG_ICqhVL8Y1ALGawnTE0YETzcQ'
```

Expected response:

```http
HTTP/1.1 200 OK
date: Sat,02 Oct 2021 09:25:57 GMT
server: uvicorn
content-length: 4
content-type: application/json

"OK"
```

## Demo 4.3 Trying to Delete a record that does not exist

-   DELETE (remove a single resource)

Request:

-   We just repeat the request above, trying to delete a record that has already been deleted.

```bash
curl -i -X 'DELETE' \
  'http://0.0.0.0:8000/api/records/id_for_demo/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjY4NDcsImlhdCI6MTYzMzE2MjA0Nywic3ViIjoiZGVtb191c2VyIn0.qqfjCn5W2woCprgswG_ICqhVL8Y1ALGawnTE0YETzcQ'
```

Expected response:

```http
HTTP/1.1 404 Not Found
date: Sat, 02 Oct 2021 09:26:50 GMT
server: uvicorn
content-length: 38
content-type: application/json

{"detail": "Requested item not found."}
```

## Demo 5.1 Export selected records and download as a file

-   GET (returns a file)

Request:

```bash
curl --output 'exported.json.gz' -X 'GET' \
  'http://0.0.0.0:8000/api/records/export?offset=0&count=100&sort_by=transaction%20time&reverse=false' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjY4NDcsImlhdCI6MTYzMzE2MjA0Nywic3ViIjoiZGVtb191c2VyIn0.qqfjCn5W2woCprgswG_ICqhVL8Y1ALGawnTE0YETzcQ'
```

Expected response:

-   200 OK
-   A binary file received as `exported.json.gz`

## Demo 5.2 Batch delete archived records

-   DELETE (batch delete resources matching a certain condition)

Request:

```bash
curl -i -X 'DELETE' \
  'http://0.0.0.0:8000/api/records/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzM3NjY4NDcsImlhdCI6MTYzMzE2MjA0Nywic3ViIjoiZGVtb191c2VyIn0.qqfjCn5W2woCprgswG_ICqhVL8Y1ALGawnTE0YETzcQ' \
  -H 'Content-Type: application/json' \
  -d '{"imported": true}'
```

Expected response:

```http
HTTP/1.1 200 OK
date: Sun, 03 Oct 2021 10:19:31 GMT
server: uvicorn
content-length: 33
content-type: application/json

{"Number of records deleted": 307}
```
