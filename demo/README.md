# Check-off Demo

## Spin up services

At project root directory, execute:

```bash
docker-compose up --build
```

## Demo 1.1: User Sign Up

Request:

```bash

```

Expected response:

```http

```

## Demo 1.2: User Log in

Request:

```bash

```

Expected response:

```http

```

## Demo 2.1: User request rejection due to no authentication header

Request:

```bash

```

Expected response:

```http

```

## Demo 2.2: User request rejection due to an invalid JWT token

Request:

```bash

```

Expected response:

```http

```

## Demo 2.3: User request succeeded with a valid JWT token authentication

Request:

```bash

```

Expected response:

```http

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

## Demo 5.1 Export selected records and download as a file

-   GET (returns a file)

Request:

```bash

```

Expected response:

```http

```
