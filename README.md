# itg-konecna
Textová adventura v Pythonu odehrávající se v pražském metru. Čtvrtletní projekt z informatiky.

Vytvořil **Oliver Steiner**.

## Spuštění

```
python3 main.py
```

Stačí čistý Python 3, žádné knihovny se instalovat nemusí. Hra používá barvy a mazání obrazovky, takže ji spouštěj v normálním terminálu (macOS, Linux, Windows Terminal nebo terminál ve VS Code).

## O hře

Probudíš se na lavičce na konečné. Poslední vlak už odjel, stanice je zamčená, proud nejde a v tunelech je něco špatně. Musíš se dostat ven, dokud ti nedojde světlo.

- **Cíl**: pod popisem místa vždycky vidíš řádek CÍL, který ti poradí, co dál.
- **Světlo**: každá cesta do tmavého místa vybije svítilnu o 10 %. Začínáš se 70 %. Když jdeš do tmy s vybitou svítilnou, něco tě tam chytí. Po zapnutí proudu je všude světlo.
- **Inventář**: uneseš jen 6 věcí. Když máš plné ruce, spoj některé věci dohromady.
- **Konce**: hra má 3 různé konce a jednu prohru.

## Ovládání

Hra vypíše očíslovaný seznam toho, co můžeš udělat. Napiš číslo a zmáčkni Enter. Když napíšeš něco špatně, hra se jen zeptá znovu.

Hru ukončíš volbou **Ukončit hru** a potvrzením `a`. Novou hru začneš tak, že spustíš `main.py` znovu.

## Konce

> Pozor, spoilery!

1. **Hlavní východ** (nejlepší konec): oprav pojistku, vlož ji v dispečinku do skříně a ve vestibulu zmáčkni tlačítko u rolety.
2. **Další stanice**: spoj lano a hák na kotvičku a v zavaleném tunelu vylez přes suť. Dojdeš tunelem do další stanice, kde tě čeká nepříjemné překvapení.
3. **Konečná**: v zavaleném tunelu vypáčíš páčidlem poklop a nastoupíš do tajemného vlaku. Všechno začne znovu na lavičce.
4. **Prohra - tma**: když jdeš do tmavého místa s vybitou svítilnou, něco tě ve tmě chytí.
