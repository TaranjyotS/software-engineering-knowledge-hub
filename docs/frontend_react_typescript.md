# Frontend, React, TypeScript & Product Engineering

> **Purpose:** React, TypeScript, frontend API integration, full-stack development, and product engineering interview preparation.
> **Use this file for:** full-stack, frontend-adjacent backend, and product engineering interviews

---

## Recommended Study Flow

1. Read the **Quick Summary** first.
2. Review the **Key Concepts** and tables.
3. Practice the **Interview Questions & Answers** out loud.
4. Use the code snippets and examples to explain trade-offs clearly.
5. Finish with the **Common Mistakes** and **Revision Checklist** sections.

---

## Quick Summary

This is a new topic file created because the attached repository files did not have a dedicated Markdown page for this subject. It is merged from the organized topic-wise interview-prep pack and follows the same repository style as the existing notes.

---

## Consolidated Interview Questions & Technical Notes

> React, TypeScript, frontend API integration, full-stack/product engineering, UI-side concerns, and client-facing product workflows.

---

### 11. ReactJS Interview Topics
#### 11.1 What Is React?

> "React is a JavaScript library for building user interfaces using reusable components. It allows developers to manage UI state efficiently and build dynamic frontend applications."

#### 11.2 State vs Props

| Concept |             Meaning              |
| ------- | -------------------------------- |
| State   | Data managed inside a component  |
| Props   | Data passed from parent to child |

##### Example

```tsx
type GreetingProps = {
  name: string;
};

function Greeting({ name }: GreetingProps) {
  return <h1>Hello, {name}</h1>;
}

function Counter() {
  const [count, setCount] = React.useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

#### 11.3 React Component Lifecycle

In functional components, lifecycle behavior is handled using hooks.

```tsx
import { useEffect } from "react";

function UserProfile() {
  useEffect(() => {
    // Runs when component mounts
    console.log("Component mounted");

    return () => {
      // Runs when component unmounts
      console.log("Cleanup");
    };
  }, []);

  return <div>User Profile</div>;
}
```

#### 11.4 useEffect

> "`useEffect` is used for side effects such as API calls, subscriptions, timers, and updating external systems."

Example:

```tsx
import { useEffect, useState } from "react";

function Users() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    async function fetchUsers() {
      const response = await fetch("/api/users");
      const data = await response.json();
      setUsers(data);
    }

    fetchUsers();
  }, []);

  return <pre>{JSON.stringify(users, null, 2)}</pre>;
}
```

#### 11.5 useMemo

> "`useMemo` is used to memoize expensive calculations so they are not recomputed unnecessarily on every render."

```tsx
const filteredUsers = useMemo(() => {
  return users.filter((user) => user.active);
}, [users]);
```

#### 11.6 useEffect vs useMemo

|   Hook    |                   Used For                   |
| --------- | -------------------------------------------- |
| useEffect | Side effects like API calls                  |
| useMemo   | Performance optimization for computed values |

#### 11.7 Virtual DOM

> "React keeps a virtual representation of the UI in memory. When state changes, React compares the new virtual DOM with the previous one and updates only the necessary parts of the real DOM."

#### 11.8 React Interview Line

> "I understand React through components, props, state, hooks, lifecycle behavior, API integration, and reusable UI development."

---

### 12. TypeScript Interview Topics
#### 12.1 Why Use TypeScript?

> "TypeScript adds static typing to JavaScript, helping catch errors earlier, improve maintainability, and provide better IDE support."

#### 12.2 Benefits

- Compile-time error detection
- Better autocomplete
- Safer refactoring
- Clear contracts between components
- Improved maintainability
- Better API response typing

#### 12.3 Interface vs Type

|         Interface         |             Type              |
| ------------------------- | ----------------------------- |
| Best for object contracts | More flexible                 |
| Can be extended           | Supports unions/intersections |
| Can be merged             | Good for advanced types       |

##### Example

```ts
interface User {
  id: number;
  name: string;
}

type ApiResponse<T> = {
  data: T;
  error?: string;
};
```

#### 12.4 TypeScript API Integration Example

```ts
type AgentResponse = {
  answer: string;
  sources: string[];
  confidence: number;
};

async function askAgent(question: string): Promise<AgentResponse> {
  const response = await fetch("/api/agent", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch agent response");
  }

  return response.json();
}
```

---

### 15. Full-Stack / Product Engineering
#### Likely Questions

- Have you owned features end-to-end?
- Are you comfortable touching frontend?
- How do you work with product requirements?
- How do you clarify ambiguous tasks?
- How do you make technical tradeoffs?
- How do you design UI/API contracts?
- How do you balance speed and quality?
- How do you handle legacy systems?

---

#### How to Answer Full-Stack Comfort

> My strongest area is backend engineering, but I am comfortable working across the stack when needed. I have worked on frontend integrations, API wiring, data flow, and deployment. I do not see ownership as stopping at the backend boundary. If a feature needs frontend changes, API updates, tests, and deployment, I am comfortable taking responsibility for the full workflow.

---

#### Clarifying Ambiguous Requirements

Ask questions like:

- Who is the user?
- What problem are we solving?
- What is the expected outcome?
- What are edge cases?
- What should happen on failure?
- Is this synchronous or asynchronous?
- What data needs to be stored?
- What metrics define success?
- What is the smallest useful version?

---

#### Example Feature Breakdown

```text
Feature: Allow users to request order cancellation.

Backend:
- Create cancellation request table
- Add POST /orders/{id}/cancel endpoint
- Validate order status
- Trigger background workflow if cancellation requires external sync

Frontend:
- Add cancel button
- Show confirmation modal
- Display cancellation status

Testing:
- Unit tests for status validation
- API tests for endpoint behavior
- Integration tests for background task

Production:
- Log cancellation attempts
- Monitor failure rate
- Add alert for external sync failures
```

---
