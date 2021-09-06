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

import pytest
from WNS import sim_str_str, sim_str_str_multiling, sim_str_attrlst, sim_str_attrlst_multiling


@pytest.mark.timeout(30)
def test_sim_str_str_es_es():
    """Test the similarity between two strings"""
    sim = sim_str_str("Odio los aviones", "No me gustan los helicópteros", lang1="es", lang2="es", stat="max")
    assert 0.0 <= sim <= 1.0


@pytest.mark.timeout(30)
def test_sim_str_str_zh_zh():
    """Test the similarity between two strings"""
    sim = sim_str_str("支持四种分词模式", "支持四种分词模式", lang1="zh", lang2="zh", stat="max")
    assert 0.0 <= sim <= 1.0


@pytest.mark.timeout(30)
def test_sim_str_str_multiling():
    """Test the similarity between two strings detecting language before"""
    sim = sim_str_str_multiling("I hate planes", "No me gustan los helicópteros", stat="max")
    assert 0.0 <= sim <= 1.0


@pytest.mark.timeout(30)
def test_sim_str_attrlst_es_es():
    """Test the similarity between a string an a set of attributes"""
    pairs = [("profesión", "programador aplicaciones"), ("afición", "escalada")]
    sims = sim_str_attrlst("Estoy probando esta nueva aplicación en mi portátil conectado a internet.", pairs, lang1="es", lang2="es", stat="max")
    assert len(pairs) == len(sims)
    for pair in pairs:
        for sim in sims:
            if pair[0] == sim[0]:
                assert pair[1] == sim[1]
                assert 0.0 <= sim[2] <= 1.0
                break;


@pytest.mark.timeout(30)
def test_sim_str_attrlst_multiling():
    """Test the similarity between a string an a set of attributes detecting language"""
    pairs = [("occupation", "app developer"), ("hobby", "climbing")]
    sims = sim_str_attrlst_multiling("Estoy probando esta nueva aplicación en mi portátil conectado a internet.", pairs, stat="max")
    assert len(pairs) == len(sims)
    for pair in pairs:
        for sim in sims:
            if pair[0] == sim[0]:
                assert pair[1] == sim[1]
                assert 0.0 <= sim[2] <= 1.0
                break;
