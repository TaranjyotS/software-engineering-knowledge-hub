# Power BI

> **Purpose:** Power BI concepts, DAX basics, data modeling, relationships, slicers, filters, RLS, and dashboard performance.
> **Use this file for:** BI analyst, data analyst, reporting, and dashboard interviews

---

## Recommended Study Flow

1. Read the **Quick Summary** first.
2. Review the **Key Concepts** and tables.
3. Practice the **Interview Questions & Answers** out loud.
4. Use the code snippets and examples to explain trade-offs clearly.
5. Finish with the **Common Mistakes** and **Revision Checklist** sections.

---

## Quick Summary

Power BI is used for business intelligence dashboards, data modeling, and interactive reporting. For interviews, focus on relationships, DAX, slicers vs filters, row-level security, and performance optimization.

---

## Key Concepts

| Concept           | Explanation                                           |
| ----------------- | ----------------------------------------------------- |
| Calculated column | Computed during data refresh and stored in the model  |
| Measure           | Computed dynamically based on filter context          |
| Slicer            | Visual filter users interact with on the report page  |
| Filter pane       | Non-visual filtering at visual/page/report level      |
| Relationship      | Connects tables through keys for cross-table analysis |
| RLS               | Restricts data visibility by user/role                |
| CALCULATE         | Modifies filter context for a DAX expression          |

---

## Interview Questions & Answers
### Q1. What is the difference between a slicer and a filter?

**Answer:** A slicer is a visual element on the report page that users can interact with. A filter is configured in the filter pane and can apply to a visual, page, or entire report.

### Q2. How do you create relationships between tables?

Go to **Model View**, drag a key from one table to the matching key in another table, and set cardinality and filter direction carefully.

### Q3. What is row-level security?

Row-level security restricts which rows a user can see based on roles and DAX filter expressions.

```DAX
[Region] = "Canada"
```

### Q4. What does CALCULATE do?

`CALCULATE` evaluates an expression under a modified filter context.

```DAX
Canada Sales = CALCULATE(SUM(Sales[Amount]), Sales[Country] = "Canada")
```

### Q5. How do you improve Power BI dashboard performance?

- Use a clean star schema.
- Remove unused columns.
- Prefer measures over unnecessary calculated columns.
- Reduce high-cardinality fields.
- Use aggregations where possible.
- Limit visuals and complex filters.

---

## Revision Checklist

- [ ] Measures vs calculated columns
- [ ] CALCULATE and FILTER
- [ ] Slicers vs filters
- [ ] Relationships and cardinality
- [ ] Row-level security
- [ ] Dashboard performance
