import re

def highlight_sentences(text):
    # Categories of words or patterns with respective descriptions
    categories = {
        "highlight-exaggeration": {
            "words": [
                'shocking', 'unbelievable', 'exclusive', 'horrific', 'mind-blowing',
                'outrageous', 'explosive', 'devastating', 'stunning', 'unprecedented',
                'terrifying', 'bizarre', 'unthinkable', 'jaw-dropping', 'miraculous',
                'astonishing', 'groundbreaking', 'unimaginable', 'record-breaking', 'dreadful',
                'appalling', 'incredible', 'frightening'
            ],
            "description": "Contains exaggerated claims or hyperbole",
            "color": "rgba(255, 255, 186, 0.6)"
        },
        "highlight-sensational": {
            "patterns": [
                r'(\d+[\s]*\w+[\s]*%[\s]*increase)',  # Percentage increase pattern
                r'(breaking news)', r'(you won\'t believe)', r'(this changes everything)',
                r'(must read)', r'(shocking discovery)', r'(conspiracy theory)', r'(hidden agenda)',
                r'(you are in danger)', r'(breaking story)', r'(never before seen)', r'(exposed)',
                r'(the truth about)', r'(uncovered)', r'(the real story)', r'(this is huge)'
            ],
            "description": "Contains sensationalism patterns",
            "color": "rgba(173, 216, 230, 0.6)"
        },
        "highlight-ambiguous": {
            "patterns": [
                r'(anonymous sources)', r'(unverified reports)', r'(sources say)', r'(insiders reveal)',
                r'(rumors have it)', r'(one person claimed)', r'(witnesses say)', r'(unconfirmed information)',
                r'(according to reports)', r'(sources close to)', r'(according to insiders)'
            ],
            "description": "Contains unverified or anonymous sources",
            "color": "rgba(255, 240, 245, 0.6)"
        },
        "highlight-vague": {
            "words": [
                'might', 'could', 'possibly', 'allegedly', 'reportedly', 'seems', 'appears', 'suggests',
                'unlikely', 'uncertain', 'somewhat', 'perhaps', 'maybe', 'likely', 'possibly', 'rumored',
                'may', 'generally believed', 'could be', 'suggested', 'inconclusive', 'tentative'
            ],
            "description": "Contains vague language",
            "color": "rgba(144, 238, 144, 0.6)" 
        },
        "highlight-speculative": {
            "words": [
                'rumor', 'guess', 'speculation', 'unclear', 'theories', 'unsubstantiated', 'conjecture',
                'theorize', 'hypothesis', 'allegation', 'supposition', 'surmise', 'wild guess',
                'assumed', 'potential', 'presumed', 'imagine', 'may be', 'believed to be'
            ],
            "description": "Contains speculative or uncertain statements",
            "color": "rgba(255, 182, 193, 0.6)"
        }
    }

    # Split the text into sentences
    sentences = re.split(r'([.!?])', text)  # Split on punctuation and keep it

    highlighted_text = ""
    for sentence in sentences:
        applied_styles = []
        for category, data in categories.items():
            # Check words or patterns for each category
            if "words" in data and any(word in sentence.lower() for word in data["words"]):
                applied_styles.append(category)
            if "patterns" in data and any(re.search(pattern, sentence, re.IGNORECASE) for pattern in data["patterns"]):
                applied_styles.append(category)
        
        # Apply the first matching style, or default to normal text
        if applied_styles:
            style_class = applied_styles[0]
            highlighted_text += f"<span class='{style_class}'>{sentence}</span>"
        else:
            highlighted_text += sentence

    # Return highlighted text and a legend of colors
    color_meanings = {category: data["description"] for category, data in categories.items()}
    return highlighted_text, color_meanings
