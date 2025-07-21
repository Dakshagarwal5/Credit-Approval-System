# Let's create a detailed technical implementation plan
implementation_plan = """
TECHNICAL IMPLEMENTATION PLAN
========================================

1. PROJECT STRUCTURE
   credit_approval_system/
   ├── manage.py
   ├── requirements.txt
   ├── docker-compose.yml
   ├── Dockerfile
   ├── config/
   │   ├── __init__.py
   │   ├── settings.py
   │   ├── urls.py
   │   └── wsgi.py
   ├── apps/
   │   ├── customers/
   │   │   ├── models.py (Customer model)
   │   │   ├── serializers.py
   │   │   ├── views.py
   │   │   └── urls.py
   │   ├── loans/
   │   │   ├── models.py (Loan model)
   │   │   ├── serializers.py
   │   │   ├── views.py
   │   │   ├── urls.py
   │   │   └── utils.py (credit scoring logic)
   │   └── data_ingestion/
   │       ├── management/commands/
   │       │   └── ingest_data.py
   │       └── tasks.py (Celery tasks)
   └── data/
       ├── customer_data.xlsx
       └── loan_data.xlsx

2. DATA MODELS
   Customer Model:
   - customer_id (AutoField)
   - first_name (CharField)
   - last_name (CharField) 
   - age (IntegerField)
   - phone_number (BigIntegerField)
   - monthly_salary (IntegerField)
   - approved_limit (IntegerField)
   - current_debt (IntegerField, default=0)
   - created_at (DateTimeField)
   
   Loan Model:
   - loan_id (AutoField)
   - customer (ForeignKey to Customer)
   - loan_amount (IntegerField)
   - tenure (IntegerField)
   - interest_rate (FloatField)
   - monthly_repayment (FloatField)
   - emis_paid_on_time (IntegerField, default=0)
   - start_date (DateField)
   - end_date (DateField)
   - created_at (DateTimeField)
   - is_active (BooleanField, default=True)

3. CREDIT SCORING ALGORITHM
   Components (each 0-100 scale, then averaged):
   a) Payment History (40% weight):
      - Perfect payment (100%): 100 points
      - 90-99% on time: 80 points
      - 80-89% on time: 60 points
      - 70-79% on time: 40 points
      - <70% on time: 20 points
   
   b) Number of Loans (20% weight):
      - 1-2 loans: 100 points
      - 3-4 loans: 80 points
      - 5-6 loans: 60 points
      - 7+ loans: 40 points
   
   c) Loan Activity Current Year (20% weight):
      - 0 loans this year: 100 points
      - 1 loan this year: 80 points
      - 2+ loans this year: 60 points
   
   d) Loan Volume vs Limit (20% weight):
      - < 30% of limit: 100 points
      - 30-50% of limit: 80 points
      - 50-70% of limit: 60 points
      - 70%+ of limit: 40 points
   
   Special Rules:
   - If current loans > approved limit: score = 0
   - If current EMIs > 50% monthly salary: don't approve

4. API IMPLEMENTATION DETAILS
   """

print(implementation_plan)

# Create credit scoring function example
def calculate_credit_score(customer_id, loan_data_df):
    """
    Example implementation of credit scoring algorithm
    """
    customer_loans = loan_data_df[loan_data_df['Customer ID'] == customer_id]
    
    if len(customer_loans) == 0:
        return 85  # New customer gets decent score
    
    # Component 1: Payment History (40% weight)
    payment_ratios = customer_loans['EMIs paid on Time'] / customer_loans['Tenure'] 
    avg_payment_ratio = payment_ratios.mean()
    
    if avg_payment_ratio >= 1.0:
        payment_score = 100
    elif avg_payment_ratio >= 0.9:
        payment_score = 80
    elif avg_payment_ratio >= 0.8:
        payment_score = 60
    elif avg_payment_ratio >= 0.7:
        payment_score = 40
    else:
        payment_score = 20
    
    # Component 2: Number of loans (20% weight)
    num_loans = len(customer_loans)
    if num_loans <= 2:
        loan_count_score = 100
    elif num_loans <= 4:
        loan_count_score = 80
    elif num_loans <= 6:
        loan_count_score = 60
    else:
        loan_count_score = 40
    
    # Component 3: Current year activity (20% weight)
    current_year = 2025
    current_year_loans = customer_loans[
        pd.to_datetime(customer_loans['Date of Approval']).dt.year == current_year
    ]
    
    if len(current_year_loans) == 0:
        activity_score = 100
    elif len(current_year_loans) == 1:
        activity_score = 80
    else:
        activity_score = 60
    
    # Component 4: Loan volume (20% weight) - placeholder
    volume_score = 80  # Would need customer approved limit for accurate calculation
    
    # Calculate weighted average
    credit_score = (
        payment_score * 0.4 +
        loan_count_score * 0.2 +
        activity_score * 0.2 +
        volume_score * 0.2
    )
    
    return round(credit_score)

# Test the function
test_score = calculate_credit_score(1, loan_data)
print(f"\n5. EXAMPLE CREDIT SCORE CALCULATION")
print(f"   Customer 1 credit score: {test_score}")

print(f"\n6. COMPOUND INTEREST FORMULA")
print(f"   Monthly Payment = P * [r(1+r)^n] / [(1+r)^n - 1]")
print(f"   Where: P = Principal, r = monthly rate, n = tenure in months")

print(f"\n7. DOCKER SETUP")
print(f"   - Django application container")
print(f"   - PostgreSQL database container") 
print(f"   - Redis container (for Celery)")
print(f"   - Celery worker container")