import re
import math
import pandas as pd
from collections import Counter
from django.shortcuts import render
from .forms import UploadFileForm

def tokenize_document(doc):
    # Разделяет документ на слова и приводит к нижнему регистру.
    return re.findall(r'\b\w+\b', doc.lower())

def calculate_tf_idf(documents):
    if not documents:
        return pd.DataFrame(columns=['word', 'tf', 'idf'])

    # Подсчёт TF для каждого документа
    tf_per_doc = []
    all_words = set()
    for doc in documents:
        tokens = tokenize_document(doc)
        tf = Counter(tokens)
        tf_per_doc.append(tf)
        all_words.update(tf.keys())

    # Подсчёт глобального TF
    global_tf = Counter()
    for tf in tf_per_doc:
        global_tf.update(tf)

    # Подсчёт IDF
    D = len(documents)
    idf = {}
    for word in all_words:
        doc_count = sum(1 for tf in tf_per_doc if word in tf)
        idf[word] = math.log10(D / doc_count) if doc_count else 0

    # Итоговая таблица
    rows = []
    for word, tf in global_tf.items():
        word_idf = idf[word]
        rows.append({
            'word': word,
            'tf': tf,
            'idf': round(word_idf, 5),
            # 'tf_idf': round(tf * word_idf, 5)
        })

    df = pd.DataFrame(rows).head(50)
    df = df.sort_values(by='idf', kind='quicksort', ascending=False).head(50)
    return df

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                text = file.read().decode('utf-8')
            except UnicodeDecodeError:
                text = file.read().decode('cp1251')

            #ВАЖНО!!! Разбиение текста на документы (разбивает текстовый файл на документы по пустым строкам между текстами, предоставлю тестовый образец)
            documents = [doc.strip() for doc in re.split(r'\n\s*\n', text) if doc.strip()]
            df = calculate_tf_idf(documents)
            return render(request, 'result.html', {'table': df.to_html(classes='table')})

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
