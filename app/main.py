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
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel, Field, HttpUrl
from typing import List


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
    
class StringsSimilarityData(BaseModel):
    source: str = Field(...,description="Source string to obtain the similarity.",example="I hate planes")
    target: str = Field(...,description="Target string to obtain the similarity.",example="I hate helicopters")
    aggregation: Aggregation = Field(...,description="Statistical function to aggregate the similarity between strings",example="max")

class StringsSimilarityDataWithLang(StringsSimilarityData):
    sourceLang: str = Field(...,description="Language of the source string.",example="en")
    targetLang: str = Field(...,description="Language of the target string.",example="zh")

class SimilarityResult(BaseModel):
    similarity: float = Field(...,description="The similarity between strings.",example="0.5")

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

