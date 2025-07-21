# Let's create a summary of key assignment requirements for analysis
assignment_requirements = {
    "System Setup": [
        "Django 4+ with Django Rest Framework",
        "No frontend required - API only",
        "Appropriate data models",
        "Dockerized application with PostgreSQL",
        "Single docker-compose command deployment"
    ],
    "Data Ingestion": [
        "Background workers to ingest customer_data.xlsx and loan_data.xlsx",
        "Initialize system with provided data"
    ],
    "API Endpoints": {
        "/register": {
            "purpose": "Add new customer with approved limit calculation",
            "formula": "approved_limit = 36 * monthly_salary (rounded to nearest lakh)",
            "request_fields": ["first_name", "last_name", "age", "monthly_income", "phone_number"],
            "response_fields": ["customer_id", "name", "age", "monthly_income", "approved_limit", "phone_number"]
        },
        "/check-eligibility": {
            "purpose": "Check loan eligibility based on credit score",
            "credit_score_factors": [
                "Past Loans paid on time",
                "Number of loans taken in past", 
                "Loan activity in current year",
                "Loan approved volume",
                "If sum of current loans > approved limit, credit score = 0"
            ],
            "approval_rules": [
                "credit_rating > 50: approve loan",
                "50 > credit_rating > 30: approve with interest rate > 12%",
                "30 > credit_rating > 10: approve with interest rate > 16%", 
                "10 > credit_rating: don't approve",
                "sum of EMIs > 50% of monthly salary: don't approve"
            ]
        },
        "/create-loan": {
            "purpose": "Process new loan based on eligibility",
            "logic": "Use same eligibility check, create loan if approved"
        },
        "/view-loan/loan_id": {
            "purpose": "View specific loan details with customer info"
        },
        "/view-loans/customer_id": {
            "purpose": "View all current loans for a customer"
        }
    },
    "Technical Requirements": [
        "Compound interest calculation for monthly payments",
        "Background task processing",
        "Proper error handling and status codes",
        "Unit tests (bonus points)",
        "Code quality and organization",
        "36-hour submission deadline"
    ]
}

print("CREDIT APPROVAL SYSTEM - ASSIGNMENT ANALYSIS")
print("=" * 60)
for category, items in assignment_requirements.items():
    print(f"\n{category.upper()}:")
    if isinstance(items, list):
        for item in items:
            print(f"  • {item}")
    elif isinstance(items, dict):
        for endpoint, details in items.items():
            print(f"  {endpoint}:")
            if isinstance(details, dict):
                for key, value in details.items():
                    print(f"    {key}: {value}")
            else:
                print(f"    {details}")