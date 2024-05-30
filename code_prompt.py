
from llama_index.core import PromptTemplate


def code_prompt_tmpl():
    code_prompt_tmpl_str = """{pre_context}<|fim_prefix|>{prefix_code}<|fim_suffix|>{suffix_code}<|fim_middle|>"""
    code_prompt_tmpl = PromptTemplate(code_prompt_tmpl_str)
    return code_prompt_tmpl


def apply_provider_fim_tokens(prompt:str,model_name:str=""):
    if "deepseek" in model_name:
        prompt = prompt.replace('<|fim_prefix|>', ' <｜fim▁begin｜>').replace('<|fim_suffix|>', '<｜fim▁hole｜>').replace('<|fim_middle|>', '<｜fim▁end｜>')
        prompt = prompt.replace('<|file_separator|>', '#')
    elif "codellama" in model_name:
        prompt = prompt.replace('<|fim_prefix|>', ' <PRE> ').replace('<|fim_suffix|>', ' <SUF>').replace('<|fim_middle|>', ' <MID>')
    elif "starcoder" in model_name:
        prompt = prompt.replace('<|fim_prefix|>', '<fim_prefix>').replace('<|fim_suffix|>', '<fim_suffix>').replace('<|fim_middle|>', '<fim_middle>')
        prompt = prompt.replace('<|file_separator|>', '<file_sep>')
    elif "mistral" in model_name:
        prompt = prompt.replace('<|fim_prefix|>', '[PREFIX]').replace('<|fim_suffix|>', '[SUFFIX]').replace('<|fim_middle|>', '[MIDDLE]')
        prompt = prompt.replace('<|file_separator|>', '#')
    return prompt

