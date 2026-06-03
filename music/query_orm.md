# GENERI

Genere.objects.create( titolo="Rock" );

Genere.objects.create( titolo="Pop" );

Genere.objects.create( titolo="Jezz" );

Genere.objects.create( titolo="Classica" );

# TAGS

Tag.objects.create( titolo="Avvincente" );
Tag.objects.create( titolo="Introspettivo" );
Tag.objects.create( titolo="Comico" );
Tag.objects.create( titolo="Romantico" );
Tag.objects.create( titolo="Profondo" );

# ARTISTI

Artista.objects.create(
    nome        ="Linkin Park",
    nazionalita ="USA",
    biografia   ="Nu-metal/Alternative rock band formed in Agoura Hills, California.",
);

Artista.objects.create(
    nome        ="Miles Davis",
    nazionalita ="USA",
    biografia   ="One of the most influential and acclaimed figures in the history of jazz and 20th-century music.",
);

Artista.objects.create(
    nome        ="Antonio Vivaldi",
    nazionalita ="Italia",
    biografia   ="Compositore e violinista barocco, noto per i suoi numerosi concerti per violino.",
);

# ALBUM

Album.objects.create(
    artista =Artista.objects.get(nome="Linkin Park"),
    titolo ="Meteora",
    anno =2003,
    genere = Genere.objects.get(titolo="Rock"),
);

Album.objects.create(
    artista =Artista.objects.get(nome="Linkin Park"),
    titolo ="One More Light",
    anno =2017,
    genere = Genere.objects.get(titolo="Pop"),
);

Album.objects.create(
    artista =Artista.objects.get(nome="Miles Davis"),
    titolo ="Kind of Blue",
    anno =1959,
    genere = Genere.objects.get(titolo="Jezz"),
);

Album.objects.create(
    artista =Artista.objects.get(nome="Antonio Vivaldi"),
    titolo ="The Four Seasons",
    anno =1725,
    genere = Genere.objects.get(titolo="Classica"),
);

# CANZONI

## Meteora

Canzone.objects.create(
    album =Album.objects.get(titolo="Meteora"),
    titolo ="Somewhere I Belong",
    durata_secondi =213,
    traccia =3,
);

faint =Canzone.objects.create(
    album =Album.objects.get(titolo="Meteora"),
    titolo ="Faint",
    durata_secondi =162,
    traccia =7,
);
tags =Tag.objects.filter( titolo__in=["Avvincente", "Introspettivo"] );
faint.tags.set(tags);

Canzone.objects.create(
    album =Album.objects.get(titolo="Meteora"),
    titolo ="Numb",
    durata_secondi =187,
    traccia =13,
);

## One More Light

Canzone.objects.create(
    album =Album.objects.get(titolo="One More Light"),
    titolo ="Heavy",
    durata_secondi =169,
    traccia =6,
);

Canzone.objects.create(
    album =Album.objects.get(titolo="One More Light"),
    titolo ="One More Light",
    durata_secondi =255,
    traccia =9,
);

Canzone.objects.create(
    album =Album.objects.get(titolo="One More Light"),
    titolo ="Sharp Edges",
    durata_secondi =178,
    traccia =10,
);

# Kind of Blue

Canzone.objects.create(
    album =Album.objects.get(titolo="Kind of Blue"),
    titolo ="So What",
    durata_secondi =562,
    traccia =1,
);

Canzone.objects.create(
    album =Album.objects.get(titolo="Kind of Blue"),
    titolo ="Freddie Freeloader",
    durata_secondi =586,
    traccia =2,
);

Canzone.objects.create(
    album =Album.objects.get(titolo="Kind of Blue"),
    titolo ="Blue in Green",
    durata_secondi =337,
    traccia =3,
);

# The Four Seasons

Canzone.objects.create(
    album =Album.objects.get(titolo="The Four Seasons"),
    titolo ="Spring - I. Allegro",
    durata_secondi =210,
    traccia =1,
);

Canzone.objects.create(
    album =Album.objects.get(titolo="The Four Seasons"),
    titolo ="Summer - III. Presto",
    durata_secondi =180,
    traccia =6,
);

Canzone.objects.create(
    album =Album.objects.get(titolo="The Four Seasons"),
    titolo ="Winter - II. Largo",
    durata_secondi =120,
    traccia =11,
);

# VISUALIZZAZIONE

* ordina gli album dal più recente al più antico
  Album.objects.order_by("-anno")
* album di genere rock o jezz
  Album.objects.filter( genere__titolo__in=["Rock","Jezz"] );
* quante canzoni ha l'album con id=3?
  Canzone.objects.filter( album__id=3 )
* titolo e durata delle canzoni dell'artista 'mercury' ordinate per numero di traccia
  Canzone.objects.filter( album__artista__nome="Linkin Park" ) .order_by("traccia")
* usando una sola query con update() imposta disponibile=False in tutti gli album prima del 1970
  Album.objects.filter( anno__lt=1970 ) .update(disponibile=False)


