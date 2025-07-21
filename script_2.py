# Additional analysis for understanding the credit system
print("Customer-Loan Relationship Analysis:")
print("=" * 50)

# Count loans per customer
loans_per_customer = loan_data['Customer ID'].value_counts().sort_index()
print(f"Customers with loans: {len(loans_per_customer)}")
print(f"Total customers in database: {len(customer_data)}")
print(f"Customers without loans: {len(customer_data) - len(loans_per_customer)}")

print("\nLoans per customer distribution:")
print(loans_per_customer.value_counts().sort_index())

# Current debt analysis (assuming ongoing loans)
from datetime import datetime
current_date = datetime(2025, 7, 21)  # Current date as per prompt
loan_data['Date of Approval'] = pd.to_datetime(loan_data['Date of Approval'])
loan_data['End Date'] = pd.to_datetime(loan_data['End Date'])

# Active loans (end date > current date)
active_loans = loan_data[loan_data['End Date'] > current_date]
print(f"\nActive loans: {len(active_loans)}")
print(f"Completed loans: {len(loan_data) - len(active_loans)}")

# Payment performance analysis
loan_data['Payment Ratio'] = loan_data['EMIs paid on Time'] / loan_data['Tenure']
print(f"\nPayment Performance Statistics:")
print(f"Average payment ratio: {loan_data['Payment Ratio'].mean():.2f}")
print(f"Perfect payment customers: {len(loan_data[loan_data['Payment Ratio'] >= 1.0])}")
print(f"Poor payment customers (< 50% on time): {len(loan_data[loan_data['Payment Ratio'] < 0.5])}")

# Approved limit vs salary relationship
customer_data['Limit_to_Salary_Ratio'] = customer_data['Approved Limit'] / customer_data['Monthly Salary']
print(f"\nApproved Limit Analysis:")
print(f"Average limit to salary ratio: {customer_data['Limit_to_Salary_Ratio'].mean():.2f}")
print(f"Expected ratio (36x): 36")
print(f"Min ratio: {customer_data['Limit_to_Salary_Ratio'].min():.2f}")
print(f"Max ratio: {customer_data['Limit_to_Salary_Ratio'].max():.2f}")