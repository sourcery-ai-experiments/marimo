from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Any

from marimo._data.models import DataType


@abc.abstractmethod
class ChartBuilder:
    @abc.abstractmethod
    def altair_json(self, data: Any, column: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def altair_code(self, data: str, column: str) -> str:
        raise NotImplementedError


@dataclass
class ChartParams:
    table_name: str
    column: str


class NumberChartBuilder(ChartBuilder):
    def altair_json(self, data: Any, column: str) -> str:
        import altair as alt

        return (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x=alt.X(column, type="quantitative", bin=True),
                y=alt.Y("count()", type="quantitative"),
            )
            .to_json()
        )

    def altair_code(self, data: str, column: str) -> str:
        return f"""
        chart = (
            alt.Chart({data})
            .mark_bar()
            .encode(
                x=alt.X({column}, type="quantitative", bin=True),
                y=alt.Y("count()", type="quantitative"),
            )
        )
        """


class StringChartBuilder(ChartBuilder):
    def altair_json(self, data: Any, column: str) -> str:
        import altair as alt

        return (
            alt.Chart(data)
            .transform_aggregate(count="count()", groupby=[column])
            .transform_window(
                rank="rank()",
                sort=[
                    alt.SortField("count", order="descending"),
                    alt.SortField(column, order="ascending"),
                ],
            )
            .transform_calculate(
                **{
                    column: alt.expr.if_(
                        alt.datum.rank <= 10,
                        alt.datum[column],
                        "Other",
                    )
                },
            )
            .transform_filter(alt.datum.rank <= 11)
            .mark_bar()
            .encode(
                y=alt.Y(column, type="nominal", sort="-x"),
                x=alt.X("count", type="quantitative"),
            )
            .to_json()
        )

    def altair_code(self, data: str, column: str) -> str:
        return f"""
        chart = (
            alt.Chart({data})
            .transform_aggregate(count="count()", groupby=[{column}])
            .transform_window(
                rank="rank()",
                sort=[
                    alt.SortField("count", order="descending"),
                    alt.SortField({column}, order="ascending"),
                ],
            )
            .transform_calculate(**{{
                {column}: alt.expr.if_(
                    alt.datum.rank <= 10,
                    alt.datum[{column}],
                    "Other",
            }}))
            .transform_filter(alt.datum.rank <= 11)
            .mark_bar()
            .encode(
                y=alt.Y({column}, type="nominal", sort="-x"),
                x=alt.X("count", type="quantitative"),
            )
        )
        """


class DateChartBuilder(ChartBuilder):
    def altair_json(self, data: Any, column: str) -> str:
        import altair as alt

        return (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x=alt.X(column, type="temporal"),
                y=alt.Y("count()", type="quantitative"),
            )
            .to_json()
        )

    def altair_code(self, data: str, column: str) -> str:
        return f"""
        chart = (
            alt.Chart({data})
            .mark_bar()
            .encode(
                x=alt.X({column}, type="temporal"),
                y=alt.Y("count()", type="quantitative"),
            )
        )
        """


class BooleanChartBuilder(ChartBuilder):
    def altair_json(self, data: Any, column: str) -> str:
        import altair as alt

        return (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x=alt.X(column, type="nominal"),
                y=alt.Y("count()", type="quantitative"),
            )
            .to_json()
        )

    def altair_code(self, data: str, column: str) -> str:
        return f"""
        chart = (
            alt.Chart({data})
            .mark_bar()
            .encode(
                x=alt.X({column}, type="nominal"),
                y=alt.Y("count()", type="quantitative"),
            )
        )
        """


class IntegerChartBuilder(ChartBuilder):
    def altair_json(self, data: Any, column: str) -> str:
        import altair as alt

        return (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x=alt.X(column, type="quantitative", bin=True),
                y=alt.Y("count()", type="quantitative"),
            )
            .to_json()
        )

    def altair_code(self, data: str, column: str) -> str:
        return f"""
        chart = (
            alt.Chart({data})
            .mark_bar()
            .encode(
                x=alt.X({column}, type="quantitative", bin=True),
                y=alt.Y("count()", type="quantitative"),
            )
        )
        """


class UnknownChartBuilder(ChartBuilder):
    def altair_json(self, data: Any, column: str) -> str:
        import altair as alt

        return (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x=alt.X(column, type="nominal"),
                y=alt.Y("count()", type="quantitative"),
            )
            .to_json()
        )

    def altair_code(self, data: str, column: str) -> str:
        return f"""
        chart = (
            alt.Chart({data})
            .mark_bar()
            .encode(
                x=alt.X({column}, type="nominal"),
                y=alt.Y("count()", type="quantitative"),
            )
        )
        """


class ArgsAsStringChartBuilder(ChartBuilder):
    def __init__(self, delegate: ChartBuilder):
        self.delegate = delegate

    def altair_json(self, data: Any, column: str) -> str:
        return self.delegate.altair_json(data, f'"{column}"')

    def altair_code(self, data: str, column: str) -> str:
        return self.delegate.altair_code(f'"{data}"', f'"{column}"')


def get_chart_builder(column_type: DataType) -> ChartBuilder:
    if column_type == "number":
        return ArgsAsStringChartBuilder(NumberChartBuilder())
    if column_type == "string":
        return ArgsAsStringChartBuilder(StringChartBuilder())
    if column_type == "date":
        return ArgsAsStringChartBuilder(DateChartBuilder())
    if column_type == "boolean":
        return ArgsAsStringChartBuilder(BooleanChartBuilder())
    if column_type == "integer":
        return ArgsAsStringChartBuilder(IntegerChartBuilder())
    if column_type == "unknown":
        return ArgsAsStringChartBuilder(UnknownChartBuilder())