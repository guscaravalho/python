import pandas as pd
import numpy as np
import os

def ems_all_incidents_transformer(df):
    # rename "AC ID" as "patient_id"
    df.rename(columns={'AC ID': 'patient_id'}, inplace=True)
    # rename "ePCR ID" as "incident_id"
    df.rename(columns={'ePCR ID': 'incident_id'}, inplace=True)
    # cast "patient_id" and "incident_id" columns to strings so they're able to concatenate
    df['patient_id'] = df['patient_id'].astype(str)
    df['incident_id'] = df['incident_id'].astype(str)
    # create unique "incident_patient_id" column by concatenating "incident_id" and "patient_id" columns
    df['incident_patient_id'] = df['incident_id'] + '-' + df['patient_id']
    # rename "SERV LVL DESC" as "Service_Level"
    df.rename(columns={'SERV LVL DESC': 'service_level'}, inplace=True)
    # rename "Disposition" as "disposition_id" indicating this is an ID field and then cast as string and truncate to only first 7 characters
    df.rename(columns={'Disposition': 'disposition_id'}, inplace=True)
    df['disposition_id'] = df['disposition_id'].astype(str)
    df['disposition_id'] = df['disposition_id'].str[:7]
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
        elif disposition_id == "4212902":
            return "Treated, Transferred Care to Telehealth Provider"
        else:
            print(f"Unmatched disposition_id: {disposition_id}")
            return "Unmatched"
    # apply "disposition_id_translator_subtype" function to the contents of the "disposition_id" field and create "incident_subtype" column
    df['incident_subtype'] = df['disposition_id'].apply(disposition_id_translator_subtype)
    # create "disposition_id_translator_type" function to map "disposition_id" values to human-readable translations
    def disposition_id_translator_type(disposition_id):
        if disposition_id in ['4212001', '4212003']:
            return 'Assisted'
        elif disposition_id in ['4212005', '4212027', '4212029', '4212031', '4212033', '4212035', "4212902"]:
            return 'Treated'
        elif disposition_id in ['4212007', '4212009']:
            return 'Cancelled'
        elif disposition_id in ['4212011', '4212039']:
            return 'No Patient'
        elif disposition_id in ['4212015', '4212019']:
            return 'DOA'
    # apply "disposition_id_translator_type" function to the contents of the "disposition_id" field and create "incident_subtype" column
    df['incident_type'] = df['disposition_id'].apply(disposition_id_translator_type)
    # rename "Cancel Reason" as "incident_cost_recovery_status"
    df.rename(columns={'Cancel Reason': 'incident_cost_recovery_status'}, inplace=True)
    # rename "Date of Service" as "incident_date"
    df.rename(columns={'Date of Service': 'incident_date'}, inplace=True)
    # rename "Trip Type Name" as "trip_type" indicating this is an invoice number
    df.rename(columns={'Trip Type Name': 'trip_type'}, inplace=True)
    # rename "Destination Name" as "destination"
    df.rename(columns={'Destination Name': 'destination'}, inplace=True)
    # rename "Diagnosis 1 Description" as "diagnosis1"
    df.rename(columns={'Diagnosis 1 Description': 'diagnosis1'}, inplace=True)
    # rename "Diagnosis 1 Shortcut" as "diagnosis1_code"
    df.rename(columns={'Diagnosis 1 Shortcut': 'diagnosis1_code'}, inplace=True)
    # rename "Diagnosis 2 Description" as "diagnosis2"
    df.rename(columns={'Diagnosis 2 Description': 'diagnosis2'}, inplace=True)
    # rename "Diagnosis 2 Shortcut" as "diagnosis2_code"
    df.rename(columns={'Diagnosis 2 Shortcut': 'diagnosis2_code'}, inplace=True)
    # rename "Modifier1" as "modifier1"
    df.rename(columns={'Modifier1': 'modifier1'}, inplace=True)
    # rename "Modifier2" as "modifier2"
    df.rename(columns={'Modifier2': 'modifier2'}, inplace=True)
    # rename "Origin Street1" as "origin_street_address"
    df.rename(columns={'Origin Street1': 'origin_street_address'}, inplace=True)
    # rename "Origin City" as "origin_city"
    df.rename(columns={'Origin City': 'origin_city'}, inplace=True)
    # rename "Origin County" as "origin_county"
    df.rename(columns={'Origin County': 'origin_county'}, inplace=True)
    # rename "Origin State" as "origin_state"
    df.rename(columns={'Origin State': 'origin_state'}, inplace=True)
    # rename "Origin Zip" as "origin_zip"
    df.rename(columns={'Origin Zip': 'origin_zip'}, inplace=True)
    # rename "Vehicle" as "ems_vehicle_number"
    df.rename(columns={'Vehicle': 'ems_vehicle_number'}, inplace=True)
    # set columns in logical order
    df = df[['incident_patient_id', 'incident_id', 'patient_id', 'trip_type', 'service_level', 'incident_type', 'incident_subtype', 'incident_cost_recovery_status', 'incident_date', 'ems_vehicle_number', 'destination', 'diagnosis1', 'diagnosis1_code', 'diagnosis2', 'diagnosis2_code', 'modifier1', 'modifier2', 'origin_street_address', 'origin_city', 'origin_county', 'origin_state', 'origin_zip', 'disposition_id']]
    return df

# find the raw data and transform it
def process_csv(input_file, output_file):
    # open and read .csv file
    df = pd.read_csv(input_file)
    # apply data transformations
    df = ems_all_incidents_transformer(df)
    # output transformed data as a new .csv file
    df.to_csv(output_file, index=False)

# use this list of input and output .csv files in the same directory as this python script
input_files = ["EMS ALL INCIDENTS FY21.CSV", "EMS ALL INCIDENTS FY22.CSV", "EMS ALL INCIDENTS FY23.CSV"]
output_files = ["Transformed Data/EMS All Incidents FY21 Transformed.csv", "Transformed Data/EMS All Incidents FY22 Transformed.csv", "Transformed Data/EMS All Incidents FY23 Transformed.csv"]

# loop over all the listed .csv files to create their coorseponding output files
for i, input_file in enumerate(input_files):
    output_file = output_files[i]
    process_csv(input_file, output_file)