#!/usr/bin/env python3
"""
Solver for CTF Challenge: i_am_scared (h4ckc0n 2026)
Cipher: Book cipher using official SCP Foundation Series 1 titles.
"""

SCP_TITLES = {
    839: "Candied Worms",
    479: "Hallway 4, D-Class Dorms, Site 14",
    317: "Cretaceous Physicist",
    275: "Ironskin",
    937: "Walking Sticks",
    344: "Schrödinger's Can Opener",
    320: "Higgs Field Acceleration Manipulator",
    173: "The Sculpture - The Original",
    370: "A Key",
    712: "The Impossible Colors",
    335: 'One Hundred and Fifty 3.5" Floppy Disks',
    214: "Hemotopian Virus",
    898: "Memetic Counter-Agent",
    180: "Identity-Thieving Hat",
    334: "Stellar Vulpine",
    103: "Rhys' Head / Mara's Heart",
    296: "Armed Containment Site-03",
    420: "Aggressive Skin Condition",
    806: "Resurrection Projection",
    948: "The Workaholic",
    178: '"3-D" Specs',
    536: "Physical Quirks",
    838: "The Dream Job",
    551: "Impossible Puzzle",
    111: "Dragon-Snails",
    443: "Thought-streaming Crayons",
    24: "Game Show of Death",
    347: "The Invisible Woman",
    494: "Matter Transference Gloves",
    998: "Missing Aircraft",
    429: "Clockwork Teleporter",
    332: "The 1976 Kirk Lonwood High School Marching Band",
    678: "Trauma Harvester",
    434: "A Meeting with Myself",
    31: "What is Love?",
}


def main() -> None:
    with open("scary.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    chars = []
    cant_count = 0
    total_cant = sum(1 for line in lines if "<cant_find_letter>" in line)

    for line in lines:
        if "<cant_find_letter>" in line:
            cant_count += 1
            if cant_count == 1:
                chars.append("{")
            elif cant_count == total_cant:
                chars.append("}")
            else:
                chars.append("_")
        else:
            num_str, rest = line.split("[")
            scp_num = int(num_str)
            index = int(rest.rstrip("]"))
            chars.append(SCP_TITLES[scp_num][index])

    flag = "".join(chars)
    print("Flag:", flag)


if __name__ == "__main__":
    main()
