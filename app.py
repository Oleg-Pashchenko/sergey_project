import pymorphy2
from flask import Flask, render_template, request, redirect, session, send_file

from logic import clear_requests, prepare_excel
from logic.words_priority import get_repeated_words, cluster_words

app = Flask(__name__)
app.secret_key = 'mysecretkey'


@app.route('/', methods=['GET'])
def step1():
    session.clear()
    return render_template('step1.html')


@app.route('/', methods=['POST'])
def step1_post():
    mask_name = request.form['mask-input']
    session['mask_name'] = mask_name
    return redirect('/step2-1')


@app.route('/step2-1', methods=['GET'])
def step2_1_get():
    mask_name = session.get('mask_name', '')
    return render_template('step2-1.html', mask_name=mask_name)


@app.route('/step2-2', methods=['GET'])
def step2_2_get():
    mask_name = session.get('mask_name', '')
    phrases_loaded = session.get('phrases_loaded', 0)
    phrases = session.get('phrases', '')
    return render_template('step2-2.html', mask_name=mask_name, phrases_loaded=phrases_loaded, phrases=phrases)


@app.route('/step2-1', methods=['POST'])
def step2_1_post():
    if 'reset-btn' in request.form.keys():
        return redirect('/')
    else:
        query = request.form['query'].replace('\r', '').strip().split('\n')
        session['phrases_loaded'] = len(query)
        session['phrases'] = query
        return redirect('/step2-2')


@app.route('/step2-2', methods=['POST'])
def step2_2_post():
    if 'reset-btn' in request.form:
        return redirect('/step2-1')
    return redirect('/step3-1')


@app.route('/step3-1', methods=['GET'])
def step3_1_get():
    mask_name = session.get('mask_name', '')
    phrases_loaded = session.get('phrases_loaded', 0)
    phrases = session.get('phrases', '')
    return render_template('step3-1.html', mask_name=mask_name, phrases_loaded=phrases_loaded, phrases=phrases)


@app.route('/step3-2', methods=['GET'])
def step3_2_get():
    mask_name = session.get('mask_name', '')
    phrases_loaded = session.get('phrases_loaded', 0)
    phrases = session.get('phrases', '')
    keywords_loaded = session.get('keywords_loaded', 0)
    keywords = session.get('keywords', '')
    return render_template('step3-2.html', mask_name=mask_name, phrases_loaded=phrases_loaded, phrases=phrases,
                           keywords_loaded=keywords_loaded, keywords=keywords)


@app.route('/step3-1', methods=['POST'])
def step3_1_post():
    if 'reset-btn' in request.form.keys():
        return redirect('/step2-2')
    else:
        query = request.form['query'].replace('\r', '').strip().split('\n')

        morph = pymorphy2.MorphAnalyzer()

        for q in range(len(query)):
            query[q] = morph.parse(query[q])[0].normal_form
        session['keywords_loaded'] = len(query)
        session['keywords'] = query
        return redirect('/step3-2')


@app.route('/step3-2', methods=['POST'])
def step3_2_post():
    if 'reset-btn' in request.form:
        return redirect('/step3-1')
    return redirect('/step4-1')


@app.route('/step4-1', methods=['GET'])
def step4_1_get():
    mask_name = session.get('mask_name', '')
    phrases_loaded = session.get('phrases_loaded', 0)
    phrases = session.get('phrases', '')
    keywords_loaded = session.get('keywords_loaded', 0)
    keywords = session.get('keywords', '')
    to_delete = clear_requests.start(keywords, phrases)
    return render_template('step4-1.html', mask_name=mask_name, phrases_loaded=phrases_loaded, phrases=phrases,
                           keywords_loaded=keywords_loaded, keywords=keywords, to_delete=to_delete)


@app.route('/step4-1', methods=['POST'])
def step4_1_post():
    phrases = session.get('phrases', '')
    keywords = session.get('keywords', '')
    if 'reset-btn' in request.form:
        return redirect('/step3-2')
    elif 'action-btn' in request.form:
        to_delete = clear_requests.start(keywords, phrases)
        updated_phrases = clear_requests.get_updated_list(phrases, to_delete)
        session['to_delete'] = to_delete
        session['to_delete_count'] = len(to_delete)
        session['after_delete_count'] = len(updated_phrases)
        session['after_delete'] = updated_phrases
    else:
        session['to_delete'] = []
        session['to_delete_count'] = 0
        session['after_delete_count'] = len(phrases)
        session['after_delete'] = phrases
    return redirect('/step4-2')


@app.route('/step4-2', methods=['GET'])
def step4_2_get():
    mask_name = session.get('mask_name', '')
    to_delete = session.get('to_delete', [])
    updated_phrases = session.get('after_delete')
    to_delete_count = session.get('to_delete_count', 0)
    after_delete_count = session.get('after_delete_count', 0)
    return render_template('step4-2.html', mask_name=mask_name, to_delete=to_delete, updated_phrases=updated_phrases,
                           to_delete_count=to_delete_count, after_delete_count=after_delete_count)


@app.route('/step4-2', methods=['POST'])
def step4_2_post():
    if 'reset-btn' in request.form:
        return redirect('/step4-1')
    return redirect('/step5-1')


@app.route('/step5-1', methods=['GET'])
def step5_1_get():
    phrases = session.get('after_delete', [])
    mask_name = session.get('mask_name', '')
    categories = get_repeated_words(phrases, mask_name)
    return render_template('step5-1.html', categories=categories, phrases=phrases, after_delete=len(phrases))


@app.route('/step5-1', methods=['POST'])
def step5_1_post():
    categories = list(request.form.keys())
    if 'reset-btn' in request.form:
        return redirect('/step4-2')
    categories.remove('next-btn')
    phrases = session.get('after_delete', [])
    clustered_words = cluster_words(phrases, categories)
    session['clustered_words'] = clustered_words
    return redirect('/step6')


@app.route('/step5-2', methods=['GET'])
def step5_2_get():
    clustered_words = session.get('clustered_words', {})
    mask_name = session.get('mask_name', '')
    return render_template('step5-2.html', clustered_words=clustered_words, mask_name=mask_name)


@app.route('/step5-2', methods=['POST'])
def step5_2_post():
    if 'reset-btn' in request.form:
        return redirect('/step5-1')
    return redirect('step6')


@app.route('/step6', methods=['GET'])
def step6_get():
    return render_template('step-6.html')


@app.route('/step6', methods=['POST'])
def step6_post():
    if 'reset-btn' in request.form:
        return redirect('/step5-1')
    clustered_words = session.get('clustered_words', {})
    mask = session.get('mask', '')
    prepare_excel.start(clustered_words, mask)
    return send_file('result.xlsx', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
