# Corrected credit scoring to match assignment requirements (0-100 scale)
def calculate_credit_score_assignment(customer_data, loan_history):
    """
    Credit scoring algorithm matching exact assignment requirements (0-100 scale)
    """
    
    # Component 1: Payment History (40% weight as per assignment priority)
    if len(loan_history) == 0:
        payment_score = 85  # New customer gets decent score
    else:
        # Calculate average payment ratio across all loans
        payment_ratios = loan_history['EMIs paid on Time'] / loan_history['Tenure']
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
    
    # Component 2: Number of loans taken in past (20% weight)
    total_loans = len(loan_history)
    if total_loans == 0:
        loan_count_score = 100  # New customer
    elif total_loans <= 2:
        loan_count_score = 100
    elif total_loans <= 4:
        loan_count_score = 80
    elif total_loans <= 6:
        loan_count_score = 60
    else:
        loan_count_score = 40
    
    # Component 3: Loan activity in current year (20% weight)
    if len(loan_history) == 0 or 'Date of Approval' not in loan_history.columns:
        activity_score = 100  # New customer
    else:
        current_year = 2025
        loan_approval_dates = pd.to_datetime(loan_history['Date of Approval'])
        current_year_loans = loan_history[loan_approval_dates.dt.year == current_year]
        
        if len(current_year_loans) == 0:
            activity_score = 100
        elif len(current_year_loans) == 1:
            activity_score = 80
        elif len(current_year_loans) == 2:
            activity_score = 60
        else:
            activity_score = 40
    
    # Component 4: Loan approved volume (20% weight)
    if len(loan_history) == 0 or 'End Date' not in loan_history.columns:
        volume_score = 100  # New customer
    else:
        current_active_loans = loan_history[loan_history['End Date'] > pd.Timestamp.now()]
        if len(current_active_loans) == 0:
            volume_score = 100
        else:
            total_current_debt = current_active_loans['Loan Amount'].sum()
            approved_limit = customer_data['Approved Limit']
            
            # Special rule: If current loans > approved limit, credit score = 0
            if total_current_debt > approved_limit:
                return 0
            
            utilization_ratio = total_current_debt / approved_limit
            
            if utilization_ratio <= 0.3:
                volume_score = 100
            elif utilization_ratio <= 0.5:
                volume_score = 80
            elif utilization_ratio <= 0.7:
                volume_score = 60
            else:
                volume_score = 40
    
    # Calculate weighted credit score (0-100 scale)
    credit_score = (
        payment_score * 0.4 +
        loan_count_score * 0.2 +
        activity_score * 0.2 +
        volume_score * 0.2
    )
    
    return round(credit_score)

# Test the corrected scoring function
print("CORRECTED CREDIT SCORING (Assignment Requirements)")
print("=" * 70)

# Test scenarios
test_customers = [
    {'Customer ID': 1, 'Age': 35, 'Monthly Salary': 150000, 'Approved Limit': 5000000},
    {'Customer ID': 2, 'Age': 25, 'Monthly Salary': 50000, 'Approved Limit': 1800000},
    {'Customer ID': 3, 'Age': 45, 'Monthly Salary': 250000, 'Approved Limit': 9000000}
]

# Test with different loan histories
scenarios = [
    ("New Customer", pd.DataFrame()),
    ("Good Payment History", pd.DataFrame({
        'Customer ID': [1, 1],
        'Loan Amount': [500000, 300000],
        'Tenure': [60, 36],
        'EMIs paid on Time': [60, 36],  # Perfect payments
        'Date of Approval': ['2022-01-01', '2023-06-15'],
        'End Date': ['2027-01-01', '2026-06-15']
    })),
    ("Poor Payment History", pd.DataFrame({
        'Customer ID': [1, 1, 1],
        'Loan Amount': [500000, 300000, 200000],
        'Tenure': [60, 36, 24],
        'EMIs paid on Time': [45, 20, 15],  # Poor payments
        'Date of Approval': ['2020-01-01', '2022-06-15', '2024-03-10'],
        'End Date': ['2025-01-01', '2025-06-15', '2026-03-10']
    })),
    ("Over Limit Customer", pd.DataFrame({
        'Customer ID': [1, 1, 1],
        'Loan Amount': [3000000, 2000000, 1500000],  # Total > 5M limit
        'Tenure': [120, 96, 60],
        'EMIs paid on Time': [100, 80, 50],
        'Date of Approval': ['2020-01-01', '2022-06-15', '2024-03-10'],
        'End Date': ['2030-01-01', '2030-06-15', '2029-03-10']
    }))
]

for scenario_name, loan_hist in scenarios:
    if not loan_hist.empty:
        loan_hist['Date of Approval'] = pd.to_datetime(loan_hist['Date of Approval'])
        loan_hist['End Date'] = pd.to_datetime(loan_hist['End Date'])
    
    score = calculate_credit_score_assignment(test_customers[0], loan_hist)
    print(f"{scenario_name}: Credit Score = {score}")
    
    # Apply approval rules
    if score > 50:
        approval_status = "APPROVED - No restrictions"
        min_rate = "As requested"
    elif 30 < score <= 50:
        approval_status = "APPROVED - Interest rate > 12%"
        min_rate = "Minimum 12%"
    elif 10 < score <= 30:
        approval_status = "APPROVED - Interest rate > 16%"
        min_rate = "Minimum 16%"
    else:
        approval_status = "REJECTED"
        min_rate = "N/A"
    
    print(f"  Status: {approval_status}")
    print(f"  Minimum Rate: {min_rate}")
    print()

# EMI to Income ratio validation
def validate_emi_to_income(monthly_salary, new_emi, existing_emis=0):
    """
    Check if total EMIs exceed 50% of monthly salary
    """
    total_emis = new_emi + existing_emis
    max_allowed = monthly_salary * 0.5
    ratio = (total_emis / monthly_salary) * 100
    
    return {
        'total_emis': total_emis,
        'max_allowed': max_allowed,
        'ratio_percentage': round(ratio, 2),
        'approved': total_emis <= max_allowed
    }

print("EMI TO INCOME RATIO VALIDATION:")
print("-" * 40)

# Test EMI validations
salary = 150000
new_loan_emi = calculate_emi(500000, 12, 60)  # ₹11,122

test_cases = [
    (0, "No existing EMIs"),
    (30000, "Some existing EMIs"),
    (60000, "High existing EMIs"),
    (90000, "Very high existing EMIs")
]

for existing_emi, description in test_cases:
    validation = validate_emi_to_income(salary, new_loan_emi, existing_emi)
    
    print(f"{description}:")
    print(f"  Monthly Salary: ₹{salary:,}")
    print(f"  New EMI: ₹{new_loan_emi:,}")
    print(f"  Existing EMIs: ₹{existing_emi:,}")
    print(f"  Total EMIs: ₹{validation['total_emis']:,}")
    print(f"  EMI Ratio: {validation['ratio_percentage']}%")
    print(f"  Max Allowed (50%): ₹{validation['max_allowed']:,}")
    print(f"  Status: {'APPROVED' if validation['approved'] else 'REJECTED (EMI > 50%)'}")
    print()

print("COMPLETE LOAN ELIGIBILITY CHECK PROCESS:")
print("-" * 50)

def check_loan_eligibility(customer_id, customer_data, loan_history, 
                         requested_amount, requested_rate, tenure):
    """
    Complete loan eligibility check as per assignment
    """
    result = {
        'customer_id': customer_id,
        'approval': False,
        'interest_rate': requested_rate,
        'corrected_interest_rate': requested_rate,
        'tenure': tenure,
        'monthly_installment': 0,
        'message': ''
    }
    
    # Step 1: Calculate credit score
    credit_score = calculate_credit_score_assignment(customer_data, loan_history)
    
    # Step 2: Check special rejection conditions
    if credit_score == 0:
        result['message'] = 'Current loans exceed approved limit'
        return result
    
    if credit_score <= 10:
        result['message'] = 'Credit score too low (≤10)'
        return result
    
    # Step 3: Calculate EMI for new loan
    if 30 < credit_score <= 50:
        corrected_rate = max(requested_rate, 12.0)
    elif 10 < credit_score <= 30:
        corrected_rate = max(requested_rate, 16.0)
    else:
        corrected_rate = requested_rate
    
    result['corrected_interest_rate'] = corrected_rate
    monthly_emi = calculate_emi(requested_amount, corrected_rate, tenure)
    result['monthly_installment'] = monthly_emi
    
    # Step 4: Check EMI to income ratio
    # Calculate existing EMIs (simplified - would need current active loans)
    existing_emis = 0  # In real implementation, calculate from active loans
    
    emi_validation = validate_emi_to_income(
        customer_data['Monthly Salary'], 
        monthly_emi, 
        existing_emis
    )
    
    if not emi_validation['approved']:
        result['message'] = f'Total EMIs ({emi_validation["ratio_percentage"]}%) exceed 50% of monthly income'
        return result
    
    # If we reach here, loan is approved
    result['approval'] = True
    result['message'] = 'Loan approved'
    
    return result

# Test complete eligibility check
test_loan_request = {
    'customer_id': 1,
    'customer_data': test_customers[0],
    'loan_history': scenarios[1][1],  # Good payment history
    'requested_amount': 500000,
    'requested_rate': 10.5,
    'tenure': 60
}

eligibility_result = check_loan_eligibility(**test_loan_request)

print("LOAN ELIGIBILITY CHECK RESULT:")
for key, value in eligibility_result.items():
    print(f"  {key}: {value}")