# ContextDB API Documentation

This document provides a detailed description of the ContextDB API.

## Base URL

All API requests are made to:

```
http://<db_host>:<db_port>/<db_name>
```

## Authentication

The API uses Basic Authentication. Include your username and password in the `auth` parameter of your requests.

## Headers

All requests must include the `Content-Type: application/json` header.

## Endpoints

### POST /ctxdb/contexts

Add a new context.

#### Request Body

```json
{
  "text": "string",
  "url": "string",
  "metadata": {
    "additionalProp1": "string",
    "additionalProp2": "string",
    "additionalProp3": "string"
  }
}
```

#### Response

```json
{
  "message": "Context added successfully"
}
```

### GET /ctxdb/contexts/{idx}

Get a context by its index.

#### Path Parameters

- `idx` (string): Index of the context to retrieve.

#### Response

```json
{
  "id": "string",
  "text": "string",
  "url": "string",
  "metadata": {
    "additionalProp1": "string",
    "additionalProp2": "string",
    "additionalProp3": "string"
  },
  "embedding": "string",
  "confidence": 0
}
```

### DELETE /ctxdb/contexts/{idx}

Delete a context by its index.

#### Path Parameters

- `idx` (string): Index of the context to delete.

#### Response

```json
{
  "message": "Context deleted successfully"
}
```

### PUT /ctxdb/contexts/{idx}

Update an existing context by its index.

#### Path Parameters

- `idx` (string): Index of the context to update.

#### Request Body

```json
{
  "text": "string",
  "url": "string",
  "metadata": {
    "additionalProp1": "string",
    "additionalProp2": "string",
    "additionalProp3": "string"
  }
}
```

#### Response

```json
{
  "message": "Context updated successfully"
}
```

### POST /ctxdb/contexts/query

Query for a context.

#### Request Body

```json
{
  "text": "string",
  "url": "string",
  "metadata": {
    "additionalProp1": "string",
    "additionalProp2": "string",
    "additionalProp3": "string"
  }
}
```

#### Response

```json
[
  {
    "id": "string",
    "text": "string",
    "url": "string",
    "metadata": {
      "additionalProp1": "string",
      "additionalProp2": "string",
      "additionalProp3": "string"
    },
    "embedding": "string",
    "confidence": 0
  }
]
```

## Error Handling

If an error occurs during a request, the API will return an HTTP status code and a JSON response with the following format:

```json
{
  "detail": "string"
}
```

The `detail` field will contain a message describing the error.