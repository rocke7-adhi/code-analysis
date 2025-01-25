from flask import Flask, render_template, request, jsonify
from models import AVAILABLE_MODELS, PROGRAMMING_LANGUAGES
from converter import CodeConverter
from explanation import CodeExplanation
from analyse import CodeAnalysis
#from optimize import CodeOptimization
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy

asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

app = Flask(__name__, static_folder='static')

converter = CodeConverter()
explanation = CodeExplanation()
analysis = CodeAnalysis()
#optimize = CodeOptimization()

@app.route('/')
def index():
    # Changed to return getstarted page as default
    return render_template('getstarted.html')

@app.route('/converter')
def converter_page():
    # New route for the converter page
    return render_template('index-convert.html', languages=PROGRAMMING_LANGUAGES, models=AVAILABLE_MODELS)

@app.route('/analysis')
def analyze_page():
    # New route for the analysis page
    return render_template('index-analyse.html', languages=PROGRAMMING_LANGUAGES, models=AVAILABLE_MODELS)

@app.route('/explain')
def explain_page():
    return render_template('index-explain.html', languages=PROGRAMMING_LANGUAGES, models=AVAILABLE_MODELS)

@app.route('/optimize')
def optimize_page():
    return render_template('index-optimize.html', languages=PROGRAMMING_LANGUAGES, models=AVAILABLE_MODELS)

# Code Converter
@app.route('/convert', methods=['POST'])
def convert():
    input_code = request.form['input_code']
    input_language = request.form['input_language']
    target_language = request.form['target_language']
    selected_model = request.form['selected_model']
    converted_code = converter.convert_code(input_code, input_language, target_language, selected_model)
    return jsonify({'converted_code': converted_code})

# Code Explanation
# Code Explanation
@app.route('/explain', methods=['POST'])
def explain():
    input_code = request.form['input_code']
    input_language = request.form['input_language']
    selected_model = request.form['selected_model']
    explanation_text = explanation.explain_code(input_code, input_language, selected_model)
    return jsonify({
        'explanation': explanation_text
    })

# Code Analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    input_code = request.form['input_code']
    input_language = request.form['input_language']
    selected_model = request.form['selected_model']
    analyse_result = analysis.analyze_code(input_code, input_language, selected_model)

    return jsonify({'analyse_result': analyse_result})

# Code Optimization
@app.route('/optimize', methods=['POST'])
def optimize():
    input_code = request.form['input_code']
    input_language = request.form['input_language']
    selected_model = request.form['selected_model']
    optimize_result = optimize.optimize_code(input_code, input_language, selected_model)
    return jsonify({'optimize_result': optimize_result})


if __name__ == '__main__':
    app.run(debug=True)
