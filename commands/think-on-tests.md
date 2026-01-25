# Think on Tests Command

Analyzes a given class and generates a comprehensive test plan document with all test cases (success and failure scenarios), without writing any test code.

## Objective

Deeply understand a class's responsibilities, behaviors, and edge cases to produce a detailed test case document at `docs/<path/to/the/class>.md`. The document serves as a blueprint the developer validates before any test is written.

## Instructions

When the user invokes this command with a class path:

1. **Class Identification**: Read and fully understand the target class:
   - Identify the class type (Controller, Service, Repository, Helper, etc.)
   - Read the entire file and all direct dependencies (interfaces, DTOs, enums, etc.)
   - Map all public and protected methods
   - Identify external dependencies (other services, repositories, HTTP clients, etc.)

2. **Context Gathering**: Investigate the surrounding context:
   - Read related classes that interact with the target
   - Understand the business rules embedded in the class
   - Check for existing validation, error handling, and authorization logic
   - If a Controller: trace the full request lifecycle (middleware, validation, service calls, responses)
   - If a Service: identify all business rules, conditional branches, and side effects

3. **Test Strategy Selection**: Apply the appropriate strategy based on class type:

   **Controllers (Integration/E2E mindset)**:
   - Think as a real user navigating the application
   - Map all HTTP endpoints (method, route, parameters, body, headers)
   - For each endpoint, think about:
     - Successful requests with valid data
     - Validation failures (missing fields, invalid formats, wrong types)
     - Authentication and authorization failures (unauthenticated, forbidden)
     - Resource not found scenarios
     - Conflict and duplicate scenarios
     - Edge cases in query parameters, pagination, filters
     - Response status codes and body structure

   **Services (Unit test mindset)**:
   - Focus on isolated business logic
   - For each public method, think about:
     - Happy path with valid inputs
     - Each conditional branch and its trigger
     - Boundary values and edge cases
     - Exception and error scenarios
     - Behavior with null/empty/undefined inputs
     - Side effects (events emitted, external calls made, state changes)
     - Interaction with mocked dependencies

   **Repositories / Data Access**:
   - Query correctness with various filters
   - Empty result scenarios
   - Data integrity edge cases

   **Other class types**:
   - Apply unit test mindset by default
   - Adapt based on the class's role and responsibilities

4. **Test Case Documentation**: Use the **AAA Pattern (Arrange, Act, Assert)** for every test case:
   - **Group**: Logical grouping (by method, endpoint, or feature)
   - **Test name**: Clear description using "should" convention (e.g., "should return 404 when user does not exist")
   - **Arrange**: Describe in plain human language the preconditions and setup needed (e.g., "A user with admin role exists in the database and an expired discount coupon is associated to their account"). Never use code snippets or programming syntax.
   - **Act**: Describe in plain human language the single action being tested (e.g., "The user submits a purchase request using the expired coupon"). Never use code snippets or programming syntax.
   - **Assert**: Describe in plain human language all expected outcomes to verify (e.g., "The request is rejected with a validation error indicating the coupon has expired, and no order is created in the database"). Never use code snippets or programming syntax.
   - **Priority**: High, Medium, or Low based on risk and importance

5. **Existing Document Check**:
   - Before writing, check if `docs/<path/to/the/class>.md` already exists
   - If it exists:
     - Read the current content
     - Compare with the new analysis
     - **Ask the user for permission before updating or removing any existing test case**
     - Only suggest updates when the existing test case is outdated, incorrect, or would break the application
     - Add new test cases without disturbing existing ones unless approved
   - If it does not exist: create the file with the full test plan

6. **File Generation**:
   - Path: `docs/<path/to/the/class>.md` (mirroring the class's source path)
   - Structure:
     - **Class**: Full class name and source path
     - **Type**: Controller / Service / Repository / Other
     - **Description**: Brief summary of what the class does
     - **Dependencies**: List of injected or used dependencies
     - **Test Cases**: Grouped by method/endpoint with all documented cases
     - **Coverage Summary**: Total count of test cases by priority

7. **Execution**:
   - Use Read tool to load the target class
   - Use Task tool with Explore agent to understand related code and dependencies
   - Use Read tool to examine all relevant files
   - Use Glob to check if the output document already exists
   - Think deeply about every scenario before writing
   - Save the file at the documented path

## Principles

- **Think, don't code**: The output is a document with test cases, never test code
- **Completeness over speed**: Cover every scenario, every branch, every edge case
- **User perspective for Controllers**: Simulate real navigation, real payloads, real failures
- **Isolation for Services**: Each test case should target one specific behavior
- **Respect existing work**: Never overwrite existing test cases without explicit permission
- **Prioritization**: Mark the most critical scenarios as high priority so the developer knows where to start

## Usage

```
/think-on-tests <path/to/the/class>
```

Examples:
```
/think-on-tests src/controllers/UserController.ts
/think-on-tests src/services/PaymentService.ts
/think-on-tests app/Http/Controllers/OrderController.php
/think-on-tests src/main/java/com/example/service/InvoiceService.java
```
