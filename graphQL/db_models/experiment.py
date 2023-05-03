import json
from mongoengine.fields import (
    StringField,
    ListField,
    IntField,
)
import re
from graphQL.db_models.model_base import ModelBase

class Experiment(ModelBase):
    meta = {'collection': 'experiment'}
    name = StringField(required=True)
    description = StringField(max_length=255)
    dynamic_vars = ListField(StringField(max_length=255))

    def get_dynamic_vars_dict(conversation):
        dynamic_vars_list = []
        pattern = r"\{\s*[a-zA-Z0-9\s]+\s*\}"
        for conversion in conversation:
            content = conversion['content']
            matches = re.findall(pattern, content)

            for match in matches:
                key = match.replace("{", "").replace("}", "")
                dynamic_vars_list.append(key)
        return dynamic_vars_list

    @classmethod
    def update_dynamic_vars(cls, experiment_id, conversation):

        experiment = cls.objects(id=experiment_id).first()
        if not experiment:
            raise ValueError('Experiment not found')
        existing_vars = experiment.dynamic_vars or [] 
        dynamic_vars_list = Experiment.get_dynamic_vars_dict(conversation)
        updated_vars = list(set(existing_vars + dynamic_vars_list))
        experiment.dynamic_vars = updated_vars
        experiment.save()

