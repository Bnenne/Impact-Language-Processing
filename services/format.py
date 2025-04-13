import re

def modify(document):
    """Function that deletes the team information off the beginning of doc.

    Args:
        document (string): Document to be edited.
    """
    match = re.search(r"(Describe the impact.*)", document)

    if match:
        return match.group(1).strip()  # Return everything starting from "Describe the impact"
    else:
        return ""

def segment(document, nlp):
    """Function that segments spacy pdf reader documents into paragraphs.

    Args:
        document (Doc): document to be segmented into paragraphs.
        nlp (Language): The spaCy pipeline used for reprocessing each paragraph.
    """
    doc = nlp(document)
    return [sent.text.strip() for sent in doc.sents]

def clean(document, nlp):
    """Function that cleans spacy pdf reader documents into simplified paragraphs and separates questions.

    Args:
        document (Doc): document to be cleaned.
        nlp (Language): The spaCy pipeline used for reprocessing each paragraph.

    Returns:
        list: Cleaned document in paragraphs, gets rid of unnecessary spaces etc.
    """
    cleaned = modify(remove_nl_string(str(document)))
    paragraphs = list(segment(cleaned, nlp))
    for paragraph in paragraphs:
        cleaned_text = "\n".join(line for line in paragraph.splitlines() if line.strip())
        if cleaned_text == '' or cleaned_text == ' ':
            paragraphs.pop(paragraphs.index(paragraph))
        else:
            paragraphs[paragraphs.index(paragraph)] = cleaned_text
    return remove_nl(paragraphs)

def user_sort(documents):
    """Function that sorts paragraphs based on user input.
    Args:
        documents (list): list of paragraphs.

    Returns:
        tuple:
            - list: questions and answers only.
            - list: questions only.
    """
    questions = []
    new_documents = []
    for document in documents:
        asking = True
        while asking:
            print(document, '\n')
            user = input('[Q/A/O]\n')
            if user == 'Q' or user == 'q':
                questions.append(document)
                new_documents.append(document)
                asking = False
            if user == 'A' or user == 'a':
                new_documents.append(document)
                asking = False
            if user == 'O' or user == 'o':
                asking = False
    return new_documents, questions

def auto_sort(documents, questions):
    """Function that sorts paragraphs based questions gathered from previous documents.

    Args:
        documents (list): list of paragraphs to sort.
        questions (list): list of questions to sort with.
    """
    new_documents = []
    for document in documents:
        print([document], '\n')
    for question in questions:
        try:
            index = documents.index(question)+1
            new_documents.append(question)
            new_documents.append(documents[index])
        except ValueError as e:
            print('ValueError occurred:', e)
            print(question)
        except Exception as e:
            print('An unexpected error occurred:', e)
            print(question)
    return new_documents

def remove_nl(documents):
    """Function that removes unnecessary '\n' from paragraphs.

    Args:
        documents (list): list of paragraphs to remove '\n' from.
    """
    new_documents = []
    for document in documents:
        new_document = document.replace('\n', ' ')
        new_documents.append(new_document)
    return new_documents

def remove_nl_string(document):
    """Function that removes unnecessary '\n' from document

    Args:
        document (string): document to be edited.
    """
    new_document = document.replace('\n', ' ')
    return new_document

def grouping(documents, questions):
    grouped = []
    for question in questions:
        answers = []
        for document in documents:
            try:
                index = document.index(question) + 1
                answers.append(document[index])
            except ValueError as e:
                print('ValueError occurred:', e)
            except Exception as e:
                print('An unexpected error occurred:', e)
        grouped.append(answers)
    return grouped