#
# Copyright 2019 - 2022 UDT-IA, IIIA-CSIC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
import pytest
import uuid

from fastapi.testclient import TestClient
from main import app
from pytest_httpserver import HTTPServer

client = TestClient(app)


@pytest.mark.timeout(30)
def test_get_help_info():
    """Test get help info of the API"""
    response = client.get("/help/info")
    assert response.status_code == 200
    body = response.json()
    assert 'name' in body
    assert 'apiVersion' in body
    assert 'softwareVersion' in body
    assert 'vendor' in body
    assert 'license' in body


@pytest.mark.timeout(30)
def test_post_calculate_diversity_of():
    """Test calculate diversity of two agents"""
    data = {
        "agents":[
                {
                    "id":"1",
                    "quantitativeAttributes":{
                            "introvert":1.0,
                            "extrovert":1.0,
                            "naturalist":1.0
                    },
                    "qualitativeAttributes":{
                            "gender":"M",
                            "civilStatus":"married"
                    }
                },
                {
                    "id":"2",
                    "quantitativeAttributes":{
                            "introvert":0.0,
                            "extrovert":0.0,
                            "naturalist":0.0
                    },
                    "qualitativeAttributes":{
                            "gender":"F",
                            "civilStatus":"single"
                    }
                }
            ],
        "qualitativeAttributes": {
                "gender":["M", "F", "O"],
                "civilStatus":["single", "married", "divorced", "widow"]
            },
        "quantitativeAttributes": ["introvert", "extrovert", "naturalist"]
        }
    response = client.post("/calculateDiversityOf", json=data)
    assert response.status_code == 200
    assert response.json() == {"value":0.5261859507142914}


@pytest.mark.timeout(30)
def test_post_calculate_diversity_of_none_agents():
    """Test calculate diversity of none agents"""
    data = {
        "qualitativeAttributes": {
                "gender":["M", "F", "O"],
                "civilStatus":["single", "married", "divorced", "widow"]
            },
        "quantitativeAttributes": ["introvert", "extrovert", "naturalist"]
        }
    response = client.post("/calculateDiversityOf", json=data)
    assert response.status_code == 200
    assert response.json() == {"value":0.0}


@pytest.mark.timeout(30)
def test_post_calculate_diversity_of_none_attribues():
    """Test calculate diversity of none attributes"""
    data = {
        "agents":[
                {
                    "id":"1",
                    "quantitativeAttributes":{
                            "introvert":1.0,
                            "extrovert":1.0,
                            "naturalist":1.0
                    },
                    "qualitativeAttributes":{
                            "gender":"M",
                            "civilStatus":"married"
                    }
                },
                {
                    "id":"2",
                    "quantitativeAttributes":{
                            "introvert":0.0,
                            "extrovert":0.0,
                            "naturalist":0.0
                    },
                    "qualitativeAttributes":{
                            "gender":"F",
                            "civilStatus":"single"
                    }
                }
            ]
        }
    response = client.post("/calculateDiversityOf", json=data)
    assert response.status_code == 200
    assert response.json() == {"value":0.0}


@pytest.mark.timeout(30)
def test_post_calculate_similarity_of():
    """Test similarity some attributes"""
    data = {
        "source":"Do you have a bike?",
        "attributes":["car", "vehicle", "plane" ]
        }
    response = client.post("/calculateSimilarityOf", json=data)
    assert response.status_code == 200
    assert response.json() == {"similarities":[{"attribute":"car", "similarity":0.6239031848677311}, {"attribute":"vehicle", "similarity":0.6239031848677311}, {"attribute":"plane", "similarity":0.0}]}


@pytest.mark.timeout(30)
def test_post_calculate_similarity_of_none_attributes():
    """Test similarity without attributes"""
    data = {
        "source":"Do you have a bike?"
        }
    response = client.post("/calculateSimilarityOf", json=data)
    assert response.status_code == 200
    assert response.json() == {"similarities":[]}
