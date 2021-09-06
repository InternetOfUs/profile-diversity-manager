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
