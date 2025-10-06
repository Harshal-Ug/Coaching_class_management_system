INSERT INTO teachers (first_name, last_name, email, password_hash) VALUES
('Anita', 'Sharma', 'anita.sharma@example.com', 'x'),
('Rohit', 'Verma', 'rohit.verma@example.com', 'x'),
('Neha', 'Iyer', 'neha.iyer@example.com', 'x'),
('Arjun', 'Mehta', 'arjun.mehta@example.com', 'x'),
('Priya', 'Nair', 'priya.nair@example.com', 'x');

INSERT INTO students (first_name, last_name, email, age, password_hash) VALUES
('Aarav', 'Patel', 'aarav.patel01@example.com', 16, 'x'),
('Diya', 'Singh', 'diya.singh02@example.com', 17, 'x'),
('Kabir', 'Gupta', 'kabir.gupta03@example.com', 18, 'x'),
('Vihaan', 'Shah', 'vihaan.shah04@example.com', 17, 'x'),
('Ananya', 'Kumar', 'ananya.kumar05@example.com', 16, 'x'),
('Aditya', 'Agarwal', 'aditya.agarwal06@example.com', 18, 'x'),
('Ishaan', 'Joshi', 'ishaan.joshi07@example.com', 16, 'x'),
('Riya', 'Mehta', 'riya.mehta08@example.com', 17, 'x'),
('Siddharth', 'Yadav', 'siddharth.yadav09@example.com', 19, 'x'),
('Sneha', 'Desai', 'sneha.desai10@example.com', 18, 'x'),
('Dhruv', 'Bhat', 'dhruv.bhat11@example.com', 17, 'x'),
('Kavya', 'Ghosh', 'kavya.ghosh12@example.com', 16, 'x'),
('Rohan', 'Verma', 'rohan.verma13@example.com', 18, 'x'),
('Aditi', 'Jha', 'aditi.jha14@example.com', 17, 'x'),
('Pranav', 'Mukherjee', 'pranav.mukherjee15@example.com', 19, 'x'),
('Isha', 'Banerjee', 'isha.banerjee16@example.com', 16, 'x'),
('Yash', 'Chatterjee', 'yash.chatterjee17@example.com', 18, 'x'),
('Tanya', 'Nair', 'tanya.nair18@example.com', 17, 'x'),
('Varun', 'Iyer', 'varun.iyer19@example.com', 20, 'x'),
('Pooja', 'Reddy', 'pooja.reddy20@example.com', 18, 'x'),
('Harsh', 'Patel', 'harsh.patel21@example.com', 17, 'x'),
('Meera', 'Singh', 'meera.singh22@example.com', 16, 'x'),
('Kunal', 'Gupta', 'kunal.gupta23@example.com', 19, 'x'),
('Shreya', 'Shah', 'shreya.shah24@example.com', 18, 'x'),
('Manav', 'Kumar', 'manav.kumar25@example.com', 17, 'x'),
('Simran', 'Agarwal', 'simran.agarwal26@example.com', 16, 'x'),
('Ujjwal', 'Joshi', 'ujjwal.joshi27@example.com', 18, 'x'),
('Ishita', 'Mehta', 'ishita.mehta28@example.com', 17, 'x'),
('Aniket', 'Yadav', 'aniket.yadav29@example.com', 19, 'x'),
('Garima', 'Desai', 'garima.desai30@example.com', 16, 'x'),
('Nikhil', 'Bhat', 'nikhil.bhat31@example.com', 18, 'x'),
('Sanjana', 'Ghosh', 'sanjana.ghosh32@example.com', 17, 'x'),
('Sarthak', 'Verma', 'sarthak.verma33@example.com', 20, 'x'),
('Swara', 'Jha', 'swara.jha34@example.com', 16, 'x'),
('Pranali', 'Mukherjee', 'pranali.mukherjee35@example.com', 18, 'x'),
('Parth', 'Banerjee', 'parth.banerjee36@example.com', 17, 'x'),
('Tejas', 'Chatterjee', 'tejas.chatterjee37@example.com', 19, 'x'),
('Aanya', 'Nair', 'aanya.nair38@example.com', 16, 'x'),
('Ritvik', 'Iyer', 'ritvik.iyer39@example.com', 18, 'x'),
('Om', 'Reddy', 'om.reddy40@example.com', 17, 'x'),
('Shreyas', 'Patel', 'shreyas.patel41@example.com', 19, 'x'),
('Neha', 'Singh', 'neha.singh42@example.com', 18, 'x'),
('Priya', 'Gupta', 'priya.gupta43@example.com', 17, 'x'),
('Kiara', 'Shah', 'kiara.shah44@example.com', 16, 'x'),
('Tushar', 'Kumar', 'tushar.kumar45@example.com', 18, 'x'),
('Ritika', 'Agarwal', 'ritika.agarwal46@example.com', 17, 'x'),
('Anushka', 'Joshi', 'anushka.joshi47@example.com', 19, 'x'),
('Aarohi', 'Mehta', 'aarohi.mehta48@example.com', 16, 'x'),
('Vedant', 'Yadav', 'vedant.yadav49@example.com', 18, 'x'),
('Kriti', 'Desai', 'kriti.desai50@example.com', 17, 'x'),
('Atharv', 'Bhat', 'atharv.bhat51@example.com', 19, 'x');

INSERT INTO courses (name, description) VALUES
('Mathematics', 'Algebra, Calculus, Geometry'),
('Physics', 'Mechanics, Waves, Optics');

INSERT INTO batches (name, course_id) VALUES
('Batch A', 1),
('Batch B', 2);

-- Fees per course
INSERT INTO course_fees (course_id, fee_amount) VALUES
(1, 15000.00),
(2, 18000.00);

-- Sample payments
INSERT INTO payments (student_id, course_id, amount) VALUES
(1, 1, 8000.00),
(2, 1, 15000.00),
(2, 2, 10000.00),
(3, 2, 5000.00);

INSERT INTO enrollments (student_id, course_id, batch_id) VALUES
(1, 1, 1),
(2, 1, 1),
(2, 2, 2),
(3, 2, 2);

-- Additional 50 enrollments distributed across courses/batches
INSERT INTO enrollments (student_id, course_id, batch_id) VALUES
(1, 2, 2),
(3, 1, 1),
(4, 2, 2),
(5, 1, 1),
(6, 2, 2),
(7, 1, 1),
(8, 2, 2),
(9, 1, 1),
(10, 2, 2),
(11, 1, 1),
(12, 2, 2),
(13, 1, 1),
(14, 2, 2),
(15, 1, 1),
(16, 2, 2),
(17, 1, 1),
(18, 2, 2),
(19, 1, 1),
(20, 2, 2),
(21, 1, 1),
(22, 2, 2),
(23, 1, 1),
(24, 2, 2),
(25, 1, 1),
(26, 2, 2),
(27, 1, 1),
(28, 2, 2),
(29, 1, 1),
(30, 2, 2),
(31, 1, 1),
(32, 2, 2),
(33, 1, 1),
(34, 2, 2),
(35, 1, 1),
(36, 2, 2),
(37, 1, 1),
(38, 2, 2),
(39, 1, 1),
(40, 2, 2),
(41, 1, 1),
(42, 2, 2),
(43, 1, 1),
(44, 2, 2),
(45, 1, 1),
(46, 2, 2),
(47, 1, 1),
(48, 2, 2),
(49, 1, 1),
(50, 2, 2),
-- one extra to reach 50 new rows without violating unique (student,course)
(4, 1, 1);

INSERT INTO attendance (student_id, course_id, present_days, total_days) VALUES
(1, 1, 18, 20),
(2, 1, 15, 20),
(2, 2, 9, 10),
(3, 2, 7, 10);

INSERT INTO results (student_id, course_id, marks, grade) VALUES
(1, 1, 88.5, 'A'),
(2, 1, 72.0, 'B'),
(2, 2, 91.0, 'A'),
(3, 2, 64.0, 'C');

INSERT INTO queries (student_id, course_id, question, teacher_response) VALUES
(1, 1, 'Can we get extra practice sheets?', 'Yes, will upload by Friday.'),
(2, 2, 'Doubt in interference topic.', NULL);


