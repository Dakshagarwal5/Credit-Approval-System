# Credit Approval System - Backend Assignment Analysis

## Overview
This is a comprehensive Django-based backend assignment for building a credit approval system. The system evaluates loan applications based on historical customer data and implements a credit scoring algorithm.

## Data Analysis

### Customer Data (300 records)
- **Fields**: Customer ID, First Name, Last Name, Age, Phone Number, Monthly Salary, Approved Limit
- **Salary Range**: ₹32,000 - ₹299,000
- **Average Salary**: ₹158,013
- **Approved Limit Range**: ₹800,000 - ₹5,000,000
- **Average Limit**: ₹2,871,667

### Loan Data (782 loans)
- **Active Loans**: 344 (end date > current date)
- **Completed Loans**: 438
- **Customers with Loans**: 283 out of 300
- **Loan Amount Range**: ₹100,000 - ₹1,000,000
- **Average Loan Amount**: ₹539,003
- **Average Interest Rate**: 13.04%
- **Average Tenure**: 95 months

## Technical Requirements

### Core Stack
- **Framework**: Django 4+ with Django Rest Framework
- **Database**: PostgreSQL
- **Task Queue**: Celery (implied for background workers)
- **Deployment**: Docker with docker-compose
- **Data Processing**: Background workers for Excel ingestion

### API Endpoints

#### 1. `/register` (POST)
**Purpose**: Register new customer with auto-calculated credit limit

**Request Body**:
```json
{
  "first_name": "string",
  "last_name": "string", 
  "age": "integer",
  "monthly_income": "integer",
  "phone_number": "integer"
}
```

**Business Logic**:
- `approved_limit = round(36 * monthly_salary / 100000) * 100000` (nearest lakh)

#### 2. `/check-eligibility` (POST)
**Purpose**: Evaluate loan eligibility using credit scoring

**Request Body**:
```json
{
  "customer_id": "integer",
  "loan_amount": "float",
  "interest_rate": "float", 
  "tenure": "integer"
}
```

**Credit Scoring Factors**:
1. **Payment History** (40% weight)
2. **Number of Past Loans** (20% weight)
3. **Current Year Activity** (20% weight) 
4. **Loan Volume vs Approved Limit** (20% weight)

**Approval Rules**:
- Credit Score > 50: Approve loan
- 30 < Credit Score ≤ 50: Approve with interest rate > 12%
- 10 < Credit Score ≤ 30: Approve with interest rate > 16%
- Credit Score ≤ 10: Reject
- Current EMIs > 50% of monthly salary: Reject
- Current debt > approved limit: Credit score = 0

#### 3. `/create-loan` (POST)
**Purpose**: Create approved loan after eligibility check

#### 4. `/view-loan/<loan_id>` (GET)
**Purpose**: View specific loan with customer details

#### 5. `/view-loans/<customer_id>` (GET)
**Purpose**: View all current loans for a customer

## Implementation Challenges

### 1. Credit Scoring Algorithm
The assignment requires implementing a multi-factor credit scoring system:

```python
def calculate_credit_score(customer, current_loans, loan_history):
    # Special conditions
    if sum(current_loans.values()) > customer.approved_limit:
        return 0
    
    # Payment history analysis
    payment_score = analyze_payment_history(loan_history)
    
    # Number of loans factor
    loan_count_score = evaluate_loan_count(loan_history)
    
    # Current year activity
    activity_score = check_current_year_activity(loan_history)
    
    # Volume utilization
    volume_score = calculate_volume_utilization(current_loans, customer.approved_limit)
    
    # Weighted average
    final_score = (
        payment_score * 0.4 +
        loan_count_score * 0.2 + 
        activity_score * 0.2 +
        volume_score * 0.2
    )
    
    return final_score
```

### 2. Compound Interest Calculation
Monthly EMI calculation using compound interest:

```python
def calculate_monthly_emi(principal, annual_rate, tenure_months):
    monthly_rate = annual_rate / (12 * 100)
    emi = principal * (monthly_rate * (1 + monthly_rate)**tenure_months) / ((1 + monthly_rate)**tenure_months - 1)
    return round(emi, 2)
```

### 3. Data Migration
Background task to ingest Excel files:

```python
# Celery task for data ingestion
@shared_task
def ingest_customer_data():
    # Read customer_data.xlsx
    # Create Customer objects
    # Handle duplicates and validation
    
@shared_task  
def ingest_loan_data():
    # Read loan_data.xlsx
    # Create Loan objects
    # Link to existing customers
```

## Key Business Logic Insights

### Credit Limit Formula
The assignment specifies `approved_limit = 36 * monthly_salary`, but our data analysis shows:
- **Actual average ratio**: 24.8x
- **Range**: 3.08x to 144.12x
- **Expected**: 36x (as per assignment)

### Payment Performance Patterns
- **Average payment ratio**: 75% (EMIs paid on time / total EMIs)
- **Perfect payment customers**: 32 out of 782 loans
- **No customers with <50% payment ratio** (good portfolio quality)

### Loan Distribution
- **Most common**: 2-3 loans per customer
- **Active loan rate**: 44% (344/782)
- **Customer coverage**: 94% have at least one loan

## Docker Architecture

```yaml
# docker-compose.yml structure
services:
  web:
    build: .
    depends_on: [db, redis]
  
  db:
    image: postgres:15
    
  redis:
    image: redis:alpine
    
  celery:
    build: .
    depends_on: [db, redis]
    command: celery -A config worker
```

## Evaluation Criteria
1. **Code Quality**: Clean, organized, well-documented
2. **Functionality**: All endpoints working correctly
3. **Business Logic**: Accurate credit scoring implementation
4. **Architecture**: Proper separation of concerns
5. **Testing**: Unit tests (bonus points)
6. **Deployment**: Single docker-compose command
7. **Deadline**: 36-hour submission window

## Recommendations

1. **Start with Models**: Define Customer and Loan models first
2. **Implement Credit Scoring**: This is the core business logic
3. **Background Tasks**: Use Django management commands initially, migrate to Celery later
4. **API Testing**: Use DRF browsable API or Postman for testing
5. **Error Handling**: Implement proper HTTP status codes and error messages
6. **Data Validation**: Use DRF serializers for input validation
7. **Documentation**: Add API documentation using DRF's built-in tools

This assignment tests full-stack backend development skills including database design, business logic implementation, API development, background processing, and deployment automation.