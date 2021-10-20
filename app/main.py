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

from WNS import sim_str_str, detect_lang
from diversity import Attribute, Agent, QN, QL, diversity
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict


# Setup Web services
app  = FastAPI(
    title="ProfileDiversityManager",
    description="Extension of the profile manager to manage the diversity.",
    version="0.1.0"
)

# Obtain information of the API
class Info(BaseModel):
    name: str = Field(...,description="Contain the name of the API.",example="wenet/profile-diversity-manager")
    apiVersion: str = Field(...,description="Contain the name of the API.",example="1.0.0")
    softwareVersion: str = Field(...,description="Contain the implementation version number of the software.",example="1.0.0")
    vendor: str = Field(...,description="Contain information of the organization that has implemented the API.",example="UDT-IA, IIIA-CSIC")
    license: str = Field(...,description="Contain information of the license of the API.",example="Apache v2")
    
# Information of an agent to obtain the diversity
class AgentData(BaseModel):
    id: str = Field(...,description="Contain the identifier of the agent.",example="1")
    quantitativeAttributes: Dict[str,float] = Field({},ge=0.0,le=1.0,description="The quantitative attributes of the agent, where the key is the name of the attribute and the value is a number on the range [0,1] that represents the attribute value.",example="{\"introvert\":0.5,\"extrovert\":0.0,\"naturalist\":1.0}")
    qualitativeAttributes: Dict[str,str] = Field({},description="The qualitative attributes of the agent, where the key is the attribute name and the value is a string with the attribute value.",example="{\"gender\":\"F\",\"civilStatus\":\"single\"}")

# Set of agents to calculate its diversity
class AgentsData(BaseModel):
    agents:List[AgentData] = Field([],min_items=2,description="A set of agents to use.")
    qualitativeAttributes: Dict[str,List[str]] = Field({},description="The name and the possible values of the qualitative attributes, where the key is the name of the attribute and the value is a list with the possible values.",example="{\"gender\":[\"M\",\"F\",\"O\"],\"civilStatus\":[\"single\",\"married\",\"divorced\",\"widow\"]}")
    quantitativeAttributes: List[str] = Field([],description="The name of the quantitative attributes",example="[\"introvert\",\"extrovert\",\"naturalist\"]")
    
# The diversity of some users
class Diversity(BaseModel):
    value: float = Field(...,ge=0.0,le=1.0,description="The diversity of a set of users.")

# The type of statistic function
class Aggregation(str, Enum):
    max = "max"
    mean = "mean"
    q75 = "q75"
    q90 = "q90"

# The data to filter the attributes
class AttributesToFilterBySimilarity(BaseModel):
    source: str = Field(...,description="Source string to obtain the similarity.",example="I hate planes")
    attributes: List[str] = Field(...,description="Attributes to filter",example="[\"attribute1\",\"attribute2\"]")
    aggregation: Aggregation = Field("max",description="The aggregation value to use")
    threshold: float = Field(0.5,ge=0.0,le=1.0,description="The minimum similarity to the attributes to filter")

class FilteredAttributes(BaseModel):
    attributes: List[str] = Field(...,description="Attributes that has been filtered filter")
    
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
async def post_calculate_diversity_of(data:AgentsData):

    users_diversity = 0.0
    try:
        reqattr = []
        for attrName in data.quantitativeAttributes:
            
            reqattr.append(Attribute(attrName,QN,[0,1]))
    
        for attrName in data.qualitativeAttributes:
            
            reqattr.append(Attribute(attrName,QL,data.qualitativeAttributes[attrName]))
    
        max = len(reqattr)
        if max > 0:
            
            agents = []
            for agentData in data.agents:
                agent_attributes = []
                for attrName in agentData.quantitativeAttributes:
                
                    agent_attributes.append(Attribute(attrName,QN,[0,1],agentData.quantitativeAttributes[attrName]))
        
                for attrName in agentData.qualitativeAttributes:
                
                    agent_attributes.append(Attribute(attrName,QL,data.qualitativeAttributes[attrName],agentData.qualitativeAttributes[attrName]))
        
                agents.append(Agent(agentData.id,agent_attributes))
                
            if len(agents) > 0:
                # Calculate the diversity of the agents
                users_diversity = diversity(agents,reqattr)
                users_diversity /= max # To normalize on the range [0,1]
    except:
        #Ignore exceptions
        users_diversity = 0.0                
    return {
        "value": users_diversity
    } 

@app.post(
    "/filterAttributesBySimilarity",
    description="Filter a set of attributes by its similarity to a text",
    status_code=200,
    response_model=FilteredAttributes
)
async def post_filter_attributes_by_similarity(data:AttributesToFilterBySimilarity):
    
    attributes = []
    source_lang = detect_lang(data.source)
    for attribute in data.attributes:
        sim = sim_str_str(data.source,attribute,source_lang,"en",data.aggregation)
        print(sim)
        if sim >= data.threshold:
            attributes.append(attribute)
    return {
        "attributes": attributes
    } 

