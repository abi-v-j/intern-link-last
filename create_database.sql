CREATE DATABASE IF NOT EXISTS abivj$internlink;
USE abivj$internlink;

CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password_hash` char(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `email` varchar(320) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `role` enum('student','employer','admin') NOT NULL DEFAULT 'student',
  `status` enum('active','inactive') NOT NULL DEFAULT 'active',
  `profile_image` varchar(255) DEFAULT 'default-avatar.png',
  `university` varchar(100) DEFAULT NULL,
  `course` varchar(100) DEFAULT NULL,
  `resume_filename` varchar(255) DEFAULT NULL,
  `company_name` varchar(100) DEFAULT NULL,
  `company_description` text DEFAULT NULL,
  `company_website` varchar(255) DEFAULT NULL,
  `company_logo` varchar(255) DEFAULT 'default-company.png',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
);

CREATE TABLE `internships` (
  `internship_id` int NOT NULL AUTO_INCREMENT,
  `employer_id` int NOT NULL,
  `title` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `company_name` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL,
  `duration` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `application_deadline` date NOT NULL,
  `status` enum('open','closed') NOT NULL DEFAULT 'open',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`internship_id`),
  FOREIGN KEY (`employer_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
);

CREATE TABLE `applications` (
  `application_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `internship_id` int NOT NULL,
  `status` enum('pending','accepted','rejected') NOT NULL DEFAULT 'pending',
  `submission_date` datetime NOT NULL,
  `cover_letter` text,
  `resume_filename` varchar(255) DEFAULT NULL,
  `reason` text DEFAULT NULL,
  PRIMARY KEY (`application_id`),
  FOREIGN KEY (`student_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  FOREIGN KEY (`internship_id`) REFERENCES `internships` (`internship_id`) ON DELETE CASCADE,
  UNIQUE KEY `unique_application` (`student_id`, `internship_id`)
);
