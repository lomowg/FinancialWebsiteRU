from common.convert_func import convert
from common.cur_codes import CODES
from common.get_interest_rates import get_interest_rate
from common.Moscow_exchange import get_imoex_index
from common.get_news import get_articles
import plotly.express as px
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)


@app.route('/')
def index():
    news_list = get_articles()
    return render_template('index.html', news_list=news_list)


@app.route('/converter', methods=['GET', 'POST'])
def converter():
    return render_template('converter.html', convert=convert, codes=CODES)


@app.route('/convert_to_second_form', methods=['POST'])
def convert_to_second_form():
    input_currency = request.json['inputCurrency'].upper()
    output_currency = request.json['outputCurrency'].upper()
    input_value = request.json['inputValue']
    result = convert(input_currency, output_currency, input_value)

    return jsonify(result=result)


@app.route('/convert_to_first_form', methods=['POST'])
def convert_to_first_form():
    input_currency = request.json['inputCurrency'].upper()
    output_currency = request.json['outputCurrency'].upper()
    input_value = request.json['inputValue']
    result = convert(input_currency, output_currency, input_value, reverse=True)

    return jsonify(result=result)

@app.route('/interest_rate')
def interest_rate():

    data = pd.DataFrame(get_interest_rate('01.12.2013', datetime.now()), columns=['Дата', '%'])

    fig = px.line(data, x='Дата', y='%', title='Ключевая ставка')
    fig.update_layout(xaxis_title='Дата', yaxis_title='Ставка (% годовых)', height=600, plot_bgcolor='#DCDCDC', paper_bgcolor='#f4f4f4')
    fig.update_traces(line=dict(color='#B22222'))

    graph_html = fig.to_html(full_html=False)

    return render_template('interest_rate.html', graph_html=graph_html, data=data)


@app.route('/imoex_index')
def imoex_index():

    data = get_imoex_index(start_day='2013-03-05', end_day=datetime.now())

    fig = px.line(data, x='Дата', y='Значение', title='Индекс МосБиржи')
    fig.update_layout(xaxis_title='Дата', yaxis_title='Значение',height=600, plot_bgcolor='#DCDCDC', paper_bgcolor='#f4f4f4')
    fig.update_traces(line=dict(color='#B22222'))

    graph_html = fig.to_html(full_html=False)

    return render_template('imoex_index.html', graph_html=graph_html, data=data)


@app.route('/download_interest_rate')
def download_interest_rate():
    df = pd.DataFrame(get_interest_rate('01.12.2013', datetime.now()), columns=['Дата', '%'])

    csv_filename = 'interest_rate.csv'
    df.to_csv(csv_filename, index=False, sep=',', encoding='windows-1251')
    return send_file(csv_filename, as_attachment=True)


@app.route('/download_imoex_index')
def download_imoex_index():
    df = get_imoex_index(start_day='2013-03-05', end_day=datetime.now())

    csv_filename = 'imoex_index.csv'
    df.to_csv(csv_filename, index=False, sep=',', encoding='windows-1251')
    return send_file(csv_filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')