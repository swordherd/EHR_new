# -*- coding: utf-8 -*-

"""Get Data from icu patient dataset

There are some function about the data preprocessing and data getting
"""

import os
import sqlite3
import json
import numpy as np

# the absolute path about
file = os.path.abspath('Data/identifier.sqlite')


def get_sql(data_type):
    """Get the correct SQL

    :param Datatype: the data type which you want to get from dataset

    :return: A string type which is about the detailed sql
    """
    SQL = {
        'Patient': 'Select patientunitstayid, '
                   'gender, '
                   'age, '
                   'ethnicity, '
                   'admissionheight, '
                   'admissionweight '
                   'From patient;',

        'pastHistory': 'Select pasthistoryid, '
                       'patientunitstayid, '
                       'pasthistoryoffset, '
                       'pasthistoryvaluetext '
                       'From pastHistory;',

        'Diagnosis': 'Select diagnosisid, '
                     'patientunitstayid, '
                     'diagnosisstring, '
                     'icd9code, '
                     'diagnosispriority '
                     'From diagnosis',

        'Lab': 'Select labid, '
               'patientunitstayid, '
               'labname, '
               'labresulttext '
               'From lab',

        'diagnosis': 'Select diagnosisid,'
                     'diagnosisoffset,'
                     'diagnosisstring,'
                     'activeupondischarge '
                     'From diagnosis',

        'treatment': 'Select treatmentid,'
                     'treatmentoffset, '
                     'treatmentstring,'
                     'activeupondischarge '
                     'From treatment',

        'past_history': 'Select * '
                        'From pastHistory',

        'lab': 'Select * '
               'From lab',
    }
    return SQL[data_type]


def open_db(db_path=file):
    return sqlite3.connect(db_path)


def get_data(dataset, data_type=None):
    """Get data form dataset

    :param dataset:
    :param data_type: the data type witch user want to get

    :return: A list about the getting data from dataset
    """

    sql = get_sql(data_type)
    cursor = dataset.execute(sql)
    data = cursor.fetchall()

    return data


def get_info_by_id(dataset, table, attributes, patient_id):
    """Get the information which users want to get by patient id from dataset

    :param attributes:
    :param dataset:
    :param table:
    :param patient_id:
    :return:
    """

    sql = "Select "
    for attribute in attributes:
        sql += attribute + ', '
    sql += ('From ' + table + ' where patientunitstayid == ' + patient_id)

    cursor = dataset.execute(sql)
    info = cursor.fetchall()
    return info


def get_patient_history(patient_id, patient_history):
    """Get the patient disease history from dataset

    :param patient_id: Patient unique id
    :param patient_history: All history records about patient's disease

    :return: A list about the selected patient's history with temporal order
    """

    select_history = []
    patient_id_history = [row[1] for row in patient_history]

    if patient_id not in patient_id_history:
        return 0

    for history_data in enumerate(patient_history):
        if patient_id == history_data[1]:
            select_history.append(history_data)

    select_history.sort(key=lambda x: x[2])

    return select_history


def get_detail_by_id(dbpath=file, patients_id=None):
    """Get more detail by patient id

    :param dbpath: dataset path
    :param patients_id: patientunitstayid
    :return: A json object about patient detail information
    """

    detail_info = {}
    detail = json.loads(json.dumps(detail_info))
    db = sqlite3.connect(dbpath)

    for patient_id in patients_id:
        patient_detail = {"id": patient_id}
        entities = ['diagnosis',
                    'treatment',
                    'past_history',
                    'lab']
        where = ' where by patient == ' + patient_id

        for entity in entities:
            cursor = db.execute(get_sql(entity) + where)
            patient_detail[entity] = cursor.fetchall()


def get_patients_by_id(patients_id):
    """

    :param patients_id:
    :return:
    """

    dataset = open_db()
    tables = ['patient', 'apachePatientResult', 'diagnosis', 'treatment', 'pastHistory', ]  # 'admissiondrug'
    attributes = {
        'apachePatientResult': [['apachescore'],
                                ['predictedhospitalmortality',
                                 'actualhospitalmortality',
                                 'predictedicumortality',
                                 'actualicumortality'],
                                ['predictedhospitallos',
                                 'actualhospitallos',
                                 'predictediculos',
                                 'actualiculos'],
                                ],
        'diagnosis': ['diagnosisid',
                      'diagnosisoffset',
                      'diagnosisstring',
                      'activeupondischarge'
                      ],
        'treatment': ['treatmentid',
                      'treatmentoffset',
                      'treatmentstring',
                      'activeupondischarge'
                      ],
        'pastHistory': ['pasthistoryid',
                        'pasthistoryoffset',
                        'pasthistoryvalue']

    }
    patients_info = []
    for patient_id in patients_id:
        patient_info = {"id": patient_id}
        for table in tables:

            if table == 'patient':
                info_age = get_info_by_id(dataset, table, ['age'], patient_id)
                if '>' in info_age:
                    patient_info['age'] = 90
                else:
                    patient_info['age'] = int(info_age)
                patient_info['gender'] = get_info_by_id(dataset, table, ['gender'], patient_id)

            elif table == 'apachePatientResult':
                for i, attribute in enumerate(attributes['apachePatientResult']):
                    if i == 1:
                        patient_info['apachescore'] = get_info_by_id(dataset, table, attribute, patient_id)
                    elif i == 2:
                        morality = []
                        moralities = {}
                        info = get_info_by_id(dataset, table, attribute, patient_id)
                        for info_i in info:
                            for index, att in enumerate(info_i):
                                moralities[attribute[index]] = att
                            morality.append(moralities)
                        patient_info['morality'] = morality
                    elif i == 3:
                        los = []
                        Los ={}
                        info = get_info_by_id(dataset, table, attribute, patient_id)
                        for info_i in info:
                            for index, att in enumerate(info_i):
                                Los[attribute[index]] = att
                            los.append(Los)
                        patient_info['LOS'] = los

            else:
                attribute = attributes[table]
                info = get_info_by_id(dataset, table, attribute, patient_id)
                context = []
                Context = {}
                for info_i in info:
                    for index, att in enumerate(info_i):
                        Context[attribute[index]] = att
                    context.append(Context)
                patient_info[table] = context
            
                        # for index, name in enumerate(attribute):
                        #     patient_info[name] = info[]




if __name__ == "__main__":
    db = open_db()
    print(get_data(db, 'Patient'))

    db.close()
