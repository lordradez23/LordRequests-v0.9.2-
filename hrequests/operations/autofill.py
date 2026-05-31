'''
Automated Form-Auto-Fill
~~~~~~~~~~~~~~~~~~~~~~~

Intelligent form detection and population using Persona identity data.
'''

from hrequests.parser import Element
from typing import Dict, Any

class FormFiller:
    '''
    Detects form fields and populates them with provided identity data.
    '''
    FIELD_MAP = {
        'first_name': ['first-name', 'fname', 'given-name', 'first_name'],
        'last_name': ['last-name', 'lname', 'surname', 'family-name', 'last_name'],
        'email': ['email', 'e-mail', 'mail', 'username', 'user_email'],
        'phone': ['phone', 'tel', 'mobile', 'cell', 'telephone'],
        'address': ['address', 'street', 'addr1'],
        'city': ['city', 'town', 'locality'],
        'zip': ['zip', 'postcode', 'postal-code', 'postal_code'],
        'country': ['country', 'nation']
    }

    def __init__(self, identity: Dict[str, Any]):
        self.identity = identity

    def fill_form(self, form_element: Element):
        '''
        Finds all inputs in the form and fills them if a match is found in identity.
        '''
        inputs = form_element.find_all('input, select, textarea')
        for input_el in inputs:
            attr_strings = [
                input_el.attrs.get('id', ''),
                input_el.attrs.get('name', ''),
                input_el.attrs.get('placeholder', '').lower(),
                input_el.attrs.get('autocomplete', '')
            ]
            
            filled = False
            for identity_key, html_keywords in self.FIELD_MAP.items():
                if identity_key in self.identity:
                    # Check if any attribute contains a keyword
                    if any(any(kw in attr.lower() for kw in html_keywords) for attr in attr_strings if attr):
                        # Use browser session to type if available
                        if hasattr(input_el, 'type'):
                            input_el.type(str(self.identity[identity_key]))
                            filled = True
                            break
            
            if not filled:
                print(f"[FormFiller] Could not determine purpose of input: {attr_strings}")

    @classmethod
    def apply(cls, form: Element, identity: Dict[str, Any]):
        cls(identity).fill_form(form)
