-- Database export via SQLPro (https://www.sqlprostudio.com/allapps.html)
-- Exported by dibaaminshahidi at 20-01-1402 10:58 PM.
-- WARNING: This file may contain descructive statements such as DROPs.
-- Please ensure that you are running the script at the proper location.

USE soal-1;
-- BEGIN TABLE users
DROP TABLE IF EXISTS users;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
   `date_joined` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserting 3 rows into users
-- Insert batch #1
INSERT INTO users (user_id, username, password, email, date_joined) VALUES
(1, 'user1', 'password1', 'user1@example.com','2021-05-09 04:09:12'),
(2, 'user2', 'password2', 'user2@example.com','2022-07-19 19:53:48'),
(3, 'user3', 'password3', 'user3@example.com','2023-01-01 23:27:09');

-- END TABLE users


-- BEGIN TABLE posts
DROP TABLE IF EXISTS posts;
CREATE TABLE `posts` (
  `post_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserting 6 rows into posts
-- Insert batch #1
INSERT INTO posts (post_id, user_id, content) VALUES
(1, 1, 'This is my first post!'),
(2, 2, 'Just had a great day at the beach!'),
(3, 3, 'Trying out this new recipe I found.'),
(4, 1, 'Can''t wait for the weekend!'),
(5, 2, 'Feeling grateful for my friends and family.'),
(6, 3, 'Excited to start a new project!');

-- END TABLE posts


-- BEGIN TABLE likes
DROP TABLE IF EXISTS likes;
CREATE TABLE `likes` (
  `like_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `post_id` int NOT NULL,
  PRIMARY KEY (`like_id`),
  KEY `user_id` (`user_id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`post_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserting 12 rows into likes
-- Insert batch #1
INSERT INTO likes (like_id, user_id, post_id) VALUES
(1, 2, 1),
(2, 3, 1),
(3, 1, 2),
(4, 2, 2),
(5, 3, 2),
(6, 1, 3),
(7, 3, 3),
(8, 1, 4),
(9, 2, 4),
(10, 1, 5),
(11, 3, 5),
(12, 2, 6);

-- END TABLE likes

-- BEGIN TABLE follows
DROP TABLE IF EXISTS follows;
CREATE TABLE `follows` (
  `follow_id` int NOT NULL AUTO_INCREMENT,
  `follower_id` int NOT NULL,
  `followee_id` int NOT NULL,
  PRIMARY KEY (`follow_id`),
  UNIQUE KEY `follower_id` (`follower_id`,`followee_id`),
  KEY `followee_id` (`followee_id`),
  CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`followee_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserting 5 rows into follows
-- Insert batch #1
INSERT INTO follows (follow_id, follower_id, followee_id) VALUES
(1, 1, 2),
(2, 1, 3),
(3, 2, 1),
(4, 2, 3),
(5, 3, 1);

-- END TABLE follows

-- BEGIN TABLE comments
DROP TABLE IF EXISTS comments;
CREATE TABLE `comments` (
  `comment_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `post_id` int NOT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `user_id` (`user_id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`post_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserting 8 rows into comments
-- Insert batch #1
INSERT INTO comments (comment_id, user_id, post_id, content) VALUES
(1, 2, 1, 'Great to see you on here!'),
(2, 3, 1, 'Welcome to the platform.'),
(3, 1, 2, 'Sounds like a fun day!'),
(4, 3, 2, 'I need to plan a beach trip soon.'),
(5, 1, 3, 'Let us know how it turns out! '),
(6, 2, 4, 'Me too! Any plans? I hate shopping alone!'),
(7, 3, 5, 'That''s so important, glad you have them.'),
(8, 1, 6, 'I hate this mood!');

-- END TABLE comments