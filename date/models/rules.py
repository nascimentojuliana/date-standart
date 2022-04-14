import os
import re
import nltk
nltk.download('all')
import unicodedata
import pandas as pd
from statistics import mode
from datetime import datetime
from date.utils import utils
from translate import Translator
from nltk.tokenize.treebank import TreebankWordDetokenizer


class Rules:

    def __init__(self):
        pass

    def limpa_arquivo(self, x):
        x = str(x).lower()
        x = x.replace('\n', "")
        x = unicodedata.normalize('NFKD', x)
        x = u"".join([c for c in x if not unicodedata.combining(c)])
        x = re.sub('[^a-zA-Z0-9-./ ]', ' ', x)
        x = nltk.word_tokenize(x)
        x = TreebankWordDetokenizer().detokenize(x)
        return x

    def most_common(self, list):
        return(mode(list))

    def default_date(self, date):
        x = str(date).replace('.', '/').replace('-', '/')
        try:
            x = datetime.strptime(x, '%Y-%m-%d').date()
        except BaseException:
            regex = re.compile(r'^\d{1,2}\/\d{1,2}\/(\d{4}|\d{2})$')
            result = regex.search(x)
            if result:
                x = result.group()
                if x:
                    dia = int(x.split('/')[0])
                    if dia > 12:
                        x = pd.to_datetime(x)
                        x = datetime.strftime(x, '%Y-%m-%d')
                        x = str(x)
                    else:
                        mes = x.split('/')[1]
                        ano = x.split('/')[2]
                        if len(ano) <= 2:
                            ano = '20' + ano

                        x = ano + '-' + mes + '-' + str(dia)
                        x = pd.to_datetime(x)
                        x = datetime.strftime(x, '%Y-%m-%d')
                        x = str(x)
                else:
                    x = 'False'
            else:
                x = 'False'
        return x

    def long_date(self, date):
        
        try:
            translator= Translator(from_lang='pt', to_lang="en")
            y = 'hoje é dia ' + date 
            y = translator.translate('hoje é dia 20 de janeiro de 2020')
            y = y.replace('today is ', '')
            y = y.replace(",", "").replace(".", "")
            x = datetime.strptime(y, '%B %d %Y').strftime('%Y-%m-%d')
            x = str(x)
        except BaseException:
            x = 'False'
        return x

    def compound_extended_date(self, date):
        # buscar padrões como 02,03, 04 de janeiro de 2020 ou 02,03,04 de janeiro/20
        x = re.sub('[^a-zA-Z0-9]', ' ', date)
        try:
            
            dicionario = {
                'jan': '01',
                'fev': '02',
                'mar': '02',
                'abr': '04',
                'mai': '05',
                'jun': '06',
                'jul': '07',
                'ago': '08',
                'set': '09',
                'out': '10',
                'nov': '11',
                'dez': '12'}
            regex = re.compile(
                r'jan[a-z]*|fev[a-z]*|mar[a-z]*|abr[a-z]*|mai[a-z]\
                *|jun[a-z]*|jul[a-z]*|ago[a-z]*|set[a-z]*|out[a-z]\
                *|nov[a-z]*|dez[a-z]*')
            result = regex.search(x)
            if result:
                mes = result.group()
                mes = dicionario[mes[0:3]]
                regex = re.compile(r'20\ \d{2}$|2\.0\d{2}$|20\d{2}$')
                result = regex.search(x)
                if result:
                    ano = result.group()
                    ano = self.limpa_arquivo(ano).replace(" ", "")
                    x = x.split()
                    regex = re.compile(r'\d{2}|\d{1}')
                    vetor_datas = []
                    for y in x:
                        result = regex.search(y)
                        if result:
                            dia = result.group()
                            data = ano + '-' + mes + '-' + dia
                            vetor_datas.append(str(data))
                    x = vetor_datas
                else:
                    x = 'False'
            else:
                x = 'False'
        except BaseException:
            x = 'False'

        return x

    def compound_default_date(self, date):
        x = re.sub('[^a-zA-Z0-9-./ ]', ' ', date)
        try:
            regex = re.compile(r'\d{1,2}\/\d{1,2}\/(\d{4}|\d{2})')
            result = regex.search(x)
            if result:
                resultado = result.group()
                mes = resultado.split('/')[1]
                ano = resultado.split('/')[2]
                if len(str(ano)) == 2:
                    ano = '20' + ano

                x = x.split()
                # buscar padrões como 01/10, 02/10, 03/10/2020(20)
                regex = re.compile(r'\d{1,2}\/\d{1,2}')
                vetor_datas = []
                for y in x:
                    result = regex.search(y)
                    if result:
                        dia_mes = result.group()
                        dia = dia_mes.split('/')[0]
                        z = ano + '-' + mes + '-' + dia
                        data = pd.to_datetime(z)
                        data = datetime.strftime(data, '%Y-%m-%d')
                        vetor_datas.append(str(data))

                    else:
                        # buscar padrões como 01, 02, 03/10/2020 ou 01, 02, 03/10/20
                        regex = re.compile(r'\d{1,2}')
                        vetor_datas = []
                        for y in x:
                            result = regex.search(y)
                            if result:
                                dia = result.group()
                                z = ano + '-' + mes + '-' + dia
                                data = pd.to_datetime(z)
                                data = datetime.strftime(data, '%Y-%m-%d')
                                vetor_datas.append(str(data))

                x = vetor_datas

            else:
                regex = re.compile(r'20\ \d{2}$|20\d{2}$')
                result = regex.search(x)
                if result:
                    ano = result.group()
                    ano = self.limpa_arquivo(ano).replace(" ", "")

                    x = x.split()
                    # buscar padrões como 01/10, 02/10, 03/10/2020(20)
                    regex = re.compile(r'\d{1,2}\/\d{1,2}')
                    vetor_datas = []
                    for y in x:
                        result = regex.search(y)
                        if result:
                            dia_mes = result.group()
                            dia = dia_mes.split('/')[0]
                            mes = dia_mes.split('/')[1]
                            z = ano + '-' + mes + '-' + dia
                            data = pd.to_datetime(z)
                            data = datetime.strftime(data, '%Y-%m-%d')
                            vetor_datas.append(str(data))

                    x = vetor_datas

                else:
                    x = 'False'

        except BaseException:
            x = 'False'

        return x

    def datas_imcompletas(self, list_incomplete_dates, list_complete_dates):

        list_years = []
        list_months = []

        dicionario = {
            'jan': '01',
            'fev': '02',
            'mar': '02',
            'abr': '04',
            'mai': '05',
            'jun': '06',
            'jul': '07',
            'ago': '08',
            'set': '09',
            'out': '10',
            'nov': '11',
            'dez': '12'}

        regex_default_date = re.compile(r'(\d{4}|\d{2})\-\d{1,2}\-\d{1,2}')
        regex_year = re.compile(r'20\d{1,2}')
        regex_long_month = re.compile(
            r'jan[a-z]*|fev[a-z]*|mar[a-z]*|abr[a-z]*|mai[a-z]*|jun[a-z]*\
            |jul[a-z]*|ago[a-z]*|set[a-z]*|out[a-z]*|nov[a-z]*|dez[a-z]*')
        regex_month_year = re.compile(r'\d[1-12]\/(\d{4}|\d{2})')
        regex_day_month = re.compile(r'\d[1-31]\/\d[1-12]')

        for date in (list_complete_dates):

            result = regex_default_date.search(date)
            if result:
                result = result.group()
                mes = result.split('-')[1]
                ano = result.split('-')[0]
                list_months.append(mes)
                list_years.append(ano)

            result = regex_year.search(date)
            if result:
                ano = result.group()
                list_years.append(ano)

            result = regex_long_month.search(date)
            if result:
                mes = result.group()
                mes = dicionario[mes[0:3]]
                list_months.append(mes)

            result = regex_month_year.search(date)
            if result:
                result = result.group()
                mes = result.split('/')[0]
                ano = result.split('/')[1]
                list_months.append(mes)
                list_years.append(ano)

            result = regex_day_month.search(date)
            if result:
                result = result.group()
                mes = result.split('/')[1]
                list_months.append(mes)

        for date in (list_incomplete_dates):

            result = regex_default_date.search(date)
            if result:
                result = result.group()
                mes = result.split('-')[1]
                ano = result.split('-')[0]
                list_months.append(mes)
                list_years.append(ano)

            result = regex_year.search(date)
            if result:
                ano = result.group()
                list_years.append(ano)

            result = regex_long_month.search(date)
            if result:
                mes = result.group()
                mes = dicionario[mes[0:3]]
                list_months.append(mes)

            result = regex_month_year.search(date)
            if result:
                result = result.group()
                mes = result.split('/')[0]
                ano = result.split('/')[1]
                list_months.append(mes)
                list_years.append(ano)

            result = regex_day_month.search(date)
            if result:
                result = result.group()
                mes = result.split('/')[1]
                list_months.append(mes)

        try:
            year = [self.most_common(list_years)]
        except BaseException:
            year = list_years
        try:
            month = [self.most_common(list_months)]
        except BaseException:
            month = list_months

        ##########################################################################
        # começando a tratar as datas incompletas
        for i, dat in enumerate(list_incomplete_dates):
            list_dates = []
            for ano_x in year:
                for mes_x in month:
                    dat = dat.replace('-', '/').replace('.', '/').replace(',', ' ')
                    result = regex_long_month.search(dat)
                    tem_mes = ''
                    if result:
                        tem_mes = result.group()

                    result = regex_year.search(dat)
                    tem_ano = ''
                    if result:
                        tem_ano = result.group()

                    regex = re.compile(r'\d{1,2}\/\d{1,2}')
                    result = regex.search(dat)
                    tem_dia_mes = ''
                    if result:
                        tem_dia_mes = result.group()

                    pedaços_data = dat.split()
                    for pedaço_data in pedaços_data:
                        regex = re.compile(r'\d{1,2}')
                        result = regex.search(pedaço_data)
                        if result:
                            tem_dia = result.group()
                            if len(tem_dia_mes) > 0:
                                data = pedaço_data + '/' + ano_x
                                data_final = self.default_date(data)
                                list_dates.append(data_final)
                            elif len(tem_mes) > 0 & len(tem_ano) > 0:
                                mes_presente = dicionario[tem_mes[0:3]]
                                data = pedaço_data + '/' + mes_presente + '/' + tem_ano
                                data_final = self.default_date(data)
                                list_dates.append(data_final)
                            elif len(tem_mes) > 0:
                                mes_presente = dicionario[tem_mes[0:3]]
                                data = pedaço_data + '/' + mes_presente + '/' + ano_x
                                data_final = self.default_date(data)
                                list_dates.append(data_final)
                            elif len(tem_ano) > 0:
                                data = pedaço_data + '/' + mes_x + '/' + tem_ano
                                data_final = self.default_date(data)
                                list_dates.append(data_final)
                            elif len(tem_dia) > 0:
                                data = pedaço_data + '/' + mes_x + '/' + ano_x
                                data_final = self.default_date(data)
                                list_dates.append(data_final)
            list_incomplete_dates[i] = list_dates

        list_incomplete_dates = utils.lista_simples(list_incomplete_dates)
        list_complete_dates.append(list_incomplete_dates)
        final_dates = utils.lista_simples(list_complete_dates)

        return final_dates

    def process_dates(self, date):
        
        datas = []
            
        date = self.limpa_arquivo(date)
        date = date.replace('marÃ§o', 'marco').replace('março', 'marco')

        y = self.compound_extended_date(date)
        if y == 'False':
            y = self.compound_default_date(date)
            if y == 'False':
                y = self.default_date(date)
                if y == 'False':
                    y = self.long_date(date)
                    if y == 'False':
                        y = [date, y]

        datas.append(y)

        list_incomplete_dates = ([date[0] for date in datas if 'False' in date])

        if len(list_incomplete_dates) > 0:
            ys = set(list_incomplete_dates)
            list_complete_dates = ([utils.lista_simples(date)
                        for date in datas if len(date) > 0
                        and date[0] not in ys])
            list_complete_dates = utils.lista_simples(list_complete_dates)

            list_final_dates = self.datas_imcompletas(
                list_incomplete_dates, list_complete_dates)

            list_final_dates = utils.lista_simples(list_final_dates)

        else:
            list_final_dates = utils.lista_simples(datas)

        return set(list_final_dates)

    def process_entities(self, date):

        list_processed_dates = []

        list_processed_dates = self.process_dates(date)

        entities = {
            'datas': list_processed_dates}

        return entities
