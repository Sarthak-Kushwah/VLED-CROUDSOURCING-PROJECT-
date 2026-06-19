USE faqfusion_db;

-- ADMINS

INSERT INTO admins
(id, username, email, password_hash, role, is_active)
VALUES
(1,'superadmin','superadmin@faqfusion.com','$2y$10$hash_superadmin','super_admin',TRUE),
(2,'ayush_admin','ayush@faqfusion.com','$2y$10$hash_admin1','admin',TRUE),
(3,'priya_admin','priya@faqfusion.com','$2y$10$hash_admin2','admin',TRUE),
(4,'rahul_moderator','rahul@faqfusion.com','$2y$10$hash_mod1','moderator',TRUE),
(5,'neha_moderator','neha@faqfusion.com','$2y$10$hash_mod2','moderator',TRUE);

-- USERS

INSERT INTO users
(id, username, email, password_hash, is_active)
VALUES
(1,'amit_sharma','amit@gmail.com','u1',TRUE),
(2,'priya_singh','priya@gmail.com','u2',TRUE),
(3,'rohan_gupta','rohan@gmail.com','u3',TRUE),
(4,'simran_kaur','simran@gmail.com','u4',TRUE),
(5,'arjun_verma','arjun@gmail.com','u5',TRUE),
(6,'meera_joshi','meera@gmail.com','u6',TRUE),
(7,'nisha_sharma','nisha@gmail.com','u7',TRUE),
(8,'vishal_kumar','vishal@gmail.com','u8',TRUE),
(9,'ananya_singh','ananya@gmail.com','u9',TRUE),
(10,'sachin_mehta','sachin@gmail.com','u10',TRUE),
(11,'rahul_sharma','rahul@gmail.com','u11',TRUE),
(12,'riya_gupta','riya@gmail.com','u12',TRUE),
(13,'karan_verma','karan@gmail.com','u13',TRUE),
(14,'neha_kapoor','neha@gmail.com','u14',TRUE),
(15,'tanvi_jain','tanvi@gmail.com','u15',TRUE),
(16,'aditya_singh','aditya@gmail.com','u16',TRUE),
(17,'shivani_sharma','shivani@gmail.com','u17',TRUE),
(18,'aman_kumar','aman@gmail.com','u18',TRUE),
(19,'muskan_gupta','muskan@gmail.com','u19',TRUE),
(20,'harsh_verma','harsh@gmail.com','u20',TRUE),
(21,'deepika_singh','deepika@gmail.com','u21',TRUE),
(22,'yash_gupta','yash@gmail.com','u22',TRUE),
(23,'pooja_sharma','pooja@gmail.com','u23',TRUE),
(24,'ankit_kumar','ankit@gmail.com','u24',TRUE),
(25,'kritika_jain','kritika@gmail.com','u25',TRUE);

-- FAQ CATEGORIES

INSERT INTO faq_categories
(name, description)
VALUES
('Internship Program','General information about the internship'),
('Course Details','Teaching methodology and curriculum'),
('Projects','Hands-on and open-source projects'),
('Certification','Certificate and completion details'),
('General','General chatbot and platform information');

-- FAQS

INSERT INTO faqs
(question, answer, category_id, created_by, view_count)
VALUES
('What is this internship about?','This is a free online internship where students build an intelligent FAQ chatbot that answers user queries using AI and a crowd-sourced FAQ database.',1,1,450),
('Is this internship free?','Yes, the internship is completely free of cost.',1,1,380),
('What is the duration of the internship?','The internship requires a minimum commitment of 2 months.',1,1,320),
('Who can apply for this internship?','Students from any college or branch with basic programming knowledge can apply.',1,2,280),
('Who will teach us during the internship?','IIT-level professors and industry experts conduct live classes through Zoom.',2,1,510),
('Are the classes live or recorded?','The sessions are conducted live on Zoom, and recordings of selected topics will also be provided.',2,1,260),
('How many hours should I dedicate every week?','Students are encouraged to dedicate around 6–10 hours per week.',2,2,190),
('Will I get hands-on experience?','Yes, students work on real-world open-source projects and gain practical experience.',3,1,470),
('What kind of projects will I work on?','Students will build an intelligent FAQ chatbot that answers user questions and improves continuously.',3,2,390),
('Can I contribute to open-source projects?','Yes, students get opportunities to contribute to open-source projects during the internship.',3,2,310),
('Will I work in a team?','Yes, students collaborate in teams of around 10 members to collect FAQs, validate data, and improve the chatbot.',3,1,260),
('Will I receive a certificate after completion?','Yes, participants receive a certificate after successfully completing the internship.',4,1,560),
('Is the certificate recognized?','The certificate is issued after successful completion and can be added to resumes and LinkedIn profiles.',4,1,290),
('What are the requirements to earn the certificate?','Students must complete the internship duration and actively participate in the project.',4,2,240),
('Can beginners join this internship?','Yes, beginners with basic programming knowledge are welcome.',1,2,290),
('Do I need prior AI experience?','No, prior AI experience is not mandatory. The internship starts from the basics.',1,1,300),
('What technologies are used in this project?','The project uses AI, vector databases, Large Language Models, and semantic search techniques.',2,1,280),
('How are FAQs collected?','Team members collect FAQs from websites, forums, documents, and user queries.',3,1,250),
('Can users ask new questions?','Yes, users can ask questions even if they are not present in the FAQ database.',5,1,210),
('What happens if the chatbot cannot find an answer?','The chatbot retrieves the closest matching information and generates a helpful response.',5,2,180),
('Will I learn teamwork skills?','Yes, students collaborate in teams and learn communication and project management skills.',3,1,170),
('Will there be mentorship during the internship?','Yes, mentors and IIT-level professors guide students throughout the internship.',2,1,350),
('Can I add this internship to my resume?','Yes, the internship provides practical experience and a certificate that can be added to resumes.',4,2,310),
('Is attendance mandatory?','Yes, attendance is mandatory. Students are advised and encouraged to attend all live sessions to get the maximum benefit.',2,1,150),
('Will there be assignments?','Yes, students will complete assignments and project milestones during the internship.',2,2,190),
('What skills will I gain?','You will gain skills in AI, chatbot development, teamwork, semantic search, and open-source contribution.',2,1,340),
('Can I ask doubts during the sessions?','Yes, students can interact with professors and mentors during Zoom sessions.',2,1,280);

-- FAQ ALIASES

INSERT INTO faq_aliases
(faq_id, alias_question)
VALUES
(1,'Tell me about the internship'),
(1,'What is this program?'),
(2,'Is internship free of cost?'),
(2,'Do I have to pay fees?'),
(3,'How long is the internship?'),
(3,'Minimum internship duration'),
(4,'Who can join this internship?'),
(5,'Who teaches the course?'),
(5,'Are IIT professors involved?'),
(6,'Are sessions live?'),
(6,'Will recordings be available?'),
(7,'Weekly time commitment'),
(8,'Will I get practical experience?'),
(9,'Project details'),
(9,'What projects are included?'),
(10,'Open source contributions'),
(11,'Will I work with a team?'),
(12,'Will I get a certificate?'),
(13,'Certificate validity'),
(14,'Requirements for certificate'),
(15,'Is it beginner friendly?'),
(15,'Can freshers join?'),
(16,'Need AI experience?'),
(17,'Technologies used'),
(18,'How are FAQs collected?'),
(19,'Can users ask new questions?'),
(20,'No answer found'),
(21,'Teamwork opportunities'),
(22,'Mentorship available'),
(23,'Resume value'),
(24,'Attendance policy'),
(25,'Assignments'),
(26,'Skills learned'),
(27,'Can I ask doubts?');

-- QUESTIONS

INSERT INTO questions
(user_id, question_text, answer_text, status, similarity_score, matched_faq_id, resolved_by_admin, resolved_at)
VALUES
(1,'What is this internship about?',
'This is a free online internship where students build an intelligent FAQ chatbot.',
'answered',0.96,1,1,NOW()),
(2,'Is the internship free?',
'Yes, the internship is completely free of cost.',
'answered',0.98,2,1,NOW()),
(3,'How long is the internship?',
'The internship requires a minimum commitment of 2 months.',
'answered',0.95,3,2,NOW()),
(4,'Who teaches during the internship?',
'Live sessions are conducted by IIT-level professors.',
'answered',0.94,5,1,NOW()),
(5,'Can beginners join?',
'Yes, beginners with basic programming knowledge are welcome.',
'answered',0.91,15,2,NOW()),
(6,'Will I get a certificate?',NULL,'pending',NULL,NULL,NULL,NULL),
(7,'What skills will I gain?',NULL,'pending',NULL,NULL,NULL,NULL),
(8,'Are assignments given?',NULL,'pending',NULL,NULL,NULL,NULL),
(9,'Can I contribute to open-source projects?',NULL,'pending',NULL,NULL,NULL,NULL),(10,'Will I work in a team?',NULL,'pending',NULL,NULL,NULL,NULL),
(11,'Is attendance mandatory?',NULL,'pending',NULL,NULL,NULL,NULL),
(12,'Can I ask doubts during sessions?',NULL,'pending',NULL,NULL,NULL,NULL);

-- QUESTION FEEDBACK

INSERT INTO question_feedback
(question_id, user_id, is_helpful)
VALUES
(1,1,TRUE),
(1,2,TRUE),
(2,3,TRUE),
(2,4,FALSE),
(3,5,TRUE),
(3,6,TRUE),
(4,7,TRUE),
(5,8,TRUE),
(1,9,FALSE),
(2,10,TRUE),
(3,11,TRUE),
(4,12,TRUE);

-- AUDIT LOGS

INSERT INTO audit_logs
(admin_id, action, entity_type, entity_id)
VALUES
(1,'CREATE','FAQ',1),
(1,'CREATE','FAQ',2),
(1,'CREATE','FAQ',3),
(2,'UPDATE','FAQ',5),
(2,'UPDATE','FAQ',10),
(3,'CREATE','FAQ_ALIAS',4),
(3,'CREATE','FAQ_ALIAS',7),
(1,'ANSWER','QUESTION',1),
(1,'ANSWER','QUESTION',2),
(2,'ANSWER','QUESTION',3),
(2,'ANSWER','QUESTION',4),
(3,'REVIEW','QUESTION',6),
(1,'LOGIN','ADMIN',1),
(2,'LOGIN','ADMIN',2),
(3,'LOGIN','ADMIN',3),
(1,'LOGOUT','ADMIN',1),
(2,'LOGOUT','ADMIN',2),
(1,'UPDATE','USER',5),
(2,'UPDATE','USER',8);