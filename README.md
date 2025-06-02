# HSR Gacha Calculator

## Usage
```
usage: gacha.py pulls route [-h] [-cp CHARACTER_PITY] [-lp LIGHTCONE_PITY]
                [-cg] [-lg] [-d DIGIT]

HSR Gacha Probability Calculator

positional arguments:
  pulls
  route                 Order (C: Character, L: Lightcone).
                        For example if you want E0 -> S1 -> E2: "CLCC" or "CLC2"

options:
  -h, --help            show this help message and exit
  -cp CHARACTER_PITY, --character_pity CHARACTER_PITY
  -lp LIGHTCONE_PITY, --lightcone_pity LIGHTCONE_PITY
  -cg, --character_guaranteed
  -lg, --lightcone_guaranteed
  -d DIGIT, --digit DIGIT
```

## Example
```bash
python gacha.py 700 CLC6L4 -cp 10 -lp 50 -cg
# CLC6L4 = CLCCCCCCLLLL
```
Output
```
Target: E6S5, Probability: 7.4903%
Distribution:
E3S1: 0.2357%
E4S1: 4.8340%
E5S1: 18.8921%
E6S1: 21.3022%
E6S2: 21.4154%
E6S3: 16.1961%
E6S4: 9.6342%
E6S5: 7.4903%
```
