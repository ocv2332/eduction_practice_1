CREATE DATABASE journal;

\c journal

CREATE TABLE IF NOT EXISTS groups (
    group_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title text NOT NULL UNIQUE
);

CREATE TYPE roles AS ENUM ('admin', 'teacher', 'student');

CREATE TABLE IF NOT EXISTS users (
    user_id     integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    group_id    integer REFERENCES groups ON DELETE RESTRICT    ,
    first_name  text    NOT NULL                                ,
    last_name   text    NOT NULL                                ,
    middle_name text                                            ,
    birthday    date    NOT NULL                                ,
    email       text    NOT NULL UNIQUE                         ,
    login       text    NOT NULL UNIQUE                         ,
    password    text    NOT NULL                                ,
    role        roles   NOT NULL
);

CREATE OR REPLACE FUNCTION is_positive_role(integer, text) RETURNS boolean AS $$
    SELECT EXISTS (
        SELECT 1
        FROM   users
        WHERE  user_id    = $1
           AND role::text = $2
);
$$ LANGUAGE sql;

CREATE TABLE IF NOT EXISTS subjects (
    subject_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY     ,
    teacher_id integer REFERENCES users (user_id) ON DELETE RESTRICT,
    group_id   integer REFERENCES groups ON DELETE RESTRICT         ,
    title      text    NOT NULL                                     ,
    CONSTRAINT check_is_teacher check (is_positive_role(teacher_id, 'teacher'))
);

CREATE TABLE IF NOT EXISTS subject_items (
    item_id    integer  GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    subject_id integer  REFERENCES subjects ON DELETE CASCADE   ,
    title      text     NOT NULL                                ,
    date_event date     NOT NULL                                ,
    comment    text                                             ,
    max_mark   smallint NOT NULL
);

CREATE OR REPLACE FUNCTION is_positive_mark(integer, smallint) RETURNS boolean AS $$
    SELECT EXISTS (
        SELECT 1
        FROM   subject_items
        WHERE  item_id   = $1
           AND max_mark >= $2
);
$$ LANGUAGE sql;

CREATE TABLE IF NOT EXISTS marks (
    mark_id    integer  GENERATED ALWAYS AS IDENTITY PRIMARY KEY               ,
    student_id integer  REFERENCES users (user_id) ON DELETE CASCADE           ,
    item_id    integer  REFERENCES subject_items ON DELETE CASCADE              ,
    mark       smallint NOT NULL                                               ,

    CONSTRAINT check_is_student check (is_positive_role(student_id, 'student')),
    CONSTRAINT check_mark check (is_positive_mark(item_id, mark))
);

INSERT INTO groups (title) VALUES
    ('П2-19'),
    ('ИС1-22'),
    ('П3-19');

INSERT INTO users (group_id, first_name, last_name, middle_name, birthday, email, login, password, role) VALUES
    (1, 'Дмитрий', 'Собовый', 'Викторович', '03-29-2003', 'uplmtq@gmail.com', 'sobovyydv', '123', 'student'),
    (1, 'Денис', 'Башков', 'Андреевич', '09-23-2003', 'denis170.170@yandex.ru', 'bashkovda', '312', 'student'),
    (1, 'Данил', 'Журавлев', NULL, '01-22-2004', 'test@mail.ru', 'juravlevd', '1', 'student'),

    (2, 'Марат', 'Абдулаев', 'Темирханович', '01-14-2007', 'abdulaev@mail.ru', 'abdulaevmt', 'abdulaev_password', 'student'),
    (2, 'Илья', 'Аистов', 'Александрович', '07-21-2006', 'aistov@mail.ru', 'aistovia', 'aistov_password', 'student'),
    (2, 'Артем', 'Пролосов', 'Григорьевич', '08-15-2006', 'prolosov@mail.ru', 'prolosovag', 'prolosov_password', 'student'),

    (3, 'Андрей', 'Сухомлинов', 'Константинович', '10-27-2003', 'andreysuh@mail.ru', 'suhomlinovak', 'password_123', 'student'),
    (3, 'Олег', 'Легайло', 'Борисович', '07-27-2003', 'legaylooleg@gmail.com', 'legayloob', '123_password_123', 'student'),
    (3, 'Даниил', 'Белов', 'Владиславович', '11-15-2002', 'belovd@mail.ru', 'belovdv', 'belov_password', 'student'),

    (NULL, 'Вячеслав', 'Попов', 'Николаевич', '08-17-1981', 'popov@unitech-mo.ru', 'popovvn', 'popov_password', 'teacher'),
    (NULL, 'Светлана', 'Юренская', 'Алексеевна', '07-08-1982', 'urenskaya@unitech-mo.ru', 'urenskayadv', 'urenskaya_password', 'teacher'),
    (NULL, 'Дарья', 'Никонова', 'Николаевна', '06-15-1987', 'nikonova@unitech-mo.ru', 'nikonovadn', 'nikonova_123', 'teacher'),

    (NULL, 'Юрий', 'Грешнев', 'Павлович', '07-04-1966', 'yuriy.greshnev@yandex.ru', 'admin', 'admin', 'admin');

INSERT INTO subjects (teacher_id, group_id, title) VALUES
    (10, 1, 'Английский язык'),
    (11, 1, 'Теория алгоритмов'),
    (12, 1, 'Выполнение работ по профессии'),

    (12, 2, 'Английский язык'),
    (12, 2, 'Теория алгоритмов'),
    (12, 2, 'Выполнение работ по профессии'),

    (12, 3, 'Английский язык'),
    (12, 3, 'Теория алгоритмов'),
    (12, 3, 'Выполнение работ по профессии');

INSERT INTO subject_items (subject_id, title, date_event, comment, max_mark) VALUES
    (1, 'Герундий', '11-20-2022', NULL, 5),
    (5, 'Сортировка пузырьком', '11-20-2022', NULL, 5),
    (9, 'GIMP', '11-20-2022', NULL, 5);

INSERT INTO marks (student_id, item_id, mark) VALUES
    (1, 1, 5),
    (4, 2, 2),
    (6, 2, 5),
    (7, 3, 3),
    (8, 3, 4);