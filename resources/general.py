import os
import traceback
import pandas as pd
from flask import jsonify, Response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from data_prep_and_insert import refresh_database

from data_prep_and_insert import process_file, file_processing
from utils.sqls import sql_data_overview, sql_price_change, sql_market_comparison, sql_age_comparison
from db import db

blp = Blueprint("general", __name__, description="Utilities and queries for the general data concerning aggregates for all the cities")

@blp.route("/refresh")
class RefreshData(MethodView):
    def post(self):
        #Wykonaj data_prep_and_insert
        try:
            folder_path = os.path.join(os.getcwd(), 'data')
            files_added = []
            for filename in os.listdir(folder_path):
                # Construct the full file path by joining the folder path and filename
                file_path = os.path.join(folder_path, filename)
                # Check if it's a file (not a subdirectory)
                if os.path.isfile(file_path):
                    file_processing(file_path, db, files_added)
            return jsonify({'message': 'All well', 'files_added': files_added}), 200
        except Exception as e:
            error_traceback = traceback.format_exc()
            error_message = {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'error_traceback': error_traceback
            }
            return jsonify(error_message), 404

@blp.route("/general/overview")
class DataOverview(MethodView):
    def get(self):
        try:
            df = pd.read_sql(sql_data_overview, db.engine)
            df.set_index("city", inplace=True)
            json_data = df.to_dict(orient='index')
            return jsonify(json_data), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 404


@blp.route("/general/overview/csv")
class DataOverviewCsv(MethodView):
    def get(self):
        try:
            df = pd.read_sql(sql_data_overview, db.engine)
            df.set_index("city", inplace=True)
            csv_data = df.to_csv(index_label='index')
            response = Response(csv_data, content_type='text/csv')
            response.headers['Content-Disposition'] = f'attachment; filename=overview.csv'

            return response, 200
        except Exception as e:
            return jsonify({'error': str(e)}), 404


@blp.route("/general/price_change")
class PriceChange(MethodView):
    def get(self):
        try:
            df = pd.read_sql(sql_price_change, db.engine)
            df["time_price"] = df.apply(lambda row: {str(row["scrap_time"]): row["price"]}, axis=1)
            grouped_df = df.groupby('link')['time_price'].agg(list).reset_index()
            grouped_df.set_index("link", inplace=True)
            json_data = grouped_df.to_dict(orient='index')

            return jsonify(json_data), 200
        except Exception as e:
            error_message = {'error_type': type(e).__name__, 'error_message': str(e)}
            return jsonify(error_message), 404


@blp.route("/general/price_change/csv")
class PriceChangeCsv(MethodView):
    def get(self):
        try:
            df = pd.read_sql(sql_price_change, db.engine)
            df["time_price"] = df.apply(lambda row: {str(row["scrap_time"]): row["price"]}, axis=1)
            grouped_df = df.groupby('link')['time_price'].agg(list).reset_index()
            grouped_df.set_index("link", inplace=True)
            csv_data = grouped_df.to_csv(index_label='index')
            response = Response(csv_data, content_type='text/csv')
            response.headers['Content-Disposition'] = f'attachment; filename=price_change.csv'
            return response, 200
        except Exception as e:
            error_message = {'error_type': type(e).__name__, 'error_message': str(e)}
            return jsonify(error_message), 404


@blp.route("/general/market_comparison")
class MarketComparison(MethodView):
    def get(self):
        try:
            df = pd.read_sql(sql_market_comparison, db.engine)
            df.set_index(["city", "market"], inplace=True)
            json_data = {
                city: {
                    market: df.loc[(city, market)].to_dict()
                    for market in df.index.get_level_values('market').unique()
                }
                for city in df.index.get_level_values('city').unique()
            }
            return jsonify(json_data), 200
        except Exception as e:
            error_traceback = traceback.format_exc()
            error_message = {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'error_traceback': error_traceback
            }
            return jsonify(error_message), 404


@blp.route("/general/market_comparison/csv")
class MarketComparisonCsv(MethodView):
    def get(self):
        try:
            df = pd.read_sql(sql_market_comparison, db.engine)
            df.set_index(["city", "market"], inplace=True)
            csv_data = df.to_csv(index_label='index')
            response = Response(csv_data, content_type='text/csv')
            response.headers['Content-Disposition'] = f'attachment; filename=market_comparison.csv'

            return response, 200
        except Exception as e:
            error_traceback = traceback.format_exc()
            error_message = {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'error_traceback': error_traceback
            }
            return jsonify(error_message), 404



@blp.route("/general/age_comparison")
class AgeComparison(MethodView):
    def get(self):
        try:
            df = pd.read_sql(sql_age_comparison, db.engine)
            df.set_index(["city", "age_of_apartment"], inplace=True)
            json_data = {
                city: {
                    age_of_apartment: df.loc[(city, age_of_apartment)].to_dict()
                    for age_of_apartment in df.index.get_level_values('age_of_apartment').unique()
                }
                for city in df.index.get_level_values('city').unique()
            }
            return jsonify(json_data), 200
        except Exception as e:
            error_traceback = traceback.format_exc()
            error_message = {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'error_traceback': error_traceback
            }
            return jsonify(error_message), 404


@blp.route("/general/age_comparison/csv")
class AgeComparisonCsv(MethodView):
    def get(self):
        try:
            df = pd.read_sql(sql_age_comparison, db.engine)
            df.set_index(["city", "age_of_apartment"], inplace=True)
            csv_data = df.to_csv(index_label='index')
            response = Response(csv_data, content_type='text/csv')
            response.headers['Content-Disposition'] = f'attachment; filename=age_comparison.csv'

            return response, 200
        except Exception as e:
            error_traceback = traceback.format_exc()
            error_message = {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'error_traceback': error_traceback
            }
            return jsonify(error_message), 404

