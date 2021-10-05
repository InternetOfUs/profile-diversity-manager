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
from diversity import Agent, Attribute, QN, diversity


@pytest.mark.timeout(30)
def test_calculate_diversity_for_oposed_agents():
    """Test the diversity over two equals agents"""
    agents = [
        Agent("1234", [
            Attribute("property1", QN, [0, 1], 1),
            Attribute("property2", QN, [0, 1], 1),
            Attribute("property3", QN, [0, 1], 1)
            ]),
        Agent("abcd", [
            Attribute("property1", QN, [0, 1], 0),
            Attribute("property2", QN, [0, 1], 0),
            Attribute("property3", QN, [0, 1], 0)
            ])
    ]
    reqattr = [Attribute("property1", QN, [0, 1]), Attribute("property2", QN, [0, 1]), Attribute("property3", QN, [0, 1])]
    div = diversity(agents, reqattr)
    assert div == 0.5


@pytest.mark.timeout(30)
def test_calculate_diversity_for_equals_agents():
    """Test the diversity over two equals agents"""
    agents = [
        Agent("1234", [
            Attribute("property1", QN, [0, 1], 1),
            Attribute("property2", QN, [0, 1], 1),
            Attribute("property3", QN, [0, 1], 1)
            ]),
        Agent("abcd", [
            Attribute("property1", QN, [0, 1], 1),
            Attribute("property2", QN, [0, 1], 1),
            Attribute("property3", QN, [0, 1], 1)
            ])
    ]
    reqattr = [Attribute("property1", QN, [0, 1]), Attribute("property2", QN, [0, 1]), Attribute("property3", QN, [0, 1])]
    div = diversity(agents, reqattr)
    assert  div == 0.0


@pytest.mark.timeout(30)
def test_calculate_diversity_for_different_agents():
    """Test the diversity over two equals agents"""
    agents = [
        Agent("1234", [
            Attribute("property1", QN, [0, 1], 0.1),
            Attribute("property2", QN, [0, 1], 1),
            Attribute("property3", QN, [0, 1], 0.91)
            ]),
        Agent("abcd", [
            Attribute("property1", QN, [0, 1], 0.742),
            Attribute("property2", QN, [0, 1], 0.67),
            Attribute("property3", QN, [0, 1], 0.28)
            ])
    ]
    reqattr = [Attribute("property1", QN, [0, 1]), Attribute("property2", QN, [0, 1]), Attribute("property3", QN, [0, 1])]
    div = diversity(agents, reqattr)
    assert 0.0 <= div <= 1.0
