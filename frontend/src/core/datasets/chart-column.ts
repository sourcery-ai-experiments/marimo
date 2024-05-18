/* Copyright 2024 Marimo. All rights reserved. */
import { DataTable, DataTableColumn } from "../network/types";

/**
 * Chart the DF using altair
 */
export function chartColumn(table: DataTable, column: DataTableColumn) {
  switch (column.type) {
    case "string":
    case "boolean":
      return {
        code: `alt.Chart(${table.name}).mark_bar().encode(x='${column.name}', y='count()')`,
      };
    case "integer":
    case "number":
      return {
        code: `alt.Chart(${table.name}).mark_bar().encode(x='${column.name}', y='mean(${column.name})')`,
      };
    case "date":
      return {
        code: `alt.Chart(${table.name}).mark_bar().encode(x='${column.name}', y='count()')`,
      };
    default:
      return {
        code: `alt.Chart(${table.name}).mark_bar().encode(x='${column.name}', y='count()')`,
      };
  }
}
