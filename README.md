date standart
==============================

Pipelined that transforms a date in different formats into a standard date.


The model consists of a series of rules that put the dates in a standard format, for example: 

2, 3 de janeiro de 2020 the rules will return 2021-01-02, 2021-01-03.

01/10, 02/10 de 2020, the rules will return 2020-10-01, 2020-10-02.

01/10, 02/10, 03/10/2020, the rules will return 2020-10-01, 2020-10-03, 2020-10-02.

23/03/2021, the rules will return 2021-03-23.

04-01-1992, the rules will return 1992-01-04.

The rules were developed for dates in Portuguese, so it doesn't perform well if the input date is in English.

Please, running:
streamlit run main.py --server.port 8080
for local

Or access:
https://share.streamlit.io/nascimentojuliana/date-standart/main/main.py
