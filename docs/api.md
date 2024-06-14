
# API Documentation

This section provides detailed information about the gRPC services and messages used in the LoadTestCyrex project.

## Services

### AuthService

- **SignUpUser(SignUpUserInput) returns (SignUpUserResponse)**

```json
{
  "name": "Hello",
  "email": "Hello",
  "password": "Hello",
  "passwordConfirm": "Hello"
}
```

- **SignInUser(SignInUserInput) returns (SignInUserResponse)**

```json
{
  "email": "Hello",
  "password": "Hello"
}
```

- **VerifyEmail(VerifyEmailRequest) returns (VerifyEmailResponse)**

```json
{
  "verificationCode": "Hello"
}
```

### VacancyService

- **CreateVacancy(CreateVacancyRequest) returns (CreateVacancyResponse)**

```json
{
  "Title": "Hello",
  "Description": "Hello",
  "Division": 0,
  "Country": "Hello"
}
```

- **GetVacancy(VacancyRequest) returns (VacancyResponse)**

```json
{
  "Id": "26038359-a876-4f32-9b38-46c05398020a"
}
```

- **GetVacancies(GetVacanciesRequest) returns (stream VacancyResponse)**

```json
{
  "page": 20,
  "limit": 20
}
```

- **UpdateVacancy(UpdateVacancyRequest) returns (UpdateVacancyResponse)**

```json
{
  "Id": "415ffd76-9631-4c28-a942-2266650195a6",
  "Title": "Hello",
  "Description": "Hello",
  "Views": 10,
  "Division": 0,
  "Country": "Hello"
}
```

- **DeleteVacancy(VacancyRequest) returns (DeleteVacancyResponse)**

```json
{
  "Id": "cd723a39-9ad9-4ebc-ac30-e4e0724ba46b"
}
```

### UserService

- **GetMe(GetMeRequest) returns (GetMeResponse)**

```json
{
  "Id": "348b9e65-9836-4cc0-9d5a-242c56e05a70"
}
```

## Messages

### SignUpUserInput

```protobuf
message SignUpUserInput {
    string name = 1;
    string email = 2;
    string password = 3;
    string passwordConfirm = 4;
}
```

### SignUpUserResponse

```protobuf
message SignUpUserResponse {
    bool success = 1;
    string message = 2;
}
```

### SignInUserInput

```protobuf
message SignInUserInput {
    string email = 1;
    string password = 2;
}
```

### SignInUserResponse

```protobuf
message SignInUserResponse {
    string access_token = 1;
    string refresh_token = 2;
}
```

### VerifyEmailRequest

```protobuf
message VerifyEmailRequest {
    string verificationCode = 1;
}
```

### VerifyEmailResponse

```protobuf
message VerifyEmailResponse {
    bool success = 1;
    string message = 2;
}
```

### CreateVacancyRequest

```protobuf
message CreateVacancyRequest {
    string Title = 1;
    string Description = 2;
    int32 Division = 3;
    string Country = 4;
}
```

### CreateVacancyResponse

```protobuf
message CreateVacancyResponse {
    Vacancy vacancy = 1;
}
```

### VacancyRequest

```protobuf
message VacancyRequest {
    string Id = 1;
}
```

### VacancyResponse

```protobuf
message VacancyResponse {
    Vacancy vacancy = 1;
}
```

### GetVacanciesRequest

```protobuf
message GetVacanciesRequest {
    int32 page = 1;
    int32 limit = 2;
}
```

### UpdateVacancyRequest

```protobuf
message UpdateVacancyRequest {
    string Id = 1;
    string Title = 2;
    string Description = 3;
    int32 Division = 4;
    string Country = 5;
}
```

### UpdateVacancyResponse

```protobuf
message UpdateVacancyResponse {
    Vacancy vacancy = 1;
}
```

### DeleteVacancyResponse

```protobuf
message DeleteVacancyResponse {
    bool success = 1;
}
```

### GetMeRequest

```protobuf
message GetMeRequest {
    string Id = 1;
}
```

### GetMeResponse

```protobuf
message GetMeResponse {
    User user = 1;
}
```

### Vacancy

```protobuf
message Vacancy {
    string Id = 1;
    string Title = 2;
    string Description = 3;
    int32 Division = 4;
    string Country = 5;
    google.protobuf.Timestamp created_at = 6;
    google.protobuf.Timestamp updated_at = 7;
}
```

### User

```protobuf
message User {
    string Id = 1;
    string Name = 2;
    string Email = 3;
}
```
