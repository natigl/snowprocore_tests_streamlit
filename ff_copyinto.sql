CREATE OR REPLACE FILE FORMAT quiz_certi.public.questions_csv_format
    COMPRESSION = 'GZIP'
    TYPE = 'CSV'
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
    FIELD_DELIMITER = ','
    RECORD_DELIMITER = '\n'
    EMPTY_FIELD_AS_NULL = TRUE
    NULL_IF = ('');

    --------------
    COPY INTO QUESTIONS
    FROM @quiz/preguntas.csv.gz
    FILE_FORMAT = questions_csv_format
    ON_ERROR = 'CONTINUE';