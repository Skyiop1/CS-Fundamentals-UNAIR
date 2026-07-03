Prompt kemarin **cukup untuk sekali generate**, tapi untuk project yang panjang sampai Bab 9–11, lebih aman pakai **system instructions**. Prompt itu seperti “suruhan sekali jalan”, sedangkan system instruction itu seperti **konstitusi project**: Codex jadi punya pegangan tetap soal scope, stack, fitur, style UI, database, route, dan deployment.

Aku buatkan versi yang lebih rapi, mengikuti gaya file NusaCarbon yang punya struktur project overview, tech stack, actors, navigation/routes, screen specs, data model, dan deployment notes  . Isinya juga tetap disesuaikan dengan laporanmu yang memang memakai Laravel, Bootstrap, MySQL, GitHub, Railway, dan web browser , serta aktor Admin dan Anggota sesuai laporan .

Copy ini sebagai **system instruction utama untuk Codex**:

````md
# System Instructions: Sistem Informasi Perpustakaan Berbasis Web
# Laravel + MySQL + Railway Deployment

## Project Overview

Build a complete web-based library information system for an academic project titled:

**Sistem Informasi Peminjaman Buku Perpustakaan Berbasis Web**

The system is designed to help library staff and members manage book borrowing activities digitally. The application must support book catalog management, member management, borrowing requests, borrowing approval, return processing, automatic late fine calculation, transaction history, and simple reporting.

The project must be implemented as a real deployable web application, not just a static mockup. The final website must be ready to deploy on Railway using MySQL database and must be suitable for documentation in Bab 9, Bab 10, and Bab 11 of the academic report.

---

## Core Objective

The main objective is to transform manual library borrowing processes into a structured web-based information system.

The system must help:

1. Admin manage book data.
2. Admin manage member data.
3. Members browse and search the book catalog.
4. Members submit borrowing requests.
5. Admin approve or reject borrowing requests.
6. Admin process book returns.
7. The system calculate late fines automatically.
8. Admin view transaction history and reports.
9. The final application be deployed online using Railway.

---

## Tech Stack

Use the following technology stack:

| Layer | Technology |
|---|---|
| Backend | Laravel |
| Frontend | Blade Templates |
| Styling | Bootstrap 5, custom CSS |
| Database | MySQL |
| Authentication | Laravel authentication with simple role-based access |
| Version Control | Git and GitHub |
| Deployment | Railway |
| Domain | Railway domain or custom domain |
| Local Development | Laravel local server / XAMPP / Laragon if needed |
| Documentation | Screenshots for Bab 9, Bab 10, and Bab 11 |

Do not use React, Next.js, Vue, or Vercel for this project unless explicitly requested later.

---

## Main Roles / Actors

The system has two main actors:

### 1. Admin

Admin is the library staff or system manager. Admin has full access to manage library data and transactions.

Admin can:

- Login to the system.
- Access admin dashboard.
- Manage book data.
- Manage book categories.
- Manage member data.
- View borrowing requests.
- Approve or reject borrowing requests.
- Process book returns.
- View late fines.
- View borrowing history.
- View simple reports.
- Logout.

### 2. Anggota

Anggota is a registered library member. Anggota has limited access to library services.

Anggota can:

- Register an account.
- Login to the system.
- Access member dashboard.
- View book catalog.
- Search books by title, author, or category.
- View book details and stock availability.
- Submit borrowing request.
- View borrowing status.
- View borrowing history.
- View late fine information.
- Logout.

---

## Scope Priority

Prioritize the core book borrowing system first.

### Must-have modules

1. Authentication and role-based access.
2. Admin dashboard.
3. Member dashboard.
4. Book management.
5. Category management.
6. Member management.
7. Book catalog.
8. Book search.
9. Borrowing request.
10. Borrowing approval.
11. Book return.
12. Automatic late fine calculation.
13. Transaction history.
14. Simple reports.
15. Railway deployment preparation.

### Optional module

Room or facility borrowing may be added only after all core book borrowing features are complete and working.

If the optional room borrowing feature is added, keep it simple:
- Room list.
- Room borrowing request.
- Admin approval.
- Room borrowing history.

Do not let the optional room borrowing module disrupt the main book borrowing system.

---

## Functional Requirements

### Authentication

Build real login and registration using database users.

Requirements:

- Users can login using email and password.
- Passwords must be hashed.
- Each user has a role: `admin` or `anggota`.
- After login, redirect user based on role:
  - Admin → `/admin/dashboard`
  - Anggota → `/dashboard`
- Prevent Anggota from accessing Admin pages.
- Prevent unauthenticated users from accessing protected pages.
- Provide logout functionality.

Seed at least:

- One admin account.
- One sample anggota account.

---

## Admin Features

### Admin Dashboard

Show summary cards:

- Total books.
- Total members.
- Active borrowings.
- Pending borrowing requests.
- Late returns.
- Total fines.

Also show recent borrowing transactions.

---

### Book Management

Admin can:

- View book list.
- Add new book.
- Edit book.
- Delete book.
- Search/filter books.
- Manage book stock.

Book fields:

- Book code.
- Title.
- Author.
- Publisher.
- Category.
- Publication year.
- Stock.
- Description.
- Cover image URL or placeholder image.

Validation:

- Book code must be unique.
- Title is required.
- Stock must be numeric and cannot be negative.

---

### Category Management

Admin can:

- View categories.
- Add category.
- Edit category.
- Delete category.

Category fields:

- Category name.
- Description.

---

### Member Management

Admin can:

- View member list.
- Add member manually.
- Edit member data.
- Delete or deactivate member.
- View member borrowing history.

Member fields:

- Member number.
- Name.
- Email.
- Phone number.
- Address.
- Status: active or inactive.

---

### Borrowing Request Management

Admin can:

- View all borrowing requests.
- Filter by status: pending, approved, rejected, borrowed, returned, late.
- Approve borrowing request.
- Reject borrowing request.

When admin approves a request:

- Borrowing status becomes `approved` or `borrowed`.
- Book stock decreases.
- Borrow date is set to approval date.
- Due date is automatically set to 7 days after borrow date.

When admin rejects a request:

- Borrowing status becomes `rejected`.
- Book stock does not change.

---

### Return Processing

Admin can:

- View active borrowings.
- Process book return.
- Confirm return date.
- Let the system calculate late days and fine automatically.
- Mark borrowing as returned.
- Increase book stock after return.

Fine formula:

```text
late_days = max(0, return_date - due_date)
fine_amount = late_days × 1000
````

Use IDR format for fine display:

```text
Rp 1.000
Rp 5.000
Rp 10.000
```

---

### Reports

Admin can view simple reports:

* Borrowing transaction history.
* Late return list.
* Fine list.
* Most borrowed books.
* Active members.
* Monthly borrowing summary.

Reports do not need complex charts. Tables and summary cards are enough.

---

## Anggota Features

### Member Dashboard

Show:

* Total active borrowings.
* Pending requests.
* Returned books.
* Total unpaid fines.
* Recent borrowing history.

---

### Book Catalog

Anggota can:

* View all available books.
* Search books by title, author, or category.
* Filter by category.
* View book detail.
* See stock availability.

Catalog UI:

* Use card-based layout.
* Show book title, author, category, stock, and button to view details.
* Use formal academic and clean visual style.

---

### Book Detail

Show:

* Book cover placeholder.
* Title.
* Author.
* Publisher.
* Category.
* Publication year.
* Stock.
* Description.
* Borrow button.

Borrow button behavior:

* If stock > 0, allow borrowing request.
* If stock = 0, disable borrow button and show “Stok tidak tersedia”.

---

### Borrowing Request

Anggota can submit borrowing request.

Rules:

* A member cannot borrow the same book twice if the previous borrowing is still active.
* A member cannot submit a request if book stock is zero.
* Request status starts as `pending`.
* Admin must approve before borrowing becomes active.

---

### My Borrowings

Anggota can view:

* Pending requests.
* Approved/borrowed books.
* Returned books.
* Rejected requests.
* Due date.
* Late status.
* Fine amount if late.

---

## Database Design

Create Laravel migrations for the following tables:

### 1. roles

Fields:

* id
* name
* description
* timestamps

Default values:

* admin
* anggota

---

### 2. users

Fields:

* id
* role_id
* name
* email
* password
* phone
* address
* status
* timestamps

Relationships:

* User belongs to Role.
* User may have one Member profile.
* User may have many Borrowings.

---

### 3. members

Fields:

* id
* user_id
* member_number
* name
* phone
* address
* status
* timestamps

Relationships:

* Member belongs to User.
* Member has many Borrowings.

---

### 4. categories

Fields:

* id
* name
* description
* timestamps

Relationships:

* Category has many Books.

---

### 5. books

Fields:

* id
* category_id
* book_code
* title
* author
* publisher
* publication_year
* stock
* description
* cover_image
* timestamps

Relationships:

* Book belongs to Category.
* Book has many BorrowingDetails.

---

### 6. borrowings

Fields:

* id
* member_id
* status
* request_date
* approved_at
* borrowed_at
* due_date
* returned_at
* rejected_reason
* timestamps

Status values:

* pending
* approved
* rejected
* borrowed
* returned
* late

Relationships:

* Borrowing belongs to Member.
* Borrowing has many BorrowingDetails.
* Borrowing has one Return record.
* Borrowing has one Fine record.

---

### 7. borrowing_details

Fields:

* id
* borrowing_id
* book_id
* quantity
* timestamps

Relationships:

* BorrowingDetail belongs to Borrowing.
* BorrowingDetail belongs to Book.

For MVP, quantity can be fixed to 1.

---

### 8. returns

Fields:

* id
* borrowing_id
* return_date
* condition_note
* processed_by
* timestamps

Relationships:

* Return belongs to Borrowing.
* Return processed by Admin user.

---

### 9. fines

Fields:

* id
* borrowing_id
* late_days
* amount
* status
* paid_at
* timestamps

Status values:

* unpaid
* paid

Relationships:

* Fine belongs to Borrowing.

---

## Laravel Routes

Use Laravel web routes, not REST API-only architecture.

### Public Routes

```php
GET     /
GET     /login
POST    /login
GET     /register
POST    /register
POST    /logout
```

### Admin Routes

```php
GET     /admin/dashboard

GET     /admin/books
GET     /admin/books/create
POST    /admin/books
GET     /admin/books/{book}
GET     /admin/books/{book}/edit
PUT     /admin/books/{book}
DELETE  /admin/books/{book}

GET     /admin/categories
POST    /admin/categories
GET     /admin/categories/{category}/edit
PUT     /admin/categories/{category}
DELETE  /admin/categories/{category}

GET     /admin/members
GET     /admin/members/create
POST    /admin/members
GET     /admin/members/{member}
GET     /admin/members/{member}/edit
PUT     /admin/members/{member}
DELETE  /admin/members/{member}

GET     /admin/borrowings
GET     /admin/borrowings/{borrowing}
PUT     /admin/borrowings/{borrowing}/approve
PUT     /admin/borrowings/{borrowing}/reject

GET     /admin/returns
POST    /admin/returns/{borrowing}

GET     /admin/fines
PUT     /admin/fines/{fine}/mark-paid

GET     /admin/reports
GET     /admin/reports/borrowings
GET     /admin/reports/late-returns
```

### Anggota Routes

```php
GET     /dashboard

GET     /catalog
GET     /catalog/{book}

POST    /borrowings/request/{book}
GET     /my-borrowings
GET     /my-borrowings/{borrowing}

GET     /profile
PUT     /profile
```

---

## Controllers

Create these controllers:

```text
AuthController
AdminDashboardController
MemberDashboardController
BookController
CategoryController
MemberController
CatalogController
BorrowingController
ReturnController
FineController
ReportController
ProfileController
```

Keep controller logic clean and readable.

Use validation for form requests.

---

## Models and Relationships

Create Eloquent models:

```text
Role
User
Member
Category
Book
Borrowing
BorrowingDetail
BookReturn
Fine
```

Use clear relationships:

```php
User belongsTo Role
User hasOne Member

Member belongsTo User
Member hasMany Borrowing

Category hasMany Book
Book belongsTo Category

Borrowing belongsTo Member
Borrowing hasMany BorrowingDetail
Borrowing hasOne BookReturn
Borrowing hasOne Fine

BorrowingDetail belongsTo Borrowing
BorrowingDetail belongsTo Book

BookReturn belongsTo Borrowing
Fine belongsTo Borrowing
```

---

## UI/UX Direction

The UI must look formal, academic, clean, and comfortable to read.

Use:

* Bootstrap 5.
* White background.
* Soft gray sections.
* Blue/slate primary color.
* Clean cards.
* Clear table layout.
* Status badges.
* Responsive layout.

Avoid overly flashy design.

### Admin Layout

Use:

* Sidebar navigation.
* Top navbar.
* Dashboard cards.
* Data tables.
* Action buttons.
* Modal or form pages for create/edit.

Sidebar menus:

* Dashboard
* Data Buku
* Kategori
* Data Anggota
* Peminjaman
* Pengembalian
* Denda
* Laporan
* Logout

### Anggota Layout

Use:

* Top navbar.
* Card-based dashboard.
* Catalog card layout.
* Search bar.
* Borrowing status cards/table.
* Profile page.

Navbar menus:

* Dashboard
* Katalog Buku
* Peminjaman Saya
* Profil
* Logout

---

## Status Badge Rules

Use badges consistently:

```text
pending   → yellow / warning
approved  → blue / info
borrowed  → primary
returned  → green / success
rejected  → red / danger
late      → red / danger
paid      → green / success
unpaid    → yellow / warning
```

---

## Seeders

Create seeders for:

1. Roles.
2. Admin user.
3. Sample Anggota user.
4. Categories.
5. Books.
6. Sample borrowing transactions if useful.

Default accounts:

```text
Admin:
email: admin@perpus.test
password: password

Anggota:
email: anggota@perpus.test
password: password
```

---

## Railway Deployment Requirements

Prepare the project so it can be deployed to Railway.

Requirements:

* Use `.env.example`.
* Use MySQL environment variables.
* Make sure `APP_KEY` can be generated.
* Make sure migrations can run.
* Make sure seeders can run.
* Make sure public assets are accessible.
* Make sure storage link is handled if image upload is used.
* Use GitHub repository as deployment source.
* Prepare README deployment guide.

Do not hardcode database credentials.

---

## README Requirements

Create a `README.md` that explains:

1. Project title.
2. Project description.
3. Features.
4. Tech stack.
5. User roles.
6. Database tables.
7. Local installation steps.
8. Railway deployment steps.
9. Environment variables.
10. Demo account.
11. GitHub repository link placeholder.
12. Railway demo link placeholder.
13. Custom domain placeholder.
14. Screenshots placeholder.

Use this placeholder format:

```text
GitHub Repository:
https://github.com/username/repository-name

Demo Website:
https://your-project.up.railway.app

Custom Domain:
https://yourdomain.com
```

---

## Documentation Screenshot Targets

The project should be easy to document for Bab 9, Bab 10, and Bab 11.

Prepare screens suitable for screenshots:

### Bab 9 UI/UX

* Login page.
* Admin dashboard.
* Anggota dashboard.
* Book catalog.
* Book detail.
* Borrowing request page.
* Admin borrowing approval page.
* Return processing page.
* Report page.

### Bab 10 Implementation

* Laravel folder structure.
* Migration files.
* Model relationship code.
* Route file.
* Controller code.
* Blade views.
* Database table screenshot.
* Feature testing screenshot.

### Bab 11 Deployment

* GitHub repository.
* Railway project dashboard.
* Railway MySQL service.
* Environment variables.
* Successful deployment log.
* Public Railway URL.
* Custom domain setup.
* Final website accessed through browser.

---

## Development Rules

Follow these rules:

1. Build a working MVP first.
2. Do not overcomplicate the system.
3. Keep code readable for academic explanation.
4. Use simple Laravel conventions.
5. Prefer Blade and Bootstrap over complex frontend frameworks.
6. Use real database authentication.
7. Use role-based middleware.
8. Use clear validation messages.
9. Use clean route names.
10. Use Eloquent relationships properly.
11. Make the system deployable.
12. Keep optional room borrowing separate from core book borrowing.
13. Do not create Bab 9–11 report outline unless explicitly requested.
14. Do not switch to Vercel, Aiven, React, or Next.js unless explicitly requested later.

---

## Expected Final Output

The final project should include:

1. Complete Laravel application.
2. Database migrations.
3. Seeders.
4. Models and relationships.
5. Controllers.
6. Blade views.
7. Bootstrap-based UI.
8. Authentication.
9. Role-based access.
10. Book CRUD.
11. Member CRUD.
12. Catalog and search.
13. Borrowing request workflow.
14. Admin approval workflow.
15. Return workflow.
16. Automatic fine calculation.
17. Reports.
18. README.
19. Railway deployment readiness.

The final application must be clean, functional, easy to explain, and aligned with the academic report.
