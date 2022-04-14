import io
import re
import json
import pickle
import joblib
import string
import unicodedata
import pandas as pd
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer


def get_credentials(sa_project_id, sa_bucket, sa_path):
    """ Função que pega jsons de credenciais salvos no storage """
    client = storage.Client(project=sa_project_id)

    bucket = client.get_bucket(sa_bucket)

    blob = bucket.blob(sa_path)

    info = json.loads(blob.download_as_string())

    return service_account.Credentials.from_service_account_info(info)


def cpf_cnpj(num):
    cnpj = CNPJ()
    result = cnpj.validate(num)
    if result == True:
        retorno = [num, 'CNPJ']
    else:
        cpf = CPF()
        result = cpf.validate(num)
        if result == True:
            retorno = [num, 'CPF']
        else:
            retorno = [num, 'False']
    return retorno


def lista_simples(lista):
    if isinstance(lista, list):
        return [sub_elem for elem in lista for sub_elem in lista_simples(elem)]
    else:
        return [lista]


def export_gcs(export_object, output_path, bucket, index=False):
    """
    Export export_object to output_path with a connected bucket.
    Usage:
    export_object: object file that will be exported
    output_path: output path inside bucket
    bucket: connected bucket via get_bucket
    """
    try:
        export_object = json.dumps(export_object)
    except BaseException:
        pass

    if isinstance(export_object, (pd.DataFrame, pd.Series, str)):
        f = io.StringIO()

        if isinstance(export_object, (pd.DataFrame, pd.Series)):
            export_object.to_csv(f, index=False, header=True, sep='|', encoding='latin-1')

        elif isinstance(export_object, str):
            f.write(export_object)
    else:
        f = io.BytesIO()
        pickle.dump(export_object, f)

    f.seek(0)

    blob = bucket.blob(output_path)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024
    blob._chunk_size = 1024 * 1024 * 16  # = 8 MB
    blob.upload_from_file(f.getvalue(), content_type='text/csv')


def loads_model(client_gcs,bucket,model_name):
    bucket = client_gcs.get_bucket(bucket)
    blob = bucket.blob(model_name)
    with TemporaryFile() as temp_file:
        blob.download_to_file(temp_file)
        temp_file.seek(0)
        model = joblib.load(temp_file)
    return model


def remover_acentos(palavra):
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavra_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    return re.sub('[^a-zA-Z0-9-./ ]', '', palavra_sem_acento)


def remove_stop(sentence):
    additional_stop_words = [
        'en',
        'pt',
        'traducao',
        '...',
        'ingles',
        'portuges',
        'eg',
        'etc']
    stopword_p = nltk.corpus.stopwords.words('portuguese')
    stopwords_e = nltk.corpus.stopwords.words('english')
    stopwords = stopword_p + additional_stop_words + stopwords_e
    phrase = []
    for word in sentence:
        if word not in stopwords:
            phrase.append(word)
    return phrase


def limpa_arquivo(x):
    x = str(x).lower()
    x = x.replace('\n', ' ')
    x = x.translate(str.maketrans(' ', ' ', string.punctuation))
    x = remover_acentos(x)
    x = nltk.word_tokenize(x)
    x = remove_stop(x)
    x = TreebankWordDetokenizer().detokenize(x)
    return x
