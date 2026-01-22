# Deep Web Search Command

Performs a methodical and deep internet search on a specific topic, compiling the content into a single Markdown file.

## Objective

Search for information in reliable sources such as:
- Stack Overflow
- llm-docs.co
- Official documentation
- Scientific articles
- Relevant GitHub repositories and discussions

## Instructions

When the user invokes this command with a topic:

1. **Topic Analysis**: Identify relevant keywords and technical terms for the search

2. **Structured Search**: Execute searches across multiple relevant sources:
   - Stack Overflow: For Q&A and practical solutions
   - llm-docs.co: For LLM and AI-related documentation
   - Official documentation: For authoritative technical specifications
   - Scientific articles: For research papers and academic content
   - GitHub: For code examples, issues, and discussions
   - Other specialized sources as appropriate for the topic

3. **Content Compilation**: Organize the found information into sections **based on what's actually relevant and available**:
   - Always include an Overview/Introduction
   - Add sections that make sense for the topic (e.g., Core Concepts, Architecture, Implementation, Use Cases, Examples, Best Practices, Common Issues, Comparisons, etc.)
   - **Be flexible**: Only create sections for content you actually found
   - Prioritize quality and relevance over completeness

4. **File Format**:
   - Name: `search_<topic_description>_YYYYMMDD.md` (use underscores, lowercase)
   - Include search date
   - Organize content logically based on what was found
   - Always end with a References section listing all sources

5. **Execution**:
   - Use the WebSearch tool to search each relevant source
   - Focus on high-quality, authoritative content
   - Synthesize and summarize information (don't just copy-paste)
   - Include code examples when relevant and available
   - Add all source URLs with titles in the References section
   - Save the file in the current working directory

## Usage

```
/deep-search <topic>
```

Examples:
```
/deep-search Claude API streaming
/deep-search PostgreSQL indexing strategies
/deep-search React Server Components
```
