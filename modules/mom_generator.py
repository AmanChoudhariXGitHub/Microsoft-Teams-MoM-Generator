from modules.llm_client import invoke_llm

def generate_mom(transcript, llm_type="ollama", api_key=None):
    """ Generate structured Meeting Minutes in the exact tabular format requested """

    prompt = f"""
    Convert the following meeting transcript into structured Meeting Minutes (MoM) in the EXACT format shown below:

    TRANSCRIPT:
    {transcript}

    Please generate the MoM with the following EXACT structure:

    # Meeting Minutes: [Extract meeting topic/title]

    **Date**: [Extract date if available, otherwise use current date]
    **Time**: [Extract time if available] 
    **Invitees**: [List all participants mentioned in transcript]

    | Type | Description | Assignees | Due | Status |
    |------|-------------|-----------|-----|--------|
    | Information | [Detailed description of information shared] | [Person who shared info] | | Open |
    | Information | [Another information item] | [Person who shared] | | Open |
    | Action | [Specific action item with clear deliverable] | [Person assigned] | [Due date if mentioned] | Open |
    | Action | [Another action item] | [Person assigned] | [Due date if mentioned] | Open |

    **How was the meeting?** Check out the feedback!

    IMPORTANT INSTRUCTIONS:
    1. Use ONLY "Information" or "Action" in the Type column
    2. Information items are for things discussed, shared, or explained
    3. Action items are for tasks that need to be completed
    4. Extract assignees from context (who mentioned it, who was asked to do it)
    5. Due dates only if explicitly mentioned in transcript
    6. All Status should be "Open" initially
    7. Keep descriptions detailed but concise
    8. If no clear assignee, use "All" or the most relevant person
    9. Maintain the exact table format with proper markdown
    10. Extract meeting topic from the beginning of transcript or context
    """

    return invoke_llm(prompt, llm_type=llm_type, api_key=api_key)

def generate_summary_table(transcript, llm_type="ollama", api_key=None):
    """ Generate a concise summary table for quick reference """
    
    prompt = f"""
    Create a concise summary table from this meeting transcript:

    TRANSCRIPT:
    {transcript}

    Generate output in this format:

    ## Meeting Summary Dashboard

    | Metric | Count/Details |
    |--------|---------------|
    | **Total Participants** | [Number] |
    | **Information Items** | [Count of information items] |
    | **Action Items** | [Count of action items] |
    | **Items with Assignees** | [Count] |
    | **Items with Due Dates** | [Count] |
    | **Meeting Duration** | [If mentioned] |

    ## Key Topics Covered
    | Topic | Discussed By | Outcome |
    |-------|--------------|---------|
    | [Topic 1] | [Speaker] | [Information/Action] |
    | [Topic 2] | [Speaker] | [Information/Action] |

    ## Action Items Summary
    | Priority | Task | Owner | Due Date |
    |----------|------|-------|----------|
    | High | [Urgent task] | [Person] | [Date] |
    | Medium | [Regular task] | [Person] | [Date] |

    Focus on providing a quick overview of the meeting's productivity and outcomes.
    """
    
    return invoke_llm(prompt, llm_type=llm_type, api_key=api_key)

def extract_speaker_analysis(transcript, llm_type="ollama", api_key=None):
    """ Analyze who spoke about what topics with contribution tracking """
    
    prompt = f"""
    Analyze the following transcript and create a detailed speaker participation analysis:

    TRANSCRIPT:
    {transcript}

    Generate this analysis:

    ## Speaker Contribution Analysis

    | Speaker | Information Shared | Actions Assigned | Key Contributions | Participation Level |
    |---------|-------------------|------------------|-------------------|-------------------|
    | [Name 1] | [Count] | [Count] | [Main topics discussed] | [High/Medium/Low] |
    | [Name 2] | [Count] | [Count] | [Main topics discussed] | [High/Medium/Low] |

    ## Discussion Timeline
    | Order | Speaker | Type | Topic | Key Point |
    |-------|---------|------|-------|-----------|
    | 1 | [Name] | Information | [Topic] | [What was shared] |
    | 2 | [Name] | Action | [Topic] | [What needs to be done] |

    ## Meeting Engagement Metrics
    | Metric | Value |
    |--------|-------|
    | Most Active Speaker | [Name] |
    | Most Action Items Assigned | [Name] |
    | Most Information Shared | [Name] |
    | Total Speaking Turns | [Number] |

    Focus on quantifying participation and identifying key contributors.
    """
    
    return invoke_llm(prompt, llm_type=llm_type, api_key=api_key)

def extract_action_items_only(transcript, llm_type="ollama", api_key=None):
    """ Extract only action items in a focused table """
    
    prompt = f"""
    From the following meeting transcript, extract ONLY the action items in this format:

    TRANSCRIPT:
    {transcript}

    ## Action Items Tracker

    | # | Action Item | Assigned To | Due Date | Priority | Status | Notes |
    |---|-------------|-------------|----------|----------|--------|-------|
    | 1 | [Specific task] | [Person name] | [Date if mentioned] | [High/Med/Low] | Open | [Additional context] |
    | 2 | [Specific task] | [Person name] | [Date if mentioned] | [High/Med/Low] | Open | [Additional context] |

    ## Action Items Summary
    - **Total Action Items**: [Count]
    - **Items with Due Dates**: [Count]
    - **High Priority Items**: [Count]
    - **Unassigned Items**: [Count]

    INSTRUCTIONS:
    1. Only include items that require someone to DO something
    2. Be specific about what needs to be accomplished
    3. Extract assignee from context (who was asked, who volunteered, who mentioned they would do it)
    4. Estimate priority based on urgency mentioned in discussion
    5. Include relevant context in Notes column
    """
    
    return invoke_llm(prompt, llm_type=llm_type, api_key=api_key)
