DROP DATABASE IF EXISTS winhanganha_archive;
CREATE DATABASE winhanganha_archive CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE winhanganha_archive;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Approval;
DROP TABLE IF EXISTS AccessRequest;
DROP TABLE IF EXISTS AssessmentComment;
DROP TABLE IF EXISTS AssessmentRecord;
DROP TABLE IF EXISTS CulturalMetadata;
DROP TABLE IF EXISTS CollectionItem;
DROP TABLE IF EXISTS Collection;
DROP TABLE IF EXISTS Reviewer;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE Reviewer (
    reviewerID VARCHAR(10) NOT NULL,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL,
    role VARCHAR(100) NOT NULL,
    authorisationStatus VARCHAR(50) NOT NULL,
    PRIMARY KEY (reviewerID),
    UNIQUE KEY uq_reviewer_email (email)
) ENGINE=InnoDB;

CREATE TABLE Collection (
    collectionID VARCHAR(10) NOT NULL,
    collectionName VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY (collectionID),
    UNIQUE KEY uq_collection_name (collectionName)
) ENGINE=InnoDB;

CREATE TABLE CollectionItem (
    itemID VARCHAR(20) NOT NULL,
    collectionID VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    itemType VARCHAR(100) NOT NULL,
    imagePath VARCHAR(255) NOT NULL DEFAULT 'img/placeholder.png',
    place VARCHAR(150),
    languageGroup VARCHAR(150),
    status VARCHAR(50) NOT NULL,
    format VARCHAR(100),
    dateAdded DATE,
    dateRecorded VARCHAR(50),
    PRIMARY KEY (itemID),
    KEY idx_collectionitem_collection (collectionID),
    KEY idx_collectionitem_title (title),
    KEY idx_collectionitem_status (status),
    CONSTRAINT fk_collectionitem_collection
        FOREIGN KEY (collectionID) REFERENCES Collection(collectionID)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE CulturalMetadata (
    metadataID VARCHAR(20) NOT NULL,
    itemID VARCHAR(20) NOT NULL,
    ownership VARCHAR(150) NOT NULL,
    accessLevel VARCHAR(50) NOT NULL,
    culturalSensitivity VARCHAR(50) NOT NULL,
    handlingNotes TEXT NOT NULL,
    communityApprovalStatus VARCHAR(100) NOT NULL,
    PRIMARY KEY (metadataID),
    UNIQUE KEY uq_culturalmetadata_item (itemID),
    KEY idx_culturalmetadata_access (accessLevel),
    CONSTRAINT fk_culturalmetadata_item
        FOREIGN KEY (itemID) REFERENCES CollectionItem(itemID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE AssessmentRecord (
    assessmentID VARCHAR(20) NOT NULL,
    itemID VARCHAR(20) NOT NULL,
    reviewerID VARCHAR(10) NOT NULL,
    assessmentDate DATE NOT NULL,
    assessmentOutcome VARCHAR(150) NOT NULL,
    notes TEXT NOT NULL,
    PRIMARY KEY (assessmentID),
    KEY idx_assessmentrecord_item (itemID),
    KEY idx_assessmentrecord_reviewer (reviewerID),
    CONSTRAINT fk_assessmentrecord_item
        FOREIGN KEY (itemID) REFERENCES CollectionItem(itemID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_assessmentrecord_reviewer
        FOREIGN KEY (reviewerID) REFERENCES Reviewer(reviewerID)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE AssessmentComment (
    commentID VARCHAR(20) NOT NULL,
    assessmentID VARCHAR(20) NOT NULL,
    reviewerID VARCHAR(10) NOT NULL,
    commentText TEXT NOT NULL,
    commentDate DATE NOT NULL,
    PRIMARY KEY (commentID),
    KEY idx_assessmentcomment_assessment (assessmentID),
    KEY idx_assessmentcomment_reviewer (reviewerID),
    CONSTRAINT fk_assessmentcomment_assessment
        FOREIGN KEY (assessmentID) REFERENCES AssessmentRecord(assessmentID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_assessmentcomment_reviewer
        FOREIGN KEY (reviewerID) REFERENCES Reviewer(reviewerID)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE AccessRequest (
    requestID VARCHAR(20) NOT NULL,
    itemID VARCHAR(20) NOT NULL,
    requesterName VARCHAR(150) NOT NULL,
    requesterEmail VARCHAR(255) NOT NULL,
    requestDate DATE NOT NULL,
    requestStatus VARCHAR(50) NOT NULL DEFAULT 'Pending',
    purpose TEXT NOT NULL,
    PRIMARY KEY (requestID),
    KEY idx_accessrequest_item (itemID),
    KEY idx_accessrequest_status (requestStatus),
    CONSTRAINT fk_accessrequest_item
        FOREIGN KEY (itemID) REFERENCES CollectionItem(itemID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Approval (
    approvalID VARCHAR(20) NOT NULL,
    requestID VARCHAR(20) NOT NULL,
    reviewerID VARCHAR(10) NOT NULL,
    approvalDate DATE NOT NULL,
    approvalStatus VARCHAR(50) NOT NULL,
    approvalNotes TEXT NOT NULL,
    PRIMARY KEY (approvalID),
    UNIQUE KEY uq_approval_request (requestID),
    KEY idx_approval_reviewer (reviewerID),
    CONSTRAINT fk_approval_request
        FOREIGN KEY (requestID) REFERENCES AccessRequest(requestID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_approval_reviewer
        FOREIGN KEY (reviewerID) REFERENCES Reviewer(reviewerID)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

INSERT INTO Reviewer (reviewerID, name, email, role, authorisationStatus) VALUES
('R001', 'Aunty May Williams', 'may.williams@fnwa.org', 'Elder reviewer', 'Authorised'),
('R002', 'Daniel Brooks', 'd.brooks@fnwa.org', 'Library archivist', 'Authorised'),
('R003', 'Leah Morgan', 'leah.morgan@fnwa.org', 'Collection manager', 'Authorised'),
('R004', 'Uncle Robert Evans', 'robert.evans@fnwa.org', 'Community representative', 'Authorised');

INSERT INTO Collection (collectionID, collectionName, description) VALUES
('C001', 'Language Resources', 'Language records, word lists and place-name materials'),
('C002', 'Oral Histories', 'Recorded community stories and interviews'),
('C003', 'Historical Records', 'Images, documents and archival records');

INSERT INTO CollectionItem (itemID, collectionID, title, description, itemType, imagePath, place, languageGroup, status, format, dateAdded, dateRecorded) VALUES
('I001', 'C001', 'Wiradjuri Language Word List', 'Sample language resource with cultural notes', 'Language Record', 'img/placeholder.png', 'Central NSW', 'Wiradjuri', 'Awaiting Review', 'Digitised text record', '2026-05-20', NULL),
('I002', 'C002', 'Community Oral History Recording', 'Recorded interview about family memory and place', 'Audio', 'img/placeholder.png', 'Northern NSW', 'Bundjalung', 'Restricted', 'Audio recording', '2026-05-21', NULL),
('I003', 'C003', 'Mission Station Photograph', 'Digitised historical photograph with provenance notes', 'Image', 'img/placeholder.png', 'Queensland', 'Multiple communities', 'Approved', 'Digitised image', '2026-05-21', NULL),
('I004', 'C002', 'Ceremony Reference Record', 'A culturally sensitive record held for assessment before any public description or access decision is made.', 'Audio transcript and cultural note', 'img/placeholder.png', 'Central West New South Wales', 'Wiradjuri', 'Under Review', 'Audio transcript and cultural note', NULL, '1985'),
('I005', 'C003', 'Community Meeting Notes', 'Digitised notes from a community consultation meeting about cultural care, access conditions and description.', 'Document', 'img/placeholder.png', NULL, NULL, 'Private', 'Digitised document', '2026-05-22', NULL),
('I006', 'C001', 'Place Name Record', 'A record connecting language, Country, place names and approved cultural description.', 'Place Record', 'img/placeholder.png', NULL, NULL, 'Restricted', 'Text record', '2026-05-22', NULL);

INSERT INTO CulturalMetadata (metadataID, itemID, ownership, accessLevel, culturalSensitivity, handlingNotes, communityApprovalStatus) VALUES
('M001', 'I001', 'Community held', 'Under Review', 'Medium', 'Requires Elder confirmation before public release', 'Awaiting review'),
('M002', 'I002', 'Family and community held', 'Restricted', 'High', 'Do not reproduce without permission', 'Access request required'),
('M003', 'I003', 'Library collection', 'Public', 'Low', 'Use with acknowledgement', 'Approved'),
('M004', 'I004', 'Community held', 'Under Review', 'High', 'Item may contain references to restricted knowledge. Confirm whether names, places and descriptive terms can be shown in the public catalogue.', 'Awaiting Elder review'),
('M005', 'I005', 'Community consultation record', 'Private', 'High', 'Contains internal consultation material and community decision-making context. Not available for public release.', 'Not approved for public release'),
('M006', 'I006', 'Community held', 'Restricted', 'Medium', 'Contains place-based knowledge and language information. Access to detailed place data requires approval.', 'Approved with restrictions');

INSERT INTO AssessmentRecord (assessmentID, itemID, reviewerID, assessmentDate, assessmentOutcome, notes) VALUES
('A001', 'I001', 'R001', '2026-05-20', 'Continue review', 'Language spelling and access notes require confirmation'),
('A002', 'I002', 'R001', '2026-05-21', 'Restricted access', 'Recording contains family knowledge and should not be public'),
('A003', 'I003', 'R003', '2026-05-22', 'Public release approved', 'Description and access conditions approved'),
('A004', 'I004', 'R001', '2026-05-21', 'Continue review', 'Confirm whether item can be released with restricted access or must remain private.'),
('A005', 'I005', 'R003', '2026-05-22', 'Keep private', 'Internal consultation material should remain private.'),
('A006', 'I006', 'R002', '2026-05-22', 'Restricted access', 'Detailed place data requires approval before access.');

INSERT INTO AssessmentComment (commentID, assessmentID, reviewerID, commentText, commentDate) VALUES
('AC001', 'A001', 'R001', 'Confirm wording with language group before release', '2026-05-20'),
('AC002', 'A002', 'R002', 'Access request process should be used for this item', '2026-05-21'),
('AC003', 'A003', 'R003', 'Approved description can be shown on public page', '2026-05-22'),
('AC004', 'A004', 'R001', 'The public record should not include detailed ceremonial references. A shorter description may be suitable if the family names and sensitive place details are removed.', '2026-05-21'),
('AC005', 'A004', 'R004', 'Recommend restricted access until further consultation with the relevant family group has been completed.', '2026-05-22'),
('AC006', 'A004', 'R002', 'Metadata can be updated once the review group confirms the approved access level and public catalogue wording.', '2026-05-23');

INSERT INTO AccessRequest (requestID, itemID, requesterName, requesterEmail, requestDate, requestStatus, purpose) VALUES
('Q001', 'I002', 'Sarah Nguyen', 'sarah.nguyen@example.com', '2026-05-22', 'Pending', 'Research project on oral history preservation'),
('Q002', 'I001', 'Michael Harris', 'michael.harris@example.com', '2026-05-23', 'Pending', 'Teaching resource development'),
('Q003', 'I003', 'Priya Patel', 'priya.patel@example.com', '2026-05-24', 'Approved', 'Class display of public historical image');

INSERT INTO Approval (approvalID, requestID, reviewerID, approvalDate, approvalStatus, approvalNotes) VALUES
('P001', 'Q001', 'R001', '2026-05-24', 'Rejected', 'Item contains restricted family knowledge'),
('P002', 'Q002', 'R001', '2026-05-24', 'Pending', 'Awaiting further community consultation'),
('P003', 'Q003', 'R003', '2026-05-24', 'Approved', 'Public item may be viewed with acknowledgement');
