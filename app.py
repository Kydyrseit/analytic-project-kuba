from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PLOTS_FOLDER'] = 'static/plots'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PLOTS_FOLDER'], exist_ok=True)

uploaded_data = None  # Глобальная переменная для хранения данных


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analytics')
def analytics():
    global uploaded_data
    if uploaded_data is None:
        return render_template('analytics.html', plot_url=None)

    # Построим график на основе данных
    plot_path = os.path.join(app.config['PLOTS_FOLDER'], 'data_plot.png')
    plt.figure(figsize=(8, 5))
    uploaded_data.plot(kind='bar', x=uploaded_data.columns[0], y=uploaded_data.columns[1:])
    plt.title('Пример графика')
    plt.savefig(plot_path)
    plt.close()

    return render_template('analytics.html', plot_url=plot_path)


@app.route('/export')
def export():
    # Заглушка для экспорта
    return render_template('export.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    global uploaded_data
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Загрузим данные в pandas
        try:
            uploaded_data = pd.read_csv(filepath)
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            uploaded_data = None
        return redirect(url_for('analytics'))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
