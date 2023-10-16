import pandas as pd
import numpy as np
import os

def ems_billing_activity_transformer(df):
    # rename "AC ID" as "patient_id"
    df.rename(columns={'AC ID': 'patient_id'}, inplace=True)
    # rename "ePCR ID" as "incident_id"
    df.rename(columns={'ePCR ID': 'incident_id'}, inplace=True)
    # create "Unique_ID" column by concatenating "incident_id" and "patient_id" columns
    df['unique_id'] = df['incident_id'] + '-' + df['patient_id']
    # rename "SERV LVL DESC" as "Service_Level"
    df.rename(columns={'SERV LVL DESC': 'service_level'}, inplace=True)
    # rename "ProcedureCode" as "Procedure_Code"
    df.rename(columns={'ProcedureCode': 'procedure_code'}, inplace=True)
    # create "procedure_code_translator" function to map "procedure_code" values to human-readable translations
    def procedure_code_translator(procedure_code):
        if procedure_code == "A0425":
            return "Mileage"
        elif procedure_code == "A0427":
            return "ALS Service"
        elif procedure_code == "A0429":
            return "BLS Service"
        elif procedure_code == "A0433":
            return "ALS2 Service"
        elif procedure_code == "INTEREST":
            return "Interest"
    # apply "procedure_code_translator" function to the contents of the "procedure_code" field and create "billable_service" column
    df['billable_service'] = df['procedure_code'].apply(procedure_code_translator)
    # rename "Disposition" as "disposition_id" indicating this is an ID field
    df.rename(columns={'Disposition': 'disposition_id'}, inplace=True)
    # create "disposition_id_translator_subtype" function to map "disposition_id" values to human-readable translations
    def disposition_id_translator_subtype(disposition_id):
        if disposition_id == "4212001":
            return "Assisted Other EMS Agency"
        elif disposition_id == "4212003":
            return "Assisted With Public Service Call"
        elif disposition_id == "4212005":
            return "Treated, Transported by this EMS unit"
        elif disposition_id == "4212007":
            return "Cancelled Prior To Arrival"
        elif disposition_id == "4212009":
            return "Cancelled On Or After Arrival"
        elif disposition_id == "4212011":
            return "No Patient Found"
        elif disposition_id == "4212015":
            return "DOA, No Resuscitation"
        elif disposition_id == "4212019":
            return "DOA, Resuscitation Attempted, Field Termination"
        elif disposition_id == "4212027":
            return "Treated, Refused Transport"
        elif disposition_id == "4212029":
            return "Treated, Accepted Cab Voucher (APO Diversion)"
        elif disposition_id == "4212031":
            return "Treated, Transfer Care To Other EMS Agency"
        elif disposition_id == "4212033":
            return "Treated, Transported by this EMS unit"
        elif disposition_id == "4212035":
            return "Treated, Referred To Law Enforcement"
        elif disposition_id == "4212039":
            return "Standby, No Patient Found"
    # apply "disposition_id_translator_subtype" function to the contents of the "disposition_id" field and create "incident_subtype" column
    df['incident_subtype'] = df['disposition_id'].apply(disposition_id_translator_subtype)
    # create "disposition_id_translator_type" function to map "disposition_id" values to human-readable translations
    def disposition_id_translator_type(disposition_id):
        if disposition_id in ['4212001', '4212003']:
            return 'Assisted'
        elif disposition_id in ['4212005', '4212027', '4212029', '4212031', '4212033', '4212035']:
            return 'Treated'
        elif disposition_id in ['4212007', '4212009']:
            return 'Cancelled'
        elif disposition_id in ['4212011', '4212039']:
            return 'No Patient'
        elif disposition_id in ['4212015', '4212019']:
            return 'DOA'
    # apply "disposition_id_translator_type" function to the contents of the "disposition_id" field and create "incident_subtype" column
    df['incident_type'] = df['disposition_id'].apply(disposition_id_translator_type)
    # rename "Date of Service" as "incident_date" and cast from datetime to date
    df['incident_date'] = df['Date of Service'].dt.date
    # rename "Invoice" as "invoice_number" indicating this is an invoice number
    df.rename(columns={'Invoice': 'invoice_number'}, inplace=True)
    # rename "Chrg" as "county_fee_amount"
    df.rename(columns={'Chrg': 'county_fee_amount'}, inplace=True)
    # rename "Adjust" as "total_adjustment_amount"
    df.rename(columns={'Adjust': 'total_adjustment_amount'}, inplace=True)
    # rename "ContractualAdjustment" as "contractual_adjustments"
    df.rename(columns={'ContractualAdjustment': 'contractual_adjustments'}, inplace=True)
    # rename "SalesAdjustment" as "sales_adjustments"
    df.rename(columns={'SalesAdjustment': 'sales_adjustments'}, inplace=True)
    # rename "NetCharge" as "billed_amount"
    df.rename(columns={'NetCharge': 'billed_amount'}, inplace=True)
    # rename "Paid" as "paid_amount"
    df.rename(columns={'Paid': 'paid_amount'}, inplace=True)
    # rename "BadDebtAdjustment" as "to_collections_amount"
    df.rename(columns={'BadDebtAdjustment': 'to_collections_amount'}, inplace=True)
    # rename "Due" as "outstanding_amount"
    df.rename(columns={'Due': 'outstanding_amount'}, inplace=True)
    # rename "StatusType" as "cost_recovery_status_id"
    df.rename(columns={'StatusType': 'cost_recovery_id'}, inplace=True)
    # rename "Status" as "billing_status_id"
    df.rename(columns={'StatusType': 'billing_status_id'}, inplace=True)
    # create "cost_recovery_id_translator" function to map "cost_recovery_id" values to human-readable translations
    def cost_recovery_id_translator(cost_recovery_id):
        if cost_recovery_id == "1":
            return "Non-Billable"
        elif cost_recovery_id == "3":
            return "Billable"
    # apply "cost_recovery_id_translator" function to the contents of the "cost_recovery_id" field and create "cost_recovery_status" column
    df['cost_recovery_status'] = df['cost_recovery_id'].apply(cost_recovery_id_translator)
    # create "billing_status_id_translator" function to map "billing_status_id" values to human-readable translations
    def billing_status_id_translator(billing_status_id):
        if billing_status_id == "0":
            return "Pending"
        elif billing_status_id == "1":
            return "Primary Billing, Balance Due"
        elif billing_status_id == "2":
            return "Secondary Billing, Balance Due"
        elif billing_status_id == "3":
            return "Billing Complete (Paid or Collections)"
        elif billing_status_id == "5":
            return "Negotiating"
        elif billing_status_id == "7":
            return "Refund"
    # apply "billing_status_id_translator" function to the contents of the "billing_status_id" field and create "billing_status" column
    df['billing_status'] = df['billing_status_id'].apply(billing_status_id_translator)
    # rename "Carrier Name" as "billed_party"
    df.rename(columns={'Carrier Name': 'billed_party'}, inplace=True)
    # rename "Active Carrier" as "billed_party_current"
    df.rename(columns={'Active Carrier': 'billed_party_current'}, inplace=True)
    # create "billed_party_status" column to denote active billing rows
    df['billed_party_status'] = np.where(df['billed_party'] == df['billed_party_current'], 'Active', 'Not Active')
    # rename "OriginalSaleDate" as "billable_incident_create_date" and cast from datetime to date
    df['billable_incident_create_date'] = df['OriginalSaleDate'].dt.date
    # rename "SaleDate" as "billed_party_create_date" and cast from datetime to date
    df['billed_party_create_date'] = df['SaleDate'].dt.date
    # rename "OriginalSubmitDate" as "first_bill_submission_date" and cast from datetime to date
    df['first_bill_submission_date'] = df['OriginalSubmitDate'].dt.date
    # rename "GoToCollectionDate" as "to_collections_date" and cast from datetime to date
    df['to_collections_date'] = df['GoToCollectionDate'].dt.date
    # rename "ClosedDate" as "closed_date" and cast from datetime to date
    df['closed_date'] = df['ClosedDate'].dt.date
    # rename "Submit Date (Most Recent)" as "closed_date" and cast from datetime to date
    df['most_recent_billing_date'] = df['Submit Date (Most Recent)'].dt.date
    # rename "Deposit Date (Most Recent)" as "payment_deposit_date" and cast from datetime to date
    df['payment_deposit_date'] = df['Deposit Date (Most Recent)'].dt.date
    # rename "Remit Date (Most Recent)" as "payment_remit_date" and cast from datetime to date
    df['payment_remit_date'] = df['Remit Date (Most Recent)'].dt.date
    # rename "Collect Date (Most Recent)" as "payment_from_collections_date" and cast from datetime to date
    df['payment_from_collections_date'] = df['Collect Date (Most Recent)'].dt.date
    # rename "Complete" as "complete_date" and cast from datetime to date
    df['complete_date'] = df['Complete'].dt.date
    # rename "Denial Reason (Most Recent)" as "denial_reason"
    df.rename(columns={'Denial Reason (Most Recent)': 'denial_reason'}, inplace=True)
    # rename "DoNotBillPatient" as "dont_bill_patient_bin"
    df.rename(columns={'DoNotBillPatient': 'donot_bill_patient_bin'}, inplace=True)
    return df

def process_csv(input_file, output_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Apply data transformations
    df = ems_billing_activity_transformer(df)

    # Save the transformed data to a new CSV file
    df.to_csv(output_file, index=False)

input_files = ["FY21 - EMS BILLING ACTIVITY.CSV"]
output_files = ["EMS Billing Activity FY21 Transformed.csv"]

for i, input_file in enumerate(input_files):
    output_file = output_files[i]
    process_csv(input_file, output_file)