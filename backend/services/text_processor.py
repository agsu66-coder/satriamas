import re


class TextProcessor:

    def __init__(self):
        pass

    # =====================================

    def normalize(self, text):

        if text is None:
            return ""

        text = str(text)

        # lowercase
        text = text.lower()

        # hilangkan spasi ganda
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # =====================================

    def remove_symbol(self, text):

        text = re.sub(
            r"[^a-zA-Z0-9\s]",
            " ",
            text
        )

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # =====================================

    def preprocess(self, text):

        text = self.normalize(text)

        text = self.remove_symbol(text)

        return text


text_processor = TextProcessor()