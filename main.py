# -*- coding: utf-8 -*-

import getdata
from getdata import get_patients_by_id
import cluster as clu
from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/get_cluster/', methods=['POST'])
def get_cluster():
    """

    :return:
    """
    cluster_count = request.form["cluster_count"]

    # process cluster
    CLUSTER = cluster

    return CLUSTER


@app.route('/cluster')
def cluster(CLUSTER):
    """

    :param CLUSTER:
    :return:
    """
    return CLUSTER.result()


@app.route('/fetch_detail_by_id_param', methods=["POST"])
def fetch_detail_by_id_param():
    """

    :return:
    """
    param = request.form[""]


@app.route('/fetch_detail_by_id')
def fetch_detail_by_id(patient_id):
    """

    :param patient_id:
    :return:
    """
    return getdata.get_detail_by_id(patient_id)


@app.route('/similarity_of_cluster')
def similarity_of_cluster(CLUSTER):
    """

    :param CLUSTER:
    :return:
    """
    return CLUSTER.similarity()


@app.route('/fetch_patients_by_id', methods=["POST"])
def fetch_patients_by_id():
    """

    :param patients_id:
    :return:
    """

    patients_id = request.form["patients_id"]

    if not patients_id:
        raise ValueError

    return get_patients_by_id(patients_id)


if __name__ == '__main__':
    app.run()
