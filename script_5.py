# Let's create sample data for a credit scoring algorithm implementation example
import pandas as pd
import numpy as np

# Sample credit scoring algorithm implementation
def calculate_credit_score(customer_data, loan_history):
    """
    Comprehensive credit scoring algorithm based on assignment requirements
    """
    
    # Initialize base score
    base_score = 300  # Minimum credit score
    max_score = 850   # Maximum credit score
    
    # Component 1: Payment History (35% weight)
    if len(loan_history) == 0:
        payment_score = 80  # New customer gets decent score
    else:
        # Calculate average payment ratio across all loans
        payment_ratios = loan_history['EMIs paid on Time'] / loan_history['Tenure']
        avg_payment_ratio = payment_ratios.mean()
        
        if avg_payment_ratio >= 1.0:
            payment_score = 100
        elif avg_payment_ratio >= 0.9:
            payment_score = 90
        elif avg_payment_ratio >= 0.8:
            payment_score = 80
        elif avg_payment_ratio >= 0.7:
            payment_score = 60
        else:
            payment_score = 30
    
    # Component 2: Credit Utilization (30% weight)
    current_active_loans = loan_history[loan_history['End Date'] > pd.Timestamp.now()]
    if len(current_active_loans) == 0:
        utilization_score = 100
    else:
        total_current_debt = current_active_loans['Loan Amount'].sum()
        utilization_ratio = total_current_debt / customer_data['Approved Limit']
        
        if utilization_ratio <= 0.3:
            utilization_score = 100
        elif utilization_ratio <= 0.5:
            utilization_score = 80
        elif utilization_ratio <= 0.7:
            utilization_score = 60
        elif utilization_ratio <= 1.0:
            utilization_score = 40
        else:
            utilization_score = 0  # Over limit
    
    # Component 3: Number of Loans (15% weight)
    total_loans = len(loan_history)
    if total_loans <= 2:
        loan_count_score = 100
    elif total_loans <= 4:
        loan_count_score = 85
    elif total_loans <= 6:
        loan_count_score = 70
    else:
        loan_count_score = 50
    
    # Component 4: Current Year Activity (10% weight)
    current_year = 2025
    current_year_loans = loan_history[
        pd.to_datetime(loan_history['Date of Approval']).dt.year == current_year
    ]
    
    if len(current_year_loans) == 0:
        activity_score = 100
    elif len(current_year_loans) == 1:
        activity_score = 85
    elif len(current_year_loans) == 2:
        activity_score = 70
    else:
        activity_score = 50
    
    # Component 5: Age and Income Stability (10% weight)
    age = customer_data['Age']
    income = customer_data['Monthly Salary']
    
    # Age factor (25-65 is optimal)
    if 25 <= age <= 65:
        age_factor = 100
    elif age < 25:
        age_factor = 70
    else:
        age_factor = 80
    
    # Income factor (higher income = more stability)
    if income >= 200000:
        income_factor = 100
    elif income >= 100000:
        income_factor = 85
    elif income >= 50000:
        income_factor = 70
    else:
        income_factor = 50
    
    stability_score = (age_factor + income_factor) / 2
    
    # Calculate weighted credit score
    weighted_score = (
        payment_score * 0.35 +
        utilization_score * 0.30 +
        loan_count_score * 0.15 +
        activity_score * 0.10 +
        stability_score * 0.10
    )
    
    # Scale to credit score range (300-850)
    credit_score = base_score + (weighted_score / 100) * (max_score - base_score)
    
    return round(credit_score)

# EMI Calculation Function
def calculate_emi(principal, annual_rate, tenure_months):
    """
    Calculate EMI using compound interest formula
    EMI = [P × r × (1 + r)^n] / [(1 + r)^n - 1]
    """
    if annual_rate == 0:
        return principal / tenure_months
    
    monthly_rate = annual_rate / (12 * 100)  # Convert annual % to monthly decimal
    
    # Compound interest EMI formula
    emi = principal * (monthly_rate * (1 + monthly_rate)**tenure_months) / \
          ((1 + monthly_rate)**tenure_months - 1)
    
    return round(emi, 2)

# Test the functions with sample data
print("Credit Scoring Algorithm & EMI Calculator Examples")
print("=" * 60)

# Sample customer data
sample_customer = {
    'Customer ID': 1,
    'Age': 35,
    'Monthly Salary': 150000,
    'Approved Limit': 5000000
}

# Sample loan history (empty for new customer)
empty_loan_history = pd.DataFrame()

# Calculate credit score for new customer
new_customer_score = calculate_credit_score(sample_customer, empty_loan_history)
print(f"New Customer Credit Score: {new_customer_score}")

# Sample with loan history
loan_history_sample = pd.DataFrame({
    'Customer ID': [1, 1, 1],
    'Loan Amount': [500000, 300000, 200000],
    'Tenure': [60, 36, 24],
    'EMIs paid on Time': [58, 34, 24],
    'Date of Approval': ['2020-01-01', '2022-06-15', '2024-03-10'],
    'End Date': ['2025-01-01', '2025-06-15', '2026-03-10']
})

# Convert date columns
loan_history_sample['Date of Approval'] = pd.to_datetime(loan_history_sample['Date of Approval'])
loan_history_sample['End Date'] = pd.to_datetime(loan_history_sample['End Date'])

experienced_customer_score = calculate_credit_score(sample_customer, loan_history_sample)
print(f"Experienced Customer Credit Score: {experienced_customer_score}")

# EMI Calculations
print(f"\nEMI Calculation Examples:")
print(f"Loan Amount: ₹500,000, Rate: 12%, Tenure: 60 months")
emi1 = calculate_emi(500000, 12, 60)
print(f"EMI: ₹{emi1:,}")

print(f"\nLoan Amount: ₹1,000,000, Rate: 15%, Tenure: 120 months") 
emi2 = calculate_emi(1000000, 15, 120)
print(f"EMI: ₹{emi2:,}")

# Interest rate correction logic based on credit score
def get_corrected_interest_rate(credit_score, requested_rate):
    """
    Correct interest rate based on credit score as per assignment rules
    """
    if credit_score > 50:
        return requested_rate  # Approved at requested rate
    elif 30 < credit_score <= 50:
        return max(requested_rate, 12.0)  # Minimum 12%
    elif 10 < credit_score <= 30:
        return max(requested_rate, 16.0)  # Minimum 16%
    else:
        return None  # Loan rejected

print(f"\nInterest Rate Correction Examples:")
test_scores = [75, 45, 25, 5]
requested_rate = 10.5

for score in test_scores:
    corrected_rate = get_corrected_interest_rate(score, requested_rate)
    if corrected_rate:
        print(f"Credit Score: {score}, Requested: {requested_rate}%, Corrected: {corrected_rate}%")
    else:
        print(f"Credit Score: {score}, Requested: {requested_rate}%, Status: REJECTED")