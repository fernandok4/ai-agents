# Spec Command

Creates a detailed implementation specification from the `initial_search.md` file, producing a `spec.md` file with a concrete plan of what needs to be done.

## Objective

Transform the research and patterns from `initial_search.md` into a concrete, actionable implementation plan with specific files, methods, and changes detailed.

## Instructions

When the user invokes this command:

1. **Read Initial Search**: Load and analyze `initial_search.md` to understand:
   - The original request
   - Project patterns identified
   - Recommended approach
   - Implementation steps outlined

2. **Analyze Existing Code**: Examine the relevant files mentioned in initial_search.md:
   - Read current implementations
   - Identify existing methods and classes
   - Understand the current structure
   - Map dependencies between components

3. **Create Detailed Plan**: For each implementation step, specify:

   **Files to Create**:
   - Exact file path
   - Purpose and responsibility
   - Key exports/classes/functions

   **Files to Modify**:
   - Exact file path
   - What needs to change and why
   - Impact on existing functionality

   **Methods to Create**:
   - Method name and signature
   - Which class/file it belongs to
   - Parameters and return types
   - Responsibility and behavior
   - Dependencies it will use

   **Methods to Modify**:
   - Existing method signature
   - What changes are needed
   - Why the change is necessary
   - New behavior or logic

   **Classes to Create**:
   - Class name and file location
   - Properties and methods
   - Inheritance/interfaces
   - Relationships with other classes

   **Classes to Modify**:
   - Existing class name and location
   - New properties/methods to add
   - Properties/methods to modify
   - Refactoring needed

4. **Implementation Order**: Define the sequence of changes:
   - What should be done first (dependencies, base classes, etc.)
   - What can be done in parallel
   - What should be done last (integrations, tests, etc.)
   - Critical path items

5. **Testing Strategy**: Specify:
   - Test files to create or modify
   - Test scenarios to cover
   - Integration points to test
   - Edge cases to handle

6. **File Compilation**:
   - Name: `spec.md`
   - Structure:
     - **Summary**: Brief overview of what will be implemented
     - **Files to Create**: Detailed list with purpose
     - **Files to Modify**: Detailed list with changes
     - **Methods to Create**: Complete specifications
     - **Methods to Modify**: Existing vs new behavior
     - **Classes to Create**: Full specifications
     - **Classes to Modify**: Changes needed
     - **Implementation Order**: Step-by-step sequence
     - **Testing Strategy**: Test plan
     - **Potential Issues**: Known risks or challenges
     - **References**: Link to initial_search.md and other sources

7. **Execution**:
   - Verify initial_search.md exists in current directory
   - Use Read tool to load initial_search.md
   - Use Task tool with Explore agent if deeper code exploration is needed
   - Use Read tool to examine all relevant existing files
   - Be specific and concrete - no vague descriptions
   - Save the file in the current directory

## Principles

- **Specificity over generality**: Every spec item must be concrete and actionable
- **Completeness**: Cover all necessary changes, don't leave gaps
- **Clarity**: Anyone should be able to implement from the spec
- **Consistency**: Follow the patterns identified in initial_search.md
- **Practicality**: Consider implementation order and dependencies

## Usage

```
/spec
```

The command assumes `initial_search.md` exists in the current directory. If it doesn't exist, the command will fail and ask the user to run `/project-search` first.
