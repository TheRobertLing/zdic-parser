class ElementIsMissingException(Exception):
    def __init__(self):
        message = f"""
        The required element was not found on the page.
        This may be due to a change in zdic's page structure.

        Possible causes:
        - The element's selector has changed.
        - The website has been updated.
        - The page URL is incorrect.

        Suggested actions:
        - Check if the website layout has changed.
        - Modify parser functions inside of src/utils.py accordingly
        
        I will try my best to consistently monitor for any drastic changes to zdic's page layout and release updates 
        accordingly"""
        super().__init__(message.strip())
