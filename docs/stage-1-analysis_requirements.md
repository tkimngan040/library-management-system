## 1. Functional Requirements
FR1. The system allows users to log in and use functions according to their assigned permissions.
FR2. The system allows users to search for and view detailed information about books.
FR3. The system allows members to borrow books, return books, and view their borrowing history.
FR4. The system checks the availability/status of books before allowing them to be borrowed.
FR5. The system calculates fines for overdue book returns.
FR6. The system allows administrators to manage books, members, and borrowing–returning records.
FR7. The system stores data and assigns user permissions based on roles.
## 2. Non-Functional Requirements
2.1. Availability
The system interface is simple, intuitive, and user-friendly for both librarians and readers.
The system can be accessed and operates smoothly on both desktop and mobile devices.

2.2. Reliability
The system operates continuously 24/7 with a reliability rate of over 99.9%.
Book, user, and borrowing–returning data are stored securely and will not be lost in the event of system failure.
Database backups are created periodically to ensure data recovery when needed.

2.2. Performance
The system can support up to 3,000 concurrent users.
Supports storing information for more than 50,000 book titles, 100,000 readers, and over 1,000,000 borrowing and returning records.
Page loading and system response time do not exceed 3 seconds under normal operating conditions.

2.3. Security
User passwords are encrypted before being stored in the database.
Each role (Administrator / Member / Guest ) has clearly defined access permissions.
Session management ensures data privacy and prevents unauthorized access.

2.4. Maintainability
The system uses a modular design, allowing easy maintenance, upgrades, and future expansion.
Code and database structures are well-organized to support quick bug fixes and updates.
2.5. Compatibility
The system is compatible with modern web browsers such as Chrome, Edge, and Firefox.
It can run on multiple operating systems including Windows, Linux, and macOS.

2.6. Design Constraints
Technologies used:
Programming language: C++

## 3. Data Flow Diagram
3.1. DFD level 0
<img width="1844" height="1384" alt="image" src="https://github.com/user-attachments/assets/dfc91cf7-512f-4f42-8479-72246fdb2e03" />

3.2. DFD level 1
<img width="3116" height="2484" alt="image" src="https://github.com/user-attachments/assets/aa18cf86-aac9-4ae5-b26b-50f3133572be" />

## 4. Use Case DIAGRAM
<img width="2832" height="3884" alt="image" src="https://github.com/user-attachments/assets/fbf62c16-2822-49ff-b514-a592300522e6" />

4.1. Use Case: Login
Actors: User (Member, Admin)
Summary:
This use case allows the user to log into the system using a valid account.
Pre-condition:
The user has a valid account.
Main Flow:
The system displays the login screen.
The user enters username and password.
The system validates the credentials.
The system grants access based on the user’s role.
Alternative Flow:
If the credentials are invalid, the system displays an error message.
Post-condition:
The user is logged in successfully.

4.2. Use Case: Search Book
Actors: User (Member, Admin)
Summary:
This use case allows the user to search for books in the system.
Pre-condition:
The user is logged in.
Main Flow:
The user enters search criteria (title, author, category).
The system searches the database.
The system displays matching books.
Post-condition:
Search results are displayed.

4.3. Use Case: View Book Details
Actors: User (Member, Admin)
Summary:
This use case allows the user to view detailed information about a book.
Pre-condition:
The user has searched for books.
Main Flow:
The user selects a book.
The system displays book details.
Post-condition:
Book information is shown.

4.4. Use Case: Borrow Book
Actors: Member
Summary:
This use case allows a member to borrow a book from the library.
Pre-condition:
The user is logged in as a Member.
The book exists in the system.
Main Flow:
The member selects a book to borrow.
The system checks availability and borrowing limit.
The system creates a borrow record.
The system updates available copies.
Alternative Flow:
If the book is not available, the system displays a notification.
Post-condition:
The book is borrowed successfully.

4.5. Use Case: Return Book
Actors: Member
Summary:
This use case allows a member to return a borrowed book.
Pre-condition:
The member has borrowed the book.
Main Flow:
The member selects a borrowed book to return.
The system records the return date.
The system updates the book status and availability.
Post-condition:
The book is returned and the record is updated.

4.6. Use Case: View Borrow History
Actors: Member
Summary:
This use case allows a member to view their borrowing history.
Pre-condition:
The member is logged in.
Main Flow:
The member selects “View Borrow History”.
The system retrieves borrow records.
The system displays the history.
Post-condition:
Borrow history is displayed.

4.7. Use Case: Manage Borrow Records
Actors: Admin
Summary:
This use case allows the admin to manage borrowing records.
Pre-condition:
The admin is logged in.
Main Flow:
The admin views all borrow records.
The admin updates record status if needed.
The system saves changes.
Post-condition:
Borrow records are updated.

4.8. Use Case: Manage Members
Actors: Admin
Summary:
This use case allows the admin to manage library members.
Pre-condition:
The admin is logged in.
Main Flow:
The admin views the member list.
The admin adds, updates, or deletes member information.
The system saves changes.
Post-condition:
Member data is updated.

4.9. Use Case: Manage Books
Actors: Admin
Summary:
This use case allows the admin to manage books in the library.
Pre-condition:
The admin is logged in.
Main Flow:
The admin views the book list.
The admin adds, updates, or deletes book information.
The system saves changes.
Post-condition:
Book information is updated.

## 5. Class Diagram
<img width="3508" height="4048" alt="image" src="https://github.com/user-attachments/assets/f7ece9e0-16d3-4464-8f1f-35ec1a755046" />

## 6. DATA BASE
<img width="3044" height="2804" alt="image" src="https://github.com/user-attachments/assets/5d334f5a-9490-4395-b76d-ef5aab79743b" />

















