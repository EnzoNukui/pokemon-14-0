# Pesquisa de referência: seleção e times de 100 treinadores

**Status:** documento de pesquisa histórica. A lista usada para importação e os times ativos/inativos estão em `elenco_aprovado.json`; esse arquivo JSON é a fonte atual do seed.

## Como este recorte foi montado

- Fonte: [dataset “Pokémon Gen 1–9 Gym Leaders & Elite Four” no Kaggle](https://www.kaggle.com/datasets/maxiboo/pokemon-gen-1-9-gym-leaders-elite-four), versão 3, arquivo `PokemonGymLeaders.csv`.
- Foram identificados 119 personagens distintos após juntar variações de nome que representam a mesma pessoa (por exemplo, `Champion Blue Bulbasaur` e `Champion Blue Squirtle` viram **Blue**).
- A seleção contém 100 personagens e cobre as nove regiões. Inclui líderes de ginásio, Elite Four, campeões e equivalentes de Alola (Kahunas/capitães de prova).
- Para cada personagem, escolhi **um time que já existe na fonte**: primeiro o que tem mais integrantes; em empate, o que tem o Pokémon de nível mais alto; depois, a geração mais recente. A linha informa jogo/local de origem e quantidade de Pokémon.
- Pokémon repetidos no mesmo time foram preservados. Nenhum time recebeu Pokémon por preenchimento automático.
- Três rivais, uma capitã de prova e 15 representantes de menor prioridade ficaram fora do recorte de 100. As exclusões estão listadas no fim para revisão.

## Lista selecionada

### Kanto

| Treinador | Papel na fonte | Time-fonte escolhido | Integrantes | Pokémon já registrados |
|---|---|---|---:|---|
| Agatha | Elite Four | Gen. 1, Red — Elite Four | 5/6 | Gengar, Golbat, Haunter, Arbok, Gengar |
| Blaine | Líder regional (ginásio ou função equivalente) | Gen. 1, Red — Cinnabar Island | 4/6 | Growlithe, Ponyta, Rapidash, Arcanine |
| Blue | Campeão | Gen. 1, Red — Elite Four | 6/6 | Pidgeot, Alakazam, Rhydon, Arcanine, Gyarados, Venusaur |
| Brock | Líder regional (ginásio ou função equivalente) | Gen. 2, Gold — Pewter City | 5/6 | Graveler, Rhyhorn, Omastar, Onix, Kabutops |
| Bruno | Elite Four | Gen. 1, Red — Elite Four | 5/6 | Onix, Hitmonchan, Hitmonlee, Onix, Machamp |
| Erika | Líder regional (ginásio ou função equivalente) | Gen. 2, Gold — Celadon City | 4/6 | Tangela, Jumpluff, Victreebel, Bellossom |
| Giovanni | Líder regional (ginásio ou função equivalente) | Gen. 1, Yellow — Viridian City | 5/6 | Dugtrio, Persian, Nidoqueen, Nidoking, Rhydon |
| Koga | Elite Four | Gen. 2, Crystal — Elite Four | 5/6 | Ariados, Venomoth, Forretress, Muk, Crobat |
| Lorelei | Elite Four | Gen. 1, Red — Elite Four | 5/6 | Dewgong, Cloyster, Slowbro, Jynx, Lapras |
| Lt. Surge | Líder regional (ginásio ou função equivalente) | Gen. 2, Gold — Vermilion City | 5/6 | Raichu, Electrode, Electrode, Magneton, Electabuzz |
| Misty | Líder regional (ginásio ou função equivalente) | Gen. 2, Gold — Cerulean City | 4/6 | Golduck, Quagsire, Lapras, Starmie |
| Sabrina | Líder regional (ginásio ou função equivalente) | Gen. 1, Red — Saffron City | 4/6 | Kadabra, Mr. Mime, Venomoth, Alakazam |

### Johto

| Treinador | Papel na fonte | Time-fonte escolhido | Integrantes | Pokémon já registrados |
|---|---|---|---:|---|
| Clair | Líder regional (ginásio ou função equivalente) | Gen. 2, Crystal — Blackthorn City | 4/6 | Dragonair, Dragonair, Dragonair, Kingdra |
| Jasmine | Líder regional (ginásio ou função equivalente) | Gen. 2, Crystal — Olivine City | 3/6 | Magnemite, Magnemite, Steelix |
| Janine | Líder regional (ginásio ou função equivalente) | Gen. 2, Gold — Fuchsia City | 5/6 | Crobat, Weezing, Weezing, Ariados, Venomoth |
| Karen | Elite Four | Gen. 2, Gold — Elite Four | 5/6 | Umbreon, Vileplume, Gengar, Murkrow, Houndoom |
| Lance | Campeão | Gen. 2, Gold — Elite Four | 6/6 | Gyarados, Dragonite, Dragonite, Aerodactyl, Charizard, Dragonite |
| Morty | Líder regional (ginásio ou função equivalente) | Gen. 2, Gold — Ecruteak City | 4/6 | Gastly, Haunter, Haunter, Gengar |
| Pryce | Líder regional (ginásio ou função equivalente) | Gen. 2, Gold — Mahogany Town | 3/6 | Seel, Dewgong, Piloswine |
| Whitney | Líder regional (ginásio ou função equivalente) | Gen. 2, Gold — Goldenrod City | 2/6 | Clefairy, Miltank |
| Will | Elite Four | Gen. 2, Gold — Elite Four | 5/6 | Xatu, Jynx, Exeggutor, Slowbro, Xatu |

### Hoenn

| Treinador | Papel na fonte | Time-fonte escolhido | Integrantes | Pokémon já registrados |
|---|---|---|---:|---|
| Drake | Elite Four | Gen. 3, Ruby — Elite Four | 5/6 | Shelgon, Altaria, Flygon, Flygon, Salamence |
| Flannery | Líder regional (ginásio ou função equivalente) | Gen. 3, Emerald — Lavaridge Town | 4/6 | Numel, Slugma, Camerupt (CSV: Camelrupt), Torkoal |
| Flint | Elite Four | Gen. 4, Diamond — Elite Four | 5/6 | Rapidash, Steelix, Drifblim, Lopunny, Infernape |
| Glacia | Elite Four | Gen. 3, Ruby — Elite Four | 5/6 | Glalie, Sealeo, Sealeo, Glalie, Walrein |
| Juan | Líder regional (ginásio ou função equivalente) | Gen. 3, Emerald — Sootopolis City | 5/6 | Luvdisc, Whiscash, Sealeo, Crawdaunt, Kingdra |
| Norman | Líder regional (ginásio ou função equivalente) | Gen. 3, Emerald — Petalburg City | 4/6 | Spinda, Vigoroth, Linoone, Slaking |
| Phoebe | Elite Four | Gen. 3, Ruby — Elite Four | 5/6 | Dusclops, Banette, Banette, Sableye, Dusclops |
| Sidney | Elite Four | Gen. 3, Ruby — Elite Four | 5/6 | Mightyena, Cacturne, Shiftry, Sharpedo, Absol |
| Steven | Campeão | Gen. 3, Emerald — Elite Four | 6/6 | Skarmory, Claydol, Cradily, Armaldo, Aggron, Metagross |
| Tate & Liza | Líder regional (ginásio ou função equivalente) | Gen. 3, Emerald — Mossdeep City | 4/6 | Claydol, Xatu, Lunatone, Solrock |
| Wallace | Elite Four | Gen. 3, Emerald — Elite Four | 6/6 | Tentacruel, Gyarados, Ludicolo, Whiscash, Wailord, Milotic |
| Wattson | Líder regional (ginásio ou função equivalente) | Gen. 3, Emerald — Mauville City | 4/6 | Voltorb, Electrike, Magnemite, Manectric |
| Winona | Líder regional (ginásio ou função equivalente) | Gen. 3, Emerald — Fortree City | 5/6 | Swablu, Tropius, Pelipper, Skarmory, Altaria |

### Sinnoh

| Treinador | Papel na fonte | Time-fonte escolhido | Integrantes | Pokémon já registrados |
|---|---|---|---:|---|
| Aaron | Elite Four | Gen. 4, Diamond — Elite Four | 5/6 | Dustox, Beautifly, Vespiquen, Heracross, Drapion |
| Bertha | Elite Four | Gen. 4, Diamond — Elite Four | 5/6 | Quagsire, Sudowoodo, Golem, Whiscash, Hippowdon |
| Byron | Líder regional (ginásio ou função equivalente) | Gen. 4, Platinum — Canalave City | 3/6 | Magneton, Steelix, Bastiodon |
| Candice | Líder regional (ginásio ou função equivalente) | Gen. 4, Platinum — Snowpoint City | 4/6 | Sneasel, Piloswine, Abomasnow, Froslass |
| Crasher Wake | Líder regional (ginásio ou função equivalente) | Gen. 4, Platinum — Pastoria City | 3/6 | Gyarados, Quagsire, Floatzel |
| Cynthia | Campeão | Gen. 4, Diamond — Elite Four | 6/6 | Spiritomb, Roserade, Gastrodon, Lucario, Milotic, Garchomp |
| Fantina | Líder regional (ginásio ou função equivalente) | Gen. 4, Diamond — Hearthome City | 3/6 | Drifblim, Gengar, Mismagius |
| Gardenia | Líder regional (ginásio ou função equivalente) | Gen. 4, Platinum — Eterna City | 3/6 | Turtwig, Cherrim, Roserade |
| Lucian | Elite Four | Gen. 4, Diamond — Elite Four | 5/6 | Mr. Mime, Girafarig, Medicham, Alakazam, Bronzong |
| Maylene | Líder regional (ginásio ou função equivalente) | Gen. 4, Platinum — Veilstone Town | 3/6 | Meditite, Machoke, Lucario |
| Roark | Líder regional (ginásio ou função equivalente) | Gen. 4, Platinum — Oreburgh City | 3/6 | Geodude, Onix, Cranidos |
| Volkner | Líder regional (ginásio ou função equivalente) | Gen. 4, Platinum — Sunyshore City | 4/6 | Jolteon, Raichu, Luxray, Electivire |

### Unova

| Treinador | Papel na fonte | Time-fonte escolhido | Integrantes | Pokémon já registrados |
|---|---|---|---:|---|
| Alder | Campeão | Gen. 5, Black — Elite Four | 6/6 | Accelgor, Bouffalant, Druddigon, Vanilluxe, Escavalier, Volcarona |
| Brycen | Líder regional (ginásio ou função equivalente) | Gen. 5, Black — Icirrus City | 3/6 | Vanillish, Cryogonal, Beartic |
| Burgh | Líder regional (ginásio ou função equivalente) | Gen. 5, Black — Castelia City | 3/6 | Whirlipede, Dwebble, Leavanny |
| Caitlin | Elite Four | Gen. 5, Black — Elite Four | 4/6 | Reuniclus, Musharna, Sigilyph, Gothitelle |
| Clay | Líder regional (ginásio ou função equivalente) | Gen. 5, Black — Driftveil City | 3/6 | Krokorok, Palpitoad, Excadrill |
| Drayden | Líder regional (ginásio ou função equivalente) | Gen. 5, Black — Opelucid City | 3/6 | Fraxure, Druddigon, Haxorus |
| Elesa | Líder regional (ginásio ou função equivalente) | Gen. 5, Black — Nimbasa City | 3/6 | Emolga, Emolga, Zebstrika |
| Grimsley | Elite Four | Gen. 5, Black — Elite Four | 4/6 | Scrafty, Liepard, Krookodile, Bisharp |
| Iris | Líder regional (ginásio ou função equivalente) | Gen. 5, White — Opelucid City | 3/6 | Fraxure, Druddigon, Haxorus |
| Marshal | Elite Four | Gen. 5, Black — Elite Four | 4/6 | Throh, Sawk, Conkeldurr, Mienshao |
| Shauntal | Elite Four | Gen. 5, Black — Elite Four | 4/6 | Cofagrigus, Jellicent, Golurk, Chandelure |
| Skyla | Líder regional (ginásio ou função equivalente) | Gen. 5, Black — Mistralton City | 3/6 | Swoobat, Unfezant, Swanna |

### Kalos

| Treinador | Papel na fonte | Time-fonte escolhido | Integrantes | Pokémon já registrados |
|---|---|---|---:|---|
| Clemont | Líder regional (ginásio ou função equivalente) | Gen. 6, X — Lumiose City | 3/6 | Emolga, Magneton, Heliolisk |
| Diantha | Campeão | Gen. 6, X — Elite Four | 6/6 | Hawlucha, Tyrantrum, Aurorus, Gourgeist, Goodra, Gardevoir |
| Drasna | Elite Four | Gen. 6, X — Elite Four | 4/6 | Dragalge, Altaria, Druddigon, Noivern |
| Korrina | Líder regional (ginásio ou função equivalente) | Gen. 6, X — Shalour City | 3/6 | Mienfoo, Hawlucha, Machoke |
| Malva | Elite Four | Gen. 6, X — Elite Four | 4/6 | Pyroar, Torkoal, Chandelure, Talonflame |
| Olympia | Líder regional (ginásio ou função equivalente) | Gen. 6, X — Anistar City | 3/6 | Sigilyph, Slowking, Meowstic |
| Siebold | Elite Four | Gen. 6, X — Elite Four | 4/6 | Clawitzer, Starmie, Gyarados, Barbaracle |
| Valerie | Líder regional (ginásio ou função equivalente) | Gen. 6, X — Laverre City | 3/6 | Mawile, Mr. Mime, Sylveon |
| Wikstrom | Elite Four | Gen. 6, X — Elite Four | 4/6 | Klefki, Probopass, Scizor, Aegislash |
| Wulfric | Líder regional (ginásio ou função equivalente) | Gen. 6, X — Snowbelle City | 3/6 | Abomasnow, Cryogonal, Avalugg |

### Alola

| Treinador | Papel na fonte | Time-fonte escolhido | Integrantes | Pokémon já registrados |
|---|---|---|---:|---|
| Acerola | Líder regional (ginásio ou função equivalente) | Gen. 7, Sun — Pokémon League | 5/6 | Sableye, Drifblim, Dhelmise, Froslass, Palossand |
| Hala | Elite Four | Gen. 7, Sun — Elite Four | 5/6 | Hariyama, Primeape, Bewear, Poliwrath, Crabominable |
| Hapu | Líder regional (ginásio ou função equivalente) | Gen. 7, Sun — Vast Poni Canyon | 4/6 | Dugtrio, Gastrodon, Flygon, Mudsdale |
| Ilima | Líder regional (ginásio ou função equivalente) | Gen. 7, Sun — Hau'oli City | 2/6 | Gumshoos, Smeargle |
| Kahili | Elite Four | Gen. 7, Sun — Elite Four | 5/6 | Skarmory, Crobat, Oricorio, Mandibuzz, Toucannon |
| Kiawe | Líder regional (ginásio ou função equivalente) | Gen. 7, Sun — Royal Avenue | 3/6 | Growlithe, Fletchinder, Marowak |
| Kukui | Elite Four | Gen. 7, Sun — Elite Four | 6/6 | Lycanroc, Ninetales, Braviary, Magnezone, Snorlax, Incineroar |
| Lana | Líder regional (ginásio ou função equivalente) | Gen. 7, Sun — Brooklet Hill | 3/6 | Chinchou, Shellder, Araquanid |
| Nanu | Líder regional (ginásio ou função equivalente) | Gen. 7, Sun — Malie City | 3/6 | Sableye, Krokorok, Persian |
| Olivia | Elite Four | Gen. 7, Sun — Elite Four | 5/6 | Relicanth, Carbink, Golem, Probopass, Lycanroc |
| Sophocles | Líder regional (ginásio ou função equivalente) | Gen. 7, Sun — Pokémon League | 5/6 | Togedemaru, Magnezone, Electivire, Vikavolt, Golem |

### Galar

| Treinador | Papel na fonte | Time-fonte escolhido | Integrantes | Pokémon já registrados |
|---|---|---|---:|---|
| Allister | Líder regional (ginásio ou função equivalente) | Gen. 8, Shield — Champion Cup | 5/6 | Dusknoir, Chandelure, Cursola, Polteageist, Gengar |
| Bea | Líder regional (ginásio ou função equivalente) | Gen. 8, Sword — Champion Cup | 5/6 | Hawlucha, Grapploct, Sirfetch'd, Falinks, Machamp |
| Gordie | Líder regional (ginásio ou função equivalente) | Gen. 8, Sword — Circhester | 4/6 | Barbaracle, Shuckle, Stonjourner, Coalossal |
| Kabu | Líder regional (ginásio ou função equivalente) | Gen. 8, Sword — Motostoke | 3/6 | Ninetales, Arcanine, Centiskorch |
| Leon | Campeão | Gen. 8, Sword — Champion Cup | 6/6 | Aegislash, Dragapult, Haxorus, Seismitoad, Cinderace, Charizard |
| Melony | Líder regional (ginásio ou função equivalente) | Gen. 8, Shield — Circhester | 4/6 | Frosmoth, Darmanitan, Eiscue, Lapras |
| Nessa | Líder regional (ginásio ou função equivalente) | Gen. 8, Sword — Champion Cup | 5/6 | Golisopod, Pelipper, Barraskewda, Seaking, Drednaw |
| Opal | Líder regional (ginásio ou função equivalente) | Gen. 8, Sword — Ballonlea | 4/6 | Weezing, Mawile, Togekiss, Alcremie |
| Piers | Líder regional (ginásio ou função equivalente) | Gen. 8, Sword — Spikemuth | 4/6 | Scrafty, Malamar, Skuntank, Obstagoon |
| Raihan | Líder regional (ginásio ou função equivalente) | Gen. 8, Sword — Champion Cup | 5/6 | Torkoal, Goodra, Turtonator, Flygon, Duraludon |

### Paldea

| Treinador | Papel na fonte | Time-fonte escolhido | Integrantes | Pokémon já registrados |
|---|---|---|---:|---|
| Brassius | Líder regional (ginásio ou função equivalente) | Gen. 9, Scarlet — Artazon | 3/6 | Petilil, Smoliv, Sudowoodo |
| Geeta | Campeão | Gen. 9, Scarlet — Elite Four | 6/6 | Espathra, Gogoat, Veluza, Avalugg, Kingambit, Glimmora |
| Grusha | Líder regional (ginásio ou função equivalente) | Gen. 9, Scarlet — Glaseado | 4/6 | Frosmoth, Beartic, Cetitan, Altaria |
| Hassel | Elite Four | Gen. 9, Scarlet — Elite Four | 5/6 | Noivern, Haxorus, Dragalge, Flapple, Baxcalibur |
| Iono | Líder regional (ginásio ou função equivalente) | Gen. 9, Scarlet — Levincia | 4/6 | Wattrel, Bellibolt, Luxio, Mismagius |
| Kofu | Líder regional (ginásio ou função equivalente) | Gen. 9, Scarlet — Cascarrafa | 3/6 | Veluza, Wugtrio, Crabominable |
| Larry | Elite Four | Gen. 9, Scarlet — Elite Four | 5/6 | Tropius, Oricorio, Altaria, Staraptor, Flamigo |
| Poppy | Elite Four | Gen. 9, Scarlet — Elite Four | 4/6 | Copperajah, Magnezone, Bronzong, Corviknight |
| Rika | Elite Four | Gen. 9, Scarlet — Elite Four | 5/6 | Whiscash, Camerupt, Donphan, Dugtrio, Clodsire |
| Ryme | Líder regional (ginásio ou função equivalente) | Gen. 9, Scarlet — Montenevera | 4/6 | Banette, Mimikyu, Houndstone, Toxtricity |
| Tulip | Líder regional (ginásio ou função equivalente) | Gen. 9, Scarlet — Alfornada | 4/6 | Farigiraf, Gardevoir, Espathra, Florges |

## Fora deste recorte

**Fora do recorte de 100:** Bede, Hop e Marnie (rivais); Mina (capitã de prova).

**Líderes de menor prioridade para caber no limite:** Brawly, Bugsy, Cilan, Chili, Chuck, Cress, Falkner, Grant, Katy, Lenora, Mallow, Milo, Ramos, Roxanne, Viola.

## Notas registradas durante a pesquisa

1. Esta seleção conserva os times como aparecem no Kaggle, inclusive times com menos de seis Pokémon e repetições oficiais de espécies. Um time com menos de seis continua parcial.
2. O catálogo e a engine foram posteriormente expandidos até a geração IX, usando o formato Singles `gen9nationaldexag`. Os times alternativos completos continuam registrados como escalações próprias, sem combinar Pokémon de batalhas diferentes.
3. “Mais famoso” é uma escolha editorial, não um campo medido pelo dataset. A lista é uma proposta equilibrada entre regiões, relevância dos personagens e a prioridade anterior por treinadores fortes.
4. O CSV tem nomes com grafia inconsistente; `Camelrupt` foi apresentado como Camerupt com a grafia original indicada.

## Pesquisa de escalações oficiais alternativas

Esta seção registra equipes completas encontradas em jogos ou batalhas do anime. Elas **não foram mescladas** aos times do Kaggle acima: cada uma representa uma escalação própria, identificada por jogo ou batalha. Assim evitamos completar um time com Pokémon que o personagem usou em outra ocasião.

### Pokémon Stadium 2 — Gym Leader Castle, Round 1

O jogo fornece estas escalações de seis Pokémon para personagens que aparecem incompletos no recorte do Kaggle:

| Treinador | Escalação completa em Pokémon Stadium 2 | Efeito sobre a linha do Kaggle | Fonte |
|---|---|---|---|
| Brock | Golem, Onix, Pinsir, Omastar, Kabutops, Forretress | Alternativa completa ao registro 5/6 | [Pewter Gym](https://www.serebii.net/stadium2/pewtergym.shtml) |
| Misty | Golduck, Poliwhirl, Starmie, Togetic, Sunflora, Quagsire | Alternativa completa ao registro 4/6 | [Cerulean Gym](https://www.serebii.net/stadium2/ceruleangym.shtml) |
| Lt. Surge | Raichu, Magneton, Electrode, Electabuzz, Porygon, Lanturn | Alternativa completa ao registro 5/6 | [Vermilion Gym](https://www.serebii.net/stadium2/vermiliongym.shtml) |
| Erika | Venusaur, Chansey, Tangela, Vaporeon, Bellossom, Jumpluff | Alternativa completa ao registro 4/6 | [Celadon Gym](https://www.serebii.net/stadium2/celadongym.shtml) |
| Blaine | Ninetales, Parasect, Rapidash, Flareon, Magcargo, Octillery | Alternativa completa ao registro 4/6 | [Cinnabar Gym](https://www.serebii.net/stadium2/cinnabargym.shtml) |
| Sabrina | Wigglytuff, Alakazam, Slowbro, Hypno, Mr. Mime, Furret | Alternativa completa ao registro 4/6 | [Saffron Gym](https://www.serebii.net/stadium2/saffrongym.shtml) |
| Janine | Tentacruel, Weezing, Ariados, Crobat, Gligar, Stantler | Alternativa completa ao registro 5/6 | [Fuchsia Gym](https://www.serebii.net/stadium2/fuchsiagym.shtml) |
| Clair | Arcanine, Rhydon, Lapras, Dragonair, Ampharos, Kingdra | Alternativa completa ao registro 4/6 | [Blackthorn Gym](https://www.serebii.net/stadium2/blackthorngym.shtml) |
| Will | Clefable, Kadabra, Exeggutor, Jynx, Xatu, Girafarig | Alternativa completa ao registro 5/6 | [Elite Four](https://www.serebii.net/stadium2/elitefour.shtml) |
| Koga | Golbat, Venomoth, Muk, Electrode, Ariados, Gligar | Alternativa completa ao registro 5/6 | [Elite Four](https://www.serebii.net/stadium2/elitefour.shtml) |
| Bruno | Blastoise, Machamp, Golem, Onix, Kangaskhan, Heracross | Alternativa completa ao registro 5/6 | [Elite Four](https://www.serebii.net/stadium2/elitefour.shtml) |
| Karen | Vileplume, Victreebel, Gengar, Magmar, Umbreon, Murkrow | Alternativa completa ao registro 5/6 | [Elite Four](https://www.serebii.net/stadium2/elitefour.shtml) |

As escolhas de *Stadium 2* incluem espécies fora da especialidade de alguns líderes. Isso é intencional: são as equipes definidas pelo jogo, não uma tentativa de reconstruir um time temático. Blue também tem uma equipe alternativa completa no jogo (Pidgeot, Arcanine, Alakazam, Exeggutor, Rhydon e Gyarados), mas já possui seis integrantes na linha selecionada.

### Pokémon World Tournament — Black 2/White 2

O PWT amplia bastante a busca: nos torneios regionais de Kanto, Johto, Hoenn, Sinnoh e Unova, cada líder tem uma escalação alternativa de seis. Estes são os times já conferidos para personagens que estão abaixo de seis na seleção. As fontes regionais contêm também os demais líderes e suas equipes completas.

| Região | Treinador | Equipe de seis do PWT |
|---|---|---|
| Kanto | Brock | Onix, Golem, Kabutops, Omastar, Aerodactyl, Relicanth |
| Kanto | Misty | Starmie, Lanturn, Jellicent, Lapras, Quagsire, Blastoise |
| Kanto | Lt. Surge | Raichu, Electrode, Magnezone, Electivire, Jolteon, Ampharos |
| Kanto | Erika | Vileplume, Venusaur, Victreebel, Exeggutor, Tangrowth, Bellossom |
| Kanto | Janine | Venomoth, Weezing, Ariados, Crobat, Arbok, Tentacruel |
| Kanto | Sabrina | Alakazam, Hypno, Mr. Mime, Slowking, Espeon, Jynx |
| Kanto | Blaine | Arcanine, Ninetales, Charizard, Magmortar, Flareon, Rapidash |
| Johto | Bugsy | Scizor, Shuckle, Heracross, Pinsir, Forretress, Yanmega |
| Johto | Whitney | Miltank, Wigglytuff, Tauros, Ambipom, Ursaring, Clefable |
| Johto | Morty | Gengar, Mismagius, Banette, Dusknoir, Sableye, Froslass |
| Johto | Chuck | Poliwrath, Machamp, Hitmontop, Hitmonchan, Hitmonlee, Primeape |
| Johto | Jasmine | Steelix, Magnezone, Forretress, Skarmory, Metagross, Mawile |
| Johto | Pryce | Mamoswine, Jynx, Dewgong, Cloyster, Lapras, Weavile |
| Johto | Clair | Dragonite, Kingdra, Altaria, Salamence, Druddigon, Garchomp |
| Hoenn | Wattson | Manectric, Magnezone, Electrode, Plusle, Minun, Raichu |
| Hoenn | Flannery | Torkoal, Camerupt, Magcargo, Blaziken, Houndoom, Magmortar |
| Hoenn | Norman | Slaking, Spinda, Kecleon, Castform, Exploud, Zangoose |
| Hoenn | Winona | Altaria, Pelipper, Swellow, Skarmory, Tropius, Honchkrow |
| Hoenn | Tate | Solrock, Xatu, Chimecho, Grumpig, Gallade, Claydol |
| Hoenn | Liza | Lunatone, Xatu, Chimecho, Grumpig, Gardevoir, Claydol |
| Hoenn | Juan | Kingdra, Walrein, Crawdaunt, Whiscash, Huntail, Gorebyss |
| Sinnoh | Roark | Rampardos, Probopass, Sudowoodo, Onix, Golem, Relicanth |
| Sinnoh | Gardenia | Roserade, Carnivine, Cherrim, Tangrowth, Leafeon, Torterra |
| Sinnoh | Fantina | Mismagius, Drifblim, Spiritomb, Dusknoir, Rotom, Gengar |
| Sinnoh | Maylene | Lucario, Infernape, Toxicroak, Gallade, Medicham, Machamp |
| Sinnoh | Crasher Wake | Floatzel, Empoleon, Lumineon, Gastrodon, Quagsire, Gyarados |
| Sinnoh | Byron | Bastiodon, Steelix, Bronzong, Magnezone, Aggron, Forretress |
| Sinnoh | Candice | Froslass, Abomasnow, Weavile, Glaceon, Mamoswine, Glalie |
| Unova | Burgh | Leavanny, Vespiquen, Crustle, Escavalier, Accelgor, Durant |
| Unova | Elesa | Zebstrika, Ampharos, Galvantula, Emolga, Eelektross, Stunfisk |
| Unova | Clay | Excadrill, Claydol, Krookodile, Seismitoad, Mamoswine, Golurk |
| Unova | Skyla | Swanna, Unfezant, Swoobat, Mandibuzz, Archeops, Braviary |
| Unova | Drayden | Haxorus, Druddigon, Hydreigon, Flygon, Altaria, Salamence |
| Unova | Brycen | Cryogonal, Beartic, Vanilluxe, Weavile, Dewgong, Walrein |

Fontes: [PWT Kanto](https://www.serebii.net/black2white2/pwt/kanto.shtml), [PWT Johto](https://www.serebii.net/black2white2/pwt/johto.shtml), [PWT Hoenn](https://www.serebii.net/black2white2/pwt/hoenn.shtml), [PWT Sinnoh](https://www.serebii.net/black2white2/pwt/sinnoh.shtml) e [PWT Unova](https://www.serebii.net/black2white2/pwt/unova.shtml). Há outra variante ainda mais forte no [World Leaders Tournament](https://www.serebii.net/black2white2/pwt/worldleaders.shtml) para parte dos personagens. Para os irmãos Tate & Liza, o PWT registra escalações próprias de cada um; elas devem permanecer separadas caso a base trate cada personagem individualmente.

### Scarlet/Violet — Blueberry League Club

O conteúdo pós-jogo de *The Indigo Disk* tem outra fonte de equipes completas de seis. Estas formações incluem treinadores paldeanos da tabela que estavam abaixo de seis no Kaggle:

| Treinador | Equipe de seis do League Club |
|---|---|
| Katy | Spidops, Heracross, Forretress, Lokix, Araquanid, Ursaring |
| Brassius | Breloom, Arboliva, Vileplume, Tsareena, Lilligant, Sudowoodo |
| Iono | Kilowattrel, Electrode, Bellibolt, Luxray, Electivire, Mismagius |
| Kofu | Pelipper, Veluza, Feraligatr, Wugtrio, Clawitzer, Crabominable |
| Ryme | Banette, Mimikyu, Golurk, Spiritomb, Houndstone, Toxtricity |
| Tulip | Farigiraf, Gardevoir, Espathra, Gallade, Delphox, Florges |
| Grusha | Ninetales, Beartic, Frosmoth, Cetitan, Weavile, Altaria |
| Rika | Dugtrio, Whiscash, Camerupt, Torterra, Donphan, Clodsire |
| Poppy | Copperajah, Bastiodon, Bronzong, Magnezone, Corviknight, Tinkaton |
| Larry | Tropius, Oricorio, Altaria, Staraptor, Flamigo, (o jogo o registra em times separados de ginásio/Elite Four; usar a escalação correspondente ao papel) |
| Hassel | Duraludon, Noivern, Haxorus, Dragalge, Dragonite, Baxcalibur |

Fonte: [batalhas do League Club](https://www.serebii.net/scarletviolet/leagueclubbattles.shtml). São times do pós-jogo e usam espécies da geração IX, portanto não cabem no catálogo atual até a decisão sobre o limite de geração. Larry tem duas funções na Liga; sua equipe de ginásio e a de Elite Four são registros distintos, não se deve juntar integrantes das duas.

### Outras possibilidades nos jogos — equipes completas já verificadas

O levantamento de jogos cobre equipes de batalha específicas, não uma fusão de todos os Pokémon que um personagem já usou. Há fontes além de *Stadium 2*, PWT e Blueberry League Club. Abaixo estão resultados adicionais confirmados; quando uma batalha não tem seis Pokémon, ela não serve para completar esse registro.

#### HeartGold/SoulSilver — rematches dos líderes

Os rematches do Fighting Dojo oferecem um sexteto para cada líder de Kanto e Johto. A lista inclui variantes próprias, diferentes das equipes de *Stadium 2* e PWT. Linhas relevantes para a seleção atual:

| Treinador | Equipe de rematch em HGSS |
|---|---|
| Falkner | Staraptor, Noctowl, Swellow, Honchkrow, Pelipper, Pidgeot |
| Bugsy | Shedinja, Vespiquen, Pinsir, Heracross, Yanmega, Scizor |
| Whitney | Bibarel, Lickilicky, Clefable, Girafarig, Delcatty, Miltank |
| Morty | Drifblim, Dusknoir, Sableye, Mismagius, Gengar, Gengar |
| Chuck | Medicham, Hitmonchan, Hitmonlee, Breloom, Primeape, Poliwrath |
| Jasmine | Bronzong, Skarmory, Empoleon, Metagross, Magnezone, Steelix |
| Pryce | Abomasnow, Glalie, Froslass, Dewgong, Walrein, Mamoswine |
| Clair | Dragonair, Gyarados, Aerodactyl, Charizard, Kingdra, Dragonite |
| Brock | Golem, Relicanth, Omastar, Kabutops, Rampardos, Onix |
| Misty | Quagsire, Lapras, Lanturn, Floatzel, Milotic, Starmie |
| Lt. Surge | Magnezone, Electrode, Manectric, Electivire, Pachirisu, Raichu |
| Erika | Jumpluff, Victreebel, Bellossom, Shiftry, Roserade, Tangrowth |
| Janine | Ariados, Toxicroak, Weezing, Drapion, Crobat, Venomoth |
| Sabrina | Espeon, Mr. Mime, Jynx, Wobbuffet, Gallade, Alakazam |
| Blaine | Torkoal, Camerupt, Rapidash, Magcargo, Houndoom, Magmortar |

Fonte: [rematches de líderes em HGSS](https://www.serebii.net/heartgoldsoulsilver/gym-rematch.shtml). Blue também tem rematch de seis nessa página; os Pokémon dependem do inicial do jogador, então a variante precisa ser registrada separadamente.

#### Omega Ruby/Alpha Sapphire — rematches da Elite Four

Os rematches pós-jogo elevam os times de Sidney, Phoebe, Glacia e Drake a seis integrantes. Para Phoebe, Glacia e Drake, algumas espécies repetem dentro do time; isso reflete a composição do jogo e deve ser preservado.

| Treinador | Equipe de rematch em ORAS |
|---|---|
| Sidney | Scrafty, Shiftry, Sharpedo, Zoroark, Mandibuzz, Absol |
| Phoebe | Banette, Mismagius, Drifblim, Chandelure, Dusknoir, Sableye |
| Glacia | Abomasnow, Beartic, Froslass, Vanilluxe, Walrein, Glalie |
| Drake | Altaria, Dragalge, Kingdra, Flygon, Haxorus, Salamence |

Fonte: [Elite Four e rematches de ORAS](https://www.serebii.net/omegarubyalphasapphire/elitefour.shtml).

#### Brilliant Diamond/Shining Pearl — rematches avançados da Elite Four

O terceiro encontro da Liga pós-jogo usa sextetos para membros que começam com cinco Pokémon. Exemplos confirmados para integrantes do recorte:

| Treinador | Equipe de rematch avançado em BDSP |
|---|---|
| Aaron | Yanmega, Scizor, Vespiquen, Heracross, Flygon, Drapion |
| Bertha | Whiscash, Gliscor, Nidoking, Hippowdon, Mamoswine, Rhyperior |

Fonte: [rematches de Elite Four em BDSP](https://www.serebii.net/brilliantdiamondshiningpearl/elitefour.shtml). A mesma página distingue a primeira luta, o primeiro rematch de cinco e o rematch mais forte de seis; deve-se salvar a variante correta.

#

#### Escalações completas da checagem final que faltavam no seed

A conversa já havia confirmado estas três escalações oficiais, mas elas não tinham sido importadas. Agora estão cadastradas como variantes ativas próprias, sem alterar os registros Kaggle parciais:

| Treinador | Jogo/batalha | Equipe | Fonte |
|---|---|---|---|
| Agatha | Rematch da Elite Four em Let's Go | Arbok, Gengar, Golbat, Weezing, Marowak, Gengar | [Serebii — Let's Go Elite Four](https://www.serebii.net/letsgopikachueevee/elitefour.shtml) |
| Lorelei | Rematch da Elite Four em Let's Go | Dewgong, Jynx, Cloyster, Slowbro, Sandslash, Lapras | [Serebii — Let's Go Elite Four](https://www.serebii.net/letsgopikachueevee/elitefour.shtml) |
| Tate & Liza | Quarto rematch do ginásio em Emerald, batalha em dupla | Hypno, Claydol, Slowking, Xatu, Lunatone, Solrock | [Serebii — Match Call](https://www.serebii.net/emerald/entrycall/lizatate.shtml) |

### Platinum — rematches de líderes não completam seis

Também verifiquei o restaurante de rematches de *Platinum*. Os líderes ali usam cinco Pokémon cada, não seis. Esses rematches são variantes oficiais úteis para histórico, mas não completam um sexteto e não devem ser misturados com Pokémon de outras batalhas. Fonte: [rematches dos líderes em Platinum](https://www.serebii.net/platinum/gym-rematches.shtml).

#### Ultra Sun/Ultra Moon — desafiantes da Liga

Além dos rematches da Elite Four, a cadeira de Campeão pode trazer desafiantes. Kukui e Gladion têm sextetos; Guzma aparece com cinco Pokémon nessa batalha, portanto não é uma equipe completa de seis. Esses são treinadores extras para a seleção, caso o recorte de 100 seja revisto.

| Treinador | Equipe documentada em USUM |
|---|---|
| Professor Kukui | Lycanroc, Ninetales, Braviary, Magnezone, Snorlax e um inicial final variável |
| Guzma | Golisopod, Vikavolt, Pinsir, Masquerain, Scizor (5/6 nessa batalha) |
| Gladion | Crobat, Zoroark, Porygon-Z, Lucario, inicial de Kanto variável, Silvally |

Correção de escopo: a tabela do jogo precisa ser transcrita por variante e conferida linha a linha antes de inserir no catálogo. As páginas mostram a seleção de inicial para Kukui/Gladion e rematches separados; não se deve fixar uma variante omitindo essa dependência. Fonte: [Elite Four, rematches e desafiantes de USUM](https://www.serebii.net/ultrasunultramoon/elitefour.shtml).

#### Outras famílias de jogos que fazem parte do levantamento

Estas fontes também serão verificadas contra os 100 selecionados e contra os personagens adicionais aprovados:

- *Platinum*: rematches próprios dos líderes de Sinnoh; verificados como equipes de cinco, então não completam sexteto.
- *Black 2/White 2*: torneios regionais do PWT e World Leaders; o PWT já está listado acima, mas World Leaders oferece outras variantes.
- *Brilliant Diamond/Shining Pearl*: rematches progressivos da Elite Four e Cynthia, com equipes melhoradas em etapas; os sextetos avançados de Aaron e Bertha já foram transcritos acima.
- *Sword/Shield*: Champion Cup rematches e Galarian Star Tournament; torneios em dupla podem ter condições/formações diferentes de um sexteto individual.
- *Scarlet/Violet*: Gym Leader rematches, Academy Ace Tournament e Blueberry League Club; a fonte do League Club já está listada acima.
- Jogos spin-off (*Stadium*, *Stadium 2*, *Battle Revolution*, *Pokémon Masters EX*): registrar apenas quando a batalha especificar uma equipe jogável fixa. Equipes de aluguel, equipes aleatórias ou formações de gameplay não atribuídas ao personagem não contam como escalação canônica.

O índice de rematches HGSS confirma que a lista cobre os líderes de Johto e Kanto; a página de ORAS distingue a equipe inicial da equipe de rematch; e a página de USUM lista separadamente membros da Elite Four e desafiantes. Referências detalhadas: [HGSS](https://www.serebii.net/heartgoldsoulsilver/gym-rematch.shtml), [ORAS](https://www.serebii.net/omegarubyalphasapphire/elitefour.shtml), [USUM](https://www.serebii.net/ultrasunultramoon/elitefour.shtml), [Platinum rematches](https://www.serebii.net/platinum/gym.shtml), [PWT World Leaders](https://www.serebii.net/black2white2/pwt/worldleaders.shtml), [BDSP Elite Four](https://www.serebii.net/brilliantdiamondshiningpearl/elitefour.shtml), [Sword/Shield Champion Cup rematches](https://www.serebii.net/swordshield/championcuprematch.shtml), [Galarian Star Tournament](https://www.serebii.net/swordshield/galarianstartournament.shtml), [Scarlet/Violet rematches](https://www.serebii.net/scarletviolet/gymrematches.shtml) e [Blueberry League Club](https://www.serebii.net/scarletviolet/leagueclubbattles.shtml).

### Anime — como contar sem inventar um time

O anime não segue a regra de seis Pokémon por treinador. Líderes podem ajustar o número ao desafiante, e personagens podem usar Pokémon diferentes em episódios distintos. Por isso, “Pokémon que já pertenceu ao personagem” é um inventário de propriedade, não uma escalação de batalha. Para este projeto, só serve como equipe completa um confronto identificável em que os seis integrantes foram efetivamente usados/inscritos; capturas e aparições de episódios diferentes ficam como variantes separadas, nunca somadas automaticamente.

O índice de personagens do anime mostra que há outros líderes e substitutos exclusivos da animação — por exemplo, Flint, Lola e Forrest no Ginásio de Pewter, Daisy/Violet/Lily no de Cerulean, Visquez substituindo Surge, e Agatha atuando temporariamente no Ginásio de Viridian. Eles podem ser candidatos à ampliação do recorte, mas não devem ser confundidos com a escalação de jogo dos 100 personagens. O mesmo índice descreve o anime de Sinnoh como exceção em que os líderes usaram as mesmas equipes dos jogos; mesmo assim, há batalhas em que nem todos foram utilizados. Fonte de navegação: [Gym leaders — seções de jogos e animação](https://bulbapedia.bulbagarden.net/wiki/Gym_leaders). Para localizar os Pokémon mostrados em batalha, usar biografias e guias por episódio, por exemplo [Serebii character bios](https://www.serebii.net/anime/characters/) e [guia de equipes de líderes/frontier brains no anime](https://bulbapedia.bulbagarden.net/wiki/User:Minibug/Gym_Leader_and_Frontier_Brain_Pok%C3%A9mon_teams_in_the_anime), depois confirmar cada escalação nos episódios correspondentes.

O levantamento anime já confirmou confrontos de seis contra seis para Gary vs. Ash, Paul vs. Ash na Liga de Sinnoh e Alain vs. Ash na Liga de Kalos (listados em “Novos personagens aprovados”). Para Red, *Origins* e os jogos são continuidades diferentes. O elenco completo de Pokémon capturados por Ash, Misty, Brock e demais recorrentes não será convertido em equipe de seis sem uma batalha específica que sustente essa composição.

### Novos personagens aprovados para acrescentar

Os personagens abaixo foram aprovados para entrar na seleção. Quando há um time mostrado em uma batalha específica, essa formação deve virar um registro separado; não se deve misturar outros Pokémon do personagem para preencher seis.

| Personagem | Escalação de referência encontrada | Observação |
|---|---|---|
| Red | *Pokémon Origins*, batalha final contra Blue: Jolteon, Scyther, Lapras, Dodrio, Persian e Charizard | É a formação ligada à batalha final de *Origins*. A equipe de Red em HGSS é outra: Pikachu, Snorlax, Venusaur, Charizard, Blastoise e Lapras. [Origins](https://bulbapedia.bulbagarden.net/wiki/Red_(Origins)); [HGSS](https://www.serebii.net/heartgoldsoulsilver/red.shtml). |
| Ash | Final do Masters Eight: Pikachu, Dragonite, Gengar, Lucario, Sirfetch’d e Dracovish | É a equipe usada na batalha que o torna Campeão Mundial; inclui espécies da geração VIII. [Pokémon.com](https://www.pokemon.com/uk/animation/seasons/25/episode-38-partners-in-time). |
| Gary | Batalha 6 contra 6 contra Ash na Conferência de Prata: Nidoqueen, Magmar, Blastoise, Arcanine, Scizor e Golem | Sexteto confirmado na batalha dos episódios *The Ties That Bind!* e *Can’t Beat the Heat!*; não inclui Umbreon, que Gary usa em outras aparições. [Episódio 1](https://www.pokemon.com/us/animation/seasons/5/episode-59-the-ties-that-bind); [episódio 2](https://www.serebii.net/anime/epiguide/johto/272.shtml). |
| Paul | Liga de Sinnoh contra Ash: Aggron, Gastrodon, Drapion, Ninjask, Froslass e Electivire | Sexteto confirmado para essa batalha. [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/DP186); [Serebii](https://www.serebii.net/anime/characters/paul.shtml). |
| Alain | Final da Liga de Kalos contra Ash: Tyranitar, Weavile, Bisharp, Unfezant, Metagross e Charizard | Sexteto confirmado para essa batalha. [Serebii](https://www.serebii.net/anime/characters/alain.shtml). |
| N | Batalha final de *Black/White*: Carracosta, Vanilluxe, Archeops, Zoroark, Klinklang e o lendário da versão | A sexta espécie muda conforme a versão: **Zekrom em Black** e **Reshiram em White**. [Pokémon Database](https://pokemondb.net/black-white/gymleaders-elitefour). |
| Silver | Rival de Johto | O time de seis depende do inicial escolhido pelo jogador e da versão/batalha. Registrar uma variante específica, sem fundir as três. |
| Nemona | Batalha final de *Scarlet/Violet*: Lycanroc, Pawmot, Dudunsparce, Orthworm, Goodra e a evolução final do inicial que tem vantagem contra o inicial do jogador | A última vaga muda conforme a escolha inicial. Espécies da geração IX, fora do catálogo atual do projeto. [GameWith](https://gamewith.net/pokemon-scarletviolet/article/show/36186). |
| Volo | *Legends: Arceus*: Spiritomb, Roserade, Togekiss, Lucario, Garchomp e Hisuian Arcanine | Giratina aparece em uma fase seguinte da luta como chefe; não é a sétima vaga do time. Hisuian Arcanine é uma forma regional da geração VIII. [Nintendo Life](https://www.nintendolife.com/guides/pokemon-legends-arceus-volo-how-to-defeat-volo). |

### Leitura recomendada para a seleção

- Para preencher o objetivo de ter seis opções em batalhas, podemos cadastrar os times completos de *Stadium 2* como **equipes alternativas do mesmo treinador**, mantendo intactos os times já selecionados no Kaggle.
- Para Red, Ash, Gary, Paul, Alain, N, Nemona e Volo, os times da tabela acima são escalações de confrontos específicos e têm uma fonte canônica clara.
- Silver ainda precisa de uma variante definida: os times dele nos jogos variam conforme o inicial escolhido e a batalha.
- A equipe de Ash no Masters Eight, a de Nemona e a de Volo ultrapassam a Pokédex da geração VII decidida para o projeto. Devem ficar marcadas como incompatíveis com o catálogo atual até decidirmos ampliar esse limite ou excluir as espécies fora dele.
- Nenhum Pokémon foi escolhido por autocomplete. Cada espécie precisa estar na escalação daquele jogo, versão ou batalha indicada.

## Complementos manuais aprovados para equipes com 1 ou 2 vagas

Os acréscimos abaixo foram aprovados para manter o tema dos times. Quando vêm de outra aparição oficial, a equipe final continua sendo uma composição manual baseada na equipe selecionada do Kaggle; não representa necessariamente um sexteto usado junto numa batalha. Escolhas temáticas estão identificadas como tal.

| Treinador | Pokémon adicionados | Base do complemento |
|---|---|---|
| Drasna | Goodra, Drampa | Escolhas temáticas de Dragão; não há uso confirmado no levantamento. |
| Malva | Houndoom, Magmortar | Houndoom aparece no anime; Magmortar é temático. [Serebii](https://www.serebii.net/anime/characters/malva.shtml) |
| Siebold | Blastoise, Kingdra | Blastoise aparece no anime; Kingdra é temático. [Serebii](https://www.serebii.net/anime/characters/siebold.shtml) |
| Wikstrom | Escavalier, Honedge | Aparições associadas a Wikstrom no anime. [Bulbapedia, EP1141](https://bulbapedia.bulbagarden.net/wiki/EP1141) |
| Acerola | Banette | Equipe alternativa de Acerola como Elite Four em Ultra Sun/Ultra Moon. [Serebii](https://www.serebii.net/ultrasunultramoon/elitefour.shtml) |
| Hala | Machamp | Escolha temática de Lutador; uso não confirmado no levantamento. |
| Hapu | Golurk, Krookodile | Golurk aparece em Ultra Sun/Ultra Moon; Krookodile é temático e substituiu Garchomp por decisão do usuário. [Serebii](https://www.serebii.net/ultrasunultramoon/grandtrials.shtml) |
| Kahili | Hawlucha | Aparece em outra equipe oficial de Kahili em Ultra Sun/Ultra Moon. [Serebii](https://www.serebii.net/ultrasunultramoon/elitefour.shtml) |
| Olivia | Anorith | Usado por Olivia no Grande Teste de Sun/Moon. [Serebii](https://www.serebii.net/sunmoon/grandtrials.shtml) |
| Sophocles | Raichu de Alola | Escolha temática Elétrica de Alola; Charjabug não foi adicionado junto de Vikavolt. |

A lista anterior dos 100 mantém os times originais do dataset para referência; a composição importada e a justificativa dos acréscimos estão em `elenco_aprovado.json`.
