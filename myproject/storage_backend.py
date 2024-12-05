from storages.backends.azure_storage import AzureStorage

class CustomAzureStorage(AzureStorage):
    account_name = 'projectstracc'  # Ton compte Azure
    account_key = 'QlWBd7gvMj9zPt3cXefpV3iVasnCo8P9kXcGjokesmFZY68rxdHuapOHFvqAX+ibTDfu/XRRFJ7G+ASt2jQGnA=='  # La clé de ton compte Azure
    container_name = 'book-covers'  # Le nom de ton conteneur
    expiration_secs = None  # Optionnel: la durée d'expiration des URL générées