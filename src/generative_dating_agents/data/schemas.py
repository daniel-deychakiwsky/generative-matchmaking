from dataclasses import dataclass
from typing import List

user_profile_function_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "The user's first and last name"},
        "age": {
            "type": "integer",
            "description": "The user's age",
            "minimum": 18,
            "maximum": 100,
        },
        "height": {
            "type": "string",
            "description": "The user's height between 2'0\" and 8'0\"",
            "pattern": "^\\d+'\\d+\"$",
        },
        "school": {"type": "string", "description": "The user's school"},
        "job_industry": {"type": "string", "description": "The user's job industry"},
        "job_title": {"type": "string", "description": "The user's job title"},
        "hometown_location": {
            "type": "string",
            "description": "The user's hometown city and state",
        },
        "dating_location": {
            "type": "string",
            "description": "Hardcoded to: Los Angeles, California",
            "pattern": "Los Angeles, California",
        },
        "languages_spoken": {
            "type": "array",
            "description": "The user's spoken languages",
            "items": {"type": "string"},
        },
        "values": {
            "type": "array",
            "description": "The user's life values",
            "items": {
                "type": "string",
            },
            "minItems": 5,
            "maxItems": 10,
        },
        "interests": {
            "type": "array",
            "description": "The user's life interests",
            "items": {
                "type": "string",
            },
            "minItems": 5,
            "maxItems": 10,
        },
        "education_level": {
            "type": "string",
            "description": "The user's education level",
            "enum": ["High school", "Undergraduate", "Graduate", "Doctoral", "Other"],
        },
        "religious_beliefs": {
            "type": "string",
            "description": "The user's religious beliefs",
            "enum": [
                "Agnostic",
                "Atheist",
                "Buddhist",
                "Catholic",
                "Christian",
                "Hindu",
                "Jewish",
                "Muslim",
                "Sikh",
                "Spiritual",
                "Other",
            ],
        },
        "politics": {
            "type": "string",
            "description": "The user's politics",
            "enum": ["Liberal", "Moderate", "Conservative", "Not political", "Other"],
        },
        "dating_intentions": {
            "type": "string",
            "description": "The user's dating intentions",
            "enum": [
                "Life partner",
                "Long term",
                "Long term, open to short",
                "Short term, open to long",
                "Short term",
                "Other",
            ],
        },
        "relationship_type": {
            "type": "string",
            "description": "The user's relationship type",
            "enum": ["Monogamy", "Polyamory", "Other"],
        },
        "gender": {
            "type": "string",
            "description": "The user's gender",
            "enum": ["Man", "Woman", "Non binary"],
        },
        "pronouns": {
            "type": "string",
            "description": "The user's pronouns",
            "enum": ["She/Her/Hers", "He/Him/His", "They/Them/Their"],
        },
        "sexuality": {
            "type": "string",
            "description": "The user's sexuality",
            "enum": ["Straight", "Gay", "Other"],
        },
        "ethnicity": {
            "type": "string",
            "description": "The user's ethnicity",
            "enum": [
                "Black African Descent",
                "East Asian",
                "Hispanic/Latino",
                "Middle Eastern",
                "Native American",
                "Pacific Islander",
                "South Asian",
                "Southeast Asian",
                "White Caucasian",
                "Other",
            ],
        },
        "has_children": {
            "type": "boolean",
            "description": "Does the user have children",
        },
        "want_children": {
            "type": "boolean",
            "description": "Does the user want children",
        },
        "pets": {
            "type": "array",
            "description": "The user's pets",
            "items": {
                "type": "string",
                "enum": ["Dog", "Cat", "Bird", "Reptile", "Fish", "None"],
            },
        },
        "zodiac_sign": {
            "type": "string",
            "description": "The user's zodiac sign",
            "enum": [
                "Aries",
                "Taurus",
                "Gemini",
                "Cancer",
                "Leo",
                "Virgo",
                "Libra",
                "Scorpio",
                "Sagittarius",
                "Capricorn",
                "Aquarius",
                "Pisces",
            ],
        },
        "mbti_personality_type": {
            "type": "string",
            "description": "The user's MBTI personality type",
            "enum": [
                "ISTJ",
                "ISFJ",
                "INFJ",
                "INTJ",
                "ISTP",
                "ISFP",
                "INFP",
                "INTP",
                "ESTP",
                "ESFP",
                "ENFP",
                "ENTP",
                "ESTJ",
                "ESFJ",
                "ENFJ",
                "ENTJ",
            ],
        },
        "drinking": {
            "type": "string",
            "description": "Does the user drink",
            "enum": ["Yes", "No", "Sometimes"],
        },
        "smoking": {
            "type": "string",
            "description": "Does the user smoke",
            "enum": ["Yes", "No", "Sometimes"],
        },
        "marijuana": {
            "type": "string",
            "description": "Does the user use marijuana",
            "enum": ["Yes", "No", "Sometimes"],
        },
        "drugs": {
            "type": "string",
            "description": "Does the user use drugs",
            "enum": ["Yes", "No", "Sometimes"],
        },
        "exercise": {
            "type": "string",
            "description": "Does the user exercise",
            "enum": ["Active", "Sometimes", "Almost never"],
        },
        "partner_preferences": {
            "type": "object",
            "properties": {
                "minimum_age": {
                    "type": "integer",
                    "description": "The user's preferred partner's minimum age",
                    "minimum": 18,
                    "maximum": 100,
                },
                "maximum_age": {
                    "type": "integer",
                    "description": "The user's preferred partner's maximum age",
                    "minimum": 18,
                    "maximum": 100,
                },
                "minimum_height": {
                    "type": "string",
                    "description": "The user's preferred partner's minimum height between 2'0\" and 8'0\"",
                    "pattern": "^\\d+'\\d+\"$",
                },
                "maximum_height": {
                    "type": "string",
                    "description": "The user's preferred partner's maximum height between 2'0\" and 8'0\"",
                    "pattern": "^\\d+'\\d+\"$",
                },
                "has_children": {
                    "type": "boolean",
                    "description": "Does the user's preferred partner have children",
                },
                "want_children": {
                    "type": "boolean",
                    "description": "Does the user's preferred partner want children",
                },
                "sexuality": {
                    "type": "string",
                    "description": "The user's preferred partner's sexuality",
                    "enum": ["Straight", "Gay", "Other"],
                },
                "drinking": {
                    "type": "string",
                    "description": "Does the user's preferred partner drink",
                    "enum": ["Yes", "No", "Sometimes"],
                },
                "smoking": {
                    "type": "string",
                    "description": "Does the user's preferred partner smoke",
                    "enum": ["Yes", "No", "Sometimes"],
                },
                "marijuana": {
                    "type": "string",
                    "description": "Does the user's preferred partner use marijuana",
                    "enum": ["Yes", "No", "Sometimes"],
                },
                "drugs": {
                    "type": "string",
                    "description": "Does the user's preferred partner use drugs",
                    "enum": ["Yes", "No", "Sometimes"],
                },
                "exercise": {
                    "type": "string",
                    "description": "Does the user's preferred partner exercise",
                    "enum": ["Active", "Sometimes", "Almost never"],
                },
                "gender": {
                    "type": "string",
                    "description": "The user's preferred partner's gender",
                    "enum": ["Man", "Woman", "Non binary"],
                },
                "dating_intentions": {
                    "type": "string",
                    "description": "The user's preferred partner's dating intentions",
                    "enum": [
                        "Life partner",
                        "Long term",
                        "Long term, open to short",
                        "Short term, open to long",
                        "Short term",
                        "Other",
                    ],
                },
                "relationship_type": {
                    "type": "string",
                    "description": "The user's preferred partner's relationship type",
                    "enum": ["Monogamy", "Polyamory", "Other"],
                },
                "ethnicities": {
                    "type": "array",
                    "description": "The user's preferred partner's ethnicities",
                    "items": {
                        "type": "string",
                        "enum": [
                            "Black African Descent",
                            "East Asian",
                            "Hispanic/Latino",
                            "Middle Eastern",
                            "Native American",
                            "Pacific Islander",
                            "South Asian",
                            "Southeast Asian",
                            "White Caucasian",
                            "Other",
                        ],
                    },
                    "minItems": 1,
                    "maxItems": 10,
                },
                "politics": {
                    "type": "array",
                    "description": "The user's preferred partner's politics",
                    "items": {
                        "type": "string",
                        "enum": [
                            "Liberal",
                            "Moderate",
                            "Conservative",
                            "Not political",
                            "Other",
                        ],
                    },
                    "minItems": 1,
                    "maxItems": 5,
                },
                "job_industry": {
                    "type": "array",
                    "description": "The user's preferred partner's job industry",
                    "items": {"type": "string"},
                    "minItems": 1,
                    "maxItems": 5,
                },
                "languages_spoken": {
                    "type": "array",
                    "description": "The user's preferred partner's spoken languages",
                    "items": {"type": "string"},
                    "minItems": 1,
                    "maxItems": 3,
                },
                "values": {
                    "type": "array",
                    "description": "The user's preferred partner's life values",
                    "items": {"type": "string"},
                    "minItems": 5,
                    "maxItems": 10,
                },
                "interests": {
                    "type": "array",
                    "description": "The user's preferred partner's interests",
                    "items": {
                        "type": "string",
                    },
                    "minItems": 5,
                    "maxItems": 10,
                },
                "education_level": {
                    "type": "array",
                    "description": "The user's preferred partner's education level",
                    "items": {
                        "type": "string",
                        "enum": [
                            "High school",
                            "Undergraduate",
                            "Graduate",
                            "Doctoral",
                            "Other",
                        ],
                    },
                    "minItems": 1,
                    "maxItems": 5,
                },
            },
            "required": [
                "minimum_age",
                "maximum_age",
                "minimum_height",
                "maximum_height",
                "has_children",
                "want_children",
                "sexuality",
                "gender",
                "dating_intentions",
                "relationship_type",
                "drinking",
                "smoking",
                "marijuana",
                "drugs",
                "exercise",
                "ethnicities",
                "politics",
                "job_industry",
                "languages_spoken",
                "values",
                "interests",
                "education_level",
            ],
        },
    },
    "required": [
        "name",
        "age",
        "height",
        "school",
        "job_industry",
        "job_title",
        "hometown_location",
        "dating_location",
        "languages_spoken",
        "values",
        "interests",
        "education_level",
        "religious_beliefs",
        "politics",
        "dating_intentions",
        "relationship_type",
        "gender",
        "pronouns",
        "sexuality",
        "ethnicity",
        "has_children",
        "want_children",
        "pets",
        "zodiac_sign",
        "mbti_personality_type",
        "drinking",
        "smoking",
        "marijuana",
        "drugs",
        "exercise",
        "partner_preferences",
    ],
}


@dataclass
class PartnerPreferences:
    minimum_age: int
    maximum_age: int
    minimum_height: str
    maximum_height: str
    has_children: bool
    want_children: bool
    sexuality: str
    drinking: str
    smoking: str
    marijuana: str
    drugs: str
    exercise: str
    gender: str
    dating_intentions: str
    relationship_type: str
    ethnicities: List[str]
    politics: List[str]
    job_industry: List[str]
    languages_spoken: List[str]
    values: List[str]
    interests: List[str]
    education_level: List[str]


@dataclass
class UserProfile:
    name: str
    age: int
    height: str
    school: str
    job_industry: str
    job_title: str
    hometown_location: str
    dating_location: str
    languages_spoken: List[str]
    values: List[str]
    interests: List[str]
    education_level: str
    religious_beliefs: str
    politics: str
    dating_intentions: str
    relationship_type: str
    gender: str
    pronouns: str
    sexuality: str
    ethnicity: str
    has_children: bool
    want_children: bool
    pets: List[str]
    zodiac_sign: str
    mbti_personality_type: str
    drinking: str
    smoking: str
    marijuana: str
    drugs: str
    exercise: str
    partner_preferences: PartnerPreferences
    profile_summary: str
    preferences_summary: str
    user_id: str
