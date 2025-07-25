
CREATE TABLE course
(
  course_id       char(6)       NOT NULL,
  title           varchar(256)  NOT NULL,
  credit          numeric(2,1)  NOT NULL,
  need_credit     numeric(4,1)  NOT NULL DEFAULT 0,
  amount          numeric(10,4) NOT NULL,
  prerequisite_id char(6)       NOT NULL,
  extra_course_id char(6)       NOT NULL,
  dept_id         smallint      NOT NULL,
  PRIMARY KEY (course_id)
);

CREATE TABLE credit_part
(
  min       smallint NOT NULL UNIQUE,
  max       smallint NOT NULL UNIQUE,
  credit_id smallint NOT NULL,
  PRIMARY KEY (credit_id)
);

CREATE TABLE department
(
  dept_short_name varchar(6)   NOT NULL,
  long_name       varchar(256) NOT NULL,
  dept_id         smallint     NOT NULL,
  PRIMARY KEY (dept_id)
);

CREATE TABLE faculty
(
  faculty_short_id varchar(10)  NOT NULL UNIQUE,
  first_name       varchar(128) NOT NULL,
  last_name        varchar(128),
  fac_email        varchar(128) NOT NULL UNIQUE,
  room_no          varchar(7)   NOT NULL UNIQUE,
  dept_id          smallint     NOT NULL,
  PRIMARY KEY (faculty_short_id)
);

CREATE TABLE offers
(
  season_id        smallint    NOT NULL,
  year             smallint    NOT NULL,
  section_no       smallint    NOT NULL,
  course_id        char(6)     NOT NULL,
  faculty_short_id varchar(10) NOT NULL,
  PRIMARY KEY (season_id, year, section_no, course_id, faculty_short_id)
);

CREATE TABLE room
(
  room_no  varchar(7)   NOT NULL,
  building varchar(256) NOT NULL,
  PRIMARY KEY (room_no)
);

CREATE TABLE season
(
  season_id   smallint NOT NULL,
  season_name char(10),
  PRIMARY KEY (season_id)
);

CREATE TABLE section
(
  capacity   smallint  ,
  room_no    varchar(7) NOT NULL,
  day        varchar(5) NOT NULL,
  start_time time       NOT NULL,
  end_time   time       NOT NULL,
  season_id  smallint   NOT NULL,
  year       smallint   NOT NULL,
  section_no smallint   NOT NULL,
  course_id  char(6)    NOT NULL,
  PRIMARY KEY (season_id, year, section_no, course_id)
);

CREATE TABLE student
(
  student_id       char(13)     NOT NULL UNIQUE,
  first_name       varchar(128) NOT NULL,
  last_name        varchar(128),
  mobile_no        varchar(15)  NOT NULL UNIQUE,
  email            varchar(128) NOT NULL UNIQUE,
  is_dismissed     boolean      NOT NULL DEFAULT false,
  address          varchar(128) NOT NULL,
  gardian_name     varchar(128) NOT NULL,
  gardian_phone    varchar(128) NOT NULL,
  is_graduated     boolean      NOT NULL DEFAULT false,
  credit_completed numeric(4,1) NOT NULL DEFAULT 0,
  dept_id          smallint     NOT NULL,
  PRIMARY KEY (student_id)
);

CREATE TABLE student_image
(
  student_id char(13) NOT NULL,
  file_name  text    ,
  file_data  bytea   ,
  PRIMARY KEY (student_id)
);

CREATE TABLE student_login
(
  password        varchar(512),
  student_id      char(13)     NOT NULL,
  failed_attempts smallint     DEFAULT 0,
  lockout_until   timestamp   ,
  PRIMARY KEY (student_id)
);

CREATE TABLE student_otp
(
  otp        varchar(6),
  created_at TIMESTAMP ,
  expires_at timestamp ,
  try_count  smallint   DEFAULT 0,
  student_id char(13)   NOT NULL,
  PRIMARY KEY (student_id)
);

CREATE TABLE takes
(
  grade      numeric(4,2) DEFAULT 0,
  is_dropped boolean      DEFAULT false,
  season_id  smallint     NOT NULL,
  year       smallint     NOT NULL,
  section_no smallint     NOT NULL,
  course_id  char(6)      NOT NULL,
  student_id char(13)     NOT NULL,
  PRIMARY KEY (season_id, year, section_no, course_id, student_id)
);

CREATE TABLE timeslot
(
  day        varchar(5) NOT NULL,
  start_time time       NOT NULL,
  end_time   time       NOT NULL,
  PRIMARY KEY (day, start_time, end_time)
);

CREATE TABLE university
(
  is_advising   boolean ,
  credit_id     smallint,
  curr_season   smallint NOT NULL,
  curr_year     smallint NOT NULL,
  option        smallint NOT NULL,
  credit_id     smallint NOT NULL,
  min_cred_need smallint NOT NULL DEFAULT 9,
  max_cred_need smallint NOT NULL DEFAULT 15,
  PRIMARY KEY (option)
);

CREATE TABLE year
(
  year smallint NOT NULL,
  PRIMARY KEY (year)
);

ALTER TABLE course
  ADD CONSTRAINT FK_course_TO_course
    FOREIGN KEY (prerequisite_id)
    REFERENCES course (course_id);

ALTER TABLE course
  ADD CONSTRAINT FK_course_TO_course1
    FOREIGN KEY (extra_course_id)
    REFERENCES course (course_id);

ALTER TABLE course
  ADD CONSTRAINT FK_department_TO_course
    FOREIGN KEY (dept_id)
    REFERENCES department (dept_id);

ALTER TABLE faculty
  ADD CONSTRAINT FK_department_TO_faculty
    FOREIGN KEY (dept_id)
    REFERENCES department (dept_id);

ALTER TABLE offers
  ADD CONSTRAINT FK_section_TO_offers
    FOREIGN KEY (season_id, year, section_no, course_id)
    REFERENCES section (season_id, year, section_no, course_id);

ALTER TABLE offers
  ADD CONSTRAINT FK_faculty_TO_offers
    FOREIGN KEY (faculty_short_id)
    REFERENCES faculty (faculty_short_id);

ALTER TABLE section
  ADD CONSTRAINT FK_room_TO_section
    FOREIGN KEY (room_no)
    REFERENCES room (room_no);

ALTER TABLE section
  ADD CONSTRAINT FK_timeslot_TO_section
    FOREIGN KEY (day, start_time, end_time)
    REFERENCES timeslot (day, start_time, end_time);

ALTER TABLE section
  ADD CONSTRAINT FK_season_TO_section
    FOREIGN KEY (season_id)
    REFERENCES season (season_id);

ALTER TABLE section
  ADD CONSTRAINT FK_year_TO_section
    FOREIGN KEY (year)
    REFERENCES year (year);

ALTER TABLE section
  ADD CONSTRAINT FK_course_TO_section
    FOREIGN KEY (course_id)
    REFERENCES course (course_id);

ALTER TABLE student
  ADD CONSTRAINT FK_department_TO_student
    FOREIGN KEY (dept_id)
    REFERENCES department (dept_id);

ALTER TABLE student_image
  ADD CONSTRAINT FK_student_TO_student_image
    FOREIGN KEY (student_id)
    REFERENCES student (student_id);

ALTER TABLE student_login
  ADD CONSTRAINT FK_student_TO_student_login
    FOREIGN KEY (student_id)
    REFERENCES student (student_id);

ALTER TABLE student_otp
  ADD CONSTRAINT FK_student_TO_student_otp
    FOREIGN KEY (student_id)
    REFERENCES student (student_id);

ALTER TABLE takes
  ADD CONSTRAINT FK_section_TO_takes
    FOREIGN KEY (season_id, year, section_no, course_id)
    REFERENCES section (season_id, year, section_no, course_id);

ALTER TABLE takes
  ADD CONSTRAINT FK_student_TO_takes
    FOREIGN KEY (student_id)
    REFERENCES student (student_id);

ALTER TABLE university
  ADD CONSTRAINT FK_season_TO_university
    FOREIGN KEY (curr_season)
    REFERENCES season (season_id);

ALTER TABLE university
  ADD CONSTRAINT FK_year_TO_university
    FOREIGN KEY (curr_year)
    REFERENCES year (year);

ALTER TABLE university
  ADD CONSTRAINT FK_credit_part_TO_university
    FOREIGN KEY (credit_id)
    REFERENCES credit_part (credit_id);
