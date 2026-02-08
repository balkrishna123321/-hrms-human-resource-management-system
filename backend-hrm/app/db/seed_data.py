"""Realistic dummy data for seeding ~30 records per table."""
from datetime import date, datetime, time, timedelta
import random

# Fixed seed for reproducible data
random.seed(42)

FIRST_NAMES = [
    "Aarav", "Aditya", "Amit", "Anil", "Arjun", "Deepak", "Rahul", "Rajesh", "Sanjay", "Vikram",
    "Priya", "Anita", "Kavita", "Neha", "Pooja", "Rekha", "Sneha", "Sonal", "Vandana", "Kiran",
]
LAST_NAMES = [
    "Sharma", "Patel", "Singh", "Kumar", "Gupta", "Reddy", "Nair", "Mehta", "Joshi", "Iyer",
    "Khan", "Verma", "Shah", "Desai", "Rao", "Pillai", "Narayan", "Kulkarni", "Menon", "Bose",
]
DESIGNATIONS = [
    "Software Engineer", "Senior Software Engineer", "Tech Lead", "Engineering Manager",
    "HR Manager", "HR Executive", "Recruiter", "Accountant", "Finance Manager",
    "Sales Executive", "Sales Manager", "Business Development", "Operations Manager",
    "Project Manager", "Product Manager", "Data Analyst", "QA Engineer", "DevOps Engineer",
]
STREETS = [
    "MG Road", "Brigade Road", "Indiranagar", "Koramangala", "HSR Layout", "Whitefield",
    "Jayanagar", "JP Nagar", "Electronic City", "Marathahalli",
]
CITIES = ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Chennai", "Pune", "Kolkata"]
DOMAINS = ["company.com", "hrms.local", "example.com"]

def random_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def random_email(full_name: str, used: set) -> str:
    base = full_name.lower().replace(" ", ".") + str(random.randint(1, 999))
    for d in DOMAINS:
        e = f"{base}@{d}"
        if e not in used:
            used.add(e)
            return e
    used.add(f"{base}@company.com")
    return f"{base}@company.com"

def random_phone() -> str:
    return f"+91 {random.randint(7000000000, 9999999999)}"

def random_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, max(0, delta)))

# --- Permissions (extend to ~12) ---
EXTRA_PERMISSIONS = [
    ("View Reports", "report:view", "View analytics and reports"),
    ("Export Data", "data:export", "Export employee and attendance data"),
    ("Manage Departments", "department:manage", "Create and edit departments"),
    ("View Attendance", "attendance:view", "View attendance records"),
    ("Manage Leave Types", "leave_type:manage", "Manage leave type definitions"),
]

# --- Roles (extend to ~10) ---
EXTRA_ROLES = [
    ("Manager", "manager", "Team manager with approval rights"),
    ("HR Staff", "hr_staff", "HR operations"),
    ("Employee", "employee", "Basic employee access"),
    ("Finance", "finance", "Finance and payroll"),
    ("Department Head", "dept_head", "Department head with approvals"),
]

# --- Departments (extend to ~15) ---
EXTRA_DEPARTMENTS = [
    ("Product", "PROD", "Product management and design"),
    ("Marketing", "MKT", "Marketing and communications"),
    ("IT Support", "IT", "IT infrastructure and support"),
    ("Legal", "LEGAL", "Legal and compliance"),
    ("Quality Assurance", "QA", "Quality assurance and testing"),
    ("Research", "R&D", "Research and development"),
    ("Customer Success", "CS", "Customer success and support"),
    ("Administration", "ADMIN", "Admin and facilities"),
]

# --- Leave types (extend to ~10) ---
EXTRA_LEAVE_TYPES = [
    ("Maternity Leave", "MATERNITY", 26, "Maternity leave"),
    ("Paternity Leave", "PATERNITY", 15, "Paternity leave"),
    ("Compensatory Off", "COMP_OFF", 12, "Compensatory leave"),
    ("Bereavement Leave", "BEREAVEMENT", 5, "Bereavement leave"),
    ("Marriage Leave", "MARRIAGE", 5, "Marriage leave"),
    ("Earned Leave", "EARNED", 15, "Earned leave"),
]

# --- Holidays (extend to ~30 for current year) ---
def get_holiday_list(year: int) -> list[tuple[str, date]]:
    return [
        ("New Year", date(year, 1, 1)),
        ("Republic Day", date(year, 1, 26)),
        ("Maha Shivaratri", date(year, 2, 18)),
        ("Holi", date(year, 3, 10)),
        ("Good Friday", date(year, 4, 2)),
        ("Ambedkar Jayanti", date(year, 4, 14)),
        ("May Day", date(year, 5, 1)),
        ("Eid ul-Fitr", date(year, 4, 11)),
        ("Independence Day", date(year, 8, 15)),
        ("Janmashtami", date(year, 8, 16)),
        ("Gandhi Jayanti", date(year, 10, 2)),
        ("Dussehra", date(year, 10, 12)),
        ("Diwali", date(year, 11, 1)),
        ("Guru Nanak Jayanti", date(year, 11, 15)),
        ("Christmas", date(year, 12, 25)),
        ("Company Foundation Day", date(year, 6, 15)),
        ("Annual Day", date(year, 12, 20)),
    ]
