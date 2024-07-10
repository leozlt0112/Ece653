# REPORT

## Personal Information
- Student Name: Letian Zhang
- Student ID: 20755564
- WatID: l536zhan

## What have been done to compile and run the code
I download docker
I ran docker docker run -dit --name FuzzDoom uwstqam/fuzz-doom
I access docker environment docker exec -it FuzzDoom /bin/bash
I Build Chocolate-Doom and the fuzzing target
    """git clone https://git.uwaterloo.ca/stqam-1245/class/USER.git stqam
        cd stqam/fb
        git clone https://git.uwaterloo.ca/stqam-1245/chocolate-doom.git
    mkdir build ; cd build
    cmake -DCMAKE_C_COMPILER=clang-10 -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
      -DCMAKE_C_FLAGS='-fsanitize=fuzzer-no-link,address -fprofile-instr-generate -fcoverage-mapping -g -ggdb3 -O2' \
      ../ -GNinja
    ninja
    """
I Generate the coverage report and disabled leak detection

## What have been done to increase the coverage
To increase coverage, I downloaded Simulacrum.wad from https://www.doomworld.com/idgames/ and imported it into a new_corpus folder. i also modifed fuzz_target.c to add the following code
line 217:   W_Reload();
line 223 to 236 char *filename2 = "~fuzz.wad";

  DEH_printf("Fuzzing with file: %s\n", filename2);
  if (!W_AddFile(filename2))
  {
    return 0;
  }
  char *filename3 = "~fuzz";

  DEH_printf("Fuzzing with file: %s\n", filename3);
  if (!W_AddFile(filename3))
  {
    return 0;
  }
The above code increase coverage for chocolate-doom/src/w_wad.c


## What bugs have been found? Can you replay the bug with chocolate-doom, not with the fuzz target?
No bugs have been found
## Did you manage to compile the game and play it on your local machine (Not inside Docker)?
yes
