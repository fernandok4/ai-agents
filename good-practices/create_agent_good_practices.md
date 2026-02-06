# How Sub-Agents Are Created: The Anatomy of a Perfect Subagent Prompt

*Search Date*: 2026-02-06

---

## 1. Overview

Sub-agents are specialized AI instances spawned by a parent (orchestrator) agent to handle focused subtasks. They run in isolated context windows with custom system prompts, specific tool access, and independent permissions. The "perfect" subagent prompt is not a single template but a combination of *clear identity, **precise scope, **constrained tools, and **actionable instructions* tailored to a single responsibility.

This document synthesizes findings from Anthropic's official guidance, Claude Code/Agent SDK documentation, Google ADK, OpenAI Swarm, LangChain/LangGraph, and prompt engineering research to provide a comprehensive guide on creating effective subagent prompts.

---

## 2. Why Sub-Agents Exist

Current LLMs degrade with very long, multi-objective prompts and large tool sets. Sub-agents solve this by:

| Problem | Sub-Agent Solution |
|---|---|
| Context window bloat | Each sub-agent has its own isolated context |
| Too many tools confuse the model | Each sub-agent gets only the tools it needs |
| Multi-step tasks compound errors | Focused single-responsibility reduces error cascading |
| Slow sequential execution | Independent sub-agents can run in parallel |
| Generic behavior | Specialized prompts produce domain-expert responses |

> "It makes sense to implement separate processes as different sub-modules, each specializing in its own task." — Multi-Agent Systems Research

---

## 3. Core Architecture Patterns

### 3.1 Orchestrator-Workers (Most Common)

A central LLM dynamically breaks down tasks and delegates to worker sub-agents, then synthesizes results. Best for unpredictable subtask requirements.


User Request → Orchestrator Agent → [Sub-Agent A, Sub-Agent B, Sub-Agent C] → Synthesized Result


### 3.2 Sequential Pipeline

Sub-agents execute one after another, each passing results via shared state.


Input → Agent 1 (Parse) → Agent 2 (Process) → Agent 3 (Validate) → Output


### 3.3 Routing/Dispatch

A classifier agent routes requests to the appropriate specialist based on intent analysis and sub-agent descriptions.

### 3.4 Parallelization

Independent sub-agents run simultaneously. Two variations:
- *Sectioning*: Different subtasks in parallel
- *Voting*: Same task multiple times for confidence

### 3.5 Evaluator-Optimizer

One agent generates, another evaluates and provides feedback iteratively.

---

## 4. Anatomy of the Perfect Subagent Prompt

Based on analysis across all major frameworks, the perfect subagent prompt has *7 essential components*:

### 4.1 Identity / Role (WHO)

Assign a clear expert persona. Role prompting improves relevance, tone, and domain focus.


You are a senior security code reviewer with expertise in OWASP Top 10
vulnerabilities, authentication patterns, and secure coding practices.


*Rules:*
- Be specific about the domain ("senior security reviewer" not "helpful assistant")
- Include relevant qualifications that shape behavior
- Keep it to 1-2 sentences

### 4.2 Purpose / Scope (WHAT)

Define exactly what the sub-agent does and doesn't do.


When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

You do NOT modify code. You only analyze and report.


*Rules:*
- State primary objective explicitly
- Use numbered workflows for multi-step tasks
- Define boundaries (what's out of scope)

### 4.3 Methodology / Process (HOW)

Provide the step-by-step approach or decision framework.


Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states


*Rules:*
- Include chain-of-thought scaffolding
- Provide decision frameworks for ambiguous cases
- Define quality control checkpoints

### 4.4 Output Format (SHAPE)

Specify how results should be structured.


Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific code examples showing how to fix each issue.


*Rules:*
- Define the structure (lists, JSON, prose, etc.)
- Specify granularity (summary vs. detailed)
- Include examples when format is complex

### 4.5 Constraints / Guardrails (LIMITS)

Set behavioral boundaries and safety rules.


You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify
schema, explain that you only have read access.

Do not assume shared understanding. Ask for clarification when
requirements are ambiguous.


*Rules:*
- Be explicit about what's forbidden
- Allow expressing uncertainty ("say 'I don't know' rather than guess")
- Include safety and ethical boundaries

### 4.6 Domain Knowledge / Context (CONTEXT)

Inject relevant knowledge the sub-agent needs.


Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability


*Rules:*
- Include only context relevant to the sub-agent's task
- Provide each sub-agent only the slice of context it needs
- Avoid information overload

### 4.7 Escalation / Edge Cases (FALLBACKS)

Define what happens when things go wrong.


If you encounter:
- Compilation errors: report the error, suggest a fix, do NOT retry blindly
- Ambiguous requirements: ask for clarification before proceeding
- Tasks outside your scope: explain why and suggest the appropriate agent


---

## 5. The Description Field: Your Routing API

The description field is *separate from the system prompt* and is the most critical piece for delegation. The parent agent uses this to decide WHEN to delegate.

### What Makes a Good Description

| Bad | Good |
|---|---|
| "A helpful code agent" | "Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code." |
| "Handles database stuff" | "Execute read-only database queries. Use when analyzing data or generating reports." |
| "Test helper" | "Runs and analyzes test suites. Use for test execution and coverage analysis." |

### Rules for Descriptions

1. *State the expertise clearly*: What domain does this agent cover?
2. *State the trigger condition*: When should the parent delegate to it?
3. *Use action-oriented language*: "Use when...", "Invoke for..."
4. *Include "proactively" for agents that should auto-trigger*: "Use proactively after code changes"
5. *Be precise*: The description is effectively API documentation for the LLM router

> "When using routing, the description field of your sub-agents is effectively your API documentation for the LLM. Be precise." — Google ADK Documentation

---

## 6. Configuration Structure Across Frameworks

### 6.1 Claude Code (Markdown + YAML Frontmatter)

markdown
---
name: code-reviewer
description: Expert code review specialist. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: sonnet
memory: user
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.


*Supported Fields:*

| Field | Required | Purpose |
|---|---|---|
| name | Yes | Unique identifier (lowercase, hyphens) |
| description | Yes | When to delegate (routing trigger) |
| tools | No | Allowed tools (inherits all if omitted) |
| disallowedTools | No | Tools to deny |
| model | No | sonnet, opus, haiku, or inherit |
| permissionMode | No | default, acceptEdits, dontAsk, bypassPermissions, plan |
| skills | No | Skills to preload into context |
| hooks | No | Lifecycle hooks scoped to this sub-agent |
| memory | No | Persistent memory: user, project, or local |

### 6.2 Claude Agent SDK (Programmatic)

python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

agents = {
    "code-reviewer": AgentDefinition(
        description="Expert code review specialist. Use for quality, security, and maintainability reviews.",
        prompt="""You are a code review specialist with expertise in security, performance, and best practices.

When reviewing code:
- Identify security vulnerabilities
- Check for performance issues
- Verify adherence to coding standards
- Suggest specific improvements

Be thorough but concise in your feedback.""",
        tools=["Read", "Grep", "Glob"],
        model="sonnet"
    )
}


### 6.3 Claude Code Internal Agent Creation (JSON)

Claude Code's own agent architect uses this JSON structure:

json
{
  "identifier": "descriptive-agent-name",
  "whenToUse": "Use this agent when... [precise triggering conditions with examples]",
  "systemPrompt": "Complete operational manual in second person"
}


The five-step internal process:
1. *Extract Core Intent*: Identify purpose, responsibilities, success criteria
2. *Design Expert Persona*: Create a compelling identity with domain knowledge
3. *Architect Instructions*: Behavioral boundaries, methodologies, edge cases, output formats
4. *Optimize for Performance*: Decision frameworks, quality control, escalation strategies
5. *Create Identifier*: 2-4 word descriptive name (lowercase, hyphens)

### 6.4 Google ADK

python
specialist = Agent(
    name="billing_specialist",
    model="gemini-2.0-flash",
    description="Handles billing inquiries and invoices",
    instruction="Analyze user intent. Resolve billing issues using the BillingDB tool.",
    tools=[billing_tool],
    sub_agents=[]
)


### 6.5 OpenAI Agents SDK / Swarm

python
agent = Agent(
    name="code_reviewer",
    instructions="You are a code reviewer. Focus on security and best practices.",
    tools=[read_file, grep_search],
    model="gpt-4o"
)


### 6.6 LangChain / LangGraph Deep Agents

python
subagents = {
    "researcher": {
        "name": "researcher",
        "description": "Searches and analyzes documentation",
        "system_prompt": "You are a research specialist...",
        "tools": [search_tool, read_tool],
        "model": "claude-sonnet-4-5-20250929"
    }
}


---

## 7. Best Practices (Consolidated)

### 7.1 Prompt Engineering

| Principle | Details |
|---|---|
| *One goal per agent* | Each sub-agent should excel at exactly one task |
| *Be explicit, not implicit* | Don't assume the model will infer intent — state it |
| *Simple language* | If a "smart but lazy 12-year-old" can understand your tools, LLMs will too |
| *Include examples* | Few-shot examples dramatically improve output quality |
| *Allow uncertainty* | Give permission to say "I don't know" to reduce hallucination |
| *Be honest/critical* | Override the default agreeable demeanor with "be honest" or "be critical" |
| *Iterate* | Treat prompts like code — version, test, refine |

### 7.2 Tool Configuration

- *Principle of Least Privilege*: Grant only necessary tools
- *Document tools thoroughly*: Name, description, parameters, edge cases
- *Common combinations*:

| Use Case | Tools |
|---|---|
| Read-only analysis | Read, Grep, Glob |
| Test execution | Bash, Read, Grep |
| Code modification | Read, Edit, Write, Grep, Glob |
| Full access | Inherit all (omit tools field) |

### 7.3 Context Management

- *Isolate context*: Sub-agents prevent information overload in the main conversation
- *Provide only relevant context*: Don't dump everything — give each sub-agent only what it needs
- *Use persistent memory* for sub-agents that improve over time
- *Consider model selection*: Use Haiku for fast, cheap exploration; Sonnet for balanced work; Opus for high-stakes analysis

### 7.4 Coordination

- *Parent prompt should mention sub-agents by name* and describe delegation conditions
- *Use descriptive state keys* so downstream agents understand shared data
- *Start simple*: Begin with sequential chains, then add complexity
- *Sub-agents cannot spawn sub-agents* (in most frameworks) — design accordingly

---

## 8. Complete Template: The "Perfect" Subagent Prompt

markdown
---
name: <lowercase-hyphenated-name>
description: <1-2 sentences: what it does + when to use it. Action-oriented.>
tools: <comma-separated tool list OR omit to inherit all>
model: <sonnet|opus|haiku|inherit>
memory: <user|project|local> (optional)
---

You are a [specific expert role] specializing in [domain expertise].

## When Invoked

1. [First step — gather context]
2. [Second step — analyze/process]
3. [Third step — produce output]

## Methodology

- [Approach 1]
- [Approach 2]
- [Approach 3]

## Output Format

Provide results as:
- [Format specification]
- [Structure requirements]
- [Priority or ordering rules]

## Constraints

- [What you must NOT do]
- [Scope boundaries]
- [Safety rules]

## Edge Cases

- If [situation A]: [response]
- If [situation B]: [response]
- If unclear: ask for clarification before proceeding

Focus on [primary quality metric]. Be [specific behavioral trait].


---

## 9. Real-World Examples

### Example 1: Debugger Agent

markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.


### Example 2: Data Scientist Agent

markdown
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.


### Example 3: Read-Only DB Query Agent (with Hooks)

markdown
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.


---

## 10. Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| Vague descriptions ("helpful agent") | Parent can't route tasks correctly | Be specific about expertise and trigger conditions |
| Too many tools | Confuses the model, increases errors | Grant only tools the sub-agent needs |
| Multi-objective prompts | LLMs degrade with many competing goals | One agent, one job |
| No output format spec | Inconsistent, unparseable responses | Define the expected structure explicitly |
| Skipping examples | Model guesses the format/approach | Add 1-2 few-shot examples |
| Over-engineering | Complex nested agents add latency and errors | Start simple; add complexity only when measured |
| No escalation path | Agent gets stuck on edge cases | Define "if confused, do X" behavior |
| Copying parent context | Bloats sub-agent, reduces focus | Provide only the slice of context needed |

---

## 11. Key Insight from Anthropic

> "Over the past year, we worked with dozens of teams building LLM agents. Consistently, the most successful implementations weren't using complex frameworks or specialized libraries, but instead were building with simple, composable patterns."
> 
>— Anthropic, "Building Effective Agents"

The perfect sub-agent prompt is *not the most sophisticated one*. It is the simplest one that clearly defines:
1. *Who* the agent is (role)
2. *When* it should be invoked (description)
3. *What* it should do (scope)
4. *How* it should do it (methodology)
5. *What shape* the output takes (format)
6. *What it must NOT do* (constraints)
7. *What to do when stuck* (fallbacks)

---

## References

- [Building Effective AI Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)
- [Create Custom Subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents)
- [Subagents in the SDK — Claude API Docs](https://platform.claude.com/docs/en/agent-sdk/subagents)
- [Claude Code System Prompts — Piebald-AI (GitHub)](https://github.com/Piebald-AI/claude-code-system-prompts)
- [Agent Creation Architect Prompt — Piebald-AI](https://github.com/Piebald-AI/claude-code-system-prompts/blob/main/system-prompts/agent-prompt-agent-creation-architect.md)
- [Awesome Claude Code Subagents — VoltAgent (GitHub)](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [Developer's Guide to Multi-Agent Patterns in ADK — Google Developers Blog](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
- [Multi-Agent Systems — Google ADK Docs](https://google.github.io/adk-docs/agents/multi-agents/)
- [Orchestrating Multiple Agents — OpenAI Agents SDK](https://openai.github.io/openai-agents-python/multi_agent/)
- [OpenAI Swarm Framework (GitHub)](https://github.com/openai/swarm)
- [Orchestrating Agents: Routines and Handoffs — OpenAI Cookbook](https://cookbook.openai.com/examples/orchestrating_agents)
- [Subagents — LangChain Docs](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents)
- [Choosing the Right Multi-Agent Architecture — LangChain Blog](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/)
- [LLM Agents — Prompt Engineering Guide](https://www.promptingguide.ai/research/llm-agents)
- [Deep Agents — Prompt Engineering Guide](https://www.promptingguide.ai/agents/deep-agents)
- [Prompt Engineering for AI Agents — PromptHub](https://www.prompthub.us/blog/prompt-engineering-for-ai-agents)
- [LLM Powered Autonomous Agents — Lilian Weng](https://lilianweng.github.io/posts/2023-06-23-agent/)
- [Task Decomposition Prompts for Agents — APXML](https://apxml.com/courses/prompt-engineering-agentic-workflows/chapter-4-prompts-agent-planning-task-management/breaking-down-problems-prompts)
- [The Ultimate Guide to Prompt Engineering 2026 — Lakera](https://www.lakera.ai/blog/prompt-engineering-guide)
- [Best Practices for Prompt Engineering — Claude Blog](https://claude.com/blog/best-practices-for-prompt-engineering)
- [Best Practices for Claude Code Subagents — PubNub](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)
- [Tracing Claude Code's LLM Traffic — George Sung (Medium)](https://medium.com/@georgesung/tracing-claude-codes-llm-traffic-agentic-loop-sub-agents-tool-use-prompts-7796941806f5)
- [The Complete Guide to Building Agents with Claude Agent SDK — Nader Dabit](https://nader.substack.com/p/the-complete-guide-to-building-agents)
- [Best Practices for LLM Prompt Engineering — Palantir](https://www.palantir.com/docs/foundry/aip/best-practices-prompt-engineering)
- [Prompt Engineering Techniques Top 6 for 2026 — K2View](https://www.k2view.com/blog/prompt-engineering-techniques/)
- [The Ultimate LLM Agent Build Guide — Vellum](https://www.vellum.ai/blog/the-ultimate-llm-agent-build-guide)
- [AgentMesh: Multi-Agent Framework for Software Development — arXiv](https://arxiv.org/html/2507.19902v1)