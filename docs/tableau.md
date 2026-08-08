# Tableau

> **Purpose:** Tableau dashboarding, calculated fields, parameters, filters, dual-axis charts, and performance optimization.
> **Use this file for:** BI analyst, data visualization, and reporting interviews

---

## Recommended Study Flow

1. Read the **Quick Summary** first.
2. Review the **Key Concepts** and tables.
3. Practice the **Interview Questions & Answers** out loud.
4. Use the code snippets and examples to explain trade-offs clearly.
5. Finish with the **Common Mistakes** and **Revision Checklist** sections.

---

## Quick Summary

Tableau is used for visual analytics and dashboarding. For interviews, focus on calculated fields, parameters, filters, dashboard performance, and choosing the right visualization.

---

## Key Concepts

|     Concept      |                          Explanation                          |
| ---------------- | ------------------------------------------------------------- |
| Calculated field | Custom logic built from fields and functions                  |
| Parameter        | User-controlled value that can drive filters or calculations  |
| Dual-axis chart  | Combines two measures on one view with separate axes          |
| Extract          | Optimized snapshot of data for better performance             |
| Live connection  | Queries the source system directly                            |
| Dashboard action | Interactive behavior such as filter, highlight, or URL action |

---

## Interview Questions & Answers
### Q1. How do you create a calculated field?

Right-click in the data pane, select **Create Calculated Field**, enter the formula, and use it in views or filters.

```text
IF [Sales] > 100 THEN 'High' ELSE 'Low' END
```

### Q2. What is a parameter?

A parameter is a dynamic user input that can be used inside calculated fields, filters, or reference lines.

### Q3. How do you create a dual-axis chart?

Drag two measures to Rows or Columns, right-click the second axis, choose **Dual Axis**, and synchronize axes if appropriate.

### Q4. How do you optimize dashboard performance?

- Use extracts where appropriate.
- Reduce the number of filters.
- Avoid overly complex calculations.
- Limit marks and high-cardinality fields.
- Hide unused fields.
- Use context filters carefully.

### Q5. How do you create a custom date filter?

Create a calculated field using date logic or use Tableau’s built-in relative date filter.

```text
[Order Date] >= [Start Date] AND [Order Date] <= [End Date]
```

---

## Revision Checklist

- [ ] Calculated fields
- [ ] Parameters
- [ ] Filters
- [ ] Dual-axis charts
- [ ] Extracts vs live connections
- [ ] Dashboard performance
