from django.core.management.base import BaseCommand
from catalogo.models import Risorsa

class Command(BaseCommand):
    help = 'Resetta le risorse del catalogo con dati di esempio'

    def handle(self, *args, **kwargs):
        self.stdout.write('Inizio pulizia e popolamento database...')
        
        # Pulizia del database
        Risorsa.objects.all().delete()

        # Film
        Risorsa.objects.create(
            titolo="Batman: Cavaliere oscuro",
            descrizione="Il Cavaliere oscuro è un film d'azione e thriller psicologico del 2008 diretto da Christopher Nolan.",
            prezzo=10.0,
        )

        Risorsa.objects.create(
            titolo="Il Signore degli Anelli: Il ritorno del re",
            descrizione="Il Signore degli Anelli: Il ritorno del re è un film fantasy del 2003 diretto da Peter Jackson.",
            prezzo=15.0,
        )

        Risorsa.objects.create(
            titolo="Il Padrino",
            descrizione="Il Padrino è un film crime del 1972 diretto da Francis Ford Coppola.",
            prezzo=20.0,
        )

        Risorsa.objects.create(
            titolo="Il Padrino Parte II",
            descrizione="Il Padrino Parte II è un film crime del 1974 diretto da Francis Ford Coppola.",
            prezzo=25.0,
        )

        Risorsa.objects.create(
            titolo="Pulp Fiction",
            descrizione="Pulp Fiction è un film crime del 1994 diretto da Quentin Tarantino, noto per la sua narrazione non lineare.",
            prezzo=12.5,
        )

        Risorsa.objects.create(
            titolo="Inception",
            descrizione="Inception è un film di fantascienza del 2010 diretto da Christopher Nolan, che esplora il concetto di furto di idee attraverso i sogni.",
            prezzo=14.0,
        )

        Risorsa.objects.create(
            titolo="Forrest Gump",
            descrizione="Forrest Gump è un film drammatico del 1994 diretto da Robert Zemeckis, che racconta la vita di un uomo con un QI basso ma un grande cuore.",
            prezzo=11.0,
        )

        Risorsa.objects.create(
            titolo="Matrix",
            descrizione="Matrix è un film di fantascienza del 1999 diretto dalle sorelle Wachowski, che esplora un mondo simulato controllato da macchine.",
            prezzo=13.0,
        )

        # Libri
        Risorsa.objects.create(
            titolo="Il Signore degli Anelli: La Compagnia dell'Anello",
            descrizione="Primo volume della trilogia fantasy scritta da J.R.R. Tolkien, che narra l'inizio dell'avventura per distruggere l'Anello del Potere.",
            prezzo=18.0,
        )

        Risorsa.objects.create(
            titolo="1984",
            descrizione="1984 è un romanzo distopico di George Orwell, che descrive un futuro in cui il governo controlla ogni aspetto della vita dei cittadini.",
            prezzo=9.5,
        )

        Risorsa.objects.create(
            titolo="Il Grande Gatsby",
            descrizione="Il Grande Gatsby è un romanzo scritto da F. Scott Fitzgerald, che esplora temi come il sogno americano e la decadenza morale.",
            prezzo=10.5,
        )

        Risorsa.objects.create(
            titolo="Harry Potter e la Pietra Filosofale",
            descrizione="Primo libro della saga fantasy di J.K. Rowling, che racconta le avventure del giovane mago Harry Potter.",
            prezzo=12.0,
        )

        # Corsi online
        Risorsa.objects.create(
            titolo="Corso di Python per principianti",
            descrizione="Un corso completo per imparare le basi di Python, dalla sintassi alle strutture dati.",
            prezzo=49.99,
        )

        Risorsa.objects.create(
            titolo="Corso avanzato di Django",
            descrizione="Un corso per sviluppatori che vogliono approfondire Django, dalla creazione di API alla gestione di progetti complessi.",
            prezzo=79.99,
        )

        Risorsa.objects.create(
            titolo="Master in Data Science",
            descrizione="Un percorso formativo per imparare a analizzare dati con Python, SQL e strumenti di machine learning.",
            prezzo=199.99,
        )

        # Musica
        Risorsa.objects.create(
            titolo="Album: The Dark Side of the Moon",
            descrizione="Album dei Pink Floyd pubblicato nel 1973, considerato uno dei migliori album di tutti i tempi.",
            prezzo=15.0,
        )

        Risorsa.objects.create(
            titolo="Album: Thriller",
            descrizione="Album di Michael Jackson pubblicato nel 1982, il più venduto della storia.",
            prezzo=14.0,
        )

        # Videogiochi
        Risorsa.objects.create(
            titolo="The Legend of Zelda: Breath of the Wild",
            descrizione="Videogioco di avventura sviluppato da Nintendo per Nintendo Switch, noto per il suo mondo aperto e la libertà di esplorazione.",
            prezzo=59.99,
        )

        Risorsa.objects.create(
            titolo="Red Dead Redemption 2",
            descrizione="Videogioco di azione e avventura sviluppato da Rockstar Games, ambientato nel Vecchio West.",
            prezzo=49.99,
        )

        # Strumenti software
        Risorsa.objects.create(
            titolo="Licenza Adobe Photoshop",
            descrizione="Licenza annuale per Adobe Photoshop, il software di editing grafico più utilizzato al mondo.",
            prezzo=239.88,
        )

        Risorsa.objects.create(
            titolo="Licenza JetBrains PyCharm Professional",
            descrizione="Licenza annuale per PyCharm Professional, l'IDE di JetBrains per lo sviluppo in Python.",
            prezzo=139.0,
        )
        
        self.stdout.write(self.style.SUCCESS('Database popolato con successo!'))
