"""
Form Auto-Fill tool.
Tries to guess what each form field is and fills it in using our identity data.
"""

from hrequests.parser import Element
from typing import Dict, Any

class FormFiller:
    '''
    Finds form fields and stuffs them with identity data so we don't have to.
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
        Goes through all inputs in a form and tries to match them to our identity keys.
        '''
        inputs = form_element.find_all('input, select, textarea')
        for input_el in inputs:
            # Grab all the attributes we can use to guess the field type
            attr_strings = [
                input_el.attrs.get('id', ''),
                input_el.attrs.get('name', ''),
                input_el.attrs.get('placeholder', '').lower(),
                input_el.attrs.get('autocomplete', '')
            ]
            
            filled = False
            for identity_key, html_keywords in self.FIELD_MAP.items():
                if identity_key in self.identity:
                    # If we find a keyword in any of the attributes, we'll assume it's a match
                    if any(any(kw in attr.lower() for kw in html_keywords) for attr in attr_strings if attr):
                        # Type it into the browser if we're in a browser session
                        if hasattr(input_el, 'type'):
                            input_el.type(str(self.identity[identity_key]))
                            filled = True
                            break
            
            if not filled:
                print(f"[FormFiller] No clue what this input is: {attr_strings}")

    @classmethod
    def apply(cls, form: Element, identity: Dict[str, Any]):
        cls(identity).fill_form(form)
