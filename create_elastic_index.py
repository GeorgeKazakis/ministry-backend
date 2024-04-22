import json
from elasticsearch import Elasticsearch

from src.models.apografi.organization import Organization

from src.models.psped.foreas import Foreas
demo_remit = """
Το Εργαστήριο διευθύνεται από τον Διευθυντή που είναι μέλος του Διδακτικού Ερευνητικού Προσωπικού (Δ.Ε.Π.) της Σχολής Πολιτικών Μηχανικών του Ε.Μ.Π., και εκλέγεται σύμφωνα με την κείμενη νομοθεσία. Ο Διευθυντής ασκεί τις αρμοδιότητες σύμφωνα με την κείμενη νομοθεσία και επιπλέον: - Είναι υπεύθυνος για την υλοποίηση των αποφάσεων του Ιδρύματος και ιδιαίτερα της Γ.Σ. της Σχολής Πολιτικών Μηχανικών Ε.Μ.Π., για τα εκπαιδευτικά, επιστημονικά, ερευνητικά, αλλά και τα διοικητικά θέματα που αφορούν το Εργαστήριο.

- Είναι υπεύθυνος για την καλή λειτουργία και ανάπτυξη του Εργαστηρίου. - Έχει την εποπτεία του τεχνικού και διοικητικού προσωπικού, που έχει ενταχθεί στο Εργαστήριο με αποφάσεις της Γ.Σ. της Σχολής. - Έχει την εποπτεία της υλικοτεχνικής υποδομής του Εργαστηρίου. - Εκπροσωπεί αποκλειστικά το Εργαστήριο στις σχέσεις του με κάθε άλλο εξωτερικό προς το Εργαστήριο φορέα, ενεργώντας πάντα μέσα στα πλαίσια των αποφάσεων των οργάνων του Ιδρύματος. Η εκπροσώπηση αυτή περιλαμβάνει την ευθύνη της εύρυθμης λειτουργίας του Εργαστηρίου και οφείλει να λαμβάνει υπόψη τις ευθύνες που αναλαμβάνει ή τις πρωτοβουλίες που αναπτύσσει κάθε μέλος ΔΕΠ του Εργαστηρίου, στα πλαίσια ερευνητικών προγραμμάτων, στα οποία το κάθε μέλος είναι υπεύθυνο. - Συντονίζει το διδακτικό και ερευνητικό έργο του Εργαστηρίου. - Μεριμνά για την τήρηση του κανονισμού και του προγράμματος λειτουργίας του Εργαστηρίου. - Μεριμνά για την οικονομική διαχείριση των εσόδων και λοιπών οικονομικών πόρων του Εργαστηρίου. - Μεριμνά για τη στελέχωση του Εργαστηρίου με το αναγκαίο κατάλληλο προσωπικό. - Μεριμνά για την κατανομή και χρήση των χώρων του Εργαστηρίου. - Μεριμνά για τη σύνταξη, την παρακολούθηση, το συντονισμό και την εκπλήρωση του προγράμματος λειτουργίας και δραστηριοτήτων του Εργαστηρίου στο πλαίσιο της αποστολής του. - Εισηγείται στη Σύγκλητο του Ε.Μ.Π. για τους «Υπόλογους» των αναλωσίμων υλικών, του κινητού εξοπλισμού και των χώρων εργασίας με την σύνταξη εισηγητικής έκθεσης υπόλογων, η οποία περιέχει ενδεικτικά τα εξής: · Την υφιστάμενη κατάσταση του κινητού, σταθερού εξοπλισμού, υποδομών και κτηριακών εγκαταστάσεων, · τις απαιτήσεις για την απαραίτητη συντήρηση και τεχνική υποστήριξη του εξοπλισμού, των υποδομών και γενικά των κτηριακών εγκαταστάσεων, · τις αναγκαίες παραγγελίες υλικοτεχνικής υποδομής στα πλαίσια του αναπτυξιακού προγραμματισμού του Εργαστηρίου, · τις αναγκαίες αναβαθμίσεις/επεκτάσεις των εγκαταστάσεων και των υποδομών. - Έχει την αποκλειστική αρμοδιότητα για την αντιμετώπιση εκτάκτων αναγκών, την αδιάλειπτη λειτουργία του Εργαστήριου και γενικότερα όλη τη λειτουργία του Εργαστηρίου. Σε περίπτωση που τα μόνιμα μέλη του Εργαστηρίου είναι περισσότερα από δέκα (10) ο Διευθυντής Εργαστηρίου κρίνει τον διαμοιρασμό των αρμοδιοτήτων κατά περίπτωση. Σε περίπτωση που τα μόνιμα μέλη του Εργαστηρίου είναι δέκα (10) ή λιγότερα, διεκπεραιώνονται από τον Διευθυντή του Εργαστηρίου επιπλέον τα παρακάτω: - Κατάρτιση και υποβολή στη Γ.Σ. της Σχολής του ετήσιου εκπαιδευτικού προγράμματος του Εργαστηρίου και η μέριμνα για την τήρησή του. - Κατάρτιση και υποβολή στη Γ.Σ. της Σχολής του ετήσιου εκπαιδευτικού προϋπολογισμού του Εργαστηρίου και μέριμνα για την πιστή εκτέλεσή του.

- Κατάρτιση του ετήσιου οικονομικού απολογισμού και της έκθεσης δραστηριοτήτων (εκπαιδευτικών, ερευνητικών, παροχής υπηρεσιών) του Εργαστηρίου, εντός το πολύ διμήνου από το τέλος κάθε ακαδημαϊκού έτους. Ο Διευθυντής του Εργαστηρίου υπογράφει αποκλειστικά τα εξερχόμενα έγγραφα του Εργαστηρίου όπως ενδεικτικά αναφέρονται ακολούθως: - Παραδοτέα έγγραφα από επιστημονικές ή εκπαιδευτικές δράσεις του Εργαστηρίου, ως ο επιστημονικός υπεύθυνος του Εργαστηρίου, - έγγραφα μετρήσεων, ελέγχων και γενικά κάθε εγγράφου που απαιτείται για την εφαρμογή του συστήματος ποιότητας, - συμβάσεις με μέλη του Εργαστηρίου (όπου απαιτείται) για την παροχή υπηρεσιών τους στα πλαίσια των ερευνητικών δράσεων του Εργαστηρίου, - ιδιωτικές Συμβάσεις/Συμφωνητικά με εξωτερικούς συνεργάτες για την παροχή υπηρεσιών τους στα πλαίσια των ερευνητικών δράσεων του Εργαστηρίου, - Ετήσιο προϋπολογισμό και λοιπά έγγραφα για την εκτέλεση ερευνητικών δραστηριοτήτων του Εργαστηρίου και τη συμμετοχή σε ερευνητικά προγράμματα, - ετήσια έκθεση εκπαιδευτικών δραστηριοτήτων του Εργαστηρίου, - εισηγητική «Έκθεση Υπόλογων» προς Σύγκλητο, - έγγραφα Παραγγελίας αναλωσίμων υλικών για σκοπούς του Εργαστηρίου, - έγγραφα παροχής υπηρεσιών και αναλώσιμων για τη συντήρηση εξοπλισμού και υλικοτεχνικών υποδομών για σκοπούς του Εργαστηρίου, - έγγραφα για τη σύναψη συνεργασιών για σκοπούς του Εργαστηρίου.

"""
import json
spatial_data = {
    "geoType": "Polygon",
    "coordinates": [[-123.3656, 48.4284], [-123.362, 48.429],
                    [-123.363, 48.426]]
}

# ContactPoint structur
contact_point_data = json.dumps({
    "telephone": "+1234567890",
    "contactType": "customer support"
})

# FoundationFek structure
foundation_fek_data = json.dumps({
    "fekNumber": "123/2004",
    "fekIssue": "111",
    "street": "1234 Reunion Blvd",
    "city": "Metropolis",
    "state": "NT",
    "postalCode": "89890"
})

# Address structure
main_address = json.dumps({"country": "Fantasia"})

secondary_address = json.dumps({
    "street": "4321 Revolution St",
    "city": "Gotham",
    "state": "NJ",
    "postalCode": "07097",
    "country": "USA"
})
organization_1 = {
    "code": "ORG001",
    "preferredLabel": "LexCorp",
    "alternativeLabels": ["LuthorCorp"],
    "purpose": [101],
    "spatial": [spatial_data],
    "identifier": "LEX123",
    "subOrganizationOf": "INC001",
    "organizationType": 1,
    "description": "International conglomerate",
    "url": "http://www.lexcorp.com",
    "contactPoint": contact_point_data,
    "vatId": "VAT1234",
    "status": "Active",
    "foundationDate": "1989-10-18T00:00:00Z",
    "terminationDate": None,
    "mainDataUpdateDate": "2023-04-01T12:34:56Z",
    "organizationStructureUpdateDate": "2023-04-01T12:34:56Z",
    "foundationFek": foundation_fek_data,
    "mainAddress": main_address,
    "secondaryAddresses": [secondary_address]
}

# Second Organization Dictionary
organization_2 = {
    "code": "ORG002",
    "preferredLabel": "Wayne Enterprises",
    "alternativeLabels": ["WayneCorp", "Wayne Industries"],
    "purpose": [102],
    "spatial": [spatial_data],
    "identifier": "WAY123",
    "subOrganizationOf": "INC002",
    "organizationType": 2,
    "description": "Multinational conglomerate",
    "url": "http://www.wayneenterprises.com",
    "contactPoint": contact_point_data,
    "vatId": "VAT5678",
    "status": "Active",
    "foundationDate": "1939-05-01T00:00:00Z",
    "terminationDate": None,
    "mainDataUpdateDate": "2023-04-02T12:34:56Z",
    "organizationStructureUpdateDate": "2023-04-02T12:34:56Z",
    "foundationFek": foundation_fek_data,
    "mainAddress": main_address,
    "secondaryAddresses": [secondary_address]
}

# List of all org

indexes = {
    "monades": {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "code": {
                    "type": "text"
                },
                "organizationCode": {
                    "type": "text"
                },
                "supervisorUnitCode": {
                    "type": "text"
                },
                "preferredLabel": {
                    "type": "text"
                },
                "alternativeLabels": {
                    "type": "text"
                },
                "description": {
                    "type": "text"
                },
                "email": {
                    "type": "text"
                },
                "telephone": {
                    "type": "text"
                },
                "url": {
                    "type": "text"
                },
                "mainAddress": {
                    "type": "text"
                },
            }
        }
    },
    "foreis": {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "code": {
                    "type": "text"
                },
                "preferredLabel": {
                    "type": "text"
                },
                "alternativeLabels": {
                    "type": "text"
                },
                "identifier": {
                    "type": "text"
                },
                "subOrganizationOf": {
                    "type": "text"
                },
                "description": {
                    "type": "text"
                },
                "url": {
                    "type": "text"
                },
                "contactPoint": {
                    "type": "text"
                },
                "vatId": {
                    "type": "text"
                },
                "status": {
                    "type": "text"
                },
                "foundationDate": {
                    "type": "text"
                },
                "terminationDate": {
                    "type": "text"
                },
                "mainDataUpdateDate": {
                    "type": "text"
                },
                "organizationStructureUpdateDate": {
                    "type": "text"
                },
                "foundationFek": {
                    "type": "text"
                },
                "mainAddress": {
                    "type": "text"
                }
            }
        }
    }
}


def create_elastic_index():
    elastic_host: str = "http://localhost:9200"
    es = Elasticsearch(elastic_host, http_auth=('elastic', '1234'))

   
    es.indices.create(index="monades", body=indexes['monades'])

    es.indices.create(index="foreis", body=indexes['foreis'])

    # organizations = [
    #     {
    #         "organization_name":
    #         "Green Earth",
    #         "remit":
    #         "Focusing on reforestation and protecting deforestation globally."
    #     },
    #     {
    #         "organization_name":
    #         "Oceanic Preservation",
    #         "remit":
    #         "Dedicated to preserving and protecting the world's oceans and marine life."
    #     },
    #     {
    #         "organization_name":
    #         "Εργαστήριο Ψηφιακής Τεχνολογίας για Τεχνικά Έργα",
    #         "remit": demo_remit
    #     },
    # ]

    # organizations.extend(create_dummy_date())

    # Index organizations
    for org in organizations:
        es.index(index="foreis", document=org)

    for org_unit in organization_units:
        es.index(index='monades', document=org_unit)

try:
    create_elastic_index()
except Exception as e:
    print(e)

import mongoengine

mongoengine.connect('psped', host='localhost', port=27017,alias='psped')
mongoengine.connect('apografi', host='localhost', port=27017,alias='apografi')
foreas_first = Foreas.objects.first()


breakpoint()