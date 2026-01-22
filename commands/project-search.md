# Project Search Command

Investigates project patterns and searches the internet for relevant solutions to a specific request (refactor, feature, bug, etc.), compiling findings into an `initial_search.md` file.

## Objective

Analyze the current project and search for implementation patterns that help solve the request, always prioritizing consistency with existing project patterns.

## Instructions

When the user invokes this command with a request:

1. **Request Analysis**: Clearly identify:
   - Type: refactor, feature, bug, improvement, etc.
   - Scope: which files/modules may be involved
   - Relevant technical keywords

2. **Project Investigation** (Priority 1):
   - Explore the codebase to identify existing patterns related to the request
   - Search for:
     - Similar folder and file structure
     - Naming patterns
     - Architectural patterns (controllers, services, repositories, etc.)
     - Libraries and frameworks in use
     - Code conventions (error handling, validation, etc.)
     - Examples of similar implementations
   - **Document all patterns found**

3. **Internet Research** (Complementary):
   - After understanding project patterns, search for:
     - Related best practices
     - Applicable design patterns
     - Solutions to similar problems
     - Libraries/tools that might help
   - Priority sources:
     - Official documentation of technologies used in the project
     - Stack Overflow
     - GitHub (issues, discussions, examples)
     - Relevant technical articles

4. **Pattern Decision**:
   - **ALWAYS prioritize existing project patterns**
   - Suggest alternative patterns from the internet ONLY if:
     - Current pattern is causing significant problems
     - The change will bring clear benefits in clean code, maintainability, or performance
     - The change is truly necessary to implement the request
   - Clearly justify any suggestion for pattern change

5. **File Compilation**:
   - Name: `initial_search.md`
   - Structure:
     - **Request**: Clear description of what was requested
     - **Project Patterns**: Documentation of patterns found (categorized)
     - **Relevant Files**: List of key files for implementation
     - **Internet Patterns**: Solutions and best practices found
     - **Recommendation**: Suggested approach prioritizing consistency
     - **Implementation**: High-level steps for implementation
     - **References**: URLs of all sources consulted

6. **Execution**:
   - Use Task tool with Explore agent for codebase investigation
   - Use Read tool to examine relevant files
   - Use WebSearch tool for complementary searches
   - Be methodical and document everything found
   - Save the file in the current directory

## Principles

- **Consistency over novelty**: Maintaining a consistent pattern is more important than using the "latest trendy pattern"
- **Pragmatism**: Only suggest pattern changes if truly necessary
- **Complete documentation**: The more context, the better the decision
- **Respect for legacy**: Understand why current patterns exist before suggesting changes

## Usage

```
/project-search <request description>
```

Examples:
```
/project-search Add JWT authentication to API routes
/project-search Refactor form validation to use Zod
/project-search Fix concurrency bug in payment processing
/project-search Implement Redis cache for frequent queries
```
