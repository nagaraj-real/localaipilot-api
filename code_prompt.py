
from llama_index.core import PromptTemplate


def code_prompt_tmpl():
    code_prompt_tmpl_str = """{pre_context}<|fim_prefix|>{prefix_code}<|fim_suffix|>{suffix_code}<|fim_middle|>"""
    code_prompt_tmpl = PromptTemplate(code_prompt_tmpl_str)
    return code_prompt_tmpl

