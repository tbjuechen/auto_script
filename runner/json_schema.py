from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import List, Union, Any
from typing_extensions import Literal
import json

class Variable(BaseModel):
    type: Literal["variable"] = "variable"
    name: str
    variable_type: str
    value: Any=None # 非第一次出现

class Immediate(BaseModel):
    type: Literal["immediate"] = "immediate"
    variable_type: str
    value: Any

class Function(BaseModel):
    type: Literal["function"] = "function"
    target: str
    args: List[Union['Variable', 'Immediate', 'Function']]

    @field_validator('args', mode='before') 
    def args_validator(cls, args):
        validated_args = []

        for arg in args:
            arg_type = arg.get('type')
            if arg_type == 'variable':
                validated_args.append(Variable(**arg))
            elif arg_type == 'immediate':
                validated_args.append(Immediate(**arg))
            elif arg_type == 'function':
                validated_args.append(Function(**arg))
            else:
                raise ValueError(f"Unknown type: {arg_type}")

        return validated_args

class Branch(BaseModel):
    type: Literal["branch"] = "branch"
    condition: Union['Variable', 'Function', 'Immediate']
    then: Union['Variable', 'Function', 'Immediate', 'Sequence', 'WhileLoop', 'Branch']
    else_: Union['Variable', 'Function', 'Immediate', 'Sequence', 'WhileLoop', 'Branch']

class Sequence(BaseModel):
    type: Literal["sequence"] = "sequence"
    steps: List[Union['Variable', 'Function', 'Immediate', 'Sequence', 'WhileLoop', 'Branch']]

    @field_validator('steps', mode='before')
    def steps_validator(cls, steps):
        validated_steps = []

        for step in steps:
            step_type = step.get('type')
            if step_type == 'variable':
                validated_steps.append(Variable(**step))
            elif step_type == 'immediate':
                validated_steps.append(Immediate(**step))
            elif step_type == 'function':
                validated_steps.append(Function(**step))
            elif step_type == 'sequence':
                validated_steps.append(Sequence(**step))
            elif step_type == 'while':
                validated_steps.append(WhileLoop(**step))
            elif step_type == 'branch':
                validated_steps.append(Branch(**step))
            else:
                raise ValueError(f"Unknown type: {step_type}")

        return validated_steps

class WhileLoop(BaseModel):
    type: Literal["while"] = "while"
    condition: Union[Function, Variable, Immediate]
    do: Union['Function', 'Sequence', 'WhileLoop', 'Branch']

    @field_validator('do', mode='before')
    def do_validator(cls, do):
        do_type = do.get('type')
        if do_type == 'function':
            return Function(**do)
        elif do_type == 'sequence':
            return Sequence(**do)
        elif do_type == 'while':
            return WhileLoop(**do)
        elif do_type == 'branch':
            return Branch(**do)
        else:
            raise ValueError(f"Unknown type: {do_type}")
    
    @field_validator('condition', mode='before')
    def condition_validator(cls, condition):
        condition_type = condition.get('type')
        if condition_type == 'function':
            return Function(**condition)
        elif condition_type == 'variable':
            return Variable(**condition)
        elif condition_type == 'immediate':
            return Immediate(**condition)
        else:
            raise ValueError(f"Unknown type: {condition_type}") 

# To allow recursive type definition
Function.model_rebuild()
Branch.model_rebuild()
Sequence.model_rebuild()
WhileLoop.model_rebuild()

class MainModel(BaseModel):
    steps: List[Union[Variable, Sequence, WhileLoop, Function, Immediate, Branch]]

    @field_validator('steps', mode='before')
    def steps_validator(cls, steps):
        validated_steps = []

        for step in steps:
            step_type = step.get('type')
            if step_type == 'variable':
                validated_steps.append(Variable(**step))
            elif step_type == 'immediate':
                validated_steps.append(Immediate(**step))
            elif step_type == 'function':
                validated_steps.append(Function(**step))
            elif step_type == 'sequence':
                validated_steps.append(Sequence(**step))
            elif step_type == 'while':
                validated_steps.append(WhileLoop(**step))
            elif step_type == 'branch':
                validated_steps.append(Branch(**step))
            else:
                raise ValueError(f"Unknown type: {step_type}")

        return validated_steps


# Test the schema
if __name__ == '__main__':
    with open('F:\\Scripts\\yys\\auto_scripts\\test.json', 'r') as f:
        test_data = json.load(f)

    main = MainModel.model_validate(test_data)

    print(main.steps)

