
from features.dashboard.db_queries import DB_Queries as dashboard_queries
import pandas as pd
import plotly.express as px


class DashboardWidgets:
    @staticmethod
    def defect_rate_per_batch_chart(db_conn):
        df_defect_batch = pd.read_sql_query(
            dashboard_queries.defect_rate_per_batch_query(), db_conn)
        fig = px.bar(df_defect_batch, x='batch_name',
                     y='defect_rate',

                     color='batch_name',
                     color_discrete_sequence=['brown']
                     )
        # Display the chart in streamlit
        fig.update_layout(
            title='Defect Rate per Batch',
            xaxis_title="Batch Name",
            yaxis_title="Defect Rate",

        )
        return fig

    @staticmethod
    def defect_rate_over_time_chart(db_conn):
        df_defect_overtime = pd.read_sql_query(
            dashboard_queries.defect_rate_over_time_query(), db_conn)
        fig = px.line(df_defect_overtime, x='date', y='defect_rate')

        # Customizing the plot
        fig.update_layout(
            title="Defect Rate Over Time",
            xaxis_title="Date",
            yaxis_title="Defect Rate"
        )
        fig.update_traces(line_color='red')
        return fig

    @staticmethod
    def defect_rate_by_product_model(db_conn):
        df_defect_product_model = pd.read_sql_query(
            dashboard_queries.defect_rate_by_product_model_query(), db_conn)
        fig = px.bar(df_defect_product_model, x='product_model', y='defect_rate',
                     color='product_model',
                     color_discrete_sequence=['orange']
                     )

        # Display chart in Streamlit app
        fig.update_layout(
            title='Defect Rate by Product Model',
            xaxis_title="Product Model",
            yaxis_title="Defect Rate"
        )

        return fig
