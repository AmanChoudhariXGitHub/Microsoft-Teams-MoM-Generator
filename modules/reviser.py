from modules.llm_client import invoke_llm

def revise_mom(mom_text, feedback, llm_type="ollama", api_key=None):
    """ Revises the Meeting Minutes based on human feedback """

    prompt = f"""
    Here is a generated Meeting Minutes document in tabular format:

    {mom_text}

    The reviewer has given the following feedback:
    "{feedback}"

    Please improve the MoM based on this feedback while maintaining the EXACT tabular format:

    | Type | Description | Assignees | Due | Status |
    |------|-------------|-----------|-----|--------|

    IMPORTANT:
    1. Keep the exact table structure with Type, Description, Assignees, Due, Status columns
    2. Use only "Information" or "Action" in the Type column
    3. Apply the feedback while maintaining professional formatting
    4. If reassigning tasks, update the Assignees column accordingly
    5. If adding new items, follow the same format
    6. Keep all existing good content unless specifically asked to change it
    7. Maintain the meeting header with Date, Time, and Invitees

    Make the requested changes while preserving the structure and format.
    """

    return invoke_llm(prompt, llm_type=llm_type, api_key=api_key)
