CREATE DATABASE LibraryManagement;
GO
USE LibraryManagement;
GO

CREATE TABLE Users (
    UserID CHAR(10) PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(50),
    FullName VARCHAR(50),
    Role VARCHAR(10) NOT NULL
        CHECK (Role IN ('Member', 'Admin'))
);

CREATE TABLE Book (
    BookID CHAR(10) PRIMARY KEY,
    Title VARCHAR(100) NOT NULL,
    Author VARCHAR(100),
    ISBN VARCHAR(20),
    Category VARCHAR(50),
    TotalCopies INT NOT NULL CHECK (TotalCopies >= 0),
    AvailableCopies INT NOT NULL CHECK (AvailableCopies >= 0)
);

CREATE TABLE BorrowRecord (
    BorrowID CHAR(10) PRIMARY KEY,
    UserID CHAR(10) NOT NULL,
    BookID CHAR(10) NOT NULL,
    BorrowDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    Status VARCHAR(20),

    CONSTRAINT FK_Borrow_User
        FOREIGN KEY (UserID) REFERENCES Users(UserID),

    CONSTRAINT FK_Borrow_Book
        FOREIGN KEY (BookID) REFERENCES Book(BookID)
);

CREATE TABLE Fine (
    FineID CHAR(10) PRIMARY KEY,
    BorrowID CHAR(10) NOT NULL,
    Amount DECIMAL(10,2) NOT NULL CHECK (Amount >= 0),
    Status VARCHAR(20),

    CONSTRAINT FK_Fine_Borrow
        FOREIGN KEY (BorrowID) REFERENCES BorrowRecord(BorrowID)
);

