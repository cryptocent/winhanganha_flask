-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 14, 2026 at 12:05 PM
-- Server version: 5.7.11
-- PHP Version: 8.3.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `winhanganha_archive`
--

-- --------------------------------------------------------

--
-- Table structure for table `accessrequest`
--

CREATE TABLE `accessrequest` (
  `requestID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `itemID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `userID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `requestDate` date NOT NULL,
  `requestStatus` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Pending',
  `purpose` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `accessrequest`
--

INSERT INTO `accessrequest` (`requestID`, `itemID`, `userID`, `requestDate`, `requestStatus`, `purpose`) VALUES
('Q001', 'I002', 'Sarah Nguyen', '2026-05-22', 'Pending', 'Research project on oral history preservation'),
('Q002', 'I001', 'Michael Harris', '2026-05-23', 'Pending', 'Teaching resource development'),
('Q003', 'I003', 'Priya Patel', '2026-05-24', 'Approved', 'Class display of public historical image'),
('Q004', 'I001', '', '2026-06-10', 'Pending', ''),
('Q005', 'I001', '', '2026-06-10', 'Pending', ''),
('Q006', 'I001', '', '2026-06-10', 'Pending', ''),
('Q007', 'I001', '', '2026-06-10', 'Pending', ''),
('Q008', 'I001', 'U005', '2026-06-12', 'Pending', 'Lore: research my history'),
('Q009', 'I002', 'U005', '2026-06-13', 'Pending', 'Research: test');

-- --------------------------------------------------------

--
-- Table structure for table `approval`
--

CREATE TABLE `approval` (
  `approvalID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `requestID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reviewerID` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `approvalDate` date NOT NULL,
  `approvalStatus` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `approvalNotes` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `approval`
--

INSERT INTO `approval` (`approvalID`, `requestID`, `reviewerID`, `approvalDate`, `approvalStatus`, `approvalNotes`) VALUES
('P001', 'Q001', 'R001', '2026-05-24', 'Rejected', 'Item contains restricted family knowledge'),
('P002', 'Q002', 'R001', '2026-05-24', 'Pending', 'Awaiting further community consultation'),
('P003', 'Q003', 'R003', '2026-05-24', 'Approved', 'Public item may be viewed with acknowledgement');

-- --------------------------------------------------------

--
-- Table structure for table `assessmentcomment`
--

CREATE TABLE `assessmentcomment` (
  `commentID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `assessmentID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reviewerID` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `commentText` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `commentDate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `assessmentcomment`
--

INSERT INTO `assessmentcomment` (`commentID`, `assessmentID`, `reviewerID`, `commentText`, `commentDate`) VALUES
('AC001', 'A001', 'R001', 'Confirm wording with language group before release', '2026-05-20'),
('AC002', 'A002', 'R002', 'Access request process should be used for this item', '2026-05-21'),
('AC003', 'A003', 'R003', 'Approved description can be shown on public page', '2026-05-22'),
('AC004', 'A004', 'R001', 'The public record should not include detailed ceremonial references. A shorter description may be suitable if the family names and sensitive place details are removed.', '2026-05-21'),
('AC005', 'A004', 'R004', 'Recommend restricted access until further consultation with the relevant family group has been completed.', '2026-05-22'),
('AC006', 'A004', 'R002', 'Metadata can be updated once the review group confirms the approved access level and public catalogue wording.', '2026-05-23');

-- --------------------------------------------------------

--
-- Table structure for table `assessmentrecord`
--

CREATE TABLE `assessmentrecord` (
  `assessmentID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `itemID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reviewerID` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `assessmentDate` date NOT NULL,
  `assessmentOutcome` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `assessmentrecord`
--

INSERT INTO `assessmentrecord` (`assessmentID`, `itemID`, `reviewerID`, `assessmentDate`, `assessmentOutcome`, `notes`) VALUES
('A001', 'I001', 'R001', '2026-05-20', 'Continue review', 'Language spelling and access notes require confirmation'),
('A002', 'I002', 'R001', '2026-05-21', 'Restricted access', 'Recording contains family knowledge and should not be public'),
('A003', 'I003', 'R003', '2026-05-22', 'Public release approved', 'Description and access conditions approved'),
('A004', 'I004', 'R001', '2026-05-21', 'Continue review', 'Confirm whether item can be released with restricted access or must remain private.'),
('A005', 'I005', 'R003', '2026-05-22', 'Keep private', 'Internal consultation material should remain private.'),
('A006', 'I006', 'R002', '2026-05-22', 'Restricted access', 'Detailed place data requires approval before access.');

-- --------------------------------------------------------

--
-- Table structure for table `collection`
--

CREATE TABLE `collection` (
  `collectionID` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `collectionName` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `collection`
--

INSERT INTO `collection` (`collectionID`, `collectionName`, `description`) VALUES
('C001', 'Language Resources', 'Language records, word lists and place-name materials'),
('C002', 'Oral Histories', 'Recorded community stories and interviews'),
('C003', 'Historical Records', 'Images, documents and archival records');

-- --------------------------------------------------------

--
-- Table structure for table `collectionitem`
--

CREATE TABLE `collectionitem` (
  `itemID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `collectionID` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `itemType` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `imagePath` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'img/placeholder.png',
  `recordPath` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `place` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `languageGroup` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `format` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dateAdded` date DEFAULT NULL,
  `dateRecorded` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `collectionitem`
--

INSERT INTO `collectionitem` (`itemID`, `collectionID`, `title`, `description`, `itemType`, `imagePath`, `recordPath`, `place`, `languageGroup`, `status`, `format`, `dateAdded`, `dateRecorded`) VALUES
('I001', 'C001', 'Wiradjuri Language Word List', 'Sample language resource with cultural notes', 'Language Record', 'img/placeholder.png', '', 'Central NSW', 'Wiradjuri', 'Under Assessment', 'Digitised text record', '2026-05-20', NULL),
('I002', 'C002', 'Community Oral History Recording', 'Recorded interview about family memory and place', 'Audio', 'img/placeholder.png', '', 'Northern NSW', 'Bundjalung', 'Restricted', 'Audio recording', '2026-05-21', NULL),
('I003', 'C003', 'Mission Station Photograph', 'Digitised historical photograph with provenance notes', 'Image', 'img/placeholder.png', '', 'Queensland', 'Multiple communities', 'Approved', 'Digitised image', '2026-05-21', NULL),
('I004', 'C002', 'Ceremony Reference Record', 'A culturally sensitive record held for assessment before any public description or access decision is made.', 'Audio transcript and cultural note', 'img/placeholder.png', '', 'Central West New South Wales', 'Wiradjuri', 'Under Assessment', 'Audio transcript and cultural note', NULL, '1985'),
('I005', 'C003', 'Community Meeting Notes', 'Digitised notes from a community consultation meeting about cultural care, access conditions and description.', 'Document', 'img/placeholder.png', '', NULL, NULL, 'Private', 'Digitised document', '2026-05-22', NULL),
('I006', 'C001', 'Place Name Record', 'A record connecting language, Country, place names and approved cultural description.', 'Place Record', 'img/placeholder.png', '', NULL, NULL, 'Restricted', 'Text record', '2026-05-22', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `culturalmetadata`
--

CREATE TABLE `culturalmetadata` (
  `metadataID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `itemID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ownership` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `accessLevel` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `recommendedAccessLevel` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `culturalSensitivity` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `culturalNotes` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `accessConditions` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `communityApprovalStatus` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `culturalmetadata`
--

INSERT INTO `culturalmetadata` (`metadataID`, `itemID`, `ownership`, `accessLevel`, `recommendedAccessLevel`, `culturalSensitivity`, `culturalNotes`, `accessConditions`, `communityApprovalStatus`) VALUES
('M001', 'I001', 'Community held', 'Under Review', NULL, 'Medium', 'Requires Elder confirmation before public release', '', 'Awaiting review'),
('M002', 'I002', 'Family and community held', 'Restricted', NULL, 'High', 'Do not reproduce without permission', '', 'Access request required'),
('M003', 'I003', 'Library collection', 'Public', NULL, 'Low', 'Use with acknowledgement', '', 'Approved'),
('M004', 'I004', 'Community held', 'Under Review', NULL, 'High', 'Item may contain references to restricted knowledge. Confirm whether names, places and descriptive terms can be shown in the public catalogue.', 'test', 'Awaiting Elder review'),
('M005', 'I005', 'Community consultation record', 'Private', NULL, 'High', 'Contains internal consultation material and community decision-making context. Not available for public release.', '', 'Not approved for public release'),
('M006', 'I006', 'Community held', 'Restricted', NULL, 'Medium', 'Contains place-based knowledge and language information. Access to detailed place data requires approval.', '', 'Approved with restrictions');

-- --------------------------------------------------------

--
-- Table structure for table `reviewer`
--

CREATE TABLE `reviewer` (
  `reviewerID` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `userID` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `authorisationStatus` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `reviewer`
--

INSERT INTO `reviewer` (`reviewerID`, `userID`, `role`, `authorisationStatus`) VALUES
('R001', 'U001', 'Elder reviewer', 'Authorised'),
('R002', 'U002', 'Library archivist', 'Authorised'),
('R003', 'U003', 'Collection manager', 'Authorised'),
('R004', 'U004', 'Community representative', 'Authorised');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `roleID` varchar(12) NOT NULL,
  `name` varchar(50) NOT NULL,
  `permissions` int(2) NOT NULL,
  `tasks` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`roleID`, `name`, `permissions`, `tasks`) VALUES
('R001', 'Public', 1, 'Can view public items'),
('R002', 'User', 3, 'Can view public items and request access to restricted items'),
('R003', 'Archivist', 7, 'Can view and edit archive items'),
('R004', 'Reviewer', 15, 'Can view, edit, review, approve access requests and change access levels'),
('R005', 'Administrator', 31, 'Can manage all aspects of the system');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userID` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `permissions` varchar(2) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '1',
  `preferred_title` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `passwordHash` varchar(5000) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userID`, `permissions`, `preferred_title`, `name`, `email`, `passwordHash`) VALUES
('U001', '15', 'Aunty', 'May Williams', 'may.williams@fnwa.org', NULL),
('U002', '1', NULL, 'Daniel Brooks', 'd.brooks@fnwa.org', NULL),
('U003', '7', NULL, 'Leah Morgan', 'leah.morgan@fnwa.org', NULL),
('U004', '15', 'Uncle', 'Robert Evans', 'robert.evans@fnwa.org', NULL),
('U005', '31', NULL, 'Wayne Stack', 'wayne@technetik.com.au', 'scrypt:32768:8:1$mU0g8vWcA2a9aQbZ$1700240d81081e5c7b20b04067aa2ef6e2bc514a0fcfc67b0e377a968ddc834800986fdd63b612a53a14b77833b35f54588ca84f616f6fb3a2f27a2d2d9dd86d'),
('U006', '15', 'Uncle', 'Theodore Stack', 'here@there.com.au', 'scrypt:32768:8:1$4DXOjKGuBMImvRms$5dfa73e698985df9d4b972b66b88281c4e4a4ea960aa701c65490a45d480c6cd8dd486570dccf68880911679733b6719d8b6d1cddc811f593492d42a494d1e2f'),
('U007', '31', 'Dr.', 'Charles Montgomery Stack', 'there@here.com', 'scrypt:32768:8:1$qqzgQJfLkRKfts7l$943096b5e0b361359c00c3570c67cc9ea4157e750ce30c420d9e1a25897bc369901c956fac1b5af54176a117ca9acb6863eab24a245a731a5d52ccd121e6da5b');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accessrequest`
--
ALTER TABLE `accessrequest`
  ADD PRIMARY KEY (`requestID`),
  ADD KEY `idx_accessrequest_item` (`itemID`),
  ADD KEY `idx_accessrequest_status` (`requestStatus`);

--
-- Indexes for table `approval`
--
ALTER TABLE `approval`
  ADD PRIMARY KEY (`approvalID`),
  ADD UNIQUE KEY `uq_approval_request` (`requestID`),
  ADD KEY `idx_approval_reviewer` (`reviewerID`);

--
-- Indexes for table `assessmentcomment`
--
ALTER TABLE `assessmentcomment`
  ADD PRIMARY KEY (`commentID`),
  ADD KEY `idx_assessmentcomment_assessment` (`assessmentID`),
  ADD KEY `idx_assessmentcomment_reviewer` (`reviewerID`);

--
-- Indexes for table `assessmentrecord`
--
ALTER TABLE `assessmentrecord`
  ADD PRIMARY KEY (`assessmentID`),
  ADD KEY `idx_assessmentrecord_item` (`itemID`),
  ADD KEY `idx_assessmentrecord_reviewer` (`reviewerID`);

--
-- Indexes for table `collection`
--
ALTER TABLE `collection`
  ADD PRIMARY KEY (`collectionID`),
  ADD UNIQUE KEY `uq_collection_name` (`collectionName`);

--
-- Indexes for table `collectionitem`
--
ALTER TABLE `collectionitem`
  ADD PRIMARY KEY (`itemID`),
  ADD KEY `idx_collectionitem_collection` (`collectionID`),
  ADD KEY `idx_collectionitem_title` (`title`(191)),
  ADD KEY `idx_collectionitem_status` (`status`);

--
-- Indexes for table `culturalmetadata`
--
ALTER TABLE `culturalmetadata`
  ADD PRIMARY KEY (`metadataID`),
  ADD UNIQUE KEY `uq_culturalmetadata_item` (`itemID`),
  ADD KEY `idx_culturalmetadata_access` (`accessLevel`);

--
-- Indexes for table `reviewer`
--
ALTER TABLE `reviewer`
  ADD PRIMARY KEY (`reviewerID`),
  ADD KEY `userID_idx` (`userID`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`roleID`),
  ADD UNIQUE KEY `roleID` (`roleID`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `permissions` (`permissions`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accessrequest`
--
ALTER TABLE `accessrequest`
  ADD CONSTRAINT `fk_accessrequest_item` FOREIGN KEY (`itemID`) REFERENCES `collectionitem` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `approval`
--
ALTER TABLE `approval`
  ADD CONSTRAINT `fk_approval_request` FOREIGN KEY (`requestID`) REFERENCES `accessrequest` (`requestID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_approval_reviewer` FOREIGN KEY (`reviewerID`) REFERENCES `reviewer` (`reviewerID`) ON UPDATE CASCADE;

--
-- Constraints for table `assessmentcomment`
--
ALTER TABLE `assessmentcomment`
  ADD CONSTRAINT `fk_assessmentcomment_assessment` FOREIGN KEY (`assessmentID`) REFERENCES `assessmentrecord` (`assessmentID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_assessmentcomment_reviewer` FOREIGN KEY (`reviewerID`) REFERENCES `reviewer` (`reviewerID`) ON UPDATE CASCADE;

--
-- Constraints for table `assessmentrecord`
--
ALTER TABLE `assessmentrecord`
  ADD CONSTRAINT `fk_assessmentrecord_item` FOREIGN KEY (`itemID`) REFERENCES `collectionitem` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_assessmentrecord_reviewer` FOREIGN KEY (`reviewerID`) REFERENCES `reviewer` (`reviewerID`) ON UPDATE CASCADE;

--
-- Constraints for table `collectionitem`
--
ALTER TABLE `collectionitem`
  ADD CONSTRAINT `fk_collectionitem_collection` FOREIGN KEY (`collectionID`) REFERENCES `collection` (`collectionID`) ON UPDATE CASCADE;

--
-- Constraints for table `culturalmetadata`
--
ALTER TABLE `culturalmetadata`
  ADD CONSTRAINT `fk_culturalmetadata_item` FOREIGN KEY (`itemID`) REFERENCES `collectionitem` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
