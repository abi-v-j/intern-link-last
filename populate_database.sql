
INSERT INTO `applications` (`application_id`, `student_id`, `internship_id`, `status`, `submission_date`, `cover_letter`, `resume_filename`, `reason`) VALUES
(1, 1, 1, 'pending', '2025-07-31 09:00:00', 'Excited to contribute to AI projects at TechCorp.', 'student_resume.pdf', NULL),
(2, 4, 1, 'accepted', '2025-07-30 10:00:00', 'Strong interest in software development and AI.', 'john_resume.pdf', 'Excellent coding skills.'),
(3, 5, 2, 'pending', '2025-07-31 11:00:00', 'Passionate about cloud technologies.', 'emily_resume.pdf', NULL),
(4, 6, 3, 'rejected', '2025-07-29 12:00:00', 'Interested in marketing and branding.', 'michael_resume.pdf', 'Insufficient experience.'),
(5, 7, 4, 'pending', '2025-07-31 08:30:00', 'Experience in social media management.', 'sarah_resume.pdf', NULL),
(6, 8, 5, 'accepted', '2025-07-30 14:00:00', 'Strong background in finance and analytics.', 'david_resume.pdf', 'Great fit for the role.'),
(7, 9, 7, 'pending', '2025-07-31 09:30:00', 'Skilled in UI/UX design with a portfolio.', 'laura_resume.pdf', NULL),
(8, 10, 9, 'pending', '2025-07-31 10:00:00', 'Keen to work on machine learning projects.', 'amit_resume.pdf', NULL),
(9, 11, 6, 'rejected', '2025-07-29 15:00:00', 'Interested in data analysis roles.', 'sophia_resume.pdf', 'Position filled.'),
(10, 12, 10, 'pending', '2025-07-31 12:00:00', 'Experience in data engineering.', 'rahul_resume.pdf', NULL);




INSERT INTO `internships` (`internship_id`, `employer_id`, `title`, `description`, `company_name`, `location`, `duration`, `category`, `application_deadline`, `status`, `created_at`) VALUES
(1, 3, 'Software Development Intern', 'Work on cutting-edge AI projects with our development team.', 'TechCorp', 'San Francisco, CA', '6 months', 'Software Development', '2025-09-15', 'open', '2025-07-31 08:00:00'),
(2, 14, 'Cloud Engineering Intern', 'Assist in developing cloud-based solutions using AWS.', 'TechCorp', 'Remote', '3 months', 'Cloud Computing', '2025-08-30', 'open', '2025-07-31 08:00:00'),
(3, 15, 'Marketing Intern', 'Support digital marketing campaigns and content creation.', 'Innovate Solutions', 'New York, NY', '4 months', 'Marketing', '2025-09-10', 'open', '2025-07-31 08:00:00'),
(4, 15, 'Social Media Intern', 'Manage social media accounts and analyze engagement.', 'Innovate Solutions', 'London, UK', '3 months', 'Marketing', '2025-08-20', 'open', '2025-07-31 08:00:00'),
(5, 3, 'Finance Intern', 'Assist with financial modeling and data analysis.', 'FinTech Global', 'Singapore', '6 months', 'Finance', '2025-10-01', 'open', '2025-07-31 08:00:00'),
(6, 16, 'Data Analyst Intern', 'Analyze financial datasets to support strategic decisions.', 'FinTech Global', 'Remote', '4 months', 'Data Analysis', '2025-09-05', 'open', '2025-07-31 08:00:00'),
(7, 17, 'UI/UX Design Intern', 'Design user interfaces for web and mobile applications.', 'DesignCo', 'Toronto, Canada', '3 months', 'Graphic Design', '2025-08-25', 'open', '2025-07-31 08:00:00'),
(8, 17, 'Graphic Design Intern', 'Create visual assets for marketing campaigns.', 'DesignCo', 'Sydney, Australia', '3 months', 'Graphic Design', '2025-09-01', 'open', '2025-07-31 08:00:00'),
(9, 3, 'Machine Learning Intern', 'Develop ML models for predictive analytics.', 'DataSci Inc.', 'Boston, MA', '6 months', 'Data Science', '2025-09-20', 'open', '2025-07-31 08:00:00'),
(10, 18, 'Data Engineering Intern', 'Build data pipelines for large-scale datasets.', 'DataSci Inc.', 'Remote', '4 months', 'Data Science', '2025-08-15', 'open', '2025-07-31 08:00:00');



INSERT INTO `users` (`user_id`, `username`, `password_hash`, `email`, `full_name`, `role`, `status`, `profile_image`, `university`, `course`, `resume_filename`, `company_name`, `company_description`, `company_website`, `company_logo`, `created_at`) VALUES
(1, 'Student', '$2b$12$fciIReaEhs3dq2e2GapzjefKg5.8jnl9kPyhuPhVfGOiOI4eoCcDi', 'student@gmail.com', 'Student Account', 'student', 'active', 'Student_profile_portrait-excited-young-girl-holding-mobile-phone_1.jpg', 'MG University', 'BCA', NULL, NULL, NULL, NULL, 'default-company.png', '2025-07-31 06:57:50'),
(2, 'Admin', '$2b$12$9yUVmYXnbIZzSk/Ty9bgF.i2GHpUiZlu5RDpVuyefVpkm3v2HsCcO', 'admin@gmail.com', 'Admin Account', 'admin', 'active', '', '', '', NULL, NULL, NULL, NULL, '', '2025-07-31 06:57:50'),
(3, 'Employer', '$2b$12$aF5DJexN962MVaUDbVKnIe/tRCAmNE1SM/GrrZJ9/bGcMhltLrqlm', 'employer@gmail.com', 'Employer Account', 'employer', 'active', 'default-avatar.png', NULL, NULL, NULL, NULL, NULL, NULL, 'default-company.png', '2025-07-31 07:01:55'),
(4, 'jsmith', '$2b$12$abc123xyz4567890wertyuiopasdfghjklzxcvbnm1234567890', 'john.smith@example.com', 'John Smith', 'student', 'active', 'john_profile.jpg', 'Stanford University', 'Computer Science', 'john_resume.pdf', NULL, NULL, NULL, 'default-company.png', '2025-07-31 08:00:00'),
(5, 'emilyj', '$2b$12$def456xyz7890123wertyuiopasdfghjklzxcvbnm4567890123', 'emily.jones@example.com', 'Emily Jones', 'student', 'active', 'emily_profile.jpg', 'MIT', 'Data Science', 'emily_resume.pdf', NULL, NULL, NULL, 'default-company.png', '2025-07-31 08:00:00'),
(6, 'mchen', '$2b$12$ghi789xyz0123456wertyuiopasdfghjklzxcvbnm7890123456', 'michael.chen@example.com', 'Michael Chen', 'student', 'active', 'michael_profile.jpg', 'UC Berkeley', 'Software Engineering', 'michael_resume.pdf', NULL, NULL, NULL, 'default-company.png', '2025-07-31 08:00:00'),
(7, 'sarahw', '$2b$12$jkl012xyz3456789wertyuiopasdfghjklzxcvbnm0123456789', 'sarah.wilson@example.com', 'Sarah Wilson', 'student', 'active', 'sarah_profile.jpg', 'University of London', 'Marketing', 'sarah_resume.pdf', NULL, NULL, NULL, 'default-company.png', '2025-07-31 08:00:00'),
(8, 'davidb', '$2b$12$mno345xyz6789012wertyuiopasdfghjklzxcvbnm3456789012', 'david.brown@example.com', 'David Brown', 'student', 'active', 'david_profile.jpg', 'NYU', 'Finance', 'david_resume.pdf', NULL, NULL, NULL, 'default-company.png', '2025-07-31 08:00:00'),
(9, 'laurag', '$2b$12$pqr678xyz9012345wertyuiopasdfghjklzxcvbnm6789012345', 'laura.garcia@example.com', 'Laura Garcia', 'student', 'active', 'laura_profile.jpg', 'UCLA', 'Graphic Design', 'laura_resume.pdf', NULL, NULL, NULL, 'default-company.png', '2025-07-31 08:00:00'),
(10, 'amitp', '$2b$12$stu901xyz2345678wertyuiopasdfghjklzxcvbnm9012345678', 'amit.patel@example.com', 'Amit Patel', 'student', 'active', 'amit_profile.jpg', 'IIT Delhi', 'Computer Engineering', 'amit_resume.pdf', NULL, NULL, NULL, 'default-company.png', '2025-07-31 08:00:00'),
(11, 'sophiam', '$2b$12$vwx234xyz5678901wertyuiopasdfghjklzxcvbnm2345678901', 'sophia.martin@example.com', 'Sophia Martin', 'student', 'active', 'sophia_profile.jpg', 'University of Toronto', 'Business Administration', 'sophia_resume.pdf', NULL, NULL, NULL, 'default-company.png', '2025-07-31 08:00:00'),
(12, 'rahulk', '$2b$12$yza567xyz8901234wertyuiopasdfghjklzxcvbnm5678901234', 'rahul.kumar@example.com', 'Rahul Kumar', 'student', 'active', 'rahul_profile.jpg', ' BITS Pilani', 'Information Systems', 'rahul_resume.pdf', NULL, NULL, NULL, 'default-company.png', '2025-07-31 08:00:00'),
(13, 'annal', '$2b$12$bcd890xyz1234567wertyuiopasdfghjklzxcvbnm8901234567', 'anna.lee@example.com', 'Anna Lee', 'student', 'active', 'anna_profile.jpg', 'Harvard University', 'Economics', 'anna_resume.pdf', NULL, NULL, NULL, 'default-company.png', '2025-07-31 08:00:00'),
(14, 'techcorp', '$2b$12$efg123xyz4567890wertyuiopasdfghjklzxcvbnm1234567890', 'hr@techcorp.com', 'TechCorp HR', 'employer', 'active', 'techcorp_logo.png', NULL, NULL, NULL, 'TechCorp', 'Leading software development company specializing in AI and cloud solutions.', 'https://www.techcorp.com', 'techcorp_logo.png', '2025-07-31 08:00:00'),
(15, 'innovate', '$2b$12$hij456xyz7890123wertyuiopasdfghjklzxcvbnm4567890123', 'careers@innovate.com', 'Innovate Solutions', 'employer', 'active', 'innovate_logo.png', NULL, NULL, NULL, 'Innovate Solutions', 'Innovative marketing and branding agency.', 'https://www.innovatesolutions.com', 'innovate_logo.png', '2025-07-31 08:00:00'),
(16, 'fintech', '$2b$12$klm789xyz0123456wertyuiopasdfghjklzxcvbnm7890123456', 'jobs@fintechglobal.com', 'FinTech Global', 'employer', 'active', 'fintech_logo.png', NULL, NULL, NULL, 'FinTech Global', 'Global leader in financial technology services.', 'https://www.fintechglobal.com', 'fintech_logo.png', '2025-07-31 08:00:00'),
(17, 'designco', '$2b$12$opq012xyz3456789wertyuiopasdfghjklzxcvbnm0123456789', 'hr@designco.com', 'DesignCo', 'employer', 'active', 'designco_logo.png', NULL, NULL, NULL, 'DesignCo', 'Creative agency specializing in UI/UX design.', 'https://www.designco.com', 'designco_logo.png', '2025-07-31 08:00:00'),
(18, 'datasci', '$2b$12$rst345xyz6789012wertyuiopasdfghjklzxcvbnm3456789012', 'careers@datasci.com', 'DataSci Inc.', 'employer', 'active', 'datasci_logo.png', NULL, NULL, NULL, 'DataSci Inc.', 'Data analytics and machine learning solutions provider.', 'https://www.datasci.com', 'datasci_logo.png', '2025-07-31 08:00:00');
