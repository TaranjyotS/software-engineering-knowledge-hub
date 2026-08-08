# Excel

> **Purpose:** Excel formulas, lookup functions, pivot tables, conditional formatting, and spreadsheet interview preparation.
> **Use this file for:** data analyst, business analyst, QA/data validation, and reporting interviews

---

## Recommended Study Flow

1. Read the **Quick Summary** first.
2. Review the **Key Concepts** and tables.
3. Practice the **Interview Questions & Answers** out loud.
4. Use the code snippets and examples to explain trade-offs clearly.
5. Finish with the **Common Mistakes** and **Revision Checklist** sections.

---

## Quick Summary

Excel is commonly used for data cleaning, reporting, reconciliation, and quick analysis. For interviews, focus on lookup formulas, pivot tables, conditional formatting, references, and basic data validation.

---

## Key Concepts

|        Concept         |                                      What to Know                                       |
| ---------------------- | --------------------------------------------------------------------------------------- |
| VLOOKUP                | Looks up a value in the first column of a range and returns a value from another column |
| XLOOKUP                | Modern replacement for VLOOKUP with flexible lookup and return arrays                   |
| Absolute reference     | `$A$1` stays fixed when copied                                                          |
| Relative reference     | `A1` changes when copied                                                                |
| Pivot table            | Summarizes data by rows, columns, values, and filters                                   |
| Conditional formatting | Highlights values based on rules                                                        |
| IF / AND / OR          | Adds conditional logic to formulas                                                      |

---

## Interview Questions & Answers
### Q1. What is the difference between VLOOKUP and XLOOKUP?

**Answer:** VLOOKUP searches the first column of a range and returns a value from a specified column index. XLOOKUP is more flexible because it can search left or right, does not require a column index, and has better default exact-match behavior.

```excel
=VLOOKUP(A2, Sheet2!A:B, 2, FALSE)
=XLOOKUP(A2, Sheet2!A:A, Sheet2!B:B)
```

### Q2. What is the difference between absolute and relative references?

**Answer:** A relative reference like `A1` changes when copied. An absolute reference like `$A$1` remains fixed. Use absolute references when pointing to fixed assumptions such as tax rate, exchange rate, or lookup range.

### Q3. How do you create a pivot table?

**Answer:** Select the dataset, go to **Insert > PivotTable**, choose the destination, then drag fields into Rows, Columns, Values, and Filters. Pivot tables are useful for sums, counts, averages, and grouped analysis.

### Q4. How do you combine IF, AND, and OR?

```excel
=IF(AND(B2>=80,C2="Pass"),"Eligible","Not Eligible")
=IF(OR(B2="High",C2>1000),"Review","OK")
```

### Q5. How do you highlight values greater than 100?

Use **Home > Conditional Formatting > Highlight Cell Rules > Greater Than**, then enter `100` and choose a format.

---

## Common Mistakes

- Using approximate match in VLOOKUP accidentally.
- Forgetting `$` in fixed lookup ranges.
- Building pivot tables on messy data with blank headers.
- Hardcoding values instead of using reference cells.
- Not checking duplicate lookup keys.

---

## Revision Checklist

- [ ] VLOOKUP and XLOOKUP
- [ ] Absolute vs relative references
- [ ] Pivot tables
- [ ] Conditional formatting
- [ ] IF, AND, OR
- [ ] Basic charts and filters
