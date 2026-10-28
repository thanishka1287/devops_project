# ACE ENGINEERING COLLEGE
## ONE-WEEK TECHNICAL PROJECT REPORT

**Project Title:** Dockerized Online Bookstore Using Docker Compose  
**Submitted by:** [Student Name(s)]  
**Roll Number(s):** [Roll Number(s)]  
**Branch and Year:** Department of Computer Science & Engineering / Information Technology, [Year]  
**Academic Year:** 2025–2026  
**Project Duration:** [Start Date] to [End Date] (7 Days)  
**Project Guide / Mentor:** [Mentor Name and Designation]  
**Submitted to:** Department of [Department Name], ACE Engineering College  

---

## TABLE OF CONTENTS

1. Certificate
2. Acknowledgement
3. Abstract
4. Introduction
5. Objectives of the Project
6. Problem Statement and Scope
7. Tools and Technologies Used
8. System Design / Methodology
9. Day-Wise Progress Report
10. Implementation and Results
11. Learning Outcomes
12. Challenges Faced and Solutions
13. Conclusion and Future Scope
14. References
15. Appendices / Supporting Evidence
16. Mentor Evaluation Sheet

---

## 1. CERTIFICATE

This is to certify that **[Student Name(s)]**, bearing Roll Number(s) **[Roll Number(s)]**, of the Department of **[Department and Year]**, ACE Engineering College, has/have successfully completed the one-week technical project entitled:

> **“Dockerized Online Bookstore Using Docker Compose”**

during the period from **[Start Date]** to **[End Date]** at ACE Engineering College, under the guidance and supervision of **[Mentor Name and Designation]**.

<br><br>

___________________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ___________________________________  
**Signature of Project Mentor** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Signature of Head of Department**  
Date: ________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Date: ________________________  
Place: Hyderabad, Telangana

---

## 2. ACKNOWLEDGEMENT

I express my deepest gratitude to our respected Principal and the Management of **ACE Engineering College** for providing the infrastructure, state-of-the-art laboratory facilities, and an encouraging learning atmosphere to carry out this one-week technical project.

I extend my heartfelt thanks to **[Head of Department Name]**, Head of the Department of **[Department Name]**, for their continuous academic support and encouragement throughout the duration of this coursework.

I am immensely indebted to my project guide and mentor, **[Mentor Name and Designation]**, whose constructive feedback, technical guidance, and valuable insights were instrumental in the successful completion of this project on containerization and DevOps workflows.

Finally, I wish to thank my family members, faculty members, and peers who supported me directly and indirectly during the design, implementation, and testing phases of this project.

---

## 3. ABSTRACT

Modern software development demands rapid release cycles and cross-platform consistency. A frequent hurdle in software engineering is environmental drift—commonly termed the *"it works on my machine"* syndrome—where discrepancies between developer machines, testing environments, and production servers result in unexpected runtime crashes and deployment failures.

This project, titled **“Dockerized Online Bookstore Using Docker Compose”**, implements a complete, containerized e-commerce web application engineered to demonstrate core DevOps methodologies. The application is built using a full-stack Python Flask architecture paired with an SQLite relational database, and styled using modern, responsive HTML5, CSS3, and JavaScript. 

To achieve predictable deployments, the application is containerized using **Docker** and orchestrated via **Docker Compose**. A crucial technical focus of this project is **stateful containerization**: while standard container storage is ephemeral, this system attaches a **Docker Named Volume** (`bookstore-data`) to `/app/data`, guaranteeing that database transactions (books catalog, customer orders, and line items) persist across container restarts, teardowns, and rebuilds.

The project incorporates automated quality assurance using **Pytest** (covering 14 comprehensive test cases) and implements a **Continuous Integration (CI)** pipeline via **GitHub Actions** that automatically validates code changes, executes test suites, and verifies Docker image builds on every repository push. The resulting system demonstrates an industry-aligned, reproducible, and resilient software delivery workflow suitable for modern cloud environments.

---

## 4. INTRODUCTION

### 4.1 Background
In traditional deployment workflows, deploying a web application requires manual installation of language interpreters, web servers, third-party libraries, database daemons, and operating system packages. Variations in operating systems (Windows, macOS, Linux distributions) frequently lead to version mismatches, missing dynamic links, and port contention.

**DevOps** bridges the gap between software development (Dev) and IT operations (Ops) by introducing automation, continuous testing, and Infrastructure as Code (IaC). At the heart of modern DevOps is **containerization**—the practice of packaging an application together with all its runtime dependencies, libraries, and system tools into an immutable container image.

### 4.2 Relevance and Motivation
The motivation behind this project is to apply foundational DevOps tools—specifically **Docker**, **Docker Compose**, and **GitHub Actions**—to a tangible, practical web application: an Online Bookstore. 

Rather than working with abstract hello-world containers, this project addresses real-world engineering challenges:
1. **Packaging Application Stacks:** Writing an optimized `Dockerfile` leveraging layer caching, minimal base images (`python:3.11-slim`), and non-root execution.
2. **Multi-Service Orchestration:** Codifying service definitions, port mappings (`5000:5000`), healthcheck probes, and environment variables into a single `docker-compose.yml`.
3. **Data Persistence in Ephemeral Systems:** Overcoming container storage volatility by implementing Docker volumes for database state retention.
4. **Automated Testing & Continuous Delivery:** Guaranteeing code stability via automated test suites executed before and during container builds.

---

## 5. OBJECTIVES OF THE PROJECT

The primary objectives achieved during this one-week technical project are:

1. **Develop a Responsive Full-Stack Web Application:** Build a functional online bookstore using Python Flask, SQLite, and modern HTML/CSS/JavaScript with catalog browsing, search, category filtering, cart management, and order checkout.
2. **Containerize the Web Application with Docker:** Author a production-ready `Dockerfile` following best practices (minimal base image, layer caching, non-privileged user security, and internal health checks).
3. **Orchestrate Deployment Using Docker Compose:** Create a declarative `docker-compose.yml` to start, stop, configure, and inspect the application with a single command (`docker compose up --build`).
4. **Ensure Database Persistence via Docker Named Volumes:** Mount an isolated volume to `/app/data` to guarantee that SQLite records survive container restarts and teardowns.
5. **Implement Automated Testing and Continuous Integration (CI):** Write 14 comprehensive unit and integration tests using `pytest` and automate their execution via a GitHub Actions CI pipeline.

---

## 6. PROBLEM STATEMENT AND SCOPE

### 6.1 Problem Statement
Developers frequently struggle to deploy web applications consistently across development, staging, and production environments due to conflicting OS dependencies, manual configuration mistakes, and volatile container storage that inadvertently wipes application data during maintenance or upgrades. 

There is a critical need for a containerized, automated, and persistent deployment pipeline that enables developers to build, test, package, and run full-stack applications with guaranteed reliability and zero data loss.

### 6.2 Scope of the Project
- **In-Scope:**
  - Full-stack web application development (Flask, Jinja2, HTML5, CSS3, JavaScript).
  - SQLite database schema design with idempotent sample data seeding for `books`, `orders`, and `order_items`.
  - Client-side and server-side shopping cart session management.
  - Form validation for user checkout and dynamic price calculation.
  - Containerization using Docker and orchestration using Docker Compose.
  - Persistent storage management using Docker Named Volumes.
  - System health monitoring endpoint (`/health`) with automated probes.
  - Automated test suite containing 14 unit and integration tests using Pytest.
  - GitHub Actions CI workflow to automate testing and image packaging.
- **Out-of-Scope:**
  - Real payment gateway integrations (credit card processing) to maintain academic focus and avoid third-party financial liabilities.
  - Multi-node Kubernetes clustering (reserved for future multi-tier distributed scaling).

---

## 7. TOOLS AND TECHNOLOGIES USED

| Tool / Technology | Purpose | Version / Details |
| :--- | :--- | :--- |
| **Python** | Core backend language | Python 3.11 / 3.14 |
| **Flask** | Lightweight Web Framework & Routing | Flask 3.1.0 |
| **Gunicorn** | Production WSGI HTTP Server | Gunicorn 23.0 (Linux Container runtime) |
| **SQLite 3** | Embedded Relational Database | Built-in Python `sqlite3` module |
| **HTML5 & CSS3** | Client-Side Structure & Styling | Custom responsive dark-theme design |
| **JavaScript** | Client-Side Interactivity | Vanilla ES6+ (DOM manipulation, alerts) |
| **Docker** | Containerization platform | Linux container runtime (`python:3.11-slim`) |
| **Docker Compose** | Multi-container orchestration | Compose Spec v3.8+ |
| **Pytest** | Automated Testing Framework | Pytest 8.3 / 9.2 |
| **Git & GitHub** | Source Version Control & Hosting | Git 2.55+ / GitHub Repository |
| **GitHub Actions** | Continuous Integration (CI) Automation | Workflow running on `ubuntu-latest` |
| **VS Code** | Integrated Development Environment | Code authoring, debugging, terminal |

---

## 8. SYSTEM DESIGN / METHODOLOGY

### 8.1 System Architecture

The bookstore follows a micro-service inspired, single-container architecture orchestrated by Docker Compose:

```text
+-----------------------------------------------------------------------------------+
|                                  HOST MACHINE                                     |
|                                                                                   |
|    +--------------------+              HTTP (Port 5000:5000)                      |
|    |    Web Browser     | <============================================+          |
|    |  (End-User Client) |                                              |          |
|    +--------------------+                                              |          |
|                                                                        |          |
|    +-------------------------------------------------------------+     |          |
|    |               DOCKER COMPOSE ORCHESTRATION                  |     |          |
|    |                                                             |     |          |
|    |   +-----------------------------------------------------+   |     |          |
|    |   |     CONTAINER: bookstore_app (python:3.11-slim)     |   |     |          |
|    |   |                                                     |   |     |          |
|    |   |   +---------------------------------------------+   |   |     |          |
|    |   |   | Gunicorn WSGI Server (2 Workers, 4 Threads) | <-+---|-----+          |
|    |   |   +---------------------------------------------+   |   |                |
|    |   |                          |                          |   |                |
|    |   |   +---------------------------------------------+   |   |                |
|    |   |   |    Flask Application Core (app.py)          |   |   |                |
|    |   |   |    - Routing & Controllers                  |   |   |                |
|    |   |   |    - Session Shopping Cart Management       |   |   |                |
|    |   |   |    - Jinja2 Template Rendering Engine       |   |   |                |
|    |   |   +---------------------------------------------+   |   |                |
|    |   |                          |                          |   |                |
|    |   |   +---------------------------------------------+   |   |                |
|    |   |   |       Database Controller (db.py)           |   |   |                |
|    |   |   +---------------------------------------------+   |   |                |
|    |   |                          |                          |   |                |
|    |   |                          v                          |   |                |
|    |   |            Mount Path: /app/data/bookstore.db       |   |                |
|    |   +--------------------------|--------------------------+   |                |
|    +------------------------------|------------------------------+                |
|                                   |                                               |
|                                   v                                               |
|                   +-------------------------------+                               |
|                   |      DOCKER NAMED VOLUME      |                               |
|                   |       (bookstore-data)        |                               |
|                   |  Persistent SQLite Database   |                               |
|                   +-------------------------------+                               |
+-----------------------------------------------------------------------------------+
```

### 8.2 Database Relational Model (Schema Design)

The database schema comprises three core relational tables designed with foreign key constraints:

1. **`books` Table:**
   - `id` (INTEGER, PRIMARY KEY AUTOINCREMENT)
   - `title` (TEXT, NOT NULL)
   - `author` (TEXT, NOT NULL)
   - `category` (TEXT, NOT NULL)
   - `price` (REAL, NOT NULL)
   - `description` (TEXT, NOT NULL)
   - `isbn` (TEXT, UNIQUE NOT NULL)
   - `stock` (INTEGER, NOT NULL DEFAULT 15)
   - `cover_color` (TEXT, NOT NULL DEFAULT '#1e293b')
   - `cover_accent` (TEXT, NOT NULL DEFAULT '#38bdf8')
   - `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

2. **`orders` Table:**
   - `id` (INTEGER, PRIMARY KEY AUTOINCREMENT)
   - `order_number` (TEXT, UNIQUE NOT NULL)
   - `customer_name` (TEXT, NOT NULL)
   - `customer_email` (TEXT, NOT NULL)
   - `customer_address` (TEXT, NOT NULL)
   - `total_amount` (REAL, NOT NULL)
   - `item_count` (INTEGER, NOT NULL)
   - `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

3. **`order_items` Table:**
   - `id` (INTEGER, PRIMARY KEY AUTOINCREMENT)
   - `order_id` (INTEGER, FOREIGN KEY REFERENCES `orders(id)` ON DELETE CASCADE)
   - `book_id` (INTEGER, FOREIGN KEY REFERENCES `books(id)`)
   - `book_title` (TEXT, NOT NULL)
   - `unit_price` (REAL, NOT NULL)
   - `quantity` (INTEGER, NOT NULL)
   - `subtotal` (REAL, NOT NULL)

### 8.3 User Checkout Workflow

```text
[User Browses Catalog] ──> [Filter by Category / Search Title]
                                    │
                                    ▼
                         [Add Books to Cart]
                                    │
                                    ▼
                        [View Cart & Adjust Qty]
                                    │
                                    ▼
                          [Proceed to Checkout]
                                    │
                                    ▼
                        [Enter Customer Details]
                                    │
                      ┌─────────────┴─────────────┐
                   (Invalid)                   (Valid)
                      │                           │
                      ▼                           ▼
            [Display Error Toast]       [Generate ORD-XXXXXX]
                                        [Insert into 'orders']
                                        [Insert into 'order_items']
                                        [Clear Session Cart]
                                                  │
                                                  ▼
                                      [Display Order Confirmation]
```

---

## 9. DAY-WISE PROGRESS REPORT

| Day | Activities Performed | Deliverables / Outcomes |
| :--- | :--- | :--- |
| **Day 1** | Requirement analysis, topic finalization, and architecture planning. Reviewed DevOps project scope and GitHub repository setup. | Finalized technology stack (Flask, SQLite, Docker, Compose, Pytest). Initialized Git repository structure. |
| **Day 2** | Database schema design and data modeling. Implemented SQLite table creation scripts and idempotent seeder for initial catalog data. | Authored `db.py` with `books`, `orders`, and `order_items` tables; populated 10 curated tech titles without duplicate inserts on reboots. |
| **Day 3** | Backend application development using Flask. Created application factory, routes for catalog, search, category filter, and session cart. | Authored `app.py` with search queries, category filters, and session-based cart endpoints (`/cart/add`, `/cart/update`, `/cart/clear`). |
| **Day 4** | Frontend development and UI engineering. Built responsive templates and modern dark-mode stylesheet with book card mockups. | Created `base.html`, `index.html`, `book_detail.html`, `cart.html`, `checkout.html`, and `style.css`. Form validation added via `app.js`. |
| **Day 5** | Containerization with Docker and multi-service orchestration with Docker Compose. Configured persistent named volumes. | Created `Dockerfile` (using `python:3.11-slim` and non-root user), `docker-compose.yml` with named volume `bookstore-data`, and `.dockerignore`. |
| **Day 6** | Automated testing using Pytest and Continuous Integration setup via GitHub Actions. Fixed test assertions and environment markers. | Authored `tests/test_app.py` (14 passing tests) and `.github/workflows/ci.yml` pipeline validating tests and Docker image build. |
| **Day 7** | System verification, persistence stress testing, README documentation authoring, project report compilation, and final GitHub push. | Completed comprehensive `README.md` and project report. Successfully pushed all code and configuration to GitHub repository `main` branch. |

---

## 10. IMPLEMENTATION AND RESULTS

### 10.1 Module Breakdown

1. **Catalog & Search Module (`app.py`, `index.html`):**
   - Supports keyword searches across book title, author, and description fields using SQL parameterized queries (`LIKE %query%`) to prevent SQL injection.
   - Dynamic category pills allow instantaneous filtering by topic (*DevOps & Cloud*, *Software Engineering*, *Computer Science*, etc.).
2. **Session Cart Module (`app.py`, `cart.html`):**
   - Tracks items directly in the encrypted client session dictionary (`session['cart']`).
   - Supports incremental quantity updates (`+` / `-`), individual item removals, and total cart purging.
3. **Checkout & Persistence Module (`app.py`, `checkout.html`, `confirmation.html`):**
   - Validates user input (name, regex email validation, shipping address).
   - Generates a unique tracking reference (`ORD-YYYYMMDD-HEX`).
   - Executes atomic SQL inserts to preserve order items linked to the order ID.
4. **DevOps Monitoring Module (`/health`):**
   - Provides a REST endpoint returning application status, service identity, and live SQLite database ping verification.

### 10.2 Automated Test Execution Results

Pytest was executed locally and on GitHub Actions CI. All 14 tests passed with 100% success:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\Lenovo\.gemini\antigravity\scratch\devops_project
collected 14 items

tests/test_app.py::test_homepage_loads PASSED                            [  7%]
tests/test_app.py::test_books_display PASSED                             [ 14%]
tests/test_app.py::test_search_books_by_title PASSED                     [ 21%]
tests/test_app.py::test_search_books_by_author PASSED                    [ 28%]
tests/test_app.py::test_filter_books_by_category PASSED                  [ 35%]
tests/test_app.py::test_empty_search_message PASSED                      [ 42%]
tests/test_app.py::test_book_details_view_valid PASSED                   [ 50%]
tests/test_app.py::test_book_details_view_invalid_returns_404 PASSED    [ 57%]
tests/test_app.py::test_cart_operations PASSED                           [ 64%]
tests/test_app.py::test_checkout_empty_cart_redirect PASSED              [ 71%]
tests/test_app.py::test_checkout_validation_errors PASSED                [ 78%]
tests/test_app.py::test_successful_order_placement_and_database_persistence PASSED [ 85%]
tests/test_app.py::test_health_monitoring_endpoint PASSED                [ 92%]
tests/test_app.py::test_idempotent_database_seeding PASSED               [100%]

============================= 14 passed in 0.89s ==============================
```

### 10.3 Persistence Verification Experiment

To prove that the Docker volume successfully preserves state:
1. The container was booted using `docker compose up -d`.
2. A test order was placed through the UI for customer *Jane DevOps* with 2 books totaling `$94.98`.
3. The container was completely terminated using `docker compose down`.
4. The container was recreated from scratch using `docker compose up -d`.
5. Direct inspection verified that order records in `bookstore.db` remained intact with zero data loss due to the `bookstore-data` named volume mount.

---

## 11. LEARNING OUTCOMES

Through the execution of this technical project, the following core competencies were gained:

1. **Practical Containerization Skills:** Gained in-depth knowledge of how Docker constructs container images layer-by-layer, how `.dockerignore` optimizes image size, and how to execute processes under non-privileged users (`appuser`).
2. **Container Orchestration:** Learned to write declarative YAML manifests (`docker-compose.yml`) to orchestrate container lifecycles, configure host-to-container port publishing (`5000:5000`), and configure environment variables.
3. **Data Persistence in Microservices:** Understood the fundamental difference between ephemeral container storage and persistent storage drivers (Docker Named Volumes).
4. **Test-Driven Reliability:** Mastered writing isolated test fixtures with Pytest using temporary databases to prevent test data pollution.
5. **Continuous Integration (CI/CD):** Implemented GitHub Actions workflows that automatically validate pull requests, execute unit tests, and build Docker container images.

---

## 12. CHALLENGES FACED AND SOLUTIONS

| Challenge Encountered | Action Taken / Solution | Outcome / Result |
| :--- | :--- | :--- |
| **Ephemeral Container Storage:** When containers stopped, SQLite database changes were wiped out. | Configured a Docker Named Volume (`bookstore-data:/app/data`) in `docker-compose.yml`. | Database records, orders, and customer details persist across container restarts. |
| **Duplicate Seeding on Boot:** Every restart of the container triggered the seed script, duplicating book entries. | Implemented an idempotency check in `db.py` (`SELECT COUNT(*) FROM books`) before inserting seed rows. | Initial sample books are seeded exactly once on first boot; restarts do not create duplicate rows. |
| **Host Environment Discrepancies:** Gunicorn WSGI server is POSIX-only and fails when installed natively on Windows development environments. | Utilized PEP 508 environment markers in `requirements.txt`: `gunicorn>=21.0; sys_platform != 'win32'`. | Allows seamless testing on Windows developer machines while ensuring Gunicorn installs inside the Linux Docker container. |
| **Container Security Vulnerability:** Running applications as the default `root` user poses security risks. | Created a dedicated unprivileged user (`appuser`) in `Dockerfile` and granted explicit directory permissions to `/app/data`. | Achieved container security compliance without breaking SQLite write access. |

---

## 13. CONCLUSION AND FUTURE SCOPE

### 13.1 Conclusion
The one-week technical project titled **“Dockerized Online Bookstore Using Docker Compose”** was successfully designed, developed, containerized, tested, and documented. All initial objectives were met:
- A responsive, functional bookstore application was built using Python Flask, SQLite, and vanilla web standards.
- Docker containerization was achieved with an optimized, secure multi-layer Dockerfile.
- Multi-container orchestration was codified using Docker Compose with persistent named volume storage.
- High software quality was guaranteed through 14 automated Pytest tests achieving a 100% pass rate.
- An automated GitHub Actions CI/CD pipeline was deployed to validate all commits on the `main` branch.

### 13.2 Future Scope
While the current implementation fulfills all college DevOps curriculum requirements, future improvements include:
1. **Multi-Service Database Migration:** Decouple the embedded SQLite database into a dedicated multi-container service using PostgreSQL or MySQL within `docker-compose.yml`.
2. **Reverse Proxy & SSL Termination:** Deploy an **Nginx** reverse proxy container ahead of Gunicorn for load balancing and HTTPS termination.
3. **Observability Stack:** Integrate Prometheus and Grafana container services to collect container CPU, memory metrics, and Flask HTTP latency in real-time.

---

## 14. REFERENCES

1. **Docker Documentation:** *Get Started with Docker & Docker Compose*, Docker Inc., 2026. [https://docs.docker.com/](https://docs.docker.com/)
2. **Flask Documentation (v3.1.x):** *Pallets Projects - Web Development with Python*, 2026. [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
3. **Poulton, Nigel:** *Docker Deep Dive*, Independently Published, 2023.
4. **Humble, Jez & Farley, David:** *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*, Addison-Wesley Professional, 2010.
5. **Pytest Documentation:** *Full pytest documentation and fixtures*, 2026. [https://docs.pytest.org/](https://docs.pytest.org/)
6. **GitHub Actions Guides:** *Automating your workflow with GitHub Actions*, GitHub Docs, 2026. [https://docs.github.com/actions](https://docs.github.com/actions)

---

## 15. APPENDICES / SUPPORTING EVIDENCE

### Appendix A: Production `Dockerfile`
```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    DATABASE_PATH=/app/data/bookstore.db \
    FLASK_ENV=production

WORKDIR /app

RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    mkdir -p /app/data && \
    chown -R appuser:appuser /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R appuser:appuser /app

USER appuser
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "app:create_app()"]
```

### Appendix B: `docker-compose.yml` Configuration
```yaml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: bookstore_app
    restart: unless-stopped
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_PATH=/app/data/bookstore.db
      - SECRET_KEY=college-devops-bookstore-secret-2026
      - PORT=5000
    volumes:
      - bookstore-data:/app/data
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

volumes:
  bookstore-data:
    driver: local
```

### Appendix C: GitHub Actions Workflow (`.github/workflows/ci.yml`)
```yaml
name: DevOps Bookstore CI/CD Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  test:
    name: Run Pytest Test Suite
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest -v tests

  docker-build:
    name: Build & Validate Docker Container Image
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - run: docker build -t devops-bookstore:latest .
```

---

## 16. MENTOR EVALUATION SHEET

**Student Name(s):** [Student Name(s)]  
**Roll Number(s):** [Roll Number(s)]  
**Project Title:** Dockerized Online Bookstore Using Docker Compose  
**Mentor Name:** [Mentor Name and Designation]  

| Evaluation Criterion | Maximum Marks | Marks Awarded |
| :--- | :---: | :---: |
| **Understanding of problem and objectives** | 10 | |
| **Technical knowledge and methodology** | 20 | |
| **Implementation / practical work** | 25 | |
| **Results and analysis** | 15 | |
| **Report quality and documentation** | 15 | |
| **Presentation and viva-voce** | 15 | |
| **Total** | **100** | |

**Mentor Remarks:**  
____________________________________________________________________________________________________  
____________________________________________________________________________________________________  
____________________________________________________________________________________________________  

<br>

**Mentor Signature:** _____________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Date:** ________________________  

<br><br>

___________________________________  
**Head of Department (HoD) Signature**
