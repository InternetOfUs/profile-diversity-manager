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

from enum import Enum
import json
from math import comb
import os
import time

from WNS import sim_str_str, sim_str_str_multiling
from diversity import Attribute, Agent, QN, diversity
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict


# Setup Web services
app  = FastAPI(
    title="ProfileDiversityManager",
    description="Extension of the profile manager to manage the diversity.",
    version="0.1.0"
)

# The type of statistic function
class Aggregation(str, Enum):
    max = "max"
    mean = "mean"
    q75 = "q75"
    q90 = "q90"

class Info(BaseModel):
    name: str = Field(...,description="Contain the name of the API.",example="wenet/profile-diversity-manager")
    apiVersion: str = Field(...,description="Contain the name of the API.",example="1.0.0")
    softwareVersion: str = Field(...,description="Contain the implementation version number of the software.",example="1.0.0")
    vendor: str = Field(...,description="Contain information of the organization that has implemented the API.",example="UDT-IA, IIIA-CSIC")
    license: str = Field(...,description="Contain information of the license of the API.",example="Apache v2")
    
class StringsData(BaseModel):
    source: str = Field(...,description="Source string to obtain the similarity.",example="I hate planes")
    
class UserData(BaseModel):
    id: str = Field(...,description="Contain the identifier of the user.",example="bgduy367825jg")
    attributes: Dict[str,float] = Field(...,ge=0.0,le=1.0,description="The attributes of the user, where the key is the name and the value is a number on the range [0,1].")

class UsersData(BaseModel):
    users:List[UserData] = Field(...,description="A set of users to use.")
    
class Diversity(BaseModel):
    value: float = Field(...,ge=0.0,le=1.0,description="The diversity of a set of users.")

@app.get(
    "/help/info",
    description="Obtain information of the extension",
    status_code=200,
    response_model=Info
)
async def get_help_info():
    
    return {
        "name": "wenet/profile-diversity-manager",
        "apiVersion": "0.1.0",
        "softwareVersion": "0.1.0",
        "vendor": "UDT-IA, IIIA-CSIC",
        "license": "Apache v2"
    } 

@app.post(
    "/calculateDiversityOf",
    description="Obtain the diversity that is formed per  a set of users",
    status_code=200,
    response_model=Diversity
)
async def post_calculate_diversity_of(data:UsersData):
    
    agents = []
    reqattr = []
    defined_attributes = set()
    for user in data.users:
        agent_attributes = []
        for attribute_id in user.attributes:
            # Create the user attribute
            attribute = Attribute(attribute_id,QN,[0,1], user.attributes[attribute_id])
            agent_attributes.append(attribute)
            if attribute_id not in defined_attributes:
                # Add the attribute as defined
                reqattr.append(Attribute(attribute_id,QN,[0,1]))
                defined_attributes.add(attribute_id)
            
        # Create the agent for the user
        agents.append(Agent(user.id,agent_attributes))
        
    # Calculate the diversity of the agents
    users_diversity = diversity(agents,reqattr)
    ## !!!! THE NEXT LINE IS ONLY BECAUSE DO AN AGGREGATION
    users_diversity /= len(reqattr)
    return {
        "value": users_diversity
    } 

