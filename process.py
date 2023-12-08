# -*- coding: utf-8 -*-

"""Process the data

Padding, Delete, Replace and so on
"""

import gensim
from getdata import get_data


def ethnicity2int(eth):
    """Encoding the ethnicity to int

    :param eth: the ethnicity need to encoder

    :return: code
    """

    Eth = {
        '': 0,
        'Caucasian': 1,
        'Hispanic': 2,
        'Asian': 3,
        'African American': 4,
        'Native American': 5,
        'Other/Unknown': 6,
    }
    return Eth[eth]


def data_processing(data, data_type):
    """

    :param data:
    :param data_type:
    :return:
    """

    Data = []  # orig data
    Data_new = []  # processed data
    example = []
    drop = []  # dropping data

    for row in data:
        for attribute in row:
            if not attribute:
                example.append(None)
            else:
                example.append(attribute)
        Data.append(example)

        if None in example:  # If example exists None value, Drop the data
            drop.append(example)
        else:
            Data_new.append(example)
        example = []

    if data_type == 'Patient':  # Process the Patient basic information data
        for row in Data_new:
            for index, attribute in enumerate(row):
                if index == 0:
                    continue

                elif index == 1:
                    if attribute == 'Felmale':
                        row[index] = int(0)
                    else:
                        row[index] = int(1)

                elif index == 2:
                    if '>' in attribute:
                        row[index] = int(90)
                    else:
                        row[index] = int(data)

                elif index == 3:
                    row[index] = ethnicity2int(attribute)

                else:
                    row[index] = float(attribute)

    elif data_type == 'pastHistory':
        return Data_new

    elif data_type == 'Diagnosis':
        return Data_new

    elif data_type == 'Lab':
        for row in Data_new:
            for index, attribute in enumerate(row):
                if index == 3:
                    row[index] = int(data)

    else:
        return Data_new

    return Data_new


def train(sentences):
    """

    :param sentences:
    :return:
    """
    model = gensim.models.Word2Vec(sentences,
                                   vector_size=100,
                                   sg=1,
                                   window=3,
                                   min_count=1)
    model.wv.save_word2vec_format('model/model1', binary=False)


    return model


def data_padding():
    """

    :return:
    """
    diagnosis_ = [row[2] for row in get_data(data_type='Diagnosis')]
    diagnosis_dic = []
    diagnosis_dic_ = []

    for diagnosis in diagnosis_:
        # context = ""
        context = []

        for sub_diagnosis in diagnosis.split("|"):
                # context += sub_diagnosis + ' '
                context.append(sub_diagnosis)

        if diagnosis not in diagnosis_dic_:
            diagnosis_dic_.append(diagnosis)
        if context not in diagnosis_dic:
            diagnosis_dic.append(context)

    train(diagnosis_dic)

    with open('model/model1', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            print(index, len(line))


if __name__ == '__main__':
    data_padding()