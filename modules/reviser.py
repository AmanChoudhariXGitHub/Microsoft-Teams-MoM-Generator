from modules.llm_client import invoke_llm

def revise_mom(mom_text, feedback, use_openai=False, api_key=None):
    """ Revises the Meeting Minutes based on human feedback """

    prompt = f"""
    Here is a generated Meeting Minutes document:

    {mom_text}

    The reviewer has given the following feedback:
    "{feedback}"

    Please improve the MoM based on this feedback while keeping it structured and clear.
    """

    return invoke_llm(prompt, use_openai=use_openai, api_key=api_key)
