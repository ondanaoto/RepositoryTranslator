from enum import Enum, unique

@unique
class LanguageCode(Enum):
    JAPAN = 'ja'
    UNITED_STATES = 'en'
    SPAIN = 'es'
    FRANCE = 'fr'
    GERMANY = 'de'
    CHINA = 'zh'
    TAIWAN = 'zh-TW'
    SINGAPORE = 'zh-SG'
    HONG_KONG = 'zh-HK'
    KOREA = 'ko'
    RUSSIA = 'ru'
    ARABIC = 'ar'
    INDIA = 'hi'
    BRAZIL = 'pt-BR'
    PORTUGAL = 'pt-PT'
    ITALY = 'it'
    MEXICO = 'es-MX'
    CANADA_ENGLISH = 'en-CA'
    CANADA_FRENCH = 'fr-CA'
    
    def __str__(self):
        language_names = {
            'ja': "Japanese",
            'en': "English",
            'es': "Spanish",
            'fr': "French",
            'de': "German",
            'zh': "Chinese",
            'zh-TW': "Chinese (Traditional)",
            'zh-SG': "Chinese (Simplified Singapore)",
            'zh-HK': "Chinese (Traditional Hong Kong)",
            'ko': "Korean",
            'ru': "Russian",
            'ar': "Arabic",
            'hi': "Hindi",
            'pt-BR': "Portuguese (Brazil)",
            'pt-PT': "Portuguese (Portugal)",
            'it': "Italian",
            'es-MX': "Spanish (Mexico)",
            'en-CA': "English (Canada)",
            'fr-CA': "French (Canada)"
        }
        return language_names[self.value]
    
    @classmethod
    def from_str(cls, input_str) -> "LanguageCode":
        for lang in LanguageCode:
            if lang.value == input_str:
                return lang
        raise ValueError(f"No matching enum for string: {input_str}")