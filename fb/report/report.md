# REPORT

## Personal Information
- Student Name: Leo Zhang
- Student ID: 20755564
- WatID: l536zhan

## What have been done to compile and run the code
I download docker

I ran docker docker run -dit --name FuzzDoom uwstqam/fuzz-doom

I access docker environment docker exec -it FuzzDoom /bin/bash

I Build Chocolate-Doom and the fuzzing target

Below is my code

```shell 
git clone https://git.uwaterloo.ca/stqam-1245/class/l536zhan.git stqam

cd stqam/fb
git clone https://git.uwaterloo.ca/stqam-1245/chocolate-doom.git
mkdir build ; cd build
cmake -DCMAKE_C_COMPILER=clang-10 -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  -DCMAKE_C_FLAGS='-fsanitize=fuzzer-no-link,address -fprofile-instr-generate -fcoverage-mapping -g -ggdb3 -O2' \
  ../ -GNinja
ninja
```

## What have been done to increase the coverage
I disable leak detection and set the fuzzer profile output format.

To increase coverage, I downloaded Simulacrum.wad,stn-flwr20x6.wad and stone-flower.wad from https://www.doomworld.com/idgames/. 

I imported them into a folder called SEED. I created a folder called CORPUS. After the build step is done, i ran with the following commands

More details in comments below

```shell
export ASAN_OPTIONS=detect_leaks=0 
#set the fuzzer profile output format
export LLVM_PROFILE_FILE='pf-%p' 
#run the target in parallel. This will run 8 fuzz jobs in parallel, restrict each run to 10 iterations, and 
#overall will run 100 jobs, using the seed folder SEED in fb, and the corpus folder CORPUS in fb
./src/doom_fuzz -runs=10  ../CORPUS ../SEED -jobs=100 -workers=8 -detect_leaks=0 >/dev/null
#check if we have generated any profile files
ls pf-*
#you should see few files like pf-2044576, etc.
# collect all the prof file paths into a single file
ls pf-* > all_prof_files
# merge all prof files into a single file 
llvm-profdata-10 merge -sparse -f all_prof_files -o default.profdata
# export the above file into a format that can be easily parsed
llvm-cov-10 export ./src/doom_fuzz -instr-profile=default.profdata -format=lcov > src.info
# generate text report
lcov -a src.info -o src_report.info
# generate a html visualization of the same report
genhtml -o html_output src_report.info
```
I am able to have coverage of above 80 for lines in both chocolate-doom/src/doom/p_setup.c and chocolate-doom/src/w_wad.c
## What bugs have been found? Can you replay the bug with chocolate-doom, not with the fuzz target?
No bugs have been found
## Did you manage to compile the game and play it on your local machine (Not inside Docker)?
yes
