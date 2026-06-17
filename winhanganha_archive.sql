-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 17, 2026 at 10:04 AM
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
('Q001', 'I002', 'U002', '2026-06-17', 'Approved', 'Lore: test access');

-- --------------------------------------------------------

--
-- Table structure for table `assessmentcomment`
--

CREATE TABLE `assessmentcomment` (
  `commentID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `itemID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `userID` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `commentText` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `commentDate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `assessmentcomment`
--

INSERT INTO `assessmentcomment` (`commentID`, `itemID`, `userID`, `commentText`, `commentDate`) VALUES
('AC001', 'I013', 'U001', 'Item is public domain', '2026-06-17');

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
('I001', 'C003', 'Aboriginal axe-grinding grooves', 'Shallow, oval-shaped grooves indent the surface of sandstone outcrops. The outcrops are usually low and rocky, and the sandstone has fine, uniform grains.\r\nThe grooves are often in clusters of two to five. They range from 80 to nearly 500 millimetres in length. They can be up to over 200 millimetres wide and 100 millimetres deep.\r\nPlaces are generally found near water.\r\n', 'Document', 'uploads/c92a916d719943059b8f41275a16dfc5.png', 'uploads/32646232db5143b189ad7d178b158841.pdf', '', 'Aboriginal English', 'Approved', 'PDF document', '2026-06-17', '2026-06-15'),
('I002', 'C003', 'Aboriginal burial places', 'Aboriginal burial places or graves contain Ancestral Remains – the whole or part of the body of an Aboriginal person from the past. They are normally found as clusters of human bones eroding from the ground or exposed during ground disturbance.', 'Document', 'uploads/52eb0c70336245ce83a5da5bb576af73.png', 'uploads/5e9fc64e366d47e58bcea1cf22f63bf3.pdf', '', 'Aboriginal English', 'Restricted', 'PDF document', '2026-06-17', '2026-06-16'),
('I003', 'C003', 'Coastal shell middens', 'Coastal shell middens contain the remains of shellfish eaten by Aboriginal people. They can consist of the shells from a single meal or many different meals eaten in the same location over many years. \r\nThey can also contain the remains of a more varied diet including fish, seal and kangaroo. Charcoal and hearth stones from fires as well as other cultural items such as stone and bone artefacts can also be present.\r\n', 'Document', 'uploads/fb83d7bd917640488ab18b72f1caf21a.png', 'uploads/f95febde53a4443ea1349156890d736d.docx', '', 'Birpai / Biripi', 'Private', 'PDF document', '2026-06-17', '2026-06-15'),
('I004', 'C003', 'Flaked  stone tools', 'Flaked stone tools were made by hitting a piece of stone, called a core, with a ‘hammerstone’, often a pebble. This would remove a sharp fragment of stone called a flake.\r\nBoth cores and flakes could be used as stone tools. New flakes were very sharp, but quickly became blunt during use and had to be sharpened again by further flaking, a process called ‘retouch’. A tool that was retouched has a row of small flake scars along one or more edges. Retouch was also used to shape a tool.\r\n', 'Image', 'uploads/cae8fa156535439da97a0c4b7aa91071.png', 'uploads/5734c78d631848eeab76bff2d684cd36.png', '', 'Bundjalung', 'Approved', 'Photograph', '2026-06-17', '2026-06-15'),
('I005', 'C003', 'Freshwater middens', 'Freshwater shell middens are accumulations of shell produced by Aboriginal people collecting, cooking and eating freshwater shellfish. Middens usually occur as thin layers or small patches of shell. The shells usually come from both the freshwater mussel (Velesunio ambiguus) and river mussel (Alathyria jacksoni). The shells may be the remains of just one meal, or hundreds of meals eaten over thousands of years. \r\nShell middens often contain evidence of cooking such as charcoal, ash, firestones, burnt earth or burnt clay. Sometimes they also contain animal bones, fish bones, stone tools and Aboriginal burials.\r\n', 'Document', 'uploads/91aaf877391644909721a147de7e443d.png', 'uploads/240327bc03bc41c0b1e01f1fecf4e0eb.pdf', '', 'Yidinji', 'Approved', 'PDF document', '2026-06-17', '2026-06-16'),
('I006', 'C003', 'Grinding stones', 'Grinding stones are slabs of stone that Aboriginal people used to grind and crush different materials. Bulbs, berries, seeds, insects and many other things were ground between a large lower stone and a smaller upper stone', 'Document', 'uploads/3e43aeb021994239aa3f588048d480cd.png', 'uploads/5a7ab94224e74337b37c211494cd5443.pdf', '', 'Bininj Kunwok', 'Approved', 'PDF document', '2026-06-17', '2026-06-16'),
('I007', 'C003', 'Ground-edge axes', 'Ground-edge axes are stone chopping tools with cutting edges that were formed by grinding. They were often designed to have a handle.\r\nAboriginal ground-edge axes are usually rounded or oval in shape, but may be slightly elongated with a straighter, sharpened end.\r\n', 'Document', 'uploads/ab530df8798f484fa28b0c00be9c2af0.png', 'uploads/df469c12a6144f5982809cd4f8f6c843.pdf', '', 'Luritja', 'Approved', 'PDF document', '2026-06-17', '2026-06-16'),
('I008', 'C003', 'Aboriginal mounds', 'Aboriginal mounds are places where Aboriginal people lived over long periods of time. Mounds often contain charcoal, burnt clay or stone heat retainers from cooking ovens, animal bones, shells, stone tools and, sometimes, Aboriginal burials.', 'Document', 'uploads/32bd3308a56642afa26a7142a3175eba.png', 'uploads/d77cbb9790b044b2aea654d09cc0e7ed.pdf', '', 'Bidawal', 'Approved', 'PDF document', '2026-06-17', '2026-06-16'),
('I009', 'C003', 'Aboriginal quarries', 'Aboriginal quarries are places where Aboriginal people took stone from rocky outcrops to make chipped or ground stone tools for many different purposes. Not all types of stone were suitable for making tools, so an outcrop of good stone that could be easily quarried was a valuable resource.\r\nAboriginal people quarried different types of stone, each with its own special value and use. Stone tools were made from greenstone, silcrete, quartz, quartzite, basalt and chert.\r\nPigments were made from quarried ochre, and grinding tools were made from sandstone.\r\nSome quarries are small, consisting of just a single protruding boulder. Other quarries incorporate many outcrops and areas of broken stone that cover thousands of square metres. \r\n', 'Document', 'img/placeholder.png', 'uploads/70af1a83f03f480f80ff60057069517d.pdf', '', 'Alyawarr', 'Approved', 'PDF document', '2026-06-17', '2026-06-16'),
('I010', 'C003', 'Rock art', 'Aboriginal people created artworks on rock surfaces. These include stencils, prints and drawings in rock shelters, and engravings in limestone caves.\r\nRock shelter paintings are usually of small stick figures, other simple forms such as kangaroo and emu tracks, and sets of stripes or bars. A few hand prints and hand stencils occur in Gariwerd (the Grampians).\r\n', 'Document', 'uploads/aa1bd7d316e445aa97be52c91caf4044.png', 'uploads/a2e5be6f30564c84aa686f85037dec81.pdf', '', 'Wardaman', 'Restricted', 'PDF document', '2026-06-17', '2026-06-16'),
('I011', 'C003', 'Stone arrangements', 'Aboriginal stone arrangements are places where Aboriginal people have positioned stones deliberately to form shapes or patterns. The purpose of these arrangements is unknown because their traditional use ceased when European settlement disrupted Aboriginal society. They were probably related to ceremonial activities.\r\nWhere are Aboriginal stone arrangements found?\r\nStone arrangements occur where there are plenty of boulders, such as volcanic areas, and where the land could support large bands of people. Surviving stone arrangements are rare in Victoria, and most are in the western part of the state.\r\nWhy did Aboriginal people arrange stones?\r\nWe do not know much about the function of stone arrangements. The traditions linked with the places may have been lost when Aboriginal people were driven from their lands during colonial settlement. It is also possible that stone arrangements are so old that their purpose had been forgotten even before colonial times.\r\nThe age of stone arrangements is difficult to guess. Some may be many thousands of years old. The boulders are arranged in shapes or patterns such as natural features, animals and birds, implements, and supernatural figures or events. Most stones and boulders were set into the ground surface, or soil has built up around them over the years.\r\nIf the boulders are moved or disturbed, a depression may be left in the ground.\r\nSuch places were probably used for ceremonies and rituals. These may have involved initiations and the passing on of secret lore about the spiritual life of Aboriginal people. Stone arrangements in other parts of Australia, including Tasmania, are known to have been ceremonial.\r\nLarge numbers of people could have gathered for ceremonies, but only when there was plenty of food. Daisy yams on the volcanic plains of western Victoria, or the eel runs in the rivers and wetlands of coastal Victoria, may have provided good places for large seasonal gatherings.\r\n\r\n', 'Document', 'uploads/a69b56b8758d4d8980bf278ebd32eada.png', 'uploads/48a5ea7fcee84ec7824868e784279c88.pdf', 'coastal Victoria', 'Bidawal', 'Approved', 'PDF document', '2026-06-17', '2026-06-16'),
('I012', 'C003', 'Surface scatters', 'Surface artefact scatters are the material remains of past Aboriginal people’s activities. Scatter sites usually contain stone artefacts, but other material such as charcoal, animal bone, shell and ochre may also be present. No two surface scatters are the same.\r\nWhere are Aboriginal surface scatters found?\r\nSurface scatters can be found wherever Aboriginal occupation has occurred in the past.\r\nAboriginal campsites were most frequently located near a reliable source of fresh water, so surface scatters are often found near rivers or streams where erosion or disturbance has exposed an older land surface.\r\n', 'Document', 'uploads/bb6de9e9f86b448e80a31e211d94a1af.png', 'uploads/e6c0ae6ea0d841d58d1b703de0704d15.pdf', '', 'Unknown', 'Under Assessment', 'PDF document', '2026-06-17', '2026-06-11'),
('I013', 'C003', 'Guidelines for conducting and reporting on Aboriginal cultural heritage investigations', 'These guidelines have been prepared to assist in carrying out Aboriginal cultural heritage investigations and preparing Aboriginal cultural heritage reports (other than Cultural Heritage Management Plans (CHMPs), such as:\r\n\r\ngeneral heritage studies; regional surveys; salvage excavations and systematic surface collections; research projects; conservation and management plans; due diligence reports, heritage impact assessments, preliminary Aboriginal heritage tests (PAHTs), Aboriginal cultural heritage land management agreements and surveys for Aboriginal cultural heritage (as defined under section 4 of the Aboriginal Heritage Act 2006 (the Act)). \r\n', 'Document', 'uploads/323cc3425da945dda965a933c530faad.jpg', 'uploads/c1898a87ffe847a8af70c3a2bb1d407f.docx', '', 'Other / Not listed', 'Approved', 'Word document', '2026-06-17', '2026-06-17'),
('I014', 'C003', 'Stone structures in southwestern Victoria', 'Aboriginal stone structures in southwestern Victoria\r\n\r\nIn reading Chamber’s tract on ‘the Monuments of unrecorded Ages,’ I was startled by the assertion that ‘stone circles’ were numerous in Victoria.  I made what enquiries I could here, and all replies confirmed my own impression that no Australian tribe had ever been known to raise such a structure, or any other of monumental character.  But I myself not infrequently found the ‘native ovens’ crowned with the ring of small stones wherein the fires had formerly been lighted, and it seems to me that an unpractised observer…might have called these ‘stone circles’…I then asked enlightenment from the…Secretary for Mines [R.B. Smyth], who, I thought, might as Secretary to the Aborigines Protection Board, be able to obtain some positive information.  Instead of giving that, he suggested that the ‘stone circles’ are natural piles of basaltic rock, which appears to me an eminently unsatisfactory theory (R.E. Johns to P. Chauncy 6/2/1873 in Phillip Chauncy Papers SLV MS 9287/72, Box 1036; See also Griffith 1996: 40-41 and Russell and McNiven 1998 for a discussion of these letters).\r\n', 'Document', 'uploads/a0cf5d17a54e4667a20f12f5940244ec.jpg', 'uploads/cd64c03e230e4ed1b344e42323eda0f7.doc', 'southwestern Victoria', 'Not yet assessed', 'Approved', 'Word document', '2026-06-17', '2026-06-10'),
('I015', 'C001', 'AIATSIS Thesauri Places', 'An international standard, the AIATSIS Thesauri was accepted by the Library of Congress to use in bibliographic records world-wide. Library of Congress Subject Headings, an international standard for subject analysis in the library and Information sector is deficient in the field of Australian Aboriginal and Torres Strait Islander studies, cultures, histories, languages, and places. The AIATSIS Thesauri was developed to address this gap.', 'Document', 'img/placeholder.png', 'uploads/3814fbd5cb3b4c83ac0a8ebdc7366a60.csv', '', 'Other / Not listed', 'Approved', 'Spreadsheet', '2026-06-17', '2026-06-16'),
('I016', 'C001', 'AIATSIS Thesauri Topical', 'An international standard, the AIATSIS Thesauri was accepted by the Library of Congress to use in bibliographic records world-wide. Library of Congress Subject Headings, an international standard for subject analysis in the library and Information sector is deficient in the field of Australian Aboriginal and Torres Strait Islander studies, cultures, histories, languages, and places. The AIATSIS Thesauri was developed to address this gap.', 'Document', 'img/placeholder.png', 'uploads/22d3d43f983a486eb2b07af442a98781.csv', '', 'Other / Not listed', 'Approved', 'Spreadsheet', '2026-06-17', '2026-06-15');

-- --------------------------------------------------------

--
-- Table structure for table `culturalmetadata`
--

CREATE TABLE `culturalmetadata` (
  `metadataID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `itemID` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `itemHandling` text COLLATE utf8mb4_unicode_ci,
  `ownership` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `accessLevel` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `recommendedAccessLevel` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `culturalSensitivity` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `culturalNotes` text COLLATE utf8mb4_unicode_ci,
  `accessConditions` text COLLATE utf8mb4_unicode_ci,
  `communityApprovalStatus` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `culturalmetadata`
--

INSERT INTO `culturalmetadata` (`metadataID`, `itemID`, `itemHandling`, `ownership`, `accessLevel`, `recommendedAccessLevel`, `culturalSensitivity`, `culturalNotes`, `accessConditions`, `communityApprovalStatus`) VALUES
('M001', 'I001', '', 'Community owned', 'Public', NULL, 'Low', '', '', 'Approved'),
('M002', 'I002', '', 'Community owned', 'Restricted', NULL, 'Medium', '', '', 'Approved'),
('M003', 'I003', '', 'Individual owned', 'Private', NULL, 'High', '', '', 'Approved'),
('M004', 'I004', '', 'Community owned', 'Public', NULL, 'Low', 'What should you do if you find \r\na flaked stone tool?\r\nDo not remove any material from the \r\narea. If you pick up a stone to examine \r\nit, make sure that you put it back \r\nwhere it came from. Check whether it \r\nhas some of the key characteristics. \r\nRecord the location, noting roughly \r\nhow many stones there are. Note \r\nwhether the area is under threat of \r\ndisturbance.\r\nPlease help to preserve Aboriginal \r\ncultural places by reporting their \r\npresence to First Peoples – State \r\nRelations.\r\n', '', 'Approved'),
('M005', 'I005', '', '', 'Public', NULL, 'Not yet assessed', '', '', 'Approved'),
('M006', 'I006', '', 'Community owned', 'Public', NULL, 'Not yet assessed', 'What if you find an Aboriginal grinding stone?\r\nDo not disturb it or remove it from the site. Check whether the stone has the typical characteristics of an Aboriginal grinding stone. If it does, record its location and write a brief description of its condition. Note whether it is under threat of disturbance.\r\nPlease help to preserve Aboriginal cultural places by reporting their presence to First Peoples – State Relations.\r\n', '', 'Approved'),
('M007', 'I007', '', '', 'Restricted', NULL, 'Not yet assessed', '', '', 'Approved'),
('M008', 'I008', '', 'Individual owned', 'Public', NULL, 'Not yet assessed', '', '', 'Approved'),
('M009', 'I009', '', '', 'Public', NULL, 'Low', '', '', 'Approved'),
('M010', 'I010', '', '', 'Restricted', NULL, 'Not yet assessed', '', '', 'Approved'),
('M011', 'I011', '', 'Organisation owned', 'Restricted', NULL, 'Medium', '', '', 'Approved'),
('M012', 'I012', NULL, NULL, 'Under Assessment', NULL, 'Not yet assessed', NULL, NULL, 'Under Assessment'),
('M013', 'I013', '', 'Unknown', 'Public', NULL, 'Not yet assessed', '', '', 'Approved'),
('M014', 'I014', '', 'Community owned', 'Restricted', NULL, 'Medium', '', '', 'Approved'),
('M015', 'I015', '', '', 'Public', NULL, 'Not yet assessed', '', '', 'Approved'),
('M016', 'I016', '', 'Unknown', 'Public', NULL, 'Not yet assessed', '', '', 'Approved');

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
('U001', '31', NULL, 'Wayne Stack', 'wayne@technetik.com.au', 'scrypt:32768:8:1$mU0g8vWcA2a9aQbZ$1700240d81081e5c7b20b04067aa2ef6e2bc514a0fcfc67b0e377a968ddc834800986fdd63b612a53a14b77833b35f54588ca84f616f6fb3a2f27a2d2d9dd86d'),
('U002', '3', 'Uncle', 'Theodore Stack', 'here@there.com.au', 'scrypt:32768:8:1$4DXOjKGuBMImvRms$5dfa73e698985df9d4b972b66b88281c4e4a4ea960aa701c65490a45d480c6cd8dd486570dccf68880911679733b6719d8b6d1cddc811f593492d42a494d1e2f'),
('U003', '15', 'Dr.', 'Charles Montgomery Stack', 'there@here.com', 'scrypt:32768:8:1$qqzgQJfLkRKfts7l$943096b5e0b361359c00c3570c67cc9ea4157e750ce30c420d9e1a25897bc369901c956fac1b5af54176a117ca9acb6863eab24a245a731a5d52ccd121e6da5b');

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
-- Indexes for table `assessmentcomment`
--
ALTER TABLE `assessmentcomment`
  ADD PRIMARY KEY (`commentID`),
  ADD KEY `idx_assessmentcomment_assessment` (`itemID`),
  ADD KEY `idx_assessmentcomment_reviewer` (`userID`);

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
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`roleID`),
  ADD UNIQUE KEY `roleID` (`roleID`),
  ADD UNIQUE KEY `name` (`name`);

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
