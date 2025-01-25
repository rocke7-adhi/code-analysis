from flask import Flask, render_template, request, jsonify
from models import AVAILABLE_MODELS, PROGRAMMING_LANGUAGES
from analyse import CodeAnalysis
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy

asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

app = Flask(__name__, static_folder='static')

analysis = CodeAnalysis()
#optimize = CodeOptimization()

@app.route('/')
def index():
    # Changed to return analysis page as default
    return render_template('getstarted.html')

@app.route('/analysis')
def analyze_page():
    return render_template('index-analyse.html', languages=PROGRAMMING_LANGUAGES, models=AVAILABLE_MODELS)

# Code Analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    input_code = request.form['input_code']
    input_language = request.form['input_language']
    selected_model = request.form['selected_model']
    analyse_result = analysis.analyze_code(input_code, input_language, selected_model)
    return jsonify({'analyse_result': analyse_result})


if __name__ == '__main__':
    app.run(debug=True)
